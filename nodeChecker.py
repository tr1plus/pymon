import web
import ConfigParser
import schedule
import time
import os
import traceback

#monitor file
from monitor import monitor

#Helper files
from helper import logEntry

def checkNode():
	#Check if we exist, else we want to make ourselves known
	args = dict(hostname=config.get('Node', 'nodename'))
	nodes = list(db.select('Nodes', args,where="hostName = $hostname"))
	if len(nodes) > 0:
		logEntry(nodes[0]['nodeId'], os.path.basename(__file__), "Log", "Checking database connection, confirming node is in database", db)
	#nodes = list(db.query('SELECT * FROM Nodes'))
	return nodes
try:
	#declare config file
	configFileDir = 'config.cfg'
	config = ConfigParser.ConfigParser()

	if not(os.path.isfile(configFileDir)):
		configFile = open(configFileDir, 'w')
		#Node Config
		config.add_section('Node')
		config.set('Node','nodename', '')
		#Database Config
		config.add_section('Database')
		config.set('Database','debug', False)
		config.set('Database','dbn', '')
		config.set('Database','host', '')
		config.set('Database','port', '3306')
		config.set('Database','user', '')
		config.set('Database','pw', '')
		config.set('Database','db', '')
		config.write(configFile)
		configFile.close()
		print('Edit the config file for first use!')
		quit()
	else:
		config.read(configFileDir)
		
	db = web.database(dbn=config.get('Database', 'dbn'), host=config.get('Database', 'host'), port=int(config.get('Database', 'port')), user=config.get('Database', 'user'), pw=config.get('Database', 'pw'), db=config.get('Database', 'db'))
	if config.get('Database', 'debug') == "False":
		db.printing = False
	else:
		db.printing = True

	nodes = checkNode()
	if len(nodes) > 0:
		#It exists	
		nodeId = nodes[0]['nodeId']
		schedule.every().day.at("00:00").do(checkNode)
		monitor(nodeId, db)
		
		while True:
			schedule.run_pending()
			time.sleep(1)
			
	else:
		#We create the new entry
		print("Creating new node...")
		db.insert('Nodes', hostName=config.get('Node', 'nodename'))
except Exception as e:
		logEntry(nodeId, os.path.basename(__file__), "Error", traceback.format_exc(), db)
		quit()