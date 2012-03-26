import wx
import wx.dataview as dv

class CQBData(object):
	''' '''
	def __init__(self, data={}):
		''' '''
		self.data = data

class BrowserMenu():
	''' '''
	
	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(BrowserMenu, self).__init__(parent, id, *args, **kwargs)

class BrowserTree(dv.DataViewTreeCtrl):
	''' '''
	
	def __init__(self, parent, *args, **kwargs):
		''' '''
		super(BrowserTree, self).__init__(parent, *args, **kwargs)
		
		self.__collapsing = False

	def build(self, profile, tree):

		isz = (16, 16)
		il = wx.ImageList(*isz)
		fldridx = il.AddIcon(wx.ArtProvider.GetIcon(wx.ART_FOLDER, wx.ART_OTHER, isz))
		fldropenidx = il.AddIcon(wx.ArtProvider.GetIcon(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
		fileidx = il.AddIcon(wx.ArtProvider.GetIcon(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
		self.SetImageList(il)

		self.root = self.AppendContainer(dv.NullDataViewItem, profile, fldridx, fldropenidx)

		for d, t in tree.items():
			parent = self.AppendContainer(self.root, d, fldridx, fldropenidx)
			for i in t:
				self.AppendItem(parent, i[0], fileidx, fileidx)
