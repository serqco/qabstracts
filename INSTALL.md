created: Lutz Prechelt, 2025-06-06

### System Requirements

We have used a Debian Linux environment for running our code, but any other Linux should do as well.
Debian version was 12 ("Bookworm"), but we expect later versions to work just fine.
The Python code was used with dependencies as of 2022-2025, but we expect later versions to work just fine.
Ditto for the R code.

### Installation Instructions

Clone this repository with submodules or else you will be missing the `script/qscript` directory
and the scripts will not execute successfully.

Install Python, pip, R, knitr, and tidyverse:  
`sudo apt install python3 python3-pip python-is-python3 r-base r-cran-knitr r-cran-tidyverse`

Create a Python virtual environment, activate it, and install the dependencies:

```bash
mkdir ~/venvs
python -m venv ~/venvs/qabstracts
source ~/venvs/qabstracts/bin/activate  # assuming Bash; repeat this step for each usage session
pip install -r requirements.txt
```

### Steps to Reproduce

```bash
make export plotall pdf
```

The end result is `tex/qabstracts-tse.pdf`, the article.

Note that a _full_ reproduction requires running `make extract-git-timestamps` before the
`make plotall` in order to create the `img/qabstracts_timeline_commits.pdf` plot.
That command, however, requires a complete clone of the entire git repository to work.
If you do not perform this command, the plot will rely on the existing command output
in `results/git_timestamps.json`.
