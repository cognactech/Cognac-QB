#! /usr/bin/python

import wx

from threading import Thread
from wx.lib.pubsub import Publisher

import model, view

class QueryEvent(wx.PyCommandEvent):
	''' '''

	def __init__ (self, evtType, id):
		''' '''
		super(QueryEvent, self).__init__(evtType, id)

EVT_QEE_ID = wx.NewEventType()
EVT_QEE = wx.PyEventBinder(EVT_QEE_ID, 1)

class QueryEventRun(QueryEvent):
	''' '''

	def __init__ (self, id):
		''' '''
		super(ResultEventLoad, self).__init__(EVT_QEE_RUN_ID, id)

EVT_QEE_RUN_ID = wx.NewEventType()
EVT_QEE_RUN = wx.PyEventBinder(EVT_QEE_RUN_ID, 1)

class QueryEventError(QueryEvent):
	''' '''

	def __init__ (self, id, message):
		''' '''
		super(QueryEventError, self).__init__(EVT_QEE_ERR_ID, id)
		self.message = message

EVT_QEE_ERR_ID = wx.NewEventType()
EVT_QEE_ERR = wx.PyEventBinder(EVT_QEE_ERR_ID, 1)

class QueryEventStop(QueryEvent):
	''' '''

	def __init__ (self, id):
		''' '''
		super(ResultEventLoad, self).__init__(EVT_QEE_STOP_ID, id)

EVT_QEE_STOP_ID = wx.NewEventType()
EVT_QEE_STOP = wx.PyEventBinder(EVT_QEE_STOP_ID, 1)

class QueryThread(Thread):
	''' '''

	def __init__(self, frame=None, query='', *args, **kwargs):
		""" """
		super(QueryThread, self).__init__(*args, **kwargs)
		self.frame = frame
		self.query = query
		self.start()

	def run(self):
		""" """
		try:
			event = "ResultEventLoad"
			data = self.frame.helper.query(self.query)
		except Exception, exc:
			event = "QueryEventError"
			data = exc
		finally:
			wx.CallAfter(Publisher().sendMessage, event, data)

class Query(wx.Panel):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(parent, id, frame=None, *args, **kwargs):
		''' Returns a new instance or previosly generated one if found '''
		if id in Query.instances:
			return Query.instances[id]
		Query.instances[id] = Query(parent, id, frame=frame, *args, **kwargs)
		return Query.instances[id]

	def __init__ (self, parent, id, frame=None, *args, **kwargs):
		''' '''	
		super(Query, self).__init__(parent, id, *args, **kwargs)
		
		self.frame = frame
		self.SetBackgroundColour(wx.Colour(0,0,0))
		
		self.Bind(EVT_QEE_RUN, self.runQuery, self)
		Publisher().subscribe(self.queryEventError, "QueryEventError")

		self.queryEditor = view.QueryEditor(self, wx.ID_ANY)

		self.sizer = wx.GridSizer()
		self.sizer.Add(self.queryEditor, 1, wx.EXPAND|wx.ALL, 10)
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
	
	def runQuery(self, e):
		''' '''
		queryThread = QueryThread(self.frame, self.queryEditor.editorCtrl.GetValue())
		e.Skip()

	def cancelQuery(self, e):
		''' '''
		e.Skip()
	
	def queryEventError(self, exc):
		''' '''
		wx.MessageBox(str(exc), "Query Failed", wx.OK | wx.ICON_ERROR)
