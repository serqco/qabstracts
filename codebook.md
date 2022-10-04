# Codebook and coding rules for qabstracts study

created: Lutz Prechelt, 2022-07-14  
changed: Lutz Prechelt, 2022-10-04


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
   No part of any sentence pertains to two codes at once.
5. For annotation, a sentence is interpreted in its 
   backward and forward context, not in isolation.
   In particular, when a sentence can be an A or a B, but only a B is expected
   in this position, it is interpreted as a B.
6. If a classification requires a guess about what is (or is not) in 
   the article and that guess is estimated to be less than 75% reliable,
   append a `?` to the respective code. 
   Use this sparingly.


## 2. Codebook: Codes for sentences

Note: Our annotation checking script gathers the set of codes to check
for directly from this file by looking for strings of the form
"code `something-or-other`".
Make sure all code declarations take this form and no other things do.
(Allowing synonyms for the codes may be nice for graders in the beginning,
but appears to have a bad cost/benefit tradeoff, so we do not do this.)

The meanings of starting with a dash or ending with ":N" are explained
in subsequent sections.

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
- code `conclusion:N`:  
  A take-home message that is less specific than one or more results.
  Either a generalization from the results or an existence proof statement.
- code `design:N`:  
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
- code `-hype`:  
  The sentence praises the work beyond what a factual statement might state.
  Plain positive properties do not qualify ("This is helpful because..."),
  only emphasized ones do ("This is tremendously helpful because...").
  "very" does not count as hype.
  This code is not a classification of a sentence, but an additional attribute.
  It can never occur alone, only in conjunction with one of the others and
  should be given last.
- code `limitation:N`:  
  information about limitations, threats to validity, and the like
  of the study or its results.
- code `method:N`:  
  information about the approach or setup of an empirical study.
- code `objective`:  
  this work's research goal;  
  this work's specific research interest;  
  this work's research question.  
- code `resourcepointer`:  
  A concrete reference to a concrete external resource such as 
  a software artifact, materials package, data package, appendix,
  or similar item.
- code `result:N`:  
  information about the immediate outcome of a study in the form of
  empirical results. See `claim`.
- code `X`:  
  Undecided class. The sentence needs to be revisited and classified;
  consider using `fgrep {{X}}` to find these cases.
  Use `X` only when you cannot _yet_ make up your mind.
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


## 4. Coding rules: Information particle count

At least for some types of information, e.g. `method`, `design`, and `result`,
the informativeness
of an abstract will likely become better if more details are provided.
We measure this aspect by counting the number of "information particles"
that are mentioned in such a statement.

This is why some codes, such as `result:N`, have that `:N` suffix.
The `N` is meant to be replaced by an integer value: the number of 
information particles in that sentence.

The notion of information particle is subtle, so there is no closed definition.
Rather, we explain the concept by basic rules plus examples below.


### 4.1 Basic rules

- Counting is based on noun phrases, each counting as one or more information particles
  as described below. Other material is ignored:
- All "small words" count as 0:
  articles ("the", "a", ...), 
  pronouns (including personal pronouns serving in a noun-like role: "we", "it", ...),
  conjunctions ("and", "then", ...),
  prepositions ("of", "with", ...),
  unconcrete quantifiers ("many", "several", "all", "every", "no", ...).
- Adverbs ("...ly") count as 0.
- Verbs in all their forms count as 0.
  In abstracts, verbs are often uninteresting glue, so they do not count, even if they
  _happen to be_ informative in the particular case.
  This reduces semantic noise in the count and also makes the counting simpler.
- Nouns count as 1. 
  They can be simple nouns ("complexity"), proper nouns ("BeAFix"), compound nouns ("complexity reduction"),
  nouns with identifier ("candidate A"), nouns with abbreviation ("complexity reduction (CR)").
- Adjectives: The first adjective attached to a noun counts as 0, because so many nouns in abstracts need one.
- Each additional adjective counts 1. Each number (with its unit of measurement) counts 1.
  A stand-alone adjective counts 1.
- For simplicity, additional components of the noun phrase such as
  prepositional phrases, infinitive phrases, relative clauses, and others
  are considered and counted separately.  
  https://en.wikipedia.org/wiki/Noun_phrase#Components  

This counting is laborious while learning the rules, but not difficult once learned.

The above rules cover a lot of ground, but there are still lots of unclear cases.
The following examples will cover about half of those. Decide the rest by extrapolation.


### 4.2 Example particle counts explained

The first example accounts for every word;
later ones take more and more things counting 0 for granted and do not spell them out.

