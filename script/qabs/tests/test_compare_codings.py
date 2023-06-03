# pytest tests

import sys
import typing as tg

import qscript.annotations as annot
import qscript.cmd.compare_codings as cc
import qscript.icc as icc

import qabstracts

qabstracts.register_implclasses()
annots = icc.init(annot.Annotations)  # for every test to use, so we read the codebook only once


def test_compare_codings2(capsys):
    def l_a_s(la_pairs: tg.Sequence[tg.Tuple[str, str]]) -> tg.Sequence[annot.AnnotatedSentence]:
        return [annot.AnnotatedSentence(1, pair[0], pair[1]) for pair in la_pairs]

    def mycc(la_pairs1, la_pairs2):
        ctx = cc.ComparatorContext("A", "Name1", "B", "Name2", "TEST")
        comparator.compare_codings2(ctx, l_a_s(la_pairs1), l_a_s(la_pairs2), 1, annots)

    def check(la_pairs1, la_pairs2, outputelem, appears=True):
        old_msgcount = comparator.msgcount
        mycc(la_pairs1, la_pairs2)
        captured = capsys.readouterr()
        if captured.err: 
            print(captured.err, file=sys.stderr)
        if outputelem:
            if appears:
                assert (outputelem in captured.out), captured.out
            else:
                assert (outputelem not in captured.out), captured.out
        else:
            assert comparator.msgcount == old_msgcount

    comparator = icc.init(cc.CodingsComparator)
    check([("line", "{{method, result}}")], [("line", "{{method, result}}")], 
          "")
    check([("line", "{{method, result:i4}}")], [("line", "{{method, result:i4}}")], 
          "")
    check([("line", "{{method}}")], [("line", "{{}}")], 
          "Incomplete annotation")
    check([("line", "{{method}}")], [("different line", "{{method}}")], 
          "should be at parallel points")
    check([("line", "{{method, %s}}" % cc.IGNORE)], [("line", "{{method, %s}}" % cc.IGNORE)], 
          "should only appear in one coding")
    check([("line", "{{method, result}}")], [("line", "{{method}}")], 
          "sets of codes applied are different")
    check([("line", "{{method, result}}")], [("line", "{{method, %s}}" % cc.IGNORE)], 
          "sets of codes applied are different", appears=False)
    check([("line", "{{design:i4}}")], [("line", "{{design:i7}}")], 
          "Very different numbers of informativeness gaps")
    check([("line", "{{design:i4}}")], [("line", "{{design:i7, %s}}" % cc.IGNORE)], 
          "Very different numbers of informativeness gaps", appears=False)
