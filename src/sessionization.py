import sys
import datetime
from sessionObject import *

sessionObjects = {}
inactiveMax = 0
lastTimestamp = None
currTimestamp = None


def setInactivetime(inactivityFile):

	with open(inactivityFile, "r") as inactivityFileR:
		inactiveMax = inactivityFileR.read()
		print("inactiveMax: %s" %inactiveMax)


def setLastTimestamp(inputFile):

	lastLine = inputFile[len(inputFile)-1]
	lastLine = lastLine.split(",")
	lastTimeStr = lastLine[1] + " " + lastLine[2]
	lastTime = datetime.datetime.strptime(lastTimeStr, "%Y-%m-%d %H:%M:%S")
	lastTimestamp = lastTime
	print("lastTimestamp: %s" %lastTimestamp)


def parseText(line):

	line = line.split(",")
	ipAddr = line[0]
	currTimestampStr = line[1] + " " +line[2]
	currTimestamp = datetime.datetime.strptime(currTimestampStr, "%Y-%m-%d %H:%M:%S")
	document = line[4] + "/" + line[5] + "/" + line[6]

	return line, ipAddr, currTimestamp, currTimestampStr, document


def main(inputFile, inactivityFile, outputFile):

	setInactivetime(inactivityFile)
	inputFileR = open(inputFile, "r").readlines()
	setLastTimestamp(inputFileR)


	for line in inputFileR[1:len(inputFileR)]:
		
		line, ipAddr, currTimestamp, currTimestampStr, document = parseText(line)

		if (ipAddr in sessionObjects):
			sessionObjects[ipAddr].startDatetimes.append(currTimestamp)
			sessionObjects[ipAddr].startDatetimesStr.append(currTimestampStr)
			sessionObjects[ipAddr].documentList.append(document)
			sessionObjects[ipAddr].numRequests = len(sessionObjects[ipAddr].documentList)
			sessionObjects[ipAddr].show()
		else:
			session = Session(ipAddr, currTimestamp, currTimestampStr, document)
			sessionObjects[ipAddr] = session
			sessionObjects[ipAddr].show()




if __name__ == '__main__':

	if (len(sys.argv) != 4):
		sys.exit(1)
	else:
		main(sys.argv[1], sys.argv[2], sys.argv[3])


