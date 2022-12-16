import argparse
import re
import typing as tg

import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt

usage = """Computes derived data and creates plots and stats outputs.
  Reads data created by 'export'. Computes many derived data sets.
  Creates plots from them in outputdir.
"""


def configure_argparser(p_prepare_ann: argparse.ArgumentParser):
    p_prepare_ann.add_argument('datafile',
                               help="Data as created by 'export'")
    p_prepare_ann.add_argument('outputdir',
                               help="Directory where plot files will be placed")


def plot(datafile: str, outputdir: str):
    df = read_datafile(datafile)
    datasets = create_datasets(df)
    create_plots(datasets, outputdir)


def read_datafile(datafile: str) -> pd.DataFrame:
    df = pd.read_csv(datafile, sep='\t', index_col=False)
    return df


def create_datasets(df: pd.DataFrame):
    datasets = argparse.Namespace()
    datasets.df = df  # the raw datafile
    datasets.df_primary1 = df.query('words > 0 and coder == "A"')  # no auxiliary codes, only 1 coder
    datasets.by_abstract = by_abstract(datasets.df_primary1)
    datasets.abs_structures = abstracts_structures(df)
    return datasets


def by_abstract(df: pd.DataFrame) -> pd.DataFrame:
    df.groupby('citekey') \
        .aggregate()
    

def abstracts_structures(df: pd.DataFrame) -> pd.DataFrame:
    strucs = df[df['topic'] != 'other'] \
        .groupby(['citekey', 'coder'])[['citekey', 'coder', 'topic']] \
        .aggregate(firstletters)
    # print(strucs)
    return strucs


def firstletters(vals: pd.Series) -> str:
    """Find topic block sequence: Turns (background, background, objective) into 'bo' etc."""
    result = []
    prevletter = ""
    for val in vals:
        if val[0] != prevletter:
            result.append(val[0])
            prevletter = val[0]
    return "".join(result)


def create_plots(datasets: argparse.Namespace, outputdir: str):
    mpl.use('PDF')
    create_structures_histogram(datasets.abs_structures, outputdir)


def create_structures_histogram(df: pd.DataFrame, outputdir: str):
    freqs = df['topic'].value_counts()
    topfreqs = freqs[freqs > 1]
    print(topfreqs)
    plt.grid(axis='y', linewidth=0.1)
    plt.bar(range(len(topfreqs)), topfreqs, tick_label=topfreqs.index)
    plt.xticks(rotation=-30, ha="left")
    plt.yticks(step=2)
    plt.xlabel("abstract structure")
    plt.ylabel("frequency")
    plt.subplots_adjust(bottom=0.18)
    plt.savefig(f"{outputdir}/abstract_structure_freqs.pdf")


if __name__ == '__main__':
    # for tryout during development
    ...
