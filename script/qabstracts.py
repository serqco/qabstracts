#!/bin/env python3

import argparse

import qabs.prepare_ann

def main():  # uses sys.argv
    argparser = setup_argparser()
    pargs = argparser.parse_args()
    subcmd = pargs.subcmd
    if subcmd == "extract-abs":
        ...
    elif subcmd == "prepare-ann":
        qabs.prepare_ann.prepare_annotations(pargs.outputdir, pargs.textfile)
    else:
        assert False  # the above list is not complete


def setup_argparser():
    description = "Handles PDF files, abstracts files, and annotations in various ways."
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest='subcmd', required=True)

    p_extract_abs = subparsers.add_parser('extract-abs',
            help="extract abstracts from PDF files")
    p_extract_abs.add_argument('outputdir',
            help="directory where abstracts files will be placed")
    p_extract_abs.add_argument('pdffile', nargs='+',
            help="PDF file to scan for its abstract")

    p_prepare_ann = subparsers.add_parser('prepare-ann',
            # help="insert empty annotations in copies of abstracts files")
            help=qabs.prepare_ann.usage)
    p_prepare_ann.add_argument('outputdir',
            help="directory where prepared files will be placed")
    p_prepare_ann.add_argument('textfile', nargs='+',
            help="*.txt file to line-split by sentence and insert empty {{}} into")

    return parser


if __name__ == "__main__":
    main()