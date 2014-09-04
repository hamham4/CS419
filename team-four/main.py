#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from collections import namedtuple
import jsonManipulator 
import busy_times_db
import busyToFreeTimeConverter
import logging
import jinja2
import os
import scheduler
#import SearchGoogle

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)


BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")
FreeBlock = namedtuple("FreeBlock", "year, month, day, startTime, endTime")

class MainHandler(webapp2.RequestHandler):
    def get(self):

		template = JINJA_ENVIRONMENT.get_template('submitForm.html')
		self.response.write(template.render())

class SubmissionHandler(webapp2.RequestHandler):
	def post(self):
		#Get request in json format from Post
		jsonParameters = self.request.get('request', self)
		logging.info("=== request ====")
		logging.info(jsonParameters)
		#Parse out parameters from json
		requestType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees = jsonManipulator.getParsedParameters(jsonParameters)
 
		allFreeTimes = SubmissionHandler.getAllFreeTimes(attendees, startYear, endYear, startMonth, endMonth, startDay, endDay)
		logging.info("=== all free times====")
		logging.info(allFreeTimes)
		#self.response.write(allFreeTimes)
		recommendations = SubmissionHandler.getRecommendations(allFreeTimes, requestType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees)
		
		
		self.response.write(recommendations)
		logging.info("===recommendations====")
		logging.info(recommendations)
	@staticmethod
	def getRecommendations(allFreeTimes, requestType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees):
		if requestType == "findAttendees":
			freeAttendees = scheduler.getAttendees(allFreeTimes, startDay, startMonth, startYear, startTime, endTime)

			jsonAttendees = jsonManipulator.getAttendeesResponse(freeAttendees)
			return jsonAttendees

		elif requestType == "findTime":
			freeTimes = scheduler.getCommonFreeTimes(allFreeTimes, startTime, endTime)
			logging.info("===recommendations====")
			logging.info(freeTimes)
			jsonFreeTimes = jsonManipulator.getFindTimeResponse(freeTimes)
			return jsonFreeTimes

		else:
			return "error! invalid request type"

	@staticmethod
	def getAllFreeTimes(attendees, startYear, endYear, startMonth, endMonth, startDay, endDay):
		allFreeTimes = list()
		for year in range(int(startYear), int(endYear) + 1):
			for month in range(int(startMonth), int(endMonth) + 1):
				for day in range(int(startDay), int(endDay) + 1):
					freeTimesByDay = dict()
					for attendee in attendees:
						bigList = list()
							##DEMO##
						busyTeachingTimesList = busy_times_db.busy_times_db(day, month, year, attendee)
						#busyTeachingTimesList = [BusyBlock(year='2014', month='09', day='12', startTime=u'0900', endTime=u'1100')]
						#busyTeachingTimesList = []
						busyCalendarTimesList = []
						#busyCalendarTimesList = SearchGoogle.getCalendarEvents(attendee, year, month, day, year, month, day)
						#logging.info("===calendar events====")
						#logging.info(busyCalendarTimesList)

						#Convert the busy teaching times to free times
						freeTeachingTimesList = SubmissionHandler.convertToFreeTimes(busyTeachingTimesList, year, month, day)

						#Convert the busy calendar times to free times
						freeCalendarTimesList = SubmissionHandler.convertToFreeTimes(busyCalendarTimesList, year, month, day)
					
						#Get a list of the combined free times
						combinedFreeTimes = SubmissionHandler.mergeFreeTimes(freeTeachingTimesList, freeCalendarTimesList, year, month, day)
						bigList.append(combinedFreeTimes)
						freeTimesByDay[attendee] = bigList

		

					allFreeTimes.append(freeTimesByDay)

		return allFreeTimes
	@staticmethod
	def convertToFreeTimes(busyTimesList, year, month, day):
		freeTimesList = list()
		logging.info("===busy time list====")
		logging.info(busyTimesList)
		if busyTimesList == 0 or len(busyTimesList) == 0:
			
			freeBlock = FreeBlock(year, month, day, "0000", "2359")
			freeTimesList.append(freeBlock)
		else:
			freeTimesList = busyToFreeTimeConverter.getFreeTimesList(busyTimesList)

		return freeTimesList

	#takes in two lists of free time named tuples for a day. 
	#for each list it creates an array to hold all of the minutes in the day
	#the array vaues are marked true if the person is free at that minute
	#the arrays are compared. where an element is true in both arrays, we know that the people are free at the same time
	@staticmethod
	def mergeFreeTimes(freeTimeListA, freeTimeListB, year, month, day):
		MINS_PER_DAY = 1440

		#Takes time as string and returns mins in int
		def timeToMins(time):
			hour = int(int(time) / 100)

			length = len(time)
			mins = int(time[(length - 2) : length])

			return (60 * hour + mins)

		#Takes mins as int and returns 24 hr time as string: hhmm
		def minsToTime(numMins):
			hour = int(numMins / 60)
			str_hour = str(hour)
			if len(str_hour) < 2:
				str_hour = "0" + str_hour
			
			mins = int(numMins % 60)
			str_mins = str(mins)
			if len(str_mins) < 2:
				str_mins = "0" + str_mins

			return str_hour + str_mins

		#fills an array with 0s fro each minute in a day
		#switches an element to 1 if the person is free at that minute
		def markTimeAsFree(freeTimeList):
			#Create an array indicating no free time
			timeArray = [0] * MINS_PER_DAY

			#For each free time window, mark the time array as free
			for freeTime in freeTimeList:
				year, month, day, startTime, endTime = freeTime
				startMins = timeToMins(startTime)
				endMins = timeToMins(endTime)

				for i in range(startMins, endMins + 1):
					timeArray[i] = 1

			return timeArray

		#compares two time arrays to determine start and end dates of when both are free.
		#stores as a list of free block named tuples
		def combineFreeTimeArrays(timeArrayA, timeArrayB, year, month, day):
			recordingFreeTime = False
			startTime = None
			endTime = None
			combinedFreeTimes = list()

			for minute in range(0, MINS_PER_DAY):

				#If both arrays share a free time, then set as start time, if a start time has not already been determined
				if timeArrayA[minute] == 1 and timeArrayB[minute] == 1:
					if recordingFreeTime == False:
						recordingFreeTime = True
						startTime = minsToTime(minute)

				else:
					if recordingFreeTime == True:
						recordingFreeTime = False
						endTime = minsToTime(minute - 1)


				#Create a time Free time block and add to the array
				if startTime != None and endTime != None:
					sharedFreeTime = FreeBlock(year, month, day, startTime, endTime)
					combinedFreeTimes.append(sharedFreeTime)
					startTime = None
					endTime = None


			#If the end time was the end of the day
			if startTime != None and endTime == None:
				endTime = "2359"
				sharedFreeTime = FreeBlock(year, month, day, startTime, endTime)
				combinedFreeTimes.append(sharedFreeTime)

			return combinedFreeTimes
		


		timeArrayA = markTimeAsFree(freeTimeListA)
		timeArrayB = markTimeAsFree(freeTimeListB)


		return combineFreeTimeArrays(timeArrayA, timeArrayB, year, month, day)

		

		

		





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmissionHandler)
], debug=True)
