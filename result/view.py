class ResultMenu(CQBMenu)
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(ResultMenu, self).__init__(parent, id, *args, **kwargs)

class ResultToolbar(CQBToolbar)
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(ResultToolbar, self).__init__(parent, id, *args, **kwargs)

class ResultGrid(wx.grid.Grid):
	''' '''
	
	def __init__ (self, parent, id, field_names=(), results=[], *args, **kwargs):
		''' '''
		super(ResultGrid, self).__init__(parent, id, *args, **kwargs)
		
		table = ResultTable(field_names, results)
		self.SetTable(table)

		box = wx.BoxSizer()
		box.Add(self, 1, wx.EXPAND)
		self.SetSizer(box)
		
		self.HideRowLabels(True)
		
		self.SetColLabelAlignment(0, 1)
		self.AutoSizeColumns(setAsMin=False)
		self.SetDefaultCellOverflow(False)

		self.Fit()