import argparse

import pandas as pd
from matplotlib import pyplot as plt

import qscript.annotations as annot
import qscript.plottypes as pt
import qscript

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
    subparser.add_argument('datafile',
                           help="Data as created by 'export'")
    subparser.add_argument('outputdir',
                           help="Directory where plot files will be placed")


def execute(args: qscript.Namespace):
    df = read_datafile(args.datafile)
    datasets = create_all_datasets(df)
    create_all_subsets(datasets)
    print_all_stats(datasets, args.outputdir)
    create_all_plots(args.plotall, datasets, args.outputdir)


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
    """Add pt.Subsets entries in datasets."""
    datasets.ab_subsets = ab_subsets(datasets.by_ab)
    datasets.ab_topicfractions_values = ab_topicfractions_values(datasets.by_ab)


def ab_subsets(df: pd.DataFrame) -> pt.Subsets:
    """Subsets of abstracts"""
    ab_subsets_list = [
        pt.Rows(label="all", 
                x=1.0, color="red",
                rows=lambda df: df.is_struc | ~df.is_struc),
        pt.Rows(label="struc",
                x=2.5, color="darkgreen",
                rows=lambda df: df.is_struc),
        pt.Rows(label="unstruc",
                x=3.5, color="darkgreen",
                rows=lambda df: ~df.is_struc),
        pt.Rows(label="design",
                x=4.5, color="mediumblue",
                rows=lambda df: df.is_design),
        pt.Rows(label="empir",
                x=5.5, color="mediumblue",
                rows=lambda df: ~df.is_design),
    ]
    x = 7.0  # add per-venue subsets after a gap
    for venue in sorted(df.venue.unique()):
        ab_subsets_list.append(pt.Rows(label=venue, x=x,  
                                       color="grey" if venue == "IST" else "darkgrey",
                                       rows=lambda df, venue=venue: df.venue == venue))
        x += 1.0
    return pt.Subsets(ab_subsets_list)


def ab_topicfractions_values(df: pd.DataFrame) -> pt.Subsets:
    """subsets for fraction_x space-per-topic variables"""
    ab_topicfractions_list = [
        pt.Values(label="Background",
                  x=1.0,
                  values=lambda df: df.fraction_background),
        pt.Values(label="Objective",
                  x=2.0,
                  values=lambda df: df.fraction_objective),
        pt.Values(label="Design",
                  x=3.0,
                  values=lambda df: df.fraction_design),
        pt.Values(label="Methods",
                  x=4.0,
                  values=lambda df: df.fraction_method),
        pt.Values(label="Results",
                  x=5.0,
                  values=lambda df: df.fraction_result),
        pt.Values(label="Conclusion",
                  x=6.0,
                  values=lambda df: df.fraction_conclusion),
    ]
    return pt.Subsets(ab_topicfractions_list)


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
        
    ctx = pt.PlotContext(outputdir, "", datasets.by_ab, 
                         60/25.4, tse_pagewidth_mm/25.4, 
                         datasets.ab_topicfractions_values, datasets.ab_subsets)
    pt.plot_xletgroups(ctx, pt.add_boxplotlet, "topicfractions",
                       "space per topic [%]", ymax=100)


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
    plt.savefig(pt.plotfilename(outputdir))


def _nagg(colname, func) -> pd.NamedAgg:
    """Abbreviation for pd.NamedAgg."""
    return pd.NamedAgg(column=colname, aggfunc=func)


def _printheader():
    """Print separator header giving the function name from two stackframes up."""
    print("##########", pt.funcname(2))


if __name__ == '__main__':
    # for tryout during development
    ...
