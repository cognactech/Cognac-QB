import connection
from connection import errors
import sqlite3

class CQBHelper(object):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(profile, con_params):
		''' Returns a new instance or previosly generated one if found '''
		if profile in CQBHelper.instances:
			return CQBHelper.instances[profile]
		CQBHelper.instances[profile] = CQBHelper(profile, con_params)
		return CQBHelper.instances[profile]

	def __init__(self, profile, con_params):
		''' '''
		self.profile = profile

		self.host = con_params['host']
		self.user = con_params['user']
		self.passwd = con_params['passwd']
		self.port = con_params['port']
		self.driver = 'mysql'

		self.con = connection.CQBConnection.instance(self.profile, self.driver)

	def reconnect (self):
		''' '''
		if not self.con.is_connected():
			if self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port):
				return True
		return False

	def use (self, db_name):
		''' '''
		if not self.con.is_connected():
			if self.con.set_db(db_name):
				return True
		return False
		
	def tables (self, db_name=None):
		''' '''	
		if not self.con.is_connected():
			if db_name != None:
				self.use(db_name)
			results = self.con.query('SHOW TABLES')
			return results
		return False

	def columns (self, table_name):
		if not self.con.is_connected():
			results = self.con.query('SHOW COLUMNS FROM %s' % table_name)
			return results
		return False

class CQBDatabase(object):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(profile='default'):
		''' Returns a new instance or previosly generated one if found '''
		if profile in CQBDatabase.instances:
			return CQBDatabase.instances[profile]
		CQBDatabase.instances[profile] = CQBDatabase(profile)
		return CQBDatabase.instances[profile]

	def __init__(self, profile):
		''' '''
		conn = sqlite3.connect('/Users/ncurtis/CognacQB/qcb-data')
		self.cursor = conn.cursor()

	def profiles(self):
		self.cursor.execute('SELECT * FROM connections')
		return self.cursor
