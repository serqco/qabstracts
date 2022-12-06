import dataclasses
import math
import re
import typing as tg
from numbers import Number

import qabs.metadata
import qabs.annotations as annot

usage = """Splits each annotated file into one record per coding.
  Knows how to compute sentence lengths and how to split them among multiple codes where needed.
  Unavailable number values will be NA (for use with R).
  Prints resulting tab-separated values file on stdout.
"""

NAN_VALUE = "NA"  # R's "not available" value

def configure_argparser(subparser):
    subparser.add_argument('workdir',
                           help="Directory where metadata and abstracts.?/* live")

@dataclasses.dataclass
class Abstract:
    filename: str
    citekey: str
    venue: str
    volume: str
    coder_letter: str
    coder: str
    annots: annot.Annotations  # for convenience
    codebook: annot.Codebook  # for convenience


def export(workdir: str):
    annots = annot.Annotations()
    venue = qabs.metadata.Venue(workdir)
    what = qabs.metadata.WhoWhat(workdir)
    prt_head()
    for coder in sorted(what.coders):
        for file in what.files_of(coder):
            citekey = what.citekey(file)
            abstract = Abstract(filename=file, citekey=citekey, 
                                venue=venue.venue_of(citekey), volume=venue.volume_of(citekey),
                                coder_letter=what.coder_letter(file), coder=coder, 
                                annots=annots, codebook=annots.codebook)
            export_for_file(file, abstract)


def export_for_file(filename: str, abstract: Abstract):
    with open(filename, 'rt', encoding='utf8') as f:
        content = f.read()
    for i, pair in enumerate(abstract.annots.find_all_sentence_and_annotation_pairs(content)):
        sentence, annotation = pair
        process_sentence(i+1, sentence, annotation, abstract)


def process_sentence(idx: int, sentence: str, annotation: str, abstract: Abstract):
    """
    Print one or possibly several records for one pair of sentence and annotation.
    Decides which codings to report at all, how to split word count and char count among them,
    and how to determine icount and ucount. 
    """
    H_LEN = 10  # assumed number of chars corresponding to a h-* coding if there are multiple codings
    sentence2 = _unlinebreak(sentence)
    words = _count_words(sentence2)
    chars = len(sentence2)
    codings = set(abstract.annots.split_into_codings(annotation)) - set([abstract.codebook.IGNORECODE])  # forget IGNORECODEs
    codes_done = set(abstract.codebook.GARBAGE_CODES)  # consider them done right from the start
    multiple = len(codings) > 1  # whether there are multiple codings at this sentence
    #----- process extra codes (which involve no length):
    for code, csuffix in codings:
        if code not in codes_done and abstract.codebook.is_extra_code(code):
            codes_done.add(code)
            prt_record(abstract, idx, words, chars, 
                       abstract.annots.bare_codename(code), _topic(code), math.nan, math.nan)
    #----- process h-* codes (which count only 1 word):
    for code, csuffix in codings:
        if code not in codes_done and abstract.codebook.is_heading_code(code):
            codes_done.add(code)
            prt_record(abstract, idx, 
                       1 if multiple else words , H_LEN if multiple else chars, 
                       abstract.annots.bare_codename(code), _topic(code), 0, 0)
    words -= len(codes_done)
    chars -= H_LEN * len(codes_done)  # the approximation matters only if there are unprocessed codings left
    remaining = len(codings) - len(codes_done)
    if remaining > 1:
        words = words / remaining  # split length equally among remaining codes, an assumption!
        chars = chars / remaining  # ditto
    #----- process remaining codes with no IU suffix:
    for code, csuffix in codings:
        if code not in codes_done and not csuffix:
            codes_done.add(code)
            prt_record(abstract, idx, words, chars, 
                       code, _topic(code), 0, 0)
    #----- process remaining codes with explicit or implicit IU suffix:
    for code, csuffix in codings:
        if code not in codes_done:
            codes_done.add(code)
            assert abstract.codebook.exists_with_suffix(code)
            icount, ucount = abstract.annots.split_suffix(csuffix)
            prt_record(abstract, idx, words, chars, 
                       code, _topic(code), icount, ucount)


def prt_head():
    """Print header line for output file. Corresponds to prt_record."""
    prt("citekey\tvenue\tvolume\tcoder\tcodername")
    prt("sidx\twords\tchars")
    prt("code\ttopic\ticount\tucount", end_line=True)


def prt_record(a: Abstract, idx: int, words: Number, chars: Number,
               code: str, topic: str, icount: Number, ucount: Number):
    prt(f"{a.citekey}\t{a.venue}\t{a.volume}\t{a.coder_letter}\t{a.coder}")  # file-related
    prt(f"{idx}\t{_numberish(words)}\t{_numberish(chars)}")  # sentence-related
    prt(f"{code}\t{topic}\t{_numberish(icount)}\t{_numberish(ucount)}", end_line=True)  # coding-related


def prt(value: tg.Any, end_line=False):
    print(value, end='\n' if end_line else '\t')


def _count_words(s: str) -> int:
    spaces = re.findall(r"\s+", s)
    return len(spaces)  # how many groups of one-or-more blanks


def _numberish(val) -> str:
    """Provide formatted string for value which may be int or NaN or a float that needs rounding."""
    if math.isnan(val):
        return NAN_VALUE
    elif isinstance(val, int):
        return str(val)
    else:
        return "%.1f" % val


def _topic(code: str) -> str:
    """Code group, for a coarser analysis."""
    topics = ('background', 'objective', 'design', 'method', 'result', 'conclusion')
    for topic in topics:
        if code in _triple(topic):
            return topic
    if code.startswith('-'):
        return 'none'  # auxiliary codes have the 'none' topic
    return 'other'  # all other proper codes form one group


def _triple(basecode: str) -> str:
    return f"h-{basecode}", f"a-{basecode}", basecode


def _unlinebreak(s: str) -> str:
    """Dehyphenate words and replace normal line breaks by blanks."""
    return s.replace("-\n", "").replace("\n", " ")  # will a hyphen _always_ come out as an ASCII dash?