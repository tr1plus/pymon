import web
import ConfigParser
import json
import decimal
import datetime

configFileDir = 'config.cfg'
config = ConfigParser.ConfigParser()

def logEntry(nodeId, module,severity, message, database):
	print("::" + severity.upper() + "::" + " in " + module + "(" + str(nodeId) + ")" + ": " + message)
	database.insert('Logs', nodeId=nodeId, logType=severity, module=module,message=message) #Add additional entries!
	
def addConfig(section, key, default):
	config.read(configFileDir)
	#Node Config
	if not (config.has_section(section)):
		config.add_section(section)
	if not (config.has_option(section, key)):
		config.set(section, key, default)
	configFile = open(configFileDir, 'w')
	config.write(configFile)
	configFile.close()
	
class jsonExtraEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, decimal.Decimal):
			return float(obj)
		elif isinstance(obj, datetime.datetime):
			return str(obj)
		else:
			return json.JSONEncoder.default(self, obj)