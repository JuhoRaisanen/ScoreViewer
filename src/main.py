from pdfConverter import *
from pathlib import Path
import cv2 as cv


def main():
    e1 = cv.getTickCount()

    p = Path('files')
    p.mkdir(exist_ok=True)

    path = p.resolve()
    
    convertPdfs(path)
    analyzeJpgs(path) 
    #analyzeJpgFile('BalladeGm-001', path)

    #timer
    e2 = cv.getTickCount()
    time = (e2 - e1)/ cv.getTickFrequency()
    print('Execution finished at total: ' + str(time))



if __name__ == '__main__':
    main()

