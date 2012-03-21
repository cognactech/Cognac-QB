#! /usr/bin/python

import wx
import event as CQBEvent

class CQBQueryBrowser(wx.Frame, CQBEvent.CQBQueryEvent):
	
	def __init__ (self, parent, *args, **kwargs):
		super(CQBQueryBrowser, self).__init__(parent, *args, **kwargs)
		
		self.bindEvents()
		
		self.menus = {
			'&File': (
				(wx.ID_ANY, '&Run\tCtrl+R', 'Run Query', wx.EVT_MENU, self.refreshBrowser),
				(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Cognac Query Browser', wx.EVT_MENU, self.closeQueryBrowser)
			)
		}
		
		self.buildMenubar()
		
		self.buildSizers()
		self.buildToolbar()
		self.buildStatusBar()
		
		self.buildEditor()
		
		self.Centre()
		self.Show(True)
	
	def bindEvents(self):
		self.Bind(CQBEvent.EVT_CQB_QRY_RFRSH, self.refreshQueryData, self)
	
	def refreshQueryData(self, e):
		pass
	
	def menuItems(self, menuName):
		return self.menus[menuName]
	
	def buildMenubar(self):
		menubar = wx.MenuBar()
		
		for key, menu in self.menus.items():
			Menu = wx.Menu()
			for id, command, label, event_id, event_callback in menu:
				item = Menu.Append(id, command, label)
				self.Bind(event_id, event_callback, item)
			menubar.Append(Menu, key)
		
		self.SetMenuBar(menubar)
	
	def closeQueryBrowser(self, e):
		self.Close()
		e.Skip()
	
	def buildSizers(self):
		pass
	
	def buildToolbar(self):
		pass
	
	def buildStatusBar(self):
		pass
	
	def buildEditor(self):
		pass
	
	def browserError(self):
		''' Triggers QueryEventError '''
		evt = CQBEvent.CQBQueryEventError(CQBEvent.EVT_CQB_QUERYERROR_ID, self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def showBrowser(self):
		''' Triggers QueryEventResults '''
		evt = CQBEvent.CQBQueryEventResults(CQBEvent.EVT_CQB_QRY_RSLTS_ID, self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def refreshBrowser(self, event):
		''' Triggers QueryEventResults '''
		evt = CQBEvent.CQBQueryEventRefresh(CQBEvent.EVT_CQB_QRY_RFRSH_ID, self.GetId())
		self.GetEventHandler().ProcessEvent(evt)

class CQBQueryBrowserToolbar():
	pass
