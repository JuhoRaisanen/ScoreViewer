import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def xDistance(p1, p2):
	return abs(p1[0] - p2[0])
	
def yDistance(p1, p2):
	return abs(p1[1] - p2[1])
	
def yValue(p):
	#m = (p[1] // 50) * 50
	#return (m * 1000) + p[0]
	return p[1]
	
def intAverage(p1, p2):
	return ((p1 + p2) // 2)
	
def probability(height_diff, y_diff, r, bar_h):
	h_value = min(height_diff / bar_h, 1)
	y_value = min(y_diff / bar_h, 1)
	r_value = min(r / 5, 1)	
	return (1- h_value) * r_value

def analyzeJpg(fileName):
	e1 = cv.getTickCount()
	img = cv.imread(fileName + '.jpg')
	img_h, img_w, img_channel = img.shape
	
	#parameters     #parameters 8.1. :bar_h img_h//25, precision 10
	bar_h = img_h//20
	bar_w = img_w//15
	line_precision = 15

	print()
	print()
	print('Analyzing the file ' + str(fileName) + ' ......')
	print('Image size: ' + str(img_h) + ' x ' + str(img_w))
	print('Channels: ' + str(img_channel))

	#line detection
	line_count = 0
	lines_start = []
	points = []
	line_lengths = [0]*(img_h // 50) ##length starting from 0, increasing 50 by 1 index
	gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
	#edges = cv.Canny(gray,50,150,apertureSize = 3)  ---Canny is good for native jpgs
	ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY_INV)
	
	lines = cv.HoughLinesP(thresh,1,1,100,minLineLength=bar_h,maxLineGap=line_precision) 	
	mask = np.zeros((img_h,img_w,img_channel), np.uint8)
	if(lines is not None):
		for line in lines:
			x1,y1,x2,y2 = line[0]
			if(abs(x1 - x2) < bar_w//3):  ##only vertical lines accepted
				line_count += 1
				line_length = abs(y1 - y2)
				lines_start.append((x1,y1,line_length))
				
				i = line_length // 50
				line_lengths[i] += 1
				
				cv.line(mask,(x1,y1),(x2,y2),(255,255,255),2)

	#Average bar height
	i = (img_h // 50) - 1
	while i >= 0:
		if(line_lengths[i] > line_count * 0.20):
			bar_h = i*50 + 50
			break
		else:
			i -= 1

	#eliminating lines too close each other
	while (len(lines_start) > 0):
		point1 = lines_start[0]
		lines_start.pop(0)
		if(point1[2] > (bar_h * 0.6)):
			points.append(point1)
			i = 0
			while i < len(lines_start):
				line = lines_start[i]
				if(xDistance(line, point1) < bar_w/2 and yDistance(line, point1) < line[2]/2):
					lines_start.pop(i)
				else:
					i += 1
	
	print('Lines: ' + str(len(points)))
	
	print('Bar height: ' + str(bar_h))

	#calculate number of rows and bars
	points.sort(key=yValue)
	row_start = 0
	row_points = []
	i = 0
	for p in points:		
		if(abs(p[1] - row_start) < bar_h//6): #y difference
			i += 1
			cv.circle(mask,p[:2], 20, (255,0,0), -1) #writing not required
		else:
			if(i > 0):
				row_points.append(i)
			row_start = p[1]
			cv.circle(mask,p[:2], 20, (0,255,0), -1) #writing not required
			i = 1
			
	row_points.append(i)
	
	i = 0
	score_rows = []
	p_threshold = 0.70
	print('Rows: ' + str(len(row_points)))
	for r in range(len(row_points)):
		b = row_points[r]
		height_sum = 0
		y_mean = points[intAverage(i, i+b-1)][1]
		if r < len(row_points) - 1:
			y_next = points[intAverage(i+b, i+b+row_points[r+1]-1)][1]
		else:
			y_next = img_h + bar_h
		
		y_diff = y_next - y_mean
		for i in range(i, i+b):
			height_sum += points[i][2]
		
		height_avg = height_sum / b
		height_diff = abs(bar_h - height_avg)
		
		p_value = probability(height_diff, y_diff, b, bar_h)
		if p_value > p_threshold:
			score_rows.append(b-1)
			
		print('Column points: ' + str(b) + ', y_diff: ' + str(y_diff) + ', height_avg: ' + str(height_avg) + ', p: ' + str(p_value))
		i += 1
		
	
	cv.imwrite(fileName + '-mask' + '.png',mask) #writing not required
	
	print()
	print('Rows: ' + str(len(score_rows)))
	for i in range(len(score_rows)):
		print('Column ' + str(i+1) + ': ' + str(score_rows[i]))
	

	
	#timer
	e2 = cv.getTickCount()
	time = (e2 - e1)/ cv.getTickFrequency()
	print('Execution time: ' + str(time))
	
	return score_rows



