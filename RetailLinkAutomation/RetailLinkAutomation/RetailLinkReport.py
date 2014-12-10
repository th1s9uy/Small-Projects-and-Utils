#from . import *

class RetailLinkReport(object):
	
	""" Constructor for RetailLinkReport class """
	def __init__(self, Name=None, ID=None, Definition=None):
		self.Name = Name
		self.ID = ID
		self.Definition = Definition

		# Variables that must be posted when saving a report
		#hdnAppId=300
		self.hdnAppId = None
		#hdnExeId=264
		self.hdnExeId = None
		#hdnAccessCode=P
		self.hdnAccessCode = None
		#hdnCriteria=4	:	E200001	:	...
		self.hdnCriteria = Definition
		#hdnUsers=
		self.hdnUsers = None
		#hdnQId=Q680
		self.hdnQId = None
		#hdnReqName=test2
		self.hdnReqName = Name
		#hdnCompressed=1
		self.hdnCompressed = None
		#hdnFormatType=4
		self.hdnFormatType = None
		#hdnLang=
		self.hdnLang = None
		#hdnRetTxt=
		self.hdnRetTxt = None
		#hdnReqId=-1
		self.hdnReqId = None
		#hdnSchedType=
		self.hdnSchedType = None
		#hdnExpireDate=
		self.hdnExpireDate = None
		#hdnParentReport=
		self.hdnParentReport = None
		#hdnRow_limit_qty=
		self.hdnRow_limit_qty = None
		#hdnDisplay_filter_cd=
		self.hdnDisplay_filter_cd = None
		#hdnFilter_column_desc=
		self.hdnFilter_column_desc = None
		#hdnShow_alerts=
		self.hdnShow_alerts = None
		#hdnCountryCode=US
		self.hdnCountryCode = None
		#hdnErfFlag=
		self.hdnErfFlag = None
		#HdnMultiSchedInd=
		self.HdnMultiSchedInd = None
		#HdnSubmitFreq=
		self.HdnSubmitFreq = None
		#hdnPreviousSchedStatus=
		self.hdnPreviousSchedStatus = None
		#hdnApplicationId=0
		self.hdnApplicationId = None
		#hdnImportMore=
		self.hdnImportMore = None
		#hdnShowAlerts=1
		self.hdnShowAlerts = None
		#hdnImport=0
		self.hdnImport = None
		#hdnScheduleType=
		self.hdnScheduleType = None
		#hdnTransReport=Report
		self.hdnTransReport = None
		#hdnTransWasImported=was imported
		self.hdnTransWasImported = None
		#hdnTransWasSaved=was saved successfully
		self.hdnTransWasSaved = None
		#hdnDimElementReport=	
		self.hdnDimElementReport = None	
		
	def getParamsForPost(self):
		self.hdnCriteria = self.Definition.encode("windows-1252")
		
		keys = self.__dict__.keys()
		values = self.__dict__.values()
		paramDict = {}
		
		for i in xrange(len(keys)):
			key = keys[i]
			val = values[i]
			if(key.startswith("hdn")):
				paramDict[key] = val
				
		return paramDict