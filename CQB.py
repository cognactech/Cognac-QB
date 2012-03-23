#! /usr/bin/python

import sys, wx

import query
import connection

class CQB(wx.App):
	''' '''
	
	def OnInit(self):
		''' '''
		
		con = connection.CQBConnection.instance(wx.ID_ANY, 'mysql')
		con.connect(host='10.182.227.26', user='youcallmd', passwd='19u8hf9quh')
		con.set_db('youcallmd')\
		
		self.mainFrame = query.getNewQueryBrowser(connection=con, parent=None)
		self.SetTopWindow(self.mainFrame)
		return True
	

if __name__ == '__main__':
    app = CQB(0)       # Create an instance of the application class
    app.MainLoop()     # Tell it to start processing events