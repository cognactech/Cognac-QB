#! /usr/bin/python

import wx
import __init__ as query
import event as CQBEvent

class CQBQueryController(wx.EvtHandler):
	''' '''
	
	object_id = None
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		
		super(CQBQueryController, self).__init__(*args, **kwargs)
		
		self.parent = parent
		self.parent.Bind(CQBEvent.EVT_CQB_QUERY_ERR, self.displayQueryError, self)
		self.parent.Bind(CQBEvent.EVT_CQB_QRY_RFRSH, self.refreshQueryData, self)
		
		self.parent.Bind(wx.EVT_QUERY_END_SESSION, query.CQBQuery.onQueryShutdown, self)
		self.parent.Bind(wx.EVT_END_SESSION, query.CQBQuery.onShutdown, self)
	
	def GetId(self):
		''' Returns a new id or previosly generated one if already called '''
		
		if self.object_id == None:
			self.object_id = wx.ID_ANY
		return self.object_id
	
	def displayQueryError(self, e):
		''' '''
		
		e.Skip()
	
	def refreshQueryData(self, e):
		''' '''
		
		e.Skip()
	
