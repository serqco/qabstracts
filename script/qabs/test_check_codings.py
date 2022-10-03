# pytest tests

import os.path

import pytest

import qabs.check_codings as cc

codebookfile = "codebook.md"


def test_check_code():
    check_code_tests = [
        ("background", None, None),
        ("a-result", None, None),
        ("-hype", None, None),
        ("method", "4", None),
        ("background", "5", "should not have a count"),
        ("result", None, "needs a count"),
        ("bjective", None, "unknown"),
        ("metho", "7", "unknown"),
    ]
    codes, globalcodes = cc.allowed_codes(codebookfile)
    for code, num, result_fragment in check_code_tests:
        result = cc.check_code(code, num, codes)
        if result_fragment is None:
            is_correct = result is None
        else:
            is_correct = (result.find(result_fragment) != -1) 
        if not is_correct:
            print(f"test({code}, {num}, {result_fragment}) -> {result}")
        assert is_correct


def test_report_errors_within_braces():
    tests = [
        ("{{}}", 0),
        ("{{background}}", 0),
        ("{{objective, method:3}}", 0),
        ("{{method:4,result:4,-hype}}", 0),
        ("{{backgr}}", 1),
        ("{{objective, method}}", 1),
        ("{{objective:2, method}}", 2),
        ("{{method,result,-hype,stuff}}", 3),
    ]
    codes, globalcodes = cc.allowed_codes(codebookfile)
    for annot, errcount in tests:
        errors = cc.report_errors_within_braces(annot, codes)
        if len(errors) != errcount:
            print (f"{annot}, {errcount} --> {errors}")
            assert len(errors) == errcount
