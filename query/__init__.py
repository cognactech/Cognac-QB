#! /usr/bin/python

import wx
import wx.grid
import threading

class CQBQueryEvent(wx.PyCommandEvent):
	def __init__ (self, evtType, id):
		super(CQBQueryEvent, self).__init__(evtType, id)
	
EVT_CQB_QRY_ID = wx.NewEventType()
EVT_CQB_QRY = wx.PyEventBinder(EVT_CQB_QRY_ID, 1)

class CQBQueryEventError(CQBQueryEvent):
	def __init__ (self, id, message):
		super(CQBQueryEventError, self).__init__(EVT_CQB_QRY_ERR_ID, id)
		self.message = message

EVT_CQB_QRY_ERR_ID = wx.NewEventType()
EVT_CQB_QRY_ERR = wx.PyEventBinder(EVT_CQB_QRY_ERR_ID, 1)

class CQBQueryEventRefresh(CQBQueryEvent):
	def __init__ (self, id, field_names=[], data=[], execution_time=None):
		super(CQBQueryEventRefresh, self).__init__(EVT_CQB_QRY_RFRSH_ID, id)
		self.field_names = field_names
		self.data = data
		self.execution_time = execution_time

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
	
	def __init__ (self, parent, field_names=(), results=[], *args, **kwargs):
		super(CQBQueryResultGrid, self).__init__(parent, -1, *args, **kwargs)
		table = CQBQueryResult(field_names, results)
		self.SetTable(table)
	
class CQBQueryCtrl(wx.TextCtrl):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		
		#wx.Font(pointSize=12, family=wx.FONTFAMILY_MODERN, style=wx.NORMAL, weight=wx.NORMAL)
		ctrlStyles = wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB
		
		super(CQBQueryCtrl, self).__init__(parent, style=ctrlStyles, *args, **kwargs)
		
		self.SetInsertionPoint(0)

class CQBQueryThread(threading.Thread):
	''' '''
	
	def __init__(self, parent, *args, **kwargs):
		''' '''
		
		super(CQBQueryThread, self).__init__(*args, **kwargs)
		self.parent = parent

	def run(self):
		""" Overrides Thread.run. Don't call this directly its called internally when you call Thread.start(). """
		
		try:
			query = self.parent.queryEditor.GetValue()
			
			print query
			
			data = self.parent.parent.con.query(query)
			
			evt = CQBQueryEventRefresh(EVT_CQB_QRY_RFRSH_ID, field_names=data[0], data=data[1], execution_time=data[2])
		except Exception, exc:
			evt = CQBQueryEventError(EVT_CQB_QRY_ERR_ID, str(exc))
		
		wx.PostEvent(self.parent, evt)
		
	
class CQBQueryController(wx.EvtHandler):
	''' '''
	
	object_id = None
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		
		super(CQBQueryController, self).__init__(*args, **kwargs)
		
		self.parent = parent
		
		self.parent.Bind(EVT_CQB_QRY_ERR, self.displayQueryError, self)
		self.parent.Bind(EVT_CQB_QRY_RFRSH, self.refreshQueryData, self)
		self.parent.Bind(EVT_CQB_QRY_RUN, self.runQuery, self)
	
	@staticmethod
	def index(*args, **kwargs):
		browser = CQBQueryBrowser(*args, **kwargs)
		CQBQueryController(browser)
		return browser
	
	def GetId(self):
		''' Returns a new id or previosly generated one if already called '''
		
		if self.object_id == None:
			self.object_id = wx.ID_ANY
		return self.object_id
	
	def runQuery(self, e):
		''' '''
		
		self.parent.clearGrid()
		queryThread = CQBQueryThread(self.parent)
		queryThread.start()
	
	def displayQueryError(self, e):
		''' '''
		
		result = wx.MessageBox(e.message, "Query Failed", wx.OK | wx.ICON_ERROR)
		
		e.Skip()
	
	def refreshQueryData(self, e):
		''' '''
		
		self.parent.refreshGrid(e.field_names, e.data, e.execution_time)
		
		e.Skip()
	

class CQBQueryBrowser(wx.Panel):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		
		super(CQBQueryBrowser, self).__init__(parent, *args, **kwargs)
		
		self.parent = parent
		self.initLayout()
		self.Centre()
		self.Show(True)
	
	def initLayout(self):
		''' '''
		
		box = wx.BoxSizer()
		
		self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)
		
		self.queryEditorPanel = wx.Panel(self.splitter, -1, style=wx.SUNKEN_BORDER)
		
		self.queryEditor = CQBQueryCtrl(self.queryEditorPanel, -1)
		self.queryEditor.AppendText('SELECT * FROM users LIMIT 0, 1000');
		
		self.splitter.Initialize(self.queryEditorPanel)
		
		box.Add(self.splitter, 1, wx.EXPAND)
		
		self.SetSizer(box)
	
	resultsGrid = None
	def refreshGrid(self, field_names, results, execution_time):
		''' '''
		
		# build new results grid with data passed
		self.resultsGrid = CQBQueryResultGrid(self.splitter, field_names=field_names, results=results, style=wx.SUNKEN_BORDER)
		
		# split panel with current query window and new results grid
		self.splitter.SplitHorizontally(self.splitter.GetWindow1(), self.resultsGrid)
	
	def clearGrid(self):
		''' '''
		
		# un split panel destroy and del current resultsGrid
		self.splitter.Unsplit()
		if self.resultsGrid != None:
			self.resultsGrid.Destroy()
			del self.resultsGrid
	
	def loadQueryDialog(self, e):
		''' '''
		
		loadQueryDialog = wx.FileDialog(self, style=wx.OPEN)

		if loadQueryDialog.ShowModal() == wx.ID_OK:
			pass

		loadQueryDialog.Destroy()
		e.Skip()
	
	def quitApplication (self, e):
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
	
