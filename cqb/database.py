import sqlite3

class CQBDatabase(object):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(profile='default'):
		''' Returns a new instance or previosly generated one if found '''
		if profile in self.instances:
			return self.instances[profile]
		self.instances[profile] = CQBDatabase(profile)
		return self.instances[profile]

	def __init__(self, profile, con_params):
		''' '''
		try:
			conn = sqlite3.connect('/Users/ncurtis/qcb-data')
			
			c = conn.cursor()
			c.execute('SELECT * FROM connections')
			
			self.profiles = []
			for row in c:
				self.profiles.append(row)
			
			dialog = wx.SingleChoiceDialog(self.queryEditorPanel, "Select a database profile", "Welcome", [x[5] for x in self.profiles])
			
			if dialog.ShowModal() == wx.ID_OK:
				aprofile = dialog.GetSelection()
				
				# create instance of new connection
				self.con = connection.CQBConnection.instance(self.profiles[aprofile][0], 'mysql')
				self.con.connect(host=self.profiles[aprofile][1], user=self.profiles[aprofile][2], passwd=self.profiles[aprofile][3])
				
				# list databases that are available
				results = self.con.query('SHOW DATABASES')
				
				profile_dbs = [db[0] for db in results[1]]
				
				self.dbBrowserPanel.initDBList(self.profiles[aprofile][5], profile_dbs)
				del results

			else:
				self.Close()
			
			dialog.Destroy()
			
		except errors.CQBConnectionError, exc:
			result = wx.MessageBox(str(exc), "Connection Failed", wx.OK | wx.ICON_ERROR)

		except Exception, exc:
			result = wx.MessageBox(str(exc), "Application Error", wx.OK | wx.ICON_ERROR)