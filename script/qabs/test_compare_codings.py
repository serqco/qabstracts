# pytest tests

import sys

import pytest

import qabs.compare_codings as cc


def test_codes_of():
    assert cc.codes_of("a") == {'a'}
    assert cc.codes_of("a b") == {'a', 'b'}
    assert cc.codes_of("a,b") == {'a', 'b'}
    assert cc.codes_of("a, b") == {'a', 'b'}
    assert cc.codes_of("a:0, b:333") == {'a', 'b'}


def test_compare_codings2(capsys):
    def mycc(codings1, codings2):
        return cc.compare_codings2("A", "Name1", codings1, "B", "Name2", codings2, 33)

    def check(codings1, codings2, outputelem, appears=True):
        msgcount = mycc(codings1, codings2)
        captured = capsys.readouterr()
        if captured.err: print(captured.err, file=sys.stderr)
        if outputelem:
            if appears:
                assert (outputelem in captured.out), captured.out
            else:
                assert (outputelem not in captured.out), captured.out
        else:
            assert msgcount == 0

    check([("line", "a, b")], [("line", "a, b")], 
          None)
    check([("line", "a, b:4")], [("line", "a, b:4")], 
          None)
    check([("line", "a, b:4")], [("line", "")], 
          "Incomplete annotation")
    check([("line", "a, b")], [("different line", "a, b")], 
          "should be at parallel points")
    check([("line", f"a, b, {cc.IGNORE}")], [("line", f"a, b, {cc.IGNORE}")], 
          "should only appear in one coding")
    check([("line", f"a, b, c")], [("line", f"b, c")], 
          "sets of codes applied are different")
    check([("line", f"a, b, c")], [("line", f"a, b, {cc.IGNORE}")], 
          "sets of codes applied are different", appears=False)
    check([("line", "a, b:4")], [("line", "a, b:7")], 
          "counts are more different than allowed")
    check([("line", "a, b:4")], [("line", "a, b:6")], 
          "counts are more different than allowed", appears=False)
