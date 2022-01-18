from pdfConverter import *
from pathlib import Path
import cv2 as cv


def main():
    e1 = cv.getTickCount()

    p = Path('files')
    p.mkdir(exist_ok=True)

    path = p.resolve()
    maxPages = 100
    convertPdfs(path)
    analyzeJpgs(path, maxPages) 
    #analyzeJpgFile('IMSLP00716-Schumann_-_Humoreske,_Op_20-001', path)

    #timer
    e2 = cv.getTickCount()
    time = (e2 - e1)/ cv.getTickFrequency()
    print('Execution finished at total: ' + str(time))



if __name__ == '__main__':
    main()

