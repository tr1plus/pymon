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
	#id	node	mountPoint	updated		disk		percent	totalsize
	#PK	PK		PK			update		update		update	update
	partitions = psutil.disk_partitions()
	for disk in partitions:
				sdiskusage = psutil.disk_usage(disk.mountpoint)
				diskName = str(disk.device)
				mountPoint = str(disk.mountpoint)
				usedSize = str(sdiskusage.used)
				totalSize = str(sdiskusage.total)
				#Check if this exists
				args = dict(node=nodeId)
				entries = list(database.select('Disk_Usage', args,where="node = $node"))
				if len(entries) == len(partitions):
					timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
					args = dict(node=nodeId, mountPoint=mountPoint)
					database.update('Disk_Usage', where="node = $node AND mountPoint = $mountPoint", updated=timestamp, disk=diskName, usedSize=usedSize, totalsize=totalSize, vars=args)	
				else:
					database.insert('Disk_Usage', node=nodeId, mountPoint=mountPoint, disk=diskName, usedSize=usedSize, totalsize=totalSize)	
			
			#https://pypi.python.org/pypi/psutil