#! /usr/bin/python

import sys, wx

from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame

from cqb import CQBHelper, CQBDatabase, connection

import view
import query, browser, result

class CQBFrame(wx.Frame):
	''' '''
	
	def __init__ (self, parent, id, title='', con_params={}, *args, **kwargs):
		''' '''

		if con_params == None or len(con_params) <= 0:
			con_params = CQB.loadProfile()
			if con_params == False:
				self.Close()
				return

		super(CQBFrame, self).__init__(parent, id, title=con_params['name'], name=con_params['name'], size=(800, 600), *args, **kwargs)
		self.helper = CQBHelper.instance(con_params['id'], con_params)
		
		self.buildWindow()
		
		self.menu = view.CQBMenu(frame=self)
		self.toolbar = view.CQBToolbar().load(self)

		self.statusbar = self.CreateStatusBar()

		self.Show(True)

	def buildWindow(self):
		''' '''
		self.window = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE | wx.SP_NOSASH)
		self.top = wx.Panel(self.window, wx.ID_ANY, style=wx.BORDER_SUNKEN)
		self.bottom = wx.Panel(self.window, wx.ID_ANY, style=wx.BORDER_SUNKEN)
		
		self.window.Initialize(self.top)

		self.buildWindowTop()
		self.buildWindowBottom()

	def showResults(self, query, rows, execution_time):
		self.bottom.Show(True)
		self.result.Show(True)
		self.window.SplitHorizontally(self.top, self.bottom, 0)
		self.statusbar.SetFields([query, '%s records' % rows, '%s secs elapsed' % execution_time])

	def buildWindowTop(self):
		''' '''
		self.topSplitter = wx.SplitterWindow(self.top, -1, style=wx.SP_LIVE_UPDATE)
		self.query = query.Query.instance(self.topSplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN, frame=self)
		self.browser = browser.Browser.instance(self.topSplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN, frame=self)
		self.topSplitter.SplitVertically(self.browser, self.query, 230)

		self.topSizer = wx.BoxSizer()
		self.topSizer.Add(self.topSplitter, 1, wx.EXPAND)
		self.top.SetSizer(self.topSizer)
		self.topSizer.Fit(self.top)

		self.topSizer.SetMinSize((400, 400))

	def buildWindowBottom(self):
		''' '''
		self.result = result.Result.instance(self.bottom, wx.ID_ANY, frame=self)
		self.bottom.Show(False)

		self.bottomSizer = wx.BoxSizer()
		self.bottomSizer.Add(self.result, 1, wx.EXPAND)
		self.bottom.SetSizer(self.bottomSizer)
		self.bottomSizer.Fit(self.bottom)

	def showPyShell(self, event):
		''' '''
		frame = ShellFrame(parent=self)
		frame.Show()

	def showPyFilling(self, event):
		''' '''
		frame = FillingFrame(parent=self)
		frame.Show()

	def quitApplication(self, e):
		self.Close()
		e.Skip()

class CQB(wx.App):
	''' '''

	instances = {}
	@staticmethod
	def instance(id=wx.ID_ANY):
		''' Returns a new instance or previosly generated one if found '''
		if id in CQB.instances:
			return CQB.instances[id]
		CQB.instances[id] = CQB()
		return CQB.instances[id]

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
			con_params = {'id': profile[0], 'host': profile[1], 'user': profile[2], 'passwd': profile[3], 'port': profile[4], 'name': profile[5]}

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
			dialog = wx.SingleChoiceDialog(None, "Select a Profile", "Cognac Query Browser", [x[5] for x in profiles])
			while True:
				if dialog.ShowModal() == wx.ID_OK:
					# get selected profile and destroy dialog
					profile = profiles[dialog.GetSelection()]
					dialog.Destroy()

					# return profile connection paramters
					return {'id': profile[0], 'host': profile[1], 'user': profile[2], 'passwd': profile[3], 'port': profile[4], 'name': profile[5]}

		except connection.errors.CQBConnectionError, exc:
			pass#wx.MessageBox(str(exc), "New Connection Failed", wx.OK | wx.ICON_ERROR)
			return False

		except Exception, exc:
			wx.MessageBox(str(exc), "Load Profile Error", wx.OK | wx.ICON_ERROR)
			return False

if __name__ == '__main__':
	app = CQB.instance()
	app.SetUseBestVisual(True, True)
	app.SetAppDisplayName('Cognac Query Browser')
	app.MainLoop()
