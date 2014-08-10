#The purpose of this program is to return a list of times that an individual is free
#Params: The times the the individual is busy for a certain day

from collections import namedtuple

BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")
FreeBlock = namedtuple("FreeBlock", "year, month, day, startTime, endTime")

def main():
	# sample busy times stored in a list
	b1 = BusyBlock("2014", "8", "3", "9:00am", "11:00am")
	b2 = BusyBlock("2014", "8", "3", "1:00pm", "5:00pm")
	busyTimes = [b1, b2]

	#list of free times to be returned
	freeTimes = list()
	
	#create free time windows based on busy times
	stop = "12:00am"
	busyYear, busyMonth, busyDay, busyStart, busyStop = busyTimes[0]
	for busyTime in busyTimes:
		busyYear, busyMonth, busyDay, busyStart, busyStop = busyTime
		freeStart = stop
		freeStop = busyStart
		stop = busyStop
		freeTime = FreeBlock(busyYear, busyMonth, busyDay, freeStart, freeStop)
		freeTimes.append(freeTime)
	#The last free time window
	freeTime = FreeBlock(busyYear, busyMonth, busyDay, stop, "11:59pm")
	
	freeTimes.append(freeTime)
	
	#display free times
	for time in freeTimes:
		print time
main()