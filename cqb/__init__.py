import connection
import sqlite3
import time

class CQBHelper(object):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(id, con_params):
		''' Returns a new instance or previously generated one if found '''
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

	def query(self, query, benchmark=False):
		''' '''
		if benchmark == True: start = time.clock()
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			results = self.con.query(query)
			if benchmark == True: end = time.clock(); print end - start
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
		
	def db_table_tree(self, benchmark=False):
		''' '''
		tree = {}
		if benchmark == True: start = time.clock()
		results = self.databases(benchmark=False)
		for database in results[1]:
			tables = []
			tresults = self.tables(database[0], benchmark=False)
			for table in tresults[1]:
				tables.append(table[0])
			tree[database[0]] = tables
		if benchmark == True: end = time.clock(); print end - start
		return tree

	def databases(self, benchmark=False):
		''' '''	
		if benchmark == True: start = time.clock()
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			results = self.con.query('SHOW DATABASES')
			if benchmark == True: end = time.clock(); print end - start
			return results
		return False

	def tables(self, db_name=None, benchmark=False):
		''' '''	
		if benchmark == True: start = time.clock()
		if db_name != None:
			self.use(db_name)
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			results = self.con.query('SHOW TABLES')
			if benchmark == True: end = time.clock(); print end - start
			return results
		return False

	def columns (self, table_name, benchmark=False):
		if benchmark == True: start = time.clock()
		if self.con.is_connected() != True:
			self.con.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
		if self.con.is_connected() == True:
			#results = self.con.query(SHOW COLUMNS FROM ?' % table_name)
			if benchmark == True: end = time.clock(); print end - start
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
		start = time.clock()
		self.cursor.execute('SELECT * FROM connections')
		end = time.clock(); print end - start
		return self.cursor
