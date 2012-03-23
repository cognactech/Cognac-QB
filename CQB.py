#! /usr/bin/python

import sys, wx

import query
import connection
from connection import errors

class CQB(wx.App):
	''' '''
	
	def OnInit(self):
		''' '''
		
		try:
			con = connection.CQBConnection.instance(wx.ID_ANY, 'mysql')
			con.connect(host='50.57.54.39', user='youcallmd', passwd='19u8hf9quh')
			con.set_db('youcallmd')
		except errors.CQBConnectionError, exc:
			result = wx.MessageBox("You do not have an active connection! Error" + str(exc), "Connection Failed", wx.OK | wx.ICON_ERROR)
			return False
		
		self.mainFrame = query.CQBQuery.getNewQueryBrowser(connection=con, parent=None)
		self.SetTopWindow(self.mainFrame)
		return True
	

if __name__ == '__main__':
    app = CQB(0)       # Create an instance of the application class
    app.MainLoop()     # Tell it to start processing events