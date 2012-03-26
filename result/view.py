import wx, wx.grid
import wx.dataview as dv

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

		self.SetTable(table)
		
		self.SetRowLabelSize(25)
		
		self.SetColLabelAlignment(0, 1)
		#self.AutoSizeColumns(setAsMin=True)
		self.SetDefaultCellOverflow(False)

class ResultList(dv.DataViewListCtrl):
	''' '''
	
	def __init__ (self, parent, id, field_names=(''), results=((''),), *args, **kwargs):
		''' '''
		super(ResultList, self).__init__(parent, id, *args, **kwargs)

		for field in field_names:
			self.AppendTextColumn(field)

		for result in results:
			self.AppendItem(result)
