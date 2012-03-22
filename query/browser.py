#! /usr/bin/python

import wx
import event as CQBEvent
import result as CQBResult

class CQBQueryBrowser(wx.Frame, CQBEvent.CQBQueryEvent):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		
		super(CQBQueryBrowser, self).__init__(parent, *args, **kwargs)
		
		self.menus = {
			'&File': (
				(wx.ID_ANY, '&Run Query\tCtrl+R', 'Run Query', wx.EVT_MENU, self.triggerQueryRun),
				(wx.ID_ANY, '&Refresh\tShift+Ctrl+R', 'Refresh Results', wx.EVT_MENU, self.triggerRefresh),
				(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Cognac Query Browser', wx.EVT_MENU, self.closeQueryBrowser)
			)
		}
		self.buildMenubar()
		self.buildStatusBar()
		
		self.toolbar_items = (
			(wx.ID_ANY, "Run Query", "Run Query", "./images/run.png", wx.EVT_MENU, self.triggerQueryRun),
			(wx.ID_ANY, "Stop Query", "Cancel the execution of the current query", "./images/stop.png", wx.EVT_MENU, self.triggerQueryStop),
			(wx.ID_ANY, "Load File", "Load SQL from a file", "images/run.png", wx.EVT_MENU, self.loadQueryDialog),
		)
		self.buildToolbar()
		
		self.buildFrame()
	
	def buildMenubar(self):
		''' Builds menu using [self.menus] '''
		
		menubar = wx.MenuBar()
		
		for key, menu in self.menus.items():
			Menu = wx.Menu()
			for id, command, label, event_id, event_callback in menu:
				item = Menu.Append(id, command, label) 
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
	
	def buildFrame(self):
		''' '''
		
		box = wx.BoxSizer()
		
		self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)
		
		self.queryEditorPanel = wx.Panel(self.splitter, -1, style=wx.SUNKEN_BORDER)
		self.queryEditor = CQBQueryCtrl(self.queryEditorPanel, -1, name="QueryEditor")
		
		# move this to results found callback
		self.splitter.SplitHorizontally(self.queryEditorPanel, self.resultsGrid, 300)
		
		self.splitter.SetSizer(box)
		
		self.Centre()
		self.Show(True)
	
	def refreshGrid(self, field_names, results):
		# un split panel destroy and del current resultsGrid
		self.splitter.UnSplit()
		self.resultsGrid.Destroy()
		del self.resultsGrid
		
		# build new results grid with data passed
		self.resultsGrid = CQBResult.CQBQueryResultGrid(self.splitter, field_names, results, style=wx.SUNKEN_BORDER)
		
		#resize main frame to its best fit size
		self.mainFrame.SetSize(self.mainFrame.GetBestSize())
		
		# split panel with current query window and new results grid
		self.splitter.SplitHorizontally(self.splitter.GetWindow1(), self.resultsGrid, 300)
	
	def loadQueryDialog(self, e):
		''' '''
		
		loadQueryDialog = wx.FileDialog(self, style=wx.OPEN)

		if loadQueryDialog.ShowModal() == wx.ID_OK:
			pass

		loadQueryDialog.Destroy()
		e.Skip()
	
	def closeQueryBrowser(self, e):
		'''  '''

		self.triggerQueryStop()
		self.Close()
		e.Skip()
	
	def triggerQueryStop(self, e=None):
		''' Triggers CQBQueryEventStop '''
		
		evt = CQBEvent.CQBQueryEventStop(self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def triggerQueryRun(self, e=None):
		''' Triggers CQBQueryEventRun '''
		
		evt = CQBEvent.CQBQueryEventRun(self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def triggerError(self, e=None):
		''' Triggers QueryEventError '''
		
		evt = CQBEvent.CQBQueryEventError(self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def triggerRefresh(self, e=None):
		''' Opens QueryResultGrid and Triggers QueryEventResults '''
		
		evt = CQBEvent.CQBQueryEventRefresh(self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
class CQBQueryCtrl(wx.TextCtrl):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		
		#wx.Font(pointSize=12, family=wx.FONTFAMILY_MODERN, style=wx.NORMAL, weight=wx.NORMAL)
		ctrlStyles = wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB
		
		super(CQBQueryCtrl, self).__init__(parent, style=ctrlStyles, *args, **kwargs)
		
		self.SetInsertionPoint(0)
	
