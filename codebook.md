# Codebook and coding rules for qabstracts study

created: Lutz Prechelt, 2022-07-14
changed: Lutz Prechelt, 2022-07-15


## Coding rules

1. The basic idea of our coding is simplicity (in order to
   to make high inter-rater agreement possible):
   - a simple, fixed rule for granularity and segmenting
   - a small set of straightforward codes
2. Annotation granularity is by sentence.
   Sentences are terminated by a colon or a period.
3. Each sentence receives an annotation
   (marked by {{}}) with at least one code.
4. If necessary, a sentence (in particular a long one) can
   receive two or more codes.
   This means that some substantial part(s) of the sentence pertain to one code
   and other substantial parts pertain to another code.
   An interpretation with only one code is prefered.
   No part of any sentence pertains to two codes at once.
5. For annotation, a sentence is interpreted in its 
   backward and forward context, not in isolation.
   In particular, when a sentence can be an A or a B, but only a B is expected
   in this position, it is interpreted as a B.
6. If a classification requires a guess about what is or is not in 
   the article and that guess is estimated to be less than 75% reliable,
   append a '?' to the respective code.


## Codebook: Codes for sentences

Note: Our annotation checking script gathers the set of codes to check
for from this file by looking for strings of the form
"code `something`".
(Allowing synonyms for the codes would be nice for graders in the beginning,
but appears to have a bad cost/benefit tradeoff, so we do not do this.)

Make sure all code declarations take this form and no other things do.

Codes for sentences (in alphabetical order; all codes are singular; 
semicolon means OR):
- code `announce-<xyz>`:  
  A statement announcing that the article body will contain information
  of the `<xyz>` type, 
  but this and the next statement do not contain such information.
  - code `announce-background` (hopefully never to be seen)
  - code `announce-conclusion`
  - code `announce-design`
  - code `announce-futurework`
  - code `announce-method`
  - code `announce-result`
- code `background`:  
  Information about the larger topic area of the work;  
  information leading towards the research interest of the work;  
  information about related work or the state of knowledge.  
- code `claim`:  
  A non-empirical would-be result statement.
  If position and phrasing allow it to be considered `objective`, use that.
- code `conclusion`:  
  A take-home message that is less specific than one or more results.
  Either a generalization from the results or an existence proof statement.
- code `design`:  
  information about the design, design process, and designed features of 
  an artifact, such as software, a process, or a method.
  (Designed features are known at design time, in contrast to emerging features,
  which can only be determined empirically and are classified as `result`.
  Top-level design goals and non-goals are `objective`.)
- code `futurework`:  
  information about suggested future research.
- code `h-<xyz>`:  
  A section intro term "<Xyz>:" or some synonym of that,
  that announces subsequent `<xyz>` information.
  It does not matter whether the announcement is correct.
  - code `h-background`: "Background:", "Context:", etc.
  - code `h-conclusion`
  - code `h-design`: "Approach:" etc. (probably rare)
  - code `h-futurework`
  - code `h-method`: "Method:", "Approach:" etc.
  - code `h-objective`: "Objective:", "Aim:", "Goal:", "Question:", etc.
  - code `h-result`
- code `method`:  
  information about the approach or setup of an empirical study.
- code `objective`:  
  this work's research goal;  
  this work's specific research interest;  
  this work's research question.  
- code `resourcepointer`:  
  A concrete reference to a concrete external resource such as 
  a software artifact, materials package, data package, appendix,
  or similar item.
- code `X`:  
  Unknown class. The sentence needs to be revisited and classified.
