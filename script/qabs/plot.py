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
    res = df.groupby(['citekey', 'coder']) \
        .agg(dict(venue='min', volume='min', coder='min', codername='min',
                  sidx='max', words='sum', chars='sum', 
                  code='count', topic='nunique', 
                  icount='sum', ucount='sum',
                  is_struc='any'))
    res.columns = ['venue', 'volume', 'coder', 'codername',
                   'sentences', 'words', 'chars', 'codes', 'utopics', 'icount', 'ucount', 
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
    # plot_ab_topicstructure_freqs(datasets.ab_structures, outputdir)
    # plot_boxplots(datasets.by_ab, 'words', outputdir)
    # plot_boxplots(datasets.by_ab, 'icount', outputdir)
    # plot_boxplots(datasets.by_ab, 'ucount', outputdir)
    plot_boxplots(datasets.by_ab, 'sentences', outputdir)

def plot_ab_topicstructure_freqs(df: pd.DataFrame, outputdir: str):
    """Barplot of how often the most common train-of-thought structures occur."""
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


def plot_boxplots(df: pd.DataFrame, which: tg.Union[str, tg.Tuple[callable, str]], outputdir: str):
    """Draw boxplots for all abstracts, structured/unstructured ones, and per venue."""
    #----- prepare data:
    vals = df[which] if isinstance(which, str) else which[0](df)
    name_suffix = which if isinstance(which, str) else which[1]
    groups = df.groupby('venue')
    wherewhat = [ # the list of boxplots to be made, extended by the loop below:
                  (1, "all", vals), 
                  (2.5, "struc", vals[df.is_struc]), (3.5, "unstruc", vals[~df.is_struc]),
                ]
    x = 5  # third group of plots starts after a gap
    for name, group in groups:
        myvals = vals[group.index]
        wherewhat.append((x, name, myvals))
        x += 1
    #----- configure boxplots:
    theplot = plt.boxplot([vals for x, lab, vals in wherewhat], 
                notch=False, whis=(5, 95), 
                positions=[x for x, lab, vals in wherewhat], 
                labels=[lab for x, lab, vals in wherewhat], 
                widths=0.7, capwidths=0.2,
                showfliers=False, showmeans=True,
                patch_artist=True, boxprops=dict(facecolor="yellow"),
                medianprops=dict(color='black'),
                meanprops=dict(marker='o', markerfacecolor='mediumblue', markeredgecolor='mediumblue'))
    plt.ylim(bottom=0)
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
    plt.savefig(_plotfilename(outputdir, name_suffix=name_suffix))


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
