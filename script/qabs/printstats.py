import argparse
import sys

import pandas as pd

import qscript.plottypes as pt


def print_all_stats(args: argparse.Namespace, datasets: argparse.Namespace, outputdir: str):
    print_iucount_stats(datasets.df_primary1, datasets.by_ab)
    if args.printall:
        # print_abtype_table(datasets.by_ab)
        if args.withoutdesignworks:
            comment_out_design_works(args.withoutdesignworks, datasets.by_ab)
        print_abstracts_with_canonical_structure(datasets.ab_structures)
        print_ignorediff_stats(datasets.df_primary1, datasets.by_ab)


def comment_out_design_works(samplewhowhatfile: str, df: pd.DataFrame):
    """
    Does not belong into plot.py semantically, but this is a convenient place for realizing it:
    Rewrite the qconclusion sister project's 'sample-who-what.txt' file such that all studies
    that were found to be design works in the qabstracts study are commented out
    (because we want to exclude them for now to limit complexity). 
    The procedure is idempotent and can be run multiple times.
    """

    def is_designwork(line_: str) -> bool:
        if line_.startswith("#"):
            return False  # a comment line does not designate a design work we still need to work on
        parts = line_.split()
        if len(parts) == 0:
            return False  # an empty line does not designate a design work
        citekey = parts[0]
        codings = df.loc[df['_citekey'] == citekey, 'is_design']
        if len(codings) == 0:
            return False  # works not yet coded are left as they are
        else:
            return codings.all()  # the coders agree it is a design work

    with open(samplewhowhatfile, 'rt', encoding='utf8') as f:
        orig_contents = f.read()
    new_lines = []
    for line in orig_contents.split("\n"):
        if is_designwork(line):
            new_lines.append(f"# {line.rstrip()}   (is a design work)")
        else:
            new_lines.append(line)
    new_contents = "\n".join(new_lines)
    if orig_contents != new_contents:
        with open(samplewhowhatfile, 'wt', encoding='utf8') as f:
            f.write(new_contents)
            print(f"rewrote '{samplewhowhatfile}'. Stop.")
    else:
        print(f"no new design works found in '{samplewhowhatfile}'. Stop.")
    sys.exit(0)


def print_abtype_table(df: pd.DataFrame):
    _printheader()
    res = df.groupby(['is_struc', 'is_design']).count()["venue"]  # pick _any_ 1 column
    print(res)


def print_abstracts_with_canonical_structure(df):
    _printheader()
    canonical_structure = 'bgomrc'
    good_abstracts = df.loc[df['topicstructure'] == canonical_structure]
    print(f"abstracts with structure '{canonical_structure}':\n",
          list(good_abstracts['citekey'].unique()))


def print_ignorediff_stats(codings: pd.DataFrame, abstracts: pd.DataFrame):
    _printheader()
    ignorediff_codings = codings[(codings.code != 'ignorediff') & (codings.ignorediff == 1)]
    # print("### a-* -ignorediff cases:")
    # print(ignorediff_codings.query('code.str.startswith("a-")', engine='python').loc[:, ['citekey', 'sidx', 'code']])
    print("### -ignorediff counts:")
    # TODO: find ignorediff code pairs (the single codes are misleading: could have been the other one)
    per_code_count = pd.crosstab(index=ignorediff_codings['code'], columns="count")
    print(per_code_count.sort_values(by='count', ascending=False))
    per_code_percent = pd.crosstab(index=ignorediff_codings['code'], columns="count", 
                                   normalize='columns').round(3) * 100
    per_code_percent.columns = ['percent']
    print(per_code_percent.sort_values(by='percent', ascending=False))
    print("### #abstracts with N -ignorediff cases:")
    per_abstract_count = pd.crosstab(index=ignorediff_codings['citekey'], columns="count")
    per_abstract_count.columns = ['ignorediffN']
    per_count_count = pd.crosstab(index=per_abstract_count['ignorediffN'], columns="count", margins=True)
    per_count_count.columns = ['abstractsN', 'total']
    print(per_count_count)
    print("total # abstracts: ", abstracts.shape[0])
    print("---")


def print_iucount_stats(codings: pd.DataFrame, abstracts: pd.DataFrame):
    _printheader()
    for which in ('icount', 'ucount'):
        codings_with_iucount = codings[codings[which] > 0]
        per_code_percent = pd.crosstab(index=codings_with_iucount['code'], columns="count", 
                                       normalize='columns').round(3) * 100
        per_code_percent.columns = ['percent']
        per_code_percent.index.name = which
        print(per_code_percent.sort_values(by='percent', ascending=False))

    

def _printheader():
    """Print separator header giving the function name from two stackframes up."""
    print("##########", pt.funcname(2))


