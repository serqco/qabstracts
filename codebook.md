# Codebook and coding rules for qabstracts study

created: Lutz Prechelt, 2022-07-14  
changed: Lutz Prechelt, 2022-12-29


## 1. Coding rules: Fundamentals

1. The basic idea of our coding is simplicity (in order to
   make high inter-rater agreement possible):
   - a simple, fixed rule for granularity and segmenting
   - a small set of straightforward codes
2. Annotation granularity is by sentence.
   Sentences are terminated by a colon or a period.
3. Each sentence receives an annotation
   (marked by `{{}}`) with at least one code.  
   If a sentence has been inappropriately broken into several
   (typically because of an abbreviation such as "approx. "),
   apply the same codes to each part and consider them one.
4. If necessary, a sentence (in particular a long one) can
   receive two or more codes.
   This means that some substantial part(s) of the sentence pertain to one code
   and other substantial parts pertain to another code.
   An interpretation with only one code is prefered.
   No part of any sentence pertains to two codes at once
   (except the "extra codes", see below)
5. For annotation, a sentence is interpreted in its 
   backward and forward context, not in isolation.  
   In particular, when a sentence can be an A or a B, but only a B is expected
   in this position, it is interpreted as a B.
6. We are gentle in detecting negative aspects:
   We annotate them only where they are _clearly_ present.

Only by applying rules 4, 5, 6 carefully will we be able to come out
with a good intercoder agreement.


## 2. Codebook: Codes for sentences

Subsequent subsections define codes for sentences. 
All codes are singular; semicolon means OR.
The codes described here are meant to be (nearly) objective;
we strive for high inter-coder agreement.

If a code ends with `:iu`, this means it can have an "IU suffix".
The meaning of IU suffixes is explained in Section 4.
Actual `:iu` suffixes look for instance like this:
`:i1`, `:u2`, `:i2u1` or nothing (i.e., the suffix can also be missing). 
An IU suffix codifies subjective property counts of two properties
`i` and `u`, each with a default value of 0.

Our annotation checking script gathers the set of codes to check
for directly from this file by looking for strings of the form
"code `something-or-other`".
Make sure all code declarations take this form and no other things do.


### 2.1 The basics: background, objective, method (or design), results, conclusion

The above list sketches the default structure of a structured abstract.

- code `background`:  
  Information about the larger topic area of the work;  
  information leading towards the research interest of the work;  
  information about related work or the state of knowledge.  
- code `objective:iu`:  
  one or more of this work's 
  top-level research goals,
  specific top-level research interests, or
  top-level research questions.  
- code `method:iu`:  
  information about the approach or setup of an empirical (or possibly purely mathematical) study.
- code `design:iu`:  
  information about the design, design process, and designed features of 
  an artifact, such as software, a process, or a method.
  This occurs instead of (or in addition to) `method` when the article
  is artifact-centric instead of purely empirical.
  (Designed features are known at design time, in contrast to emerging features,
  which can only be determined empirically and are classified as `result`.
  Top-level design _goals_ (and non-goals) are classified as `objective`.)
- code `result:iu`:  
  information about the immediate outcome of a study in the form of
  empirical results. See `claim:iu`.
- code `conclusion`:  
  A take-home message that is less specific than one or more results.
  Either a generalization from the results or an existence proof statement.


### 2.2 Less common codes

- code `claim:iu`:  
  A non-empirical would-be result statement.
  If position and phrasing allow it to be considered `objective` or `conclusion`, use these.
- code `futurework`:  
  information about suggested future research.
- code `limitation`:  
  information about limitations, threats to validity, and the like
  of the study or its results.
- code `resourcepointer`:  
  A concrete reference to a concrete external resource such as 
  a software artifact, materials package, data package, appendix,
  or similar item.


### 2.3 Headings and announcements

- codes of the form `a-<xyz>` designate announcements:  
  A statement announcing (hence the `a-`) that the article body will 
  contain information of the `<xyz>` type, 
  but this and the next sentence do not contain such information.
  - code `a-background` (hopefully never to be seen)
  - code `a-claim` (hopefully never to be seen)
  - code `a-conclusion`
  - code `a-design` (e.g. "We present our system XYZ.")
  - code `a-futurework`
  - code `a-limitation`
  - code `a-method` (e.g. "We describe the approach used for our survey.")
  - code `a-objective`
  - code `a-result` (e.g. "We report on our empirical results in detail.")
  - code `a-resourcepointer`
- codes of the form `h-<xyz>` designate internal headings that occur in structured abstracts: 
  A section intro term "<Xyz>:" or some synonym of that,
  that announces subsequent `<xyz>` information.
  It does _not_ matter whether the announcement is correct.
  Singular and plural are considered equivalent.
  If the heading is not terminated with a colon or period, the sentence will have multiple
  codings, but the heading must be first in the sentence.
  - code `h-background`: "Background:", "Context:", etc.
  - code `h-conclusion`: "Conclusion:" etc.
  - code `h-design`: "Approach:" etc. (probably rare)
  - code `h-futurework`: "Future work:" etc.
  - code `h-method`: "Method:", "Approach:" etc.
  - code `h-objective`: "Objective:", "Aim:", "Goal:", "Question:", etc.
  - code `h-result`: "Result:" etc.


