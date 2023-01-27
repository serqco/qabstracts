import os.path
import re
import subprocess as sub
import typing as tg

import qabs.metadata as metadata

usage = """Heuristically obtains abstracts from PDF files.
  Works on one given PDF file or each local PDF file whose basename is
  listed in the given '*.list' file.
  Calls pdftotext (from the poppler-utils package) to extract page 1,
  then uses incomplete heuristics according to the given --layout to find 
  start and end of the abstract on that page. 
  Creates abstract text file with same basename in outputdir.
"""

def configure_argparser(p_extract_abs):
    p_extract_abs.add_argument('--layout', type=str, required=True,
                               choices=layouttypes.keys(),
                               help="Article layout type used in the PDFs.")
    p_extract_abs.add_argument('outputdir',
                               help="Directory where abstracts files will be placed")
    p_extract_abs.add_argument('inputfile',
                               help="PDF file to scan for its abstract")


def is_icse_in_year(volume: str, years: tg.Set[int]) -> bool:
    """Knows which ICSE years use ACM layout (versus IEEE CS layout)."""
    path, name, year = volume_path_name_year(volume)
    if name != "ICSE":
        return False
    return year in years

def is_acmconf_icse(volume: str) -> bool:
    """Knows some ICSE years that use acmconf layout."""
    return is_icse_in_year(volume, {2022, 2020, 2018, 2016})


def is_ieeeconf_icse(volume: str) -> bool:
    """Knows some ICSE years that use ieeeconf layout."""
    return is_icse_in_year(volume, {2021, 2019, 2017})


# Map from a layouttype name to a layout description and list of venues where it applies:
layouttypes = dict(  # None means "We have no clue!"
    acmconf=dict(
        cols=2,
        start=r"\nABSTRACT\s",
        end=r"\nCCS CONCEPTS\s",
        applies_to=[is_acmconf_icse, ]),
    acmtrans=dict(
        cols=1,
        start=None,  # a horizontal line not represented in the text format
        end=r"\n+CCS Concepts:|\n+Additional Key Words and Phrases:|\n+ACM Reference format:",
        applies_to=["TOSEM", ]),
    elsevier=dict(
        cols=1,  # much easier to handle this way. Abstract is in right col!
        start=r"\nABSTRACT\n+",
        end=r"\n+1.\s|\sCorresponding Author\s|\n+Received \d|\n+Available online \d|Elsevier B.V.",
        applies_to=["IST", ]),
    ieeeconf=dict(
        cols=2,
        start=r"\nAbstract—",
        end=r"\n+I\. ",
        applies_to=[is_ieeeconf_icse, ]),
    ieeetrans=dict(
        cols=1,  # abtract and index terms are single-column
        start=r"\nAbstract—",
        end=r"\n+Index Terms—",
        applies_to=["TSE", ]),
    springer=dict(
        cols=1,
        start=r"\nAbstract\s+",
        end=r"\n+Keywords\s|\n+Communicated by:",  # TODO 2: Let the latter come through: 
        # Abstract will be incomplete and need fixing; the string is helpful for finding those cases!
        applies_to=["EMSE", ]),
)


def decide_layouttype(entry: metadata.Entry) -> str:
    volume = metadata.volume(entry)
    venue = volume_path_name_year(volume)[1]
    for key, descriptor in layouttypes.items():
        for candidate in descriptor['applies_to']:
            mentioned_by_name = (candidate == venue)
            matched_by_predicate = (callable(candidate) and candidate(volume))
            if mentioned_by_name or matched_by_predicate:
                return key
    raise ValueError(f"cannot find layouttype for volume '{volume}'")
    return "???"


def extract_abstracts(outputdir: str, layouttype: str, inputfile: str):
    if inputfile.endswith('.pdf'):
        extract_abstract(inputfile, layouttype, outputdir)
    elif inputfile.endswith('.list'):
        with open(inputfile, mode='rt', encoding="utf8") as f:
            inputstring = f.read()
        for inputfile in inputstring.split('\n'):
            extract_abstract(inputfile, layouttype, outputdir)
    else:
        print(f"'{inputfile}': unknown input file type; must be .pdf or .list")


