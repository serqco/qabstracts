# Codebook and coding rules for qabstracts study

created: Lutz Prechelt, 2022-07-14  
changed: Lutz Prechelt, 2022-10-21


## 1. Coding rules: Fundamentals

1. The basic idea of our coding is simplicity (in order to
   make high inter-rater agreement possible):
   - a simple, fixed rule for granularity and segmenting
   - a small set of straightforward codes
2. Annotation granularity is by sentence.
   Sentences are terminated by a colon or a period.
3. Each sentence receives an annotation
   (marked by `{{}}`) with at least one code.
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
6. If a classification requires a guess about what is (or is not) in 
   the article and that guess is estimated to be less than 75% reliable,
   append a `?` to the respective code. 
   Use this sparingly.


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
  this work's research goal;  
  this work's specific research interest;  
  this work's research question.  
- code `method:iu`:  
  information about the approach or setup of an empirical study.
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
  If position and phrasing allow it to be considered `objective`, use that.
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
  but this and the next statement do not contain such information.
  - code `a-background` (hopefully never to be seen)
  - code `a-claim` (hopefully never to be seen)
  - code `a-conclusion`
  - code `a-design`
  - code `a-futurework`
  - code `a-limitation`
  - code `a-method`
  - code `a-objective`
  - code `a-result`
  - code `a-resourcepointer`
- codes of the form `h-<xyz>` designate internal headings that occur in structured abstracts: 
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


### 2.4 Extra codes

- code `-hype`:  
  The sentence praises the work beyond what a factual statement might state.
  Plain positive properties do not qualify ("This is helpful because..."),
  only emphasized ones do ("This is tremendously helpful because...").
  "very" does not count as hype.
  This code is not a classification of a sentence, but an additional attribute.
  It can never occur alone, only in conjunction with one of the others and
  should be given last.
- code `-ignorediff`:
  If the script flags a coding discrepancy that, after discussion, you and your fellow coder
  agree should be left in (because the two codings represent two different reasonable interpretations),
  add this code in one (and only one) of the codings to mark the discrepancy as resolved.
- code `X`:  
  Undecided class. The sentence needs to be revisited and classified;
  consider using `fgrep {{X}}` to find these cases.
  Use `X` only rarely and only when you cannot _yet_ make up your mind.
  Such a code will likely result in a discrepancy with your fellow coder.


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
- _Exception 2:_ If a code is marked as unsure, `somecode?`,
  it is considered compatible with `somecode` as well as with a lack of it.
  This is applicable only to codes without an information particle count (see below).
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
  Examples: !!!
- Each `a-*` annotation will automatically count as 1
  without needing an extra annotation to state this.
- Each other formulation that I think could have been more concrete counts as 1.
  Examples: !!!
- Any `claim` annotation is a candidate for counting 1.


### 4.2 Understandability gaps: `u`

The of spots in the abstract I have found where I feel that the abstract 
is ambiguous ("I wonder whether this means A or B") or downright unclear ("Huh?").

Typical cases:
- Each referent of a qualifier (such as a relative clause or prepositional phrase) 
  that is ambiguous counts as 1.
  Examples: !!!
- Each important term with two or more plausible meanings counts as 1.
  Examples: !!!
- Each unsure coding (where the code is decorated with a `?`) will automatically count as 1
  without needing an extra annotation to state this.


### 4.3 What to count or not to count

Do not ask too much from an abstract.
Count only gaps that are likely to be fillable in a straightforward manner.

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
