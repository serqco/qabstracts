#!/usr/bin/env python3

import qscript.argparse_subcommand
import qscript.cmd.check_codings
import qscript.cmd.compare_codings
import qscript.cmd.fix_encoding
import qscript.cmd.prepare_ann 
import qscript.cmd.select_sample
import qconcl.extract_concl
import qconcl.prepare_sample

explanation = """Handles various steps of the qconclusions study."""


def main():
    parser = qscript.argparse_subcommand.ArgumentParser(epilog=explanation)
    parser.scan(qscript.cmd.select_sample,
                qscript.cmd.fix_encoding,
                qscript.cmd.check_codings,
                qscript.cmd.compare_codings,
                qconcl.extract_concl,
                qconcl.prepare_sample,
                strict=True)
    parser.execute_subcommand()


if __name__ == "__main__":
    main()