# qabstracts: Quality of abstracts study

created: Lutz Prechelt, 2023-01-24

This file was used as a kind of presentation to introduce the
study design to Dag Sjöberg and Sebastian Baltes.


## Goals

Measure several properties of abstracts objectively (and others
intersubjectively: others will usually agree my explanation is sensible)
and use them to argue how and where SE abstracts of presumably high quality 
articles have room for improvement.

Show (if that is so) how structured abstracts tend to have better quality
than unstructured ones.


## Approach

- Draw a stratified random sample of articles from TSE, TOSEM, EMSE, ICSE, IST 2022,
  100 articles from each.
- Use a codebook with precise concepts to classify each sentence in each abstract.
- Classify each sentence twice (two coders) with very high interrater agreement
  to show the classification results are objective.
- Evaluate the codings statistically in exploratory fashion.  
  Show recurring structures, frequent anomalies, etc.  
  Compare between venues.  
  Compare structured to unstructured abstracts. (Design articles go separately.)


## Codebook

- The backbone of the code set are codes for the sections of a structured abstract:
  background, objective, method, results, conclusions.
- Other codes represent:
  - variants of the above that are devoid of usable information (e.g. `a-method`)
  - less frequent statement types
  - intercoder differences not to be resolved (`-ignorediff`)
- Some codes can be annotated with a (non-objective) number of 
  - informativeness gaps
  - understandability gaps

We will look at `codebook.md` in a minute.


## Work organization

- We work in blocks of 8 abstracts:
  reserve block, annotate abstracts, commit results, mark block as done.
- A block takes about 1 hour.
- A block should be finished on the day it is reserved.
- After committing the block, you receive a report of all open coding issues.
  Resolve yours (if any) with your fellow coder soon.

Have a look at `sample-who-what.txt` and `procedure.md`.