class Session(object):

	def __init__(self, ipAddress, startDatetimes, startDatetimesStr, documentList, activeStatus):
		self.ipAddress = ipAddress
		self.startDatetimes = [startDatetimes]
		self.startDatetimesStr = [startDatetimesStr]
		self.documentList = [documentList]
		self.numRequests = len(self.documentList)
		self.activeStatus = True

	def show(self):
		print("------------------\nIP: {}\nstartDateTime: {}\nstartDateTimeStr: {}\ndocumentList: {}\nnumRequests: {}\nactiveStatus: {}\n\n".format(self.ipAddress, self.startDatetimes, self.startDatetimesStr, self.documentList, self.numRequests, self.activeStatus))

	def lastStartDatetime(self):
		lastTime = len(self.startDatetimes)-1
		return self.startDatetimes[lastTime]

	def lastStartDatetimeStr(self):
		lastTime = len(self.startDatetimesStr)-1
		return self.startDatetimesStr[lastTime]

	def timeElapsed(self):
		lastTime = len(self.startDatetimes)-1
		return int((self.startDatetimes[lastTime]-self.startDatetimes[0]).total_seconds())+1



