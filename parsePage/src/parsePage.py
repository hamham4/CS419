from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb

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
        data = "Siple, C. MWF 0700-0800 6/26/14-9/6/14"
        cnt = 0
        last = ""
        first = ""
        days = ""
        stime = ""
        etime = ""
        sdate = ""
        edate = ""
        usr = ""

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
                                    
        cat = catdb(user=usr, lname=last, fi=first, M=mon, T=tues, W=wed, R=thur, F=fri, st=stime, et=etime, sd=sdate, ed=edate)
        cat.put()
        
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('I have parsed and uploaded the Course Catalog data for you Team Four.')


application = webapp.WSGIApplication([('/', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
