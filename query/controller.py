#! /usr/bin/python

import wx
import __init__ as query
import event as CQBEvent

class CQBQueryController(wx.EvtHandler):
	''' '''
	
	object_id = None
	
	def __init__ (self, parent, connection, *args, **kwargs):
		''' '''
		
		super(CQBQueryController, self).__init__(*args, **kwargs)
		
		self.connection = connection
		self.parent = parent
		
		if not self.connection.is_connected():
			 result = wx.MessageBox("You do not have an active connection!", "Connection Failed", wx.OK | wx.ICON_ERROR)
			 self.parent.Close()
			 self.parent.Destroy()
			 self.Close()
			 self.Destroy()
		
		self.parent.Bind(CQBEvent.EVT_CQB_QUERY_ERR, self.displayQueryError, self)
		self.parent.Bind(CQBEvent.EVT_CQB_QRY_RFRSH, self.refreshQueryData, self)
		
		self.parent.Bind(wx.EVT_QUERY_END_SESSION, query.CQBQuery.onQueryShutdown, self)
		self.parent.Bind(wx.EVT_END_SESSION, query.CQBQuery.onShutdown, self)
	
	def GetId(self):
		''' Returns a new id or previosly generated one if already called '''
		
		if self.object_id == None:
			self.object_id = wx.ID_ANY
		return self.object_id
	
	def runQuery(self, e):
		''' '''
		try
			query = self.parent.GetWindow('QueryEditor').GetValue()
			data = self.connection.query(query)
			self.parent.refreshGrid(data[0], data[1])
		except
			pass
		finally
			e.Skip()
	
	def displayQueryError(self, e):
		''' '''
		
		e.Skip()
	
	def refreshQueryData(self, e):
		''' '''
		
		e.Skip()
	

