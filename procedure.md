# Overall procedure for executing the 'qabstracts' study

created: Lutz Prechelt, 2022-09-21  
changed: Lutz Prechelt, 2022-10-04 


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

1. `git pull`
2. Edit `prestudy2/sample-who-what.txt`.
   Find the first block B that has an empty column C and that you have not yet worked on.
   Enter your firstname in all rows of the leftmost column C of block B.
3. `git add prestudy2/sample-who-what.txt; git commit -m"<firstname> will code block <B> <C>"; git push`    
   For instance, if you are Lutz and you picked column `abstracts.A` in block 3, 
   the commit message is "Lutz will code block 3 A".  
   Make sure the pull and the push are no more than 3 minutes apart so that it becomes
   unlikely that your edit conflicts with somebody else's.
4. For each abstracts file in your block (e.g. `prestudy2/abstracts.A/AbcDefGhi21.txt`):
   1. Classify each sentence with usually one or sometimes two or even three codes.
      Do not add counts (because that is distracting).
   2. Step back. Add the global codes `#inf-...` and `#und-...`.
   3. Is anything special about this abstract that we should remember?
      Then add a remark below (but usually not).
   4. Now revisit your codes in need of counting (see `codebook.md`, e.g. design, method, result, limitation,
      conclusion) and count the information particles. Enter the counts.
5. If you have Python set up, run
   `python script/qabstracts.py check-codings prestudy2`  
   If all it says is something like "checking 80 files", all is well.
   Otherwise, repair any problems you find, even if you have not produced them (if the solution is obvious).  
   This checked the codings in isolation. Next is checking them against those of your fellow coder:  
   `python script/qabstracts.py compare-codings prestudy2`  
   If problems occur here, consult with your fellow coder and resolve them together.  
   If you have no Python, skip this step.
   If your Python is not found, try `python3` in the commands above.
6. Now add the files of the block to the git index
   using either `git add -i` or (preferably) the git GUI of your choice.
7. `git commit -m"<firstname> has coded block <B> <C>"`
8. Make sure you got the commit message right.
   Use `git commit --amend ...` if not.
9. `git push`  
   (Took a while? Yes. But the next block will be so much quicker!)