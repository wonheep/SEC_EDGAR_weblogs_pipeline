class Session(object):

	def __init__(self, ipAddress, startDatetimes, startDatetimesStr, documentList):
		self.ipAddress = ipAddress
		self.startDatetimes = [startDatetimes]
		self.startDatetimesStr = [startDatetimesStr]
		self.documentList = [documentList]
		self.numRequests = len(self.documentList)

	def show(self):
		print("------------------\nIP: {}\nstartDateTime: {}\nstartDateTimeStr: {}\ndocumentList: {}\nnumRequests: {}\n\n".format(self.ipAddress, self.startDatetimes, self.startDatetimesStr, self.documentList, self.numRequests))

	def lastStartDatetime(self):
		lastTime = len(self.startDateTime)-1
		return self.startDatetime[lastTime].total_seconds()

