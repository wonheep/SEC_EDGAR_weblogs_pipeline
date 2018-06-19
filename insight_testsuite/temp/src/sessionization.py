import sys
import datetime
from sessionObject import *

sessionObjects = {}

def setInactivetime(inactivityFile):

	with open(inactivityFile, "r") as inactivityFileR:
		inactiveMax = inactivityFileR.read()
		print("inactiveMax: %s" %inactiveMax)
		return inactiveMax


def setLastTimestamp(inputFile):

	lastLine = inputFile[len(inputFile)-1]
	lastLine = lastLine.split(",")
	lastTimeStr = lastLine[1] + " " + lastLine[2]
	lastTime = datetime.datetime.strptime(lastTimeStr, "%Y-%m-%d %H:%M:%S")
	lastTimestamp = lastTime
	print("lastTimestamp: %s" %lastTimestamp)
	return lastTimestamp


def parseText(line):

	line = line.split(",")
	ipAddr = line[0]
	currTimestampStr = line[1] + " " +line[2]
	currTimestamp = datetime.datetime.strptime(currTimestampStr, "%Y-%m-%d %H:%M:%S")
	document = line[4] + "/" + line[5] + "/" + line[6]

	return line, ipAddr, currTimestamp, currTimestampStr, document

def deleteEndedSessions():
	for each in list(sessionObjects):
		if (sessionObjects[each].activeStatus == False):
			del sessionObjects[each]

def outputFinishedSessions(currTimestamp, outputFile, inactiveMax, lastTimestamp):
	
	print("Trying to Output")

	for each in list(sessionObjects):
		inactiveTime = int((currTimestamp-sessionObjects[each].lastStartDatetime()).total_seconds())
		
		print("~~~~~~~")
		print(sessionObjects[each].ipAddress)
		print(sessionObjects[each].numRequests)
		print("inactive time:%d " %inactiveTime)
		print("current time: %s " %currTimestamp)
		print("last timestamp: %s" %lastTimestamp)
		print("~~~~~~~")

		if ((inactiveTime == inactiveMax) or (currTimestamp == lastTimestamp)):
			print("READY TO OUTPUT")
			sessionObjects[each].activeStatus = False
			outputFileW = open(outputFile, "a+")
			outputFileW.write(sessionObjects[each].ipAddress+","+sessionObjects[each].startDatetimesStr[0]+","+sessionObjects[each].lastStartDatetimeStr()+","+str(sessionObjects[each].timeElapsed())+","+str(sessionObjects[each].numRequests)+"\n")

			del sessionObjects[each]


def main(inputFile, inactivityFile, outputFile):

	inactiveMax = int(setInactivetime(inactivityFile))
	inputFileR = open(inputFile, "r").readlines()
	lastTimestamp = setLastTimestamp(inputFileR)

	count = 0

	for line in inputFileR[1:len(inputFileR)]:
		count += 1
		
		line, ipAddr, currTimestamp, currTimestampStr, document = parseText(line)

		if (ipAddr in sessionObjects):
			print("EXISTING Session")
			print("LINE NO: %d" %count)
			sessionObjects[ipAddr].startDatetimes.append(currTimestamp)
			sessionObjects[ipAddr].startDatetimesStr.append(currTimestampStr)
			sessionObjects[ipAddr].documentList.append(document)
			sessionObjects[ipAddr].numRequests = len(sessionObjects[ipAddr].documentList)
			sessionObjects[ipAddr].show()

			outputFinishedSessions(currTimestamp, outputFile, inactiveMax, lastTimestamp)
			print("++++++++++++++++\n")

		else:
			print("NEW SESSION")
			print("LINE NO: %d" %count)
			session = Session(ipAddr, currTimestamp, currTimestampStr, document, True)
			sessionObjects[ipAddr] = session
			sessionObjects[ipAddr].show()

			outputFinishedSessions(currTimestamp, outputFile, inactiveMax, lastTimestamp)
			print("++++++++++++++++\n")



	#Logic

	# if currtime - lasttime of element is = 2 write to output File
	# if currtime = lasttimestamp then sort remainder items by time then ip addr, then output to file

	#TO Do


if __name__ == '__main__':

	if (len(sys.argv) != 4):
		sys.exit(1)
	else:
		open(sys.argv[3], 'w').close()
		main(sys.argv[1], sys.argv[2], sys.argv[3])


