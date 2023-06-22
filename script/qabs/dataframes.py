import argparse

import pandas as pd

import qscript.annotations as annot
import qscript.plottypes as pt

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
    res['ignorediff'] = 0  # default
    ignorediffs = df.query('code == "ignorediff"')
    for index, row in ignorediffs.iterrows():
        res.loc[(res.citekey == row['citekey']) & (res.sidx == row['sidx']), 'ignorediff'] = 1
    res['is_announce'] = res.code.str.contains('^a-')  # per-sentence entry, must be counted
    res['is_struc'] = res.code.str.contains('^h-')  # per-sentence entry, must be aggregated
    res['is_design'] = res.code == 'design'  # per-sentence entry, must be aggregated
    return res


def df_by_ab(primary: pd.DataFrame) -> pd.DataFrame:
    # ----- do basic aggregation from codings to abstracts:
    res = primary.groupby(['citekey', 'coder']) \
        .agg(_citekey=_nagg('citekey', 'min'),
             _coder=_nagg('coder', 'min'),
             venue=_nagg('venue', 'min'),
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
    codeparts = primary.groupby(['citekey', 'coder', 'code']).agg(
            codewords=_nagg('words', 'sum'),
    )

    def add_topicfraction_x(result: pd.DataFrame, x: str) -> pd.DataFrame:
        py_x = x.replace('-', '_')  # make name usable as a python identifier
        result = pd.merge(result, topicparts.query(f"topic=='{x}'"), 'left', on=('citekey', 'coder'))
        result = result.rename(columns=dict(topicwords=f'words_{py_x}'), errors="raise")
        result[f'fraction_{py_x}'] = (100 * result[f'words_{py_x}'] / result.words).fillna(0)
        return result

    def add_codefraction_x(result: pd.DataFrame, x: str) -> pd.DataFrame:
        py_x = x.replace('-', '_')  # make name usable as a python identifier
        result = pd.merge(result, codeparts.query(f"code=='{x}'"), 'left', on=('citekey', 'coder'))
        result = result.rename(columns=dict(codewords=f'words_{py_x}'), errors="raise")
        result[f'fraction_{py_x}'] = (100 * result[f'words_{py_x}'] / result.words).fillna(0)
        return result

    res = add_topicfraction_x(res, 'background')
    res = add_topicfraction_x(res, 'gap')
    res = add_topicfraction_x(res, 'objective')
    res = add_topicfraction_x(res, 'design')
    res = add_topicfraction_x(res, 'method')
    res = add_topicfraction_x(res, 'result')
    res = add_topicfraction_x(res, 'summary')
    res = add_topicfraction_x(res, 'conclusion')
    res = add_topicfraction_x(res, 'future')
    res = add_topicfraction_x(res, 'other')
    res = add_codefraction_x(res, 'a-method')
    res = add_codefraction_x(res, 'a-result')
    res = add_codefraction_x(res, 'a-conclusion')
    res = add_codefraction_x(res, 'a-fposs')
    res['fraction_introduction'] = res.fraction_background + res.fraction_gap
    res['total_gaps'] = res.icount + res.ucount + 3 * res.announcecount  # count each 'a-*' as 3 gaps
    return res


def ser_ab_structures(df: pd.DataFrame) -> pd.DataFrame:
    strucs = df[df['topic'] != 'other'] \
        .groupby(['citekey', 'coder'])[['citekey', 'topic', 'is_struc']] \
        .aggregate(
            citekey=_nagg('citekey', 'min'),
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
    datasets.ab_missinginfofractions_values = ab_missinginfofractions_values(datasets.by_ab)


def ab_subsets(df: pd.DataFrame) -> pt.Subsets:
    """Subsets of abstracts"""
    ab_subsets_list = [
        pt.Rows(label="all", 
                x=1.0, color="red",
                rows=lambda dfr: dfr.is_struc | ~dfr.is_struc),
        pt.Rows(label="struc",
                x=2.5, color="darkgreen",
                rows=lambda dfr: dfr.is_struc),
        pt.Rows(label="unstruc",
                x=3.5, color="darkgreen",
                rows=lambda dfr: ~dfr.is_struc),
        pt.Rows(label="design",
                x=4.5, color="mediumblue",
                rows=lambda dfr: dfr.is_design),
        pt.Rows(label="empir",
                x=5.5, color="mediumblue",
                rows=lambda dfr: ~dfr.is_design),
    ]
    x = 7.0  # add per-venue subsets after a gap
    for venue in sorted(df.venue.unique()):
        ab_subsets_list.append(pt.Rows(label=venue, x=x,  
                                       color="grey" if venue == "IST" else "darkgrey",
                                       rows=lambda dfr, venue_=venue: dfr.venue == venue_))
        x += 1.0
    return pt.Subsets(ab_subsets_list)


def ab_topicfractions_values(df: pd.DataFrame) -> pt.Subsets:
    """subsets for fraction_x space-per-topic variables"""
    ab_topicfractions_list = [
        pt.Values(label="Background",
                  x=1.0,
                  values=lambda dfr: dfr.fraction_background),
        pt.Values(label="Objective",
                  x=2.0,
                  values=lambda dfr: dfr.fraction_objective),
        pt.Values(label="Design",
                  x=3.0,
                  values=lambda dfr: dfr.fraction_design),
        pt.Values(label="Methods",
                  x=4.0,
                  values=lambda dfr: dfr.fraction_method),
        pt.Values(label="Results",
                  x=5.0,
                  values=lambda dfr: dfr.fraction_result),
        pt.Values(label="Conclusion",
                  x=6.0,
                  values=lambda dfr: dfr.fraction_conclusion),
    ]
    return pt.Subsets(ab_topicfractions_list)


def ab_missinginfofractions_values(df: pd.DataFrame) -> pt.Subsets:
    """subsets for frequency of a-*, :i, :u"""
    ab_missinginfofractions_list = [
        pt.Values(label="Methods",
                  x=1.0,
                  values=lambda dfr: dfr.fraction_a_method),
        pt.Values(label="Results",
                  x=2.0,
                  values=lambda dfr: dfr.fraction_a_result),
        pt.Values(label="Conclusion",
                  x=3.0,
                  values=lambda dfr: dfr.fraction_a_conclusion),
        pt.Values(label="Poss.fut.res.",
                  x=4.0,
                  values=lambda dfr: dfr.fraction_a_fposs),
        pt.Values(label="Detail",
                  x=5.0,
                  values=lambda dfr: dfr.icount),
        pt.Values(label="Detail (>1)",
                  x=6.0,
                  values=lambda dfr: dfr.icount > 1),
        pt.Values(label="Term",
                  x=7.0,
                  values=lambda dfr: dfr.ucount),
    ]
    return pt.Subsets(ab_missinginfofractions_list)


def _nagg(colname, func) -> pd.NamedAgg:
    """Abbreviation for pd.NamedAgg."""
    return pd.NamedAgg(column=colname, aggfunc=func)


