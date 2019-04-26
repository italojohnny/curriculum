DOCNAME=italojohnny_`date +'%Y%m%d'`
SOURCES=$(wildcard *.tex)
VIEWER=mupdf -r 60


default: $(SOURCES)
	python main.py
	pdflatex -jobname ./build/$(DOCNAME) ./build/output.tex
	make clear

view: default
	$(VIEWER) ./build/$(DOCNAME).pdf

clear:
	find -regex ".*\.\(aux\|log\|nav\|out\|snm\|toc\|idx\\)" -type f -delete

clearall: clear
	rm -f ./build/$(DOCNAME).pdf