def extract_abstract(pdffilepath: str, layouttype: str, outputdir: str):
    #----- skip existing:
    pdffile = os.path.basename(pdffilepath)
    basename, suffix = os.path.splitext(pdffile)
    outputpathname = f"{outputdir}/{basename}.txt"
    if os.path.exists(outputpathname):
        print(f"#### '{outputpathname}' exists!. SKIPPED.")
        return
    #----- obtain abstract:
    abstract = abstract_from_pdf(pdffilepath, layouttype)
    #----- write abstract:
    print(f"---- writing '{outputpathname}'")
    with open(outputpathname, mode='wt', encoding="utf8") as f:
        f.write(abstract)


def abstract_from_pdf(pdffile: str, layouttype: str) -> str:
    cols = layouttypes[layouttype]['cols']
    if cols == 1:
        page1 = page1_from_pdf(pdffile, keeplayout=False)
        return abstract_from_page(page1, layouttype)
    elif cols == 2:
        page1 = page1_from_pdf(pdffile, keeplayout=True)
        return abstract_from_page(left_column(page1), layouttype)
    else:
        assert False, f"impossible col: {cols}"
        return ""


def page1_from_pdf(pdffile: str, keeplayout: bool) -> str:
    if keeplayout:
        args = ["pdftotext", "-f", "1", "-l", "1", "-layout", pdffile, "-"]
    else:
        args = ["pdftotext", "-f", "1", "-l", "1", pdffile, "-"]
    result = sub.run(args, text=True, stdout=sub.PIPE)
    page1 = result.stdout
    # print(f">>>>>>>>>>>>>>> page1: {page1}\n")
    return page1


def left_column(rawpage: str) -> str:
    # As of Debian poppler-utils 20.09.0-3.1,
    # the normal mode of pdftotext creates massive violations of text order,
    # in particular inserting the right column's text in between 
    # the heading "Abstract" and the actual abstract text directly below,
    # so we use -layout and do the following:
    # 1. cut away a possible left margin, so that new lines
    #    really start at a newline
    # 2. cut away the right column for two-column layouts
    # 3. remove empty lines that can arise due to unaligned lines left/right
    leftmargin_re = r"^ {1,30}"  # must not match a line that is empty left, non-empty right 
    marginless_page, repls1 = re.subn(leftmargin_re, r"", rawpage, flags=re.MULTILINE)  # 1.
    rightcol_re = r"(\S)    .*\n| {30,}.*\n"  # with left col | empty left col
    fluffypage, repls2 = re.subn(rightcol_re, r"\1\n", marginless_page)  # 2.
    compactpage, repls3 = re.subn(r"\n+", r"\n", fluffypage)  # 3.
    # print(f">>>>>>>>>>>>>>> sub'd page({repls1},{repls2},{repls3}): {compactpage}\n")
    return compactpage


def abstract_from_page(page: str, layouttype: str) -> str:
    #--- find abstract start or use 0:
    re_start = layouttypes[layouttype]['start']
    m_start = re_start and re.search(re_start, page) or None
    startpos = m_start and m_start.end() or 0
    #--- find abstract end or use page end:
    re_end = layouttypes[layouttype]['end']
    m_end = re_end and re.search(re_end, page[startpos+1:]) or None
    endpos = m_end and startpos+1+m_end.start() or len(page)
    #--- return best approximation to abstract:
    # print(f"  abstract_from_page: len={len(page)}, start={startpos}, end={endpos}")
    # print(f"  start: '{page[startpos:startpos+30]}', end: '{page[endpos+1:endpos+30]}'")
    return page[startpos:endpos]


def volume_path_name_year(volumepath: str) -> tg.Tuple[str, str, int]:
    volumename_regexp = r"(.+/)?([A-Za-z]+)-(\d\d\d\d)"  # {perhaps_path}/{name}-{year}
    mm = re.fullmatch(volumename_regexp, volumepath) 
    path, name, year = (mm.group(1), mm.group(2), int(mm.group(3)))
    return (path, name, year)