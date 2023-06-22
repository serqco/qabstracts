import argparse

import pandas as pd
from matplotlib import pyplot as plt

import qscript.plottypes as pt
import qscript
import qabs.dataframes
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
    qabs.dataframes.create_all_subsets(datasets)
    qabs.printstats.print_all_stats(args, datasets, args.outputdir)
    create_all_plots(args.plotall, datasets, args.outputdir)


def read_datafile(datafile: str) -> pd.DataFrame:
    df = pd.read_csv(datafile, sep='\t', index_col=False)
    return df


def create_all_plots(plotall: bool, datasets: argparse.Namespace, outputdir: str):
    # mpl.use('PDF')
    if plotall:
        plot_ab_topicstructure_freqs_design(datasets.ab_structures, outputdir)
        plot_ab_topicstructure_freqs_empir(datasets.ab_structures, outputdir)
        ctx = pt.PlotContext(outputdir, "", datasets.by_ab, 
                             60/25.4, tse_pagewidth_mm/25.4, datasets.ab_subsets)
        pt.plot_boxplots(ctx, 'words', ymax=500)
        pt.plot_boxplots(ctx, 'icount', ymax=10)
        pt.plot_boxplots(ctx, 'ucount', ymax=10)
        pt.plot_boxplots(ctx, 'sentences', ymax=25)
        pt.plot_boxplots(ctx, 'fraction_introduction', ymax=100)
        pt.plot_boxplots(ctx, 'fraction_conclusion', ymax=100)
        pt.plot_boxplots(ctx, 'fraction_other', ymax=100)
        pt.plot_lowess(datasets.by_ab.fraction_introduction, "space for introduction [%]",
                       datasets.by_ab.total_gaps, "#gaps",
                       outputdir, "gaps_by_fracintro",
                       xmax=100, ymax=15, frac=0.75)
        
    # ----- topicfraction plots:
    ctx = pt.PlotContext(outputdir, "", datasets.by_ab, 
                         60/25.4, tse_pagewidth_mm/25.4, 
                         datasets.ab_topicfractions_values, datasets.ab_subsets)
    pt.plot_xletgroups(ctx, pt.add_boxplotlet, "box", "topicfractions",
                       "space per topic [%]", ymax=50)
    pt.plot_xletgroups(ctx, pt.add_zerofractionbarplotlet, "zerofractionbar", "topicmissingfractions",
                       "how often missing [%]", ymax=100)
    # ----- frequency of a-* codes and iu gaps:
    ctx = pt.PlotContext(outputdir, "", datasets.by_ab, 
                         60/25.4, tse_pagewidth_mm/25.4, 
                         datasets.ab_missinginfofractions_values, datasets.ab_subsets)
    pt.plot_xletgroups(ctx, pt.add_nonzerofractionbarplotlet, "nonzerofractionbar", "missinginfofractions",
                       "how often occuring [%]", ymax=66)


def plot_ab_topicstructure_freqs_design(df: pd.DataFrame, outputdir: str):
    design_df = df.loc[df['topicstructure'].str.contains('d')]
    plot_ab_topicstructure_freqs(design_df, outputdir)


def plot_ab_topicstructure_freqs_empir(df: pd.DataFrame, outputdir: str):
    empir_df = df.loc[~df['topicstructure'].str.contains('d')]
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


if __name__ == '__main__':
    # for tryout during development
    ...
