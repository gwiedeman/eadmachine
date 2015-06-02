import xml.etree.cElementTree as ET
from lxml import etree as lxml
from func.prettyprint import prettyprint
import func.globals
import wx
from func.messages import error
import os.path

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
		if os.path.isfile("templates/html_default.html"):
			htmlmodel_file = ET.ElementTree(file="templates/html_default.html")
			htmlmodel = htmlmodel_file.getroot()
			html_element = html(input, htmlmodel)
			for italic in html_element.findall(".//emph[@render='italic']"):
				italic.tag = "i"
				del italic.attrib['render']
			for bold in html_element.findall(".//emph[@render='bold']"):
				bold.tag = "b"
				del bold.attrib['render']
			rough_html = ET.tostring(html_element)
			parser = lxml.XMLParser(remove_blank_text=True)
			to_lxml_html = lxml.fromstring(rough_html, parser)
			#adds doctype
			pretty_html = lxml.tostring(to_lxml_html, pretty_print=True, doctype="<!DOCTYPE html>")
						
			html_output = prettyprint(pretty_html)

		else:
			error("HTML MODULE FAILED: Cannot find html_default.html in the templates folder, EADMachine will not be able to create an html file for this collection", False)
		
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
	
	test_string = ET.tostring(template)
	if "<c02" in test_string:
		no_series = False
	else:
		if template.find('archdesc/dsc/c') is None:
			no_series = True
		else:
			series_count = 0
			for series in template.find('archdesc/dsc'):
				if series.find('c') is None and series.find('c02') is None:
					pass
				else:
					series_count = series_count + 1
			if series_count > 0:
				no_series = False
			else:
				no_series = True
		
	
	# Sets Processing Instructions and pretty prints the XML
	rough_string = ET.tostring(template)
	parser = lxml.XMLParser(remove_blank_text=True)
	to_lxml = lxml.fromstring(rough_string, parser)
	
	pretty_string = lxml.tostring(to_lxml, pretty_print=True, xml_declaration=True, encoding="utf-8", doctype="<!DOCTYPE ead SYSTEM 'ead.dtd'>")
	

	if "ask_ualbany" in func.globals.new_elements:
		if no_series == True:
			FA_output = pretty_string[:38] + "\n<?xml-stylesheet type='text/xsl' href='eadcbs6-su1_gw_no_series.xsl'?> " + pretty_string[38:]
		else:
			FA_output = pretty_string[:38] + "\n<?xml-stylesheet type='text/xsl' href='eadcbs6-su1_gw_4-30-15.xsl'?> " + pretty_string[38:]
		output = prettyprint(FA_output)
	else:
		output = prettyprint(pretty_string)
	
	#file = open("test.xml", "w")
	#file.write(FA_output)
	
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