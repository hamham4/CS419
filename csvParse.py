
from bs4 import BeautifulSoup
from urllib.request import urlopen


BASE_URL = "http://catalog.oregonstate.edu/"
ADD_URL = "&columns=jk"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html,"lxml")

def get_dept_links(section_url):
    soup = make_soup(section_url)
    dlSubjects = soup.find(id = "ctl00_ContentPlaceHolder1_dlSubjects")
    dept_links = [BASE_URL + a["href"] for a in dlSubjects.findAll("a")]
    return dept_links

def get_data(links):
    catalog = []
    for url in range(len(links)):
        soup2 = make_soup(links[url]+ADD_URL)
        table = soup2.find(id = "ctl00_ContentPlaceHolder1_dlCourses")
        for div in table.findAll('div'):
            data = div.findAll('td')
            name = data[0]
            sched = data[1]
            for br in sched.findAll('br'):
                br.replace_with(" ")
            #strips out Staff and TBA entries from catalog 
            if name.get_text() == "Staff" or sched.get_text().strip() == "TBA":
                continue
            entry = name.get_text().strip()+" "+sched.get_text().strip()
            catalog.append(entry)
    return catalog

        
links = get_dept_links("http://catalog.oregonstate.edu/SOC.aspx?level=all&campus=corvallis&term=201500")
catData = get_data(links)

for k in range(len(catData)):
        cnt = 0
        last = ""
        first = ""
        days = ""
        stime = ""
        etime = ""
        sdate = ""
        edate = ""
        usr = ""
        data = catData[k]
        for i in range(len(data)):
            mon = "False"
            tues = "False"
            wed = "False"
            thur = "False"
            fri = "False"
            sat = "False"
            sun = "False"
            
            if data[i] == " " or data[i] == "-" or data[i] == "." or data[i] == ",":
                if data[i] == " " and first == "" and data[i-1] != ",":
                    last = last+" "
                    cnt = cnt - 1
                if data[i] == "-" and first == "":
                    last = last+"-"
                    cnt = cnt - 1
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
                if data[i].isdigit() == False and data[i] != '/':
                    usr = ""
                    n = 0
                    for j in range(len(last)):
                        if n==7:
                            break
                        if last[j] == "-" or last[j] == " ":
                            continue
                        usr += last[j].lower()
                        n += 1
                    usr += first.lower()
                
                    for n in range(len(days)):
                        if days[n] == "M":
                            mon = "True"
                        if days[n] == "T":
                            tues = "True"
                        if days[n] == "W":
                            wed = "True"
                        if days[n] == "R":
                            thur = "True"
                        if days[n] == "F":
                            fri = "True"
                        if days[n] == "S":
                            sat = "True"
                        if days[n] == "U":
                            sun = "True"
                
                    print(usr,",", last,",", first,",", sat,",", sun,",", mon,",", tues,",", wed,",", thur,",", fri,",", stime,",", etime,",", sdate,",", "N/A")
                
                    days = ""
                    stime = ""
                    etime = ""
                    sdate = ""
                    edate = ""
                    days += data[i]
                    cnt = 4
                    continue
                edate += data[i]
            if cnt ==9:
                usr = ""
                n = 0
                for j in range(len(last)):
                    if n==7:
                        break
                    if last[j] == "-" or last[j] == " ":
                        continue
                    usr += last[j].lower()
                    n += 1
                usr += first.lower()
                
                for n in range(len(days)):
                    if days[n] == "M":
                        mon = "True"
                    if days[n] == "T":
                        tues = "True"
                    if days[n] == "W":
                        wed = "True"
                    if days[n] == "R":
                        thur = "True"
                    if days[n] == "F":
                        fri = "True"
                    if days[n] == "S":
                        sat = "True"
                    if days[n] == "U":
                        sun = "True"
                
                print(usr,",", last,",", first,",", sat,",", sun,",", mon,",", tues,",", wed,",", thur,",", fri,",", stime,",", etime,",", sdate,",", edate)
                
                days = ""
                stime = ""
                etime = ""
                sdate = ""
                edate = ""
                days += data[i]
                cnt = 4
                continue
    
        usr = ""
        n = 0        
        for j in range(len(last)):
            if n == 7:
                break
            if last[j] == "-" or last[j] == " ":
                continue
            usr += last[j].lower()
            n += 1
        usr += first.lower()
            
        for n in range(len(days)):
            if days[n] == "M":
                mon = "True"
            if days[n] == "T":
                tues = "True"
            if days[n] == "W":
                wed = "True"
            if days[n] == "R":
                thur = "True"
            if days[n] == "F":
                fri = "True"
            if days[n] == "S":
                sat = "True"
            if days[n] == "U":
                sun = "True"
		
        if edate == "" and cnt == 7:
            edate = "N/A"
        print(usr,",", last,",", first,",", sat,",", sun,",", mon,",", tues,",", wed,",", thur,",", fri,",", stime,",", etime,",", sdate,",", edate)
