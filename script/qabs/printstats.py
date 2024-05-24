import argparse
import sys

import pandas as pd
import scipy

import qscript.plottypes as pt


def print_all_stats(args: argparse.Namespace, datasets: argparse.Namespace, outputdir: str):
    if args.printall:
        print_abtype_table(datasets.by_abstract)
        if args.withoutdesignworks:
            comment_out_design_works(args.withoutdesignworks, datasets.by_abstract)
        print_abstracts_with_canonical_structure(datasets.ab_structures)
        print_abstracts_structures_counts(datasets.ab_structures)
        print_gaps_stats(datasets.df_primary1, datasets.by_abstract)
        print_ignorediff_stats(datasets.df_primary1, datasets.by_abstract)
    print_test(datasets.by_abstract, 'is_complete')
    print_test(datasets.by_abstract, 'is_proper')


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
    print(res/2)
    res2 = df.groupby(['venue']).count()["words"]  # pick _any_ 1 column
    print(res2/2)
    print("Total:", len(df), "codings of abstracts, ", len(df)//2, "abstracts")

def print_abstracts_with_canonical_structure(df):
    _printheader()
    canonical_structure = 'bgomrc'
    good_abstracts = df.loc[df['topicstructure'] == canonical_structure]
    print(f"abstracts with structure '{canonical_structure}':\n",
          list(good_abstracts['citekey'].unique()))


def print_abstracts_structures_counts(df):
    _printheader()
    alltypes = df.topicstructure.value_counts().index
    alltypes_structured = df.loc[df.is_struc].topicstructure.value_counts().index
    for_empir = [t for t in alltypes if "d" not in t]
    for_empir_struc = [t for t in alltypes_structured if "d" not in t]
    for_design = [t for t in alltypes if "d" in t]
    print(f"#abstracts structures empirical:\n{for_empir}")
    print(f"#abstracts structures empirical (structured only):\n{for_empir_struc}")
    print(f"#abstracts structures design:\n{for_design}")
    print(f"#abstracts structures: empirical {len(for_empir)}, "
          f"empirical structured {len(for_empir_struc)}, design {len(for_design)}")


def print_ignorediff_stats(codings: pd.DataFrame, abstracts: pd.DataFrame):
    def remove_shared_codes_from_code_pairs(abstract_ignorediff_codes: pd.DataFrame):
        # We are looking at the two codings of one sentence. Get the counts of codes (either 1 or 2):
        per_code_count = pd.crosstab(index=abstract_ignorediff_codes['code'], columns="count")
        # Those with count 2 are not disagreements. Find the others:
        single_codes = per_code_count[per_code_count['count'] == 1].index
        # Return the original dataframe but suppress the count=2 codes:
        return abstract_ignorediff_codes[abstract_ignorediff_codes.code.isin(single_codes)]

    _printheader()
    ignorediff_codings = codings[(codings.code != 'ignorediff') & (codings.ignorediff == 1)]
    print("### -ignorediff counts:")
    true_ignorediff_codings = ignorediff_codings.groupby(by=['citekey', 'sidx']) \
        .apply(remove_shared_codes_from_code_pairs)
    # print(ignorediff_codings[['coder', 'code']])
    per_code_count = pd.crosstab(index=true_ignorediff_codings['code'], columns="count",
                                 margins=True, margins_name='TOTAL')
    print(per_code_count.sort_values(by='count', ascending=False))
    per_code_percent = pd.crosstab(index=true_ignorediff_codings['code'], columns="count", 
                                   normalize='columns').round(3) * 100
    per_code_percent.columns = ['percent']
    print(per_code_percent.sort_values(by='percent', ascending=False))
    print("### #abstracts with N -ignorediff cases:")
    per_abstract_count = pd.crosstab(index=true_ignorediff_codings['citekey'], columns="count")
    per_abstract_count.columns = ['ignorediffN']
    per_count_count = pd.crosstab(index=per_abstract_count['ignorediffN'], columns="count", margins=True)
    per_count_count.columns = ['abstractsN', 'total']
    print(per_count_count)
    print("total # abstracts: ", abstracts.shape[0])
    print("---")


def print_gaps_stats(codings: pd.DataFrame, abstracts: pd.DataFrame):
    _printheader()
    for which in ('icount', 'ucount'):
        codings_with_iucount = codings[codings[which] > 0]
        per_code_percent = pd.crosstab(index=codings_with_iucount['code'], columns="count", 
                                       normalize='columns').round(3) * 100
        per_code_percent.columns = ['percent']
        per_code_percent.index.name = which
        print(per_code_percent.sort_values(by='percent', ascending=False))
    per_count_percent = pd.crosstab(index=abstracts.announcecount, columns="announcecount",
                                    normalize=True).round(3) * 100
    per_count_percent.columns = ['percent']
    per_count_percent.index.name = 'abstract_has_announce'
    print(per_count_percent.sort_values(by='percent', ascending=False))
    

def print_test(df: pd.DataFrame, criterion: str):
    df_struc = df.query('is_struc')
    df_unstruc = df.query('not is_struc')
    total = len(df)
    struc_total = len(df_struc)
    struc_success = len(df_struc.query(f'{criterion} > 0'))
    struc_failure = struc_total - struc_success
    unstruc_total = len(df_unstruc)
    unstruc_success = len(df_unstruc.query(f'{criterion} > 0'))
    unstruc_failure = unstruc_total - unstruc_success
    testdf = pd.DataFrame([[struc_success, struc_failure], [unstruc_success, unstruc_failure]],
                          columns=['yes', 'no'], index=['structured', 'unstructured'])
    chi2, p, dof, expected = scipy.stats.chi2_contingency(testdf)
    print("Test '%s': chi2:%5.1f, p:%6.4f, df:%d" % (criterion, chi2, p, dof))
    print("          yes: total %4.1f%%, structured %4.1f%%, unstructured %4.1f%%" % 
          (100 * (struc_success + unstruc_success) / total,
           100 * struc_success  / total,
           100 * unstruc_success  / total))
    print(testdf)

def _printheader():
    """Print separator header giving the function name from two stackframes up."""
    print("##########", pt.funcname(2))
