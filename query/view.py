class QueryMenu(CQBMenu)
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(ResultMenu, self).__init__(parent, id, *args, **kwargs)

class QueryToolbar(CQBToolbar)
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(ResultToolbar, self).__init__(parent, id, *args, **kwargs)

class QueryEditorTextCtrl(wx.TextCtrl):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		#wx.Font(pointSize=12, family=wx.FONTFAMILY_MODERN, style=wx.NORMAL, weight=wx.NORMAL)
		ctrlStyles = wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB		
		super(QueryEditorTextCtrl, self).__init__(parent, style=ctrlStyles, *args, **kwargs)
		self.SetInsertionPoint(0)

class QueryEditor(wx.Panel):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		super(CQBQueryBrowser, self).__init__(parent, *args, **kwargs)
		
		self.queryEditor = QueryEditorTextCtrl(self, -1)
		
		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.queryEditor, 1, wx.EXPAND)
		self.SetSizer(self)
	
	def loadQueryDialog(self, e):
		''' '''
		
		loadQueryDialog = wx.FileDialog(self, style=wx.OPEN)

		if loadQueryDialog.ShowModal() == wx.ID_OK:
			pass

		loadQueryDialog.Destroy()
		e.Skip()
