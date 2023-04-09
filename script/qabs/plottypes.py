"""
Infrastructure for plot.py:
- Helper classes for groupwise plots: data subsets handling
- Parameterized plotting routines
"""
import collections
import math
import os
import traceback
import typing as tg

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


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

    def __init__(self, outputdir, basename, df, height, width,
                 subsets=None, subsets_inner=None):
        self.outputdir = outputdir
        self.basename = basename
        self.df = df
        self.subsets = subsets
        self.subsets_inner = subsets_inner
        mpl.rcParams.update({'font.size': 8})
        figsize = (width, height)
        self.fig = mpl.figure.Figure(figsize=figsize, layout='constrained')
        self.ax = self.fig.add_subplot()

    def savefig(self):
        self.fig.savefig(os.path.join(self.outputdir, self.basename + '.pdf'))

    def again_for(self, basename: str):
        """Reuse for another plot: Clear Figure, set a different filename, else the same."""
        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.basename = basename


def plot_boxplots(ctx: PlotContext, which: str, *, ymax=None):
    """Draw boxplots for all abstracts, structured/unstructured ones, and per venue."""
    ctx.again_for(f"boxplots_{which}")
    ctx.ax.set_ylim(bottom=0, top=ymax)
    ctx.ax.set_ylabel(which)
    ctx.ax.grid(axis='y', linewidth=0.1)
    for name, descriptor in ctx.subsets.items():
        vals = descriptor.filter(ctx.df)[which]
        add_boxplot(ctx, vals, descriptor, name)
    ctx.savefig()


def add_boxplot(ctx, vals, descr, name):
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
    plt.savefig(plotfilename(outputdir, name_suffix=name_suffix))


def funcname(levels_up: int) -> str:
    """The name of the function levels_up levels further up on the stack"""
    return traceback.extract_stack(limit=levels_up+1)[0].name


def plotfilename(outputdir: str, name_suffix="") -> str:
    """Filename derived from function name two stackframes up."""
    if name_suffix:
        name_suffix = "_" + name_suffix
    return "%s/%s%s.pdf" % (outputdir, funcname(2).replace('plot_', ''), name_suffix)
