#!/usr/bin/env python3

import argparse

import qabs.select_sample
import qabs.extract_abs
import qabs.prepare_ann

def main():  # uses sys.argv
    argparser = setup_argparser()
    pargs = argparser.parse_args()
    subcmd = pargs.subcmd
    if subcmd == "select-sample":
        qabs.select_sample.select_sample(pargs.size, pargs.blocksize, pargs.to, pargs.volume)
    elif subcmd == "extract-abs":
        qabs.extract_abs.extract_abstracts(pargs.outputdir, pargs.layout, 
                                           pargs.inputfile)
    elif subcmd == "prepare-ann":
        qabs.prepare_ann.prepare_annotations(pargs.outputdir, pargs.textfile)
    else:
        assert False  # the above list is not complete


def setup_argparser():
    description = "Handles PDF files, abstracts files, and annotations in various ways."
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest='subcmd', required=True)

    p_select_sample = subparsers.add_parser('select-sample',
            help="Get block-randomized articles list of given size")
    qabs.select_sample.configure_argparser(p_select_sample)

    p_extract_abs = subparsers.add_parser('extract-abs',
            help="Extract abstracts from PDF files")
    qabs.extract_abs.configure_argparser(p_extract_abs)

    p_prepare_ann = subparsers.add_parser('prepare-ann',
            help=qabs.prepare_ann.usage)  # insert empty annotations in abstracts files
    qabs.prepare_ann.configure_argparser(p_prepare_ann)

    return parser


if __name__ == "__main__":
    main()