import unittest, time

execfile('../lib/mylib.py')

class TestMyLibMethods(unittest.TestCase):

	def testPingLocalhost(self):
		net = NetworkTools()
		self.assertTrue(net.ping('localhost'))

	def testPingUnknownHost(self):
		net = NetworkTools()
		status = net.ping('zxcvbnm')
		self.assertFalse(status)

	def testMariaDBConnection(self):
		mariadb_instance = PyMaria()
		self.assertTrue(mariadb_instance.connection is not None)
		self.assertTrue("_mysql.connection" in str(mariadb_instance.connection))

	def testMariaDBVersion(self):
		mariadb_instance = PyMaria()
		self.assertTrue(len(mariadb_instance.version) > 4)
		self.assertTrue("10" in mariadb_instance.version)
		self.assertTrue("." in mariadb_instance.version)

	def testMariaDBShowSlaveStatus(self):
		mariadb_instance = PyMaria()
		slave_status  = mariadb_instance.show_slave_status()
		self.assertEqual(slave_status["Master_Host"], "localhost")
		self.assertEqual(slave_status["Slave_SQL_Running"], "Yes")
		self.assertEqual(slave_status["Slave_IO_Running"], "Yes")

	def testShowProcessList(self):
		mariadb_instance = PyMaria()
		pl = mariadb_instance.show_processlist()
		#print result_list.fetchall()[0]
		first_record = pl[0]
		self.assertTrue(first_record['Id'] > 0)
		self.assertTrue(first_record['User'] == 'pytest')
	
	def testMariaDBShowMasterStatus(self):
		mariadb_instance = PyMaria()
		master_status = mariadb_instance.show_master_status()
		self.assertTrue("mysqld-bin" in master_status['File']) 	
	
	def testMariaDBGlobalVariables(self):
		mariadb_instance = PyMaria()
		global_variables = mariadb_instance.show_global_variables()
		self.assertTrue(len(global_variables) > 250)

	def testMariaDBGlobalStatus(self):
		mariadb_instance = PyMaria()
		global_status = mariadb_instance.show_global_status()
		self.assertTrue(len(global_status) > 250)

	def testMariaDBStopSlave(self):
		mariadb_instance = PyMaria()
		if mariadb_instance.is_slave_running() == False:
			mariadb_instance.start_slave()
		self.assertTrue(mariadb_instance.stop_slave())
		mariadb_instance.start_slave()

	def testMariaDBStartSlave(self):
		mariadb_instance = PyMaria()
		if mariadb_instance.is_slave_running():
			mariadb_instance.stop_slave()
		self.assertTrue(mariadb_instance.start_slave())

	def testMariaDBIsMaster(self):
		mariadb_instance = PyMaria()
		self.assertTrue(mariadb_instance.is_master())

	def testMariaDBIsSlave(self):
		mariadb_instance = PyMaria()
		self.assertTrue(mariadb_instance.is_slave())

	def testMariaDBIsSlaveRunning(self):
		mariadb_instance = PyMaria()
		self.assertTrue(mariadb_instance.is_slave_running())

	def testMariaDBShowSlaveHosts(self):
		mariadb_instance = PyMaria()
		self.assertTrue(len(mariadb_instance.slave_hosts) == 1)
		self.assertTrue(mariadb_instance.slave_hosts[0]['Server_id'] == 2)
		self.assertTrue(mariadb_instance.slave_hosts[0]['Master_id'] == 1)
		self.assertTrue(mariadb_instance.slave_hosts[0]['Port'] == 3307)

	def testMariaDBShowDatabases(self):
		mariadb_instance = PyMaria()
		self.assertTrue(len(mariadb_instance.show_databases()) > 0)
		self.assertTrue('mysql' in str(mariadb_instance.show_databases()))
	
	def testIsPortOpen(self):
		net = NetworkTools()
		self.assertTrue(net.is_port_open("127.0.0.1", 3306))
		self.assertTrue(net.is_port_open("127.0.0.1", 3307))
		self.assertFalse(net.is_port_open("127.0.0.1", 3308))

# We call _setUp and _tearDown only once to make sure the slave has been started
def _setUp():
	mariadb_instance = PyMaria()
	if mariadb_instance.is_slave_running() == False:
		mariadb_instance.start_slave()
		print "I started the slave thread on the master..."

def _teardown(self):
	mariadb_instance = PyMaria()
	if mariadb_instance.is_slave_running == False:
		mariadb_instance.start_slave()
		print "I started the slave thread on the master..."

if __name__ == '__main__':
	_setUp()
	unittest.main()
	_tearDown()
