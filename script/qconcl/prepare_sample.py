import qscript.prepare_sample as prep

import qconcl.extract_concl as ec
import qscript

meaning = "Get and prepare conclusion sections (after select-sample)"


def add_arguments(subparser: qscript.ArgumentParser):
    prep.add_arguments(subparser)


def execute(args: qscript.Namespace):
    prep.execute_template(args, ec.conclusion_from_pdf, ec.layouttypes)
