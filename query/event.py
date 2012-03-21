import wx

class CQBQueryEvent(wx.PyCommandEvent):
	def __init__ (self, evtType, id):
		super(__init__, self, evtType, id)
	
EVT_CQB_QUERY_ID = wx.NewEventType()
EVT_CQB_QUERY = wx.PyEventBinder(EVT_CQB_QUERY_ID, 1)

class CQBQueryEventError(CQBQueryEvent):
	def __init__ (self, evtType, id):
		super(__init__, self, evtType, id)

EVT_CQB_QUERYERROR_ID = wx.NewEventType()
EVT_CQB_QUERYERROR = wx.PyEventBinder(EVT_QUERYERROR_ID, 1)

class CQBQueryEventRefresh(CQBQueryEvent):
	def __init__ (self, evtType, id):
		super(__init__, self, evtType, id)

EVT_CQB_QRY_RFRSH_ID = wx.NewEventType()
EVT_CQB_QRY_RFRSH = wx.PyEventBinder(EVT_QRY_RFRSH_ID, 1)

class CQBQueryEventResults(CQBQueryEvent):
	def __init__ (self, evtType, id):
		super(__init__, self, evtType, id)

EVT_CQB_QRY_RSLTS_ID = wx.NewEventType()
EVT_CQB_QRY_RSLTS = wx.PyEventBinder(EVT_QRY_RSLTS_ID, 1)
