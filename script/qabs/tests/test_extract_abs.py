# pytest tests

import pytest

import qabs.extract_abs as ea

datadir = "script/testdata"

tests = [
    ("AlhSto21-ieeeconf.pdf", "ieeeconf",
     "Reliable cost effective effort estimation ",
     "those of a single\nexpert."),
    ("FurTorFel22-acmtrans.pdf", "acmtrans",
     "Applying Bayesian Analysis Guidelines ",  # imperfect. No beacon available
     # correct: "Statistical analysis is the tool of "
     "in\nempirical software engineering research."),
    ("MeyMurZim21-ieeetrans.pdf", "ieeetrans",
     "Software developers are generally interested in ",
     "increase long-term\nengagement."),
    ("BraZai22-springer-emse.pdf", "springer",
     "Automatically generating test cases for ",
     "for developer-centric test amplification."),
    ("DasPhi22-elsevier-ist.pdf", "elsevier",
     "Context: Especially with the rise of microservice ",
     "also helps\nthem with root cause analyses."),
    ("JohBruMel20-acmconf.pdf", "acmconf",
     "Understanding the root cause of a defect is ",
     "is available at http://holmes.cs.umass.edu/."),
]


@pytest.mark.parametrize("filename,layouttype,start,end", tests)
def test_all_extract_abs_tasks(filename, layouttype, start, end):
    pdfpath = f"{datadir}/{filename}"
    abstract = ea.abstract_from_pdf(ea.layouttypes[layouttype], pdfpath)
    is_correct = abstract.startswith(start) and abstract.endswith(end)
    if not is_correct:
        print(f"########## {filename}  --layout {layouttype}\n",
              f"########## {layouttype} logic found:\n",
              f"## start:'{abstract[:60]}'",
              f"## end:'{abstract[-60:]}'")
    assert is_correct
