import sys
sys.path.insert(0, 'src')
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
from bs4 import BeautifulSoup
from urllib2 import urlopen
from google.appengine.api import urlfetch
import lxml

BASE_URL = "http://catalog.oregonstate.edu/"
ADD_URL = "&columns=jk"
urlfetch.set_default_fetch_deadline(30)

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


class catdb(ndb.Model):
    user = ndb.StringProperty(required=True)
    lname = ndb.StringProperty(required=True)
    fi = ndb.StringProperty(required=True)
    M = ndb.BooleanProperty(required=True, default=False)
    T = ndb.BooleanProperty(required=True, default=False)
    W = ndb.BooleanProperty(required=True, default=False)
    R = ndb.BooleanProperty(required=True, default=False)
    F = ndb.BooleanProperty(required=True, default=False)
    st = ndb.StringProperty(required=True)
    et = ndb.StringProperty(required=True)
    sd = ndb.StringProperty(required=True)
    ed = ndb.StringProperty(required=True)

class MainPage(webapp.RequestHandler):
    
    def get(self):
        

        
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
                if cnt ==9:
                    usr = ""
                    for j in range(len(last)):
                        if j==7:
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
                    
                    
                    cat1 = catdb(user=usr, lname=last, fi=first, M=mon, T=tues, W=wed, R=thur, F=fri, st=stime, et=etime, sd=sdate, ed=edate)
                    cat1.put()
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
                                        
            cat2 = catdb(user=usr, lname=last, fi=first, M=mon, T=tues, W=wed, R=thur, F=fri, st=stime, et=etime, sd=sdate, ed=edate)
            cat2.put()
        
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('I have parsed and uploaded the Course Catalog data for you Team Four.')


application = webapp.WSGIApplication([('/', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
