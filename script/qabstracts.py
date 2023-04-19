#!/usr/bin/env python3


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
import qscript.argparse_subcommand

explanation = """Handles various steps of the qabstracts study."""


def main():
    parser = qscript.argparse_subcommand.ArgumentParser(epilog=explanation)
    parser.scan(qabs.select_sample,
                qabs.prepare_sample,
                qabs.fix_encoding,
                qabs.check_codings,
                qabs.compare_codings,
                qabs.export,
                qabs.extract_abs,
                qabs.extract_concl,
                qabs.plot,
                strict=True)
    parser.execute_subcommand()


if __name__ == "__main__":
    main()