#! /usr/bin/python

import wx
import browser

class CQBQueryApp(wx.App):
	def OnInit(self):
		CQBQuery(self)

class CQBQuery():
	def __init__ (self, *args, **kwargs):
		super(__init__, self, *args, **kwargs)

	def query(self, query_text = ''):
		return results

if __name__ == '__main__':
	app = CQBQueryApp(title='Cognac Query Browser', size=(500, 600))
	app.MainLoop()
