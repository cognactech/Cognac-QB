#! /usr/bin/python

import sys, wx

import connection
from connection import errors

from cqb import database, helper

import view
import query, browser, result

class CQBData(object):
	''' '''
	def __init__(self, data={}):
		''' '''
		self.data = data

class CQBFrame(wx.Frame):
	''' '''
	
	def __init__ (self, parent, id, con_params=[], *args, **kwargs):
		''' '''
		super(CQBFrame, self).__init__(parent, id, *args, **kwargs)

		if con_params == None or len(con_params) <= 0:
			result = self.loadFrameConnection()
			con_params = []
		self.helper = helper.CQBHelper(con_params)

		# initialize panels that will be needed to complete window
		self.query = query.Query.instance(self, wx.ID_ANY)
		self.browser = browser.Browser.instance(self, wx.ID_ANY)
		self.result = result.Result.instance(self, wx.ID_ANY)

		# hide query results until we have some
		self.queryResult.Show(False)

		self.buildWindow():
		self.Show(True)

	def buildWindow(self):
		''' '''
		self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)
		self.splitter.SplitVertically(self.queryEditor)
		
		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.splitter, 1, wx.EXPAND)
		self.sizer.Add(self.result, 0, wx.EXPAND)
		self.SetSizer(self.sizer)

	def loadFrameConnection():
		


class CQB(wx.App):
	''' '''

	@staticmethod
	def getNewFrame(id):
		''' '''
		return CQBFrame(None, id)

	def __init__ (*args, **kwargs):
		''' '''
		super(CQB, self).__init__(*args, **kwargs)

		self.database = database.CQBDatabase()

	def OnInit(self):
		''' '''
		self.window = self.getNewFrame(self.con)
		self.SetTopWindow(self.getNewFrame())	
		return True

	def quitApplication(self, e):
		'''  '''
		self.Close()
		e.Skip()

if __name__ == '__main__':
	app = CQB(0)       # Create an instance of the application class
	app.MainLoop()     # Tell it to start processing events