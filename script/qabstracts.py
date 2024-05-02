#!/usr/bin/env python3

import qscript.annotations as qa 
import qscript.argparse_subcommand
import qscript.cmd.compare_codings as qccc
import qscript.icc as icc

import qabs.annotations_abs as qaa
import qabs.compare_codings_abs as qcca
import qabs.export
import qabs.extract_abs
import qabs.extract_git_timestamps
import qabs.plot
import qabs.prepare_sample

explanation = """Handles various steps of the qabstracts study."""


def main():
    register_implclasses()
    parser = qscript.argparse_subcommand.ArgumentParser(epilog=explanation)
    parser.scan("qscript.cmd.*",
                qabs.export,
                qabs.extract_abs,
                qabs.extract_git_timestamps,
                qabs.plot,
                qabs.prepare_sample,
                strict=True)
    parser.execute_subcommand()


def register_implclasses():
    icc.register_class(qa.Codebook, qaa.CodebookAbstracts)
    icc.register_class(qa.Annotations, qaa.AnnotationsAbstracts)
    icc.register_class(qccc.CodingsComparator, qcca.CodingsComparatorAbstracts)


if __name__ == "__main__":
    main()