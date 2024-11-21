This document summarizes a number of quality issues regarding the data
processing and analysis. They were discovered while attempting to
replace the hard-coded values in the `.tex` file with inline-expressions
(Knitr’s `\Sexpr{}`), which required identifying the relevant parts in
the Python datasets.

# 1 Load Data and Run Python Statistics

``` r
## This is R
library(reticulate)
# Use R's reticulate to load Python modules (import qabs.dataframes as dataframes)
py$dataframes <- import_from_path("qabs.dataframes", path = ".")
```

``` python
## This is Python
import pandas as pd

# Load data
datafile = "../results/abstracts-results.tsv"
raw = pd.read_csv(datafile, sep='\t')

# Perform the statistics
datasets = dataframes.create_all_datasets(raw)
dataframes.create_all_subsets(datasets)
```

``` r
## This is R
library(dplyr)
library(tidyr)

# Make Python variables available to R, so they can be used in the following document
for (var in names(py)) {
  assign(var, py[[var]], envir = .GlobalEnv)
}

raw <- raw |> as_tibble()
```

## 1.1 Simple Statistics and A Glimpse into the Structure

``` r
n_distinct(raw$citekey) # Number of Abstracts
```

    ## [1] 362

``` r
raw |> head(1) |> t()
```

    ##           [,1]         
    ## citekey   "PanLinZam22"
    ## venue     "TOSEM"      
    ## volume    "TOSEM22"    
    ## coder     "B"          
    ## codername "Franz"      
    ## sidx      "2"          
    ## words     "10"         
    ## chars     "84"         
    ## syllables "28"         
    ## fkscore   "-19.7"      
    ## code      "background" 
    ## suffixes  NA           
    ## topic     "background" 
    ## icount    "0"          
    ## ucount    "0"

``` r
datasets$by_abstract |> head(1) |> t()
```

    ##                             1            
    ## _citekey                    "AbdBadCos22"
    ## _coder                      "A"          
    ## venue                       "TSE"        
    ## volume                      "TSE22"      
    ## codername                   "Lutz"       
    ## sentences                   "11"         
    ## words                       "300"        
    ## chars                       "1973"       
    ## ignorediffs                 "0"          
    ## fkscore                     "22.64167"   
    ## codes                       "12"         
    ## utopics                     "6"          
    ## icount                      "1"          
    ## ucount                      "2"          
    ## announcecount               "0"          
    ## is_struc                    "FALSE"      
    ## is_design                   "FALSE"      
    ## words_background            "76"         
    ## fraction_background         "25.33333"   
    ## words_gap                   "27"         
    ## fraction_gap                "9"          
    ## words_objective             "49"         
    ## fraction_objective          "16.33333"   
    ## words_design                NA           
    ## fraction_design             "0"          
    ## words_method                "44"         
    ## fraction_method             "14.66667"   
    ## words_result                "88"         
    ## fraction_result             "29.33333"   
    ## words_summary               NA           
    ## fraction_summary            "0"          
    ## words_conclusion            "16"         
    ## fraction_conclusion         "5.333333"   
    ## words_Outlook               NA           
    ## fraction_Outlook            "0"          
    ## words_other                 NA           
    ## fraction_other              "0"          
    ## words_backgroundcode        "76"         
    ## fraction_code_background    "25.33333"   
    ## words_gapcode               "27"         
    ## fraction_code_gap           "9"          
    ## words_objectivecode         "49"         
    ## fraction_code_objective     "16.33333"   
    ## words_methodcode            "44"         
    ## fraction_code_method        "14.66667"   
    ## words_resultcode            "88"         
    ## fraction_code_result        "29.33333"   
    ## words_conclusioncode        "16"         
    ## fraction_code_conclusion    "5.333333"   
    ## words_a_methodcode          NA           
    ## fraction_code_a_method      "0"          
    ## words_a_resultcode          NA           
    ## fraction_code_a_result      "0"          
    ## words_a_conclusioncode      NA           
    ## fraction_code_a_conclusion  "0"          
    ## words_a_fposscode           NA           
    ## fraction_code_a_fposs       "0"          
    ## fraction_introduction       "34.33333"   
    ## fraction_conclusion_longbg  NA           
    ## fraction_conclusion_shortbg NA           
    ## avg_wordlength              "5.376667"   
    ## total_gaps                  "3"          
    ## is_complete                 "TRUE"       
    ## is_proper                   "FALSE"

# 2 Issues that cause wrong numbers

## 2.1 Problem: Unclear calculation of `ignorediffs`

There appears to be some issue with the calculation of the `ignorediffs`
column.

