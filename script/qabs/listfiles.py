"""Simple reusable operations"""
import re
import typing as tg

Entry = str  # Pseudo type for strings of form "mypath/EMSE-2021/AbuDab21.pdf"

def citekey(list_line: Entry) -> str:
    """From a line like EMSE-2021/AbuDab21.pdf return AbuDab21"""
    return split_entry(list_line)[1]


def split_entry(list_line: Entry) -> tg.Tuple[str, str]:
    """From a line like EMSE-2021/AbuDab21.pdf return its semantic parts EMSE-2021 and AbuDab21"""
    mm = re.fullmatch(r"(.+)/(.+)\.pdf", list_line)
    assert mm
    return (mm.group(1), mm.group(2))


def volume(list_line: Entry) -> str:
    """From a line like EMSE-2021/AbuDab21.pdf return EMSE-2021"""
    return split_entry(list_line)[0]


def read_list(filename: str) -> tg.Sequence[Entry]:
    with open(filename, 'rt', encoding='utf-8') as lst:
        mylist = lst.read().split('\n')
        mylist.pop()  # file ends with \n, so last item is empty
    return mylist


def write_list(to: str, entries: tg.Iterator[Entry]):
    with open(to, 'w', encoding='utf8') as lst:
        for elem in entries:
            lst.write(f"{elem}\n")


