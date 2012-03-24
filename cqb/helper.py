import connection

class CQBHelper(object):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(profile, con_params):
		''' Returns a new instance or previosly generated one if found '''
		if profile in self.instances:
			return self.instances[profile]
		self.instances[profile] = CQBHelper(profile, con_params)
		return self.instances[profile]

	def __init__(self, profile, con_params):
		''' '''
		self.profile = profile

		self.host = con_params['host']
		self.user = con_params['user']
		self.passwd = con_params['passwd']
		self.port = con_params['port']
		self.driver = con_params['driver']

		self.con = connection.Connection.instance(self.profile, self.driver)

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
			if db_name != None
				self.use(db_name)
			results = self.con.query('SHOW TABLES')
			return results
		return False

	def columns (self, table_name):
		if not self.con.is_connected():
			results = self.con.query('SHOW COLUMNS FROM %s' % table_name)
			return results
		return False