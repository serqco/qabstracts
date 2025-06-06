# qabstracts: Quality of scientific abstracts


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

These artefacts can be found permanently at the following DOI: TODO!!! Zenodo of GitHub Release Here
(Use the version-agnostic DOI, not the version-specific DOI)


### 2. Author and Article Details

Lutz Prechelt <prechelt@inf.fu-berlin.de>, Freie Universität Berlin, Germany  
Lloyd Montgomery <lloyd.montgomery@uni-hamburg.de>, University of Hamburg, Germany 
Julian Frattini <julian.frattini@chalmers.se>, Chalmers University of Technology and Gothenburg University, Sweden  
Franz Zieris <franz.zieris@bth.se>, BTH, Karlskrona, Sweden  

**Article Title**: How (Not) To Write a Software Engineering Abstract

**Article Abstract**: see file tex/our_abstract.txt

**Please cite this work as**:  
TODO!!!


### 3. Description of Artefacts

##### 3.1 Scientific Data (and Protocols)

- `procedure.md`: Description of how the study was carried out overall.
- `codebook.md`: The detailed and thoroughly evolved rules applied in the qualitative coding.
- `abstracts/`: The sample of abstracts used (or potentially used) in the study. 
  Contains subdirectories `abstracts/abstracts.A`, `abstracts/abstracts.B` (with identical sets of filenames)
  for the abstracts as annotated by the two respective coders of each.
    - `abstracts/sample.list` contains lines of the form "EMSE-2022/FrePetGer22.pdf" (volumename, citekey).  
    - `abstracts/sample-titles.json` maps citekeys to article titles.  
    - `abstracts/sample-who-what.txt` work status file: 
      Which citekeys belong to which block? Who is has coded which block?
- `history.md`: A rough timeline of the qabstracts project.
- `prestudy/`: A preliminary look at a small sample of abstracts in order to understand the domain.
  Is only of interest for understanding how the study was carried out, but not part of its immediate results.
- `prestudy2/`: A preliminary coding with several coders to understand coding, structure akin to `abstracts`.
  Is only of interest for understanding how the study was carried out, but not part of its immediate results.
- `results/`: Data files derived from the annotated abstracts and files created by statistical evaluation.
- `volumes/`: The subcorpora used in the study (as external directories). Each subcorpus is the result of a call to the `retrievelit` downloader.


##### 3.2 Scripts

- `Makefile`: Set of commands used regularly in this project.
  Shows how various parts relate to each other.
- `script/`: Python and R scripts for study execution, analysis, and plotting.
- `requirements.txt`: Dependencies required for the Python virtual environment to run the included scripts.
  You must do the setup of your venv manually.


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
- Plots modified? 
  Then run `make extract-git-timestamps plotall pdf`.
- Article accepted/published? 
  Then update article data in Section 2 of the present file.
- Switch between journal version and arXiv version?
  Then set `\ifarxiv` accordingly in `tex/*.Rnw`.
