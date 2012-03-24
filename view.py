import wx

class CQBMenu(wx.Menu):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(parent, id):
		''' Returns a new instance or previosly generated one if found '''
		if id in self.instances:
			return self.instances[id]
		self.instances[id] = Query(parent, id)
		return self.instances[id]

	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(CQBMenu, self).__init__(parent, id, *args, **kwargs)
		
		self.menus = {
			'&File': (
				(wx.ID_ANY, '&Run Query\tCtrl+R', 'Run Query', wx.EVT_MENU, self.queryEditorPanel.triggerQueryRun),
				(wx.ID_ANY, '&Refresh\tShift+Ctrl+R', 'Refresh Results', wx.EVT_MENU, self.queryEditorPanel.triggerRefresh),
				(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Cognac Query Browser', wx.EVT_MENU, [self.quitApplication, self.queryEditorPanel.quitApplication])
			)
		}

		menubar = wx.MenuBar()
		for key, menu in self.menus.items():
			Menu = wx.Menu()
			for id, command, label, event_id, event_callback in menu:
				item = Menu.Append(id, command, label) 
				try:
					for callback in event_callback:
						self.Bind(event_id, callback, item)
				except:
					self.Bind(event_id, event_callback, item)
			menubar.Append(Menu, key)
		self.SetMenuBar(menubar)

class CQBToolbar():
	''' '''
	
	instances = {}
	@staticmethod
	def instance(parent, id):
		''' Returns a new instance or previosly generated one if found '''
		if id in self.instances:
			return self.instances[id]
		self.instances[id] = Query(parent, id)
		return self.instances[id]

	def __init__ (self, parent, id, *args, **kwargs):
		''' '''
		super(CQBMenu, self).__init__(parent, id, *args, **kwargs)
		
		self.toolbar_items = (
			(wx.ID_ANY, "Run Query", "Run Query", "images/run.png", wx.EVT_MENU, self.queryEditorPanel.triggerQueryRun),
			(wx.ID_ANY, "Stop Query", "Cancel the execution of the current query", "images/stop.png", wx.EVT_MENU, self.queryEditorPanel.triggerQueryStop),
			(wx.ID_ANY, "Load File", "Load SQL from a file", "images/run.png", wx.EVT_MENU, self.queryEditorPanel.loadQueryDialog),
		)

		self.toolbar = self.CreateToolBar()
		for item in self.toolbar_items:
			menuitem = self.toolbar.AddSimpleTool(-1, wx.Bitmap(item[3]), item[1], item[2])
			self.Bind(item[4], item[5], menuitem)
		self.toolbar.Realize()
