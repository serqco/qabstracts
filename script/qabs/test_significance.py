import pandas as pd
import numpy as np

from scipy.stats import chi2_contingency

# list of codes required in an abstract to be considered "complete"
CODES_OF_COMPLETE_ABSTRACT = ['background', 'objective', 'method', 'result', 'conclusion']
SIGNIFICANCE_LEVEL: float = 0.05

def read_datafile(datafile: str) -> pd.DataFrame:
    df = pd.read_csv(datafile, sep='\t', index_col=False)
    return df

def is_complete(data: pd.DataFrame, abs_id: str) -> bool:
    """Determine, whether an abstract contains at least one instance of the following codes: background, objective, method, result, and conclusion.

    parameters:
        data -- dataframe containing one row per abstract per sentence, where the code is stored in a column "code"
        abs_id -- identifier of the abstract in question
    
    returns: 
        true -- iff the abstract is complete
        false -- otherwise
    """
    # obtain all codes associated with the given abstract
    abstract_codes: list[str] = data[data['citekey'] == abs_id]['code'].values

    # determine whether all codes required for completeness are contained in the abstract
    return all(code in abstract_codes for code in CODES_OF_COMPLETE_ABSTRACT)

def is_proper(data: pd.DataFrame, abs_id: str) -> bool:
    """Determine, whether an abstract is considered proper, i.e., is complete, contains no informativeness gap, no announcement, no undefined important term, and no ambiguous formulation 

    parameters:
        data -- dataframe containing one row per abstract per sentence
        abs_id -- identifier of the abstract in question
    
    returns: 
        true -- iff the abstract is proper ((1) is_complete, (2) icount=0, (3) ucount=0, (4) no a-* codes, and (5) no -ignorediff)
        false -- otherwise
    """
    # obtain the subset of the data set representing the abstract
    abstract = data[data['citekey'] == abs_id]

    # check whether the abstract is complete (criterion (1))
    if not is_complete(abstract, abs_id):
        return False
    
    # sum the icount and ucount and check whether both are 0 (criteria (2) and (3))
    isum: int = int(np.nansum(abstract['icount'].values))
    usum: int = int(np.nansum(abstract['ucount'].values))
    if isum > 0 or usum > 0:
        return False
    
    # check whether the abstract contains any announcement codes (criterion 4)
    abstract_codes: list[str] = abstract['code'].values
    announcement_codes: list[str] = [code for code in abstract_codes if code.startswith('a-')]
    if len(announcement_codes) > 0:
        return False
    
    # check whether the abstract contains no ignorediff flag (criterion (5))
    if 'ignorediff' in abstract_codes:
        return False

    return True

def is_structured(data: pd.DataFrame, abs_id: str) -> bool:
    """Determine, whether an abstract is considered structured 

    parameters:
        data -- dataframe containing one row per abstract per sentence
        abs_id -- identifier of the abstract in question
    
    returns: 
        true -- iff the abstract contains at least one code with a h- prefix
        false -- otherwise
    """
    # obtain all codes associated with the given abstract
    abstract_codes: list[str] = data[data['citekey'] == abs_id]['code'].values

    # check for h- codes
    header_codes: list[str] = [code for code in abstract_codes if code.startswith('h-')]
    return len(header_codes) > 0

def compile_data(df: pd.DataFrame) -> pd.DataFrame:
    """Processes a data frame of abstract sentences and returns a dataframe with one row per abstract associated with a boolean judgement of their structuredness, completeness, and properness.

    parameters:
        data -- dataframe containing one row per abstract per sentence

    returns: dataframe with one row per abstract and columns for determining whether the abstract is "structured", "complete", and "proper"
    """

    # obtain a list of unique abstract IDs
    abs_ids: list = list(set(df['citekey']))
    
    # for each abstract, determine whether it is structured, complete, and proper
    data: dict[dict] = {}
    for abs_id in abs_ids:
        complete: bool = is_complete(df, abs_id)
        data[abs_id] = {
            'structured': is_structured(df, abs_id),
            'complete': complete,
            'proper': (is_proper(df, abs_id) if complete else False)
        }
    dfa: pd.DataFrame = pd.DataFrame.from_dict(data, 
                                               orient='index', 
                                               columns=['structured', 'complete', 'proper'])
    return dfa

def test_significance(dep_proper: bool=False) -> float:
    """Perform a test of statistically significant difference in the dependent variable when stratifying by the independent variable. Given that the independent variable (structuredness) and dependent variables (completeness and properness) are all binary, apply a Chi2 test of independence.
    
    parameters:
        dep_proper : True when using properness as the dependent variable, false when using completeness
        
    returns: p-value of the Chi2 test of significant difference"""

    # load the data and compile (dfc) the required view
    df: pd.DataFrame = read_datafile('./results/abstracts-results.tsv')
    dfc: pd.DataFrame = compile_data(df)
    
    # count the occurrences of the dependent variable stratified by the independent variable "structured"
    dependent_variable: str = 'proper' if dep_proper else 'complete'
    contingency_table = pd.crosstab(dfc['structured'], dfc[dependent_variable])
    _, p, _, _ = chi2_contingency(contingency_table)
    return p

if __name__ == '__main__':
    # for tryout during development
    p_complete = test_significance(dep_proper=False)
    print(f'The difference in abstract completeness is {"" if p_complete < SIGNIFICANCE_LEVEL else "not "}statistically significant (p = {p_complete:.2%}) for structured vs. unstructured abstracts.')

    p_proper = test_significance(dep_proper=True)
    print(f'The difference in abstract properness is {"" if p_proper < SIGNIFICANCE_LEVEL else "not "}statistically significant (p = {p_proper:.2%}) for structured vs. unstructured abstracts.')
    