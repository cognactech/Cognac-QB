#! /usr/bin/python

import wx, time

from threading import Thread
from wx.lib.pubsub import Publisher

from cqb import CQBHelper

import model
import view

class BrowserThread(Thread):
	''' '''

	def __init__(self, con_params, *args, **kwargs):
		""" """
		super(BrowserThread, self).__init__(*args, **kwargs)
		self.con_params = con_params
		self.start()

	def run(self):
		''' '''
		try:
			event = "BrowserEventLoad"
			helper = CQBHelper.instance(time.clock(), self.con_params)
			data = helper.db_table_tree()
		except Exception, exc:
			event = "BrowserEventError"
			data = exc
		finally:
			wx.CallAfter(Publisher().sendMessage, event, data)

class Browser(wx.Panel):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(parent, id, *args, **kwargs):
		''' Returns a new instance or previously generated one if found '''
		if id in Browser.instances:
			return Browser.instances[id]
		Browser.instances[id] = Browser(parent, id, *args, **kwargs)
		return Browser.instances[id]

	def __init__ (self, parent, id, frame=None, *args, **kwargs):
		''' '''	
		super(Browser, self).__init__(parent, id, *args, **kwargs)

		self.frame = frame
		#self.SetBackgroundColour(wx.Colour(0,0,0))
		
		Publisher().subscribe(self.browserEventLoad, "BrowserEventLoad")
		Publisher().subscribe(self.browserEventError, "BrowserEventError")

		dbs = self.frame.helper.databases()

		self.tree = view.BrowserTree(self)

		BrowserThread(self.frame.helper.get_params())
		
		#data = self.frame.helper.db_table_tree()
		#self.tree.build(self.frame.helper.name, data)

		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.tree, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
	
	def browserEventLoad(self, data):
		''' '''
		self.tree.build(self.frame.helper.name, data.data)
	
	def browserEventError(self, exc):
		''' '''
		wx.MessageBox(str(exc), "Browser Failed", wx.OK | wx.ICON_ERROR)
