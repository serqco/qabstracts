#!/usr/bin/env python3

import qscript.argparse_subcommand
import qabs.export
import qabs.extract_abs
import qabs.plot
import qabs.prepare_sample

explanation = """Handles various steps of the qabstracts study."""


def main():
    parser = qscript.argparse_subcommand.ArgumentParser(epilog=explanation)
    parser.scan("qscript.cmd.*",
                qabs.export,
                qabs.extract_abs,
                qabs.plot,
                qabs.prepare_sample,
                strict=True)
    parser.execute_subcommand()


if __name__ == "__main__":
    main()