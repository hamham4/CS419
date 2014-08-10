from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import csv
import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
 
 
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
    ('/upload', UploadHandler)
], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