### 2.4 Codes for special circumstances

- code `cruft`:  
  This sentence is not part of the abstract.
  It is garbage that should have been removed during the preparation of the abstract files.
- code `X`:  
  Undecided class. The sentence needs to be revisited and classified;
  consider using `fgrep {{X}}` to find these cases.
  Use `X` only rarely and only when you cannot _yet_ make up your mind.
  Such a code will likely result in a discrepancy with your fellow coder.


### 2.5 Extra codes

These codes can never occur alone, only in conjunction with one of the others.
They start with a dash to signal this and should be given last. 

- code `-hype`:  
  The sentence praises the work beyond what a factual statement might state.
  Plain positive properties do not qualify ("This is helpful because..."),
  only emphasized ones do ("This is tremendously helpful because...").
  "very" does not count as hype.
  This code is not a classification of a sentence, but an additional attribute.
- code `-ignorediff`:
  If the script flags a coding discrepancy that, after discussion, you and your fellow coder
  agree should be left in (because the two codings represent two different reasonable interpretations),
  add this code in one (and only one) of the codings to mark the discrepancy as resolved.
- code `-problemstmt`:
  The sentence formulates a statement of a problem to be solved that is more general
  than the study's `objective`. Typically only found in `background` statements.  
  (This code is for collecting data for a possible future research interest.
  We only want to find some examples, so not everybody needs to apply this code all the time.
  Feel free to overlook as many instances as needed to avoid slowing you down.)


## 3. Coding rules: Avoiding inter-coder discrepancies

- The layout of an abstracts file is rigid.
  Make changes only between the existing `{{}}` pairs and nowhere else:
  No additions or modifications, including linebreaks.
- _Exception:_ When there is no blank after a sentence end, our script will
  overlook that sentence end. If you detect this, insert a `{{}}` on a
  line of its own in between the sentences and use it for coding normally.
- Some lines are long. 
  Using a wide window or the word-wrapped-view mode of your text editor
  may be helpful. Beware of actual word wrapping, though!
- If you find an additional `{{}}` at a spot where there is no sentence end,
  just leave it empty. Do not remove it.
- These rules are used for making it easier to align corresponding abstracts files
  of multiple coders.
  For alignment, the contents of the `{{}}` pairs are compared simply in order
  of the `{{}}` pairs' occurrence and expected to be equivalent.
- _Exception:_ Codes starting with a dash ("minor codes"), such as `-hype`, 
  may be present in one coding without being present in the other.
- A GitHub action will check for discrepancies after every push and notify
  the committer if any problem is found.
  Please correct such problems promptly, because the next person doing a push
  will get them as well and be confused.
  If you receive a notification of a problem you have not created yourself
  but the correction is obvious, correct it.


## 4. Coding rules: The `:iu` suffixes for subjective codings

We grade two **aspects**, each on a cardinality scale (count scale, absolute scale):
- informativeness gaps `i`: At how many spots the abstract noticably fails to provide information 
  it could presumably provide in the eyes of the given reader.
- understandability gaps `u`: At how many spots the abstract is unclear or ambiguous
  to the given reader.

**Goals:** What we want to assess by these is: 
- Is the space used efficiently to convey a lot of information in the abstract?
- Can I (as a reader) digest the information well?
What we do _not_ want to assess is:
- Does the information conveyed cover the most _relevant_ things to be said
  about the article?
- Is the understanding I have achieved actually correct?

**Syntax:** `ì`and `u` are provided in the IU suffix of certain codes, see Section 2.
There are four cases, explained by example:
- `:i4u3`: the sentence has 4 informativess gaps and 3 understandability gaps;
- `:i2`: 2 informativess gaps and 0 understandability gaps;
- `:u1`: 0 informativess gaps and 1 understandability gap;
- `` (no suffix at all): 0 informativess gaps and 0 understandability gaps.

If the sentence has only 1 code annotated to it, the counts pertain to the entire sentence.
If there are two or more codes annotated to it, the counts pertain only to the respective part.


### 4.1 Informativeness gaps: `i`

The number of spots in the abstract I have found where I feel that the abstract 
fails to provide information it presumably could have provided without requiring much
additional space and, in my opinion, should have provided.

