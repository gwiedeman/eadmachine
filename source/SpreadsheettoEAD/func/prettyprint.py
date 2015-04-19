import xml.etree.cElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import parseString
from encoding import strip_non_ascii
import globals

def prettyprint(element):
	if "ask_gui" in globals.new_elements: 
		import wx
		from wx.lib.pubsub import pub
		wx.CallAfter(pub.sendMessage, "update", msg="Pretty Printing XML...")
	stripped_element = strip_non_ascii(element)
	fix_quote = stripped_element.replace('&quot;', "\"")
	lessthen = fix_quote.replace('&lt;', '<')
	greaterthen = lessthen.replace('&gt;', '>')
	#with open("parse_test.txt", 'w') as f:  
            #f.write(greaterthen)  
	reparsed = parseString(greaterthen)
	output = '\n'.join([line for line in reparsed.toprettyxml(indent=' '*2).split('\n') if line.strip()])
	quotefix = output.replace('&quot;', '"')
	if "ask_gui" in globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Removing non-ascii characters...")
	return quotefix
