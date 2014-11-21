from . import *


def testAll():
	autoBot1 = RetailLinkAutomator()
#	testGetLoginPage(autoBot1) # passed
#	testReadLoginInfoFromFile() # passed
#	testPrintForms(autoBot1) # passed
#	testPrintControls(autoBot1) # passed
#	testLogin(autoBot1) # passed
#	testGoToDSSPage(autoBot1) # passed
#	testGoToMyReports(autoBot1) # passed
	testExtractReports(autoBot1)
	
""" Function to test extraction of reports from the MyReports page """
def testExtractReports(autoBot):
	print("\r\n********  BEGIN TEST FOR testExtractReports()  **************")
	loginCredList = readLoginInfoFromFile()
	autoBot.getLoginPage()
	autoBot.loginFromLoginPage(loginCredList[0]['User'], loginCredList[0]['Pass'])
	autoBot.goToDSSPage()
	autoBot.goToMyReports()
	autoBot.extractReports()

	print("Method existed successfully")
	print("########## END TEST FOR testExtractReports()  ################\r\n")			
	
""" Function to test the successful open of the My Reports page """
def testGoToMyReports(autoBot):
	print("\r\n********  BEGIN TEST FOR testGoToMyReports()  **************")
	loginCredList = readLoginInfoFromFile()
	autoBot.getLoginPage()
	autoBot.loginFromLoginPage(loginCredList[0]['User'], loginCredList[0]['Pass'])
	autoBot.goToDSSPage()
	response = autoBot.goToMyReports()
	result = response.read()
	print("Length of response from My Reports page is: %s" % len(result))
	autoBot.writeLastResponse()
	print("Response html of My Reports page written to Output/lastResponse.html")
	autoBot.writeLinks()
	print("Links on the My Reports page page have been written to Output/currentPageLinks.txt")	
	print("Method existed successfully")
	print("########## END TEST FOR testGoToMyReports()  ################\r\n")			
	
""" Function to test the successful transition to the DSS page """
def testGoToDSSPage(autoBot):
	print("\r\n********  BEGIN TEST FOR testgoToDSSPage()  **************")
	loginCredList = readLoginInfoFromFile()
	autoBot.getLoginPage()
	response = autoBot.loginFromLoginPage(loginCredList[0]['User'], loginCredList[0]['Pass'])
	result = response.read()
	print("Length of response from homepage: %s" % len(result))
	autoBot.writeLastResponse()
	print("Response html of homepage written to Output/lastResponse.html")
	autoBot.writeLinks()
	print("Links on the home page have been written to Output/currentPageLinks.txt")	
	response = autoBot.goToDSSPage()
	result = response.read()
	print("Length of response from DSS page: %s" % len(result))
	autoBot.writeLastResponse()
	print("Response html of DSS page written to Output/lastResponse.html")
	autoBot.writeLinks()
	print("Links on the DSS page page have been written to Output/currentPageLinks.txt")	
	print("Method existed successfully")
	print("########## END TEST FOR testgoToDSSPage()  ################\r\n")	
	

""" Function that reads sensitive login information from file """
def readLoginInfoFromFile():
	import csv
	userList = []
	
	with open("Sensitive/loginInfo.txt", 'rb') as csvfile:
		for row in csv.reader(csvfile, delimiter=","):
			userDict = {}
			userDict["User"] = row[0] 
			userDict["Pass"] = row[1]
			userList.append(userDict)
	return userList

""" Function to test the successful login to Retail Link """
def testLogin(autoBot):
	print("\r\n********  BEGIN TEST FOR loginFromLoginPage()  **************")
	loginCredList = readLoginInfoFromFile()
	autoBot.getLoginPage()
	response = autoBot.loginFromLoginPage(loginCredList[0]['User'], loginCredList[0]['Pass'])
	result = response.read()
	print("Length of response: %s" % len(result))
	autoBot.writeLastResponse()
	print("Response html written to Output/lastResponse.html")
	autoBot.writeLinks()
	print("Links on the current page have been written to Output/currentPageLinks.txt")
	print("Method existed successfully")
	print("########## END TEST FOR loginFromLoginPage()  ################\r\n")		

""" Function to test multiple logins with separate browser objects
	Cookies should not be shared.
"""
def testMultiLogin():
	return None
""" Function to test the enumeration of all retail link reports
"""
def testReportEnum():
	return None
""" Function to test pulling a report definition out of a 
	saved retail link report
"""
def testGetReportDef():
	return None
	
""" Function to test the saving of a stored report definition from retail link 
"""
def testSaveReportDef():
	return None
	
def testReadLoginInfoFromFile():
	print("\r\n********  BEGIN TEST FOR readLoginInfoFromFile()  ************")
	loginCredList = readLoginInfoFromFile()
	print("Method existed successfully")
	print("Login credential list: %s" % loginCredList)
	print("#########  END TEST FOR readLoginInfoFromFile()  #################\r\n")

def testGetLoginPage(autoBot):
	print("\r\n********  BEGIN TEST FOR getLoginPage()  **************")
	response = autoBot.getLoginPage()
	print("Method existed successfully")
	#print(response.read())
	print("Length of response: %s" % len(response.read()))
	print("########## END TEST FOR getLoginPage()  ################\r\n")	
		
def testPrintForms(autoBot):
	print("\r\n********  BEGIN TEST FOR printForms()  ************")
	autoBot.printForms()
	print("Method existed successfully")
	print("#########  END TEST FOR printForms()  #################\r\n")
		
def testPrintControls(autoBot):
	print("\r\n********  BEGIN TEST FOR printControls()  ************")
	autoBot.printControls()
	print("Method existed successfully")
	print("#########  END TEST FOR printControls()  #################\r\n")
