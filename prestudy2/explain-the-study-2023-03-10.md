# qabstracts: Quality of abstracts study

created: Lutz Prechelt, 2023-03-10

This file was used as a kind of presentation to introduce the
study design to Franz Zieris and Julian Frattini.


## Goals

- Demonstrate quality issues in SE abstracts.
- Show how to write good abstracts

Conjecture:  
Structured abstracts tend to have better quality.


## Approach

- Draw a stratified random sample of articles from TSE, TOSEM, EMSE, ICSE, IST 2022,
  100 articles from each.
- Use a codebook with precise concepts to classify each sentence in each abstract.
  Some concepts are subjective, but most are objective.
- Classify each sentence twice (two coders) with high interrater agreement
  to show that the objective concepts are objective.
- Explain the typical structure of an abstract and how and why it works.
- Evaluate the codings statistically in exploratory fashion.  
  Show frequent anomalies, correlations with subjective concepts, etc.  
  Compare between venues.  
  Compare structured to unstructured abstracts. (Design articles go separately.)


## Codebook

- Principles: code by sentence; single code prefered; be friendly.
- Archetype: Introduction, Study Description, Outlook with
  several concepts within each and turning points between them. 
- Further codes and annotations represent:
  - subjective judgments, including gaps in informativeness or understandability
  - intercoder differences not to be resolved (`-ignorediff`)

We will look at `codebook.md` in a minute.


## Work organization

- We work in blocks of 8 abstracts:
  reserve block, annotate abstracts, commit results, mark block as done.
- A block takes about 1 hour.
- A block should be finished on the day it is reserved.
- After committing the block, you receive a report of all open coding issues.
  Resolve yours (if any) with your fellow coder soon.

Have a look at `sample-who-what.txt` and `procedure.md`.