**Example:** `AtaMasHem22` has 2 sentences which Lutz annotated with
`-ignorediff`. In the Python dataset, however, the numbers 4 (for Lutz)
and 2 (for Lloyd) show up.

``` r
raw |> filter(citekey == "AtaMasHem22") |>
    group_by(sidx) |>
    filter("ignorediff" %in% code) |>
    select(citekey, coder, codername, sidx, words, code) |>
    arrange(codername, sidx)
```

    ## # A tibble: 6 × 6
    ## # Groups:   sidx [2]
    ##   citekey     coder codername  sidx words code      
    ##   <chr>       <chr> <chr>     <dbl> <dbl> <chr>     
    ## 1 AtaMasHem22 B     Lloyd         5    28 background
    ## 2 AtaMasHem22 B     Lloyd         6    14 background
    ## 3 AtaMasHem22 A     Lutz          5    29 ignorediff
    ## 4 AtaMasHem22 A     Lutz          5    27 design    
    ## 5 AtaMasHem22 A     Lutz          6    15 ignorediff
    ## 6 AtaMasHem22 A     Lutz          6    13 design

``` r
datasets$by_abstract |> filter(`_citekey` == 'AtaMasHem22') |>
    select(`_citekey`, `_coder`, codername, ignorediffs)
```

    ##      _citekey _coder codername ignorediffs
    ## 1 AtaMasHem22      A      Lutz           4
    ## 2 AtaMasHem22      B     Lloyd           2

It looks the the number of codes each coder assigned to problematic
sentences is summed up. This count is way too much!

## 2.2 Problem: Different Word Counts

Several abstracts differ in their word count.

``` r
datasets$by_abstract |>
    filter(min(words) != max(words) | min(sentences) != max(sentences), .by = `_citekey`) |>
    select(`_citekey`,  `_coder`, words, sentences) |>
    pivot_wider(id_cols = `_citekey`, names_from = `_coder`, values_from = c(words, sentences))
```

    ## # A tibble: 36 × 5
    ##    `_citekey`  words_A words_B sentences_A sentences_B
    ##    <chr>         <dbl>   <dbl>       <dbl>       <dbl>
    ##  1 AtaMasHem22     378     336          11          11
    ##  2 BöhSzeMet22     197     172           7           7
    ##  3 CajLárGei22     278     263          20          20
    ##  4 CheJinZho22     350     293          15          15
    ##  5 ChoGueSil22     153     139          11          11
    ##  6 CopAlé22        250     236          17          17
    ##  7 EbrTusMah22     208     227          11          11
    ##  8 FahGruBey22     329     316          19          19
    ##  9 FouConMen22     214     239           8           8
    ## 10 HarThuLo22      266     252          14          14
    ## # ℹ 26 more rows

It appears as if the coders’ comments below the `---` are counted as
well.

## 2.3 Problem: Different `fkscore`s

A few abstracts have different `fkscore`s:

``` r
datasets$by_abstract |>
    filter(min(fkscore) < max(fkscore), .by = `_citekey`) |>
    select(`_citekey`,  `_coder`, fkscore) |>
    pivot_wider(id_cols = `_citekey`, names_from = `_coder`, values_from = fkscore, names_prefix = "fkscore_")
```

    ## # A tibble: 5 × 3
    ##   `_citekey`  fkscore_A fkscore_B
    ##   <chr>           <dbl>     <dbl>
    ## 1 CasZamNov22     22.8      21.6 
    ## 2 GonRajHas22     24.9      20.1 
    ## 3 Liu22          -11.0     -10.3 
    ## 4 WalGhaAla22      8.25      9.06
    ## 5 YanXiaLo22      32.5      31.2

I have no idea what might cause this.

## 2.4 Problem: Calculation of `fkscore` ignores multi-codings

Example: `XueZhoLuo22` has a double-coded sentence:

``` r
raw |> filter(citekey == "XueZhoLuo22", coder == "A") |> select(citekey, coder, sidx, code, fkscore)
```

    ## # A tibble: 7 × 5
    ##   citekey     coder  sidx code       fkscore
    ##   <chr>       <chr> <dbl> <chr>        <dbl>
    ## 1 XueZhoLuo22 A         1 background    18.4
    ## 2 XueZhoLuo22 A         2 background     6.2
    ## 3 XueZhoLuo22 A         3 gap           16.1
    ## 4 XueZhoLuo22 A         4 objective     12.3
    ## 5 XueZhoLuo22 A         5 objective     30.3
    ## 6 XueZhoLuo22 A         5 design        30.3
    ## 7 XueZhoLuo22 A         6 result        -1.8

