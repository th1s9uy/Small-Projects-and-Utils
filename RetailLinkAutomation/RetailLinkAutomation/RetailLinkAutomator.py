""" 
	http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet
	http://stackoverflow.com/questions/5035390/submit-without-the-use-of-a-submit-button-mechanize/6894179#6894179
"""

from . import *
import mechanize
import urllib
import json
import re
from bs4 import BeautifulSoup as BS


class RetailLinkAutomator(object):
	
	
	""" Default init method loads libraries,
		sets up browser mechanize object and sets default header		
	"""
	def __init__(self, User=None, Pass=None):
		self.br = mechanize.Browser()
		self.br.set_handle_robots(False)
		self.br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; MS-RTC EA 2')]		
		self.User = User
		self.Pass = Pass
		self.loggedIn = False

	""" High level method to log in to RL """ 
	def login(self):
		self.getLoginPage()
		self.loginFromLoginPage()
		self.loggedIn = True
		
		
	""" Method to move a report id to a folder id """
	def moveReportToFolder(self, reportId, folderId):
		postUrl = "https://retaillink.wal-mart.com/decision_support/mySavedReports.aspx/SaveNewChildParent"
		req = mechanize.Request(postUrl)
		req.add_header('Content-Type','application/json')
		params = {"folderId":folderId,"reportId":reportId,"userId":self.User}
		data = 	json.dumps(params)
		return self.br.open(req,data)
		
		
	""" High level function to get all folders for an ID
	"""
	def getFolders(self):
		self.login()
		self.goToDSSPage()
		self.goToMyReports()
		
		self.writeLastResponse()		
		soup = BS(self.br.response().read())

		folders = []
		#for tag in soup.find_all("span", {"onclick":re.compile("selectFolder\('FF")}):
		for tag in soup.find_all("span", {"id":re.compile("^S2")}):
			folders.append(self.getFolderFromSpan(tag))
			
		return folders
		
	""" Function to handle extracting information from HTML bits
	"""
	def getFolderFromSpan(self, tag):
		name = tag.string
		
		#print("ID attribute: %s" % tag["id"])
		
		#HTML has: selectFolder('FF7171159');
		#onclickAttr = tag["onclick"]
		#m = re.match("selectFolder\('FF(?P<folderId>\d+)'\);", onclickAttr)
		spId = tag["id"]
		m = re.match("S2(?P<folderId>.*)", spId)
		id = m.group('folderId')
		
		return RetailLinkFolder(ID=id, Name=name)
		
		
	""" High level message to log in and get all reports matching pattern """
	def getReportsForPattern(self, pattern, getDefs=True):
		if(not(self.loggedIn)):
			self.login()
		self.goToDSSPage()
		self.goToMyReports()
		reports = self.extractReports()
		
		reports = [report for report in reports if re.match(pattern, report.Name)]
		
		if(getDefs):
			reports = self.getReportDefs(reports)
		
		return reports
		

	""" Function that will use the class's browser object 
		to open the initial RL page.
	"""
	def getLoginPage(self):
		return self.br.open("https://rllogin.wal-mart.com/rl_security/rl_logon.aspx?ServerType=IIS1&CTAuthMode=BASIC&CTLoginErrorMsg=BAD_PWD_OR_USER&language=en&CTUser=&CT_ORIG_URL=%2Frl_security%2Frl_logon.aspx%3FServerType%3DIIS1%26redir%3D%2F&ct_orig_uri=%2Frl_security%2Frl_logon.aspx")

	"""	Function that will log in to retail link. 
	    Side affect of setting the instance User and Pass
		variables if values are passed.
	"""
	def loginFromLoginPage(self, userName=None, passWord=None):
		
		if(userName != None or passWord != None):
			self.User = userName
			self.Pass = passWord
		
		# select the login form
		self.br.select_form("frmLogin")
		userCtrl = self.br.form.find_control("txtUser")
		passCtrl = self.br.form.find_control("txtPass")
		
		userCtrl.value = self.User
		passCtrl.value = self.Pass
		
		return self.br.submit()
	
	
	""" Function to save a report to the current instance of RL """
	def saveReport(self, report, name=None, rename=False):
		if(not(self.loggedIn)):
			self.login()
		postUrl = "https://retaillink.wal-mart.com/decision_support/Save_Schedule_Reports.aspx"
		
		if(name != None):
			report.hdnReqName = name
		
		if(rename == True):
			report.hdnReqId = report.ID
		
		params = report.getParamsForPost()
		data = urllib.urlencode(params)
		response = self.br.open(postUrl,data)
		
		if(not(self.checkSaveSuccess(response))):
			raise RLSaveException("Error saving report")
		
		return response
	
	""" Function to check for a successful save """
	def checkSaveSuccess(self, response):
		
		self.writeLastResponse()
		
		soup = BS(response.read())
		
		#<input name="hdnRetTxt" type="hidden" id="hdnRetTxt" value="Request was updated successfully." />
		#<input name="hdnReqId" type="hidden" id="hdnReqId" value="29379513" />
		for tag in soup.find_all("input", {"id":"hdnRetTxt"}):
			val = tag["value"]
			
		if(val == "Request was updated successfully."):
			return True
		else:
			return False
	
	""" Function that will go to the DSS Link """
	def goToDSSPage(self):
		for link in self.br.links():
			if(link.text == "Decision Support"):
				request = self.br.click_link(link)
				return self.br.follow_link(link)
	
	""" Function to open the My Reports interface from the DSS page """
	def goToMyReports(self):		
		postUrl = "https://retaillink.wal-mart.com/mydss/mySavedReports.aspx"
		params = {"ApplicationId" : "300"}
		data = urllib.urlencode(params)		
		return self.br.open(postUrl,data)
		
	""" Function to extract report names and IDs from the My Reports page
		Returns a list of report objects
	"""
	def extractReports(self):	
		soup = BS(self.br.response().read())

		reports = []
		for sp in soup.find_all("span", {"reportinfostring":True}):				
			reports.append(self.getReportFromSpan(sp))
			
		return reports
		
	""" Function that will get the report definitions of all reports
		passed in as a list. 
	"""
	def getReportDefs(self, reports):
		for report in reports:
			self.getReportDefPage(report.ID)
			report = self.extractReportDef(report)
			
		return reports
			
		
	""" Function that gets the response page with definition in the HTML for
		a report ID
	"""
	def getReportDefPage(self, reportID):
		postUrl = "https://retaillink.wal-mart.com/mydss/Report_Builder.aspx"
		params = {
					"reopen":"true",
					"AppId":"300",
					"jobid":reportID,
					"getSavedRequests":"1",
					"isShared":"N",
					"isScheduled":"N",
					"country_cd":"US",
					"divid":"1"
		}
		data = urllib.urlencode(params)
		return self.br.open(postUrl,data)
	
	""" Function to extract the reports definition form or raw HTML,
		whichever is easier.
	"""
	def extractReportDef(self, report):
		#self.writeControls()
		#self.writeLastResponse()
		
		soup = BS(self.br.response().read())
		for eKeyListTag in soup.find_all("input", {"id":"hdnAllEkeysonMemory"}):				
			eKeyList = eKeyListTag["value"].split(",")
			#print(eKeyList)
			
		for eKeyNumListTag in soup.find_all("input", {"id":"hdnAllKeyNumOnMemory"}):				
			eKeyNumList = eKeyNumListTag["value"].split(",")
			#print(eKeyNumList)
					
		self.br.select_form("Memory")
		report.Definition = self.buildCriteriaString(eKeyList, eKeyNumList)
		report = self.setAllReportProps(report)
		return report
	
	""" Function to set all the extra properies the report needs
		when being saved 
	"""
	def setAllReportProps(self, report):
		report.hdnAppId  = self.br["AppId"]
		report.hdnExeId = self.br["exe_id"]
		report.hdnAccessCode = "P"
		report.hdnUsers = ""
		report.hdnQId = self.br["qid"]
		report.hdnCompressed = self.br["Compresed"]
		report.hdnFormatType = self.br["Format"]
		report.hdnLang = ""
		report.hdnRetTxt = ""
		report.hdnReqId = "-1"
		report.hdnSchedType = self.br["SchedType"]
		report.hdnExpireDate = self.br["ExpireDate"]
		report.hdnParentReport = ""
		report.hdnRow_limit_qty = "" # self.br["row_limit_qty"]
		report.hdnDisplay_filter_cd = "" # self.br["display_filter_cd"]
		report.hdnFilter_column_desc = self.br["filter_column_desc"]
		report.hdnShow_alerts = ""
		report.hdnCountryCode = self.br["CountryCode"]
		report.hdnErfFlag = ""
		report.HdnMultiSchedInd = ""
		report.HdnSubmitFreq = ""
		report.hdnPreviousSchedStatus = ""
		report.hdnApplicationId = "0"
		report.hdnImportMore = self.br["importMore"]
		report.hdnShowAlerts = "1"
		report.hdnImport = "0"
		report.hdnScheduleType = self.br["SchedType"]
		report.hdnTransReport = "Report"
		report.hdnTransWasImported = "was imported"
		report.hdnTransWasSaved = "was saved successfully"
		report.hdnDimElementReport = ""
		
	
	""" Function to build out the criteria string that will
		be the definition of the report
	"""
	def buildCriteriaString(self, eKeyList, eKeyNumList):	
		sep1 = u"\t^\t"
		sep2 = u"\t:\t"
		stepList = []
		criteria = u""
		
		# Get all the step controls
		for control in self.br.form.controls:
			if(control.name == "Step"):
				#print("Control.value type: %s" % type(control.value))
				#http://stackoverflow.com/questions/2365411/python-convert-unicode-to-ascii-without-errors
				unicodeValue = control.value.decode("windows-1252")
				stepList.append(unicodeValue)			
		
		# Loop over the valid Ekeys and extract them from the steps
		for i in xrange(len(eKeyList)):
			eKey = unicode(eKeyList[i])
			eKeyNum = unicode(eKeyNumList[i])
			
			for step in stepList:
				if(eKey in step):
					criteria = criteria + sep1 + eKeyNum + sep2 + step
		
		criteria = criteria.lstrip(sep1)		
		return criteria
		
	
	""" Function to extract and build a report object from a span BS tag """
	def getReportFromSpan(self, sp):
		infoString = sp['reportinfostring']
		reportId = infoString.split("|")[0]
		reportName = sp.img.string
		report = RetailLinkReport(ID=reportId, Name=reportName)
		return report
		
	
	""" Function to print out the forms in the last response """
	def printForms(self):
		for form in self.br.forms():
			print("Form name: %s" % form.name)
		
	""" Function to write out the last response's forms to a file"""
	def writeForms(self):
		with open("Output/currentPageForms.txt", "wb") as curPageForms:
			for form in self.br.forms():
				curPageForms.write("Form name: %s" % form.name)
			
	""" Function to print out the controls in every form in the
		last response
	"""
	def printControls(self):
		for form in self.br.forms():
			self.br.select_form(form.name)
			for control in self.br.form.controls:
				print control
				#try:
					#print("type=%s, name=%s value=%s" %(control.type, control.name, control.value))
				#except AmbiguityError:
					#print("type=%s, name=%s" %(control.type, control.name))
					
	""" Function to write controls in the last respose to a file
	"""
	def writeControls(self):
		with open("Output/currentPageControls.txt", "wb") as curPageControls:
			for form in self.br.forms():
				self.br.select_form(form.name)
				for control in self.br.form.controls:
					curPageControls.write("%s\n" % str(control))
					#try:
					#	curPageControls.write("type=%s, name=%s value=%s\n" %(control.type, control.name, control.value))
					#except AmbiguityError:
					#	curPageControls.write("type=%s, name=%s\n" %(control.type, control.name))
	
	""" Function that will print out all the links on the current
		page """ 
	def printLinks(self):
		for link in self.br.links():
			print link.text, link.url
			
	""" Function that will write out all the links on the current
		page to a default file""" 
	def writeLinks(self):
		with open("Output/currentPageLinks.txt", 'wb') as curPageLinks:
			for link in self.br.links():
				curPageLinks.write("%s, %s\n" % (link.text, link.url))
				
	""" Function that will print the last response the 
		browser object contains
	"""
	def printLastResponse(self):
		print(br.response().read())
		
	""" Function that will write the last response the
		browser object contains to a default file
	"""
	def writeLastResponse(self):
		with open("Output/lastResponse.html", 'wb') as lastResponse:
			lastResponse.write(self.br.response().read())
			
		
	
if __name__ == '__main__':
	RLAutomationUnitTests.testAll()