Typical cases:
- Each indefinite or qualitative statement that should have been a quantitative one (giving a number) counts as 1.
  Examples: 
  _"...we first collect and track a large number of fixed and unfixed violations..."_ 
  should say how many violations (`:i1`, asking for two numbers would be exaggerated; see 4.3);
  _"We learned that the ratio of scattered features remained nearly constant
  and that most features were introduced without scattering."_ should state what the ratio is
  and what fraction is "most" (`:i2`).  
  Generally, many uses of vague qualifiers such as "many", "large", "most" etc. call for a number
  (if that number is presumably known) and should provoke an `i` suffix.   
  Even unqualified nouns should get a number if they talk about a discrete number of types.
  Example: "Our tool suggests modifications" should be 
  "Our tool suggests 11 different types of modifications". 
- Each other formulation that I think could and should have been more concrete counts as 1.
  Examples:
  _"We conducted a qualitative analysis of 99 artifacts from..."_ 
  should mention what the qualitative analysis aims at (`:i1`);
  _"...using an industrial software composition analysis tool"_:
  Which tool? Or is it internal only? (`:i1`);
  _"Our results suggest that the factors that most strongly correlate with self-rated productivity were 
  non-technical factors, such as..."_: 
  Out of how many factors overall? (`:i1`) 
- Any `claim` annotation is a candidate for counting 1 or more; see 4.3 for hints.
- Each `a-*` annotation will automatically count as 1
  without needing an extra annotation to state this.


### 4.2 Understandability gaps: `u`

The of spots in the abstract I have found where I feel that the abstract 
is ambiguous ("I wonder whether this means A or B") or downright unclear ("Huh?").

Typical cases:
- Each referent of a qualifier (such as a relative clause or prepositional phrase) 
  that is ambiguous counts as 1.
- Each important term with two or more plausible meanings counts as 1.
  Example:
  _"...this research developed [a solution to monitor developers'] code review effectiveness."_:
  This is the second mention of effectiveness, but still no definition, although the background
  suggests we are more concerned with efficiency here (`:u1`).
- Each important term for which not even an approximate meaning comes to mind counts as 1.
  Example: 
  _"...that utilizes convolutional neural networks to learn features and clustering 
  to regroup similar instances."_: 
  No groups were mentioned or are obvious so far, so "regrouping" is a mysterious notion. 


### 4.3 What to count or not to count

Information or understanding that are provided by a subsequent sentence in the abstract
do not count as gaps.

Do not ask too much from an abstract.
Count only gaps that are likely to be fillable in a straightforward manner.

Example 1: Consider these two sentences:
> The results show that the top-10 most frequent change types account for 51% of the build changes.
> Among them, changes to version numbers and changes to dependencies of the projects occur 
> most frequently.

the second of these should be annotated `:i2`, because we could have learned how common
these two types are, specifically. For instance like this (the numbers are fictive):
> The results show that the top-10 most frequent change types account for 51% of the build changes, 
> the top types being changes to version numbers (13%) and 
> changes to dependencies of the projects (11%).

Generally, if you get annoyed because you want to know more, that suggests an informativeness gap.
If little space will be needed by the additional information (or none at all, like above),
add an `i` suffix.

Example 2: In the abstract containing this sentence
> We try to (i) correlate each metric with understandability and 
> (ii) build models combining metrics to assess understandability.

the key term "understandability" has so far been taken for granted, but for a statement
like this, we need to know how it was operationalized, resulting in a big fat `:u1`.

Generally, if you furrow your brows while reading, that is a good sign there is an
understandability gap somewhere.

If you have deep knowledge in the article's subject matter,
grade as if you were only normally knowledgable
in order to make agreement with your fellow coder more likely.


### 4.4 Rationale: Which codes have `:iu` suffixes?

We use `:iu` suffixes only for a few codes for the following reasons:
- `objective`, `method` (or `design`) and `result` form the backbone of an abstract,
  so we must judge those parts.  
  On the other hand:
- Subjectivity would get out of hand for some codes, e.g. `background` and all `a-*` codes, 
  because that information is naturally less concrete.
- The importance of gaps is low for `background`, yet
  abstracts provide lots of `background`, so we can save a lot of work there.
- It appears inappropriate to require more information from a `conclusion` or `limitation`,
  which many authors do not provide at all.
- The notion is not applicable to `h-*` codes.


### 4.5 Historical notes

- Until 2022-10-21, we used a three-level ordinal scale (low, ok, high) for
  informativeness and understandability, but this had two disadvantages:
  - it provides only little information
  - it was difficult to define where the boundaries should be
- A third subjective (and global) aspect was initially proposed: _appeal_.
  How much does an abstract trigger a reader's interest in learning 
  more about the work?  
  This is likely too dependent on the specific grader's interests spectrum
  to lead to useful results: If I am interested in the topic area,
  an abstract can have more appeal or less.
  But if I am not much interested in the topic area (and in our grading process,
  this will be the usual case), even the best abstract will not have 
  much appeal to me.    
  Decision: We do not grade appeal.


## 5 Adding remarks on an abstract

At the end of an abstract there is a separator line consisting of three dashes.
Below that, you can add whatever remark you feel
should be recorded for this abstract -- most often none.
Write whatever text you like, just do not use '#' at the beginning of a line.
