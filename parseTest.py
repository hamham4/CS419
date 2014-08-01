data1 = "Siple, C. MWF 0700-0800 6/26/14-9/6/14"
data2 = "Tobias, D. TR 1300-1400 6/26/14-9/6/14"
datas = [ data1, data2]
catalog = []

for i in range(len(datas)):
	catalog.append(datas[i])
	

for k in range(len(catalog)):
	cnt = 0
	last = ""
	first = ""
	days = ""
	stime = ""
	etime = ""
	sdate = ""
	edate = ""
	usr = ""
	data = []
	data = catalog[k]

	for i in range(len(data)):
		mon = False
		tues = False
		wed = False
		thur = False
		fri = False
	
		if data[i] == " " or data[i] == "-" or data[i] == "." or data[i] == ",":
			cnt += 1
			continue
		if cnt == 0:
			last += data[i]
		if cnt == 2:
			first += data[i]
		if cnt == 4:
			days += data[i]
		if cnt == 5:
			stime += data[i]
		if cnt == 6:
			etime += data[i]
		if cnt == 7:
			sdate += data[i]
		if cnt == 8:
			edate += data[i]
		if cnt == 9:
			usr = ""
			for j in range(len(last)):
				if j == 7:
					break
				usr += last[j].lower()  
			usr += first.lower()
				
			for n in range(len(days)):
				if days[n] == "M":
					mon = True
				if days[n] == "T":
					tues = True
				if days[n] == "W":
					wed = True
				if days[n] == "R":
					thur = True
				if days[n] == "F":
					fri = True
				
			print (usr, last, first, days, stime, etime, sdate, edate)
			days = ""
			stime = ""
			etime = ""
			sdate = ""
			edate = ""
			days += data[i]
			cnt = 4
			continue
		
	usr = ""			
                
	for j in range(len(last)):
		if j == 7:
			break
		usr += last[j].lower()
    
	usr += first.lower()
            
	for n in range(len(days)):
		if days[n] == "M":
			mon = True
		if days[n] == "T":
			tues = True
		if days[n] == "W":
			wed = True
		if days[n] == "R":
			thur = True
		if days[n] == "F":
			fri = True
		
	print (usr, last, first, days, stime, etime, sdate, edate)