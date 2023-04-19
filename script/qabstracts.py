#!/usr/bin/env python3


import qscript.cmd.select_sample
import qscript.cmd.prepare_sample
import qscript.cmd.fix_encoding
import qscript.cmd.check_codings
import qscript.cmd.compare_codings
import qabs.export
import qabs.extract_abs
import qabs.extract_concl
import qabs.plot
import qscript.cmd.prepare_ann 
import qscript.argparse_subcommand

explanation = """Handles various steps of the qabstracts study."""


def main():
    parser = qscript.argparse_subcommand.ArgumentParser(epilog=explanation)
    parser.scan(qscript.cmd.select_sample,
                qscript.cmd.prepare_sample,
                qscript.cmd.fix_encoding,
                qscript.cmd.check_codings,
                qscript.cmd.compare_codings,
                qabs.export,
                qabs.extract_abs,
                qabs.extract_concl,
                qabs.plot,
                strict=True)
    parser.execute_subcommand()


if __name__ == "__main__":
    main()