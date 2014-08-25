# Sara Thorup
# CS 419 - Final Project: Group 4

import json

def main():
	#Get request parameters
	#Parse json request
	sample1 = '{"request": {"type": "findTime","startYear": "2014","endYear": "2014","startMonth": "08","endMonth": "08","startDay": "21","endDay": "21","startTime": "09:30","endTime": "13:30","attendees": {"attendee": [{"username": "thorups"},{"username": "siplec"},{"username": "busherir"}]}}}'
	requesType, startYear, endYear, startMonth, endMonth, startDay, endDay, startTime, endTime, attendees = getParsedParameters(sample1)
	#Send to program A
	#Send to program B
	#Send to program C
	#Determine availability
	#Send response


#Takes the scheduling request in json format and returns parsed options
def getParsedParameters(jsonRequest):
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

main()