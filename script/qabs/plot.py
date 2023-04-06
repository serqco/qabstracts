import argparse
import collections
import math
import os
import traceback
import typing as tg

import pandas as pd
import matplotlib as mpl
import matplotlib.figure
import matplotlib.axes
from matplotlib import pyplot as plt

import qabs.annotations as annot

usage = """Computes derived data and creates plots and stats outputs.
  Reads data created by 'export'. Computes many derived data sets.
  Creates plots in outputdir.
"""

# Terminology: ab=abstract(s)  df=dataframe  freq=frequency  struc=structured


def configure_argparser(p_prepare_ann: argparse.ArgumentParser):
    p_prepare_ann.add_argument('--plotall', action='store_const', const=True,
                               help="run all plots, not only those currently under development")
    p_prepare_ann.add_argument('datafile',
                               help="Data as created by 'export'")
    p_prepare_ann.add_argument('outputdir',
                               help="Directory where plot files will be placed")


def plot(plotall: bool, datafile: str, outputdir: str):
    df = read_datafile(datafile)
    datasets = create_all_datasets(df)
    create_all_subsets(datasets)
    print_all_stats(datasets, outputdir)
    create_all_plots(plotall, datasets, outputdir)

tse_columnwidth_mm = 88
tse_pagewidth_mm = 180

class Subsets:
    """
    Define and handle overlapping subsets of something, e.g. rows in pd.Dataframes.
    Initialize by a mapping from group name to a df-filtering predicate 'filter' plus
    possibly other per-group attributes:
      ss = Subsets(dict(a=dict(filter=lambda df: df.a >= 0, color='red'),
                        b=dict(filter=lambda df: df.b <= 0, color='blue'))
    Then iterate over groups and retrieve their rows and other attributes, e.g.
      for name, descriptor in ss.items():
          somecall(descriptor['color'], descriptor.color, descriptor.filter(df).somecolumn.mean())
    or even
      ss.a.filter(df)
    In fact, the class knows nothing about Pandas, so instead of a Dataframe, you can use it with
    any other container or even a virtual collection.
    The class simply bundles a filter with several constants, bundles several such tuples
    into a single object, and provides nice syntax for accessing them.
    """

    def __init__(self, descriptor: tg.Mapping[str, tg.Mapping[str, tg.Any]]):
        # ----- copy subsets descriptor:
        self.descriptor = collections.OrderedDict()
        for name, descr in descriptor.items():
            self.descriptor[name] = self.Subset(descr)
        # ----- check consistency:
        self.attrs = set()
        for name, descr in self.descriptor.items():
            myattrs = set(descr.keys())
            if len(self.attrs) == 0:
                self.attrs = myattrs  # record the canonical set of attr names
                if 'filter' not in myattrs:
                    raise ValueError(f"subset '{name}' lacks required attribute 'filter': {myattrs}")
            if self.attrs > myattrs:
                raise ValueError(f"subset '{name}' has attributes missing: %s" %
                                 self.attrs - myattrs)
            if myattrs > self.attrs:
                raise ValueError(f"subset '{name}' has extra attributes: %s" %
                                 myattrs - self.attrs)

    def items(self):
        return self.descriptor.items()
    
    class Subset(dict):
        def __getattr__(self, attrname):
            """subset attributes become Python pseudo attributes"""
            return self[attrname]

    def __getattr__(self, attrname):
        """subset names become Python pseudo attributes holding a Subset object"""
        return self.descriptor[attrname]


