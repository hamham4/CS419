# Chris Siple
# CS 419 - Final Project: Group 4
# The purpose of this program is to return a list of times that an individual is busy by querying 
# the course catalog data stored in a GAE datastore via a GAE web application
# Params: 4 digit year, 2 digit month, 2 digit day, and username
# Use: import busy_times_db and call busy_times_db( day, month, year, usr )
# Returns: list of named tuples which represent busy blocks of time for a username on a specific date

import bs4
#from urllib.request import urlopen changed to urlfetch
from google.appengine.api import urlfetch  
from collections import namedtuple


BASE_URL = 'http://parser-cs419.appspot.com/get'
BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")


def busy_times_db( day, month, year, usr ):
	#Make sure that the months and day have two digits
	str_month = str(month)
	if len(str_month) < 2:
		month = "0" + str_month
	else:
		month = str_month
	str_day = str(day)
	
	if len(str_day) < 2:
		day = "0"+ str_day
	else:
		day = str_day

	date = str( year ) + '-' + month + '-' + day
        
	ADD_URL = '?username=' + usr + '&date=' + date + '&submit=Submit'
	URL = BASE_URL + ADD_URL
	
	busyTimes = get_data( URL, date ) 
	if busyTimes == 0:
		return 0
	#for window in range( len( busyTimes ) ):
		#print( busyTimes[window] )
	uniqueBusyTimes = list(OrderedDict.fromkeys(busyTimes))
	return uniqueBusyTimes


def make_soup( url ):
	html = urlfetch.fetch(url).content
	return bs4.BeautifulSoup(html,"lxml")

def get_data( url, date ):
	r = check_date( date )
	if r == 1:
		busyTimes = list()
		busyYear = date[0]+date[1]+date[2]+date[3]
		busyMonth = date[5]+date[6]
		busyDay = date[8]+date[9]
		soup = make_soup(url)
		table = soup.find(id = "db_table")
		for tr in soup.findAll('tr'):
			data = tr.findAll('td')
			data = data[0].get_text().split()
			stime = data[0]
			etime = data[1]
			busyBlock = BusyBlock( busyYear, busyMonth, busyDay, stime, etime)
			busyTimes.append(busyBlock)
		return busyTimes
	return 0

		
def check_date( date ):
	y = date[2]+date[3]
	if y != '14':
		return 0
	m = int( date[6] )
	if m < 6 or m > 9:
		return 0
	d = int( date[8]+date[9] )
	if m == 6 and d < 16:
		return 0
	elif m == 9 and d > 5:
		return 0
	else:
		return 1
