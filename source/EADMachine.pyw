import wx
import GUI.panelOne, GUI.panelTwo, GUI.panelThree
from subprocess import Popen
from GUI.resource_path import resource_path
 
########################################################################
class Notebook(wx.Notebook):
    """
    Notebook class
    """
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
 
        		
		# Spreadsheet to EAD Tab
        tabOne = GUI.panelOne.TabPanel(self)
        self.AddPage(tabOne, "Spreadsheet to EAD")
 
        # EAD to Spreadsheet Tab
        tabTwo = GUI.panelTwo.TabPanel(self)
        self.AddPage(tabTwo, "EAD to Spreadsheet")
 
        # EAD2002 to EAD3 tab
        #self.AddPage(GUI.panelThree.TabPanel(self), "EAD2002 to EAD3")
 
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
 
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        #print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()
 
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        #print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()
 
 
########################################################################
class mainFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""        
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          "EADMachine",
                          size=(600,400)
                          )
        panel = wx.Panel(self)

	favicon = wx.Icon(resource_path('resources/em.gif'), wx.BITMAP_TYPE_GIF, 16, 16)
	self.SetIcon(favicon)
	
	menuBar = wx.MenuBar()
		
	fileButton = wx.Menu()
	helpButton = wx.Menu()
		
	exitItem = wx.MenuItem(fileButton, wx.ID_EXIT, 'Quit\tCtrl+Q')
	aboutItem = wx.MenuItem(helpButton, wx.ID_ABOUT, 'About\tCtrl+B')
	documentItem = wx.MenuItem(helpButton, wx.ID_HELP, 'Documentation\tCtrl+D')
	fileButton.AppendItem(exitItem)
	helpButton.AppendItem(aboutItem)
	helpButton.AppendItem(documentItem)
		
		
	menuBar.Append(fileButton, "File")
	menuBar.Append(helpButton, "Help")
		
	self.SetMenuBar(menuBar)
		
	self.Bind(wx.EVT_MENU, self.Quit, exitItem)
	self.Bind(wx.EVT_MENU, self.AboutBox, aboutItem)
	self.Bind(wx.EVT_MENU, self.Document, documentItem)
 
        #import error_dialog
        notebook = Notebook(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        panel.Layout()
        self.Centre()
 
        self.Show()
		
    def Quit(self, e):
        self.Close()
			
    def AboutBox(self, e):
			
        description = """	EADMachine is an easy EAD creation tool for 
Archives and Special Collections that uses a XML template 
to conform to your local EAD implementations.

Use either the default EAD2002 or EAD3 templates or use 
one of your own local EAD files. EADMachine will match you 
new data exactly to your EAD template.
	"""

        licence = """EADMachine is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 3 of the License, 
or (at your option) any later version.

EADMachine is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with File Hunter; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
Suite 330, Boston, MA  02111-1307  USA"""


        info = wx.AboutDialogInfo()
            
        info.SetIcon(wx.Icon(resource_path('resources/em.gif'), wx.BITMAP_TYPE_GIF))
        info.SetName('EADMachine')
        info.SetVersion('0.7 - beta')
        info.SetDescription(description)
        info.SetCopyright('(C) 2014 - 2015 Gregory Wiedeman')
        info.SetWebSite('https://github.com/gwiedeman/eadmachine')
        info.SetLicence(licence)

			
        wx.AboutBox(info)
			
    def Document(self, e):
        Popen("README.html",shell=True)
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = mainFrame()
    app.MainLoop()
