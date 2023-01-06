# qabstracts: Quality of scientific abstracts

created: Lutz Prechelt, 2022-07-12  
updated: Gunnar Bergersen, 2023-01-06

Empirical study on how well abstracts actually summarize the article

See `procedure.md` for how the study is carried out overall and specifically
`codebook.md` for the rules applied in the qualitative coding.

Directories (in sort of a chrono-logical order):

- `volumes`:
  The corpora used in the study (as external directories).
- `prestudy`:
  preliminary look at a small sample of abstracts in order
  to understand the domain.
- `prestudy2`:
  preliminary coding with several coders to understand coding, structure akin to `abstracts`.
- `scripts`:
  Python and R scripts for study execution, analysis, and plotting.
- `abstracts`:
  The sample of abstracts used (or potentially used) in the study.  
  Contains subdirectories `abstracts/abstracts.A`, `abstracts/abstracts.B` for the abstracts to be annotated by the coders.  
  `abstracts/sample*` (3 files) describes the sample and indicates the origin of the abstracts.
- `results`: 
  Data files derived from the annotated abstracts and files created by statistical evaluation.
- `img`:
  Plots created by statistical evaluation and perhaps other images.
- `write`:
  The articles and reports eventually written about the study.
  
Setup issues for Mac users (Monterey 12.6.1) 2023-01-06, Gunnar
- use `python3` instead of `python` when running scripts, see `procedure.md`.
- if scripts fail with python issues, run `pip3 install -r requirements.txt` (use 'homebrew' if pip isn't already installed')
