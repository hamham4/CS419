from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import csv
import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
import datetime
 
 
class MainHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
 
        html_string = """
         <form action="%s" method="POST" enctype="multipart/form-data">
        Upload File:
        <input type="file" name="file"> <br>
        <input type="submit" name="submit" value="Submit">
        </form>""" % upload_url
 
        self.response.write(html_string)
        

class getHandler(webapp2.RequestHandler):
    def get(self):
        req_html = """ <html><body>
        <form method="GET" >
        Get Busy Times: <br>
        <input name="username" class="required">
        <input name="date" type="date" class="required">
        <input type="submit" name="submit" value="Submit">
        </form>"""
        
        self.response.write(req_html)
        
        if self.request.get('username') != '':
            usr = self.request.get('username') + ' '
            flag = 0
            d = datetime.datetime.strptime( self.request.get('date'), '%Y-%m-%d').strftime('%a')
            day = format_date( self.request.get( 'date' ) )
            r = check_date( day, usr )
            if r == 1:
                flag = 1
            
            q = EntriesDB.all()
            q.filter( 'user =', usr )
            if flag == 0:
                if d == 'Sun':
                    d == 'U'
                elif d == 'Thu':
                    d == 'R'
                else:
                    d = d[0]
                d += ' ='
                q.filter( d, ' True ' )
            else:
                q.filter( 'sDate =', day )
            
            self.response.write( '<table id="db_table">' )
            for e in q.run():
                    line = e.sTime + ' ' + e.eTime
                    self.response.write( '<tr>' )
                    self.response.write( '<td>' + line + '</td>' )
                    self.response.write( '</tr>' )
        self.response.write( '</table></body></html>' )

def format_date( date ):
    y = date[2]+date[3]
    if date[5] == '0':
        m = date[6]
    else:
        m = date[5]+date[6]
    if date[8] == '0':
        d = date[9]
    else:
        d = date[8]+date[9]
    day = ' ' + m + '/' + d + '/' + y + ' '
    return day

def check_date( day, usr ):

    c = EntriesDB.all()
    c.filter( 'user =', usr )
    c.filter( 'sDate =', day )
    for e in c.run():
        if e.eDate == ' N/A':
            return 1
    
    return 0


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        process_csv(blob_info)
 
        blobstore.delete(blob_info.key())  # optional: delete file after import
        self.redirect("/")
 
 
def process_csv(blob_info):
    blob_reader = blobstore.BlobReader(blob_info.key())
    reader = csv.reader(blob_reader, delimiter=',')
    for row in reader:
        user, lname, fi, S, U, M, T, W, R, F, sTime, eTime, sDate, eDate = row
        entry = EntriesDB(user=user, lname=lname, fi=fi, S=S, U=U, M=M, T=T, W=W, R=R, F=F, sTime=sTime, eTime=eTime, sDate=sDate, eDate=eDate)
        entry.put()
 
class testOut(webapp2.RequestHandler):
    def get(self):
        one = '0600 0700'
        two = '1200 1300'
        self.response.write( "<html><body><table id='db'><tr><td>"+one+"</td></tr><tr><td>"+two+"</td></tr></table></body></html>")
        
class EntriesDB(db.Model):
    user = db.StringProperty()
    lname = db.StringProperty()
    fi = db.StringProperty()
    S = db.StringProperty()
    U = db.StringProperty()
    M = db.StringProperty()
    T = db.StringProperty()
    W = db.StringProperty()
    R = db.StringProperty()
    F = db.StringProperty()
    sTime = db.StringProperty()
    eTime = db.StringProperty()
    sDate = db.StringProperty()
    eDate = db.StringProperty()
 
application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', UploadHandler),
    ( '/get', getHandler ),
    ( '/test', testOut )
], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
