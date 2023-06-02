#!/usr/bin/env python3

import qscript.annotations as qa 
import qscript.argparse_subcommand
import qscript.icc as icc

import qabs.annotations_abs as qaa
import qabs.export
import qabs.extract_abs
import qabs.plot
import qabs.prepare_sample

explanation = """Handles various steps of the qabstracts study."""


def main():
    register_implclasses()
    parser = qscript.argparse_subcommand.ArgumentParser(epilog=explanation)
    parser.scan("qscript.cmd.*",
                qabs.export,
                qabs.extract_abs,
                qabs.plot,
                qabs.prepare_sample,
                strict=True)
    parser.execute_subcommand()


def register_implclasses():
    icc.register_class(qa.Codebook, qaa.CodebookAbstracts)
    icc.register_class(qa.Annotations, qaa.AnnotationsAbstracts)

if __name__ == "__main__":
    main()