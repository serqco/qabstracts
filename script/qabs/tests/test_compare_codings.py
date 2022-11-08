# pytest tests

import sys

import qabs.annotations as annot
import qabs.compare_codings as cc

annots = annot.Annotations()  # for every test to use, so we read the codebook only once

def test_compare_codings2(capsys):
    def mycc(la_pairs1, la_pairs2):
        return cc.compare_codings2("A", "Name1", la_pairs1, "B", "Name2", la_pairs2, 2, annots)

    def check(la_pairs1, la_pairs2, outputelem, appears=True):
        msgcount = mycc(la_pairs1, la_pairs2)
        captured = capsys.readouterr()
        if captured.err: print(captured.err, file=sys.stderr)
        if outputelem:
            if appears:
                assert (outputelem in captured.out), captured.out
            else:
                assert (outputelem not in captured.out), captured.out
        else:
            assert msgcount == 0

    check([("line", "{{a, b}}")], [("line", "{{a, b}}")], 
          None)
    check([("line", "{{a, b:i4}}")], [("line", "{{a, b:i4}}")], 
          None)
    check([("line", "{{a, b:4}}")], [("line", "{{}}")], 
          "Incomplete annotation")
    check([("line", "{{a, b}}")], [("different line", "{{a, b}}")], 
          "should be at parallel points")
    check([("line", "{{a, b, %s}}" % cc.IGNORE)], [("line", "{{a, b, %s}}" % cc.IGNORE)], 
          "should only appear in one coding")
    check([("line", "{{a, b, c}}")], [("line", "b, c}}")], 
          "sets of codes applied are different")
    check([("line", "{{a, b, c}}")], [("line", "{{a, b, %s}}" % cc.IGNORE)], 
          "sets of codes applied are different", appears=False)
    check([("line", "{{a, design:i4}}")], [("line", "{{a, design:i7}}")], 
          "Very different numbers of informativeness gaps")
    check([("line", "{{a, result:u1}}")], [("line", "{{a, result:u4}}")], 
          "counts are more different than allowed", appears=False)
