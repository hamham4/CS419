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
#from apiclient import discovery
from apiclient.discovery import build
#from oauth2client import file
#from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client import client
from google.appengine.api import urlfetch


BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")



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


def googleSearch(userId, startTimeParam, startDate, endTime, endDate):

  service = build(serviceName='calendar', version='v3',
       developerKey='AIzaSyCInh7DEEH7Zv2H-htNy7o9Z_7ktqkWY1Q')
	   
  calendar_client = gdata.calendar.client.CalendarClient()


  try:
	  page_token = None
	  
	  myStartTime = startDate + "T" + startTimeParam + ":01"
	  #end time  string put together  add :00 for the seconds or else it fails
	  myEndTime = endDate + "T" + endTime + ":00"
	  
	  while True:
	  
		  calendarID = userId + "@gmail.com"
		  
		  urlBegin = 'https://www.google.com/calendar/feeds/'
		  urlEnd = '/public/full?orderby=starttime&singleevents=true&start-min='
		  urlComplete = urlBegin + calendarID + urlEnd + myStartTime + '&start-max=' + myEndTime
		  
		  feed = calendar_client.GetCalendarEventFeed(uri=urlComplete)
		  
		  busyTimes = list()
		  for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
			  #print '\t%s. %s' % (i, an_event.title.text,)
			  for a_when in an_event.when:
				#print '\t\tStart time: %s' % (a_when.start,)
				#print '\t\tEnd time:   %s' % (a_when.end,)
				
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
				busyBlock = BusyBlock(year, month, day, startTime, endTimes)
				busyTimes.append(busyBlock)
		      
		  return busyTimes
		  
		  if not page_token:
                   break
    
  except client.AccessTokenRefreshError:
    pass

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


      if not page_token:
        break

  except client.AccessTokenRefreshError:
    pass

  

