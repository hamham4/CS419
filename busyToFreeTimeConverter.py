# Sara Thorup
# CS 419 - Final Project: Group 4
#The purpose of this program is to return a list of times that an individual is free
#Params: A list of named tuples of busy times
from collections import namedtuple

BusyBlock = namedtuple("BusyBlock", "year, month, day, startTime endTime")
FreeBlock = namedtuple("FreeBlock", "year, month, day, startTime, endTime")

def getFreeTimesList(busyBlockList):
	#list of free times to be returned
	freeTimes = list()

	#Inital end of busy time
	endOfBusyTime = "12:00am"

	#Create a list of free time blocks for every busy block

	#set the busy variables to the first BusyBlock in hte list
	for busyWindow in busyBlockList:
		busyYear, busyMonth, busyDay, busyStartTime, busyStopTime = busyWindow
		freeStartTime = endOfBusyTime
		freeStopTime = busyStartTime
		endOfBusyTime = busyStopTime

		freeBlock = FreeBlock(busyYear, busyMonth, busyDay, freeStartTime, freeStopTime)
		freeTimes.append(freeBlock)

	#End of free time block 
	endOfFreeTime = "11:59pm"

	#Get the year, month, and day for the time block
	busyYear, busyMonth, busyDay, busyStartTime, busyStopTime = busyBlockList[0]

	#The last free time window
	freeBlock = FreeBlock(busyYear, busyMonth, busyDay, endOfBusyTime, endOfFreeTime)

	#Add the final free block to the list
	freeTimes.append(freeBlock)

	return freeTimes
