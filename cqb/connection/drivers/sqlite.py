#try to import sqlite3
try:
	import sqlite3
except:
	raise CQBConnectionErrors.CQBConnectionError("Unable to load sqlite3 module. Please install sqlite3.")
import time

class CQBConnectionDriver_sqlite():
	
	#init variables
	_connection = None
	_last_error = None
	_last_error_number = None
	_last_query = None

	def __init__(self):
		pass

	def connect(self, **kwargs):
		try:
			self._connection = sqlite3.connect(**kwargs)
		except sqlite3.Error, e:
			self._last_error = e.args[0]
			raise CQBConnectionErrors.CQBConnectionError("Unable to connect to SQLite database.")

	def set_db(self, name):
		try:
			self._connection = sqlite3.connect(name)
		except sqlite3.Error, e:
			self._last_error = e.args[0]
			self._last_error_number = 0
			raise CQBConnectionErrors.CQBConnectionError(e.args[0])

	def query(self, query_text, replacements = ()):
		#check for active connection
		if not isinstance(replacements, (list, tuple)):
			replacements = (replacements)

		cursor = self._connection.cursor()

		try:
			start_time = time.time()
			cursor.execute(str(query_text), replacements)
			end_time = time.time()
			self._connection.commit()
		except sqlite3.Error, e:
			self._last_error = e.args[0]
			raise CQBConnectionErrors.CQBConnectionQueryError(0, e.args[1], str(query_text) % replacements)

		self._last_query = cursor._last_executed

		#execution time
		execution_time = end_time - start_time

		#build the column names
		field_names = []
		for field in cursor.description:
			field_names.append(field[0])

		results = []

		for row in cursor:
			results.append(row)

		return (field_names, results, execution_time)

	def explain(self, query_text, replacements = ()):
		#just rewrite query_text and return self.query
		query_text = "EXPLAIN %s" % str(query_text)
		return self.query(query_text, replacements)

	def last_query(self):
		return self._last_query

	def last_error(self):
		return self._last_error_number, self._last_error

	def is_connected(self):
		"""
		SQLite can't technically disconnect.
		"""
		if self._connection is None:
			return False

		return True