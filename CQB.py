#! /usr/bin/python

import sys, wx

import query
import connection
from connection import errors
import sqlite3

class CQB(wx.App):
	''' '''
	
	def OnInit(self):
		''' '''
		self.mainFrame = CQBWindow(None)
		self.SetTopWindow(self.mainFrame)
		return True

		
class CQBWindow(wx.Frame):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		
		super(CQBWindow, self).__init__(parent, size=(800, 600), *args, **kwargs)
		
		box = wx.BoxSizer()
		
		self.dbBrowserPanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
		
		self.queryEditorPanel = query.CQBQueryController.index(self, -1, style=wx.SUNKEN_BORDER)
		
		box.Add(self.dbBrowserPanel, 2, wx.EXPAND)
		box.Add(self.queryEditorPanel, 8, wx.EXPAND)
		
		self.SetSizer(box)
		
		self.menus = {
			'&File': (
				(wx.ID_ANY, '&Run Query\tCtrl+R', 'Run Query', wx.EVT_MENU, self.queryEditorPanel.triggerQueryRun),
				(wx.ID_ANY, '&Refresh\tShift+Ctrl+R', 'Refresh Results', wx.EVT_MENU, self.queryEditorPanel.triggerRefresh),
				(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Cognac Query Browser', wx.EVT_MENU, [self.quitApplication, self.queryEditorPanel.quitApplication])
			)
		}
		self.buildMenubar()
		self.buildStatusBar()
		
		self.toolbar_items = (
			(wx.ID_ANY, "Run Query", "Run Query", "images/run.png", wx.EVT_MENU, self.queryEditorPanel.triggerQueryRun),
			(wx.ID_ANY, "Stop Query", "Cancel the execution of the current query", "images/stop.png", wx.EVT_MENU, self.queryEditorPanel.triggerQueryStop),
			(wx.ID_ANY, "Load File", "Load SQL from a file", "images/run.png", wx.EVT_MENU, self.queryEditorPanel.loadQueryDialog),
		)
		self.buildToolbar()
		
		self.Centre()
		self.Show(True)
		
		try:
			conn = sqlite3.connect('/Users/ncurtis/qcb-data')
			
			c = conn.cursor()
			c.execute('SELECT * FROM connections')
			
			self.profiles = []
			for row in c:
				self.profiles.append(row)
			
			dialog = wx.SingleChoiceDialog(self.queryEditorPanel, "Select a database profile", "Welcome", [x[5] for x in self.profiles])
			
			if dialog.ShowModal() == wx.ID_OK:
				aprofile = dialog.GetSelection()
				
				self.con = connection.CQBConnection.instance(self.profiles[aprofile][0], 'mysql')
				self.con.connect(host=self.profiles[aprofile][1], user=self.profiles[aprofile][2], passwd=self.profiles[aprofile][3])
				self.con.set_db('youcallmd')
				
				dialog.Destroy()
			
			else:
				dialog.Destroy()
			
		except errors.CQBConnectionError, exc:
			result = wx.MessageBox(str(exc), "Connection Failed", wx.OK | wx.ICON_ERROR)

		except Exception, exc:
			result = wx.MessageBox(str(exc), "Application Error", wx.OK | wx.ICON_ERROR)
	
	def buildMenubar(self):
		''' Builds menu using [self.menus] '''

		menubar = wx.MenuBar()

		for key, menu in self.menus.items():
			Menu = wx.Menu()
			for id, command, label, event_id, event_callback in menu:
				item = Menu.Append(id, command, label) 
				try:
					for callback in event_callback:
						self.Bind(event_id, callback, item)
				except:
					self.Bind(event_id, event_callback, item)
					
			menubar.Append(Menu, key)

		self.SetMenuBar(menubar)

	def buildToolbar(self):
		''' '''

		self.toolbar = self.CreateToolBar()
		for item in self.toolbar_items:
			menuitem = self.toolbar.AddSimpleTool(-1, wx.Bitmap(item[3]), item[1], item[2])
			self.Bind(item[4], item[5], menuitem)
		self.toolbar.Realize()

	def buildStatusBar(self):
		''' '''

		self.statusBar = self.CreateStatusBar()
	
	def quitApplication (self, e):
		''' '''
		
		self.Close()
		e.Skip()

if __name__ == '__main__':
	app = CQB(0)       # Create an instance of the application class
	app.MainLoop()     # Tell it to start processing events