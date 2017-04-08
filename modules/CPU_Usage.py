import web
import json
import psutil
import os

#Helper files
from helper import logEntry
from helper import addConfig
from helper import jsonExtraEncoder

def setupConfig(section):
	addConfig(section, 'schedule', 30)
	return 30

def run(database, nodeId):
	#CPU Usage block
	#possibly support multiple CPUs
	usage = psutil.cpu_percent(interval=1, percpu=True)
	usage = usage[0]
	database.insert('CPU_Usage', value=usage, nodeId=nodeId)
	
def webModule(db, nodes):
	section = os.path.splitext(os.path.basename(__file__))[0]
	addConfig(section, 'dashboardImportance', 5)
	if(len(nodes) == 1):
		nodeId = nodes[0].nodeId
		args = dict(node=nodeId)
		cpuUsageTemp = list(db.select('CPU_Usage', args, order='timestamp DESC', limit='50', where="nodeId = $node"))
		cpuUsageTemp = reversed(cpuUsageTemp)
	elif(len(nodes) > 1):
		cpuUsageTemp = []
		for node in nodes:
			args = dict(node=node.nodeId)
			cpuPerNode = list(db.select('CPU_Usage', args, order='timestamp DESC', where="nodeId = $node", limit='50'))
			cpuPerNode = list(reversed(cpuPerNode))
			cpuUsageTemp.append(cpuPerNode)
		#cpuUsageTemp = list(db.select('CPU_Usage', order='timestamp DESC', limit='50'))
		#cpuUsageTemp = list(reversed(cpuUsageTemp))
	cpuUsageTemp = list(cpuUsageTemp)
	cpuUsage = {}
	for nodeIndex in range (0, len(nodes)):
		#cpuUsage.append(nodes[nodeIndex].nodeId)
		nodeValue = []
		for element in cpuUsageTemp:
			if(len(nodes) == 1):
				if nodes[nodeIndex].nodeId == element.nodeId:
						nodeValue.append({'time': element.timestamp, 'value': element.value})
			else:
				for entry in element:
					if nodes[nodeIndex].nodeId == entry.nodeId:
						nodeValue.append({'time': entry.timestamp, 'value': entry.value})
		cpuUsage[nodes[nodeIndex].nodeId] = nodeValue
	cpuUsage = json.dumps(cpuUsage, cls=jsonExtraEncoder)
	return cpuUsage
	