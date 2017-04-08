import web
import ConfigParser
import json
import datetime
import pkgutil
import traceback

import modules

web.config.debug = True

#Helper
from helper import jsonExtraEncoder

urls = (
  '/', 'index',
  '/index', 'index',
  '/logs', 'logs',
  '/settings', 'settings',
  #API
  '/CPU_Usage', 'cpuUsage',
)

configFileDir = 'config.cfg'
config = ConfigParser.ConfigParser()
config.read(configFileDir)
db = web.database(dbn=config.get('Database', 'dbn'), host=config.get('Database', 'host'), port=int(config.get('Database', 'port')), user=config.get('Database', 'user'), pw=config.get('Database', 'pw'), db=config.get('Database', 'db'))

class index:
	def GET(self):
		moduleRender = web.template.render('templates/modules')
		render = web.template.render('templates/', base='layout')
		sortOrder = []
		templateList = []
		
		nodeId = web.input(node=-1)
		nodeId = int(nodeId.node)
		
		nodes = None
		amountOfNodes = None
		
		if nodeId > 0:
			args = dict(node=nodeId)
			nodes = list(db.select('Nodes', args,where="nodeId = $node"))
			amountOfNodes = len(nodes)
		else:
			nodes = list(db.select('Nodes'))
			amountOfNodes = len(nodes)
		
		#Pass the database instance and nodes to the functions
		for loader, name, is_pkg in pkgutil.walk_packages(modules.__path__):
			module = loader.find_module(name).load_module(name)
			try:
				renderMethod = getattr(moduleRender, name)
				#templateList.append(unicode(renderMethod(module.webModule(db, nodes))))
				#entry = "{" + config.get(name, 'dashboardimportance') + ":" + unicode(renderMethod(module.webModule(db, nodes))) + "}"
				nodesJson = json.dumps(nodes, cls=jsonExtraEncoder)
				sortOrder.append([int(config.get(name, 'dashboardimportance')), unicode(renderMethod(module.webModule(db, nodes), nodesJson))])
			except AttributeError as a:
				print(traceback.format_exc())
				print (name + " has no webModule defined, skipping...")
		
		sortOrder = sorted(sortOrder)
		for entry in sortOrder:
			templateList.append(entry[1])
		
		return render.index(nodes, amountOfNodes, templateList)
		
class database:
	def GET(self):
		renderNoLayout = web.template.render('templates')
		render = web.template.render('templates', base='layout')
		templatesList = []
		templatesList.append(unicode(renderNoLayout.database()))
		templatesList.append(unicode(renderNoLayout.temp()))
		return render.nodes(templatesList)

class logs:
	def GET(self):
		render = web.template.render('templates/', base='layout')
		logs = list(db.select('Logs', order="id DESC"))
		logsJson = json.dumps(logs, cls=jsonExtraEncoder)
		return render.logs(logsJson)
		
class settings:
	def GET(self):
		nodes = list(db.select('Nodes'))
		amountOfNodes = len(nodes)
		nodesJson = json.dumps(nodes, cls=jsonExtraEncoder)
		render = web.template.render('templates/', base='layout')
		return render.settings(nodesJson, amountOfNodes)
	def POST(self):
		nodes = list(db.select('Nodes'))
		i = web.input()
		for key, value in i.iteritems():
			#print key, value
			for node in nodes:
				if key == 'cp' + str(node.nodeId):
					args = dict(node=node.nodeId)
					color = dict(color=value)
					db.update('Nodes', vars=args, where="nodeId = $node", **color)
		return settings.GET(self)

class cpuUsage:
	def GET(self):
		nodes = list(db.select('Nodes'))
		cpuUsage = []
		nodeId = web.input(node=-1)
		nodeId = int(nodeId.node)
		
		nodes = None
		amountOfNodes = None
		
		if nodeId > 0:
			args = dict(node=nodeId)
			cpuPerNode = list(db.select('CPU_Usage', args, order='timestamp DESC', where="nodeId = $node", limit='15'))
			cpuUsage.append(cpuPerNode)
		#for node in nodes:
			#args = dict(node=node.nodeId)
			#cpuPerNode = list(db.select('CPU_Usage', args, order='timestamp DESC', where="nodeId = $node", limit='15'))
			#cpuUsage.append(cpuPerNode)
		#cpuUsage = list(db.select('CPU_Usage', order='timestamp DESC', limit='1'))
		#cpuUsage = list(cpuUsage)
		cpuUsage = json.dumps(cpuUsage, cls=jsonExtraEncoder)
		return cpuUsage
		
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()