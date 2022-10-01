"""Simple reusable operations"""
import re
import typing as tg

def citekey(list_line: str) -> str:
    """From a line like EMSE-2021/AbuDab21.pdf return AbuDab21"""
    return split_entry(list_line)[1]


def split_entry(list_line: str) -> tg.Tuple[str, str]:
    """From a line like EMSE-2021/AbuDab21.pdf return its semantic parts EMSE-2021 and AbuDab21"""
    mm = re.fullmatch(r"(.+)/(.+)\.pdf", list_line)
    assert mm
    return (mm.group(1), mm.group(2))


def volume(list_line: str) -> str:
    """From a line like EMSE-2021/AbuDab21.pdf return EMSE-2021"""
    return split_entry(list_line)[0]
