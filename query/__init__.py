#! /usr/bin/python

import wx
import browser as CQBBrowser

class CQBQuery(wx.App):

	def OnInit(self):
		mainFrame = CQBBrowser.CQBQueryBrowser(None)
		self.SetTopWindow(mainFrame)
		return True

if __name__ == '__main__':
	app = CQBQuery()
	app.MainLoop()

