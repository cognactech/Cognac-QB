#! /usr/bin/python

import wx
import threading

import model, view

class Browser(wx.Panel):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(parent, id):
		''' Returns a new instance or previosly generated one if found '''
		if id in Browser.instances:
			return Browser.instances[id]
		Browser.instances[id] = Query(parent, id)
		return Browser.instances[id]

	def __init__ (self, parent, id, *args, **kwargs):
		''' '''	
		super(Query, self).__init__(*args, **kwargs)
		
		self.tree = view.BrowserTree(self)

		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.tree, 1, wx.EXPAND)
		self.SetSizer(self.sizer)

	def OnExpandItem(self, e):
		''' '''
		try:
			data = self.GetPyData(e.GetItem())
			
			if data.data['database'] == False and data.data['table'] == False:
				print 'pass'
				
			elif data.data['database'] == True:
				self.parent.useDatabase('youcallmd')
				tables = self.parent.getTables()
		
				data = CQBData(data={'database': False, 'table': True})
				for table in tables[1]:
					item = self.AppendItem(e.GetItem(), table[0], data=wx.TreeItemData(data))
					self.SetItemHasChildren(item, True)
	
			elif data.data['database'] == False:
				print 'open table'
		
		except Exception, exc:
			result = wx.MessageBox(str(exc), "Database Error", wx.OK | wx.ICON_ERROR)
		finally:
			e.Skip()

	def OnCollapseItem(self, e):
		''' '''
		
		if self.__collapsing:
			e.Veto()
		else:
			self.__collapsing = True
			pass
			self.__collapsing = False

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
