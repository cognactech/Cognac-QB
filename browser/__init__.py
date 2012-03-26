#! /usr/bin/python

import wx

import model
import view

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
		#self.SetBackgroundColour(wx.Colour(0,0,0))

		dbs = self.frame.helper.databases()

		self.tree = view.BrowserTree(self, databases=dbs[1])

		self.tree.build(self.frame.helper.name, self.frame.helper.db_table_tree())

		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.tree, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
