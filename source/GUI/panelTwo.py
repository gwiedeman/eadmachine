import wx
from resource_path import resource_path
from EADtoSpreadsheet import EADtoSpreadsheet
import xml.etree.cElementTree as ET
from EADtoSpreadsheet.func.encoding import strip_non_ascii
from threading import Thread
from wx.lib.pubsub import pub
import sys

########################################################################
class ProgressBarThread(Thread):
    """Test Worker Thread Class."""
 
    #----------------------------------------------------------------------
    def __init__(self, EAD_xml):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._EAD_xml = EAD_xml
        self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        
        generic_error = "I'm afraid there has been an unhandled error. This may be a problem with EADMachine, or you may be using uncommon EAD encoding that is not supported. If you would like to help fix these issues, please send the error_log.txt file along with the XML files you are using to the developer at GWiedeman@Albany.edu."
		
        try:		
			output_spread_bad = EADtoSpreadsheet.EADtoSpreadsheet(self._EAD_xml)
			comp_spread = strip_non_ascii(output_spread_bad)
			wx.CallAfter(pub.sendMessage, "finish_spread", output_spread = comp_spread, EAD_xml = self._EAD_xml)
        except:
			error_log = open("error_log.txt", "a")
			error_log.write("EAD to Spreadsheet." + traceback.format_exc() + "######################################################################################")
			error_log.close()
			print  traceback.format_exc()
			errorbox = wx.MessageDialog(None, generic_error, "Unhandled Error!", wx.OK | wx.ICON_ERROR)
			errorbox.ShowModal()

 
########################################################################
class MyProgressDialog(wx.Dialog):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, EAD_xml):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Creating EAD file...", size=(500,150))
        self.count = 0
		
        self.count_file = ET.ElementTree(file=EAD_xml)
        count_file_root = self.count_file.getroot()
        count_number = 8
        """
        for all_tags in count_file_root.iter():
			if all_tags.tag.endswith('dsc'):
				for top_level in all_tags:
					count_number = count_number + 1
        """
        self.progress = wx.Gauge(self, range=count_number)
		
        self.progresstxt = wx.StaticText(self, id=-1, label="Creating Spreadsheet file...", style=wx.ALIGN_CENTER)
 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.progress, 0, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.progresstxt, 0, wx.ALL | wx.EXPAND, 10)
        
        # create a pubsub receiver
        pub.subscribe(self.updateProgress, "update_spread")
		
		
        self.SetSizer(self.sizer)
		
        self.Bind(wx.EVT_CLOSE, self.OnClose)
		
    def OnClose(self, event):
        ProgressBarThread.stopped = True
        self.Destroy()
 
    #----------------------------------------------------------------------
    def updateProgress(self, msg):
        """"""
        self.count += 1

        #count_file = ET.ElementTree(file=self.EAD_xml)
        count_file_root = self.count_file.getroot()
        count_number = 8
        """
        for all_tags in count_file_root.iter():
			if all_tags.tag.endswith('dsc'):
				for top_level in all_tags:
					count_number = count_number + 1
        """		
        if self.count >= count_number:
			self.Destroy()
		
        self.progress.SetValue(self.count)
        self.sizer.Hide(self.progresstxt)
        self.progresstxt = wx.StaticText(self, id=-1, label=msg, style=wx.ALIGN_CENTER, pos=(20, 30))
        self.sizer.Add(self.progresstxt, 0, wx.ALL | wx.EXPAND, 10)
        print msg
 
