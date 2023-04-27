import io
import re
import typing as tg

import pdfminer.high_level as pdfhl
import pdfminer.layout as pdfl

import qscript.extract_part as ep
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
                     args.layout, args.outputdir, args.inputfile)


default_section_heading = r"\n\n((\d\d?) .+)\n\n"  # group 2 must be section number
default_end_of_concl = (r"\n("
                        r"Acknowledge?ments?|Acknowledge?ments? [A-Z].+|ACKNOWLEDGE?MENTS?|"
                        r"CRediT .{10,36}|"
                        r"Declarations|Declaration of [Cc]ompeting [Ii]nterest.?\s*|"
                        r"Open Access This article is licensed under .+|"
                        r"References\s?|REFERENCES|"
                        r"APPENDIX|Appendix( A(: .+)?)?"
                        r")\n")
# Map from a layouttype name to a layout description and list of venues where it applies:
layouttypes = dict(  # None means "We have no clue!"
    acmconf=dict(
        laparams=pdfl.LAParams(),
        section_heading=r"\n\n((\d\d?)\s+[^a-z\n]+)\n",  # UPPERCASE, no empty line may follow
        end_of_concl=default_end_of_concl,
        removestuff=(r"\n\n\d+\n\n",  # page number
                     r"\x0c.+\n\n.+"),  # page header
        applies_to=[ep.is_acmconf_icse, ]),
    acmtrans=dict(
        laparams=pdfl.LAParams(),
        section_heading=r"\n\n?((\d\d?)\s+[^a-z\n]{3,200})\n\n?",  # no empty line may follow nor precede!
        end_of_concl=default_end_of_concl,
        removestuff=(r"\n\n\x0c.*\n",  # page header
                     r"\n\n\d+:\d+\n",  # page number if split off of page header
                     r"\n\nACM Transactions .+20\d\d\.?\n\n",  # page header without formfeed
                     ),
        applies_to=["TOSEM", ]),
    elsevier=dict(
        laparams=pdfl.LAParams(),
        section_heading=r"\n\n((\d\d?)\. .+)\n\n",  # number ends with dot
        end_of_concl=default_end_of_concl,
        removestuff=(r"\nInformationandSoftwareTechnology.+\x0c.+\n\n",
                    ),
        applies_to=["IST", ]),
    ieeeconf=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,  # not so! to be done
        end_of_concl=default_end_of_concl,
        removestuff=(),
        applies_to=[ep.is_ieeeconf_icse, ]),
    ieeetrans=dict(
        laparams=pdfl.LAParams(),
        section_heading=r"\n\n((\d\d?)\s+[^a-z\n]+)\n",  # UPPERCASE, no empty line may follow
        end_of_concl=default_end_of_concl,
        removestuff=(r"\n\x0c.+\n\n\d+\n\n",  # page header left
                     r"\n\x0c\d+\n\n.+(TRANSACTIONS|:).+\n\n",  # page header right
                    ),
        applies_to=["TSE", ]),
    springer=dict(
        laparams=pdfl.LAParams(),
        section_heading=default_section_heading,
        end_of_concl=default_end_of_concl,
        removestuff=(r"(\x0c|\n)\d+\s+Page\s+\d+\s+of\s+\d+\n\n",
                     r"(\x0c|\n)Empir\s+Software\s+Eng\s\(20\d\d\)\s+\d+:\s?\d+\n\n"),
        applies_to=["EMSE", ]),
)


def conclusion_from_pdf(layout: ep.LayoutDescriptor, pdffile: str) -> str:
    out = io.StringIO()
    with open(pdffile, 'rb') as f:
        pdfhl.extract_text_to_fp(f, out, laparams=layout['laparams'], 
                                 output_type='text', codec="")
    txt = ep.more_readable(out.getvalue())
    # print("###pre-removestuff:", txt)
    txt = ep.remove_stuff(txt, layout['removestuff'])
    # print("###post-removestuff:", txt)
    headings_mms = find_headings([mm for mm in re.finditer(layout['section_heading'], txt)])
    headings_txt = "".join([f"# {mm.group(1)}\n" for mm in headings_mms])
    # print("###headings:", layout['section_heading'], '\n', headings_txt)
    conclusion_plus_rest = txt[headings_mms[-1].start(1):]
    mm = re.search(layout['end_of_concl'], conclusion_plus_rest)
    concl_endpos = mm.start() if mm else len(conclusion_plus_rest)-1
    return "\n%s.\n\n%s" % (headings_txt, conclusion_plus_rest[:concl_endpos])


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
        if thisnumber > lastnumber and thisnumber <= lastnumber+1:
            # Allow gaps of 1 to accomodate occasional multiline-long headings? Better not.
            result.append(mm)
            lastnumber = thisnumber
    return result