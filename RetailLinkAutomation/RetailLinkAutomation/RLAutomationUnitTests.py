from . import *
import codecs

def testAll():
#	autoBot1 = RetailLinkAutomator()
#	testGetLoginPage(autoBot1) # passed
#	testReadLoginInfoFromFile() # passed
#	testPrintForms(autoBot1) # passed
#	testPrintControls(autoBot1) # passed
#	testLogin(autoBot1) # passed
#	testGoToDSSPage(autoBot1) # passed
#	testGoToMyReports(autoBot1) # passed
#	testExtractReports(autoBot1) # passed
#	testGetReportDef(autoBot1) # passed for all reports
#	testSaveReportDefinition(autoBot1) # passed for 1
#	testEnumFolders(autoBot1) # passed, including recycle bin and system generated folders
#	testMoveReportToFolder(autoBot1) # Successfully tested, bia
	testMoveReportsToAnotherID() # Successfully moved 64 reports. Spot checked that they run successfully. 

""" Function that will move a report from one ID to the next 
"""	
def testMoveReportsToAnotherID():
	print("\r\n********  BEGIN TEST FOR testMoveReportsToAnotherID()  **************")
	autoBotJapril = RetailLinkAutomator()
	autoBotMike = RetailLinkAutomator()
	loginCredList = readLoginInfoFromFile()
	
	autoBotJapril.User = loginCredList[0]['User']
	autoBotJapril.Pass = loginCredList[0]['Pass']
	
	autoBotMike.User = loginCredList[1]['User']
	autoBotMike.Pass = loginCredList[1]['Pass']
	
	reports = autoBotJapril.getReportsForPattern("zzz_2014_zzz")
	
	print("Got %s reports" % len(reports))
	#raw_input("Hit any key to begin moving reports...")
	
	for report in reports:
		print("Saving report %s: " % report.Name)
		autoBotMike.saveReport(report)
		
	#raw_input("Moved all reports. Hit any key to move them to Category 2014 folder...")
	mikeMovedReports = autoBotMike.getReportsForPattern("zzz_2014_zzz", getDefs=False)
	
	for report in mikeMovedReports:
		print("Moving report %s: " % report.Name)
		autoBotMike.moveReportToFolder(report.ID, "7201699")
	
	print("Method exited successfully")
	print("########## END TEST FOR testMoveReportsToAnotherID()  ################\r\n")		
	
	
	
	
""" Function that will test functionality to move reports to a specific folder
"""
def testMoveReportToFolder(autoBot):
	print("\r\n********  BEGIN TEST FOR testMoveReportToFolder()  **************")
	loginCredList = readLoginInfoFromFile()
	
	autoBot.User = loginCredList[0]['User']
	autoBot.Pass = loginCredList[0]['Pass']
	
	folders = autoBot.getFolders()
	
	for folder in folders:
		print("Folder name: %s, id: %s" % (folder.Name, folder.ID))
		
	print("Moving report to folder: 7201661")
	
	autoBot.moveReportToFolder("29210604", "7201661")
	
	print("Method exited successfully")
	print("########## END TEST FOR testMoveReportToFolder()  ################\r\n")		
	
""" Function that will test functionality to enumerate folders for an ID
"""
def testEnumFolders(autoBot):
	print("\r\n********  BEGIN TEST FOR testEnumFolders()  **************")
	loginCredList = readLoginInfoFromFile()
	
	autoBot.User = loginCredList[0]['User']
	autoBot.Pass = loginCredList[0]['Pass']
	
	folders = autoBot.getFolders()
	
	for folder in folders:
		print("Folder name: %s, id: %s" % (folder.Name, folder.ID))
	
	print("Method exited successfully")
	print("########## END TEST FOR testEnumFolders()  ################\r\n")		
	
