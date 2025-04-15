import argparse
import datetime as dt
import json
import subprocess
import typing as tg

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, dates as mdates

import qscript.plottypes as pt
import qscript
import qabs.dataframes
import qabs.extract_git_timestamps
import qabs.printstats

tse_columnwidth_mm = 88
tse_pagewidth_mm = 180
meaning = """Computes derived data and creates plots and stats outputs.
  Reads data created by 'export'. Computes many derived data sets.
  Creates plots in outputdir.
"""

# Terminology: ab=abstract(s)  df=dataframe  freq=frequency  struc=structured


def add_arguments(subparser: qscript.ArgumentParser):
    subparser.add_argument('--plotall', action='store_const', const=True,
                           help="run all plots, not only those currently under development")
    subparser.add_argument('--printall', action='store_const', const=True,
                           help="print all text outputs, not only those currently under development")
    subparser.add_argument('--withoutdesignworks', type=str, default="",
                           metavar="sample-who-what.txt",
                           help="ad-hoc extension for preparing qconclusions:\n"
                                "comment-out all entries of the qconclusion workfile that\n"
                                "belong to abstracts we have judged to be clearly design works.\n"
                           )
    subparser.add_argument('datafile',
                           help="Data as created by 'export'")
    subparser.add_argument('outputdir',
                           help="Directory where plot files will be placed")


def execute(args: qscript.Namespace):
    df = read_datafile(args.datafile)
    datasets = qabs.dataframes.create_all_datasets(df)
    with open(qabs.extract_git_timestamps.git_timestamp_file, 'rt', encoding='utf8') as f:
        datasets.timestamps = json.load(f)
    qabs.dataframes.create_all_subsets(datasets)
    qabs.printstats.print_all_stats(args, datasets, args.outputdir)
    create_all_plots(args.plotall, datasets, args.outputdir)


def read_datafile(datafile: str) -> pd.DataFrame:
    df = pd.read_csv(datafile, sep='\t', index_col=False)
    return df


def create_all_plots(plotall: bool, datasets: argparse.Namespace, outputdir: str):
    # mpl.use('PDF')
    height1 = 60/25.4
    wideplot = tse_pagewidth_mm/25.4
    onecolumnplot = tse_columnwidth_mm/25.4
    if plotall:
        # ----- topicstructure plots:
        plot_ab_topicstructure_freqs_design(datasets.ab_structures, outputdir)
        plot_ab_topicstructure_freqs_empir(datasets.ab_structures, outputdir)
        plot_ab_topicstructure_freqs_empir_structured(datasets.ab_structures, outputdir)
        # ----- boxplots counts:
        ctx = pt.PlotContext(outputdir, "", datasets.by_abstract, 
                             60/25.4, tse_pagewidth_mm/25.4, datasets.ab_subsets)
        pt.plot_boxplots(ctx, 'sentences', ymax=25)
        pt.plot_boxplots(ctx, 'words', ymax=500)
        pt.plot_boxplots(ctx, 'avg_wordlength', ymax=8)
        pt.plot_boxplots(ctx, 'fkscore', ymax=50)
        pt.plot_boxplots(ctx, 'icount', ymax=10)
        pt.plot_boxplots(ctx, 'ucount', ymax=10)
        # ----- boxplots fractions:
        pt.plot_boxplots(ctx, 'fraction_introduction', ymax=100)
        pt.plot_boxplots(ctx, 'fraction_conclusion', ymax=100)
        pt.plot_boxplots(ctx, 'fraction_other', ymax=100)
        pt.plot_lowess(datasets.by_abstract.fraction_introduction, "space for introduction [%]",
                       datasets.by_abstract.total_gaps, "#gaps",
                       outputdir, "gaps_by_fracintro",
                       xmax=100, ymax=15, frac=0.75)
        # ----- topicfraction plots:
        ctx = pt.PlotContext(outputdir, "", datasets.by_abstract, height1, wideplot, 
                             datasets.ab_topicfractions_values, datasets.ab_subsets)
        pt.plot_xletgroups(ctx, pt.add_boxplotlet, "box", "topicfractions",
                           "space per topic [%]", ymax=50)
        ctx = pt.PlotContext(outputdir, "", datasets.by_abstract_coding, height1, wideplot,
                             datasets.ab_topicfractions0_values, datasets.ab_subsets)
        pt.plot_xletgroups(ctx, pt.add_zerofractionbarplotlet_with_errorbars, "zerofractionbar", "topicmissingfractions",
                           "how often missing [%]", ymax=100)
        # ----- frequency of a-* codes and iu gaps:
        ctx = pt.PlotContext(outputdir, "", datasets.by_abstract_coding, height1, wideplot,
                             datasets.ab_missinginfofractions_values, datasets.ab_subsets)
        pt.plot_xletgroups(ctx, pt.add_nonzerofractionbarplotlet_with_errorbars, "nonzerofractionbar", "missinginfofractions",
                           "how often occurring [%]", ymax=75)
        ctx = pt.PlotContext(outputdir, "", datasets.by_abstract, height1, onecolumnplot, 
                             datasets.ab_conclusionfractions_bybg_values, datasets.ab_subsets)
        pt.plot_xletgroups(ctx, pt.add_boxplotlet, "box", "conclusionfractions",
                           "space per topic [%]", ymax=30)
        # ----- timeline:
        plot_qabstracts_timeline_commits(outputdir, datasets.timestamps)
    
    # ----- fraction of complete and of proper abstracts:
    ctx = pt.PlotContext(outputdir, "", datasets.by_abstract_coding, height1, onecolumnplot,
                         datasets.ab_totalqualityfractions_values, datasets.ab_subsets)
    pt.plot_xletgroups(ctx, pt.add_nonzerofractionbarplotlet_with_errorbars, "nonzerofractionbar", "totalqualityfractions",
                       "how often occurring [%]", ymax=65)


