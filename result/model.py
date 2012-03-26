import wx, wx.grid
import wx.dataview as dv

class ResultListModel():
	''' '''
	
	def __init__ (self, *args, **kwargs):
		''' '''
		pass
		#super(ResultListModel, self).__init__(*args, **kwargs)

class ResultGridTable(wx.grid.PyGridTableBase):
	'''	'''
	
	def __init__ (self, field_names, results, *args, **kwargs):
		''' '''
		super(ResultGridTable, self).__init__(*args, **kwargs)
		self.field_names = field_names
		self.results = results
	
	def GetNumberRows(self):
		''' '''
		return len(self.results)
	
	def GetNumberCols(self):
		''' '''
		return len(self.results[0])
	
	def IsEmptyCell(self, row, col):
		''' '''
		row = self.results[row]
		if col in row:
			return False
		return True
	
	def GetValue(self, row, col):
		''' '''
		row = self.results[row]
		if row[col] == None and row[col] <= 0:
			return '[NULL]'
		else:
			return row[col]
	
	def SetValue(self, row, col, value):
		''' '''
		pass
	
	def GetColLabelValue(self, col):
		''' '''
		if self.field_names:
			return self.field_names[col]
	
	def GetRowLabelValue(self, row):
		''' '''
		return ' '

	def Clear(self):
		''' '''
		self.field_names = []
		self.results = []

	def SetTable(self, object, *attributes):
		''' '''
		self.tableRef = weakref.ref(object)
		return wxGrid.SetTable(self, object, *attributes)
	
	def GetTable(self):
		''' '''
		return self.tableRef()
