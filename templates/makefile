DOCNAME=italojohnny_`date +'%Y%m%d'`
SOURCES=$(wildcard *.tex)
VIEWER=mupdf

CONFIG=config.txt
SCRIPT=script.py
BACKUPDIR=backup
BUILDDIR=build

INFO=$$(cat $(CONFIG) | egrep "INFO=" | egrep -io "[^=]*\.json$$")
TEMPLATE=$$(cat $(CONFIG) | egrep "TEMPLATE=" | egrep -io "[^=]*\.tex$$")

default: make_dir
	@clear
	@python $(SCRIPT) $(INFO) $(TEMPLATE) $(BUILDDIR)
	@cd $(BUILDDIR); pdflatex -jobname $(DOCNAME) output.tex
	@mv $(BUILDDIR)/$(DOCNAME).pdf $(BACKUPDIR)


make_dir:
	@mkdir -p $(BACKUPDIR)
	@mkdir -p $(BUILDDIR)


clear:
	@rm $(BUILDDIR) -rf
	@find -regex ".*\.\(aux\|log\|nav\|out\|snm\|toc\|idx\\)" -type f -delete


clearall: clear
	rm -f $(DOCNAME).pdf