""" Function to test the saving of a report definition 
"""
def testSaveReportDefinition(autoBot):
	print("\r\n********  BEGIN TEST FOR testSaveReportDefinition()  **************")
	loginCredList = readLoginInfoFromFile()
	
	autoBot.User = loginCredList[0]['User']
	autoBot.Pass = loginCredList[0]['Pass']
	reports = autoBot.getReportsForPattern("zzz_2014_zzz_RLDS_DailyStoreItemWTDColumnsDailyForCurrentWeek_StoreDetail_Daily_002_001")
	#autoBot.getReportsForPattern("^zzz_2014_zzz(.*)")
	print("Got report %s" % reports[0].Name)
	raw_input("About to test save. Hit any key...")
	autoBot.saveReport(reports[0], name="testFromTester")
	autoBot.writeLastResponse()
	
	print("Method exited successfully")
	print("########## END TEST FOR testSaveReportDefinition()  ################\r\n")		
	
""" Function to test pulling a report definition out of a 
	saved retail link report
"""
def testGetReportDef(autoBot):
	print("\r\n********  BEGIN TEST FOR testGetReportDef()  **************")
	loginCredList = readLoginInfoFromFile()
	autoBot.getLoginPage()
	autoBot.loginFromLoginPage(loginCredList[0]['User'], loginCredList[0]['Pass'])
	autoBot.goToDSSPage()
	autoBot.goToMyReports()
	reports = autoBot.extractReports()
	
	reports = [report for report in reports if report.Name == "zzz_2014_zzz_RLDS_DailyStoreItemWTDColumnsDailyForCurrentWeek_StoreDetail_Daily_002_001"]
	autoBot.getReportDefs(reports)
	
	with codecs.open("Output/reports.txt", "wb", "utf8") as writer:
		for report in reports:
			print("Writing %s" % report.Name)
			print(report.getParamsForPost)
			#print("ID:%s, Name: %s, Definition:\n%s" % (report.ID, report.Name, report.Definition))
			#print("*******************************************\n\n")
			writer.write(u"ID:%s, Name: %s, Definition:\n%s\n\n" % (report.ID, report.Name, report.Definition))
			writer.write(unicode(report.getParamsForPost()))
			writer.write(u"\n\n*******************************************\n\n")
		
	
	print("Method exited successfully")
	print("########## END TEST FOR testGetReportDef()  ################\r\n")		
	
""" Function to test extraction of reports from the MyReports page """
def testExtractReports(autoBot):
	print("\r\n********  BEGIN TEST FOR testExtractReports()  **************")
	loginCredList = readLoginInfoFromFile()
	autoBot.getLoginPage()
	autoBot.loginFromLoginPage(loginCredList[0]['User'], loginCredList[0]['Pass'])
	autoBot.goToDSSPage()
	autoBot.goToMyReports()
	reports = autoBot.extractReports()
	
	print("Extracted %s reports." % len(reports))
	for report in reports:
		print("ID: %s, Name: %s	" % (report.ID, report.Name))

	print("Method exited successfully")
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
	print("Method exited successfully")
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
	print("Method exited successfully")
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
	print("Method exited successfully")
	print("########## END TEST FOR loginFromLoginPage()  ################\r\n")		

""" Function to test multiple logins with separate browser objects
	Cookies should not be shared.
"""
def testMultiLogin():
	return None
	
""" Function to test the saving of a stored report definition from retail link 
"""
def testSaveReportDef():
	return None
	
def testReadLoginInfoFromFile():
	print("\r\n********  BEGIN TEST FOR readLoginInfoFromFile()  ************")
	loginCredList = readLoginInfoFromFile()
	print("Method exited successfully")
	print("Login credential list: %s" % loginCredList)
	print("#########  END TEST FOR readLoginInfoFromFile()  #################\r\n")

def testGetLoginPage(autoBot):
	print("\r\n********  BEGIN TEST FOR getLoginPage()  **************")
	response = autoBot.getLoginPage()
	print("Method exited successfully")
	#print(response.read())
	print("Length of response: %s" % len(response.read()))
	print("########## END TEST FOR getLoginPage()  ################\r\n")	
		
def testPrintForms(autoBot):
	print("\r\n********  BEGIN TEST FOR printForms()  ************")
	autoBot.printForms()
	print("Method exited successfully")
	print("#########  END TEST FOR printForms()  #################\r\n")
		
def testPrintControls(autoBot):
	print("\r\n********  BEGIN TEST FOR printControls()  ************")
	autoBot.printControls()
	print("Method exited successfully")
	print("#########  END TEST FOR printControls()  #################\r\n")
