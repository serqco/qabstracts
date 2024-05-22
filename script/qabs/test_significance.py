import pandas as pd
import numpy as np

from scipy.stats import chisquare

def read_datafile(datafile: str) -> pd.DataFrame:
    df = pd.read_csv(datafile, sep='\t', index_col=False)
    return df

# list of codes required in an abstract to be considered "complete"
codes_of_complete_abstract = ['background', 'objective', 'method', 'result', 'conclusion']
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
    return all(code in abstract_codes for code in codes_of_complete_abstract)

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

def test_significance(dep_proper: bool=False):
    """Perform a test of significant difference in the dependent variable when stratifying by the independent variable.
    
    parameters:
        dep_proper : True when using properness as the dependent variable, false when using completeness
        
    returns: list of value counts"""

    # load the data and compile (dfc) the required view
    df: pd.DataFrame = read_datafile('./results/abstracts-results.tsv')
    dfc: pd.DataFrame = compile_data(df)
    
    # count the occurrences of the dependent variable stratified by the independent variable "structured"
    dependent_variable: str = 'proper' if dep_proper else 'complete'
    return dfc[['structured', dependent_variable]].value_counts()

if __name__ == '__main__':
    # for tryout during development
    print('Testing whether abstract structuredness affects abstract completeness:')
    print(test_significance(dep_proper=False))

    print('\nTesting whether abstract structuredness affects abstract properness:')
    print(test_significance(dep_proper=True))