import wx

class CQBQueryEvent(wx.PyCommandEvent):
	def __init__ (self, evtType, id):
		super(__init__, self, evtType, id)
	
CQBQueryEvent_ID = wx.NewEventType()
CQBQueryEvent = wx.PyEventBinder(wx.NewEventType(), 1)

class CQBQueryEventError(CQBQueryEvent):
	def __init__ (self, evtType, id):
		super(__init__, self, evtType, id)

CQBQueryEventError_ID = wx.NewEventType()
CQBQueryEventError = wx.PyEventBinder(wx.NewEventType(), 1)

class CQBQueryEventRefresh(CQBQueryEvent):
	def __init__ (self, evtType, id):
		super(__init__, self, evtType, id)

CQBQueryEventRefresh_ID = wx.NewEventType()
CQBQueryEventRefresh = wx.PyEventBinder(wx.NewEventType(), 1)

class CQBQueryEventResults(CQBQueryEvent):
	def __init__ (self, evtType, id):
		super(__init__, self, evtType, id)

CQBQueryEventResults_ID = wx.NewEventType()
CQBQueryEventResults = wx.PyEventBinder(wx.NewEventType(), 1)
