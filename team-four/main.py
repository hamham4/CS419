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
import json

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class SubmissionHandler(webapp2.RequestHandler):
	def post(self):
		#Get request from Post
		jsonParameters = self.request.get('request', self)

		#Parse out parameters from json
		requestType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees = getParsedParameters(jsonParameters)

		#Display parameters
		self.response.write(requestType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees)

	#Takes the scheduling request in json format and returns parsed options
	def getParsedParameters(jsonParameters):
		try:
			decodedJson = json.loads(jsonRequest)
			requestType = decodedJson["request"]["type"]
			startYear = decodedJson["request"]["startYear"]
			endYear = decodedJson["request"]["endYear"]
			startMonth = decodedJson["request"]["startMonth"]
			endMonth = decodedJson["request"]["endMonth"]
			startDay = decodedJson["request"]["startDay"]
			endDay = decodedJson["request"]["endDay"]
			startTime = decodedJson["request"]["startTime"]
			endTime = decodedJson["request"]["endTime"]
			attendees = list()

			numAttendees = len(decodedJson["request"]["attendees"]["attendee"])

			#Add all of the attendees
			for i in range(0, numAttendees):
				attendees.append(decodedJson["request"]["attendees"]["attendee"][i]["username"])

			return requestType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees

		except (ValueError, KeyError, TypeError):
			print "JSON format error"


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmissionHandler)
], debug=True)