class PlotContext:
    outputdir: str
    basename: str
    df: pd.DataFrame
    subsets: tg.Optional[Subsets] = None
    subsets_inner: tg.Optional[Subsets] = None
    fig: tg.Optional[mpl.figure.Figure] = None
    ax: tg.Optional[mpl.axes.Axes] = None

    def __init__(self, outputdir, basename, df, subsets=None, subsets_inner=None,
                 height=60 / 25.4, width=tse_pagewidth_mm / 25.4):
        self.outputdir = outputdir
        self.basename = basename
        self.df = df
        self.subsets = subsets
        self.subsets_inner = subsets_inner
        matplotlib.rcParams.update({'font.size': 8})
        self.fig = mpl.figure.Figure(figsize=(width, height), layout='constrained')
        self.ax = self.fig.add_subplot()

    def savefig(self):
        self.fig.savefig(os.path.join(self.outputdir, self.basename + '.pdf'))

    def again_for(self, basename: str):
        """Reuse for another plot: Clear Figure, set a different filename, else the same."""
        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.basename = basename


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
    res['is_announce'] = res.code.str.contains('^a-')  # per-sentence entry, must be counted
    res['is_struc'] = res.code.str.contains('^h-')  # per-sentence entry, must be aggregated
    res['is_design'] = res.code == 'design'  # per-sentence entry, must be aggregated
    return res


def df_by_ab(primary: pd.DataFrame) -> pd.DataFrame:
    # ----- do basic aggregation from codings to abstracts:
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
             announcecount=_nagg('is_announce', 'sum'),
             is_struc=_nagg('is_struc', 'any'), 
             is_design=_nagg('is_design', 'any'))
    # ----- add derived variables:
    topicparts = primary.groupby(['citekey', 'coder', 'topic']).agg(
            topicwords=_nagg('words', 'sum'),
    )

    def add_fraction_x(result: pd.DataFrame, x: str) -> pd.DataFrame:
        result = pd.merge(result, topicparts.query(f"topic=='{x}'"), 'left', on=('citekey', 'coder'))
        result = result.rename(columns=dict(topicwords=f'words_{x}'), errors="raise")
        result[f'fraction_{x}'] = (100 * result[f'words_{x}'] / result.words).fillna(0)
        return result

    res = add_fraction_x(res, 'background')
    res = add_fraction_x(res, 'gap')
    res = add_fraction_x(res, 'objective')
    res = add_fraction_x(res, 'design')
    res = add_fraction_x(res, 'method')
    res = add_fraction_x(res, 'result')
    res = add_fraction_x(res, 'summary')
    res = add_fraction_x(res, 'conclusion')
    res = add_fraction_x(res, 'future')
    res = add_fraction_x(res, 'other')
    res['fraction_introduction'] = res.fraction_background + res.fraction_gap
    res['total_gaps'] = res.icount + res.ucount + 3 * res.announcecount  # count each 'a-*' as 3 gaps
    return res


def ser_ab_structures(df: pd.DataFrame) -> pd.DataFrame:
    strucs = df[df['topic'] != 'other'] \
        .groupby(['citekey', 'coder'])[['topic', 'is_struc']] \
        .aggregate(
            topicstructure=_nagg('topic', topicletters),
            is_struc=_nagg('is_struc', 'any'))
    return strucs


def topicletters(topics: pd.Series) -> str:
    """Find topic block sequence: Turns (background, background, objective) into 'bo' etc."""
    result = []
    prevletter = ""
    for val in topics:
        if val == annot.Codebook.NONETOPIC:
            continue  # not to be part of our sequence
        if val[0] != prevletter:  # collapse stretches into a single letter
            result.append(val[0])
            prevletter = val[0]
    return "".join(result)


def create_all_subsets(datasets: argparse.Namespace):
    """Add Subsets entries in datasets."""
    ab_subsets_dict = dict(
        all=dict(
                x=1.0, 
                filter=lambda df: df.loc[df.is_struc | ~df.is_struc]),
        struc=dict(
                x=2.5,
                filter=lambda df: df.loc[df.is_struc]),
        unstruc=dict(
                x=3.5,
                filter=lambda df: df.loc[~df.is_struc]),
        design=dict(
                x=4.5,
                filter=lambda df: df.loc[df.is_design]),
        empir=dict(
            x=5.5,
            filter=lambda df: df.loc[~df.is_design]),
    )
    x = 7.0  # add per-venue subsets after a gap
    for venue in sorted(datasets.by_ab.venue.unique()):
        ab_subsets_dict[venue] = dict(
            x=x, filter=lambda df: df.loc[df.venue == venue]
        )
        x += 1.0
    datasets.ab_subsets = Subsets(ab_subsets_dict)


