import wx
import event from query

class CQBQueryApp(wx.App):
	def OnInit(self):
		CQBQueryBrowser(self)

class CQBQueryBrowser(wx.Frame, query.QCBQueryEvent):
	
	def __init__ (self, parent, *args, **kwargs):
		super(__init__, self, *args, **kwargs)
		
		self.buildMenubar()
		self.buildSizers()
		self.buildToolbar()
		self.buildStatusBar()
		
		self.buildEditor()
		
		self.Centre()
	
	def bindEvents(self):
		self.Bind(self.EVT_CQB_QRY_RFRSH, self.refreshQueryBrowser, self)
	
	def buildMenuBar(self):
		runQueryMenuItem = fileMenu.Append(wx.ID_ANY, '&Run\tCtrl+R', 'Run Query')
		quitAppMenuItem = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Cognac Query Browser')
		
		self.Bind(wx.EVT_MENU, self.refreshBrowser, runQueryMenuItem)
		self.Bind(wx.EVT_MENU, self.closeQueryBrowser, quitAppMenuItem)
	
	def refreshQueryBrowser(e):
		self.refreshBrowser()
	
	def closeQueryBrowser(e):
		self.Close()
		e.skip()
	
	def buildSizers():
		pass
	
	def buildToolbar(self):
		pass
	
	def buildStatusBar(self):
		pass
	
	def buildEditor(self):
		pass
	
	def browserError(self):
		''' Triggers QueryEventError '''
		evt = CQBQueryEventError(CQBQueryEventError_ID, self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def showBrowser(self):
		''' Triggers QueryEventResults '''
		evt = CQBQueryEventResults(CQBQueryEventResults_ID, self.GetId())
		self.GetEventHandler().ProcessEvent(evt)
	
	def refreshBrowser(self, event):
		''' Triggers QueryEventResults '''
		evt = CQBQueryEventRefresh(CQBQueryEventRefresh_ID, self.GetId())
		self.GetEventHandler().ProcessEvent(evt)

class CQBQueryBrowserToolbar():
	pass
	
if __name__ == '__main__':
	app = CQBQueryApp(title='New Query', size=(500, 600))
	app.MainLoop()
