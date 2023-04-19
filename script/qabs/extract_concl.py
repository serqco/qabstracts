import io
import re
import typing as tg

import pdfminer.high_level as pdfhl
import pdfminer.layout as pdfl

import qabs.extract_part as ep
import qscript

meaning = """Heuristically obtains the last sections (conclusion section) from PDF files.
  Works on one given PDF file or each local PDF file whose basename is
  listed in the given '*.list' file.
  Uses pdfminer.six to extract the PDF text,
  then uses incomplete heuristics according to the given --layout to find 
  start and end of the last numbered section. 
  Creates conclusion text file with same basename in outputdir.
"""


def add_arguments(subparser: qscript.ArgumentParser):
    subparser.add_argument('--layout', type=str, required=True,
                           choices=layouttypes.keys(),
                           help="Article layout type used in the PDFs.")
    subparser.add_argument('outputdir',
                           help="Directory where conclusions files will be placed")
    subparser.add_argument('inputfile',
                           help="PDF file to scan for its last section")


def execute(args: qscript.Namespace):
    ep.extract_parts(conclusion_from_pdf, layouttypes, 
                     args.layouttype, args.outputdir, args.inputfile)


default_section_heading = r"\n\n((\d\d?) .+)\n\n"  # group 2 must be section number
default_end_of_concl = (r"\n(Acknowledgments?|ACKNOWLEDGMENTS?|CRediT .{10,36}|"
                        r"References\s?|REFERENCES|Appendix( A(: .+)?)?)\n")
# Map from a layouttype name to a layout description and list of venues where it applies:
layouttypes = dict(  # None means "We have no clue!"
    acmconf=dict(
        laparams=pdfl.LAParams(),
        section_heading=r"\n\n((\d\d?)\s+[^a-z\n]+)\n",
        end_of_concl=default_end_of_concl,
        remove_pars=(r"\d+",  # page number
                     r"\x0c.+\n\n.+"),  # page header
        applies_to=[ep.is_acmconf_icse, ]),
    acmtrans=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        remove_pars=(),
        applies_to=["TOSEM", ]),
    elsevier=dict(
        laparams=pdfl.LAParams(),
        section_heading=r"\n\n((\d\d?)\. .+)\n\n",
        end_of_concl=default_end_of_concl,
        remove_pars=(),
        applies_to=["IST", ]),
    ieeeconf=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        remove_pars=(),
        applies_to=[ep.is_ieeeconf_icse, ]),
    ieeetrans=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        remove_pars=(),
        applies_to=["TSE", ]),
    springer=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        remove_pars=(r"\x0c\d+\s+Page\s+\d+\s+of\s+\d+",
                     r"Page\s+\d+\s+of\s+\d+\s+\d+",
                     r"\x0c?Empir\s+Software\s+Eng\s\(20\d\d\)\s+\d+:\d+"),
        applies_to=["EMSE", ]),
)


def conclusion_from_pdf(layout: ep.LayoutDescriptor, pdffile: str) -> str:
    out = io.StringIO()
    with open(pdffile, 'rb') as f:
        pdfhl.extract_text_to_fp(f, out, laparams=layout['laparams'], 
                                 output_type='text', codec=None)
    txt = ep.more_readable(out.getvalue(), layout['remove_pars'])
    headings_mms = find_headings([mm for mm in re.finditer(layout['section_heading'], txt)])
    headings_txt = "\n".join([mm.group(1) for mm in headings_mms])
    # return "%s\n***\n%s" % (headings_txt, txt)  # use for debugging
    conclusion_plus_rest = txt[headings_mms[-1].start(1):]
    mm = re.search(layout['end_of_concl'], conclusion_plus_rest)
    concl_endpos = mm.start() if mm else len(conclusion_plus_rest)-1
    return "%s\n\n%s" % (headings_txt, conclusion_plus_rest[:concl_endpos])


def find_headings(matches: tg.List[re.Match]) -> tg.List[re.Match]:
    """
    Simple heuristic for letting through only proper headings:
    We ensure that the numbers increase by 1.
    Exception: We allow increase by 2 for the case that one(!) heading in between is longer than 1 line.
    """
    result = []
    lastnumber = 0
    for mm in matches:
        thisnumber = int(mm.group(2))  # see regexp in layouttypes
        if thisnumber > lastnumber and thisnumber <= lastnumber+2:
            # we allow gaps of 1 to accomodate occasional multiline-long headings
            result.append(mm)
            lastnumber = thisnumber
    return result