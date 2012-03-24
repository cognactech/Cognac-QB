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

	def __init__ (self, id, message=''):
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

	def __init__(self, query='', *args, **kwargs):
		""" """
		super(QueryThread, self).__init__(*args, **kwargs)
		self.query = query
		self.start()

	def run(self):
		""" """
		try:
			event = "ResultEventLoad"
			data = self.parent.parent.con.query(self.query)
		except Exception, exc:
			event = "QueryEventError"
			data = str(exc)
		finally:
			wx.CallAfter(Publisher().sendMessage, event, data)

class Query(wx.Panel):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(parent, id):
		''' Returns a new instance or previosly generated one if found '''
		if id in Query.instances:
			return Query.instances[id]
		Query.instances[id] = Query(parent, id)
		return Query.instances[id]

	def __init__ (self, parent, id, *args, **kwargs):
		''' '''	
		super(Query, self).__init__(*args, **kwargs)
		
		self.Bind(EVT_CQB_QRY_RUN, self.runQuery, self)
		Publisher().subscribe(self.queryEventError, "QueryEventError")

		self.queryEditor = view.QueryEditor(self)

		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.queryEditor, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
	
	def runQuery(self, e):
		''' '''
		queryThread = QueryThread(self.parent, self.queryEditor.GetValue())
		e.Skip()
	
	def queryEventError(self, e):
		''' '''
		result = wx.MessageBox(e.message, "Query Failed", wx.OK | wx.ICON_ERROR)
