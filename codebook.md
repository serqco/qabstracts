# Codebook and coding rules for qabstracts study

created: Lutz Prechelt, 2022-07-14  
changed: Lutz Prechelt, 2023-05-05


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
   because of an abbreviation such as "approx. ", "et al. ", "etc. ", "vs. " etc.,
   remove the superfluous `{{}}` line.
4. If necessary, a sentence (in particular a long one) can
   receive two or more codes.
   This means that some substantial part(s) of the sentence pertain to one code
   and other substantial parts pertain to another code.
   An interpretation with only one code is prefered.
   Use multiple codes if otherwise a key element of an abstract (objective, method,
   result, conclusion) would appear to be missing entirely from the abstract.
   No part of any sentence pertains to two codes at once
   (except the "extra codes", see below)
5. For annotation, a sentence is interpreted in its 
   backward and 1-sentence forward context, not in isolation.  
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

A code may allow for one or more suffixes, which provide additional
detail and are considered subjective.
The meaning of the suffixes is explained in Section 3.

Our annotation checking script gathers the set of codes to check
for directly from the present file by looking for strings of the form
"code `something-or-other:suffix1:othersuffix`".
Make sure all code declarations take this form and no other things do.


### 2.1 The abstracts archetype

Empirically, nearly all abstracts share a common overall structure which we call the
"archetype" of abstracts.
Deviations occur sometimes, but usually mean the abstract is ill-formed.
The archetype describes an abstract as a sequence of stretches.
A stretch is a sequence of one (occasionally only a part of one) or more sentences.
The archetype describes what the sequence looks like and what the role (stretch type)
of each stretch is.
This section describes the archetype and mentions the most typical code(s) used for
each role (core codes). 
All codes, including the less frequent ones, will be defined in detail in 
subsequent sections.

The archetype:

1. An abstract typically consists of three parts, in this order:
   _Introduction_, _Study Description_, and _Outlook_. 
   The _Outlook_ is sometimes missing.
2. Two turning points connect the three parts:
   - A statement of the study goals (`objective`) connects _Introduction_ to _Study Description_.
   - A generalizing statement ("take-home message", `conclusion`) 
     connects _Study Description_ to _Outlook_, but may be missing.
3. The _Introduction_ first introduces the topic area of the study and what is known (`background`)
   and then may or may not point out a gap in knowledge (`gap`) or 
   postulate a need for a certain research (`need`).
4. For an empirical article, the _Study Description_ begins with
   method description (`method`), followed by results description (`result`).
   Sometimes, this sequence occurs twice in a row, very rarely more.
5. For a design article, design description (`design`, see below) may precede the structure
   described in the previous point or may be interleaved with it.
6. Occasionally (but infrequently), _Study Description_ will end with a study summary (`summary`).
7. _Outlook_ talks about future research and states 
   what could now be done (`fposs`, for future possibilities),
   what should now be done (`fneed`),
   what the authors themselves intend to do (`fwork`), or
   what is still not known (`fgap`).
   Several of these may occur, in no particular order.

**The archetype guides the coding**: During coding, we will expect the next sentence
to be either part of the same stretch or the beginning of one
that the archetype describes as a possible successor.  
Only if the next sentence clearly defies any such interpretation will we consider
a different code for it.


### 2.2 Core codes for the turning points

The turning points are the most informative sentences (typically only one each)
in an abstract: 
The first describes what the study is about, 
the second describes what it found.

From _Introduction_ to _Study Description_:
- code `objective:hype:u\d`:  
  one or more of this work's 
  top-level research goals,
  specific top-level research interests, or
  top-level research questions.  
  Objectives sentences often contain material that is ambiguous as goal-or-method
  or as goal-or-design. In those cases, assign two codes only if there is no 
  method (or design) information elsewhere in the abstract (according to general rule 4).
  If the method (or design) information is too specific and concrete to be a goal,
  assign two codes in any case.

From _Study Description_ to _Outlook_:
- code `conclusion:hype:incredible:timid:u\d`:  
  A take-home message that is less specific than one or more results.
  Usually a generalization from the results, sometimes a non-obvious existence proof statement.


### 2.3 Core codes for _Introduction_

The above list sketches the default structure of a structured abstract.

- code `background`:  
  Information about the larger topic area of the work, the state-of-the-art,
  related work, what is known.
- code `gap:hype`:  
  A statement of what is not yet known or 
  what is so far difficult to achieve in research or in practice
  which directly leads over to the topic of the present work (the `objective`).
- code `need:hype`:  
  A postulate about what research needs to be performed
  which directly leads over to the topic of the present work (the `objective`).


### 2.4 Core codes for _Study Description_

