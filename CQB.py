#! /usr/bin/python

import sys, wx

import query as CQBQuery
import connection as CQBConnection

class CQB(wx.App):
	''' '''
	
    def OnInit(self):
    	''' '''
    	
    	connection = CQBConnection.instance(wx.ID_ANY, 'mysql')
		connection.connect(host='10.182.227.26', user='youcallmd', passwd='19u8hf9quh')
		connection.set_db('youcallmd')
    	
        self.mainFrame = CQBQuery.CQBQuery.getNewQueryBrowser(connection=connection, parent=None)
        self.SetTopWindow(self.mainFrame)
        return True

if __name__ == '__main__':
    app = CQB(0)       # Create an instance of the application class
    app.MainLoop()     # Tell it to start processing events