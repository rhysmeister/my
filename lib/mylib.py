import os, platform, MySQLdb, socket, subprocess, re

class NetworkTools:
	"""
	A collection of Network related functions
	"""

	def ping(self, host):
    		"""
    		Returns True if host responds to a ping request
    		"""
    		# Ping parameters as function of OS
    		ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    		# Ping
		devnull_str = "" if platform.system().lower == "windows" else " &> /dev/null"
		s = None
		ping = "ping " + ping_str + " " + host + devnull_str
		try:
			success = None
			if subprocess.check_call([ping], shell=True) == 0:
				success = True
		except Exception as excep:
			#print dir(excep)
			if excep.returncode in [1, 2]:
				success = False
			else:
				raise excep
		return success

        def is_port_open(self, hostname, port):
                port_open = False
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if s.connect_ex((hostname, port)) == 0:
                        port_open = True
                return port_open

class PyMaria:
	"""
	A bunch of methods for MariaDB 
	"""

	def __init__(self, hostname="127.0.0.1", port=3306, username="pytest", password="secret", database="mysql"):
		
		self.hostname = hostname
		self.port = port
		self.username = username
		self.password = password
		self.database = database

		self.connection = self.m_connection(self.hostname,
						    self.port,
						    self.username,
						    self.password,
						    self.database)

		self.slave_status = self.show_slave_status()
		self.master_status = self.show_master_status()
		self.processlist = self.show_processlist()
		self.global_variables = self.show_global_variables()
		self.global_status = self.show_global_status()
		self.slave_hosts = self.show_slave_hosts()
		self.version = self.mariadb_version()

	def run_query(self, query):
		"""
		Runs a mariadb query returning a dictionary of the resultset
		"""
		cursor = None
		try:
			cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(query)
		except Exception as excep:
			raise excep
		return cursor

	def mariadb_version(self):
		return re.sub("[^0-9^.]", "", self.run_query("SELECT VERSION() AS v").fetchall()[0]['v'])

	def show_slave_status(self):
		ss = None
		try:
			ss = self.run_query("SHOW ALL SLAVES STATUS").fetchall()
		except MySQLdb.Error as excep:
			if excep[0] == 1064:
				ss = self.run_query("SHOW SLAVE STATUS").fetchall() # MariaDB 5.5 <
			else:
				raise excep
		return ss

	def show_processlist(self, is_full=False):
		if is_full:
			query = "SHOW FULL PROCESSLIST"
		else:
			query = "SHOW PROCESSLIST"
		return self.run_query(query).fetchall()

	def show_master_status(self):
		return self.run_query("SHOW MASTER STATUS").fetchall()[0]

	def show_global_variables(self):
        	global_variables_dict = {}
                for gv_dict in self.run_query("SHOW GLOBAL VARIABLES").fetchall():
                        global_variables_dict[gv_dict["Variable_name"].lower()] = gv_dict["Value"]
                return global_variables_dict

	
	def show_global_status(self):
		global_status_dict = {}
		for gs_dict in self.run_query("SHOW GLOBAL STATUS").fetchall():
			global_status_dict[gs_dict["Variable_name"].lower()] = gs_dict["Value"] 
		return global_status_dict

	def stop_slave(self):
		s = False
		if self.run_query("STOP SLAVE"):
			s = True
		return s

	def start_slave(self):
		s = False
		if self.run_query("START SLAVE"):
			s = True
		return s

	def m_connection(self, hostname, port, username, password, database):
		return MySQLdb.connect(host=hostname, port=port, user=username, passwd=password, db=database);

	def is_master(self, strict=False):
		is_master = False
		if strict == False:
			if len(self.master_status) > 0:
				is_master = True
		else:
			if len(self.show_slave_hosts()) > 0:
				is_master = True
		return is_master

	def is_slave(self):
		is_slave = False
		if len(self.slave_status) > 0:
			is_slave = True
		return is_slave

	def is_multi_master_slave(self):
		is_multi_master_slave = False
		if len(self.slave_status) > 1:
			is_multi_master_slave = True
		return is_multi_master_slave

	def is_single_master_slave(self):
		is_single_master_slave = False
		if len(self.slave_status) == 1:
			is_single_master_slave = True
		return is_single_master_slave

	def is_slave_running(self, slave):
		slave_ok = False
		if slave["Slave_IO_Running"] == "Connecting":
			slave_name = slave["Connection_name"]
			slave_status = self.run_query("SHOW SLAVE '{0}' STATUS".format(slave_name))
		if slave["Slave_IO_Running"] == "Yes" and slave["Slave_SQL_Running"] == "Yes":
			slave_ok = True
		return slave_ok

	def is_using_gtid(self, slave):
		using_gtid = None
		if slave.get("Using_Gtid") == "No":
			using_gtid = False
		elif slave.get("Using_Gtid") in ["Slave_Pos", "Current_Pos"]:
			using_gtid = True
		elif "Using_Gtid" not in slave.keys():
			using_gtid = False
		return using_gtid		

	def show_slave_hosts(self):
		return self.run_query("SHOW SLAVE HOSTS").fetchall()

	def show_binary_logs(self):
		return self.run_query("SHOW BINARY LOGS").fetchall()

	def show_engines(self):
		return self.run_query("SHOW ENGINES").fetchall()

	def show_plugins(self):
		return self.run_query("SHOW PLUGINS").fetchall()

	def show_databases(self):
		return self.run_query("SHOW DATABASES").fetchall()

	

