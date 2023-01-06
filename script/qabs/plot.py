import argparse
import math
import traceback
import typing as tg

import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt

usage = """Computes derived data and creates plots and stats outputs.
  Reads data created by 'export'. Computes many derived data sets.
  Creates plots in outputdir.
"""

# Terminology: ab=abstract(s)  df=dataframe  freq=frequency  struc=structured

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
    """Input data w/o 'extra' codes, plus some helper columns"""
    res = df.query('words > 0').copy()  # suppress the auxiliary codes (extra codes)
    res['is_struc'] = res.code.str.contains('^h-')  # per-sentence entry, must be aggregated
    res['is_design'] = res.code == 'design'  # per-sentence entry, must be aggregated
    return res


def df_by_ab(primary: pd.DataFrame) -> pd.DataFrame:
    #----- do basic aggregation from codings to abstracts:
    res = primary.groupby(['citekey', 'coder']) \
        .agg(venue=_nagg('venue', 'min'),
             volume=_nagg('volume', 'min'),
             codername=_nagg('codername', 'min'),
             sentences=_nagg('sidx', 'max'),
             words=_nagg('words', 'sum'), 
             chars=_nagg('chars', 'sum'), 
             codes=_nagg('code', 'count'), 
             utopics=_nagg('topic', 'nunique'),
             icount=_nagg('icount', 'sum'), 
             ucount=_nagg('ucount', 'sum'),
             is_struc=_nagg('is_struc', 'any'), 
             is_design=_nagg('is_design', 'any'))
    #----- add derived variables:
    topicparts = primary.groupby(['citekey', 'coder', 'topic']).agg(
            topicwords=_nagg('words', 'sum'),
    )
    def add_fraction_x(res: pd.DataFrame, x: str) -> pd.DataFrame:
        res = pd.merge(res, topicparts.query(f"topic=='{x}'"), 'left', on=('citekey','coder'))
        res = res.rename(columns=dict(topicwords=f'words_{x}'), errors="raise")
        res[f'fraction_{x}'] = (100 * res[f'words_{x}'] / res.words).fillna(0)
        return res
    res = add_fraction_x(res, 'background')
    res = add_fraction_x(res, 'conclusion')
    res = add_fraction_x(res, 'other')
    return res

def ser_ab_structures(df: pd.DataFrame) -> pd.DataFrame:
    strucs = df[df['topic'] != 'other'] \
        .groupby(['citekey', 'coder'])[['topic', 'is_struc']] \
        .aggregate(
            topicstructure=_nagg('topic', firstletters),
            is_struc=_nagg('is_struc', 'any'))
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
    # print_abtype_table(datasets.by_ab)
    ...

def print_abtype_table(df: pd.DataFrame):
    _printheader()
    res = df.groupby(['is_struc', 'is_design']).count()["venue"]  # pick _any_ 1 column
    print(res)


def create_all_plots(datasets: argparse.Namespace, outputdir: str):
    mpl.use('PDF')
    # plot_ab_topicstructure_freqs(datasets.ab_structures, outputdir)
    # plot_boxplots(datasets.by_ab, 'words', outputdir)
    # plot_boxplots(datasets.by_ab, 'icount', outputdir, ymax=10)
    # plot_boxplots(datasets.by_ab, 'ucount', outputdir, ymax=10)
    # plot_boxplots(datasets.by_ab, 'sentences', outputdir, ymax=20)
    plot_boxplots(datasets.by_ab, 'fraction_background', outputdir, ymax=100)
    plot_boxplots(datasets.by_ab, 'fraction_conclusion', outputdir, ymax=100)
    plot_boxplots(datasets.by_ab, 'fraction_other', outputdir, ymax=100)

def plot_ab_topicstructure_freqs(df: pd.DataFrame, outputdir: str):
    """Barplot of how often the most common train-of-thought structures occur."""
    plt.figure()
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


def plot_boxplots(df: pd.DataFrame, which: str, outputdir: str, *, ymax=None):
    """Draw boxplots for all abstracts, structured/unstructured ones, and per venue."""
    #----- prepare data:
    vals = df[which]
    groups = df.groupby('venue')
    wherewhat = [ # the list of boxplots to be made, extended by the loop below:
                  (1, "all", vals), 
                  (2.5, "struc", vals[df.is_struc & ~df.is_design]),
                  (3.5, "unstruc", vals[~df.is_struc & ~df.is_design]),
                  (4.5, "design", vals[df.is_design]),
                ]
    x = 6  # third group of plots starts after a gap
    for name, group in groups:
        wherewhat.append((x, name, vals[group.index]))
        x += 1
    #----- configure boxplots:
    plt.figure()
    plt.boxplot([vals for x, lab, vals in wherewhat], 
            notch=False, whis=(5, 95), 
            positions=[x for x, lab, vals in wherewhat], 
            labels=[lab for x, lab, vals in wherewhat], 
            widths=0.7, capwidths=0.2,
            showfliers=False, showmeans=True,
            patch_artist=True, boxprops=dict(facecolor="yellow"),
            medianprops=dict(color='black'),
            meanprops=dict(marker='o', markerfacecolor='mediumblue', markeredgecolor='mediumblue'))
    plt.ylim(bottom=0, top=ymax)
    plt.ylabel(which)
    plt.grid(axis='y', linewidth=0.1)
    #----- add "n=123" at the bottom:
    for x, lab, vals in wherewhat:
        plt.text(x, 0, "n=%d" % len(vals), 
                 verticalalignment='bottom', horizontalalignment='center', color='mediumblue', fontsize=8)
    #----- add error bars for the mean:
    for x, lab, vals in wherewhat:
        mymean = vals.mean()
        se = vals.std() / math.sqrt(len(vals))  # standard error of the mean
        plt.vlines(x+0.1, mymean-se, mymean+se, 
                   colors='red', linestyles='solid', linewidth=0.7)
    plt.savefig(_plotfilename(outputdir, name_suffix=which))


def _funcname(levels_up: int) -> str:
    """The name of the function levels_up levels further up on the stack"""
    return traceback.extract_stack(limit=levels_up+1)[0].name


def _nagg(colname, func) -> pd.NamedAgg:
    """Abbreviation for pd.NamedAgg."""
    return pd.NamedAgg(column=colname, aggfunc=func)


def _plotfilename(outputdir: str, name_suffix="") -> str:
    """Filename derived from function name two stackframes up."""
    if name_suffix:
        name_suffix = "_" + name_suffix
    return "%s/%s%s.pdf" % (outputdir, _funcname(2).replace('plot_', ''), name_suffix)


def _printheader():
    """Print separator header giving the function name from two stackframes up."""
    print("##########", _funcname(2))


if __name__ == '__main__':
    # for tryout during development
    ...
