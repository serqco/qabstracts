import re
import subprocess as sub

import qabs.extract_part as ep

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


# Map from a layouttype name to a layout description and list of venues where it applies:
layouttypes = dict(  # None means "We have no clue!"
    acmconf=dict(
        cols=2,
        start=r"\nABSTRACT\s",
        end=r"(?i)\nCCS CONCEPTS|\nACM Reference Format:|\nKEYWORDS\n",
        applies_to=[ep.is_acmconf_icse, ]),
    acmtrans=dict(
        cols=1,
        start=None,  # a horizontal line not represented in the text format
        # Author names precede the abstract in ALL CAPS, but this criterion is difficult and risky
        end=r"(?i)\n+CCS Concepts:|\n+Additional Key Words and Phrases:|\n+ACM Reference format:",
        applies_to=["TOSEM", ]),
    elsevier=dict(
        cols=1,  # much easier to handle this way. Abstract is in right col!
        start=r"\n(ABSTRACT|A B S T R A C T)\n+(Keywords:\n(.+\n)+\n)?",
        end=r"\n+1.\s|\sCorresponding Author\s|\n+Received \d|\n+Available online \d|Elsevier B.V.",
        applies_to=["IST", ]),
    ieeeconf=dict(
        cols=2,
        start=r"\nAbstract—",
        end=r"\n+I\. ",
        applies_to=[ep.is_ieeeconf_icse, ]),
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


def extract_abs(outputdir: str, layouttype: str, inputfile: str):
    ep.extract_parts(abstract_from_pdf, layouttypes, layouttype, outputdir, inputfile)


def abstract_from_pdf(layouttype: ep.LayoutDescriptor, pdffile: str) -> str:
    cols = layouttype['cols']
    if cols == 1:
        page1 = page1_from_pdf(pdffile, keeplayout=False)
        return abstract_from_page(layouttype, page1)
    elif cols == 2:
        page1 = page1_from_pdf(pdffile, keeplayout=True)
        return abstract_from_page(layouttype, left_column(page1))
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


def abstract_from_page(layouttype: ep.LayoutDescriptor, page: str) -> str:
    # --- find abstract start or use 0:
    re_start = layouttype['start']
    m_start = re_start and re.search(re_start, page) or None
    startpos = m_start and m_start.end() or 0
    # --- find abstract end or use page end:
    re_end = layouttype['end']
    m_end = re_end and re.search(re_end, page[startpos+1:]) or None
    endpos = m_end and startpos+1+m_end.start() or len(page)
    # --- return best approximation to abstract:
    # print(f"  abstract_from_page: len={len(page)}, start={startpos}, end={endpos}")
    # print(f"  start: '{page[startpos:startpos+30]}', end: '{page[endpos+1:endpos+30]}'")
    return ep.more_readable(page[startpos:endpos])
