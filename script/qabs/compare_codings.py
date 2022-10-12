import re
import sys
import typing as tg

usage = """Compares annotations between coders and flags discrepancies.
  Knows about the maximum allowed information particle count difference.
  Knows about codes for silencing discrepancies.
  Reports problems on stdout.
"""

IGNORE = '-ignorediff'  # code that signals not to report coding differences

def configure_argparser(subparser):
    subparser.add_argument('workdir',
                           help="Directory where sample-who-what.txt and abstracts.?/* live")
    subparser.add_argument('--maxcountdiff', type=int, default=33,
                           help="percentage how much smaller count may be smaller without a message")


def compare_codings(maxcountdiff: int, workdir: str):
    with open (f"{workdir}/sample-who-what.txt", 'r', encoding='utf8') as f:
        lines = f.readlines()
    msgcount = 0
    for line in lines:
        if line.startswith("#"):
            continue
        parts = line.strip().split()  # splits on single or multiple whitespace after removing trailing \n
        basename = parts[0] + ".txt"
        columns = parts[1:]
        numpairs = (len(columns)+1)//2 if len(columns) > 1 else 0  # 2 columns: 1; 3 columns: 2, 4 columns: 2, ...
        # compare subsequent pairs of columns (k, k+1), (k+2, k+3), ... and compare last two if number is odd:

        def filename(columnindex: int):
            """Knows the abstracts.A, abstracts.B dirname convention."""
            char = chr(ord('A') + columnindex)  # 26 columns maximum (we'll never need more than 10)
            return f"{workdir}/abstracts.{char}/{basename}"

        for p in range(numpairs):
            firstindex = 2*p
            neighbor = 1 if firstindex+1 < len(columns) else -1  # compare (p,p+1) if possible, (p, p-1) if not
            if len(columns[firstindex]) > 1 and len(columns[firstindex+neighbor]) > 1:  # but skip incomplete pairs
                msgcount += compare_files(filename(firstindex), columns[firstindex],
                                          filename(firstindex+neighbor), columns[firstindex+neighbor],
                                          maxcountdiff)
    sys.exit(msgcount)  # 0 if no messages, number of messages otherwise


def compare_files(file1: str, name1: str, file2: str, name2: str, maxcountdiff: int) -> int:
    with open(file1, 'r', encoding='utf8') as f1:
        content1 = f1.read()
    with open(file2, 'r', encoding='utf8') as f2:
        content2 = f2.read()
    codings1 = re.findall("(.*)\n{{(.*)}}", content1)  # list of pairs (previousline, coding)
    codings2 = re.findall("(.*)\n{{(.*)}}", content2)  # ditto
    return compare_codings2(file1, name1, codings1, file2, name2, codings2, maxcountdiff)


def compare_codings2(file1: str, name1: str, codings1: tg.Sequence[tg.Tuple[str, str]], 
                     file2: str, name2: str, codings2: tg.Sequence[tg.Tuple[str, str]], 
                     maxcountdiff: int):
    msgcount = 0
    def printmsg(msg: str, item1: str, item2: str, afterline: tg.Optional[str]=None):
        print("\n#####", msg)
        print("%s, (%s)\n   %s" % (file1, name1, item1))
        print("%s, (%s)\n   %s" % (file2, name2, item2))
        if afterline:
            print(f"after line '{line1}'")
        return 1

    for coding1, coding2 in zip(codings1, codings2):
        line1, codes1 = coding1
        line2, codes2 = coding2
        # ----- check for incomplete annotation:
        if codes1.strip() == "" or codes2.strip() == "":
            msgcount += printmsg("Incomplete annotation found, skipping rest of this file pair:",
                                 "{{%s}}" % codes1, "{{%s}}" % codes2, line1)
            break
        # ----- check for non-parallel codings:
        if line1 != line2:
            msgcount += printmsg("Codings should be at parallel points in the files, but are at different points here:",
                                 f"\"{line1}\"", f"\"{line2}\"")
            break
        # ----- check for double IGNORE:
        set1 = codes_of(codes1)
        set2 = codes_of(codes2)
        if IGNORE in set1 and IGNORE in set2:
            msgcount += printmsg(f"Code '{IGNORE}' should only appear in one coding, never in both as it does here:",
                                 "{{%s}}" % codes1, "{{%s}}" % codes2, line1)
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
        for code, pair in codes_with_counts(codes1, codes2).items():
            count1, count2 = int(pair[0]), int(pair[1])
            if (count1 < count2 and count1 < minfactor * count2) or \
                    (count2 < count1 and count2 < minfactor * count1):
                msgcount += printmsg(f"These counts are more different than allowed, please reconsider:",
                                     f"{code}:{count1}", f"{code}:{count2}", line1)
    return msgcount


def codes_of(annotation: str) -> tg.Set[str]:
    """Return set of codes without counts from annotation text without the braces."""
    result = set()
    annotation_regexp = r"([\w-]+\??)(:\d+)?"  # we simply ignore commas and blanks (and any non-word garbage symbols)
    for code, count in re.findall(annotation_regexp, annotation):
        result.add(code)
    return result


def codes_with_counts(annotation1: str, annotation2: str) -> tg.Mapping[str, tg.Tuple[int, int]]:
    """Map codes to pairs of counts for the codes that have counts."""
    result = dict()
    annotation_regexp = r"([\w-]+):(\d+)"
    for code, count in re.findall(annotation_regexp, annotation1):
        result[code] = count
    for code, count in re.findall(annotation_regexp, annotation2):
        result[code] = (result[code], count)  # turn single count into a pair of counts
    # counts are never optional, so all values are pairs now
    return result
