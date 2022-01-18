
"""
The Star And Thank Author License (SATA)

Copyright (c) 2021 Piotr Piekielny (pp.piekielny@gmail.com)

Project Url: https://github.com/retip94/pdf-to-jpg

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice should be included in all copies or substantial portions of the Software.

And wait, the most important, you should star/+1/like the project(s) in project url section above first, and then thank the author(s) in Copyright section.

Here are some suggested ways:

Email the authors a thank-you letter, and make friends with him/her/them. Report bugs or issues. Tell friends what a wonderful project this is. And, sure, you can just express thanks in your mind without telling the world. Contributors of this project by forking have the option to add his/her name and forked project url at copyright and project url sections, but shall not delete or modify anything else in these two sections.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import glob
import ghostscript
import locale
import os
from scoreView import *

def convertPdfs(path):
    pdfs = get_all_pdfs(path)
    for pdf in pdfs:
        name = pdf.split('.pdf')[0]
        pdf_to_jpg(
            pdf,
            name
        )
		

def analyzeJpgs(path, maxPages):
	i = 0
	jpgs = get_all_jpgs(path)
	for jpg in jpgs:
		name = jpg.split('.jpg')[0]
		analyzeJpg(name, path)
		
		i += 1
		if i == maxPages:
			break
			

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

