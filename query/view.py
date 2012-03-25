import wx, wx.stc
import shlex
import sql

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
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(QueryEditorTextCtrl, self).__init__(parent, *args, **kwargs)

		self.SetLexer(wx.stc.STC_LEX_CPP)
		keywords = [sql.SQL_KW, sql.SQL_DBO, sql.SQL_PLD, sql.SQL_UKW1, sql.SQL_UKW2, sql.SQL_UKW4]

		allwords= list()
		for group in keywords:
			words = shlex.split(group[1])
			for word in words:
				allwords.append(word)

		self.SetKeyWords(1, keyWords=' '.join(allwords))

		self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
		self.SetMarginMask(1, wx.stc.STC_STYLE_LINENUMBER)
		self.SetMarginWidth(1, 25)

		self.SetProperty('fold', "0")

		self.AppendText('SELECT * FROM youcallmd.users LIMIT 0, 1000')

		self.Update()

class QueryEditor(wx.Panel):
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(QueryEditor, self).__init__(parent, id, *args, **kwargs)

		self.queryEditor = QueryEditorTextCtrl(self, wx.ID_ANY)

		self.SetBackgroundColour(wx.Colour(169,169,169))
		
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
