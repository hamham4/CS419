#This module is used to help parse json request parameters
import json

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