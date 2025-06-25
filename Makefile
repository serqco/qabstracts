QABSTRACTS=python3 script/qabstracts.py
STUDYDIR=abstracts

EXPORTFILE=results/$(STUDYDIR)-results.tsv
TIMESTAMPFILE=results/git_timestamps.json

ZENODO_ZIP=zip/qabstracts-zenodo.zip
ZENODO_FILES=README.md codebook.md history.md INSTALL.md LICENSE LICENSE-DATA \
    Makefile procedure.md requirements.txt serqco-abstracts-structure.md \
    abstracts \
    img \
    prestudy/abstracts.A prestudy/abstracts.B prestudy/abstracts.raw \
    prestudy/explain-the-study-2022-08-31.txt prestudy/README.md \
    prestudy2 \
    script \
    tex/qabstracts-tse.Rnw tex/qabstracts-tse.tex tex/qabstracts-tse.pdf \
    tex/our-abstract.txt tex/appendix.tex tex/*.jpg tex/special.bib
ARXIV_ZIP=zip/qabstracts-arxiv.zip
ARXIV_FILES=img tex/qabstracts-tse.tex tex/qabstracts-tse.bbl tex/*.jpg
TSE_ZIP=zip/qabstracts-tse.zip

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

extract-git-timestamps:
	$(QABSTRACTS) extract-git-timestamps  # requires the full git repo!

knit:
	Rscript -e "library(knitr); knit('tex/qabstracts-tse.Rnw', output='tex/qabstracts-tse.tex')" --args $(KNIT_ARGS)

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
	$(QABSTRACTS) plot --printall $(EXPORTFILE) img  # mostly obsolete: now covered by knitr

zip: zenodo_zip arxiv_zip

zenodo_zip:
	rm -rf $(ZENODO_ZIP) script/.pytest_cache  # clean, to avoid unwanted content
	zip -r -q $(ZENODO_ZIP) $(ZENODO_FILES) 

arxiv_zip:
	rm -rf $(ARXIV_ZIP)
	zip -r -q -j $(ARXIV_ZIP) $(ARXIV_FILES)

tse_zip:
	rm -rf $(TSE_ZIP)
	zip -r -q -j $(TSE_ZIP) $(ARXIV_FILES)  # PDF file is needed, but uploaded separately
