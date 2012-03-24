import wx

class BrowserMenu():
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(BrowserMenu, self).__init__(parent, id, *args, **kwargs)

class BrowserToolbar():
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(BrowserToolbar, self).__init__(parent, id, *args, **kwargs)

class BrowserTree(wx.TreeCtrl):
	''' '''
	
	def __init__(self, parent, *args, **kwargs):
		''' '''
		super(BrowserTree, self).__init__(parent, *args, **kwargs)
		
		self.__collapsing = False
		
		self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
		self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapseItem)

	def OnExpandItem(self, e):
		''' '''
		try:
			data = self.GetPyData(e.GetItem())
			
			if data.data['database'] == False and data.data['table'] == False:
				print 'pass'
				
			elif data.data['database'] == True:
				self.parent.useDatabase('youcallmd')
				tables = self.parent.getTables()
		
				data = CQBData(data={'database': False, 'table': True})
				for table in tables[1]:
					item = self.AppendItem(e.GetItem(), table[0], data=wx.TreeItemData(data))
					self.SetItemHasChildren(item, True)
	
			elif data.data['database'] == False:
				print 'open table'
		
		except Exception, exc:
			result = wx.MessageBox(str(exc), "Database Error", wx.OK | wx.ICON_ERROR)
		finally:
			e.Skip()

	def OnCollapseItem(self, e):
		''' '''
		
		if self.__collapsing:
			e.Veto()
		else:
			self.__collapsing = True
			pass
			self.__collapsing = False
