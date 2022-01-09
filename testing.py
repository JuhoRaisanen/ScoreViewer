
def printTestResults(results):
	print()
	print('Test overview: ')
	f = open("correctTestResults.txt", "r")
	
	s = f.readline()
	print(s)
	s = f.readline()
	test_page = 0
	i = 0
	page_results = results[test_page]
	r_sum = 0
	bar_sum = 0
	while True:
		if s[0] != '/':
			bar_sum += int(s)
			if i < len(page_results):
				r_sum += page_results[i]
			i += 1
		else:
			print('Correspondence: ' + str(r_sum/bar_sum))
			test_page += 1
			if test_page < len(results):
				page_results = results[test_page]
			else:
				break
			i = 0
			r_sum = 0
			bar_sum = 0
			print(s)
			
		s = f.readline()
		if s == '': #end of file
			break
		

	f.close()