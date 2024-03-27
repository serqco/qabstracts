import argparse

import numpy as np
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
    """A dataframe with records that aggregate data at the level of one abstract."""
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
             fkscore=_nagg('fkscore', 'mean'), 
             codes=_nagg('code', 'count'), 
             utopics=_nagg('topic', 'nunique'),
             icount=_nagg('icount', 'sum'), 
             ucount=_nagg('ucount', 'sum'),
             announcecount=_nagg('is_announce', 'sum'),
             is_struc=_nagg('is_struc', 'any'), 
             is_design=_nagg('is_design', 'any'))
    # ----- add derived variables:
    topicparts = primary.groupby(['citekey', 'coder', 'topic']).agg(  # num of words pertaining to topic
            topicwords=_nagg('words', 'sum'),
    )
    codeparts = primary.groupby(['citekey', 'coder', 'code']).agg(  # num of words pertaining to code
            codewords=_nagg('words', 'sum'),
    )

    def add_wordsfraction(result: pd.DataFrame, grouping, variable: str, x: str) -> pd.DataFrame:
        """Which percentage of the abstract's total number of words pertains to the <variable>-part with value x?"""
        py_x = x.replace('-', '_')  # make name usable as a python identifier
        result = pd.merge(result, grouping.query(f"{variable}=='{x}'"), 'left', on=('citekey', 'coder'))
        result = result.rename(columns={f"{variable}words": f'words_{py_x}'}, errors="raise")
        result[f'fraction_{py_x}'] = (100 * result[f'words_{py_x}'] / result.words).fillna(0)
        return result

    res = add_wordsfraction(res, topicparts, 'topic', 'background')
    res = add_wordsfraction(res, topicparts, 'topic', 'gap')
    res = add_wordsfraction(res, topicparts, 'topic', 'objective')
    res = add_wordsfraction(res, topicparts, 'topic', 'design')
    res = add_wordsfraction(res, topicparts, 'topic', 'method')
    res = add_wordsfraction(res, topicparts, 'topic', 'result')
    res = add_wordsfraction(res, topicparts, 'topic', 'summary')
    res = add_wordsfraction(res, topicparts, 'topic', 'conclusion')
    res = add_wordsfraction(res, topicparts, 'topic', 'Outlook')
    res = add_wordsfraction(res, topicparts, 'topic', 'other')
    res = add_wordsfraction(res, codeparts, 'code', 'a-method')
    res = add_wordsfraction(res, codeparts, 'code', 'a-result')
    res = add_wordsfraction(res, codeparts, 'code', 'a-conclusion')
    res = add_wordsfraction(res, codeparts, 'code', 'a-fposs')
    res['fraction_introduction'] = res.fraction_background + res.fraction_gap
    q25, q75 = res.fraction_background.quantile([0.25, 0.75])
    res['fraction_conclusion_longbg'] = np.where(res.fraction_background >= q75, 
                                                 res.fraction_conclusion / (1-res.fraction_background/100),
                                                 np.NaN)
    res['fraction_conclusion_shortbg'] = np.where(res.fraction_background <= q25, 
                                                  res.fraction_conclusion / (1-res.fraction_background/100),
                                                  np.NaN)
    res['avg_wordlength'] = (res.chars - 1.2*res.words) / res.words  # deduct spaces and punctuation
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
    datasets.ab_topicfractions0_values = ab_topicfractions0_values(datasets.by_ab)
    datasets.ab_missinginfofractions_values = ab_missinginfofractions_values(datasets.by_ab)
    datasets.ab_conclusionfractions_bybg_values = ab_conclusionfractions_bybg_values(datasets.by_ab)


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
        pt.Values(label="Outlook",
                  x=7.0,
                  values=lambda dfr: dfr.fraction_Outlook),
    ]
    return pt.Subsets(ab_topicfractions_list)


def ab_topicfractions0_values(df: pd.DataFrame) -> pt.Subsets:
    """subsets for fraction_x space-per-topic variables when we are interested in zero-fractions"""
    ab_topicfractions_list = [
        pt.Values(label="Background",
                  x=1.0,
                  values=lambda dfr: dfr.fraction_background),
        pt.Values(label="Gap",
                  x=2.0,
                  values=lambda dfr: dfr.fraction_gap),
        pt.Values(label="Objective",
                  x=3.0,
                  values=lambda dfr: dfr.fraction_objective),
        pt.Values(label="Methods",
                  x=4.0,
                  values=lambda dfr: dfr.fraction_method),
        pt.Values(label="Results",
                  x=5.0,
                  values=lambda dfr: dfr.fraction_result),
        pt.Values(label="Conclusion",
                  x=6.0,
                  values=lambda dfr: dfr.fraction_conclusion),
        pt.Values(label="Outlook",
                  x=7.0,
                  values=lambda dfr: dfr.fraction_Outlook),
    ]
    return pt.Subsets(ab_topicfractions_list)


def ab_conclusionfractions_bybg_values(df: pd.DataFrame) -> pt.Subsets:
    """subsets for fraction_conclusion space-per-topic for abstracts with short vs. long background sections"""
    ab_conclusionfractions_list = [
        pt.Values(label="Conclusion\n(after short Background)",
                  x=1.0,
                  values=lambda dfr: dfr.fraction_conclusion_shortbg),
        pt.Values(label="Conclusion\n(after long Background)",
                  x=2.0,
                  values=lambda dfr: dfr.fraction_conclusion_longbg),
    ]    
    return pt.Subsets(ab_conclusionfractions_list)


def ab_missinginfofractions_values(df: pd.DataFrame) -> pt.Subsets:
    """subsets for frequency of :i, a-*, :u"""
    ab_missinginfofractions_list = [
        pt.Values(label="Inf.gap",
                  x=1.0,
                  values=lambda dfr: dfr.icount),
        pt.Values(label="Inf.gap (≥3)",
                  x=2.0,
                  values=lambda dfr: dfr.icount >= 3),
        pt.Values(label="Ann. method",
                  x=3.0,
                  values=lambda dfr: dfr.fraction_a_method),
        pt.Values(label="Ann. result",
                  x=4.0,
                  values=lambda dfr: dfr.fraction_a_result),
        pt.Values(label="Ann. concl.",
                  x=5.0,
                  values=lambda dfr: dfr.fraction_a_conclusion),
        pt.Values(label="Ann. poss.fut.res.",
                  x=6.0,
                  values=lambda dfr: dfr.fraction_a_fposs),
        pt.Values(label="Und.gap",
                  x=7.0,
                  values=lambda dfr: dfr.ucount),
    ]
    return pt.Subsets(ab_missinginfofractions_list)


def _nagg(colname, func) -> pd.NamedAgg:
    """Abbreviation for pd.NamedAgg."""
    return pd.NamedAgg(column=colname, aggfunc=func)
