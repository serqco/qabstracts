"""Get the expensive data for plot_qabstracts_timeline_commits, write it to git_timestamp_file"""
import json
import subprocess
import typing as tg

import qscript


git_timestamp_file = "results/git_timestamps.json"
meaning = f"""Retrieves subsets of commits according to the filespecs in the hardcoded git_timestamp_cases
  and writes the corresponding Unix timestamps lists to '{git_timestamp_file}' as JSON.
"""
git_timestamp_cases = [  # y, label, symbol, files
    (5.0, "codebook", "C", "codebook.md procedure.md"),
    (4.0, "training", "T", "prestudy2/abstracts.?"),
    (3.0, "coding", "A", "abstracts/abstracts.A"),
    (2.8, "", "B", "abstracts/abstracts.B"),
    (2.0, "stat. eval.", "E", "script/qabs/dataframes.py script/qabs/plot.py script/qabs/printstats.py script/qscript/annotations.py"),
]


def add_arguments(subparser: qscript.ArgumentParser):
    pass  # no options or arguments; the only input is the entire git directory itself


def execute(args: qscript.Namespace):
    args  # noqa, not used
    result = dict()
    for y, l, s, filespec in git_timestamp_cases:
        result[filespec] = git_commit_timestamps(filespec)
    with open(git_timestamp_file, 'wt', encoding='utf8') as f:
        json.dump(result, f)


def git_commit_timestamps(filespec: str) -> tg.Sequence[int]:
    # an expensive operation!
    git_cmd_base = "git log --pretty='format:%at' "  # one unix timestamp per line
    result = subprocess.run(git_cmd_base + filespec, shell=True, capture_output=True)
    assert not result.stderr, result.stderr
    timestamps = [int(line) for line in result.stdout.splitlines(keepends=False)]
    return timestamps