- <i>"We evaluated the attack effectiveness using 5 state-of-the-art deep learning models and  
  real-world samples collected from 30 users."</i> `{{method:6}}`
  - 0: "We": pronoun
  - 0: "evaluated": verb
  - 1: "attack effectiveness": compound noun
  - 0: "using": verb (not really; we are simplifying some grammar concepts)
  - 2: "5 state-of-the-art deep learning models": number, compound noun with one adjective
  - 1: "real-world samples": noun with adjective
  - 0: "collected": verb
  - 2: "30 users": number, noun
- <i>"BeAFix is backed with a novel strategy for bounded exhaustive, yet scalable, exploration of 
  the spaces of fix candidates and a formally rigorous, sound pruning of such spaces."</i> `{{design:10}}`
  - 1: "BeAFix is backed": proper noun, (verb "is backed" is ignored)
  - 1: "novel strategy": noun with adjective
  - 3: "bounded exhaustive, yet scalable, exploration": 2 additional adjectives, noun with adjective.
    We count "bounded" and "exhaustive" as two adjectives although semantically they could be considered one.
  - 2: "spaces of fix candidates": noun, compound noun
  - 1: "formally rigorous": (adverb ignored), adjective
  - 2: "sound pruning of such spaces": noun with adjective, noun with adjective
- <i>"Evaluated on our dataset of 23 projects with flaky tests, FlakeFlagger outperformed the prior approach
  (by F1 score) on 16 projects and tied on 4 projects."</i> `{{result:11}}`
  - 1: "Evaluated on our dataset": (verb ignored), noun with adjective
  - 3: "23 projects with flaky tests": number, noun, noun with adjective
  - 2: "FlakeFlagger outperformed the prior approach": proper noun, (verb ignored), noun with adjective
  - 1: "F1 score": compound noun
  - 2: "16 projects": number, noun
  - 2: "tied on 4 projects": (verb ignored), number, noun
- The remaining two examples are more complex, because their coding involves more than one code:
- <i>"To overcome these challenges and aid developers in this task, this paper presents TANGO, a duplicate
  detection technique that operates purely on video-based bug reports by leveraging both visual and 
  textual information."</i> `{{objective,design:6}}`
  - 0: "To overcome these challenges and aid developers in this task": This is the `objective` part of the sentence
    and is hence not analyzed for the count.
  - 2: "this paper presents TANGO": noun, (verb ignored), proper noun
  - 1: "duplicate detection technique": compound noun (there is no adjective involved!)
  - 1: "operates purely on video-based bug reports": (verb and adverb ignored), compound noun with adjective
  - 2: "visual and textual information": stand-alone adjective, noun with adjective
- <i>"We describe the design of a Crowd Planning Poker (CPP) process implemented on Amazon Mechanical Turk 
  and the results of a substantial set of trials, involving more than 5000 crowd workers and 
  39 diverse software tasks."</i> `{{design:3,method:7}}`
  - Design part (up to "end"):
    - 1: "We describe the design": noun
    - 1: "Crowd Planning Poker (CPP) process": compound noun
    - 1: "Amazon Mechanical Turk": proper noun
    - (Note that "We describe the design of a Crowd Planning Poker (CPP) process" alone would have been an `a-design`,
      only the "implemented on" suffix makes the whole thing a `design`.)
  - Method part:
    - 3: "results of a substantial set of trials": noun, noun with adjective, noun.
      ("substantial" grammatically refers to "set of trials". We simplify once again to get simpler rules -- and
      in the present case (if not every other) it makes no difference for the count.)
    - 4: "5000 crowd workers and 39 diverse software tasks": number, compound noun, number, compound noun with adjective

Now try counting each example yourself and compare the results.
Understand where the differences come from.
If you find a severe ambiguity in the rules, speak up!

Later in real coding, we will not strive for exact counts and will
consider differences up to 33% acceptable (e.g. 4 vs. 6).


## 5. Codebook: Global codes for entire abstracts

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


### 5.1 The global codes

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

If you have **deep knowledge** in the article's subject matter,
grade as if you were only normally knowledgable
in order to make agreement with your fellow coder more likely.


### 5.2 Remarks

In the lines directly below the global codes, you can add whatever remark 
feels like it should be recorded for this abstract.
Write whatever text you like, just do not use '#' at the beginning of a line.


### 5.3 Historical note

A third global aspect was proposed: appeal.
How much does an abstract trigger a reader's interest in learning 
more about the work?

This is likely too dependent on the specific grader's interests spectrum
to lead to useful results: If I am interested in the topic area,
an abstract can have more appeal or less.
But if I am not much interested in the topic area (and in our grading process,
this will be the usual case), even the best abstract will not have 
much appeal to me.  
Decision: We do not grade appeal.