default:
	pdflatex main.tex

clear:
	find -regex ".*\.\(aux\|log\|nav\|out\|snm\|toc\|idx\\)" -type f -delete
