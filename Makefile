QABSTRACTS=python3 script/qabstracts.py
STUDYDIR=abstracts

EXPORTFILE=results/$(STUDYDIR)-results.tsv
TIMESTAMPFILE=results/git_timestamps.json

all:
	echo "There is no top-level target. Pick a specific one:"
	grep '^[a-zA-Z][a-zA-Z0-9_-]*:' Makefile

check-codings:
	$(QABSTRACTS) check-codings $(STUDYDIR)

compare-codings:
	$(QABSTRACTS) compare-codings $(STUDYDIR)

export:
	$(QABSTRACTS) export $(STUDYDIR) >$(EXPORTFILE)
	$(QABSTRACTS) extract-git-timestamps

pdf:
	cd tex; latexmk -bibtex qabstracts-tse

plotall:
	$(QABSTRACTS) plot --plotall --printall $(EXPORTFILE) img

plot:
	$(QABSTRACTS) plot $(EXPORTFILE) img

printall:
	$(QABSTRACTS) plot --printall $(EXPORTFILE) img
