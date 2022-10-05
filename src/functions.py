import cv2 as cv
import math
import os
from globals import *

def startTimer():
	return cv.getTickCount()
	
def stopTimer(start):
	end = cv.getTickCount()
	return (end - start)/ cv.getTickFrequency()

def xDistance(p1, p2):
	return abs(p1 - p2)
	
def yDistance(p1, p2):
	return abs(p1 - p2)
    
def pointDistance(p1, p2):
    x = xDistance(p1[0], p2[0])
    y = yDistance(p1[1], p2[1])   
    return math.sqrt(x*x + y*y)
	
def y_(p):
	return p[1]
	
def x_(p):
	return p[0]
	
def length(p):
	return p[2]
	
def intAverage(p1, p2):
	return ((p1 + p2) // 2)
	
def max(list):
	max = 1
	for l in list:
		if l > max:
			max = l			
	return max
	
	
def probability(height_ratio, width_ratio, point_ratio):

	height_ratio = min(height_ratio, 1)
	width_ratio = min(width_ratio, 1)
	point_ratio = min(point_ratio, 1)	
	return (1- height_ratio) * width_ratio * point_ratio
	
	
	
def imageAnalysis(img, line_precision):
	
	gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
	ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY_INV)

	return cv.HoughLinesP(
		thresh, 1, 1, 100, minLineLength=getHEIGHT(), maxLineGap=line_precision
	)
	

def avgLineLength(line_lengths):	
	line_count = len(line_lengths)
	i = line_count - 1
	while i >= 0:
		if(line_lengths[i] > line_count * 0.20):
			return i*50 + 25
		else:
			i -= 1			
	return 100 #default
	
	
def eliminateShortLines(points):
	i = 0
	while i < len(points):
		p = points[i]
		if(length(p) < (getHEIGHT() * 0.50)):
			points.pop(i)
			continue
		i += 1

def eliminateRedundantLines(points):
	i = 0
	while i < len(points):
		p = points[i]

		j = 0
		while j < len(points):
			if(j == i):
				j += 1
				continue

			line = points[j]
			if(pointDistance(line, p) < getWIDTH()/2 and length(line) <= length(p)):
				points.pop(j)
				if(j < i): i -= 1

			else: j += 1               				  
		i += 1
		
		
		
def makeInitialRows(points):
	row_points = 0
	rows = []
	for i in range(len(points)):
		p = points[i]

		if(yDistance(y_(p), y_(points[i - row_points])) < getHEIGHT()/6): #y difference
			row_points += 1
		else:
			if(i > 0):
				rows.append(points[i - row_points : i])
			row_points = 1

	if rows:
		i = len(points)
		rows.append(points[i - row_points : i])
	return rows
	
def calculateWidths(rows):
	widths = []
	for r in rows:
		r.sort(key=x_)
		min_x = x_(r[0])
		max_x = x_(r[len(r) - 1])
		
		widths.append(max_x - min_x)
	return widths
	
def calculateStats(rows, widths):
	max_w = max(widths)
	stats = []
	for i in range(len(rows)):
		r = len(rows[i])
		height_sum = sum(length(p) for p in rows[i])

		height_avg = height_sum / r
		height_diff = abs(getHEIGHT() - height_avg) / getHEIGHT()
		width_ratio = widths[i] / (max_w * 0.80)
		points_ratio = r / (getPOINTS() / 7)

		stats.append(probability(height_diff, width_ratio, points_ratio))

			#print('Row points: %2d, height_avg: %5.2f, width: %3d, p: %5.2f' % (r, height_avg, widths[i], stats[i]))
	return stats
		
def deleteRedundantRows(rows, stats):
	d_treshold = 0.10
	i = 0
	prev_y = -1000
	while i < len(rows):
		if stats[i] < d_treshold:
			rows.pop(i)
			stats.pop(i)
			continue

		this_y = y_(rows[i][0])
		if yDistance(this_y, prev_y) < getHEIGHT():		
			if stats[i] > stats[i-1]:
				rows.pop(i-1)
				stats.pop(i-1)
				prev_y = this_y
			else:
				rows.pop(i)
				stats.pop(i)
			continue

		i += 1
		prev_y = this_y
		

def drawToImage(points, rows, img, path, fileName):
	#All points and lines with red
	for p in points:
		cv.circle(img,p[:2], 20, (0, 0, 255), -1)
		cv.line(img, (x_(p),y_(p)), (x_(p),y_(p)-length(p)), (0,0,255), 4) 

	#Row points with green
	for r in rows:
		for p in r:
			cv.circle(img,p[:2], 20, (0, 255, 0), -1)

	#Write to image
	cv.imwrite(os.path.join(path, f'{fileName}-mask.png'), img)
	