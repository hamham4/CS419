# from /usr/lib/python2.6/site-packages import argparse


import imp
import httplib2
import os
import sys
import json
#sys.path.remove('/usr/lib/python2.6/site-packages')
#foo = imp.load_source('argparse.py', '/usr/lib/python2.6/site-packages/')
import argparse
from datetime import datetime
from collections import namedtuple
#import tzlocal
#import pytz

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")

#CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

#FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  #scope=[
      #'https://www.googleapis.com/auth/calendar',
      #'https://www.googleapis.com/auth/calendar.readonly',
    #],
    #message=tools.message_if_missing(CLIENT_SECRETS))

#def googleSearch(userId, startYear, endYear, startMonth, endMonth, startday, endDay, startTime, endTime):
def googleSearch(userId, startTimeParam, startDate, endTime, endDate):
  #used from the google reference code
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    ##print credentials
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Calendar API.
  service = discovery.build('calendar', 'v3', http=http)

  try:

    tz = "-0000"
    page_token = None

    myStartTime = startDate + "T" + startTimeParam + ":01" + tz
    #end time  string put together  add :00 for the seconds or else it fails
    myEndTime = endDate + "T" + endTime + ":00" + tz

    while True:
		#get the calendar id is always the onid plus this email or else it wont work
      calendarID = userId + "@gmail.com"
      #calendarID = "cs419.team4@gmail.com"

      startTime = "startTime"

	  #we run into an issue if the calendar id doesnt exist
      try:
		#when we get the events
		#order by the start time, have it all as single events, min and max time are our parameters we put in
		#also we are having it return in the time zone of the local machine, not useful for full day events but very helpful for datetime events
        events = service.events().list(calendarId=calendarID, pageToken=page_token, orderBy=startTime, singleEvents=True, timeMin=myStartTime, timeMax=myEndTime).execute()
      except:
	    #when we get an error from the events return, normally meaning a bad onid id
        events = "NoID"

      def ld_writeDicts(filePath,events):
        f=open(filePath, 'w')
        newData = json.dumps(events,indent=4)
        f.write(newData)
        f.close()

      ld_writeDicts('results.json', events)

      busyTimes = list()

      with open("results.json") as json_file:
        json_data = json.load(json_file)

        i = -1
        for items in json_data['items']:
            n = i
            i +=1
            for key, value in items.iteritems():
                start = json_data['items'][n]['start']
                start1 = str(start)
                if len(start1) == 43:
                    st1 = start1[16:32]
                    year = st1[0:4]
                    month = st1[5:7]
                    day = st1[8:10]
                    sHour = st1[11:13]
                    sMin =  st1[14:16]
                    startTime = sHour + sMin
                if len(start1) == 24:
                    st1 = start1[12:22]
                    year = st1[0:4]
                    month = st1[5:7]
                    day = st1[8:10]
                    #sHour = st1[12:13]
                    #sMin =  st1[14:15]
                    startTime = "0000"
                end = json_data['items'][n]['end']
                end1 = str(end)
                if len(end1) == 43:
                    en1 = end1[16:32]
                    eYear = en1[0:4]
                    eMonth = en1[5:7]
                    eDay = en1[8:10]
                    eHour = en1[11:13]
                    eMin =  en1[14:16]
                    endTime = eHour + eMin
                if len(end1) == 24:
                    en1 = end1[12:28]
                    eYear = en1[0:4]
                    eMonth = en1[5:7]
                    eDay = en1[8:10]
                    #eHour = en1[11:13]
                    #eMin =  en1[14:16]
                    endTime = "0000"

            print year, month, day, startTime, eYear, eYear, eMonth, eDay, endTime

            busyBlock = BusyBlock(year, month, day, startTime, endTime)
            busyTimes.append(busyBlock)
        return busyTimes

      if not page_token:
        break

  except client.AccessTokenRefreshError:
    pass
    #print ("The credentials have been revoked or expired, please re-run the application to re-authorize")

  return events


if __name__ == '__main__':
  userId = "rezalution786"

  startYear = "2014"
  startMonth = "08"
  startDay =  "30"
  startDate = startYear + "-" + startMonth + "-" + startDay
  startDate = str(startDate)

  startHour = "00"
  startMin =  "00"
  startTimeParam = startHour + ":" + startMin
  startTimeParam = str(startTimeParam)

  endHour = "00"
  endMin = "00"
  endTime = endHour + ":" + endMin
  endTime = str(endTime)

  endYear = "2014"
  endMonth = "09"
  endDay =  "02"
  endDate = endYear + "-" + endMonth + "-" + endDay
  endDate = str(endDate)

  googleSearch(userId, startTimeParam, startDate, endTime, endDate)
