#! /usr/bin/python

import wx
import controller as CQBController
import browser as CQBBrowser

class CQBQuery(wx.App):
	''' '''
	
	def OnInit(self):
		''' '''
		self.mainFrame = CQBBrowser.CQBQueryBrowser(None, title='Cognac Query Browser', size=(800, 600))
		self.SetTopWindow(self.mainFrame)
		controller = CQBController.CQBQueryController(self.mainFrame)
		return True
	
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
