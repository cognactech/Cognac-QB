import connection
import sqlite3

class CQBHelper(object):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(id, con_params):
		''' Returns a new instance or previosly generated one if found '''
		if id in CQBHelper.instances:
			return CQBHelper.instances[id]
		CQBHelper.instances[id] = CQBHelper(id, con_params)
		return CQBHelper.instances[id]

	def __init__(self, id, con_params):
		''' '''
		self.id = int(id)
		self.name = con_params['name']
		self.host = con_params['host']
		self.user = con_params['user']
		self.passwd = con_params['passwd']
		self.port = int(con_params['port'])
		self.driver = 'mysql'

		self.con = connection.CQBConnection.instance(self.id, self.driver)

	def query(self, query):
		''' '''
		''' '''	
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			results = self.con.query(query)
			return results

		return False

	def reconnect(self):
		''' '''
		if self.con.is_connected() == True:
			return True
		else:
			if self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port):
				return True
		return False

	def use(self, db_name):
		''' '''
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			if self.con.set_db(db_name):
				return True
		return False
		
	def db_table_tree(self):
		''' '''
		tree = {}
		results = self.databases()
		for database in results[1]:
			tables = []
			tresults = self.tables(database[0])
			for table in tresults[1]:
				tables.append(table[0])
			tree[database[0]] = tables
		return tree

	def databases(self):
		''' '''	
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			results = self.con.query('SHOW DATABASES')
			return results
		return False

	def tables(self, db_name=None):
		''' '''	
		if db_name != None:
			self.use(db_name)
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			results = self.con.query('SHOW TABLES')
			return results
		return False

	def columns (self, table_name):
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			#results = self.con.query(SHOW COLUMNS FROM ?' % table_name)
			return []
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
