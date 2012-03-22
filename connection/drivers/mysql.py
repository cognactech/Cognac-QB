import MySQLdb
#try to import errors
import errors as CQBConnectionErrors

class CQBConnectionDriver_mysql():
	
	#init variables
	_connection = None
	_last_error = None
	_last_error_number = None
	_last_query = None

	def __init__(self):
		pass

	def connect(self, **kwargs):
		try:
			self._connection = MySQLdb.connect(**kwargs)
		except MySQLdb.Error, e:
			self._last_error = e.args[1]
			self._last_error_number = e.args[0]
			raise CQBConnectionErrors.CQBConnectionError("Unable to connect to MySQL database.")

	def set_db(self, name):
		try:
			self._connection.select_db(name)
		except MySQLdb.Error, e:
			self._last_error = e.args[1]
			self._last_error_number = e.args[0]
			raise CQBConnectionErrors.CQBConnectionQueryError(e.args[0], e.args[1])

	def query(self, query_text, replacements = ()):
		#check for active connection
		if not isinstance(replacements, (list, tuple)):
			replacements = (replacements)

		cursor = self._connection.cursor()

		try:
			cursor.execute(str(query_text), replacements)
		except MySQLdb.Error, e:
			self._last_error = e.args[1]
			self._last_error_number = e.args[0]
			raise CQBConnectionErrors.CQBConnectionQueryError(e.args[0], e.args[1], str(query_text) % replacements)

		self._last_query = cursor._last_executed

		#build the column names
		field_names = []
		for field in cursor.description:
			field_names.append(field[0])

		return (field_names, cursor.fetchall())

	def last_query(self):
		return self._last_query

	def last_error(self):
		return self._last_error_number, self._last_error

	def is_connected(self):
		if self._connection is None:
			return False
		try:
			result = self._connection.stat()
			if result == 'MySQL server has gone away':
				return False
		except:
			return False

		return True