#! /usr/bin/python

import wx

from threading import Thread
from wx.lib.pubsub import Publisher

import model, view

class ResultEvent(wx.PyCommandEvent):
	''' '''

	def __init__ (self, evtType, id):
		''' '''
		super(ResultEvent, self).__init__(evtType, id)

EVT_QRE_QRY_ID = wx.NewEventType()
EVT_QRE_QRY = wx.PyEventBinder(EVT_QRE_QRY_ID, 1)

class ResultEventLoad(ResultEvent):
	''' '''

	def __init__ (self, id, field_names=[], results=[], execution_time=0):
		''' '''
		super(ResultEventLoad, self).__init__(EVT_QRE_ERR_ID, id)
		self.field_names = field_names
		self.results = results
		self.execution_time = execution_time

EVT_QRE_ERR_ID = wx.NewEventType()
EVT_QRE_ERR = wx.PyEventBinder(EVT_QRE_ERR_ID, 1)

class ResultEventError(ResultEvent):
	''' '''

	def __init__ (self, id, message):
		''' '''
		super(ResultEventError, self).__init__(EVT_QRE_ERR_ID, id)
		self.message = message

EVT_QRE_ERR_ID = wx.NewEventType()
EVT_QRE_ERR = wx.PyEventBinder(EVT_QRE_ERR_ID, 1)

class ResultThread(Thread):
	''' '''

	def __init__(self, *args, **kwargs):
		""" """
		super(ResultThread, self).__init__(*args, **kwargs)
		self.start()

	def run(self):
		""" """
		pass

class Result(wx.Panel):
	''' '''

	instances = {}
	@staticmethod
	def instance(parent, id):
		''' Returns a new instance or previosly generated one if found '''
		if id in Result.instances:
			return Result.instances[id]
		Result.instances[id] = Query(parent, id)
		return Result.instances[id]

	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(Result, self).__init__(parent, -1, *args, **kwargs)
		
		Publisher().subscribe(self.processResult, "ResultEventLoad")

		self.grid = view.ResultGrid(self, field_names=field_names, results=results)

		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.grid, 1, wx.EXPAND)
		self.SetSizer(self.sizer)

	def processResult(self, data):
		''' '''
		self.grid.ClearGrid()
		table = ResultTable(data[0], data[1])
		self.grid.SetTable(table)
		self.ForceRefresh()
