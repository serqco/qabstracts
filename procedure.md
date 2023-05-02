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

You need a work environment equipped with 
[git](https://git-scm.com/book/en/v2) and a text editor or IDE.

Additionally, a Python setup is very convenient, because it allows you to run the 
checking scripts locally _before_ checking in your codings.
Even without a local Python installation, GitHub will run the checking scripts
whenever you check in any file and send an email if there are any problems.

### 2.1 I have a development setup already and know how to use it

- Just use whatever IDE or editor you are most familiar with.
  Learn how to open a file by partial filename instead of by browsing; 
  you will need this a lot when resolving disagreements.
- Set up Python (see below) if you want to run the checking scripts locally.

### 2.2 I have no development setup and want the simplest possible solution

- Log into GitHub
- Use the free GitHub online VS Code IDE [github.dev](https://github.dev/serqco/qabstracts/)
- Learn how to create a Git commit involving several files.
  Read it up in 
  [the documentation](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor#using-source-control)
- In this setup, you cannot run the Python checking scripts yourself.
  You need to perform a commit to have the GitHub CI run them for you.
  Please create a commit only when coding your block is finished
  to avoid cluttering our commit history too much (it will be cluttered already
  by the additional mistake-fixing commits you will likely need from time to time).

### 2.3 I have no development setup but want to install and learn one

- Get Git. 
  - On Windows, install [git for windows](https://gitforwindows.org/).
    "Git Bash" will become the command line shell that you need to use,
    not CMD or PowerShell.
  - On Debian/Ubuntu, do `sudo apt install git`
  - On Mac OS X, do the equivalent of the above with HomeBrew.
- [Set up SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
- Start a shell and the ssh-agent, add your SSH keys to the agent,
  visit the place where your `qabstracts` work directory should be created, and do
  `git clone --recurse-submodules git@github.com:serqco/qabstracts.git`.
- `cd qabstracts`. This directory is where you will do 
  all the git calls (if you do them from the command line rather than the IDE) and 
  Python calls.
- As an IDE, install either
  [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download)
  or
  [Visual Studio Code](https://code.visualstudio.com/) (usually called VS Code).
  Both work perfectly fine for our purposes.
- In the IDE documentation, learn the following functions:
  - setting up Git (and then do that once now)
  - Opening a file by typing or pasting a fraction of its filename
    (which you will want to pick from `sample-who-what.txt` or a checking script message)
  - Git `commit`
  - Perhaps also Git `push`, `pull` (with rebase, not merge), `log`. 
    - 🥸 __Pro tip__: Call `git config pull.rebase true` once to have all `git pull`s in this repo do rebases automatically 
- You can mix Git use on the command line with Git use in the IDE.
  For instance, the IDE is unbeatably good for creating commits,
  but some people prefer the command line for `push`, `pull` and `log`.

### 2.4 I want to set up Python to run the checking scripts locally

The scripts are programs to be called from the command line.

- Depending on your setup, the resulting Python command may be called `python` or `python3` and
  the Pip command may be called `pip` or `pip3`. Try the second variant first.
- Install Python 3.8 or higher: https://www.python.org/
- Create a [Python virtual environment](https://docs.python.org/3/library/venv.html)
  (or "venv" for short)
- [Activate](https://docs.python.org/3/library/venv.html#how-venvs-work) the venv. 
  Whenever you start a new command line shell, you need to activate the venv there.
- Go to the qabstracts directory and execute `pip install -r requirements.txt`
  to install the libraries required by the scripts.
- Should additional dependencies be introduced in the scripts later,
  repeat the above step to add them into your venv.


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
