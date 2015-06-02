import wx
from resource_path import resource_path
from subprocess import Popen
from SpreadsheettoEAD.func.globals import init
import SpreadsheettoEAD.func.globals
import xml.etree.cElementTree as ET
import wx.lib.scrolledpanel as scrolled
from SpreadsheettoEAD import SpreadsheettoEAD
import traceback
import sys

from threading import Thread
from wx.lib.pubsub import pub

########################################################################
class ProgressBarThread(Thread):
    """Test Worker Thread Class."""
 
    #----------------------------------------------------------------------
    def __init__(self, input_xml, template_xml):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._input_xml = input_xml
        self._template_xml = template_xml
        self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        generic_error = "I'm afraid there has been an unhandled error. This may be a problem with EADMachine, or you may be using uncommon EAD encoding that is not supported. If you would like to help fix these issues, please send the error_log.txt file along with the XML files you are using to the developer at GWiedeman@Albany.edu."
		
        try:
			comp_EAD, comp_HTML = SpreadsheettoEAD.SpreadsheettoEAD(self._input_xml, self._template_xml)
			wx.CallAfter(pub.sendMessage, "finish_EAD", output_EAD = comp_EAD, output_HTML = comp_HTML)
        except:
			error_log = open("error_log.txt", "a")
			error_log.write("Spreadsheet to EAD." + traceback.format_exc() + "######################################################################################")
			error_log.close()
			print traceback.format_exc()
			errorbox = wx.MessageDialog(None, generic_error, "Unhandled Error!", wx.OK | wx.ICON_ERROR)
			errorbox.ShowModal()

	
       

 
########################################################################
class MyProgressDialog(wx.Dialog):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Creating EAD file...", size=(500,150))
        self.count = 0
 
        if "ask_html" in SpreadsheettoEAD.func.globals.new_elements:
			self.progress = wx.Gauge(self, range=15)
        else:
			self.progress = wx.Gauge(self, range=13)
		
        self.progresstxt = wx.StaticText(self, id=-1, label="Creating EAD file...", style=wx.ALIGN_CENTER)
 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.progress, 0, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.progresstxt, 0, wx.ALL | wx.EXPAND, 10)
        
        # create a pubsub receiver
        pub.subscribe(self.updateProgress, "update")
		
		
        self.SetSizer(self.sizer)
		
        self.Bind(wx.EVT_CLOSE, self.OnClose)
		
    def OnClose(self, event):
        ProgressBarThread.stopped = True
        self.Destroy()
 
    #----------------------------------------------------------------------
    def updateProgress(self, msg):
        """"""
        self.count += 1
 
        if "ask_html" in SpreadsheettoEAD.func.globals.new_elements:
			if self.count >= 15:
				self.Destroy()
        else:
			if self.count >= 13:
				self.Destroy()
		
        self.progress.SetValue(self.count)
        self.sizer.Hide(self.progresstxt)
        self.progresstxt = wx.StaticText(self, id=-1, label=msg, style=wx.ALIGN_CENTER, pos=(20, 30))
        self.sizer.Add(self.progresstxt, 0, wx.ALL | wx.EXPAND, 10)
        print msg
 