def plot_ab_topicstructure_freqs_design(df: pd.DataFrame, outputdir: str):
    design_df = df.loc[df['topicstructure'].str.contains('d')]
    plot_ab_topicstructure_freqs(design_df, outputdir)


def plot_ab_topicstructure_freqs_empir(df: pd.DataFrame, outputdir: str):
    empir_df = df.loc[~df['topicstructure'].str.contains('d')]
    plot_ab_topicstructure_freqs(empir_df, outputdir)


def plot_ab_topicstructure_freqs_empir_structured(df: pd.DataFrame, outputdir: str):
    dfstruc = df.loc[df.is_struc]
    empir_df = dfstruc.loc[~dfstruc['topicstructure'].str.contains('d')]
    plot_ab_topicstructure_freqs(empir_df, outputdir)


def plot_ab_topicstructure_freqs(df: pd.DataFrame, outputdir: str):
    """Barplot of how often the most common train-of-thought structures occur."""
    plt.figure()
    freqs = df.topicstructure.value_counts() / 2  # each abstract is coded twice, but should count only 1
    topfreqs = freqs[freqs > 2]
    plt.grid(axis='y', linewidth=0.1)
    plt.bar(range(len(topfreqs)), topfreqs, tick_label=topfreqs.index)
    plt.xticks(rotation=-30, ha="left")
    plt.yticks(range(0, int(topfreqs.max()+1), 2))
    plt.xlabel("abstracts' structure")
    plt.ylabel("frequency")
    plt.subplots_adjust(bottom=0.18)
    filename = pt.plotfilename(outputdir, nesting=1)
    plt.savefig(filename)


def plot_qabstracts_timeline_commits(outputdir: str, all_timestamps: dict[str,list[int]]):
    """stripplots of the timestamps of various subsets of git commits"""
    # ----- configs of the stripplots:
    cases = qabs.extract_git_timestamps.git_timestamp_cases
    # ----- set up the plot:
    fig, axs = plt.subplots()
    axs.set_yticks([y for y, l, s, f in cases], [l for y, l, s, f in cases])
    axs.set_xlim(dt.date(2022, 6, 1), dt.date(2025, 1, 15))
    # fix label frequency: https://matplotlib.org/stable/gallery/text_labels_and_annotations/date.html
    axs.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    axs.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=range(1, 12+1)))
    axs.grid(axis='x', linestyle=':')
    # ----- plot the stripplots:
    for y, label, symbol, files in cases:
        datetimes = [dt.datetime.fromtimestamp(ts) for ts in all_timestamps[files]]
        ys = np.random.uniform(low=y-0.2, high=y+0.2, size=len(datetimes))
        axs.scatter(datetimes, ys, marker=f"${symbol}$", linewidths=0.1, s=20)  # noqa
    # ----- save the plot:
    plt.savefig(pt.plotfilename(outputdir))


if __name__ == '__main__':
    # for tryout during development
    ...
