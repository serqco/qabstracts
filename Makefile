QABSTRACTS=python3 script/qabstracts.py
STUDYDIR=abstracts

EXPORTFILE=results/$(STUDYDIR)-results.tsv
TIMESTAMPFILE=results/git_timestamps.json

# You can call e.g. "make pdf" or "make pdf KNIT_ARGS=debug"
KNIT_ARGS ?=

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

knit:
	Rscript -e "library(knitr); knit('tex/qabstracts-tse.Rnw', output='tex/qabstracts-tse.tex')" --args $(KNIT_ARGS)

sanity:
	Rscript -e "library(rmarkdown); render('script/quality-check.Rmd')"

pdf: knit
	cd tex; latexmk -pdf -bibtex qabstracts-tse

pdf-nonstop: knit
	cd tex; latexmk -pdf -bibtex -interaction=nonstopmode qabstracts-tse

pdf-cleanfiles:
	cd tex; rm -f *.{aux,bbl,blg,fdb_latexmk,fls,log,out,pdf}

plotall:
	$(QABSTRACTS) plot --plotall --printall $(EXPORTFILE) img

plot:
	$(QABSTRACTS) plot $(EXPORTFILE) img

printall:
	$(QABSTRACTS) plot --printall $(EXPORTFILE) img