- code `method:hype:i\d:u\d`:  
  information about the approach or setup of an empirical (or possibly purely mathematical) study.
- code `design:hype:i\d:u\d`:  
  To be used only if the article is artifact-centric instead of purely empirical, i.e., 
  if the article's main contribution is an artifact or the knowledge how to build it,
  not the empirical results obtained with its help.
  A `design` statement provides information about the design, design process, and designed features of 
  an artifact, such as software, a process, or a method.  
  We call articles where the abstract contains a design statement "design articles"
  (or artifact-centric articles). 
  - Such articles will typically also contain some empirical contribution and `method`/`result` are used
    for its description.  
  - The "designed features" mentioned above are known at design time
    and classified as `design`.
    This is in contrast to emerging features,
    which can only be determined empirically and are classified as `result`.
  - Top-level design _goals_ (and non-goals) are classified as `objective`.
    Subordinate design goals and non-goals are classified as `design`.
  - Statements about the design of subordinate artifacts, 
    that do not represent the main contribution but rather only aid an empirical study, 
    are classified as `method`.
- code `result:hype:incredible:i\d:u\d`:  
  information about the immediate outcome of a study in the form of
  empirical results. See `claim`.
  If the information is questionable because insufficient explanation of the underlying method
  was provided, use a `u` suffix to mark the doubts.
- code `summary:hype:incredible:u\d`:  
  A statement that summarizes several results, but does not provide new information.
  A summary statement does not generalize beyond the immediate results.

### 2.5 Core codes for _Outlook_

- code `fgap:u\d`:  
  Statement about what is still not known after the study.
- code `fneed:u\d`:  
  Statement about what future research should be done (by whoever).
  Also used when authors "hope" (etc.) for certain research to be done. 
- code `fposs:hype:u\d`:  
  Statement about what future research is now possible (i.e., could now be done, by whoever).  
  Note: Statements what practitioners can now do are `conclusion`!
- code `fwork:u\d`:  
  Statement about what future research the authors intend to do.


### 2.6 Structured abstracts' headings

Codes of the form `h-<xyz>` designate internal headings that occur in structured abstracts: 
A section intro term "Xyz:" or some synonym of that,
that announces subsequent `<xyz>` information.

It does _not_ matter whether the announcement is correct.
Singular and plural are considered equivalent.
If the heading is not terminated with a colon or period, the sentence will have multiple
codings, but the heading must be first in the sentence.

_Introduction_:
  - code `h-background`: "Background:", "Context:", "Introduction:", "Topic:", etc.

_Study Description_:
  - code `h-objective`: "Objective:", "Aim:", "Goal:", "Question:", etc.
  - code `h-design`: "Approach:" etc. (probably rare)
  - code `h-method`: "Method:", "Approach:" etc.
  - code `h-result`: "Result:" etc.
  - code `h-summary`: "Summary:" etc. (probably rare)
  - code `h-limitation`: "Limitations:" etc.  (probably rare)

_Outlook_:
  - code `h-conclusion`: "Conclusion:" etc.
  - code `h-fwork`: "Future work:", "Outlook:", etc.  (probably rare)

Note 1: Our codings are more differentiated than these headings
so that multiple different codings are often expected to occur after a heading `h-xx`,
not only `xx`.

Note 2: If `summary` occurs, it will typically follow `h-conclusion`, 
although it is logically part of Study Description, not Outlook.



### 2.7 Less common codes

- code `claim:i\d:u\d`:
  A non-empirical would-be result statement.
  In the article itself, the statement may have empirical backing, but in the abstract
  we cannot see which or where it may stem from.
  If position and phrasing allow it to be considered `background`, `objective`, or `conclusion`, use these.
- code `limitation:u\d`:  
  information about limitations, threats to validity, and the like
  of the study or its results.
- code `resourcepointer:i\d:u\d`:  
  A reference to a concrete external resource such as 
  a software artifact, materials package, data package, appendix,
  or similar item.


### 2.8 "Announcements"

- codes of the form `a-<xyz>` designate announcements:  
  A statement announcing (hence the `a-`) that the article body will 
  contain information of the `<xyz>` type, 
  but this and the next sentence do not contain such information.
  - code `a-background` (hopefully never to be seen)
  - code `a-claim` (hopefully never to be seen)
  - code `a-conclusion`
  - code `a-design` (e.g. "We present our system XYZ.")
  - code `a-fgap`
  - code `a-fneed`
  - code `a-fposs`
  - code `a-fwork`
  - code `a-gap`
  - code `a-limitation`
  - code `a-method` (e.g. "We describe the approach used for our survey.")
  - code `a-need`
  - code `a-objective`
  - code `a-result` (e.g. "We report on our empirical results in detail.",
    "For various parameters, we study the correlations."
    In some contexts, the latter could also be `a-method` or `method`.)
  - code `a-resourcepointer`
  - code `a-summary`


