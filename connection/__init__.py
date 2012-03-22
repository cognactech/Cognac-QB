import errors
import sys

class CQBConnectionDriver():

	_instances = {}

	@staticmethod
	def instance(instance_name = 'default', driver_type = 'mysql'):
		"""
		Returns an instance of driver_type
		"""
		if instance_name not in CQBConnectionDriver._instances:
			CQBConnectionDriver._instances[instance_name] = CQBConnectionDriver(driver_type)
			
		return CQBConnectionDriver._instances[instance_name]

	def __init__(self, driver_type = 'mysql'):
		self.driver_type = driver_type.lower()

		#try to import the driver
		try:
			module_name = "drivers.%s" % self.driver_type
			__import__(module_name)
			self.module = sys.modules[module_name]

			cls = getattr(self.module, "CQBConnectionDriver_%s" % self.driver_type)
			self.driver = cls()
		except:
			raise errors.CQBConnectionError("Driver %s not found" % self.driver_type)

	def connect(self, **kwargs):
		self.driver.connect(**kwargs)

	def set_db(self, name):
		self.driver.set_db(name)

	def query(self, query_text, replacements = ()):
		if not self.is_connected():
			raise errors.CQBConnectionError("Driver not connected.")

		return self.driver.query(query_text, replacements)

	def last_query(self):
		return self.driver.last_query()

	def last_error(self):
		return self.driver.last_error()

	def is_connected(self):
		return self.driver.is_connected()

if __name__ == '__main__':
	c = CQBConnectionDriver.instance('mysql', 'mysql')
	c.connect(user='root',passwd='kaizer')
	c.set_db("youcallmd");
	print c.query("SELECT * FROM users WHERE id = %s LIMIT 1", 1455)
	#print c.last_error()
	#print c.last_query()
	