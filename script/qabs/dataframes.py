import argparse

import numpy as np
import pandas as pd

import qscript.annotations as annot
import qscript.plottypes as pt


def create_all_datasets(df: pd.DataFrame):
    datasets = argparse.Namespace()
    datasets.df = df  # the raw datafile
    datasets.df_primary1 = df_primary1(df)
    datasets.by_abstract_coding = df_by_abstract_coding(datasets.df_primary1)
    datasets.by_abstract = df_by_abstract(datasets.by_abstract_coding)
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


def df_by_abstract_coding(primary: pd.DataFrame) -> pd.DataFrame:
    """A dataframe with records that aggregate data at the level of one abstract coding."""
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
             syllables=_nagg('syllables', 'sum'), 
             ignorediffs=_nagg('ignorediff', 'sum'), 
             codes=_nagg('code', 'count'), 
             utopics=_nagg('topic', 'nunique'),
             icount=_nagg('icount', 'sum'), 
             ucount=_nagg('ucount', 'sum'),
             announcecount=_nagg('is_announce', 'sum'),
             is_struc=_nagg('is_struc', 'any'), 
             is_design=_nagg('is_design', 'any'))

    # ----- sentence-level fkscores cannot be averaged, we take the full :
    def calc_fkscore(group):
        # ignore headers in calculation
        filtered_group = group[~group['code'].str.startswith('h-')]
        total_sentences = len(filtered_group)
        total_words = filtered_group['words'].sum()
        total_syllables = filtered_group['syllables'].sum()
        return 206.835 - 1.015*total_words/total_sentences - 84.6*total_syllables/total_words
    res['fkscore'] = primary.groupby(['citekey', 'coder']).apply(calc_fkscore)

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
        suffix = "code" if variable == 'code' else ""
        _infix = "_code" if variable == 'code' else ""  # topicfractions: fraction_x, codefractions: fraction_code_x
        wordcountname = f'words_{py_x}{suffix}'
        result = pd.merge(result, grouping.query(f"{variable}=='{x}'"), 'left', on=('citekey', 'coder'))
        result = result.rename(columns={f"{variable}words": wordcountname}, errors="raise")
        result[f'fraction{_infix}_{py_x}'] = (100 * result[wordcountname] / result.words).fillna(0)
        return result
    
    def has_code(codename: str) -> bool:
        codeid = codename.replace('-', '_')  # make name usable as a python identifier
        return res[f"fraction_code_{codeid}"] > 0  # see _infix in add_wordsfraction

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
    res = add_wordsfraction(res, codeparts, 'code', 'background')
    res = add_wordsfraction(res, codeparts, 'code', 'gap')
    res = add_wordsfraction(res, codeparts, 'code', 'objective')
    res = add_wordsfraction(res, codeparts, 'code', 'method')
    res = add_wordsfraction(res, codeparts, 'code', 'result')
    res = add_wordsfraction(res, codeparts, 'code', 'conclusion')
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
    res['is_complete'] = (has_code('background') | has_code('gap')) & \
            has_code('objective') & has_code('method') & has_code('result') & has_code('conclusion') 
    res['is_proper'] = (res['is_complete'] & # section 4.6
                        (res['fkscore'] >= 20) &  # section 4.1/3.10 
                        (res['icount'] == 0) &  # section 4.8.1
                        (res['announcecount'] == 0) &  # section 4.8.2
                        (res['ucount'] == 0) &  # section 4.9
                        (res['ignorediffs'] == 0))  # section 4.10
                        # 4.2, 4.3 are irrelevant; we have no criteria for 4.4, 4.5, 4.7
    return res