In the calculation datasets, its overall `fkscore` is given as:

``` r
datasets$by_abstract |> filter(`_citekey` == "XueZhoLuo22", `_coder` == "A") |> select(`_citekey`, fkscore)
```

    ##      _citekey  fkscore
    ## 1 XueZhoLuo22 15.97143

… which is the same as the average from the raw data:

``` r
raw |> filter(citekey == "XueZhoLuo22", coder == "A") |> summarize(fkscore = mean(fkscore))
```

    ## # A tibble: 1 × 1
    ##   fkscore
    ##     <dbl>
    ## 1    16.0

But sentence 5 is counted *twice* (because of the double-coding), so it
should actually be:

``` r
raw |> filter(citekey == "XueZhoLuo22", coder == "A") |>
    slice(1, .by = sidx) |>
    summarize(fkscore = mean(fkscore))
```

    ## # A tibble: 1 × 1
    ##   fkscore
    ##     <dbl>
    ## 1    13.6

I did not check where in the code the abstract-level calculation is
done.

## 2.5 Problem: Improper Calculation of Fresch-Kincaid

Consider the first four sentences of `CheHuWei22`:

    Source code summarization is a crucial yet far from settled task for describing structured code
    snippets in natural language.
    High-quality code summaries could effectively facilitate program comprehension
    and software maintenance.
    A good code summary is supposed to have the following characteristics:
    complete
    information, correct meaning, and consistent description.

Calculating the FRES for each sentence individually (setting *total
sentences := 1*) and calculating the average gives:

![](https://wikimedia.org/api/rest_v1/media/math/render/svg/bd4916e193d2f96fa3b74ee258aaa6fe242e110e)

``` r
example <- raw |> filter(citekey == "CheHuWei22", coder == "A", sidx >= 2, sidx <= 5) |>
    select(words, syllables, fkscore) |> # Note: requires "syllables" column in raw data!
    mutate(words = words + 1) |> # Fixing the word count -- see next problem!
    mutate(fres = 206.835 - 1.015 * words / 1 - 84.6 * (syllables / words))
example
```

    ## # A tibble: 4 × 4
    ##   words syllables fkscore   fres
    ##   <dbl>     <dbl>   <dbl>  <dbl>
    ## 1    19        34    36.2  36.2 
    ## 2    11        31   -42.7 -42.7 
    ## 3    11        21    34.2  34.2 
    ## 4     7        17    -5.7  -5.73

``` r
mean(example$fres)
```

    ## [1] 5.461528

But using the formula properly and taking all sentences into account,
the overall score is:

``` r
example |>
    summarize(fres = 206.835 - 1.015 * (sum(words) / n()) - 84.6 * (sum(syllables) / sum(words)))
```

    ## # A tibble: 1 × 1
    ##    fres
    ##   <dbl>
    ## 1  13.1

The aggregation of sentence-level `fkscores` should not be done through

## 2.6 Problem: Improper Word Count

Sentence ID 8 from `LiuLiFu22` (including its annotation) looks like
this:

    Experimen-
    tal results on java methods show that our model can outperform
    the state-of-the-art results by a large margin on method name sug-
    gestion, demonstrating the effectiveness of our proposed model.
    {{a-method,result:i1,conclusion}}

The logic in `qscript/annotations.py` calculates the following values:

- words: 31
- syllables: 58
- chars: 204

The export logic in `qabs/export.py` however, creates the following
three entries:

``` r
raw |> filter(citekey == "LiuLiFu22", coder == "B", sidx == 8) |>
    select(citekey, sidx, words, chars, syllables, code, suffixes, topic)
```

    ## # A tibble: 3 × 8
    ##   citekey    sidx words chars syllables code       suffixes topic     
    ##   <chr>     <dbl> <dbl> <dbl>     <dbl> <chr>      <chr>    <chr>     
    ## 1 LiuLiFu22     8    15    97        58 a-method   <NA>     method    
    ## 2 LiuLiFu22     8    15    97        58 conclusion <NA>     conclusion
    ## 3 LiuLiFu22     8    15    97        58 result     :i1      result

We can see the following problems:

- Word count was 31, but turned into 15 (three times):
  - The overall word count is *always* reduced by one
    (<https://github.com/serqco/qabstracts/blob/main@%7B2024-11-20%7D/script/qabs/export.py#L89>)
  - The word count (30) is then split into *two*, even though there are
    *three* codes
    (<https://github.com/serqco/qabstracts/blob/main@%7B2024-11-20%7D/script/qabs/export.py#L93>)
- Char count was 204, but turned into 97 (three times):
  - The overall char count is *always* reduced by 10
    (<https://github.com/serqco/qabstracts/blob/main@%7B2024-11-20%7D/script/qabs/export.py#L90>)
  - The char count (194) is then split into *two*, instead of *three*
    (<https://github.com/serqco/qabstracts/blob/main@%7B2024-11-20%7D/script/qabs/export.py#L94>)

I don’t know why the export logic was setup this way, but it makes all
number-based analyses pretty weird.

# 3 Issues related to Double Coding of Abstracts

The following issues do not lead to *wrong* number per se, but to
questionable ones.

## 3.1 I-Gaps and U-Gaps

Each abstract has two `icount` and `ucount` values, which are often not
the same:

``` r
datasets$by_abstract |>
    filter(min(icount) != max(icount) | min(ucount) != max(ucount), .by = `_citekey`) |>
    select(`_citekey`, `_coder`, icount, ucount) |>
    pivot_wider(id_cols = `_citekey`, names_from = `_coder`, values_from = c(icount, ucount))
```

    ## # A tibble: 215 × 5
    ##    `_citekey`  icount_A icount_B ucount_A ucount_B
    ##    <chr>          <dbl>    <dbl>    <dbl>    <dbl>
    ##  1 AbdBadCos22        1        0        2        0
    ##  2 AbiRahOpe22        3        2        0        0
    ##  3 AhmAshAzg22        1        1        1        0
    ##  4 AhmFanYi22         4        2        0        1
    ##  5 AlDAhmMah22        1        3        0        0
    ##  6 AlkAlaKeb22        2        1        0        1
    ##  7 AlmGay22           4        7        0        0
    ##  8 AlmKorTah22        0        1        0        0
    ##  9 AmnPoe22           1        0        0        0
    ## 10 AndLimMar22        1        0        0        0
    ## # ℹ 205 more rows

A naive computation of ratios of abstracts with either type of gap
ignores this (this is what appears to be happening for the plots, e.g.,
Figure 10 in the paper, with the red bar around 55%):

``` r
sum(datasets$by_abstract$icount >= 1) / nrow(datasets$by_abstract) * 100
```

    ## [1] 55.1105

A better computation would to take the two rating into account,
requiring that both coders saw a gap (`i_min`), at least one saw a gap
(`i_max`), or they saw at least one gap on average (`i_mean`, e.g., 0
and 2 gaps, respectively). This leads to different percentages:

``` r
datasets$by_abstract |>
    group_by(`_citekey`) |>
    summarize(i_min = min(icount), i_mean = mean(icount), i_max = max(icount)) |>
    summarize(across(c(i_min, i_mean, i_max), ~sum(. >= 1) / n() * 100)) |>
    t()
```

    ##            [,1]
    ## i_min  43.92265
    ## i_mean 53.03867
    ## i_max  66.29834

## 3.2 Completeness and Properness

There are a number of paper for which the coders disagree whether they
are *complete* or disagree whether they are *proper*.

``` r
datasets$by_abstract |>
    filter(sum(is_complete) == 1 | sum(is_proper) == 1, .by = `_citekey`) |>
    select(`_citekey`, `_coder`, is_complete, is_proper) |>
    pivot_wider(id_cols = `_citekey`, names_from = `_coder`, values_from = c(is_complete, is_proper))
```

    ## # A tibble: 13 × 5
    ##    `_citekey`  is_complete_A is_complete_B is_proper_A is_proper_B
    ##    <chr>       <lgl>         <lgl>         <lgl>       <lgl>      
    ##  1 AbdBadCos22 TRUE          TRUE          FALSE       TRUE       
    ##  2 AmnPoe22    TRUE          TRUE          FALSE       TRUE       
    ##  3 BaiJiaCap22 TRUE          TRUE          FALSE       TRUE       
    ##  4 FahGruBey22 FALSE         TRUE          FALSE       FALSE      
    ##  5 GerMarLat22 TRUE          TRUE          TRUE        FALSE      
    ##  6 HeMenChe22  TRUE          TRUE          FALSE       TRUE       
    ##  7 HuCheWan22  TRUE          FALSE         FALSE       FALSE      
    ##  8 HuaWeiWan22 TRUE          FALSE         FALSE       FALSE      
    ##  9 OliAssGar22 TRUE          TRUE          TRUE        FALSE      
    ## 10 TanFeiAvg22 TRUE          TRUE          TRUE        FALSE      
    ## 11 ValHunFig22 TRUE          FALSE         FALSE       FALSE      
    ## 12 WuSheChe22  TRUE          TRUE          FALSE       TRUE       
    ## 13 YuKeuXia22  TRUE          TRUE          FALSE       TRUE