########################################################################
class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        
        #global variables
        init()
        
        self.panel_one = FirstPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        #self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        passID = ""
		
        pub.subscribe(self.saveFile, "finish_EAD")
 
    def nextClick(self, event, FAinput, Teminput):
        self.panel_one.Hide()
        self.panel_two = NextPanel(self)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.panel_two.Show()
        self.Layout()
        
    def goClick(self, event, input_xml, template_xml, cID):
        self.panel_two.Hide()
        if cID.startswith('nam_'):
            self.passID = cID.replace('nam_', '')
        else:
            self.passID = cID
		
        
        
        btn = event.GetEventObject()
        #btn.Disable()
 
        ProgressBarThread(input_xml, template_xml)
        dlg = MyProgressDialog()
        dlg.ShowModal()
        #output_EAD, output_HTML = SpreadsheettoEAD.SpreadsheettoEAD(input_xml, template_xml)
        
 
        btn.Enable()
		
        
		
    def saveFile(self, output_EAD, output_HTML):
        saveFileDialog = wx.FileDialog(self, "Save As", "", self.passID, 
                                       "XML files (*.xml)|*.xml", 
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        result = saveFileDialog.ShowModal()
        inFile = saveFileDialog.GetPath()
        saveFileDialog.Destroy()
        if result == wx.ID_OK:          #Save button was pressed
            #output_element = ET.fromstring(output_EAD)
            #output1 = ET.ElementTree(output_element)
            #output1.write(inFile, xml_declaration=True, encoding='utf-8', method='xml')
            #with open(inFile, 'w') as f:
				#f.write('<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE ead SYSTEM "ead.dtd">')
				#output1.write(f, 'utf-8')
            with open(inFile, "w") as f:
				#f.write('<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE ead SYSTEM "ead.dtd">')
				#output_EAD.write(f, 'utf-8')
				f.write(output_EAD)
        elif result == wx.ID_CANCEL:    #Either the cancel button was pressed or the window was closed
            pass
            
        if output_HTML == False:
            pass
        else:
            saveFileDialog2 = wx.FileDialog(self, "Save As", "", self.passID, 
                                           "HTML files (*.html)|*.html", 
                                           wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            result2 = saveFileDialog2.ShowModal()
            inFile2 = saveFileDialog2.GetPath()
            saveFileDialog2.Destroy()
            if result2 == wx.ID_OK:          #Save button was pressed
                output_web = ET.fromstring(output_HTML)
                output2 = ET.ElementTree(output_web)
                #output2.write(inFile2, xml_declaration=False)
                with open(inFile2, 'w') as g:
					g.write('<!DOCTYPE html>')
					output2.write(g, 'utf-8')
				#output_HTML.write(inFile2, xml_declaration=True, encoding='utf-8', method='xml')
				#with open(inFile2, "w") as g:
					#g.write(output_HTML)
            elif result2 == wx.ID_CANCEL:    #Either the cancel button was pressed or the window was closed
                pass
		SpreadsheettoEAD.func.globals.new_elements = [w for w in SpreadsheettoEAD.func.globals.new_elements if w != "add_unitid"]
		SpreadsheettoEAD.func.globals.new_elements = [x for x in SpreadsheettoEAD.func.globals.new_elements if x != "ask_ualbany"]
		SpreadsheettoEAD.func.globals.new_elements = [y for y in SpreadsheettoEAD.func.globals.new_elements if y != "ask_fileunitid"]
		SpreadsheettoEAD.func.globals.new_elements = [z for z in SpreadsheettoEAD.func.globals.new_elements if z != "ask_html"]
        self.panel_one.Show()
 
########################################################################
class FirstPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
		
        def scale_bitmap(bitmap, width, height):
			image = wx.ImageFromBitmap(bitmap)
			image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
			result = wx.BitmapFromImage(image)
			return result
        
        vbox = wx.BoxSizer(wx.VERTICAL)
		
        logobox = wx.BoxSizer(wx.HORIZONTAL)
        titleImage = wx.StaticBitmap(self, size=(360,65))
        titleImage.SetBitmap(wx.Bitmap(resource_path('resources/logotitle.gif')))
        logobox.Add(titleImage, 1, wx.TOP | wx.EXPAND, 10)
		
        instuctbox = wx.BoxSizer(wx.HORIZONTAL)
        instructtxt = wx.StaticText(self, id=-1, label="Spreadsheet     +     XML Template     =     <EAD> and <HTML>", style=wx.ALIGN_CENTER)
        instuctbox.Add(instructtxt, 1, wx.ALL | wx.EXPAND, 5)
		
        middlebox = wx.BoxSizer(wx.VERTICAL)
        inputtxtbox = wx.BoxSizer(wx.HORIZONTAL)
                
        FAtxt = wx.StaticText(self, id=-1, label="Select Finding Aid Data exported from spreadsheet:")
        inputtxtbox.Add(FAtxt, 1, wx.TOP | wx.EXPAND, 10)
                
        inputfilebox = wx.BoxSizer(wx.HORIZONTAL)
        self.FAinput = wx.TextCtrl(self, size=(450,25))        
        browseButton = wx.Button(self, label='Browse...', size=(75, 28))
        inputfilebox.Add(self.FAinput, 1, wx.ALL | wx.EXPAND, 1)
        inputfilebox.Add(browseButton, 1, wx.ALL | wx.EXPAND, 1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.browseClick(event, self.FAinput), browseButton)
                    
        temtxtbox = wx.BoxSizer(wx.HORIZONTAL)
        Temtxt = wx.StaticText(self, id=-1, label="Select Template:")
        temtxtbox.Add(Temtxt, 1, wx.TOP | wx.EXPAND, 1)
                
        temfilebox = wx.BoxSizer(wx.HORIZONTAL)
        self.Teminput = wx.TextCtrl(self, size=(450,25))
        tempButton = wx.Button(self, label='Browse...')
        temfilebox.Add(self.Teminput, 1, wx.ALL | wx.EXPAND, 1)
        temfilebox.Add(tempButton, 1, wx.ALL | wx.EXPAND, 1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.tempClick(event, self.Teminput), tempButton)
            
        middlebox.Add(inputtxtbox, 1, wx.ALL | wx.EXPAND, 1)
        middlebox.Add(inputfilebox, 1, wx.ALL | wx.EXPAND, 1)
        middlebox.Add(temtxtbox, 1, wx.ALL | wx.EXPAND, 1)
        middlebox.Add(temfilebox, 1, wx.BOTTOM | wx.EXPAND, 1)
                
        
		
        nextbuttonbox = wx.BoxSizer(wx.HORIZONTAL)
        nextbuttonbox.Add((453, 10))
        nextButton = wx.Button(self, label='Next >', size=(175, 28))
        nextbuttonbox.Add(nextButton, 1, wx.RIGHT | wx.EXPAND, 1.5)
        self.Bind(wx.EVT_BUTTON, lambda event: parent.nextClick(event, self.FAinput, self.Teminput), nextButton)
		
        vbox.Add(logobox, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(instuctbox, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(middlebox, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(nextbuttonbox, 1, wx.ALL | wx.EXPAND, 5)
		
        self.SetSizer(vbox)
        vbox.Fit(self)
        
        
        
    def browseClick(self, event, FAinput):
        inputBox = wx.FileDialog(None, "Select Finding Aid Data:", 'Select', '*.xml')
        if inputBox.ShowModal()==wx.ID_OK:
            inputFile = inputBox.GetPath()
        FAinput.Clear()
        FAinput.AppendText(inputFile)
                    
            
    def tempClick(self, event, Teminput):
        tempBox = wx.FileDialog(None, "Select Template:", 'Select', '*.xml')
        if tempBox.ShowModal()==wx.ID_OK:
            templateFile = tempBox.GetPath()
            Teminput.Clear()
            Teminput.AppendText(templateFile)
                    
           
            

########################################################################
class NextPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        


        overallbox = wx.BoxSizer()
        verticalbox = wx.BoxSizer(wx.VERTICAL)
        overallbox.Add(verticalbox, 1, wx.LEFT, 5)
        question_count = 0
        
        
        input_xml = parent.panel_one.FAinput.GetValue()
        template_xml = parent.panel_one.Teminput.GetValue()
		
        input_file = ET.ElementTree(file=input_xml)
        template_file = ET.ElementTree(file=template_xml)

        input = input_file.getroot()
        template = template_file.getroot()
		
        #makes error messages show as alert windows instead of printing them
        SpreadsheettoEAD.func.globals.new_elements.append("ask_gui")
		
        if len(input_xml) < 1: #verifies finding aid data file
            from SpreadsheettoEAD.func.messages import error
            error("You failed to enter your Finding Aid Data. The first file must be an XML file exported from the EADMachine spreadsheet. Please save your spreadsheet as an XML file and try again.", False)
            parent.panel_one.Show()
        if len(template_xml) < 1: #verifies template file
            from SpreadsheettoEAD.func.messages import error
            error("You failed to enter an EAD template file. The EAD Template file must be one of the default XML files in the templates folder, or a valid EAD file. Please enter a valid EAD template file and try again.", False)
            parent.panel_one.Show()
        if input.tag != "FindingAid" or input.find('CollectionSheet') is None: #verifies finding aid data file
            from SpreadsheettoEAD.func.messages import error
            error("You entered an incorrect XML file for your Finding Aid Data. The first file must be an XML file exported from the EADMachine spreadsheet. Please save your spreadsheet as an XML file and try again.", False)
            parent.panel_one.Show()
        elif not str(template.tag).endswith("ead"): #verifies template file
            from SpreadsheettoEAD.func.messages import error
            error("You entered an incorrect EAD template file. The EAD Template file must be one of the default XML files in the templates folder, or a valid EAD file. Please enter a valid EAD template file and try again.", False)
            parent.panel_one.Show()
        else:
			
			#removes namespaces
			template.tag = "ead"
			for all_tags in template.iter():
				all_tags.tag = str(all_tags.tag).split("}",1)[-1]
				
				
			if template.find('archdesc') is None: #verifies template file again
				from SpreadsheettoEAD.func.messages import error
				error("You entered an incorrect EAD template file. The EAD Template file must be one of the default XML files in the templates folder, or a valid EAD file. Please enter a valid EAD template file and try again.", False)
				parent.panel_one.Show()
				
			if template[0].tag == "eadheader":
				version = "ead2002"
			else:
				version = "ead3"
				
			"""
			if input.find('CollectionSheet/ProcessedBy') is None:
				pass
			else:
				if input.find('CollectionSheet/ProcessedBy').text:
					if template.find('eadheader/filedesc/titlestmt/author') is None or template.find('frontmatter/titlepage/author') is None:
						if template.find('control/filedesc/titlestmt/author') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_author", "an author", "<author>")
			
			if input.find('CollectionSheet/Subtitle') is None:
				pass
			else:
				if input.find('CollectionSheet/Subtitle').text:
					if template.find('eadheader/filedesc/titlestmt/subtitle') is None or template.find('frontmatter/titlepage/subtitle') is None:
						if template.find('control/filedesc/titlestmt/subtitle') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_subtitle", "a Subtitle", "<subtitle>")

			if input.find('CollectionSheet/Sponsor') is None:
				pass
			else:
				if input.find('CollectionSheet/Sponsor').text:
					if template.find('control/filedesc/titlestmt/sponsor') is None and template.find('eadheader/filedesc/titlestmt/sponsor') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_sponsor", "a Sponsor", "<sponsor>")

			if input.find('CollectionSheet/Edition') is None:
				pass
			else:
				if input.find('CollectionSheet/Edition').text:
					if template.find('control/filedesc/editionstmt') is None and template.find('eadheader/filedesc/editionstmt') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_edition", "an Edition", "<editionstmt>")

			if input.find('CollectionSheet/Publisher/AddressLine') is None:
				if input.find('CollectionSheet/Publisher/PublisherName') is None:
					pass
				else:
					if input.find('CollectionSheet/Publisher/PublisherName').text:
						if template.find('control/filedesc/publicationstmt/publisher') is None and template.find('eadheader/filedesc/publicationstmt/publisher') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_publication", "a Publisher", "<publicationstmt>")
			else:
				if input.find('CollectionSheet/Publisher/PublisherName') is None:
					pass
				else:
					if input.find('CollectionSheet/Publisher/PublisherName').text or input.find('CollectionSheet/Publisher/AddressLine').text:
						if template.find('control/filedesc/publicationstmt/publisher') is None and template.find('eadheader/filedesc/publicationstmt/publisher') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_publication", "a Publisher", "<publicationstmt>")
					
			if input.find('CollectionSheet/PartofSeries') is None:
				pass
			else:
				if input.find('CollectionSheet/PartofSeries').text:
					if template.find('control/filedesc/seriesstmt') is None and template.find('eadheader/filedesc/seriesstmt') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_seriesstmt", "a Series statement", "<seriesstmt>")
			
			if input.find('CollectionSheet/NoteStatements/NoteStatement') is None:
				pass
			else:
				if input.find('CollectionSheet/NoteStatements/NoteStatement').text:
					if template.find('control/filedesc/notestmt') is None and template.find('eadheader/filedesc/notestmt') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_notestmt", "a Note Statement", "<notestmt>")
					
			#EAD2002 only questions:
			if version == "ead2002":
				
				if input.find('CollectionSheet/EADCreator') is None or input.find('CollectionSheet/FindingAidLanguages/FALanguage/Lang') is None:
					pass
				else:
					if input.find('CollectionSheet/EADCreator').text or input.find('CollectionSheet/FindingAidLanguages/FALanguage/Lang').text:
						if template.find('eadheader/profiledesc') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_profile", "EAD languages and/or a creation date", "<profiledesc>")
						
				if input.find('CollectionSheet/EADCreator') is None:
					pass
				else:
					if input.find('CollectionSheet/EADCreator').text:
						if template.find('eadheader/profiledesc/creation') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_eadcre", "an EAD creator", "<creation>")
						
				if input.find('CollectionSheet/FindingAidLanguages/FALanguage/Lang') is None:
					pass
				else:
					if input.find('CollectionSheet/FindingAidLanguages/FALanguage/Lang').text:
						if template.find('eadheader/profiledesc/langusage') is None or template.find('eadheader/profiledesc/langusage/language') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_lang1", "an EAD Language", "<langusage> or <language>")
						
				if input.find('CollectionSheet/StandardConventions/Convention/Citation') is None or input.find('CollectionSheet/LocalConventions/Convention/Citation') is None:
					pass
				else:
					if input.find('CollectionSheet/StandardConventions/Convention/Citation').text or input.find('CollectionSheet/LocalConventions/Convention/Citation').text:
						if template.find('eadheader/profiledesc/descrules') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_descrule", "Descriptive Rules", "<descrules>")
						
				if input.find('CollectionSheet/Revisions/Event/Date') is None:
					pass
				else:
					if input.find('CollectionSheet/Revisions/Event/Date').text:
						if template.find('eadheader/revisiondesc') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_revisions", "Revisions", "<revisiondesc>")
						
			
			#EAD3 only questions:
			if version == "ead3":
			
				if input.find('CollectionSheet/OtherID').text:
					if template.find('control/otherrecordid') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_otherid", "one or more Other IDs", "<otherrecordid>")
			
				if input.find('CollectionSheet/Representation').text:
					if template.find('control/representation') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_rep", "one or more Representations", "<representation>")
			
				if input.find('CollectionSheet/PublicationStatus').text:
					if template.find('control/publicationstatus') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_pubstatus", "a Publication Status", "<publicationstatus>")
						
				if input.find('CollectionSheet/FindingAidLanguages/FALanguage/Lang').text:
					if template.find('control/languagedeclaration') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_langdec", "a Finding Aid Language or a Language Description", "<languagedeclaration>")
						
				if input.find('CollectionSheet/StandardConventions/Convention/Citation').text:
					if template.find('control/conventiondeclaration') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_stancon", "a Standard Convention", "<conventiondeclaration>")
						
				if input.find('CollectionSheet/LocalConventions/Convention/Citation').text:
					if template.find('control/localtypedeclaration') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_localcon", "a Local Convention", "<localtypedeclaration>")
						
				if input.find('CollectionSheet/LocalControls/Control/Term').text:
					if template.find('control/localcontrol') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_localctr", "a Local Control", "<localcontrol>")
						
				if input.find('CollectionSheet/OutsideSources/Source/SourceName').text:
					if template.find('control/sources') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_sources", "external Sources", "<sources>")
						
				if input.find('CollectionSheet/Relations/Relation/RelationEntry').text or input.find('CollectionSheet/Relations/Relation/RelationLink').text or input.find('CollectionSheet/Relations/Relation/RelationNote').text:
					if template.find('archdesc/relations') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_relation", "Relations", "<relations>")					
			"""			
			#<archdesc> questions:
			
			if input.find('CollectionSheet/CollectionID').text:
				if template.find("archdesc/did/unitid") is None:
					question_count = question_count + 1
					self.radio_ask(verticalbox, "add_unitid", "custom", "Your EAD template does not contain a <unitid> within the collection-level <did>. EADMachine recommends that you add a <unitid> here. Would you like to do so?")

			"""
			if input.find('CollectionSheet/DateBulk').text:
				if template.find("archdesc/did/unitdate[@type='bulk']") is None and template.find("archdesc/did/unittitle/unitdate[@type='bulk']") is None and template.find("archdesc/did/unitdate[@unitdatetype='bulk']") is None:
					question_count = question_count + 1
					self.radio_ask(verticalbox, "add_bulkdate", "a collection-level bulk date", "<unitdate type='bulk'>")
			
			if input.find('CollectionSheet/Abstract') is None:
				pass
			else:
				if input.find('CollectionSheet/Abstract').text:
					if template.find("archdesc/did/abstract") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_abstract", "an Abstract", "<abstract>")
			
			if input.find('CollectionSheet/Origins/Origination/Part') is None:
				pass
			else:
				if input.find('CollectionSheet/Origins/Origination/Part').text:
					if template.find('archdesc/did/origination') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_origin", "Origination information", "<origination>")
					
			if template.find('control') is None:
				if input.find('CollectionSheet/PhysicalDescriptionSet/PhysicalDescription/Quantity').text or input.find('CollectionSheet/PhysicalDescriptionSet/PhysicalDescription/Dimensions').text:
					if template.find('archdesc/did/physdesc') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_physdesc", "collection-level Physical Description", "<physdesc>")
			else:
				if input.find('CollectionSheet/PhysicalDescriptionSet/PhysicalDescription/Quantity').text or input.find('CollectionSheet/PhysicalDescriptionSet/PhysicalDescription/Dimensions').text:
					if template.find('archdesc/did/physdescstructured') is None:
						if template.find('archdesc/did/physdesc') is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_physdesc", "collection-level Physical Description", "<physdesc> or <physdescstructured>")
						
			if input.find('CollectionSheet/Languages/Language/Lang') is None:
				pass
			else:
				if input.find('CollectionSheet/Languages/Language/Lang').text:
					if template.find("archdesc/did/langmaterial") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_langmat", "a Collection Language  or a Language Description", "<languagematerial>")
				
			if input.find('CollectionSheet/Access/Statement') is None:
				if input.find('CollectionSheet/Access/SpecificMaterialRestrictions/SpecificRestriction/Restriction') is None:
					pass
				else:
					if input.find('CollectionSheet/Access/SpecificMaterialRestrictions/SpecificRestriction/Restriction').text:
						if template.find("archdesc/accessrestrict") is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_accessrestrict", "Access Restrictions", "<accessrestrict>")
			else:
				if input.find('CollectionSheet/Access/Statement').text or input.find('CollectionSheet/Access/SpecificMaterialRestrictions/SpecificRestriction/Restriction').text:
					if template.find("archdesc/accessrestrict") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_accessrestrict", "Access Restrictions", "<accessrestrict>")
			
			if input.find('CollectionSheet/Accruals/Accrual/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/Accruals/Accrual/Text').text:
					if template.find("archdesc/accruals") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_accruals", "Accruals", "<accruals>")
			
			if input.find('CollectionSheet/AcquisitionInfo/Acquis/Event') is None:
				pass
			else:
				if input.find('CollectionSheet/AcquisitionInfo/Acquis/Event').text:
					if template.find("archdesc/acqinfo") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_acq", "Acquisition information", "<acqinfo>")
			
			if input.find('CollectionSheet/AlternateForms/Alternative/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/AlternateForms/Alternative/Text').text:
					if template.find("archdesc/altformavail") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_altforms", "Alternate Forms or Copies", "<altformavail>")
							
			if input.find('CollectionSheet/AppraisalInfo/Appraisal/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/AppraisalInfo/Appraisal/Text').text:
					if template.find("archdesc/appraisal") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_appraisal", "Appraisal information", "<appraisal>")
			
			if input.find('CollectionSheet/CollectionArrangement/Arrangement/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/CollectionArrangement/Arrangement/Text').text:
					if template.find("archdesc/arrangement") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_arrange", "Arrangement information", "<arrangement>")
							
			if input.find('CollectionSheet/PublicationBibliography/Publication/Title').text or input.find('CollectionSheet/ManuscriptBibliography/Manuscript/UnitTitle').text:
				if template.find('archdesc/bibliography') is None:
					question_count = question_count + 1
					self.radio_ask(verticalbox, "add_biblio", "a Bibliography", "<bibliography>")
							
			if input.find('CollectionSheet/HistoricalNote/p') is None:
				pass
			else:
				if input.find('CollectionSheet/HistoricalNote/p').text:
					if template.find('archdesc/bioghist') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_bio", "a Historical Note", "<bioghist>")
							
			if input.find('CollectionSheet/ControlledAccess/AccessPoint/Part') is None or input.find('CollectionSheet/ControlledAccess/AccessPoint/ElementName') is None:
				pass
			else:
				if input.find('CollectionSheet/ControlledAccess/AccessPoint/Part').text and input.find('CollectionSheet/ControlledAccess/AccessPoint/ElementName').text:
					if template.find('archdesc/controlaccess') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_controlaccess", "Controlled Access points", "<controlaccess>")
							
			if input.find('CollectionSheet/CustodialHistory/Event/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/CustodialHistory/Event/Text').text:
					if template.find('archdesc/custodhist') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_custhistory", "Custodial History", "<custodhist>")
							
			if input.find('CollectionSheet/LegalStatus/Status/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/LegalStatus/Status/Text').text:
					if template.find('archdesc/legalstatus') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_legalstatus", "Legal Status information", "<legalstatus>")
							
			if input.find('CollectionSheet/OtherFindingAids/Other/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/OtherFindingAids/Other/Text').text:
					if template.find('archdesc/otherfindaid') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_otherfa", "Other Finding Aids", "<otherfindaid>")
							
			if input.find('CollectionSheet/PhysicalTechnical/Details/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/PhysicalTechnical/Details/Text').text:
					if template.find('archdesc/phystech') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_phystech", "Physical or Technical details", "<phystech>")

			if input.find('CollectionSheet/PreferredCitation/Example') is None:
				pass
			else:
				if input.find('CollectionSheet/PreferredCitation/Example').text:
					if template.find('archdesc/prefercite') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_prefcite", "a Preferred Citation", "<prefercite>")
							
			if input.find('CollectionSheet/ProcessingInformation/Details/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/ProcessingInformation/Details/Text').text:
					if template.find('archdesc/processinfo') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_processinfo", "Processing information", "<processinfo>")
			if input.find('CollectionSheet/RelatedPublications/Publication/Title') is None or input.find('CollectionSheet/RelatedManuscripts/Manuscript/UnitTitle') is None:
				pass
			else:
				if input.find('CollectionSheet/RelatedPublications/Publication/Title').text or input.find('CollectionSheet/RelatedManuscripts/Manuscript/UnitTitle').text:
					if template.find('archdesc/relatedmaterial') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_related", "Related Material", "<relatedmaterial>")
							
			if input.find('CollectionSheet/ScopeContent/p') is None:
				pass
			else:
				if input.find('CollectionSheet/ScopeContent/p').text:
					if template.find('archdesc/scopecontent') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_scope", "a Scope and Content note", "<scopecontent>")
							
			if input.find('CollectionSheet/SeparatedMaterial/Material/Text') is None:
				pass
			else:
				if input.find('CollectionSheet/SeparatedMaterial/Material/Text').text:
					if template.find('archdesc/separatedmaterial') is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_sepmat", "Separated Material", "<separatedmaterial>")
			
			if input.find('CollectionSheet/UseRestrictions/Statement') is None:
				if input.find('CollectionSheet/UseRestrictions/SpecificMaterialRestrictions/SpecificRestriction/Restriction') is None:
					pass
				else:
					if input.find('CollectionSheet/UseRestrictions/SpecificMaterialRestrictions/SpecificRestriction/Restriction').text:
						if template.find("archdesc/userestrict") is None:
							question_count = question_count + 1
							self.radio_ask(verticalbox, "add_userestrict", "Use Restrictions", "<userestrict>")
			else:
				if input.find('CollectionSheet/UseRestrictions/Statement').text or input.find('CollectionSheet/UseRestrictions/SpecificMaterialRestrictions/SpecificRestriction/Restriction').text:
					if template.find("archdesc/userestrict") is None:
						question_count = question_count + 1
						self.radio_ask(verticalbox, "add_userestrict", "Use Restrictions", "<userestrict>")
			"""
			# UAlbany Format question
			question_count = question_count + 1
			ask_ualbany = wx.StaticText(self, id=-1, label="Do you want to insert UAlbany's stylesheet and follow UAlbany's local formatting for the <titleproper>?")
			ask_ualbany.Wrap(530)
			ask_ualbanyY = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
			ask_ualbanyN = wx.RadioButton(self, label = "No")
			qbox98 = wx.BoxSizer(wx.HORIZONTAL)
			abox98 = wx.BoxSizer(wx.HORIZONTAL)
			qbox98.Add(ask_ualbany, 1, wx.TOP, 5)
			abox98.Add(ask_ualbanyY, 1, wx.ALL, 3)
			abox98.Add(ask_ualbanyN, 1, wx.ALL, 3)
			verticalbox.Add(qbox98, 0, wx.TOP|wx.EXPAND, 5)
			verticalbox.Add(abox98, 0, wx.ALL, 3)
			SpreadsheettoEAD.func.globals.new_elements.append('ask_ualbany')
			self.Bind(wx.EVT_RADIOBUTTON, lambda event: self.radioYes("ask_ualbany"), ask_ualbanyY)
			self.Bind(wx.EVT_RADIOBUTTON, lambda event: self.radioNo("ask_ualbany"), ask_ualbanyN)
			
			# <unitid> at file level question
			question_count = question_count + 1
			ask_fileunitid = wx.StaticText(self, id=-1, label="Do you want to keep the <unitid> tags at the file level?")
			ask_fileunitid.Wrap(530)
			ask_fileunitidY = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
			ask_fileunitidN = wx.RadioButton(self, label = "No")
			qbox97 = wx.BoxSizer(wx.HORIZONTAL)
			abox97 = wx.BoxSizer(wx.HORIZONTAL)
			qbox97.Add(ask_fileunitid, 1, wx.TOP, 5)
			abox97.Add(ask_fileunitidY, 1, wx.ALL, 3)
			abox97.Add(ask_fileunitidN, 1, wx.ALL, 3)
			verticalbox.Add(qbox97, 0, wx.TOP|wx.EXPAND, 5)
			verticalbox.Add(abox97, 0, wx.ALL, 3)
			SpreadsheettoEAD.func.globals.new_elements.append('ask_fileunitid')
			self.Bind(wx.EVT_RADIOBUTTON, lambda event: self.radioYes("ask_fileunitid"), ask_fileunitidY)
			self.Bind(wx.EVT_RADIOBUTTON, lambda event: self.radioNo("ask_fileunitid"), ask_fileunitidN)
			
			# HTML output question
			question_count = question_count + 1
			ask_html = wx.StaticText(self, id=-1, label="Do you want to create a basic HTML <html> file for this collection?")
			ask_html.Wrap(530)
			ask_htmlY = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
			ask_htmlN = wx.RadioButton(self, label = "No")
			qbox99 = wx.BoxSizer(wx.HORIZONTAL)
			abox99 = wx.BoxSizer(wx.HORIZONTAL)
			qbox99.Add(ask_html, 1, wx.TOP, 5)
			abox99.Add(ask_htmlY, 1, wx.ALL, 3)
			abox99.Add(ask_htmlN, 1, wx.ALL, 3)
			verticalbox.Add(qbox99, 0, wx.TOP|wx.EXPAND, 5)
			verticalbox.Add(abox99, 0, wx.ALL, 3)
			SpreadsheettoEAD.func.globals.new_elements.append('ask_html')
			self.Bind(wx.EVT_RADIOBUTTON, lambda event: self.radioYes("ask_html"), ask_htmlY)
			self.Bind(wx.EVT_RADIOBUTTON, lambda event: self.radioNo("ask_html"), ask_htmlN)

			
			name = input.find('CollectionSheet/CollectionName').text
			if "ask_ualbany" in SpreadsheettoEAD.func.globals.new_elements:
				if input.find('CollectionSheet/CollectionID').text:
					cID = input.find('CollectionSheet/CollectionID').text.replace("-", "").lower()
				else:
					cID = ""
			else:
				cID = input.find('CollectionSheet/CollectionID').text
			goButton = wx.Button(self, label='Create EAD')
			if cID is None:
				self.Bind(wx.EVT_BUTTON, lambda event: parent.goClick(event, input_xml, template_xml, name), goButton)
			else:
				self.Bind(wx.EVT_BUTTON, lambda event: parent.goClick(event, input_xml, template_xml, cID), goButton)
			buttonbox = wx.BoxSizer(wx.HORIZONTAL)
			buttonbox.Add((400, 10))
			buttonbox.Add(goButton, 1, wx.ALL|wx.EXPAND, 5)
			verticalbox.Add(buttonbox, 1, wx.ALL|wx.EXPAND, 5)        			
		 
		  
			
			self.SetSizer(overallbox)
			overallbox.Fit(self)
			self.SetAutoLayout(1)
			self.SetupScrolling()
		
    def radioYes(self, keyword):
        SpreadsheettoEAD.func.globals.new_elements.append(keyword)
        #print SpreadsheettoEAD.func.globals.new_elements
        
    def radioNo(self, keyword):
        SpreadsheettoEAD.func.globals.new_elements.remove(keyword)
        #print SpreadsheettoEAD.func.globals.new_elements
		
    def radio_ask(self, verticalbox, add_var, name, element):
        if name.lower() == "custom":
			add_question = wx.StaticText(self, id=-1, label=element)
        else:
			add_question = wx.StaticText(self, id=-1, label="You entered " + name + " but there is no " + element + " tag in your EAD template, would you like EADMachine to add one for this collection?")
        add_question.Wrap(530)
        add_questionY = wx.RadioButton(self, label="Yes", style=wx.RB_GROUP)
        add_questionN = wx.RadioButton(self, label = "No")
        qbox = wx.BoxSizer(wx.HORIZONTAL)
        abox = wx.BoxSizer(wx.HORIZONTAL)
        qbox.Add(add_question, 1, wx.TOP, 5)
        abox.Add(add_questionY, 1, wx.ALL, 3)
        abox.Add(add_questionN, 1, wx.ALL, 3)
        verticalbox.Add(qbox, 0, wx.TOP|wx.EXPAND, 5)
        verticalbox.Add(abox, 0, wx.ALL, 3)
        SpreadsheettoEAD.func.globals.new_elements.append(add_var)
        self.Bind(wx.EVT_RADIOBUTTON, lambda event: self.radioYes(add_var), add_questionY)
        self.Bind(wx.EVT_RADIOBUTTON, lambda event: self.radioNo(add_var), add_questionN)
