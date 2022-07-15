# Codebook and coding rules for qabstracts study

created: Lutz Prechelt, 2022-07-14
changed: Lutz Prechelt, 2022-07-14


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


## Codebook

Note: Our annotation checking script gathers the set of codes to check
for from this file by looking for strings of the form
"code `something`".
A declaration of the form 
"code `something-else` = `something`" 
introduces `something-else` as a synonym for `something`.

Make sure all code declarations take this form and no other things do.

Codes (in alphabetical order; all codes are singular; semicolon means OR):
- code `aim` = `objective`
- code `announce-conclusion`:  
  A statement announcing that the article body will contain information
  of the `conclusion` type, 
  but this and the next statement do not contain such information.
- code `announce-design`:  
  Ditto for `design` information.
- code `announce-futurework`:  
  Ditto for `futurework` information.
- code `announce-method`:  
  Ditto for `method` information.
- code `announce-result`:  
  Ditto for `result` information.
- code `announce-conclusion`:  
  A statement announcing that the article body will contain information
  of the `conclusion` type, 
  where the statement itself does not contain such information.
- code `announce-design`:  
  Ditto for `design`
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
- code `context` = `background`
- code `design`:  
  information about the design, design process, and designed features of 
  an artifact, such as software, a process, or a method.
  (Designed features are known at design time, in contrast to emerging features,
  which can only be determined empirically and are classified as `result`.
  Top-level design goals and non-goals are `objective`.)
- code `futurework`:  
  information about suggested future research.
- code `h-background`:  
  A section intro term "Background:", "Context:", or the like,
  that announces subsequent `background` information.
  It does not matter whether the announcement is correct.
- code `h-conclusion`:  
  Ditto for `conclusion` information.
- code `h-futurework`:  
  Ditto for `futurework` information.
- code `h-method`:  
  Ditto for `method` information.
- code `h-objective`:  
  Ditto for `objective` information.
- code `h-result`:  
  Ditto for `result` information.
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
  
- code ``:  
  
- code `` = ``
- code `` = ``
- code `` = ``
- code `` = ``
- code `` = ``
- code `` = ``
- code `` = ``
  
