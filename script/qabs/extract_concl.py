import re
import typing as tg

import pdfminer.high_level as pdfhl
import pdfminer.layout as pdfl

import qabs.extract_part as ep

usage = """Heuristically obtains the last sections (conclusion section) from PDF files.
  Works on one given PDF file or each local PDF file whose basename is
  listed in the given '*.list' file.
  Uses pdfminer.six to extract the PDF text,
  then uses incomplete heuristics according to the given --layout to find 
  start and end of the last numbered section. 
  Creates conclusion text file with same basename in outputdir.
"""


def configure_argparser(p_extract_abs):
    p_extract_abs.add_argument('--layout', type=str, required=True,
                               choices=layouttypes.keys(),
                               help="Article layout type used in the PDFs.")
    p_extract_abs.add_argument('outputdir',
                               help="Directory where conclusions files will be placed")
    p_extract_abs.add_argument('inputfile',
                               help="PDF file to scan for its last section")


default_section_heading = r"\n\n(\d\d? .+)\n\n"
default_end_of_concl = r"\n(Acknowledgments|ACKNOWLEDGMENTS|References|REFERENCES)\n"
# Map from a layouttype name to a layout description and list of venues where it applies:
layouttypes = dict(  # None means "We have no clue!"
    acmconf=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        applies_to=[ep.is_acmconf_icse, ]),
    acmtrans=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        applies_to=["TOSEM", ]),
    elsevier=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        applies_to=["IST", ]),
    ieeeconf=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        applies_to=[ep.is_ieeeconf_icse, ]),
    ieeetrans=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        applies_to=["TSE", ]),
    springer=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        applies_to=["EMSE", ]),
)


def extract_concl(outputdir: str, layouttype: str, inputfile: str):
    ep.extract_parts(conclusion_from_pdf, layouttypes, layouttype, outputdir, inputfile)


def conclusion_from_pdf(layout: ep.LayoutDescriptor, pdffile: str) -> str:
    txt = pdfhl.extract_text(pdffile, layout['laparams'])
    txt = ep.more_readable(txt)  # TODO: extract last numbered section
    headings_mms = [mm for mm in re.finditer(layout['section_heading'], txt)]
    conclusion_plus_rest = txt[headings_mms[-1].start():]
    mm = re.search(layout['end_of_concl'], conclusion_plus_rest)
    concl_endpos = mm.start()
    return conclusion_plus_rest[:concl_endpos]
