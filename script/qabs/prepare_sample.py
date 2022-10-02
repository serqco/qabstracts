import json
import os.path
import random
import typing as tg

import qabs.extract_abs
import qabs.listfiles as lf
import qabs.prepare_ann

def configure_argparser(subparser):
    subparser.add_argument('workdir', type=str,
                           help="directory where to find sample* files and where to place abstracts.A result dir")
    subparser.add_argument('--volumedir', metavar="dir", type=str, required=True,
                           help="target directory where to to find the volumes directories mentioned in 'sample.list'")


def prepare_sample(workdir: str, volumedir: str):
    targetdir = f"{workdir}/abstracts.A"
    #----- prepare directories:
    if os.path.exists(targetdir):
        raise ValueError(f"'{targetdir}' already exists. I will not overwrite it.")
    os.mkdir(targetdir)
    #----- obtain data:
    sample = lf.read_list(f'{workdir}/sample.list')
    with open(f"{workdir}/sample-titles.json") as f:
        titles = json.load(f)
    #----- create abstracts files:
    for article in sample[:2]:
        prepare_article(targetdir, volumedir, article, titles)


def prepare_article(targetdir: str, volumedir: str, article: lf.Entry, titles: tg.Mapping[str,str]):
    citekey = lf.citekey(article)
    targetfile = f"{targetdir}/{citekey}.txt"
    #----- obtain abstract:
    layouttype = qabs.extract_abs.decide_layouttype(article)
    print(f"{article}  (layouttype {layouttype})\t-> {targetfile}")
    abstract = qabs.extract_abs.abstract_from_pdf(f"{volumedir}/{article}", layouttype)  # may not be pure
    #----- annotate abstract and write abstract file:
    title = titles[citekey]
    annotated_abstract = qabs.prepare_ann.prepared(abstract)
    with open(targetfile, 'wt', encoding='utf8') as out:
        out.write(f"{title}\n\n{annotated_abstract}")
        out.write("---\n#inf-?\n#und-?\n")
