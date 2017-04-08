import web
import psutil
import datetime
import time 

#Helper files
from helper import logEntry
from helper import addConfig

def setupConfig(section):
	addConfig(section, 'schedule', 30)
	return 30

def run(database, nodeId):
	#id	node	bootTime
	#PK	PK		update
	args = dict(node=nodeId)
	entries = list(database.select('Boot_Time', args,where="node = $node"))
	timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
	bootTime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
	if len(entries) == 1:
		database.update('Boot_Time', where="node = $node", updated=timestamp, boot_time=bootTime, vars=args)	
	else:
		database.insert('Boot_Time', node=nodeId, updated=timestamp, boot_time=bootTime)	