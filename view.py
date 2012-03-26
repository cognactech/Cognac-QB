import wx

class CQBMenu(wx.MenuBar):
	''' '''
	
	instances = {}
	@staticmethod
	def instance(parent, id):
		''' Returns a new instance or previosly generated one if found '''
		if id in CQBMenu.instances:
			return CQBMenu.instances[id]
		CQBMenu.instances[id] = CQBMenu(parent, id)
		return CQBMenu.instances[id]

	def __init__ (self, frame=None, *args, **kwargs):
		''' '''
		super(CQBMenu, self).__init__(*args, **kwargs)
		
		self.menus = {
			'&File': (
				(wx.ID_ANY, '&Run Query\tCtrl+R', 'Run Query', wx.EVT_MENU, frame.query.runQuery),
				(),
				(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Cognac Query Browser', wx.EVT_MENU, frame.quitApplication)
			),
			"&Debug": (
				(wx.ID_ANY, "&Namespace Viewer", "Open Namespace Viewer", wx.EVT_MENU, frame.showPyShell),
				(wx.ID_ANY, "&Python Shell", "Open Python Shell", wx.EVT_MENU, frame.showPyFilling)
			)
		}

		for key, menu in self.menus.items():
			Menu = wx.Menu()
			for menuData in menu:
				if len(menuData) > 0:
					id, command, label, event_id, event_callback = list(menuData)
					item = Menu.Append(id, command, label)
					try:
						for callback in event_callback:
							frame.Bind(event_id, callback, item)
					except:
						frame.Bind(event_id, event_callback, item)
				else:
					Menu.AppendSeparator()
			self.Append(Menu, key)
		frame.SetMenuBar(self)

class CQBToolbar():
	''' '''
	
	@staticmethod
	def load(parent, more_items=()):
		toolbar_items = (
			(wx.ID_ANY, "Run Query", "Run Query", "images/run.png", wx.EVT_MENU, parent.query.runQuery),
			(wx.ID_ANY, "Stop Query", "Cancel the execution of the current query", "images/stop.png", wx.EVT_MENU, parent.query.cancelQuery)
		)

		toolbar_items = toolbar_items + more_items

		toolbar = parent.CreateToolBar()
		for item in toolbar_items:
			menuitem = toolbar.AddSimpleTool(-1, wx.Bitmap(item[3]), item[1], item[2])
			parent.Bind(item[4], item[5], menuitem)
		toolbar.Realize()

		return toolbar
