#! /usr/bin/python

import sys, wx

from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame

from cqb import CQBHelper, CQBDatabase, connection

import view
import query, browser, result

class CQBData(object):
	''' '''
	def __init__(self, data={}):
		''' '''
		self.data = data

class CQBFrame(wx.Frame):
	''' '''
	
	def __init__ (self, parent, id, con_params={}, *args, **kwargs):
		''' '''
		super(CQBFrame, self).__init__(parent, id, *args, **kwargs)

		if con_params == None or len(con_params) <= 0:
			con_params = CQB.loadProfile()
			if con_params == False:
				self.Close()
				return

		self.helper = CQBHelper.instance(con_params['name'], con_params)

		self.buildWindow()
		self.Show(True)

		self.OnShell(None)
		self.OnFilling(None)

	def buildWindow(self):
		''' '''
		self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)

		# initialize panels that will be needed to complete window
		self.query = query.Query.instance(self.splitter, wx.ID_ANY)
		self.browser = browser.Browser.instance(self.splitter, wx.ID_ANY)
		self.result = result.Result.instance(self, wx.ID_ANY)

		# hide query results until we have some
		self.result.Show(False)
		
		self.splitter.SplitVertically(self.browser, self.query)
		
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.sizer.Add(self.splitter, 1, wx.EXPAND)
		self.sizer.Add(self.result, 1, wx.EXPAND)
		
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)

	def OnShell(self, event):
		''' '''
		frame = ShellFrame(parent=self)
		frame.Show()

	def OnFilling(self, event):
		''' '''
		frame = FillingFrame(parent=self)
		frame.Show()

class CQB(wx.App):
	''' '''

	@staticmethod
	def getNewFrame(id, con_params={}):
		''' '''
		return CQBFrame(None, id, con_params=con_params)

	def OnInit(self):
		''' '''
		self.database = CQBDatabase.instance()

		try:
			profiles = list(self.database.profiles())
			dialog = wx.SingleChoiceDialog(None, "Select a Profile", "Cognac QueryBrowser", [x[5] for x in profiles])
			while True:
				if dialog.ShowModal() == wx.ID_OK:
					# get selected profile and destroy dialog
					profile = profiles[dialog.GetSelection()]
					break
				else:
					return False

			# pass connection to new instance of CQBFrame
			dialog.Destroy()
			con_params = {'host': profile[1], 'user': profile[2], 'passwd': profile[3], 'port': profile[4], 'name': profile[5]}

			frame = CQB.getNewFrame(wx.ID_ANY, con_params=con_params)
			self.SetTopWindow(frame)
			return True

		except connection.errors.CQBConnectionError, exc:
			wx.MessageBox(str(exc), "Initial Connection Failed", wx.OK | wx.ICON_ERROR)
			return False
		
		except Exception, exc:
			wx.MessageBox(str(exc), "Application Error", wx.OK | wx.ICON_ERROR)
			return False

		return False

	@staticmethod
	def loadProfile():
		''' '''
		database = CQBDatabase.instance()
		try:
			profiles = list(database.profiles())
			dialog = wx.SingleChoiceDialog(None, "Select a Profile", "Cognac QueryBrowser", [x[5] for x in profiles])
			while True:
				if dialog.ShowModal() == wx.ID_OK:
					# get selected profile and destroy dialog
					profile = profiles[dialog.GetSelection()]
					dialog.Destroy()

					# return profile connection paramters
					return {'host': profile[1], 'user': profile[2], 'passwd': profile[3], 'port': profile[4], 'name': profile[5]}

		except connection.errors.CQBConnectionError, exc:
			pass#wx.MessageBox(str(exc), "New Connection Failed", wx.OK | wx.ICON_ERROR)
			return False
		
		except Exception, exc:
			wx.MessageBox(str(exc), "Load Profile Error", wx.OK | wx.ICON_ERROR)
			return False

if __name__ == '__main__':
	app = CQB(0)
	app.SetAppDisplayName('Cognac Query Browser')
	app.MainLoop()