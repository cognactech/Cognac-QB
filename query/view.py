import wx, wx.stc

class QueryMenu():
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(QueryMenu, self).__init__(parent, id, *args, **kwargs)

class QueryToolbar():
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(QueryToolbar, self).__init__(parent, id, *args, **kwargs)

class QueryEditorTextCtrl(wx.stc.StyledTextCtrl):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		super(QueryEditorTextCtrl, self).__init__(parent, *args, **kwargs)
		self.SetMargins(0, 50)
		self.SetInsertionPoint(0)

class QueryEditor(wx.Panel):
	''' '''
	
	def __init__ (self, parent, *args, **kwargs):
		''' '''
		super(QueryEditor, self).__init__(parent, *args, **kwargs)
		
		self.queryEditor = QueryEditorTextCtrl(self, -1)
		
		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.queryEditor, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
	
	def loadQueryDialog(self, e):
		''' '''
		
		loadQueryDialog = wx.FileDialog(self, style=wx.OPEN)

		if loadQueryDialog.ShowModal() == wx.ID_OK:
			pass

		loadQueryDialog.Destroy()
		e.Skip()
