import qscript.prepare_sample as prep

import qabs.extract_abs as ea
import qscript

meaning = "Get and prepare abstracts (after select-sample)"


def add_arguments(subparser: qscript.ArgumentParser):
    prep.add_arguments(subparser)
    

def execute(args: qscript.Namespace):
    prep.execute_template(args, ea.abstract_from_pdf, ea.layouttypes)
