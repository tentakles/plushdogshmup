import json
import os.path

class Datastore:
	def __init__(self,filename):
		self.file = filename
	def getFile(self):
		if os.path.isfile(self.file):
			with open(self.file, 'r') as fp:
				data = json.load(fp)	
				return data
		return {}
		
	def setData(self, index,highscore):
		data = self.getFile()		
		data[str(index)] = highscore	
		with open(self.file, 'w') as fp:
			json.dump(data, fp)
			
	def getData(self, index):
		data = self.getFile()
		if str(index) in data:
			return data[str(index)]
		return None