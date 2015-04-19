import wx
 
class TabPanel(wx.Panel):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
 
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
 
        titleImage = wx.StaticBitmap(self, pos=(110,0), size=(360,100))
	titleImage.SetBitmap(wx.Bitmap('images/logotitle.gif'))
        instructtxt = wx.StaticText(self, id=-1,  pos=(130,100), label="Batch Migrate EAD2002 to EAD3", name="")