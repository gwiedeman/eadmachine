# module for the <frontmatter> portion
import xml.etree.cElementTree as ET
import wx
import globals
import sys

def error(message, critical):
	if "ask_gui" in globals.new_elements:
		def ShowMessage():
				wx.MessageBox(message, 'Error', 
					wx.OK | wx.ICON_ERROR)
		ShowMessage()
		if critical == True:
			sys.exit()

	else:
		print "ERROR: " + message
		if critical == True:
			sys.exit()