import web
import psutil
import time 

#Helper files
from helper import logEntry
from helper import addConfig

def setupConfig(section):
	addConfig(section, 'schedule', 30)
	return 30

def run(database, nodeId):
	all = psutil.net_io_counters(pernic=False)
	database.insert('Network_Usage', value=all.bytes_recv, nodeId=nodeId)