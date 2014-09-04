# Sara Thorup
# CS 419 - Final Project: Group 4
# Examples from: https://docs.python.org/2/howto/curses.html
# https://www.youtube.com/watch?v=eN1eZtjLEnU
# http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/


import curses
from collections import namedtuple
from datetime import date
import httplib
import urllib
import json

DateWindow = namedtuple("DateWindow", "startYear startMonth startDay endYear endMonth endDay")
TimeWindow = namedtuple("TimeWindow", "startHour, startMin, endHour, endMin")
HOST_URL = "localhost:10080"

def refreshAllScreens(screen, win, subwin):
	screen.noutrefresh()
	win.noutrefresh()
	subwin.noutrefresh()
	curses.doupdate()

def displayOptions(screen, subwin):
	#Where the options will be located in the window
	start_y = 0
	start_x = 0 
	subwin.addstr(start_y, start_x, "Select an option, then hit the return key.", curses.A_BOLD)
	start_y = start_y + 1
	subwin.addstr(start_y, start_x, "1: Select scheduling goal (default get open times)")
	start_y = start_y + 1
	subwin.addstr(start_y, start_x, "2: Add usernames (at least one needed)")
	start_y = start_y + 1
	subwin.addstr(start_y, start_x, "3: Edit window dates (default today)")
	start_y = start_y + 1
	subwin.addstr(start_y, start_x, "4: Edit window times (default 09:00 - 13:00)")
	start_y = start_y + 1
	subwin.addstr(start_y, start_x, "5: Validate and get scheduling recommendations")
	start_y = start_y + 1
	
	#Returns the number of options to help with formatting later
	return start_y

def getMenuChoice(screen, subwin, win):
	#Coordinates of where text will belocated
	start_y = 0
	start_x = 0

	userSelection = None
	x = None

	#Display the menu until the user hits return
	while x != ord('\n'):

		#Displays the menu options
		start_y = displayOptions(screen, subwin)

		#Gets user's selection echo and curser are turned on
		subwin.addstr(start_y, start_x, "Selection: ")
		curses.curs_set(1)
		curses.echo()
		x = subwin.getch()
		if x == ord('1') or x == ord('2') or x == ord('3') or x == ord('4') or x == ord('5') or x == ord('q') or x == ord('Q'):
			userSelection = x

		#Refresh screen (is the necessary?)
		refreshAllScreens(screen, win, subwin)

	#Turn off echo and cursor
	curses.echo()
	curses.curs_set(0)

	#Return the user's selection
	return userSelection


