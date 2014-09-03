#This module is used to help parse json request parameters
import json
from collections import namedtuple


FreeBlock = namedtuple("FreeBlock", "year, month, day, startTime, endTime")

#Takes the scheduling request in json format and returns parsed options
def getParsedParameters(jsonParameters):
	try:
		decodedJson = json.loads(jsonParameters)
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

#Takes a list of free time blocks and returns them in json format
def getFindTimeResponse(freeTimes):
	response = ""
	if len(freeTimes) > 0:
		response = '{"response": { "valid": "true", "freeTimes": { "freeTime": ['
		for freeTimeBlock in freeTimes:
			year, month, day, startTime, endTime = freeTimeBlock
			response = response + '{"year": "' + str(year) + '", "month": "' + str(month) + '", "day": "' + str(day) + '", "startTime": "' + startTime + '", "endTime": "' + endTime + '"},'
		response = response[0: len(response) - 1]
		response = response + ']}}}'

	else:
		response = '{"response": { "valid": "false","freeTimes": {"freeTime": [{"year": "0000", "month": "00", "day": "00", "startTime": "0000", "endTime": "0000"}]}}}'
	return response

#Takes a list of available attendees and returns them in json format
def getAttendeesResponse(attendees):
	response = ""
	if len(attendees) > 0:
		response = '{"response": {"valid": "true", "attendees": {"attendee": ['
		for attendee in attendees:
			response = response + '{"username": "' + attendee + '"},'
		response = response[0: len(response) - 1]
		response = response + ']}}}'
	else:
		response = '{"response": {"valid": "false", "attendees": {"attendee": [{"username": "none"}]}}}'
	return response