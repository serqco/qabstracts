# Chronology of design and execution of the qabstracts study

created: Lutz Prechelt, 2023-01-27

- 2022-07-12 manually obtained 20 abstracts for prestudy for understanding the domain
- 2022-07-13 started scripting infrastructure: Split abstract by sentence, insert {{}}
- 2022-07-14 started codebook.md
- 2022-07-19 started `extract-abs`
- 2022-08-31 meeting with Martin Shepperd, Lloyd Montgomery, Gunnar Bergersen; 
  consolidated codebook.md;
  we will run a 20-abstracts prestudy with four coders to perfect and learn the codebook
  and validate some intuitions about the domain
- 2022-09 improved codebook.md
- 2022-10 `select-sample`, `prepare-sample`, `check-codings`, `compare-codings`; 
  prepared `prestudy2/` and started prestudy2; improvements to the codebook
  (in particular replacing the previous "global codes" with `:iu` suffixes)
- 2022-11 prestudy2 runs; various small improvements
  (in particular clearer messages from `compare-codings`, clarifications in codebook);
  first attempts at data analysis (using R)
- 2022-11-08 second coding of last block of prestudy2 is done
- 2022-11-16 differences resolved between first and second codings
- 2022-12 started over with the data analysis code in Python
- 2023-01-10 last coding differences resolved in prestudy2 among coder pairs (A,B) and (C,D).
- 2023-01-20 run prestudy2 comparisons (A,C), (A,D); 
  found 22 minor (acceptable), 15 major (must be resolved), 1 severe (should not have happened) 
  disagreements
- 2023-01-27 created study sample, extracted abstracts:  
  - `qabstracts select-sample --size 525 --blocksize 8 --to abstracts volumes/EMSE-2022 volumes/ICSE-2022 volumes/IST-2022 volumes/TOSEM-2022 volumes/TSE-2022`
  - `qconclusions prepare-sample --volumedir volumes abstracts`
- 2023-01-31 intro meeting with Sebastian Baltes and Dag Sjøberg.
- 2023-02-08 blockwise coding started for the fullstudy.
  Several smaller optimizations and one larger change (adding `gap` and several other codes)
  to the codebook until end of April.
- 2023-03-08 Sebastian Baltes leaves the project
- 2023-03-10 intro meeting with Franz Zieris and Julian Frattini.
- 2023-03-31 article writing starts
- 2023-05-02 introduced script/qscript submodule and qconclusions team.
  At this time, an overlapping team planned to run a similar study on the contents of 
  Conclusions sections in articles. This later turned out to be infeasible; we dropped the idea.
- 2023-05-22 Martin Shepperd and Dag Sjøberg leave the project
- 2023-07-04 half of the theoretical maximum of blocks is done: 33
- 2023-07-12 agreement to drive forward the analysis and article-writing to see
  where we actually need more data.
  (Today, the study has been running for exactly one year.)
- 2023-09-29 long pause (it just happens)
- 2024-01-29 work resumes full throttle
- 2024-03-21 coding of blocks of abstracts is done, only evaluation and writing are left
- 2024-05-04 initial article draft is complete, internal reviews start 
- 2024-11-21 convert article from *.tex to *.Rnw (knitr)
  Knitr embedds evaluation code into the markup, so that the numbers are always correct and up-to-date.
- 2025-04-15 article draft declared feature-complete
- 2025-05-09 article polishing starts
