import dataclasses
import math
import typing as tg
from numbers import Number

import qscript.annotations as annot
import qscript.metadata
import qscript

import qabs.annotations_abs as annota

NAN_VALUE = "NA"  # R's "not available" value
meaning = """Splits each annotated file into one record per coding.
  Knows how to compute sentence lengths and how to split them among multiple codes where needed.
  Unavailable number values will be NA (for use with R).
  Prints resulting tab-separated values file on stdout.
"""


def add_arguments(subparser: qscript.ArgumentParser):
    subparser.add_argument('workdir',
                           help="Directory where metadata and abstracts.?/* live")


def execute(args: qscript.Namespace):
    annots = annota.AnnotationsAbstracts()
    venue = qscript.metadata.Venue(args.workdir)
    what = qscript.metadata.WhoWhat(args.workdir)
    prt_head()
    for coder in sorted(what.coders):
        for file in what.files_of(coder):
            citekey = what.citekey(file)
            abstract = Abstract(filename=file, citekey=citekey,
                                venue=venue.venue_of(citekey), volume=venue.volume_of(citekey),
                                coder_letter=what.coder_letter(file), coder=coder,
                                annots=annots, codebook=annots.codebook)
            export_for_file(file, abstract)


@dataclasses.dataclass
class Abstract:
    filename: str
    citekey: str
    venue: str
    volume: str
    coder_letter: str
    coder: str
    annots: annota.AnnotationsAbstracts  # for convenience
    codebook: annota.CodebookAbstracts  # for convenience


def export_for_file(filename: str, abstract: Abstract):
    with open(filename, 'rt', encoding='utf8') as f:
        content = f.read()
    for i, annot_sentence in enumerate(abstract.annots.find_all_sentence_and_annotation_pairs(content)):
        process_sentence(i + 1, annot_sentence, abstract)


def process_sentence(idx: int, annot_sentence: annot.AnnotatedSentence, abstract: Abstract):
    """
    Print one or possibly several records for one pair of sentence and annotation.
    Decides which codings to report at all, how to split word count and char count among them,
    and how to determine icount and ucount.
    """
    H_LEN = 10  # assumed number of chars corresponding to a h-* coding if there are multiple codings
    words = annot_sentence.words
    chars = annot_sentence.chars
    syllables = annot_sentence.syllables
    readability = annot_sentence.fk_readability  # counted N times for N-fold encodings
    no_readability = math.nan  # what should not be included in the total abstract average
    codings = (set(abstract.annots.split_into_codings(annot_sentence.annotation)) -
               {abstract.codebook.IGNORECODE})  # forget IGNORECODEs
    codes_done = set(abstract.codebook.GARBAGE_CODES)  # consider them done right from the start
    multiple = len(codings) > 1  # whether there are multiple codings at this sentence
    # ----- process extra codes (which involve no length):
    for code, csuffix in codings:
        if code not in codes_done and abstract.codebook.is_extra_code(code):
            codes_done.add(code)
            prt_record(abstract, idx,
                       math.nan, math.nan, math.nan, no_readability,
                       abstract.annots.bare_codename(code), csuffix, abstract.codebook.topic(code), 
                       math.nan, math.nan)
    # ----- process h-* codes (which count only 1 word):
    for code, csuffix in codings:
        if code not in codes_done and abstract.codebook.is_heading_code(code):
            codes_done.add(code)
            prt_record(abstract, idx,
                       1 if multiple else words,
                       H_LEN if multiple else chars,
                       math.nan, no_readability,
                       abstract.annots.bare_codename(code), csuffix, abstract.codebook.topic(code), 
                       0, 0)
            words -= 1
            chars -= H_LEN
    remaining = len(codings) - len(codes_done) + len(set(abstract.codebook.GARBAGE_CODES))
    if remaining > 1:
        words = words / remaining         # split length equally among remaining codes, an assumption!
        chars = chars / remaining         # ditto
        syllables = syllables / remaining # ditto
    # ----- process remaining codes with no IU suffix:
    # ----- process remaining codes with explicit or implicit IU suffix:
    for code, csuffix in codings:
        if code not in codes_done:
            codes_done.add(code)
            if csuffix:
                assert abstract.codebook.can_have_iu_suffix(code)
                icount, ucount = abstract.annots.get_iu_counts(csuffix)
            else:
                icount, ucount = 0, 0
            prt_record(abstract, idx, words, chars, syllables, readability,
                       code, csuffix, abstract.codebook.topic(code), 
                       icount, ucount)

def prt_head():
    """Print header line for output file. Corresponds to prt_record."""
    prt("citekey\tvenue\tvolume\tcoder\tcodername")
    prt("sidx\twords\tchars\tsyllables\tfkscore")
    prt("code\tsuffixes\ttopic\ticount\tucount", end_line=True)


def prt_record(a: Abstract, idx: int, words: Number, chars: Number, syllables: Number, fkscore: Number,
               code: str, suffixes: str, topic: str, icount: Number, ucount: Number):
    prt(f"{a.citekey}\t{a.venue}\t{a.volume}\t{a.coder_letter}\t{a.coder}")  # file-related
    prt(f"{idx}\t{_numberish(words)}\t{_numberish(chars)}\t{_numberish(syllables)}\t{_numberish(fkscore)}")  # sentence-related
    prt(f"{code}\t{suffixes}\t{topic}\t{_numberish(icount)}\t{_numberish(ucount)}", end_line=True)  # coding-related


def prt(value: tg.Any, end_line=False):
    print(value, end='\n' if end_line else '\t')


def _numberish(val) -> str:
    """Provide formatted string for value which may be int or NaN or a float that needs rounding."""
    if math.isnan(val):
        return NAN_VALUE
    elif isinstance(val, int):
        return str(val)
    else:
        return "%.1f" % val
