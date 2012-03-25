#! /usr/bin/python

import wx

import model, view

class Browser(wx.Panel):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(parent, id, *args, **kwargs):
		''' Returns a new instance or previosly generated one if found '''
		if id in Browser.instances:
			return Browser.instances[id]
		Browser.instances[id] = Browser(parent, id, *args, **kwargs)
		return Browser.instances[id]

	def __init__ (self, parent, id, frame=None, *args, **kwargs):
		''' '''	
		super(Browser, self).__init__(parent, id, *args, **kwargs)
		
		self.frame = frame
		
		dbs = self.frame.helper.databases()

		self.tree = view.BrowserTree(self, databases=dbs)

		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.tree, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)

	databases = []
	def initDBList(self, connection_name, databases):
		''' '''
		self.databases = databases
		
		root = self.AddRoot(connection_name)
		self.SetItemData(root, data=wx.TreeItemData(CQBData(data={'database': False, 'table': False})))
		
		data = CQBData(data={'database': True, 'table': False})
		for db in self.databases:
			if db != None:
				item = self.AppendItem(root, db, data=wx.TreeItemData(data))
				self.SetItemHasChildren(item, True)
		
		self.SetItemHasChildren(root, True)
