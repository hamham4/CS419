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

MINS_PER_DAY = 1440

BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")
FreeBlock = namedtuple("FreeBlock", "year, month, day, startTime, endTime")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class SubmissionHandler(webapp2.RequestHandler):
	def post(self):
		#Get request in json format from Post
		jsonParameters = self.request.get('request', self)
		#Parse out parameters from json
		requestType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees = jsonManipulator.getParsedParameters(jsonParameters)
 
		allFreeTimes = SubmissionHandler.getAllFreeTimes(attendees, startYear, endYear, startMonth, endMonth, startDay, endDay)

	@staticmethod
	def getAllFreeTimes(attendees, startYear, endYear, startMonth, endMonth, startDay, endDay):
		allFreeTimes = dict()
		for attendee in attendees:
			freeBlocksByDay = list()
			for year in range(int(startYear), int(endYear) + 1):
				for month in range(int(startMonth), int(endMonth) + 1):
					for day in range(int(startDay), int(endDay) + 1):
						
						#busyTeachingTimesList = busy_times_db.busy_times_db(day, month, year, attendee)
						busyTeachingTimesList = [BusyBlock(year='2014', month='06', day='17', startTime=u'0900', endTime=u'1100'), BusyBlock(year='2014', month='06', day='17', startTime=u'1300', endTime=u'1550'), BusyBlock(year='2014', month='06', day='17', startTime=u'1700', endTime=u'2050')]
						##DEMO##
						busyCalendarTimesList = [BusyBlock(year='2014', month='06', day='17', startTime=u'0000', endTime=u'1200'), BusyBlock(year='2014', month='06', day='17', startTime=u'1300', endTime=u'1900')]

						#Convert the busy teaching times to free times
						freeTeachingTimesList = SubmissionHandler.convertToFreeTimes(busyTeachingTimesList, year, month, day)

						#Convert the busy calendar times to free times
						freeCalendarTimesList = SubmissionHandler.convertToFreeTimes(busyCalendarTimesList, year, month, day)
						
						#Get a list of the combined free times
						combinedFreeTimes = SubmissionHandler.mergeFreeTimes(freeTeachingTimesList, freeCalendarTimesList, year, month, day)

						freeBlocksByDay.append(combinedFreeTimes)

						logging.info("combined free times")
						logging.info(combinedFreeTimes)


			allFreeTimes[attendee] = freeBlocksByDay
		return allFreeTimes
	@staticmethod
	def convertToFreeTimes(busyTimesList, year, month, day):
		if len(busyTimesList) == 0:
			freeTimesList = list()
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

		#Takes time as string and returns mins in int
		def timeToMins(time):
			hour = int(time) / 100
			length = len(time)
			mins = int(time[(length - 2) : length])

			return (60 * hour + mins)


		#Takes mins as int and returns 24 hr time as string: hhmm
		def minsToTime(numMins):
			hour = numMins / 60
			str_hour = str(hour)
			if len(str_hour) < 2:
				str_hour = "0" + str_hour
			
			mins = numMins % 60
			str_mins = str(mins)
			if len(str_mins) < 2:
				str_mins = "0" + str_mins

			return str_hour + str_mins

		#fills an array with Os fro each minute in a day
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


			#If the end time was the nd of the day
			if startTime != None and endTime == None:
				endTime = "2459"
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