def df_by_abstract(df_by_abstract_coding: pd.DataFrame) -> pd.DataFrame:
    """A dataframe with records that aggregate data at the level of one abstract."""
    res = df_by_abstract_coding.groupby(['_citekey']) \
        .agg(_citekey=_nagg('_citekey', 'min'), # should be no differences from here ...
             venue=_nagg('venue', 'min'),
             volume=_nagg('volume', 'min'),
             sentences=_nagg('sentences', 'max'),
             words=_nagg('words', 'max'), 
             chars=_nagg('chars', 'max'), 
             syllables=_nagg('syllables', 'max'), 
             fkscore=_nagg('fkscore', 'max'), 
             avg_wordlength=_nagg('avg_wordlength', 'max'), # ... to here.
             ignorediffs=_nagg('ignorediffs', 'max'), 
             codes=_nagg('codes', 'max'), 
             utopics=_nagg('utopics', 'max'),
             # How to count :i and :u?
             #  max = one coder saw an issue
             #  min = both coders saw an issue
             #  mean = one saw none, other saw two (or more)
             icount=_nagg('icount', 'min'),
             ucount=_nagg('ucount', 'min'),
             #
             total_gaps=_nagg('total_gaps', 'max'),
             announcecount=_nagg('announcecount', 'max'),
             fraction_introduction=_nagg('fraction_introduction', 'mean'),
             fraction_background=_nagg('fraction_background', 'mean'),
             fraction_gap=_nagg('fraction_gap', 'mean'),
             fraction_objective=_nagg('fraction_objective', 'mean'),
             fraction_design=_nagg('fraction_design', 'mean'),
             fraction_method=_nagg('fraction_method', 'mean'),
             fraction_result=_nagg('fraction_result', 'mean'),
             fraction_Outlook=_nagg('fraction_Outlook', 'mean'),
             fraction_conclusion=_nagg('fraction_conclusion', 'mean'),
             fraction_other=_nagg('fraction_other', 'mean'),
             fraction_code_a_method=_nagg('fraction_code_a_method', 'mean'),
             fraction_code_a_result=_nagg('fraction_code_a_result', 'mean'),
             fraction_code_a_conclusion=_nagg('fraction_code_a_conclusion', 'mean'),
             fraction_code_a_fposs=_nagg('fraction_code_a_fposs', 'mean'),
             fraction_conclusion_shortbg=_nagg('fraction_conclusion_shortbg', 'mean'),
             fraction_conclusion_longbg=_nagg('fraction_conclusion_longbg', 'mean'),
             # How to treat binary properties?
             #  any = one satisfied coder is enough
             #  all = both coders need to be satisfied
             is_struc=_nagg('is_struc', 'any'),
             is_design=_nagg('is_design', 'any'),
             is_complete=_nagg('is_complete', 'any'),
             is_proper=_nagg('is_proper', 'any')
            )
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
    datasets.ab_subsets = ab_subsets(datasets.by_abstract)
    datasets.ab_topicfractions_values = ab_topicfractions_values(datasets.by_abstract)
    datasets.ab_topicfractions0_values = ab_topicfractions0_values(datasets.by_abstract)
    datasets.ab_missinginfofractions_values = ab_missinginfofractions_values(datasets.by_abstract)
    datasets.ab_totalqualityfractions_values = ab_totalqualityfractions_values(datasets.by_abstract)
    datasets.ab_conclusionfractions_bybg_values = ab_conclusionfractions_bybg_values(datasets.by_abstract)


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
                  values=lambda dfr: dfr.fraction_code_a_method),
        pt.Values(label="Ann. result",
                  x=4.0,
                  values=lambda dfr: dfr.fraction_code_a_result),
        pt.Values(label="Ann. concl.",
                  x=5.0,
                  values=lambda dfr: dfr.fraction_code_a_conclusion),
        pt.Values(label="Ann. poss.fut.res.",
                  x=6.0,
                  values=lambda dfr: dfr.fraction_code_a_fposs),
        pt.Values(label="Und.gap",
                  x=7.0,
                  values=lambda dfr: dfr.ucount),
    ]
    return pt.Subsets(ab_missinginfofractions_list)


def ab_totalqualityfractions_values(df: pd.DataFrame) -> pt.Subsets:
    """subsets for frequency of is_complete and is_proper"""
    ab_totalqualityfractions_list = [
        pt.Values(label="complete",
                  x=1.0,
                  values=lambda dfr: dfr.is_complete),
        pt.Values(label="proper",
                  x=2.0,
                  values=lambda dfr: dfr.is_proper),
    ]
    return pt.Subsets(ab_totalqualityfractions_list)


def _nagg(colname, func) -> pd.NamedAgg:
    """Abbreviation for pd.NamedAgg."""
    return pd.NamedAgg(column=colname, aggfunc=func)
