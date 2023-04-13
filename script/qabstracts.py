#!/usr/bin/env python3

import argparse

import qabs.select_sample
import qabs.prepare_sample
import qabs.fix_encoding
import qabs.check_codings
import qabs.compare_codings
import qabs.export
import qabs.extract_abs
import qabs.extract_concl
import qabs.plot
import qabs.prepare_ann 

def main():  # uses sys.argv
    argparser = setup_argparser()
    pargs = argparser.parse_args()
    subcmd = pargs.subcmd
    if subcmd == "select-sample":
        qabs.select_sample.select_sample(pargs.size, pargs.blocksize, pargs.to, pargs.volume)
    elif subcmd == "prepare-sample":
        qabs.prepare_sample.prepare_sample(pargs.whatpart, pargs.workdir, pargs.volumedir, pargs.remainder)
    elif subcmd == "fix-encoding":
        qabs.fix_encoding.fix_encoding(pargs.files)
    elif subcmd == "check-codings":
        qabs.check_codings.check_codings(pargs.workdir)
    elif subcmd == "compare-codings":
        qabs.compare_codings.compare_codings(pargs.maxcountdiff, pargs.onlyfor, pargs.workdir)
    elif subcmd == "export":
        qabs.export.export(pargs.workdir)
    elif subcmd == "extract-abs":
        qabs.extract_abs.extract_abs(pargs.outputdir, pargs.layout, pargs.inputfile)
    elif subcmd == "extract-concl":
        qabs.extract_concl.extract_concl(pargs.outputdir, pargs.layout, pargs.inputfile)
    elif subcmd == "plot":
        qabs.plot.plot(pargs.plotall, pargs.datafile, pargs.outputdir)
    elif subcmd == "prepare-ann":
        qabs.prepare_ann.prepare_annotations(pargs.outputdir, pargs.textfile)
    else:
        assert False, f"unknown command: {subcmd}"  # the above list is not complete


def setup_argparser():
    description = "Handles PDF files, abstracts files, and annotations in various ways."
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # TODO: does nothing?
    subparsers = parser.add_subparsers(dest='subcmd', required=True)

    subparser = subparsers.add_parser('select-sample',
            help="Get block-randomized articles list of given size")
    qabs.select_sample.configure_argparser(subparser)

    subparser = subparsers.add_parser('prepare-sample',
            help="Get and prepare abstracts (after select-sample)")
    qabs.prepare_sample.configure_argparser(subparser)

    subparser = subparsers.add_parser('fix-encoding',
            help="Make sure all files are readable as UTF-8")
    qabs.fix_encoding.configure_argparser(subparser)

    subparser = subparsers.add_parser('check-codings',
            help="Check annotated abstracts for unallowed syntax and undefined codes")
    qabs.check_codings.configure_argparser(subparser)

    subparser = subparsers.add_parser('compare-codings',
            help="Cross-check pairs of corresponding annotated abstracts from different coders")
    qabs.compare_codings.configure_argparser(subparser)

    subparser = subparsers.add_parser('export',
            help="Create TSV data file with one record per coding")
    qabs.export.configure_argparser(subparser)

    subparser = subparsers.add_parser('extract-abs',
            help="Extract abstracts from PDF files")
    qabs.extract_abs.configure_argparser(subparser)

    subparser = subparsers.add_parser('extract-concl',
            help="Extract conclusion sections from PDF files")
    qabs.extract_concl.configure_argparser(subparser)

    subparser = subparsers.add_parser('plot',
            help=qabs.plot.usage)
    qabs.plot.configure_argparser(subparser)

    subparser = subparsers.add_parser('prepare-ann',
            help=qabs.prepare_ann.usage)  # insert empty annotations in abstracts files
    qabs.prepare_ann.configure_argparser(subparser)

    return parser


if __name__ == "__main__":
    main()