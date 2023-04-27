#!/usr/bin/env python3

import qscript.argparse_subcommand
import qconcl.extract_concl
import qconcl.prepare_sample

explanation = """Handles various steps of the qconclusions study."""


def main():
    parser = qscript.argparse_subcommand.ArgumentParser(epilog=explanation)
    parser.scan("qscript.cmd.*",
                qconcl.extract_concl,
                qconcl.prepare_sample,
                strict=True, trace=False)
    parser.execute_subcommand()


if __name__ == "__main__":
    main()