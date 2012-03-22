#! /usr/bin/python

import wx
import controller as CQBController
import browser as CQBBrowser
import connection as CQBConnection

class CQBQuery(wx.App):
	''' '''
	
	def OnInit(self):
		''' '''
		
		# build main frame of query application and define it as top window
		self.mainFrame = CQBBrowser.CQBQueryBrowser(None, title='Cognac Query Browser', size=(400, 400))
		self.SetTopWindow(self.mainFrame)
		
		# load connection module and connect to database
		try
			self.connection = CQBConnection.instance(self.mainFrame.GetId(), 'mysql')
			self.connection.connect(host='10.182.227.26', user='youcallmd', passwd='19u8hf9quh')
			self.connection.set_db('youcallmd')
			self.controller = CQBController.CQBQueryController(self.mainFrame, self.connection)
			return True
		except e
			
		finally
			return False
	
	def getNewQueryBrowser (self, connection, parent=None):
		''' '''
		
		return CQBBrowser.CQBQueryBrowser(parent)
	
	def onQueryShutdown(self, e):
		''' Called when a EVT_QUERY_END_SESSION event is triggered '''
		
		e.Skip()
	
	def onShutdown(self, e):
		''' Called when a EVT_END_SESSION event is triggered'''
		
		e.Skip()

if __name__ == '__main__':
	app = CQBQuery()
	app.MainLoop()
