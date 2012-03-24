import connection.errors as CQBConnectionErrors
#try to import MySQL
try:
	import pgdb
except:
	raise CQBConnectionErrors.CQBConnectionError("Unable to load pgdb module. Please install pgdb.")
import time

class CQBConnectionDriver_mysql():
	
	#init variables
	_connection = None
	_last_error = None
	_last_query = None

	def __init__(self):
		pass

	def connect(self, **kwargs):
		try:
			self._connection = pgdb.connect(**kwargs)
		except pgdb.Error, e:
			self._last_error = e.message
			raise CQBConnectionErrors.CQBConnectionError(e.message)

	def set_db(self, name):
		try:
			self._connection.select_db(name)
		except pgdb.Error, e:
			self._last_error = e.message
			raise CQBConnectionErrors.CQBConnectionQueryError(0, e.message)

	def query(self, query_text, replacements = ()):
		#force tuple
		if not isinstance(replacements, (list, tuple)):
			replacements = (replacements)

		cursor = self._connection.cursor()

		try:
			start_time = time.time()
			cursor.execute(str(query_text), replacements)
			end_time = time.time()
			self._connection.commit()
		except pgdb.Error, e:
			self._last_error = e.message
			raise CQBConnectionErrors.CQBConnectionQueryError(0, e.message)

		self._last_query = cursor._last_executed

		#execution time
		execution_time = end_time - start_time

		#build the column names
		field_names = []
		for field in cursor.description:
			field_names.append(field[0])

		results = []

		row = cursor.fetchone()
		while row is not None:
			results.append(row)
			row = cursor.fetchone()

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
		if self._connection is None:
			return False
		try:
			result = self._connection.stat()
			if result == 'MySQL server has gone away':
				return False
		except:
			return False

		return True