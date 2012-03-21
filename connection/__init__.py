#! /usr/bin/python

class CQBConnection():
	_connections = {}

	def __init__(self):
		#populate list of connections, currently the list is dynamic and none are saved.
		self.connection = None

	def store_connection(self, name):
		"""
		Store the connection for later use.
		Currently only adds it the connection 
		"""
		CQBConnection._connections[name] = self

		return self

	def get_connection(self, name):
		"""
		Grabs the connection stored.
		"""
		if name in CQBConnection._connections:
			return CQBConnection._connections[name]
		else:
			return None

	def connect(self, DB, connection_name=None, user=None, passwd=None, host = 'localhost', port = 3306, **kwargs):
		"""
		Connects to the database specified and stores it.
		If a connection with that name already exists, returns that connection.
		"""
		connection = self.get_connection(connection_name)

		if connection is None:
			self.connection = DB.connect(user=user, passwd=passwd, host=host, port=port, **kwargs)
			self.store_connection(connection_name)
			return self
		else:
			return connection

	def set_database(self, name):
		if self.connection is not None:
			self.query("USE `%s`;" % str(name))
		return self

	def query(self, query_text, replacements = None):
		cursor = self.connection.cursor()
		
		if replacements is None:
			cursor.execute(query_text)
		else:
			cursor.execute(query_text, replacements)

		return cursor.fetchall()
	