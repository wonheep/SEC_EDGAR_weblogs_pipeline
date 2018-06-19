import sys
import datetime
from sessionObject import *

sessionObjects = {}

# NOTE: set time that determines inactivity of session
def setInactivetime(inactivityFile):
	with open(inactivityFile, "r") as inactivityFileR:
		inactiveMax = inactivityFileR.read()
		# print("inactiveMax: %s" %inactiveMax)
		return inactiveMax


# NOTE: set last requesttime that ends all active sessions, coming from input file
def setLastTimestamp(inputFile):
	lastLine = inputFile[len(inputFile)-1]
	lastLine = lastLine.split(",")
	lastTimeStr = lastLine[1] + " " + lastLine[2]
	lastTime = datetime.datetime.strptime(lastTimeStr, "%Y-%m-%d %H:%M:%S")
	lastTimestamp = lastTime
	# print("lastTimestamp: %s" %lastTimestamp)
	return lastTimestamp


# NOTE: parse each line from input file to get pertinent data fields
def parseText(line):
	line = line.split(",")
	ipAddr = line[0]
	currTimestampStr = line[1] + " " +line[2]
	currTimestamp = datetime.datetime.strptime(currTimestampStr, "%Y-%m-%d %H:%M:%S")
	document = line[4] + "/" + line[5] + "/" + line[6]

	return line, ipAddr, currTimestamp, currTimestampStr, document


# NOTE: Check sessionObjects hashmap to see if any of the sessions have become inactive or currenttime=lasttimestamp, output to file
def outputFinishedSessions(currTimestamp, outputFile, inactiveMax, lastTimestamp):

	for each in list(sessionObjects):
		inactiveTime = int((currTimestamp-sessionObjects[each].lastStartDatetime()).total_seconds())
		
		# DEBUG
		# print(sessionObjects[each].ipAddress)
		# print(sessionObjects[each].numRequests)
		# print("inactive time:%d " %inactiveTime)
		# print("current time: %s " %currTimestamp)
		# print("last timestamp: %s" %lastTimestamp)

		if ((inactiveTime == inactiveMax) or (currTimestamp == lastTimestamp)):
			sessionObjects[each].activeStatus = False
			outputFileW = open(outputFile, "a+")
			outputFileW.write(sessionObjects[each].ipAddress+","+sessionObjects[each].startDatetimesStr[0]+","+sessionObjects[each].lastStartDatetimeStr()+","+str(sessionObjects[each].timeElapsed())+","+str(sessionObjects[each].numRequests)+"\n")

			# delete session element from hashmap after writing to file 
			del sessionObjects[each]


# NOTE: reads each line of input file and either creates session object or updates existing one 
def main(inputFile, inactivityFile, outputFile):

	inactiveMax = int(setInactivetime(inactivityFile))
	inputFileR = open(inputFile, "r").readlines()
	lastTimestamp = setLastTimestamp(inputFileR)
	count = 0

	for line in inputFileR[1:len(inputFileR)]:

		line, ipAddr, currTimestamp, currTimestampStr, document = parseText(line)

		count += 1
		print("LINE NO: %d" %count)

		if (ipAddr in sessionObjects):
			print("EXISTING SESSION")
			sessionObjects[ipAddr].startDatetimes.append(currTimestamp)
			sessionObjects[ipAddr].startDatetimesStr.append(currTimestampStr)
			sessionObjects[ipAddr].documentList.append(document)
			sessionObjects[ipAddr].numRequests = len(sessionObjects[ipAddr].documentList)
			sessionObjects[ipAddr].show()

			outputFinishedSessions(currTimestamp, outputFile, inactiveMax, lastTimestamp)

		else:
			print("NEW SESSION")
			session = Session(ipAddr, currTimestamp, currTimestampStr, document)
			sessionObjects[ipAddr] = session
			sessionObjects[ipAddr].show()

			outputFinishedSessions(currTimestamp, outputFile, inactiveMax, lastTimestamp)



if __name__ == '__main__':

	# check proper # of arguments
	if (len(sys.argv) != 4):
		sys.exit(1)
	else:
		# delete contents of output file before running main
		open(sys.argv[3], 'w').close()
		main(sys.argv[1], sys.argv[2], sys.argv[3])


