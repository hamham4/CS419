# Sara Thorup
# CS 419 - Final Project: Group 4
# Examples from: https://docs.python.org/2/howto/curses.html
# https://www.youtube.com/watch?v=eN1eZtjLEnU
# http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/


import curses
from collections import namedtuple
from datetime import date


DateWindow = namedtuple("DateWindow", "startYear startMonth startDay endYear endMonth endDay")
TimeWindow = namedtuple("TimeWindow", "startHour, startMin, endHour, endMin")

def displayOptions(screen, subwin):
	#Where the options will be located in the window
	start_y = 0
	start_x = 0 
	numOptions = 5
	subwin.addstr(start_y, start_x, "Select an option, then hit the return key.", curses.A_BOLD)
	subwin.addstr(start_y + 1, start_x, "1: Add usernames (at least one needed)")
	subwin.addstr(start_y + 2, start_x, "2: Edit window dates (default tomorrow)")
	subwin.addstr(start_y + 3, start_x, "3: Edit window times (default 9am - 5pm)")
	subwin.addstr(start_y + 4, start_x, "4: Get scheduling recommendations")
	
	#Returns the number of options to help with formatting later
	return numOptions

def getMenuChoice(screen, subwin, win):
	#Coordinates of where text will belocated
	start_y = 0
	start_x = 0

	userSelection = None
	x = None

	#Display the menu until the user hits return
	while x != ord('\n'):

		#Displays the menu options
		numOptions = displayOptions(screen, subwin)

		#Gets user's selection echo and curser are turned on
		subwin.addstr(start_y + numOptions, start_x, "Selection: ")
		curses.curs_set(1)
		curses.echo()
		x = subwin.getch()
		if x == ord('1') or x == ord('2') or x == ord('3') or x == ord('4') or x == ord('q') or x == ord('Q'):
			userSelection = x

		#Refresh screen (is the necessary?)
		screen.noutrefresh()
		win.noutrefresh()
		subwin.noutrefresh()
		curses.doupdate()

	#Turn off echo and cursor
	curses.echo()
	curses.curs_set(0)

	#Return the user's selection
	return userSelection

def getRecommendations(screen, subwin, win, attendees):
	start_y = 0
	start_x = 0

	if attendees == None or len(attendees) == 0:
		#Return to options window
		subwin.addstr(start_y, start_x, "You need to enter at least one username.", curses.color_pair(1))
		start_y = start_y + 1
		subwin.addstr(start_y, start_x, "Hit Enter to return to menu")
		curses.curs_set(0)
		subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))

		input = subwin.getch()
		return
	else:
		subwin.addstr(start_y, start_x, "The following criteria will be submitted:")
		curses.curs_set(0)
		input = subwin.getch()


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

def validateDate():
	pass

def validateTime():
	pass

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

	validateTime()

	#Get end time of window
	subwin.addstr(start_y, start_x, "Enter end time", curses.color_pair(2))
	start_y = start_y + 1
	endHour = getTimePart("hour", screen, subwin, win, start_y)
	start_y = start_y + 1
	endMin = getTimePart("min", screen, subwin, win, start_y)
	start_y = start_y + 1

	validateTime()

	subwin.clear()
	start_y = 0
	subwin.addstr(start_y, start_x, "Time window " + startHour+ ":" + startMin + " - " + endHour + ":" + endMin + " was saved.")
	start_y = start_y + 1
	
	#Refresh screens
	screen.noutrefresh()
	win.noutrefresh()
	subwin.noutrefresh()
	curses.doupdate()

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

	validateDate()

	#Get end date of window
	subwin.addstr(start_y, start_x, "Enter end date", curses.color_pair(2))
	start_y = start_y + 1
	endYear = getDatePart("year", screen, subwin, win, start_y)
	start_y = start_y + 1
	endMonth = getDatePart("month", screen, subwin, win, start_y)
	start_y = start_y + 1
	endDay = getDatePart("day", screen, subwin, win, start_y)
	start_y = start_y + 1

	validateDate() 

	subwin.clear()
	start_y = 0
	subwin.addstr(start_y, start_x, "Date window " + startYear + "\\" + startMonth + "\\" + startDay + " - " + endYear + "\\" + endMonth + "\\" + endDay + " was saved.")
	start_y = start_y + 1
	
	#Refresh screens
	screen.noutrefresh()
	win.noutrefresh()
	subwin.noutrefresh()
	curses.doupdate()

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
	screen.noutrefresh()
	win.noutrefresh()
	subwin.noutrefresh()
	curses.doupdate()

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
	for attendee in attendees:
		subwin.addstr(start_y, start_x, attendee)
		start_y = start_y + 1

		#Refresh screen (is the necessary?)
		screen.noutrefresh()
		win.noutrefresh()
		subwin.noutrefresh()
		curses.doupdate()

	#Return to options window
	subwin.addstr(start_y, start_x, "Hit Enter to continue")
	curses.curs_set(0)
	subwin.chgat(start_y, 4, 5, curses.A_BOLD | curses.color_pair(2))
	
	screen.noutrefresh()
	win.noutrefresh()
	subwin.noutrefresh()
	curses.doupdate()

	input = subwin.getch()
	return attendees


def main(screen):
	#User's selections
	attendees = None

	#Set default date window as tomorrow
	dateWindow = DateWindow(date.today().year, date.today().month, date.today().day + 1, date.today().year, date.today().month, date.today().day + 1)
	timeWindow = TimeWindow("9", "00", "17", "00")
	#Define color options
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

	#Adds a title and fills in remaining line
	screen.addstr("Time Finder", curses.A_REVERSE)
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
			attendees = selectUsernames(screen, subwin, win)

		elif selection == ord('2'):
			dateWindow = specifyDataWindow(screen, subwin, win)

		elif selection == ord('3'):
			timeWindow = specifyTimeWindow(screen, subwin, win)
		
		elif selection == ord('4'):
			getRecommendations(screen, subwin, win, attendees)

		elif selection == ord('q') or selection == ord('Q'):
			displayMenu = False
		
		subwin.clear()
		screen.noutrefresh()
		win.noutrefresh()
		subwin.noutrefresh()
		curses.doupdate()
	

try:
	#Curses wrapper initalizes screen, etc
	curses.wrapper(main)
except KeyboardInterrupt:
    print "Got KeyboardInterrupt exception. Exiting..."
    exit() 