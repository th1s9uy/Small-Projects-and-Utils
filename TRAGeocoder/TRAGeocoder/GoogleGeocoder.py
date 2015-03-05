""" 
	http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet
	http://stackoverflow.com/questions/5035390/submit-without-the-use-of-a-submit-button-mechanize/6894179#6894179
"""

from . import *
import requests
import json

class GoogleGeocoder(object):
	""" Default init method takes an API key. If none is given
		Then it reads from an assumed file in an assumed folder.
	"""
	def __init__(self, APIKey=None):
		self.jsonResponse = None
		if(APIKey == None):
			self.getAPIKey()
		else:
			self.APIKey = APIKey
			
	""" Method to extract the Lat and Lon from the JSON
	"""
	def getLatLon(self):
		if(self.jsonResponse == None):
			raise GeocodeException("No JSON. Have you called geocode() with an address?")
		else:
			lat = self.jsonResponse["results"][0]["geometry"]["location"]["lat"]
			lon = self.jsonResponse["results"][0]["geometry"]["location"]["lng"]
			return "%s,%s" % (lat, lon)

	""" Geocode an address """ 
	def geocode(self, address):
		geoUrl = "https://maps.googleapis.com/maps/api/geocode/json"
		self.getAPIKey()
		payload = {'address' : address, 'key' : self.APIKey}
		r = requests.get(geoUrl, params=payload)
		self.jsonResponse = r.json()
		return self.jsonResponse
		
	def writeLastResponse(self):
		with open("Output/lastResponse.json", 'wb') as lastResponse:
			lastResponse.write(self.jsonResponse)
		
	""" Method get the API key from a file and assign it to
		this object.
	"""
	def getAPIKey(self):
			keyList = self.readAPIKeyFromFile()
			self.APIKey = keyList[0]["APIKey"]
		
	def readAPIKeyFromFile(self):
		import csv
		userList = []
		with open("Sensitive/apiKey.txt", 'rb') as csvfile:
			for row in csv.reader(csvfile, delimiter="|"):
				userDict = {}
				userDict["UserEmail"] = row[0] 
				userDict["APIKey"] = row[1]
				userList.append(userDict)
		return userList
		
if __name__ == '__main__':
	RLAutomationUnitTests.testAll()