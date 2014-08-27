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
						
						busyTeachingTimesList = busy_times_db.busy_times_db(day, month, year, attendee)
						#busyCalendarTimesList = blah blah blah

						#Convert the busy teaching times to free times
						freeTeachingTimesList = SubmissionHandler.convertToFreeTimeList(busyTeachingTimesList, year, month, day)
						
						#Get a list of free times from a list of free times and a list of busy times
						combinedFreeTimes = SubmissionHandler.mergeBusyandFree(busyCalendarTimesList, freeTeachingTimesList)

						freeBlocksByDay.append(combinedFreeTimes)
						self.response.write(busyTeachingTimesList)
						self.response.write(freeTeachingTimesList)

			allFreeTimes[attendee] = freeBlocksByDay
	@staticmethod
	def convertToFreeTimes(busyTimeList, year, month, day):
		if len(busyTeachingTimesList) == 0:
			freeTeachingTimesList = list()
			freeBlock = FreeBlock(year, month, day, "0000", "2359")
			freeTeachingTimesList.append(freeBlock)
		else:
			freeTeachingTimesList = busyToFreeTimeConverter.getFreeTimesList(busyTeachingTimesList)

		return freeTeachingTimesList

	@staticmethod
	def mergeBusyandFree(busyTimesList, freeTimesList):
		#If there are no busy times, then all times are free
		combinedBusyTimes = list()
		if len(busyTimesList) == 0:
			combinedFreeTimes = freeTimesList
		else: 
			for busyWindow in busyTimesList:
				pass
		
		return combinedFreeTimes

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmissionHandler)
], debug=True)
