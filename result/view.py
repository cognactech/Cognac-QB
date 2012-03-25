import wx, wx.grid

class ResultMenu():
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(ResultMenu, self).__init__(parent, id, *args, **kwargs)

class ResultToolbar():
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(ResultToolbar, self).__init__(parent, id, *args, **kwargs)

class ResultGrid(wx.grid.Grid):
	''' '''
	
	def __init__ (self, parent, id, table=None, *args, **kwargs):
		''' '''
		super(ResultGrid, self).__init__(parent, id, *args, **kwargs)
		
		self.SetBackgroundColour(wx.Colour(0,66,56))

		self.SetTable(table)

		box = wx.BoxSizer()
		box.Add(self, 1, wx.EXPAND)
		self.SetSizer(box)
		
		self.HideRowLabels()
		
		self.SetColLabelAlignment(0, 1)
		self.AutoSizeColumns(setAsMin=False)
		self.SetDefaultCellOverflow(False)

		self.Fit()