def isInputValid(screen, subwin, win, attendees, dayWindow, timeWindow, schedulingGoal, y_position):
	start_y = y_position
	start_x = 0

	#Retrieve values from named tuples
	startYear, startMonth, startDay, endYear, endMonth, endDay = dayWindow
	startHour, startMin, endHour, endMin = timeWindow

	if attendees == None or len(attendees) == 0:
		#Return to options window
		subwin.addstr(start_y, start_x, "You need to enter at least one username.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif  not str(startYear).isdigit() or not str(endYear).isdigit() or not str(startMonth).isdigit or not str(endMonth).isdigit() or not str(startDay).isdigit() or not str(endDay).isdigit():
		#Return to options window
		subwin.addstr(start_y, start_x, "Years, months, and days must be expressed in numbers.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif not str(startHour).isdigit() or not str(endHour).isdigit() or not str(startMin).isdigit() or not str(endMin).isdigit():
		#Return to options window
		subwin.addstr(start_y, start_x, "Hours and minutes must be expressed in numbers.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif len(str(startYear)) != 4 or len(str(endYear)) != 4 :
		#Return to options window
		subwin.addstr(start_y, start_x, "Must enter 4 digit year", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif len(str(startHour)) > 2 or len(str(endHour)) > 2 or len(str(startMin)) > 2 or len(str(endMin)) > 2:

		#Return to options window
		subwin.addstr(start_y, start_x, "Must enter 2 digit hour and minute", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif len(str(startMonth)) > 2 or len(str(endMonth)) > 2 or len(str(startDay)) > 2 or len(str(endDay)) > 2:

		#Return to options window
		subwin.addstr(start_y, start_x, "Must enter 2 digit month and day", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif int(startMonth) < 1 or int(startMonth) > 12 or int(endMonth) < 1 or int(endMonth) > 12:
		#Return to options window
		subwin.addstr(start_y, start_x, "Month must be from 1-12", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif int(startDay) < 1 or int(startDay) > 31 or int(endDay) < 1 or int(endDay) > 31:
		#Return to options window
		subwin.addstr(start_y, start_x, "Day must be from 1-31", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif int(startHour) < 0 or int(startHour) > 23 or int(endHour) < 0 or int(endHour) > 23:
		#Return to options window
		subwin.addstr(start_y, start_x, "Hour must be from 0-23", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False

	elif int(startMin) < 0 or int(startMin) > 59 or int(endMin) < 0 or int(endMin) > 59:
		#Return to options window
		subwin.addstr(start_y, start_x, "Minute must be from 0-59", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return False


	elif int(startYear) > int (endYear):
		#Return to options window
		subwin.addstr(start_y, start_x, "Start year cannot be larger than end year.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
		input = subwin.getch()
		return False
	
	elif int(startYear) == int(endYear) and int(startMonth) > int(endMonth):
		#Return to options window
		subwin.addstr(start_y, start_x, "Start month cannot be larger than end month.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
		input = subwin.getch()
		return False
	
	elif int(startYear) == int(endYear) and int(startMonth) == int(endMonth) and int(startDay) > int(endDay):
		#Return to options window
		subwin.addstr(start_y, start_x, "Start day cannot be larger than end day.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
		input = subwin.getch()
		return False
	
	elif int(startHour) > int(endHour):
		#Return to options window
		subwin.addstr(start_y, start_x, "Start hour cannot be larger than end hour.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
		input = subwin.getch()
		return False
	
	elif int(startHour) <= int(endHour) and int(startMin) > int(endMin):
		#Return to options window
		subwin.addstr(start_y, start_x, "Start min cannot be larger than end min.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
		input = subwin.getch()
		return False 
	
	elif schedulingGoal == "findAttendees" and int(startDay) != int(endDay):
		#Return to options window
		subwin.addstr(start_y, start_x, "A specific day must be selected for finding attendees", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
		input = subwin.getch()
		return False
	 
	else:
		return True


def getRecommendations(screen, subwin, win, attendees, dayWindow, timeWindow, schedulingGoal):
	start_y = 0
	start_x = 0

	#Retrieve values from named tuples
	startYear, startMonth, startDay, endYear, endMonth, endDay = dayWindow
	startHour, startMin, endHour, endMin = timeWindow

	
	if isInputValid(screen, subwin, win, attendees, dayWindow, timeWindow, schedulingGoal, start_y) == True:
		subwin.addstr(start_y, start_x, "The following criteria will be submitted:")
		start_y = start_y + 1
		curses.curs_set(0)
		
		#Display scheduling goal
		subwin.addstr(start_y, start_x, "Scheduling goal:", curses.A_BOLD)
		start_y = start_y + 1

		if schedulingGoal == ("findTime"):
			subwin.addstr(start_y, start_x, "Find a time during the window where the attendees are available")
			start_y = start_y + 1
		elif schedulingGoal == ("findAttendees"):
			subwin.addstr(start_y, start_x, "Find the attendees who are available during the window")
			start_y = start_y + 1

		#Display attendees
		subwin.addstr(start_y, start_x, "Attendees:", curses.A_BOLD)
		start_y = start_y + 1

		for attendee in attendees:
			subwin.addstr(start_y, start_x, attendee)
			start_y = start_y + 1

			#Refresh screen (is the necessary?)
			refreshAllScreens(screen, win, subwin)

		#Display window
		subwin.addstr(start_y, start_x, "Event window set for:", curses.A_BOLD)
		start_y = start_y + 1

		

		subwin.addstr(start_y, start_x, str(startYear) + "/" + str(startMonth) + "/" + str(startDay) + " - " + str(endYear) + "/" + str(endMonth) + "/" + str(endDay))
		start_y = start_y + 1


		subwin.addstr(start_y, start_x, startHour + ":" + startMin + " - " + endHour + ":" + endMin)
		start_y = start_y + 2 


		subwin.addstr(start_y, start_x, "Hit Enter to display recommendations")
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
		start_y = start_y + 1
		input = subwin.getch()

		subwin.addstr(start_y, start_x, "Recommendations:", curses.A_BOLD)
		start_y = start_y + 1
		start_y = fetchRecommendations(attendees, dayWindow, timeWindow, schedulingGoal, start_y, screen, subwin, win)
		start_y = start_y + 1

		subwin.addstr(start_y, start_x, "Hit Enter to return to main menu.")
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
		input = subwin.getch()

def sendRequest(jsonRequest):
	#sample1 = '{"request": {"type": "findTime","startYear": "2014","endYear": "2014","startMonth": "06","endMonth": "06","startDay": "17","endDay": "17","startTime": "1200","endTime": "2000","attendees": {"attendee": [{"username": "driskilq"}]}}}'
	params = urllib.urlencode({'request': jsonRequest})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = httplib.HTTPConnection("team-four.appspot.com")
	conn.request("POST", "/submit", params, headers)
	response = conn.getresponse().read()

	return response
	
def fetchRecommendations(attendees, dayWindow, timeWindow, schedulingGoal, y_position, screen, subwin, win):
	start_y = y_position
	start_x = 0
	jsonRequest = convertRequestToJson(attendees, dayWindow, timeWindow, schedulingGoal)
	recommendations = sendRequest(jsonRequest)
	response = ""
	try:
		decodedJson = json.loads(recommendations)
		isValid = decodedJson["response"]["valid"]

		if isValid == "false":
			subwin.addstr(start_y, start_x, "No matches were found.")
			start_y = start_y + 1
		else:
			if schedulingGoal == "findAttendees":
				subwin.addstr(start_y, start_x, "Usernames who are available:")
				start_y = start_y + 1
				
				numAttendees = len(decodedJson["response"]["attendees"]["attendee"])
				attendeeString = ""
				
				for i in range(0, numAttendees):
					attendee = decodedJson["response"]["attendees"]["attendee"][i]["username"]
					attendeeString =  attendeeString + attendee + ", "

				attendeeString = attendeeString[0 : len(attendeeString) - 2]
				subwin.addstr(start_y, start_x, attendeeString)
				start_y = start_y + 1


			elif schedulingGoal == "findTime":
				subwin.addstr(start_y, start_x, "Times when everyone is free:")
				start_y = start_y + 1

				numFreeTimes = len(decodedJson["response"]["freeTimes"]["freeTime"])
				for i in range (0, numFreeTimes):
					year = decodedJson["response"]["freeTimes"]["freeTime"][i]["year"]
					month = decodedJson["response"]["freeTimes"]["freeTime"][i]["month"]
					day = decodedJson["response"]["freeTimes"]["freeTime"][i]["day"]
					startTime = decodedJson["response"]["freeTimes"]["freeTime"][i]["startTime"]
					endTime = decodedJson["response"]["freeTimes"]["freeTime"][i]["endTime"]
					freeTimeString = "Year: " + year + ", Month: " + month + ", Day: " + day + ", Start Time: " + startTime + ", End Time: " + endTime
					subwin.addstr(start_y, start_x, freeTimeString)
					start_y = start_y + 1

	
	except (ValueError, KeyError, TypeError):
		print "JSON format error"


	return start_y

def addLeadingZero(digit):
	if len(str(digit)) == 1:
		paddedDigit = "0" + str(digit)
		return paddedDigit
	else:
		return str(digit)

#Puts the users request into json format
def convertRequestToJson(attendees, dayWindow, timeWindow, schedulingGoal):
	#Retrieve values from named tuples
	startYear, startMonth, startDay, endYear, endMonth, endDay = dayWindow
	startHour, startMin, endHour, endMin = timeWindow
	
	startTime = addLeadingZero(startHour) + addLeadingZero(startMin)
	endTime = addLeadingZero(endHour) + addLeadingZero(endMin)

	#creates a string of the request parameters in json format
	jsonRequest = '{"request": {"type": "' + schedulingGoal + '","startYear": "' + str(startYear) + '","endYear": "' + str(endYear) + '","startMonth": "' + addLeadingZero(startMonth) + '","endMonth": "' + addLeadingZero(endMonth) + '","startDay": "' + addLeadingZero(startDay) + '","endDay": "' + addLeadingZero(endDay) + '","startTime": "' + str(startTime) + '","endTime": "' + str(endTime)  + '","attendees": {"attendee": ['

	for attendee in attendees:
		jsonRequest = jsonRequest + '{"username": "' + attendee + '"},'

	jsonRequest = jsonRequest[0: len(jsonRequest) - 1]
	jsonRequest = jsonRequest + ']}}}'

	
	return jsonRequest


def getTimePart(part, screen, subwin, win, y_position):
	curses.echo()
	start_y = y_position
	start_x = 0
	if part == "hour":
		subwin.addstr(start_y, start_x, "Enter hour in 24hr format (0-23): ")
		input = subwin.getstr()
		return input
	elif part == "min":
		subwin.addstr(start_y, start_x, "Enter min (00-59): ")
		input = subwin.getstr()
		return input

#Return the user's selection
def getDatePart(part, screen, subwin, win, y_position):
	curses.echo()
	start_y = y_position
	start_x = 0
	if part == "year":
		subwin.addstr(start_y, start_x, "Enter year yyyy: ")
		input = subwin.getstr()
		return input
	elif part == "month":
		subwin.addstr(start_y, start_x, "Enter month 1-12: ")
		input = subwin.getstr()
		return input
	elif part == "day":
		subwin.addstr(start_y, start_x, "Enter day 1-31: ")
		input = subwin.getstr()
		return input


def getSchedulingSelection(screen, subwin, win):
	x = None
	userSelection = None

	while x != ord('\n'):
		x = subwin.getch()
		if x != ord('\n'):
			userSelection = x

	return userSelection

def getSchedulingGoal(screen, subwin, win):
	userSelection = 0
	curses.curs_set(1)
	curses.echo()
	#Display options until the user hits return
	while userSelection != ord('1') and userSelection != ord('2'):

		subwin.clear() 
		start_y = 0
		start_x = 0

		#Display instructions
		subwin.addstr(start_y, start_x, "Specify you scheduling goal.", curses.A_BOLD)
		start_y = start_y + 1

		#Scheduling choices
		subwin.addstr(start_y, start_x, "1. Get a time when everyone is available")
		start_y = start_y + 1

		subwin.addstr(start_y, start_x, "2. Get a list of who is available")
		start_y = start_y + 1

		subwin.addstr(start_y, start_x, "Selection: ")
		start_y - start_y + 1

		userSelection = getSchedulingSelection(screen, subwin, win)
		refreshAllScreens(screen, win, subwin)
		subwin.clear()
		start_y = 0
		subwin.addstr(start_y, start_x, "Selection was saved.")
		start_y = start_y + 1
		
		#Refresh screens
		refreshAllScreens(screen, win, subwin)

		#Return to options window
		subwin.addstr(start_y, start_x, "Hit Enter to continue")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
	
		input = subwin.getch()




	#Turn off echo and cursor	
	curses.echo()
	curses.curs_set(0)

	#Return the user's selection
	if userSelection == ord('1'):
		return "findTime"
	elif userSelection == ord('2'):
		return "findAttendees"
	else:
		return "error"

def specifyTimeWindow(screen, subwin, win):
	#Turn on cursor and echo
	curses.echo()
	curses.curs_set(1)

	#Coordinates of where text will be located
	start_y = 0
	start_x = 0

	#Display instructions
	subwin.addstr(start_y, start_x, "Specify a window start and end time.", curses.A_BOLD)
	start_y = start_y + 1

	#Get start time of window
	subwin.addstr(start_y, start_x, "Enter start time", curses.color_pair(2))
	start_y = start_y + 1
	startHour = getTimePart("hour", screen, subwin, win, start_y)
	start_y = start_y + 1
	startMin = getTimePart("min", screen, subwin, win, start_y)
	start_y = start_y + 1



	#Get end time of window
	subwin.addstr(start_y, start_x, "Enter end time", curses.color_pair(2))
	start_y = start_y + 1
	endHour = getTimePart("hour", screen, subwin, win, start_y)
	start_y = start_y + 1
	endMin = getTimePart("min", screen, subwin, win, start_y)
	start_y = start_y + 1



	subwin.clear()
	start_y = 0
	subwin.addstr(start_y, start_x, "Time window " + startHour+ ":" + addLeadingZero(startMin) + " - " + endHour + ":" + addLeadingZero(endMin) + " was saved.")
	start_y = start_y + 1
	
	#Refresh screens
	refreshAllScreens(screen, win, subwin)

	#Return to options window
	subwin.addstr(start_y, start_x, "Hit Enter to continue")
	curses.curs_set(0)
	subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
	
	input = subwin.getch()

	#Store date window as a named tuple
	timeWindow = TimeWindow(startHour, startMin, endHour, endMin)

	return timeWindow

def specifyDataWindow(screen, subwin, win):

	#Turn on cursor and echo
	curses.echo()
	curses.curs_set(1)

	#Coordinates of where text will be located
	start_y = 0
	start_x = 0

	#Display instructions
	subwin.addstr(start_y, start_x, "Specify a window start and end date.", curses.A_BOLD)
	start_y = start_y + 1

	#Get start date of window
	subwin.addstr(start_y, start_x, "Enter start date", curses.color_pair(2))
	start_y = start_y + 1
	startYear = getDatePart("year", screen, subwin, win, start_y)
	start_y = start_y + 1
	startMonth = getDatePart("month", screen, subwin, win, start_y)
	start_y = start_y + 1
	startDay = getDatePart("day", screen, subwin, win, start_y)
	start_y = start_y + 1

	

	#Get end date of window
	subwin.addstr(start_y, start_x, "Enter end date", curses.color_pair(2))
	start_y = start_y + 1
	endYear = getDatePart("year", screen, subwin, win, start_y)
	start_y = start_y + 1
	endMonth = getDatePart("month", screen, subwin, win, start_y)
	start_y = start_y + 1
	endDay = getDatePart("day", screen, subwin, win, start_y)
	start_y = start_y + 1


	subwin.clear()
	start_y = 0
	subwin.addstr(start_y, start_x, "Date window " + startYear + "/" + startMonth + "/" + startDay + " - " + endYear + "/" + endMonth + "/" + endDay + " was saved.")
	start_y = start_y + 1
	
	#Refresh screens
	refreshAllScreens(screen, win, subwin)

	#Return to options window
	subwin.addstr(start_y, start_x, "Hit Enter to continue")
	curses.curs_set(0)
	subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
	
	input = subwin.getch()

	#Store date window as a named tuple
	dateWindow = DateWindow(startYear, startMonth, startDay, endYear, endMonth, endDay)

	return dateWindow

def selectUsernames(screen, subwin, win):
	#Stores list of desired attendees
	attendees = list()

	#Coordinates of where text will be located
	start_y = 0
	start_x = 0


	#Display Instructions
	subwin.addstr(start_y, start_x, "Enter at least one username. ", curses.A_BOLD)

	#Refresh screens
	refreshAllScreens(screen, win, subwin)

	#Turn on cursor and echo
	curses.echo()
	curses.curs_set(1)

	#Continue to get attendees until input = n or N
	addAttendee = True
	while addAttendee == True:

		#Get and add username to attendees list
		subwin.addstr(start_y + 1, start_x, "Username: ")
		username = subwin.getstr()
		attendees.append(username)
		subwin.addstr(start_y + 1, start_x, username + " has been added as a desired attendee.", curses.color_pair(2))
		
		#Prompt for additonal attendees
		subwin.addstr(start_y + 2, start_x, "Add another attendee? y/n: ")
		input = subwin.getch()

		#Validate input
		while input != ord('n') and  input != ord('N') and input != ord('y') and input != ord('Y'):
			subwin.clear()
			subwin.addstr(start_y + 1, start_x, "Only enter 'y' or 'n': ", curses.color_pair(1))
			input = subwin.getch()

		#Update addAttendee boolean
		if input == ord('n') or input == ord('N'):
			addAttendee = False
		elif input == ord('y') or input == ord('Y'):
			addAttendee = True

		#Clear the input window
		subwin.clear()

	#Dispaly list of added attendees
	subwin.addstr(start_y, start_x, "The following attendees were added: ", curses.A_BOLD)
	start_y = start_y + 1
	cleanAttendees = list()
	for attendee in attendees:
		if attendee.isspace() == False:
			cleanAttendees.append(attendee)
			subwin.addstr(start_y, start_x, attendee)
			start_y = start_y + 1

		#Refresh screen (is the necessary?)
		refreshAllScreens(screen, win, subwin)

	#Return to options window
	subwin.addstr(start_y, start_x, "Hit Enter to continue")
	curses.curs_set(0)
	subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
	
	refreshAllScreens(screen, win, subwin)

	input = subwin.getch()
	return cleanAttendees


def main(screen):
	#User's selections
	attendees = None

	#Set default date window as tomorrow
	dateWindow = DateWindow(date.today().year, date.today().month, date.today().day, date.today().year, date.today().month, date.today().day)
	timeWindow = TimeWindow("9", "00", "17", "00")
	
	#Set default scheduling goals
	schedulingGoal = "findTime"

	#Define color options
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

	#Adds a title and fills in remaining line
	screen.addstr("Scheduling Assistant", curses.A_REVERSE)
	screen.chgat(-1, curses.A_REVERSE)

	#Adds instructions at the bottom of the screen and highlights key
	screen.addstr(curses.LINES-1, 0, "Press Q to quit")
	screen.chgat(curses.LINES-1, 6, 1, curses.A_BOLD | curses.color_pair(2))
	curses.curs_set(0)

	#Adds a window within the main screen
	win = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)

	#Creates a subwindow
	subwin = win.subwin(curses.LINES-6, curses.COLS-4, 3, 2)

	#Draw a border around the main window
	win.box()
	

	#Update the internal window data structures
	screen.noutrefresh()
	win.noutrefresh()

	#Redraw the screen
	curses.doupdate()

	displayMenu = True
	while displayMenu == True:

		#Display menu options in subwindow and ask for user's choice
		selection = getMenuChoice(screen, subwin, win)
		subwin.clear()
		if selection == ord('1'):
			schedulingGoal = getSchedulingGoal(screen, subwin, win)

		elif selection == ord('2'):
			attendees = selectUsernames(screen, subwin, win)

		elif selection == ord('3'):
			dateWindow = specifyDataWindow(screen, subwin, win)

		elif selection == ord('4'):
			timeWindow = specifyTimeWindow(screen, subwin, win)
		
		elif selection == ord('5'):
			getRecommendations(screen, subwin, win, attendees, dateWindow, timeWindow, schedulingGoal)

		elif selection == ord('q') or selection == ord('Q'):
			displayMenu = False
		
		subwin.clear()
		refreshAllScreens(screen, win, subwin)

try:
	#Curses wrapper initalizes screen, etc
	curses.wrapper(main)
except KeyboardInterrupt:
    print "Got KeyboardInterrupt exception. Exiting..."
    exit() 