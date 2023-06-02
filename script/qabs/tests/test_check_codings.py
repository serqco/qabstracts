# pytest tests

import qscript.annotations as annot
import qscript.cmd.check_codings as cc
import qscript.icc as icc

import qabstracts

qabstracts.register_implclasses()
annots = icc.init(annot.Annotations)  # reused globally in order to read codebook only once


def test_check_code():
    check_code_tests = [
        ("background", None, None),
        ("a-result", None, None),
        ("-hype", None, None),
        ("method", None, None),
        ("method", ":i4", None),
        ("background", ":i1", "should not have an IU suffix"),
        ("bjective", None, "unknown"),
        ("metho", "u1", "unknown"),
    ]
    for code, suffix, result_fragment in check_code_tests:
        result = annots.wrong_coding_msg(code, suffix)
        if result_fragment is None:
            is_correct = result is None
        else:
            is_correct = (result.find(result_fragment) != -1) 
        if not is_correct:
            print(f"test({code}, {suffix}, {result_fragment}) -> {result}")
        assert is_correct


def test_report_errors_within_braces():
    tests = [
        ("{{}}", 0),
        ("{{background}}", 0),
        ("{{objective,method}}", 0),
        ("{{objective, method:i3}}", 0),
        ("{{method,result:u1,-hype}}", 0),
        ("{{backgr}}", 1),
        ("{{objective:2, method:i}}", 2),
        ("{{method,result,-hype,stuff}}", 1),
    ]
    for annot, errcount in tests:
        errors = cc.report_errors_within_braces(annot, annots)
        if len(errors) != errcount:
            print (f"{annot}, {errcount} --> {errors}")
            assert len(errors) == errcount
