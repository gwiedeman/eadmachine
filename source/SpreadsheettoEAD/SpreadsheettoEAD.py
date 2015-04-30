import xml.etree.cElementTree as ET
from func.prettyprint import prettyprint
import func.globals
import wx
from func.messages import error
from xml.dom import minidom

def SpreadsheettoEAD(input_xml, template_xml):

	ET.register_namespace('dc','http://purl.org/DC/elements/1.0/')
	

	input_file = ET.ElementTree(file=input_xml)
	template_file = ET.ElementTree(file=template_xml)

	input = input_file.getroot()
	old_template = template_file.getroot()
	
	#removes namespaces
	old_namespaces = old_template.tag
	old_template.tag = "ead"
	for all_tags in old_template.iter():
		all_tags.tag = str(all_tags.tag).split("}",1)[-1]

	#adds ead as default namespace
	if old_template[0].tag == 'eadheader': #namespace for EAD 2002
		#comment below is for namespaces in EAD2002, which are not valid with the EAD DTD so it is omitted
		#ET.register_namespace('', 'http://www.loc.gov/ead')
		template = ET.Element('ead')
	elif old_template[0].tag == 'control': #namespace for EAD3
		ET.register_namespace('', 'http://ead3.archivists.org/schema')
		template = ET.Element('{http://ead3.archivists.org/schema}ead')
	else:
		error("Template file does not contain <control> or <eadheader> in the correct location. Please enter a valid EAD Finding Aid.", True)
	
	for ead_child in old_template:
		template.append(ead_child)
		template.attrib = old_template.attrib
		
	# Checks for @id in <ead/> wrapper and if so places Collection ID there
	id = input.find('CollectionSheet/CollectionID')
	if 'id' in old_template.attrib:
		if "ask_ualbany" in func.globals.new_elements:
			if id.text is None:
				pass
			else:
				ualbany_id = id.text.replace("-", "").lower()
				template.attrib['id'] = ualbany_id
		else:
			template.attrib['id'] = id.text

	# Imports module for the <control/> or <eadheader/> section
	from func.eadheader import eadheader
	from func.control import control
	control_root = template[0] #the first child of <ead/> which should be <control/> or <eadheader/>
	if control_root.tag == "eadheader":
		eadheader(control_root, input[0])
		version = "ead2002"
	elif control_root.tag == "control":
		control(control_root, input[0])
		version = "ead3"
	else:
		error("CONTROL/EADHEADER MODULE FAILED: template file does not contain <control> or <eadheader> in the correct location", True)

	# Frontmatter section
	from func.frontmatter import frontmatter
	if template[1].tag == "frontmatter":
		fm_root = template[1]
		frontmatter(fm_root, input[0])

	# Collection-level description section <archdesc>
	from func.archdesc import archdesc
	arch_root = template.find('archdesc')
	archdesc(arch_root, input[0], version, input)

	# HTML output
	from wx.lib.pubsub import pub
	if "ask_gui" in func.globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <html>...")
	html_output = False
	if "ask_html" in func.globals.new_elements:
		from func.html import html
		htmlmodel_file = ET.ElementTree(file="../templates/html_default.html")
		htmlmodel = htmlmodel_file.getroot()
		html_element = html(input, htmlmodel)
		for italic in html_element.findall(".//emph[@render='italic']"):
			italic.tag = "i"
			del italic.attrib['render']
		for bold in html_element.findall(".//emph[@render='bold']"):
			bold.tag = "b"
			del bold.attrib['render']
		rough_html = ET.tostring(html_element)
		#adds doctype
		dom_html = minidom.parseString(rough_html)
		#html_pi = dom_html.createProcessingInstruction('DOCTYPE', 'html')
		#html_root = dom_html.firstChild
		#dom_html.insertBefore(html_pi, html_root)
		pretty_html = dom_html.toxml()
		html_output = prettyprint(pretty_html)
		#html_output_element = ET.fromstring(pretty_html)
		#html_output = ET.ElementTree(html_output_element)
		#html_output.write(input.find('CollectionSheet/CollectionID').text + '.html', method='xml')
		
	#Removes unitids at the file level
	if "ask_fileunitid" in func.globals.new_elements:
		pass
	else:
		for did in template.find('archdesc/dsc').iter():
			if did.tag == 'did':
				if did.find('unitid') is None:
					pass
				else:
					did.remove(did.find('unitid'))
	
	# Sets Processing Instructions and pretty prints the XML
	#output_test = ET.ElementTree(template)
	#output_test.write("output_test.xml")
	rough_string = ET.tostring(template)
	
	dom = minidom.parseString(rough_string)
	if "ask_ualbany" in func.globals.new_elements:
		pi = dom.createProcessingInstruction('xml-stylesheet', 'type="text/xsl" href="eadcbs6-su1_gw_4-30-15.xsl"')
		root = dom.firstChild
		dom.insertBefore(pi, root)
	
	dt = minidom.getDOMImplementation('').createDocumentType('ead', '', 'ead.dtd')
	dom.insertBefore(dt, dom.documentElement)
		
	pretty_string = dom.toxml()
	output = prettyprint(pretty_string)
	
	#output_element = ET.fromstring(with_pi)
	#output = ET.ElementTree(output_element)
	if "ask_gui" in func.globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Finalizing EAD...")
	
	return (output, html_output)
	"""
	output.write(input.find('CollectionSheet/CollectionID').text + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

	# prints a confirmation statement
	name = template.find('archdesc/did/unittitle')
	if name.text.startswith("The") or name.text.startswith("the"):
		print name.text + " has been written to an EAD finding aid"
	else:	
		print "The " + name.text + " has been written to an EAD finding aid"
	"""
