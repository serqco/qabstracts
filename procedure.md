# Overall procedure for executing the 'qabstracts' study

created: Lutz Prechelt, 2022-09-21  
changed: Lutz Prechelt, 2023-03-06


## 1. Overall procedure

1. Find a team of 2-8 people who want to participate.
2. Decide which volumes (years) of articles to include,
   prepare `script/download-volumes.sh` accordingly.  
   Obey the directory layout as described in README.md.
   Run it.
3. Decide on the maximum sample size and the coding block size and call
   `script/qabstracts.py select-sample` accordingly.
4. Implement all required layout type descriptions in `qabs/extract_abs.py`.
   Make sure the abstracts extraction works as good as it can for each venue in the sample.
5. Create abstracts files by running
   `script/qabstracts.py prepare-sample`.  
   For journals with a layout for which abstracts extraction works nonperfectly,
   correct those abstracts by hand. See `abstracts/sample.list` for which those are.
6. Set up `.github/workflows/do_it_all.yml` appropriately, so that each coder receives
   checking output after every `git push`.
   Tell the coders to subscribe to the notifications.
7. Make annotations. 
   The participating coders annotate blocks of abstracts at their own pace.
   See "Annotating one block of abstracts" below.
8. Evaluate results (to be described)
9. Write article


## 2. Coders: Setting up your environment

- You need a work environment equipped with 
  [git](https://git-scm.com/book/en/v2) and a text editor.
- Optional: If you also have Python 3.8 or younger at hand, all the better.
- This is easy for users on Linux or Mac OS X.
  Windows users can get by with 
  [git for windows](https://gitforwindows.org/), 
  but I recommend
  [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
  for a more complete setup (e.g. with manpages and Python).
- Alternatively, you could use [GitHub Desktop](https://desktop.github.com/).
  I have no experience with this.
- [Set up SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
  You can do without this, but it will be inconvenient:
  You will have to use the `https:` clone URL and input your GitHub password upon each `push` or `pull`.
- Start a shell, visit the place where your `qabstracts` work directory should be created and do
  `git clone git@github.com:serqco/qabstracts.git`.
- If you work without SSH keys, do
  `git clone https://github.com/serqco/qabstracts.git` instead.


## 3. Coders: Annotating one block of abstracts

This is the prestudy version of the description.
The final version will talk of `abstracts/` instead of `prestudy2/`.

### 3.1 Long version for learning

1. `git pull`
2. Edit `prestudy2/sample-who-what.txt`.
   Find the first block B that has an empty column C and that you have not yet worked on.
   Enter your firstname with a leading dash in all rows of the leftmost column C of block B,
   e.g. `-Lutz`. This reserves those files for you to annotate so that nobody else works on them.
3. `git add prestudy2/sample-who-what.txt; git commit -m"<firstname> will code block <B> <C>"; git push`    
   For instance, if you are Lutz and you picked column `abstracts.A` in block 3, 
   the commit message is **"Lutz will code block 3 A"**.  
   Make sure the pull and the push are no more than 3 minutes apart so that it becomes
   unlikely that your edit conflicts with somebody else's.
4. For each abstracts file in your block (e.g. `prestudy2/abstracts.A/AbcDefGhi21.txt`):
   1. Classify each sentence with usually one or sometimes two or three codes.
   2. Step back. Is anything special about this abstract that we should remember?
      For instance, does it contain anything that makes a good example in the article?
      Then add a remark below (but usually not).
5. Edit `prestudy2/sample-who-what.txt` and remove the dashes you inserted in step 2,
   leaving your name only. This reports that the annotations of those files are done.
6. If you have Python set up, run
   `python script/qabstracts.py check-codings prestudy2`  
   If all it says is a list of coders, all is well.
   Otherwise, repair any problems you find, even if you have not produced them (if the solution is obvious).  
   This checked the codings in isolation. Next is checking them against those of your fellow coder:  
   `python script/qabstracts.py compare-codings --onlyfor <firstname> prestudy2`  
   If problems occur here, consult with your fellow coder and resolve them together.  
   If you have no Python, skip this step.
   If your Python is not found, try `python3` in the commands above.
7. Now add the files of the block to the git index
   using either `git add -i` or (preferably) the git GUI of your choice.
8. `git add prestudy2/sample-who-what.txt; git commit -m"<firstname> has coded block <B> <C>"`
   (e.g. **"Lutz has coded block 3 A"**)
9. Make sure you got the commit message right.
   Use `git commit --amend -m"<firstname> has coded block <B> <C>"` if not.
10. `git push`  
    In case of conflicts, do `git pull --rebase`, then repeat the push.    
    **Always use rebase, not merge** to keep our history tidy.

Took a while? Yes. But the next block will be so much quicker!


### 3.2 Short version as a memory aid after learning

- pull; reserve a block in 'sample-who-what.txt'; commit (e.g. **"Lutz will code block 3 A"**); push
- code the abstracts
- possibly run 'check-codings' and 'compare-codings'
- adjust 'sample-who-what.txt'; commit it and all abstracts (e.g. **"Lutz has coded block 3 A"**); push


### 3.3 Fixing problems after coding

- Once you have coded a block, it is "yours" and you'll never need to make a reservation
  again when you want to modify its files.
- If you have made **syntactical** mistakes and get messages in the 
  "check individual files" department, 
  correct them ASAP (because they block the more important "check pairs of files" messages)
  and commit them with messages of the form  
  **"Lutz fixed block 3 A"**
- You can and should do this for such mistakes of other coders as well
- If you made **semantical** changes to a block of yours (whether based on solo decisions
  or after discussing messages with your fellow coder), 
  commit them with messages of the form  
  **"Lutz adjusted block 3 A"**

## 4. Evaluators: Questions to answer

Here is a list of questions that might be interesting to investigate
during the  evaluation of the coding data:

### 4.1 Statistical evaluation

We ask most of these questions both globally and per venue.  
We ask most of these questions also separately for structured abstracts vs. unstructured ones.    
For density measures, use three denominators: #sentences, #words, #chars.  
...

- Fraction of space devoted to each of the basics:
  - empirical articles devote almost as much space to `background` than to `results`,
    design articles devote twice as much to `background` than to `results`.
  - structured abstracts have a better length balance of the core parts
    than unstructured ones
- How often each of the basics is missing completely
- How often multiple basics are missing
- Distribution of number of i and u problems overall in an abstract
- Relative frequency of i and u problems per basic code
  - design articles appear to have most of their gaps in `method`, 
    empirical ones in `result`
- Frequency of `a-*` codes
- Frequency of `claim` and `-hype`
- Frequency of unresolved intercoder differences (`ignorediff`)
- Common abstracts structures (clustering) in terms of their basics stretches sequence

### 4.2 Qualitative evaluation

Discuss examples of the following:

- Very long sentences
- Recurring coder disagreements
- Sentences with particularly many i problems
- Sentences with particularly many u problems

Especially these curiosities:

- Sentences with rare combinations of codes
- First sentences with rare codes
- Last sentences with rare codes


## 5. SERQco members: Ideas for subsequent studies

- A study of conclusions could start with abstracts sentences annotated as `conclusion`
  and focus on the corresponding parts of the article body.
- ...
