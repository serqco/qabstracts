# qabstracts: Quality of scientific abstracts

This is a work of the Software Engineering Research Quality Coalition (SERQco)  
https://serqco.github.io/


### 1. Summary of Artefacts

These artefacts accompany a research article submitted to the IEEE Transactions on Software Engineering (TSE) journal. 
This research is an empirical study on how well abstracts actually summarise the article. 
These artefacts include 

- input data to the study
- the manual annotations to the input data
- the scripts used in the analysis of the input data and annotations
- the scripts (Python and R) used for producing the plots
- the source code of the article
- a Makefile


### 2. Author and Article Details

Lutz Prechelt <prechelt@inf.fu-berlin.de>, Freie Universität Berlin, Germany  
Lloyd Montgomery <lloyd.montgomery@uni-hamburg.de>, University of Hamburg, Germany 
Julian Frattini <julian.frattini@chalmers.se>, Chalmers University of Technology and Gothenburg University, Sweden  
Franz Zieris <franz.zieris@bth.se>, BTH, Karlskrona, Sweden  

**Article Title**: How (Not) To Write a Software Engineering Abstract

**Article Abstract**: see file tex/our_abstract.txt

**Please cite this work as**:  
Lutz Prechelt, Lloyd Montgomery, Julian Frattini, Franz Zieris:
How (Not) To Write a Software Engineering Abstract.
http://arxiv.org/abs/2506.21634, June 2025


### 3. Description of Artefacts

Snapshot: DOI: 10.5281/zenodo.15736253  
Full history: https://github.com/serqco/qabstracts


##### 3.1 Scientific Data (and Protocols)

- `procedure.md`: Description of how the study was carried out overall.
- `codebook.md`: The detailed and thoroughly evolved rules applied in the qualitative coding.
- `history.md`: A rough timeline of the qabstracts project.
- `abstracts/`: The sample of abstracts used (or potentially used) in the study. 
  Contains subdirectories `abstracts/abstracts.A`, `abstracts/abstracts.B` (with identical sets of filenames)
  for the abstracts as annotated by the two respective coders of each, plus
  subdirectory `abstracts/abstracs.raw` for the unannotated abstracts.
    - `abstracts/sample.list` contains lines of the form "EMSE-2022/FrePetGer22.pdf" (volumename, citekey),
      naming the articles in the sample and explaining where they come from.  
    - `abstracts/sample-titles.json` maps citekeys to article titles.  
    - `abstracts/sample-who-what.txt` work status file: 
      Which citekeys belong to which block? Who is has coded which block?
- `prestudy/`: A preliminary look at a small sample of abstracts in order to understand the domain.
  Is only of interest for understanding how the study was carried out, but not part of its immediate results.
  Includes notes for introducing new project members into the ideas of the study (ditto in prestudy2).
- `prestudy2/`: A preliminary coding with several coders to understand and practice coding, structure akin to `abstracts`.
  Is only of interest for understanding how the study was carried out, but not part of its immediate results.
- `results/`: Data files derived from the annotated abstracts and files created by statistical evaluation.
- `volumes/`: The subcorpora used in the study (as external directories). 
  Each subcorpus is the result of a call to the `retrievelit` downloader.
  (These files are present only in local workdirectories; they will not be checked into git.)


##### 3.2 Scripts

- `Makefile`: Set of commands used regularly in this project.
  Shows how various parts relate to each other.
- `script/`: Python scripts for study execution, analysis, and plotting.
- `requirements.txt`: Dependencies required for the Python virtual environment to run the included scripts.
  You must do the setup of your venv manually.
- `tex/*.Rnw`: Article source file, includes snippets of R script for study analysis.


##### 3.3 Article source

- `tex/`: The article is written in knitr syntax (LaTeX with embedded R code snippets).
  Therefore, the *.Rnw file is the source file and the *.tex file is only an intermediate product.
- `img/`: Plots created by statistical evaluation and manually created image files.
- `events/`: Files associated with updates to the LaTeX article (submitted versions, reviews).


### 4. Notes to ourselves for future studies

TODO before running a similar study again:
- extend the "not a sentence-end" heuristic:
  "vs.", "et al.", ...
- make sure we treat data as UTF-8 always


### 5. Licences

The code is licensed under MIT license; see file `LICENSE`. 

This data in this work (c) 2025 by SERQco, the Software Engineering Research Quality Coalition,
is licensed under CC BY 4.0; see file `LICENSE-DATA`.


### 6. TODOs upon changes

- Abstract changed? 
  Then update `tex/our_abstract.txt`.
- Data or criteria modified?
  Then check hardcoded stuff marked by `#nonknitr` in the `*.Rnw`
- Plots modified? 
  Then run `make extract-git-timestamps plotall pdf`.
- Received reviews for article submission?
  Then work through TODO markers in tex/*.Rnw as well.
- Article accepted/published? 
  - update article data in Section 2 of the present file
  - bring `recommended_abstracts_structure.md` in line with the respective part of the article
  - execute https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/#electronic-posting
