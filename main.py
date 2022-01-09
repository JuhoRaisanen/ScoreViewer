from pdfConverter import *
import cv2 as cv


def main():
	e1 = cv.getTickCount()
	
	#convertPdfs()
	analyzeJpgs() 
	#analyzeJpgFile('Adagio-003')
	
	#timer
	e2 = cv.getTickCount()
	time = (e2 - e1)/ cv.getTickFrequency()
	print('Execution finished at total: ' + str(time))



if __name__ == '__main__':
    main()

