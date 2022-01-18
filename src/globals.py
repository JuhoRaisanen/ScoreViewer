POINTS = 0
BAR_HEIGHT = 200
BAR_WIDTH = 200

def setHEIGHT(h):
	global BAR_HEIGHT
	BAR_HEIGHT = h
	
def setWIDTH(w):
	global BAR_WIDTH
	BAR_WIDTH = w
	
def setPOINTS(p):
	global POINTS
	POINTS = p
	
def getPOINTS(): return POINTS

def getHEIGHT(): return BAR_HEIGHT

def getWIDTH(): return BAR_WIDTH