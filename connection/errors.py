class CQBConnectionError(Exception):
	
	def __init__(self, message=''):
		self.value = message

	def __str__(self):
		return str(self.value)

class CQBConnectionQueryError(CQBConnectionError):
	
	def __init__(self, error_number, message, query=''):
		self.error_number = error_number
		self.message = message
		self.query = query

	def __str__(self):
		return "%s: %s\nQuery: %s" % (self.error_number, self.message, self.query)