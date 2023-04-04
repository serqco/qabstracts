QABSTRACTS=python3 script/qabstracts.py
STUDYDIR=abstracts

EXPORTFILE=results/$(STUDYDIR)-results.tsv

all:
	echo "There is no top-level target. Pick a specific one:"
	grep '^[a-zA-Z][a-zA-Z0-9_-]*:' Makefile

check-codings:
	$(QABSTRACTS) check-codings $(STUDYDIR)

compare-codings:
	$(QABSTRACTS) compare-codings $(STUDYDIR)

export:
	$(QABSTRACTS) export $(STUDYDIR) >$(EXPORTFILE)

pdf:
	cd tex; pdflatex qabstracts-tse

plot:
	$(QABSTRACTS) plot --plotall $(EXPORTFILE) img

plot1:
	$(QABSTRACTS) plot $(EXPORTFILE) img
