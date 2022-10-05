"""
Algorithm steps:
0. Input music score page in jpg format

1. Hough Line Transform analysis to detect vertical lines

2. Eliminating too short lines and lines stacked together

3. Orders lines to rows according to their y-value

4. Calculates row metrics:
a. Average line length
b. Row length
c. Number of bars

5. Eliminates score rows with low metrics
"""
from functions import *
from globals import *


def analyzeJpg(fileName, path):
	
	print()
	print()
	print(f'Analyzing the file {str(fileName)} ......')	

	start = startTimer()
	img = cv.imread(os.path.join(path, f'{fileName}.jpg'))
	img_h, img_w, img_channel = img.shape

	#parameters
	setHEIGHT(img_h//20)
	setWIDTH(img_w//15)
	line_precision = 15

	#line detection
	lines = imageAnalysis(img, line_precision)

	points = []	#starting point of a line: (x, y, length)
	line_lengths = [0]*(img_h // 50) ##length starting from 0, increasing 50 by 1 index
	if(lines is not None):
		for line in lines:
			x1,y1,x2,y2 = line[0]
			if(xDistance(x1, x2) < getWIDTH()//3):  ##only vertical lines accepted
				line_length = yDistance(y1, y2)
				points.append((x1,y1,line_length))

				i = line_length // 50
				line_lengths[i] += 1

	#Average bar height
	bar_h = avgLineLength(line_lengths)
	setHEIGHT(bar_h)

	#eliminating too short lines and lines too close each other
	points.sort(key=y_)
	eliminateShortLines(points)
	eliminateRedundantLines(points)
	setPOINTS(len(points))

	#calculate number of rows and bars
	rows = makeInitialRows(points)
	widths = calculateWidths(rows)

	#calculate the probability of point row to be a bar row in the score paper
	stats = calculateStats(rows, widths)

	#delete rows with low stats and too close to another row
	deleteRedundantRows(rows, stats)

	#drawing not required
	drawToImage(points, rows, img, path, fileName)

	print(f'Image size: {str(img_h)} x {str(img_w)}')
	print(f'Total points: {str(getPOINTS())}')
	print(f'Bar height: {str(getHEIGHT())}')
	print(f'Bar width: {str(getWIDTH())}')
	print()
	print(f'Rows: {len(rows)}')
	for i in range(len(rows)):
		print(f'Row {str(i + 1)}: {str(len(rows[i]) - 1)} bars')

	time = stopTimer(start)
	print(f'Execution time: {str(time)}')
