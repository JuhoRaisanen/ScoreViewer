import glob
import ghostscript
import locale
import os
from scoreView import *
from testing import *

def convertPdfs(path):
    pdfs = get_all_pdfs(path)
    for pdf in pdfs:
        name = pdf.split('.pdf')[0]
        pdf_to_jpg(
            pdf,
            name
        )
		

def analyzeJpgs(path):
	jpgs = get_all_jpgs(path)
	results = []
	for jpg in jpgs:
		name = jpg.split('.jpg')[0]
		fileResults = analyzeJpg(name, path)
		results.append(fileResults)
			
	#printTestResults(results)


def analyzeJpgFile(filename, path):
	analyzeJpg(filename, path)
		
		
def pdf_to_jpg(pdf_input_path, jpeg_name):
    args = ["pdf2jpeg",  # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            "-r300",
            f'-sOutputFile={jpeg_name}-%03d.jpg',
            pdf_input_path]
    encoding = locale.getpreferredencoding()
    args = [a.encode(encoding) for a in args]
    with ghostscript.Ghostscript(*args) as g:
        ghostscript.cleanup()


def get_all_pdfs(path):
    pdf_files = glob.glob(os.path.join(path, '*.pdf'))
    return pdf_files
	
def get_all_jpgs(path):
    jpg_files = glob.glob(os.path.join(path, '*.jpg'))
    return jpg_files

