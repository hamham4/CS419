# Sara Thorup
# CS 419 - Final Project: Group 4
# Examples from: https://docs.python.org/2/howto/curses.html
# https://www.youtube.com/watch?v=eN1eZtjLEnU
# http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/


import curses

def displayOptions(screen, subwin):
	#Where the options will be located in the window
	start_y = 0
	start_x = 0
	numOptions = 4
	subwin.addstr(start_y, start_x, "Select an option, then hit the return key.", curses.A_BOLD)
	subwin.addstr(start_y + 1, start_x, "1: Add a username (at least one needed)")
	subwin.addstr(start_y + 2, start_x, "2: Edit window dates (default tomorrow)")
	subwin.addstr(start_y + 3, start_x, "3: Edit window times (default 9am - 5pm)")

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
		if x == ord('1') or x == ord('2') or x == ord('3'):
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

def selectUsernames(usernames, screen, subwin, win):
	#Coordinates of where text will belocated
	start_y = 0
	start_x = 0
	subwin.addstr(start_y, start_x, "Enter a username: ", curses.A_BOLD)

	
	#Refresh screen (is the necessary?)
	screen.noutrefresh()
	win.noutrefresh()
	subwin.noutrefresh()
	curses.doupdate()
	

def main(screen):
	#User's selections
	usernames = list()



	#Define color options
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_WHITE)
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

	#Display menu options in subwindow and ask for user's choice
	selection = getMenuChoice(screen, subwin, win)
	subwin.clear()
	if selection == ord('1'):
		selectUsernames(usernames, screen, subwin, win)

	
	screen.getch()

try:
	#Curses wrapper initalizes screen, etc
	curses.wrapper(main)
except KeyboardInterrupt:
    print "Got KeyboardInterrupt exception. Exiting..."
    exit() 