def print_all_stats(datasets: argparse.Namespace, outputdir: str):
    # print_abtype_table(datasets.by_ab)
    ...


def print_abtype_table(df: pd.DataFrame):
    _printheader()
    res = df.groupby(['is_struc', 'is_design']).count()["venue"]  # pick _any_ 1 column
    print(res)


def create_all_plots(plotall: bool, datasets: argparse.Namespace, outputdir: str):
    # mpl.use('PDF')
    if plotall:
        plot_ab_topicstructure_freqs(datasets.ab_structures, outputdir)
        ctx = PlotContext(outputdir, "", datasets.by_ab, datasets.ab_subsets)
        plot_boxplots(ctx, 'words', ymax=500)
        plot_boxplots(ctx, 'icount', ymax=10)
        plot_boxplots(ctx, 'ucount', ymax=10)
        plot_boxplots(ctx, 'sentences', ymax=25)
        plot_boxplots(ctx, 'fraction_introduction', ymax=100)
        plot_boxplots(ctx, 'fraction_conclusion', ymax=100)
        plot_boxplots(ctx, 'fraction_other', ymax=100)
        plot_lowess(datasets.by_ab.fraction_introduction, "space for introduction [%]",
                    datasets.by_ab.total_gaps, "#gaps", 
                    outputdir, "gaps_by_fracintro",
                    xmax=100, ymax=15, frac=0.75)


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


def plot_boxplots(ctx: PlotContext, which: str, *, ymax=None):
    """Draw boxplots for all abstracts, structured/unstructured ones, and per venue."""
    ctx.again_for(f"boxplots_{which}")
    ctx.ax.set_ylim(bottom=0, top=ymax)
    ctx.ax.set_ylabel(which)
    ctx.ax.grid(axis='y', linewidth=0.1)
    for name, descr in ctx.subsets.items():
        vals = descr.filter(ctx.df)[which]
        ctx.ax.boxplot(
                [vals], 
                notch=False, whis=(5, 95), 
                positions=[descr.x], labels=[name], 
                widths=0.7, capwidths=0.2,
                showfliers=False, showmeans=True,
                patch_artist=True, boxprops=dict(facecolor="yellow"),
                medianprops=dict(color='black'),
                meanprops=dict(marker='o', markerfacecolor='mediumblue', markeredgecolor='mediumblue'))
        # ----- add "n=123" at the bottom:
        ctx.ax.text(descr.x, 0, "n=%d" % len(vals), 
                    verticalalignment='bottom', horizontalalignment='center', color='mediumblue', 
                    fontsize=7)
        # ----- add error bar for the mean:
        mymean = vals.mean()
        se = vals.std() / math.sqrt(len(vals))  # standard error of the mean
        plt.vlines(descr.x + 0.1, mymean - se, mymean + se, 
                   colors='red', linestyles='solid', linewidth=0.7)
    ctx.savefig()


def plot_lowess(x: pd.Series, xlabel: str, y: pd.Series, ylabel: str,
                outputdir: str, name_suffix: str, *, 
                frac=0.67, show=True, xmax=None, ymax=None):
    # ----- compute lowess line:
    import statsmodels.nonparametric.smoothers_lowess as sml
    delta = 0.01 * (x.max() - x.min())
    line_xy = sml.lowess(y.to_numpy(), x.to_numpy(), frac=frac, delta=delta,
                         is_sorted=False)
    # ----- plot labeling:
    plt.figure()
    plt.xlim(left=0, right=xmax)
    plt.xlabel(xlabel)
    plt.ylim(bottom=0, top=ymax)
    plt.ylabel(ylabel)
    plt.grid(axis='both', linewidth=0.1)
    # ----- plot points:
    if show:
        plt.scatter(x, y, s=2, c="darkred")
    # ----- plot lowess line:
    # print(line_xy)
    plt.plot(line_xy[:, 0], line_xy[:, 1], )
    # ----- save:
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
