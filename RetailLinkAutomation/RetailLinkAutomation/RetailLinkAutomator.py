""" 
	http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet
	http://stackoverflow.com/questions/5035390/submit-without-the-use-of-a-submit-button-mechanize/6894179#6894179
"""

from . import *

class RetailLinkAutomator(object):
	
	
	""" Default init method loads libraries,
		sets up browser mechanize object and sets default header		
	"""
	def __init__(self, User=None, Pass=None):
		import mechanize		
		self.br = mechanize.Browser()
		self.br.set_handle_robots(False)
		#self.br.set_handle_refresh(False) # Do I want to do this?
		self.br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; MS-RTC EA 2')]
		
		self.User = User
		self.Pass = Pass
		

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
	
	""" Function that will go to the DSS Link """
	def goToDSSPage(self):
		for link in self.br.links():
			if(link.text == "Decision Support"):
				request = self.br.click_link(link)
				return self.br.follow_link(link)
	
	""" Function to open the My Reports interface from the DSS page """
	def goToMyReports(self):
		import urllib
		postUrl = "https://retaillink.wal-mart.com/mydss/mySavedReports.aspx"
		params = {"ApplicationId" : "300"}
		data = urllib.urlencode(params)		
		return self.br.open(postUrl,data)
		
	""" Function to extract report names and IDs from the My Reports page """
	
	
	""" Function to print out the forms in the last response """
	def printForms(self):
		for form in self.br.forms():
			print("Form name: %s" % form.name)
			
	""" Function to print out the controls in every form in the
		last response
	"""
	def printControls(self):
		for form in self.br.forms():
			self.br.select_form(form.name)
			for control in self.br.form.controls:
				print control
				print("type=%s, name=%s value=%s" %(control.type, control.name, self.br[control.name]))
	
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
	import RLAutomationUnitTests
	RLAutomationUnitTests.testAll()