#! /usr/bin/python

import wx
import wx.grid

class CQBQueryResult(wx.grid.PyGridTableBase):

	def __init__ (self, field_names, results, *args, **kwargs):
		self.field_names = field_names
		self.results = results
		super(__init__, self, *args, **kwargs)
	
	def GetNumberRows(self):
		return len(self.results)
	
	def GetNumberCols(self):
		return len(self.results[0])
	
	def IsEmptyCell(self, row, col):
		if self.results[row][col]
			return False
		return True
	
	def GetValue(self, row, col):
		return self.results[row][col]
	
	def SetValue(self, row, col, value):
		pass
	
	def GetColLabelValue(self, col):
		if self.field_names:
			return self.field_names[col]
	
	def GetRowLabelValue(self, row):
		return row
	
