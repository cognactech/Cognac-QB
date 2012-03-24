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
		super(CQBDBrowser, self).__init__(parent, *args, **kwargs)
		
		self.__collapsing = False
		
		self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
		self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapseItem)
