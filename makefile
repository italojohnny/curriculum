DOCNAME=italojohnny_`date +'%Y%m%d'`
SOURCES=$(wildcard *.tex)
VIEWER=mupdf


default: $(SOURCES)
	pdflatex -jobname $(DOCNAME) main.tex
	make clear

view: default
	$(VIEWER) $(DOCNAME).pdf

clear:
	find -regex ".*\.\(aux\|log\|nav\|out\|snm\|toc\|idx\\)" -type f -delete

clearall: clear
	rm -f $(DOCNAME).pdf
