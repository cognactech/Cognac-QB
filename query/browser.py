import wx

class CQBQueryApp(wx.App):
	def OnInit(self):
		CQBQueryBrowser(self)

class CQBQueryBrowser(wx.Frame):
	
	def __init__ (self, parent, *args, **kwargs):
		super(__init__, self, *args, **kwargs)
		
		self.buildMenubar()
		self.buildSizers()
		self.buildToolbar()
		self.buildStatusBar()
		
		self.buildEditor()
		
		self.Centre()
	
	def buildMenuBar(self):
		pass
	
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
	
	def refreshBrowser(self):
		''' Triggers QueryEventResults '''
		evt = CQBQueryEventRefresh(CQBQueryEventRefresh_ID, self.GetId())
		self.GetEventHandler().ProcessEvent(evt)

class CQBQueryBrowserToolbar():
	pass
	
if __name__ == '__main__':
	app = CQBQueryApp(title='New Query', size=(500, 600))
	app.MainLoop()
