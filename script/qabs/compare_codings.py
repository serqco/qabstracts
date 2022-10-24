import re
import sys
import typing as tg

import qabs.metadata
import qabs.annotations as annot

usage = """Compares annotations between coders and flags discrepancies.
  Knows about the maximum allowed IU count difference.
  Knows about codes for silencing discrepancies.
  Reports problems on stdout.
"""

IGNORE = '-ignorediff'  # code that signals not to report coding differences

def configure_argparser(subparser):
    subparser.add_argument('workdir',
                           help="Directory where sample-who-what.txt and abstracts.?/* live")
    subparser.add_argument('--maxcountdiff', type=int, default=2,
                           help="how much the smaller IU count may be smaller without a message")


def compare_codings(maxcountdiff: int, workdir: str):
    msgcount = 0
    what = qabs.metadata.WhoWhat(workdir)
    annots = annot.Annotations()
    for coder in sorted(what.coders):
        print(f"\n\n#################### {coder}'s: ####################\n")
        for file1, coder1, file2, coder2 in what.pairs_of(coder):
            if coder in (coder1, coder2):
                msgcount += compare_files(file1, coder1, file2, coder2, maxcountdiff, annots)
    sys.exit(msgcount)  # 0 if no errors, number of errors otherwise


def compare_files(file1: str, name1: str, file2: str, name2: str, maxcountdiff: int, annots: annot.Annotations) -> int:
    with open(file1, 'r', encoding='utf8') as f1:
        content1 = f1.read()
    with open(file2, 'r', encoding='utf8') as f2:
        content2 = f2.read()
    la_pairs1 = annots.find_all_line_and_annotation_pairs(content1)  # list of pairs (previousline, annotation)
    la_pairs2 = annots.find_all_line_and_annotation_pairs(content2)  # list of pairs (previousline, annotation)
    return compare_codings2(file1, name1, la_pairs1, file2, name2, la_pairs2, maxcountdiff, annots)


def compare_codings2(file1: str, name1: str, la_pairs1: tg.Sequence[tg.Tuple[str, str]],
                     file2: str, name2: str, la_pairs2: tg.Sequence[tg.Tuple[str, str]],
                     maxcountdiff: int, annots: annot.Annotations):
    msgcount = 0
    def printmsg(msg: str, item1: str, item2: str, afterline: tg.Optional[str]=None):
        print("\n#####", msg)
        print("%s, (%s)\n   %s" % (file1, name1, item1))
        print("%s, (%s)\n   %s" % (file2, name2, item2))
        if afterline:
            print(f"after line '{line1}'")
        return 1

    for pair1, pair2 in zip(la_pairs1, la_pairs2):
        line1, annotation1 = pair1
        line2, annotation2 = pair2
        # ----- check for non-parallel codings:
        if line1 != line2:
            msgcount += printmsg("Annotations should be at parallel points in the files, but are at different points here:",
                                 f"\"{line1}\"", f"\"{line2}\"")
            break
        # ----- check for incomplete annotation:
        if annots.is_empty_annotation(annotation1) or annots.is_empty_annotation(annotation2):
            msgcount += printmsg("Incomplete annotation found, skipping rest of this file pair:",
                                 annotation1, annotation2, line1)
            break
        # ----- check for double IGNORE:
        set1 = annots.codings_of(annotation1, strip_suffixes=True)
        set2 = annots.codings_of(annotation2, strip_suffixes=True)
        if IGNORE in set1 and IGNORE in set2:
            msgcount += printmsg(f"Code '{IGNORE}' should only appear in one coding, never in both as it does here:",
                                 annotation1, annotation2, line1)
            continue
        # ----- check for IGNORE:
        if IGNORE in (set1 | set2):
            continue  # do not report possible discrepancies
        # ----- check for code discrepancies:
        if set1 ^ set2:  # code sets are different
            msgcount += printmsg(f"The sets of codes applied are different, please check:",
                                 "{%s}" % ", ".join(sorted(set1)), "{%s}" % ", ".join(sorted(set2)), line1)
            continue
        # ----- check for count discrepancies:
        minfactor = (100 - maxcountdiff - 1) / 100
        for code, counts in annots.codes_with_suffixes(annotation1, annotation2).items():
            icount1, ucount1, icount2, ucount2 = counts
            if (abs(icount1 - icount2) > maxcountdiff):
                msgcount += printmsg(f"{code}: Very different informativeness counts, please reconsider:",
                                     f"{code}:i{icount1} vs :i{icount2}", line1)
    return msgcount
