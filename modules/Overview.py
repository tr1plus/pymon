import web
import json
import os

#Helper
from helper import jsonExtraEncoder
from helper import addConfig

def webModule(db, nodes):
	section = os.path.splitext(os.path.basename(__file__))[0]
	addConfig(section, 'dashboardImportance', 1)
	returnData = {}
	returnData["nodes"] = nodes
	
	if(len(nodes) == 1):
		nodeId = nodes[0].nodeId
		args = dict(node=nodeId)
		
		#CpuUsage
		cpuPerNode = list(db.select('CPU_Usage', args, order='timestamp DESC', where="nodeId = $node", limit='1'))
		returnData["cpuPerNode"] = cpuPerNode
		
		#bootTime
		bootTime = list(db.select('Boot_Time', args, where="node = $node"))
		returnData["bootTime"] = bootTime
		
		#avg disk usage
		avgDiskUsage = list(db.query("SELECT usedSize, totalsize FROM Disk_Usage WHERE node=$node", args))
		
		returnData["avgDiskUsage"] = avgDiskUsage
	else:	
		#avg disk usage
		avgDiskUsage = list(db.query("SELECT usedSize, totalsize FROM Disk_Usage"))
		
		#bootTime
		bootTime = list(db.select('Boot_Time'))
		returnData["bootTime"] = bootTime
		
		returnData["avgDiskUsage"] = avgDiskUsage
	
	returnData = json.dumps(returnData, cls=jsonExtraEncoder)
	return returnData