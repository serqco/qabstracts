# Codebook and coding rules for qabstracts study

created: Lutz Prechelt, 2022-07-14
changed: Lutz Prechelt, 2022-09-12


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
for directly from this file by looking for strings of the form
"code `something`".
Make sure all code declarations take this form and no other things do.
(Allowing synonyms for the codes may be nice for graders in the beginning,
but appears to have a bad cost/benefit tradeoff, so we do not do this.)

Codes for sentences (in alphabetical order; all codes are singular; 
semicolon means OR):
- codes of the form `a-<xyz>`:  
  A statement announcing (hence the `a-`) that the article body will 
  contain information of the `<xyz>` type, 
  but this and the next statement do not contain such information.
  - code `a-background` (hopefully never to be seen)
  - code `a-claim` (hopefully never to be seen)
  - code `a-conclusion`
  - code `a-design`
  - code `a-futurework`
  - code `a-limitations`
  - code `a-method`
  - code `a-objective`
  - code `a-result`
  - code `a-resourcepointer`
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
- codes of the form `h-<xyz>` ("header"):  
  A section intro term "<Xyz>:" or some synonym of that,
  that announces subsequent `<xyz>` information.
  It does _not_ matter whether the announcement is correct.
  Singular and plural are considered equivalent.
  - code `h-background`: "Background:", "Context:", etc.
  - code `h-conclusion`: "Conclusion:" etc.
  - code `h-design`: "Approach:" etc. (probably rare)
  - code `h-futurework`: "Future work:" etc.
  - code `h-method`: "Method:", "Approach:" etc.
  - code `h-objective`: "Objective:", "Aim:", "Goal:", "Question:", etc.
  - code `h-result`: "Result:" etc.
- code `hype`:  
  The praises the work beyond what a factual statement might state.
  Plain positive properties do not qualify ("This is helpful because..."),
  only emphasized ones do ("This is tremendously helpful because...").
  This code is not a classification of a sentence, but an additional attribute.
  It can never occur alone, only in conjunction with one of the others and
  should be given last.
- code `limitation`:  
  information about limitations, threats to validity, and the like
  of the study or its results.
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
- code `result`:  
  information about the immediate outcome of a study in the form of
  empirical results. See `claim`.
- code `X`:  
  Unknown class. The sentence needs to be revisited and classified.


## Informativeness and elementary facts

At least for `method`, `design`, and `result` information, the informativeness
of an abstract will likely become better if more details are provided.
We measure this aspect by counting the number of "new elementary facts"
that are mentioned in such a statement.

A fact is not new if it was mentioned before or is obvious from 
previous material.
For example, if the `objective` said "We explore A and B",
then A and B are not new when they are mentioned in `result`,
but a subconcept B' would be new (even if it is well-known in principle).

Now what is an elementary fact?

Decision as of 2022-08-31:
Everybody tries to develop an idea of this that appears appropriate
and then attempts to formulate some coding rules that operationalize the idea.
Then we discuss those and decide what we are going to use.
The goal is a definition that promises relevance for quality
and a reasonably (if not perfectly) repeatable operationalization.


## Codebook: Codes for entire abstracts

We grade abstracts as a hole in a subjective manner.
If both graders agree, the grading becomes credible.
So our grade definitions need to make agreement likely.

We grade two **aspects**, each on a three-point scale:
- informativeness: How much information the abstract provides.
- understandability: The abstract's level of non-ambiguity.

**Goals:** What we want to assess by these is: 
- Is the space used efficiently to convey a lot of information in the abstract?
- Do I (as a reader) find it easy to understand the information?
What we do _not_ want to assess is:
- Does the information conveyed cover the most _relevant_ things to be said
  about the article?
- Is the understanding I have achieved actually correct?

**Syntax:** The codes used to express the two aspects follow after 
a "----" separator line after the annotated abstract.
To mark their global nature, they use a different syntax:
`#mycode` rather than `{{mycode}}`

**Codes for entire abstracts:**
- Code `#inf-high`:  
  The abstract appears to summarize the article well.
- Code `#inf-ok`:  
  The abstract feels somewhat informative, but 
  appears to miss several opportunities to summarize the article better.
- Code `#inf-low`:  
  The abstract feels hardly informative and 
  appears to miss most opportunities to summarize the article better.
- Code `#und-high`:  
  The abstract is readily readable for me. 
  I did not encounter relevant ambiguity in it and so 
  I am not scratching my head now.
- Code `#und-ok`:  
  I find the abstract somewhat difficult to read and follow 
  or see at least one relevant ambiguity.
- Code `#und-low`:  
  I find the abstract difficult to read and follow and/or 
  several relevant things in it are ambiguous to me.
  
A third global aspect was proposed: appeal.
How much does an abstract trigger a reader's interest in learning 
more about the work?

This is likely too dependent on the specific grader's interests spectrum
to lead to useful results: If I am interested in the topic area,
an abstract can have more appeal or less.
But if I am not interested in the topic area (and in our grading process,
this will be the usual case), even the best abstract will not have 
much appeal to me.
Decision: We do not grade appeal.
