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

BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class SubmissionHandler(webapp2.RequestHandler):
	def post(self):
		#Get request in json format from Post
		jsonParameters = self.request.get('request', self)
		#Parse out parameters from json
		requestType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees = jsonManipulator.getParsedParameters(jsonParameters)
		busyTimes = busy_times_db.busy_times_db("17", "06", "2014", "driskilq" )
		self.response.write(busyTimes)
		self.response.write("boo")

		# for attendee in attendees:
		# 	for year in range(int(startYear), int(endYear)+ 1):
		# 		for month in range(int(startMonth), int(endMonth) + 1):
		# 			for day in range(int(startDay), int(endDay) + 1):
		# 				busyTimes = busy_times_db.busy_times_db(day, month, year, attendee)
		# 				self.response.write(busyTimes)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmissionHandler)
], debug=True)
