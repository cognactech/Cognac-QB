#! /usr/bin/python

import wx

class CQBQueryEvent(wx.PyCommandEvent):
	def __init__ (self, evtType, id):
		super(CQBQueryEvent, self).__init__(evtType, id)
	
EVT_CQB_QUERY_ID = wx.NewEventType()
EVT_CQB_QUERY = wx.PyEventBinder(EVT_CQB_QUERY_ID, 1)

class CQBQueryEventError(CQBQueryEvent):
	def __init__ (self, id):
		super(CQBQueryEventError, self).__init__(EVT_CQB_QUERY_ERR_ID, id)

EVT_CQB_QUERY_ERR_ID = wx.NewEventType()
EVT_CQB_QUERY_ERR = wx.PyEventBinder(EVT_CQB_QUERY_ERR_ID, 1)

class CQBQueryEventRefresh(CQBQueryEvent):
	def __init__ (self, id):
		super(CQBQueryEventRefresh, self).__init__(EVT_CQB_QRY_RFRSH_ID, id)

EVT_CQB_QRY_RFRSH_ID = wx.NewEventType()
EVT_CQB_QRY_RFRSH = wx.PyEventBinder(EVT_CQB_QRY_RFRSH_ID, 1)

class CQBQueryEventRun(CQBQueryEvent):
	def __init__ (self, id):
		super(CQBQueryEventRun, self).__init__(EVT_CQB_QRY_RUN_ID, id)

EVT_CQB_QRY_RUN_ID = wx.NewEventType()
EVT_CQB_QRY_RUN = wx.PyEventBinder(EVT_CQB_QRY_RUN_ID, 1)

class CQBQueryEventStop(CQBQueryEvent):
	def __init__ (self, id):
		super(CQBQueryEventStop, self).__init__(EVT_CQB_QRY_STOP_ID, id)

EVT_CQB_QRY_STOP_ID = wx.NewEventType()
EVT_CQB_QRY_STOP = wx.PyEventBinder(EVT_CQB_QRY_STOP_ID, 1)
