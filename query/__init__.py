#! /usr/bin/python

import wx
import wx.grid
import browser as CQBBrowser

class CQBQuery(wx.App):
	''' '''
	def __init__(self, *args, **kwards)
		''' ''' 
		
		self.controller = CQBController(connection)
		
	def OnInit(self, connection):
		''' '''
		
		# build main frame of query application and define it as top window
		self.mainFrame = CQBQueryBrowser(None, title='Cognac Query Browser', size=(400, 400))
		self.SetTopWindow(self.mainFrame)
	
	@staticmethod
	def getNewQueryBrowser (parent=None, connection):
		''' '''
		
		browser = CQBQueryBrowser(parent, title='Cognac Query Browser', size=(400, 400))
		CQBController(browser, connection)
		return browser
	
	def onQueryShutdown(self, e):
		''' Called when a EVT_QUERY_END_SESSION event is triggered '''
		
		e.Skip()
	
	def onShutdown(self, e):
		''' Called when a EVT_END_SESSION event is triggered'''
		
		e.Skip()
	

class CQBQueryBrowser(wx.Frame, CQBQueryEvent):
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
		self.resultsGrid = CQBQueryResultGrid(self.splitter, field_names, results, style=wx.SUNKEN_BORDER)
		
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
		
		evt = CQBQueryEventStop(self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def triggerQueryRun(self, e=None):
		''' Triggers CQBQueryEventRun '''
		
		evt = CQBQueryEventRun(self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def triggerError(self, e=None):
		''' Triggers QueryEventError '''
		
		evt = CQBQueryEventError(self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def triggerRefresh(self, e=None):
		''' Opens QueryResultGrid and Triggers QueryEventResults '''
		
		evt = CQBQueryEventRefresh(self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
class CQBQueryCtrl(wx.TextCtrl):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		
		#wx.Font(pointSize=12, family=wx.FONTFAMILY_MODERN, style=wx.NORMAL, weight=wx.NORMAL)
		ctrlStyles = wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB
		
		super(CQBQueryCtrl, self).__init__(parent, style=ctrlStyles, *args, **kwargs)
		
		self.SetInsertionPoint(0)

class CQBQueryController(wx.EvtHandler):
	''' '''
	
	object_id = None
	
	def __init__ (self, parent, connection, *args, **kwargs):
		''' '''
		
		super(CQBQueryController, self).__init__(*args, **kwargs)
		
		self.connection = connection
		self.parent = parent
		
		if not self.connection.is_connected():
			 result = wx.MessageBox("You do not have an active connection!", "Connection Failed", wx.OK | wx.ICON_ERROR)
			 self.parent.Close()
			 self.parent.Destroy()
			 self.Close()
			 self.Destroy()
		
		self.parent.Bind(EVT_CQB_QUERY_ERR, self.displayQueryError, self)
		self.parent.Bind(EVT_CQB_QRY_RFRSH, self.refreshQueryData, self)
		
		self.parent.Bind(wx.EVT_QUERY_END_SESSION, query.CQBQuery.onQueryShutdown, self)
		self.parent.Bind(wx.EVT_END_SESSION, query.CQBQuery.onShutdown, self)
	
	def GetId(self):
		''' Returns a new id or previosly generated one if already called '''
		
		if self.object_id == None:
			self.object_id = wx.ID_ANY
		return self.object_id
	
	def runQuery(self, e):
		''' '''
		try:
			query = self.parent.GetWindow('QueryEditor').GetValue()
			data = self.connection.query(query)
			self.parent.refreshGrid(data[0], data[1])
		except:
			pass
		finally:
			e.Skip()
	
	def displayQueryError(self, e):
		''' '''
		
		e.Skip()
	
	def refreshQueryData(self, e):
		''' '''
		
		e.Skip()
	

class CQBQueryEvent(wx.PyCommandEvent):
	def __init__ (self, evtType, id):
		super(CQBQueryEvent, self).__init__(evtType, id)
	
EVT_CQB_QUERY_ID = wx.NewEventType()
EVT_CQB_QUERY = wx.PyEventBinder(EVT_CQB_QUERY_ID, 1)

class CQBQueryEventError(CQBQueryEvent):
	def __init__ (self, id):
		super(CQBQueryEventError, self).__init__(EVT_CQB_QUERY_ERR_ID, id)

EVT_CQB_QUERY_ERR_ID = wx.NewEventType()
EVT_CQB_QUERY_ERR = wx.PyEventBinder(EVT_CQB_QUERY_ERR_ID, 1)

class CQBQueryEventRefresh(CQBQueryEvent):
	def __init__ (self, id):
		super(CQBQueryEventRefresh, self).__init__(EVT_CQB_QRY_RFRSH_ID, id)

EVT_CQB_QRY_RFRSH_ID = wx.NewEventType()
EVT_CQB_QRY_RFRSH = wx.PyEventBinder(EVT_CQB_QRY_RFRSH_ID, 1)

class CQBQueryEventRun(CQBQueryEvent):
	def __init__ (self, id):
		super(CQBQueryEventRun, self).__init__(EVT_CQB_QRY_RUN_ID, id)

EVT_CQB_QRY_RUN_ID = wx.NewEventType()
EVT_CQB_QRY_RUN = wx.PyEventBinder(EVT_CQB_QRY_RUN_ID, 1)

class CQBQueryEventStop(CQBQueryEvent):
	def __init__ (self, id):
		super(CQBQueryEventStop, self).__init__(EVT_CQB_QRY_STOP_ID, id)

EVT_CQB_QRY_STOP_ID = wx.NewEventType()
EVT_CQB_QRY_STOP = wx.PyEventBinder(EVT_CQB_QRY_STOP_ID, 1)

class CQBQueryResult(wx.grid.PyGridTableBase):
	'''	'''
	
	def __init__ (self, field_names, results, *args, **kwargs):
		super(CQBQueryResult, self).__init__(*args, **kwargs)
		self.field_names = field_names
		self.results = results
	
	def GetNumberRows(self):
		return len(self.results)
	
	def GetNumberCols(self):
		return len(self.results[0])
	
	def IsEmptyCell(self, row, col):
		row = self.results[row]
		if row[col]:
			return False
		return True
	
	def GetValue(self, row, col):
		row = self.results[row]
		return row[col]
	
	def SetValue(self, row, col, value):
		pass
	
	def GetColLabelValue(self, col):
		if self.field_names:
			return self.field_names[col]
	
	def GetRowLabelValue(self, row):
		return row
	
class CQBQueryResultGrid(wx.grid.Grid):
	''' '''
	
	def __init__ (self, field_names=(), results=[], *args, **kwargs):
		super(CQBQueryResultGrid, self).__init__(*args, **kwargs)
		self.SetTable(CQBQueryResult(field_names, results))
	
if __name__ == '__main__':
	import connection
	connection = CQBConnection.instance(wx.ID_ANY, 'mysql')
	connection.connect(host='10.182.227.26', user='youcallmd', passwd='19u8hf9quh')
	connection.set_db('youcallmd')
	app = CQBQuery(connection)
	app.MainLoop()