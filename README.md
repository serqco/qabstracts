# qabstracts: Quality of scientific abstracts

created: Lutz Prechelt, 2022-07-12  
updated: Lloyd Montomery, 2024-06-19

### Summary of Artefacts

These artefacts accompany a research article submitted to the IEEE Transactions on Software Engineering (TSE) journal. This research is an empirical study on how well abstracts actually summarise the article. For further details on the article itself, read the next section on Author and Article Details. These artefacts include a complex mix of: scientific data and protocols; the LaTeX and images needed to generate the article PDF; and the scripts used both in the scientific processing and evaluation of results, as well as technical tasks such as downloading and interacting with scientific articles. See below for further details regarding the Description of Artefacts and the terms of Licences.

These artefacts can be found permanently at the following DOI: !!! Zenodo of GitHub Release Here - Use the version-agnostic DOI, not the version-specific DOI !!!

### Author and Article Details

Lutz Prechelt - prechelt@inf.fu-berlin.de  
Lloyd Montgomery - lloyd.montgomery@uni-hamburg.de  
Julian Frattini - julian.frattini@bth.se  
Franz Zieris - franz.zieris@bth.se  

L. Prechelt is with Freie Universität Berlin, Germany  
L. Montgomery is with University of Hamburg, Germany  
J. Frattini and F. Zieris are with BTH, Karlskrona, Sweden  

**Article Title**: How (Not) To Write a Software Engineering Abstract

**Article Abstract**: *Background:* Abstracts are a very valuable element in a software engineering research article, but not all abstracts are as informative as they could be. *Objective:* Characterize the structure of abstracts in high-quality venues, observe and quantify deficiencies, and suggest guidelines for writing informative abstracts. *Methods:* Use open coding to derive concepts that explain relevant properties of abstracts and identify the archetypical structure of abstracts. Use quantitative content analysis to objectively characterize abstract structure over a sample of 362!!! abstracts from five presumably high-quality venues. Use exploratory data analysis to find recurring issues in abstracts. Compare the prototypical structure to actual structures to derive guidelines for producing informative abstracts. *Results:* Only 29\%!!! of our abstracts are complete, i.e., provide background, objective, method, result, and conclusion information. For structured abstracts, the fraction is twice as big. Only 3\%!!! of our abstracts also have acceptable Flesh/Kincaide readability and have neither informativeness gaps nor understandability gaps or highly ambiguous sentences. *Conclusions:* (1)~Even in top venues, a large majority of abstracts are far from ideal. (2)~Structured abstracts tend to be better than unstructured ones, but (3)~artifact-centric works need a different structured format. (4)~The community should start requiring conclusions that generalize, which currently are often missing.

**Please cite this work as**:  
!!! Article In Review. Also Update Article Abstract with Final Version !!!

### Description of Artefacts

This artefact is can be roughly split into three main components: scientific data (and protocols), scripts, and LaTeX article. Here we describe what you can (roughly) expect from each component. The list of files and folders are ordered logically—to optimise for understanding, not alphabetically.

##### Scientific Data (and Protocols)
- `procedure.md`: Description of how the study was carried out overall.
- `codebook.md`: The detailed and thoroughly evolved rules applied in the qualitative coding.
- `abstracts`: The sample of abstracts used (or potentially used) in the study. Contains subdirectories `abstracts/abstracts.A`, `abstracts/abstracts.B` for the abstracts to be annotated by the coders.    
  - `abstracts/sample.list` contains lines of the form "EMSE-2022/FrePetGer22.pdf" (volumename, citekey).  
  - `abstracts/sample-titles.json` maps citekeys to article titles.  
  - `abstracts/sample-who-what.txt` work status file: Which citekeys belong to which block? Who is going to code or has coded which block? Use coder firstnames or nicknames for entries here.
- `history.md`: A rough history of the qabstracts project.
- `prestudy`: A preliminary look at a small sample of abstracts in order to understand the domain.
- `prestudy2`: A preliminary coding with several coders to understand coding, structure akin to `abstracts`.
- `results`: Data files derived from the annotated abstracts and files created by statistical evaluation.
- `volumes`: The subcorpora used in the study (as external directories). Each subcorpus is the result of a call to the `retrievelit` downloader.
- `write`: The articles and reports eventually written about the study.

##### Scripts
- `script`: Python and R scripts for study execution, analysis, and plotting.
- `Makefile`: Set of commands used regularly in this project.
- `requirements.txt`: Dependencies required for the Python virtual environment to run the included scripts.

##### LaTeX Article
- `tex`: LaTeX files to create the article PDF.
- `img`: Plots created by statistical evaluation and perhaps other images.
- `events`: Files associated with updates to the LaTeX article.

### Notes for the Future

TODO before running a similar study again:
- extend the "not a sentence-end" heuristic:
  "vs.", "et al.", ...
- make sure we treat data as UTF-8 always

### Licences

The code is licensed under MIT. The license is included in this repository and further information can be found here: https://opensource.org/licenses/MIT

This data in this work (c) 2024 by serqco is licensed under CC BY 4.0. The license is included in this repository and further information can be found here: https://creativecommons.org/licenses/by/4.0/
