import argparse
import re
import traceback
import typing as tg

import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt

usage = """Computes derived data and creates plots and stats outputs.
  Reads data created by 'export'. Computes many derived data sets.
  Creates plots in outputdir.
"""

# Terminology: ab=abstract(s)  df=dataframe  freq=frequency

def configure_argparser(p_prepare_ann: argparse.ArgumentParser):
    p_prepare_ann.add_argument('datafile',
                               help="Data as created by 'export'")
    p_prepare_ann.add_argument('outputdir',
                               help="Directory where plot files will be placed")


def plot(datafile: str, outputdir: str):
    df = read_datafile(datafile)
    datasets = create_all_datasets(df)
    print_all_stats(datasets)
    create_all_plots(datasets, outputdir)


def read_datafile(datafile: str) -> pd.DataFrame:
    df = pd.read_csv(datafile, sep='\t', index_col=False)
    return df


def create_all_datasets(df: pd.DataFrame):
    datasets = argparse.Namespace()
    datasets.df = df  # the raw datafile
    datasets.df_primary1 = df_primary1(df)
    datasets.by_ab = df_by_ab(datasets.df_primary1)
    datasets.ab_structures = ser_ab_structures(datasets.df_primary1)
    return datasets


def df_primary1(df: pd.DataFrame) -> pd.DataFrame:
    res = df.query('words > 0').copy()  # no auxiliary codes
    res['is_struc'] = res.code.str.contains('^h-')  # per-sentence entry, must be aggregated
    return res


def df_by_ab(df: pd.DataFrame) -> pd.DataFrame:
    res = df.groupby(['citekey', 'venue']) \
        .agg(dict(sidx='max', words='sum', chars='sum', 
                  code='count', topic='nunique', 
                  icount='sum', ucount='sum',
                  is_struc='any'))
    res.columns = ['sentences', 'words', 'chars', 'codes', 'utopics', 'icount', 'ucount', 
                   'is_struc']
    return res


def ser_ab_structures(df: pd.DataFrame) -> pd.DataFrame:
    strucs = df[df['topic'] != 'other'] \
        .groupby(['citekey', 'coder'])[['topic', 'is_struc']] \
        .aggregate(
            topicstructure=_nagg('topic', firstletters),
            is_struc=_nagg('is_struc', 'any'))
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


def print_all_stats(datasets: argparse.Namespace):
    print_iu_sum_means(datasets.by_ab)


def print_iu_sum_means(df: pd.DataFrame):
    _printheader()
    res = df.groupby('is_struc').agg(dict(icount=['mean', 'median', 'max'], 
                                          ucount=['mean', 'median', 'max']))
    print(res)


def create_all_plots(datasets: argparse.Namespace, outputdir: str):
    mpl.use('PDF')
    plot_ab_topicstructure_freqs(datasets.ab_structures, outputdir)


def plot_ab_topicstructure_freqs(df: pd.DataFrame, outputdir: str):
    freqs = df.topicstructure.value_counts()
    topfreqs = freqs[freqs > 1]
    plt.grid(axis='y', linewidth=0.1)
    plt.bar(range(len(topfreqs)), topfreqs, tick_label=topfreqs.index)
    plt.xticks(rotation=-30, ha="left")
    plt.yticks(range(0, topfreqs.max()+1, 2))
    plt.xlabel("abstracts' structure")
    plt.ylabel("frequency")
    plt.subplots_adjust(bottom=0.18)
    plt.savefig(_plotfilename(outputdir))


def _funcname(levels_up: int) -> str:
    """The name of the function levels_up levels further up on the stack"""
    return traceback.extract_stack(limit=levels_up+1)[0].name


def _nagg(colname, func) -> pd.NamedAgg:
    return pd.NamedAgg(column=colname, aggfunc=func)


def _plotfilename(outputdir: str) -> str:
    return "%s/%s.pdf" % (outputdir, _funcname(2).replace('plot_', ''))


def _printheader():
    print("##########", _funcname(2))


if __name__ == '__main__':
    # for tryout during development
    ...