### 2.9 `-ignorediff`

All of the above codes are meant to be objective, which means that both
coders should arrive at the same coding.
This works most of the time, but has its limits when strage formulations
or overly complex sentences occur.
When the resulting coding discrepancies were flagged by the checking script,
it may happen that even after the coders have explained their respective views to each other
they can still not agree on a joint coding.

In that case one of them (and only one of them) has to add `-ignorediff` to the coding
to signal to the checking script that it must no longer flag this discrepancy.

- code `-ignorediff`:  
  If the script flags a coding discrepancy that, after discussion, you and your fellow coder
  agree should be left in (because the two codings represent two different reasonable interpretations),
  add this code in one (and only one) of the codings to mark the discrepancy as resolved.


### 2.10 Codes for special circumstances

- code `cruft`:  
  This sentence is not part of the abstract.
  It is garbage that should have been removed during the preparation of the abstract files.
- code `X`:  
  Undecided class. The sentence needs to be revisited and classified;
  consider using `fgrep {{X}}` to find these cases.
  Use `X` only rarely and only when you cannot _yet_ make up your mind.
  Such a code will likely result in a discrepancy with your fellow coder.
  It must always eventually be replaced with a proper code.


## 3. Codebook: Suffixes

As we saw above, a code may have one or more suffixes.
Suffixes are optional, so in a concrete coding, each suffix can be present or missing.

In contrast to the sentence classifications, which are intended to be objective
(hence the use of two coders and the use of `-ignorediff` where objectivity reaches its limits),
suffixes are optional additional attributes
that are considered subjective and need not (or not fully) agree between coders. 
Apply them with your own good judgment and keep in mind that
"we are gentle in detecting negative aspects".

There are binary suffixes, acting as flags, and 
variable suffixes that provide quantitative information.
We describe the flags first and the much more complicated quantitative "IU" suffixes then.


### 3.1 Flags

- suffix `:hype`:  
  The sentence praises the work beyond what a factual statement might state.
  The code does not talk about the truth of the statement (which is often difficult
  to judge from the abstract alone), but about the tone in which
  the statement is made.
  Plain positive properties do not qualify ("This is helpful because..."),
  only emphasized ones do ("This is tremendously helpful because...").
  "very" does not count as hype.
  The most common places for this to occur are 
  `need`, `method`, and `conclusion`.  
- suffix `:incredible`:  
  The sentence makes a statement that is very hard to believe, even after considering
  possible information that the reader of the abstract does not have.
- suffix `:timid`:  
  Applies to `conclusion` only. 
  To be used when the generalization made is overly vague or small.


### 3.2 About IU suffixes (`:i\d:u\d`)

We grade two **aspects**, each on a cardinality scale (count scale, absolute scale):
- informativeness gaps `i`: At how many spots the abstract noticably fails to provide information 
  it could presumably provide in the eyes of the given reader.
- understandability gaps `u`: At how many spots the abstract is unclear or ambiguous
  to the given reader.

**Goals:** What we want to assess is: 
- `i`: Is the space used efficiently to convey a lot of information in the abstract?
- `u`: Can I (as a reader) digest the information well?
What we do _not_ want to assess is:
- `i`: Does the information conveyed cover the most _relevant_ things to be said
  about the article?
- `u`: Is the understanding I have achieved actually correct?

**Syntax:** 
There are four cases, explained by example:
- `:i4:u3`: the sentence has 4 informativess gaps and 3 understandability gaps;
- `:i2`: 2 informativess gaps and 0 understandability gaps;
- `:u1`: 0 informativess gaps and 1 understandability gap;
- `` (no suffix at all): 0 informativess gaps and 0 understandability gaps.


### 3.3 IU suffixes: Informativeness gaps (`i\d`)

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


### 3.4 IU suffixes: Understandability gaps (`u\d`)

The spots in the abstract I have found where I feel that the abstract 
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


### 3.5 IU suffixes: What to count or not to count

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


### 3.6 Rationale: Which codes have IU suffixes?

We use IU suffixes only for some codes for the following reasons:
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


### 3.7 Historical notes

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


## 4. Coding rules: Avoiding inter-coder discrepancies

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
  remove it and its entire line.
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


## 5 Adding remarks on an abstract

At the end of an abstract there is a separator line consisting of three dashes.
Below that, you can add whatever remark you feel
should be recorded for this abstract -- most often none.
Write whatever text you like, just do not use '#' at the beginning of a line.
