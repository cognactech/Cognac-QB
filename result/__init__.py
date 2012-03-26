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

class Result(wx.Panel):
	''' '''

	instances = {}
	@staticmethod
	def instance(parent, id, *args, **kwargs):
		''' Returns a new instance or previosly generated one if found '''
		if id in Result.instances:
			return Result.instances[id]
		Result.instances[id] = Result(parent, id, *args, **kwargs)
		return Result.instances[id]

	def __init__ (self, parent, id, frame=None, *args, **kwargs):
		''' '''
		super(Result, self).__init__(parent, id, *args, **kwargs)
		
		self.frame = frame
		
		#self.SetBackgroundColour(wx.Colour(0,0,0))

		Publisher().subscribe(self.processResultGrid, "ResultEventLoad")

		self.sizer = wx.BoxSizer()
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)

	def processResultList(self, data):
		''' '''
		field_names = data.data[0]
		results = data.data[1]
		execution_time = data.data[2]
		query = data.data[3]

		try:
			self.grid.ClearGrid()
			self.grid.SetTable(table)
			self.grid.ForceRefresh()
		except:
			self.grid = view.ResultList(self, wx.ID_ANY, field_names=field_names, results=results)
			self.sizer.Add(self.grid, 1, wx.EXPAND)

		self.frame.showResults(query, len(results), execution_time)

	def processResultGrid(self, data):
		''' '''
		field_names = data.data[0]
		results = data.data[1]
		execution_time = data.data[2]
		query = data.data[3]

		table = model.ResultGridTable(field_names=field_names, results=results)

		try:
			self.grid.ClearGrid()
			self.grid.SetTable(table)
			self.grid.ForceRefresh()
		except:
			self.grid = view.ResultGrid(self, wx.ID_ANY, table=table)
			self.sizer.Add(self.grid, 1, wx.EXPAND)

		self.frame.showResults(query, len(results), execution_time)
