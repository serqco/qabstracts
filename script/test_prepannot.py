# pytest tests

import pytest

import prepannot as p

ann = "\n{{}}\n"
tests = [
    ("## normal sentences, no newline", 
       "First sentence. Second sentence.", 
       f"First sentence.{ann}Second sentence.{ann}"),
    ("## normal sentences, newline at end", 
       "First sentence. Second sentence.\n", 
       f"First sentence.{ann}Second sentence.{ann}"),
    ("## colon", 
       "First: a sentence.",
       f"First:{ann}a sentence.{ann}"),
    ("## multi-whitespace", 
       "First: \n Second \n\n  ",
       f"First:{ann}Second{ann}"),
    ("## missing blank", 
       "Sentence One.Sentence Two.",
       f"Sentence One.Sentence Two.{ann}"),
    ("## missing dot at end", 
       "One sentence",
       f"One sentence{ann}"),
    ("## e.g.", 
       "A, e.g. B.",
       f"A, e.g. B.{ann}"),
    ("## i.e.", 
       "A, i.e. B.",
       f"A, i.e. B.{ann}"),
    ("## I.e.", 
       "I.e. B.",
       f"I.e. B.{ann}"),
]


def test_all_tests():
    for name, input, output in tests:
        myoutput = p.prepared(input)
        print(f"{name}\nINPUT :{input}\nEXPECT:{output}ACTUAL:{myoutput}---\n")
        assert myoutput == output
