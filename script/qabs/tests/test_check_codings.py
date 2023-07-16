# pytest tests

import qscript.annotations as annot
import qscript.cmd.check_codings as cc
import qscript.icc as icc

import qabstracts

qabstracts.register_implclasses()
annots = icc.init(annot.Annotations)  # reused globally in order to read codebook only once


def test_check_code():
    check_code_tests = [
        ("background", "", None),
        ("a-result", "", None),
        ("method", "", None),
        ("result", "hype", None),
        ("method", ":i4", None),
        ("background", ":i1", "suffix 'i1' not allowed for code 'background': background:"),
        ("bjective", "", "unknown"),
        ("metho", "u1", "unknown"),
    ]
    for code, suffix, result_fragment in check_code_tests:
        try:
            annots.check_coding(code, suffix)
        except annot.Codebook.CodingError as exc:
            assert result_fragment in exc.args[0]
        else:
            assert not result_fragment


def test_report_errors_within_braces():
    tests = [
        ("{{}}", 0),
        ("{{background}}", 0),
        ("{{objective,method}}", 0),
        ("{{objective, method:i3}}", 0),
        ("{{method,result:u1:hype}}", 0),
        ("{{backgr}}", 1),
        ("{{objective:2, method:i}}", 2),
        ("{{method,result:hype,stuff}}", 1),
    ]
    for annot, errcount in tests:
        errors = cc.report_errors_within_braces(annot, annots)
        if len(errors) != errcount:
            print (f"{annot}, {errcount} --> {errors}")
            assert len(errors) == errcount
