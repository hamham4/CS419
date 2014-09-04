# from /usr/lib/python2.6/site-packages import argparse

import webapp2
import imp
import httplib2
import os
import sys
import json
import argparse
from datetime import datetime
from collections import namedtuple
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree


BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")

# CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
#   scope=[
#       'https://www.googleapis.com/auth/calendar',
#       'https://www.googleapis.com/auth/calendar.readonly',
#     ],
#     message=tools.message_if_missing(CLIENT_SECRETS))

# FLAGS = gflags.FLAGS
FLOW = OAuth2WebServerFlow(
    client_id='350349023880-2f831jg4i6m8ee5h9f7jp742cmqm8efc.apps.googleusercontent.com',
    client_secret='ZpguubUd9SEH9pkVvl-QPi8G',
     scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    user_agent='team-four/1')


def getCalendarEvents(userID, startYear, startMonth, startDay, endYear, endMonth, endDay):
  #Default to getting the whole day's busy events
  startHour = "00"
  startMin = "00"
  endHour = "23"
  endMin = "59"

  startDate = str(startYear) + "-" + str(startMonth) + "-" + str(startDay)
  startDate = str(startDate)

  startTimeParam = str(startHour) + ":" + str(startMin)
  startTimeParam = str(startTimeParam)

  endTime = str(endHour) + ":" + str(endMin)
  endTime = str(endTime)

  endDate = str(endYear) + "-" + str(endMonth) + "-" + str(endDay)
  endDate = str(endDate)

  return googleSearch(userID, startTimeParam, startDate, endTime, endDate)

#def googleSearch(userId, startYear, endYear, startMonth, endMonth, startday, endDay, startTime, endTime):
def googleSearch(userId, startTimeParam, startDate, endTime, endDate):
  #used from the google reference code
  # storage = Storage('calendar.dat')
  # credentials = storage.get()
  # if credentials is None or credentials.invalid:
    # pass
    ##print credentials
    #credentials = run(FLOW, storage)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it with our good Credentials.
  #http = httplib2.Http()
  #http = credentials.authorize(http)

  # Construct the service object for the interacting with the Calendar API.

  service = build(serviceName='calendar', version='v3',
       developerKey='AIzaSyCInh7DEEH7Zv2H-htNy7o9Z_7ktqkWY1Q')
	   
  calendar_client = gdata.calendar.client.CalendarClient()

  page_token = None
  
  myStartTime = startDate + "T" + startTimeParam + ":01"
  #end time  string put together  add :00 for the seconds or else it fails
  myEndTime = endDate + "T" + endTime + ":00"
  
  calendarID = userId + "@gmail.com"
  
  urlBegin = 'https://www.google.com/calendar/feeds/'
  urlEnd = '/public/full?orderby=starttime&singleevents=true&start-min='
  urlComplete = urlBegin + calendarID + urlEnd + myStartTime + '&start-max=' + myEndTime
  
  feed = calendar_client.GetCalendarEventFeed(uri=urlComplete)
  for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
      #print '\t%s. %s' % (i, an_event.title.text,)
      for a_when in an_event.when:
        #print '\t\tStart time: %s' % (a_when.start,)
        #print '\t\tEnd time:   %s' % (a_when.end,)
		
        busyTimes = list()
		
        start = a_when.start
        #start1 = str(start)
        #print len(start)
        if len(start) == 29:
			st1 = start[0:29]
			year = st1[0:4]
			print year
			month = st1[5:7]
			print month
			day = st1[8:10]
			print day
			sHour = st1[11:13]
			sMin =  st1[14:16]
			startTime = sHour + sMin
			print startTime
        if len(start) == 10:
			st1 = start[0:10]
			year = st1[0:4]
			print year
			month = st1[5:7]
			print month
			day = st1[8:10]
			print day
			sHour = st1[12:13]
			sMin =  st1[14:15]
			startTime = "0000"
		
        end = a_when.end
        #end1 = str(end)
        if len(end) == 29:
			en1 = end[0:29]
			eYear = en1[0:4]
			print eYear
			eMonth = en1[5:7]
			print eMonth
			eDay = en1[8:10]
			print eDay
			eHour = en1[11:13]
			eMin =  en1[14:16]
			endTimes = eHour + eMin
			print endTimes
        if len(end) == 10:
			en1 = end[12:28]
			eYear = en1[0:4]
			eMonth = en1[5:7]
			eDay = en1[8:10]
			#eHour = en1[11:13]
			#eMin =  en1[14:16]
			endTimes = "0000"

        #print year, month, day, startTime, endTimes
        busyBlock = BusyBlock(year, month, day, startTime, endTime)
        busyTimes.append(busyBlock)
  #return busyTimes
  

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
      #try:
		#when we get the events
		#order by the start time, have it all as single events, min and max time are our parameters we put in
		#also we are having it return in the time zone of the local machine, not useful for full day events but very helpful for datetime events
      events = service.events().list(calendarId=calendarID, pageToken=page_token, orderBy=startTime, singleEvents=True, timeMin=myStartTime, timeMax=myEndTime).execute()
      #print events
      #except:
	    #when we get an error from the events return, normally meaning a bad onid id
        #events = "NoID"
		
      #def ld_writeDicts(events):
        #f=open(filePath, 'w')
      # newData = json.dumps(events)

      # #ld_writeDicts(events)

      # #busyTimes = list()

	  # #json_data = json.loads(newData)
      # #with json.loads(newData) as json_file:
      # json_data = json.loads(newData)

      # i = -1
      # for items in json_data['items']:
            # n = i
            # i +=1
            # for key, value in items.iteritems():
                # start = json_data['items'][n]['start']
                # start1 = str(start)
                # if len(start1) == 43:
                    # st1 = start1[16:32]
                    # year = st1[0:4]
                    # month = st1[5:7]
                    # day = st1[8:10]
                    # sHour = st1[11:13]
                    # sMin =  st1[14:16]
                    # startTime = sHour + sMin
                # if len(start1) == 24:
                    # st1 = start1[12:22]
                    # year = st1[0:4]
                    # month = st1[5:7]
                    # day = st1[8:10]
                    # #sHour = st1[12:13]
                    # #sMin =  st1[14:15]
                    # startTime = "0000"
                # end = json_data['items'][n]['end']
                # end1 = str(end)
                # if len(end1) == 43:
                    # en1 = end1[16:32]
                    # eYear = en1[0:4]
                    # eMonth = en1[5:7]
                    # eDay = en1[8:10]
                    # eHour = en1[11:13]
                    # eMin =  en1[14:16]
                    # endTime = eHour + eMin
                # if len(end1) == 24:
                    # en1 = end1[12:28]
                    # eYear = en1[0:4]
                    # eMonth = en1[5:7]
                    # eDay = en1[8:10]
                    # #eHour = en1[11:13]
                    # #eMin =  en1[14:16]
                    # endTime = "0000"

            #print year, month, day, startTime, eYear, eYear, eMonth, eDay, endTime

            #busyBlock = BusyBlock(year, month, day, startTime, endTime)
            #busyTimes.append(busyBlock)
        #return busyTimes

      if not page_token:
        break

  except client.AccessTokenRefreshError:
    pass
    #print ("The credentials have been revoked or expired, please re-run the application to re-authorize")

  #return events
  


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
