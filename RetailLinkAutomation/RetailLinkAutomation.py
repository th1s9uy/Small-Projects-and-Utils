""" http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet
"""
class RetailLinkAutomator(object):
	
	loginCredList = {}
	
	""" Default init method loads libraries,
		sets up browser mechanize object and sets default header		
	"""
	def __init__(self):
		import mechanize
		self.br = mechanize.Browser()
		self.br.set_handle_robots(False)
		self.br.set_handle_refresh(False)
		self.br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; MS-RTC EA 2')]
		#self.loginCredList = self.readLoginInfoFromFile()

	""" Function that will use the class's browser object 
		to open the initial RL page.
	"""
	def getLoginPage(self):
		return self.br.open("https://rllogin.wal-mart.com/rl_security/rl_logon.aspx?ServerType=IIS1&CTAuthMode=BASIC&CTLoginErrorMsg=BAD_PWD_OR_USER&language=en&CTUser=&CT_ORIG_URL=%2Frl_security%2Frl_logon.aspx%3FServerType%3DIIS1%26redir%3D%2F&ct_orig_uri=%2Frl_security%2Frl_logon.aspx")

	""" Function that reads sensitive login information from file """
	def readLoginInfoFromFile(self):
		import csv
		userDict = {}
		with open("Sensitive/loginInfo.txt", 'rb') as csvfile:
			for row in csv.reader(csvfile, delimiter=","):
				userDict[row[0]] = row[1]
		return userDict
		
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

##################### TEST METHODS #########################		
	def testGetLoginPage(self):
		print("\r\n********  BEGIN TEST FOR getLoginPage()  **************")
		response = self.getLoginPage()
		print("Method existed successfully")
		#print(response.read())
		print("Length of response: %s" % len(response.read()))
		print("########## END TEST FOR getLoginPage()  ################\r\n")
		
	def testReadLoginInfoFromFile(self):
		print("\r\n********  BEGIN TEST FOR readLoginInfoFromFile()  ************")
		self.loginCredList = self.readLoginInfoFromFile()
		print("Method existed successfully")
		print("Login credential list: %s" % self.loginCredList)
		print("#########  END TEST FOR readLoginInfoFromFile()  #################\r\n")
		
	def testPrintForms(self):
		print("\r\n********  BEGIN TEST FOR printForms()  ************")
		self.printForms()
		print("Method existed successfully")
		print("#########  END TEST FOR printForms()  #################\r\n")
		
	def testPrintControls(self):
		print("\r\n********  BEGIN TEST FOR printControls()  ************")
		self.printControls()
		print("Method existed successfully")
		print("#########  END TEST FOR printControls()  #################\r\n")
	
	def testAll(self):
		self.testGetLoginPage()
		self.testReadLoginInfoFromFile()
		self.testPrintForms()
		self.testPrintControls()
	
if __name__ == '__main__':
	autobot = RetailLinkAutomator()
	autobot.testAll()