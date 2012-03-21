#! /usr/bin/python

import sys, wx

class CQBFrame(wx.Frame):
    panel1 = None
    panel2 = None
    
    def __init__(self, *args, **kwargs):
        super(CQBFrame, self).__init__(*args, **kwargs)
        self.SetTitle('Cognac Query Browser')
        self.SetSize((800, 600))
        self.InitUI()
        self.Center()
        self.Show(True)
    
    def InitUI(self):
        splitter = wx.SplitterWindow(self, -1)
        
        self.panel1 = wx.Panel(splitter, -1, size=(-1, 200))
        self.panel1.SetBackgroundColour(wx.LIGHT_GREY)
        
        self.panel2 = wx.Panel(splitter, -1, size=(-1, 200))
        self.panel2.SetBackgroundColour(wx.WHITE)
        
        splitter.SplitVertically(self.panel1, self.panel2)
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        
        newConnectionItem = fileMenu.Append(wx.ID_ANY, '&New Connection\tCtrl+N', 'New Connection')
        queryEditorItem = fileMenu.Append(wx.ID_ANY, '&Query Editor\tCtrl+E', 'Query Editor')
        quitAppItem = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit Cognac Query Browser')
        
        menubar.Append(fileMenu, '&File')
        
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.newConnection, newConnectionItem)
        self.Bind(wx.EVT_MENU, self.newQuery, queryEditorItem)
        self.Bind(wx.EVT_MENU, self.quitApplication, quitAppItem)
    
    def newQuery(self, e):
        QCBNewQuery(self.panel2)
    
    def newConnection(self, e):
        CQBNewConnection(self)
    
    def quitApplication(self, e):
        self.Close()
    
class QCBNewQuery (wx.Panel):
    editor = None
    
    def __init__(self, *args, **kwargs):
        super(QCBNewQuery, self).__init__(*args, **kwargs)
        self.SetSize((400, 400))
        self.Center()
        
        self.addCtrls()
        
        self.Show(True)
    
    def addCtrls (self):
        self.editor = wx.TextCtrl(self, -1, "", size=(-1, 200))
        

class CQBNewConnection(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(CQBNewConnection, self).__init__(*args, **kwargs)
        self.SetTitle('New Connection')
        self.SetSize((400, 400))
        self.Center()
        self.Show(True)
    
class QCB(wx.App):
    def OnInit(self):
        mainFrame = CQBFrame(None)
        self.SetTopWindow(mainFrame)
        return True

if __name__ == '__main__':
    app = QCB(0)       # Create an instance of the application class
    app.MainLoop()     # Tell it to start processing events