########################################################################
class TabPanel(wx.Panel):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
 
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
 
        self.panel_one = FirstPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
		
        pub.subscribe(self.saveFileEAD_xml, "finish_spread")
		
    def convertClick(self, event, EAD_xml):
        self.panel_one.Hide()
                
        EAD_xml = self.panel_one.EADinput.GetValue()
		
        btn = event.GetEventObject()
        btn.Disable()
 
        ProgressBarThread(EAD_xml)
        dlg = MyProgressDialog(EAD_xml)
        dlg.ShowModal()
 
        btn.Enable()
		
    def saveFileEAD_xml(self, output_spread, EAD_xml):
		
        if EAD_xml.find("/") != -1:
			fileName = EAD_xml[EAD_xml.index("/") + len("/"):]
        else:
			fileName = EAD_xml.split(".", 1)[0] + "-EM"
			
        saveFileDialog = wx.FileDialog(self, "Save As", "", fileName, 
                                       "XML files (*.xml)|*.xml", 
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        result = saveFileDialog.ShowModal()
        inFile = saveFileDialog.GetPath()
        saveFileDialog.Destroy()
        if result == wx.ID_OK:          #Save button was pressed
			#with open("parse_test.txt", 'w') as f:  
				#f.write(output_spread)  
			output3 = ET.fromstring(output_spread)
			output4 = ET.ElementTree(output3)
			output4.write(inFile, xml_declaration=True, encoding='utf-8', method='xml')
        elif result == wx.ID_CANCEL:    #Either the cancel button was pressed or the window was closed
            pass
            
        
        self.panel_one.Show()
		
########################################################################
class FirstPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        
        vbox = wx.BoxSizer(wx.VERTICAL)
		
        logobox = wx.BoxSizer(wx.HORIZONTAL)
        titleImage = wx.StaticBitmap(self, size=(360,65))
        titleImage.SetBitmap(wx.Bitmap(resource_path('resources/logotitle.gif')))
        logobox.Add(titleImage, 1, wx.TOP | wx.EXPAND, 10)
		
        instuctbox = wx.BoxSizer(wx.HORIZONTAL)
        instructtxt = wx.StaticText(self, id=-1, label="<EAD>      to      Spreadsheet", style=wx.ALIGN_CENTER)
        instuctbox.Add(instructtxt, 1, wx.ALL | wx.EXPAND, 5)
		
        middlebox = wx.BoxSizer(wx.VERTICAL)
        inputtxtbox = wx.BoxSizer(wx.HORIZONTAL)
                
        EADtxt = wx.StaticText(self, id=-1, label="Select EAD file:")
        inputtxtbox.Add(EADtxt, 1, wx.TOP | wx.EXPAND, 10)
                
        inputfilebox = wx.BoxSizer(wx.HORIZONTAL)
        self.EADinput = wx.TextCtrl(self, size=(450,25))        
        browseButton = wx.Button(self, label='Browse...', size=(75, 28))
        inputfilebox.Add(self.EADinput, 1, wx.ALL | wx.EXPAND, 1)
        inputfilebox.Add(browseButton, 1, wx.ALL | wx.EXPAND, 1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.browseClick(event, self.EADinput), browseButton)
                    
        #spacerbox = wx.BoxSizer(wx.VERTICAL)
            
        middlebox.Add(inputtxtbox, 1, wx.ALL | wx.EXPAND, 1)
        middlebox.Add(inputfilebox, 1, wx.BOTTOM | wx.EXPAND, 30)
		#middlebox.Add(spacerbox, 1, wx.ALL | wx.EXPAND, 1)   		
        
		
        convertbuttonbox = wx.BoxSizer(wx.HORIZONTAL)
        convertbuttonbox.Add((453, 10))
        convertButton = wx.Button(self, label='Convert', size=(175, 28))
        convertbuttonbox.Add(convertButton, 1, wx.RIGHT | wx.EXPAND, 1.5)
        self.Bind(wx.EVT_BUTTON, lambda event: parent.convertClick(event, self.EADinput), convertButton)
		
        vbox.Add(logobox, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(instuctbox, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(middlebox, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(convertbuttonbox, 1, wx.ALL | wx.EXPAND, 5)
		
        self.SetSizer(vbox)
        vbox.Fit(self)
		
    def browseClick(self, event, FAinput):
        inputBox = wx.FileDialog(None, "Select EAD file:", 'Select', '*.xml')
        if inputBox.ShowModal()==wx.ID_OK:
			inputFile = inputBox.GetPath()
        self.EADinput.Clear()
        self.EADinput.AppendText(inputFile)