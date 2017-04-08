import web
import ConfigParser
import os.path
import pkgutil
import schedule
import time
import traceback

#Helper files
import modules
from helper import logEntry

def monitor(nodeId, database):
	try:
		#declare config file
		configFileDir = 'config.cfg'
		config = ConfigParser.ConfigParser()
		config.read('config.cfg')
		
		#Database
		db = database #web.database(dbn=config.get('Database', 'dbn'), host=config.get('Database', 'host'), port=int(config.get('Database', 'port')), user=config.get('Database', 'user'), pw=config.get('Database', 'pw'), db=config.get('Database', 'db'))

		if not(os.path.isfile(configFileDir)):
			logEntry(nodeId, os.path.basename(__file__), "Error", "Edit the config file for first use", db)
			quit()
		else:
			config.read(configFileDir)

		if nodeId > 0:
			logEntry(nodeId, os.path.basename(__file__), "Log", "Starting monitoring for node.", db)
			functions = []
			#if __name__ == '__main__':
			for loader, name, is_pkg in pkgutil.walk_packages(modules.__path__):
				module = loader.find_module(name).load_module(name)
				if 'run' in dir(module):
					functions.append(module)
					if config.has_option(name, 'schedule'):
						interval = int(config.get(name,'schedule'))
					else:
						interval = module.setupConfig(name)
					logEntry(nodeId, os.path.basename(__file__), "Log", "Scheduling " + name + " every " + str(interval) + " seconds.", db)
					#Actually run the module before scheduling it
					module.run(db, nodeId)
					schedule.every(interval).seconds.do(module.run, db, nodeId)
			logEntry(nodeId, os.path.basename(__file__), "Log", "Loaded " + str(len(functions)) + " modules for node.", db)
			
			# Process each function
			#for module in functions:
				#print("executing")
				#module.run(db, nodeId)
			
			#CPU temp block
			#possibly support multiple CPUs
			#usage = psutil.cpu_percent(interval=1, percpu=True)
			#usage = usage[0]
			#db.insert('CPU_Usage', value=usage, nodeId=nodeId)
			#print(usage)
				
		else:
			#We create the new entry
			logEntry(-1, os.path.basename(__file__), "Error", "No Node selected... exiting", db)
			quit()
	except Exception as e:
		logEntry(nodeId, os.path.basename(__file__), "Error", traceback.format_exc(), db)
		quit()