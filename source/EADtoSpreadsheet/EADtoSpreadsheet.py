# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from func.resource_path import resource_path
from func.globals import init
from func.prettyprint import prettyprint
from func.messages import error
import wx

def EADtoSpreadsheet(EAD_xml):
	#ET.register_namespace('', 'http://ead3.archivists.org/schema')
	#ET.register_namespace('dc','http://purl.org/DC/elements/1.0/')
	
	#global variables
	init()

	EAD_file = ET.ElementTree(file=EAD_xml)
	old_EAD = EAD_file.getroot()
	
	from wx.lib.pubsub import pub
	wx.CallAfter(pub.sendMessage, "update_spread", msg="Clearing excess line breaks, leading and trailing spaces...")
	
	#removes line breaks, carrage returns, and excess spaces
	rough_input = ET.tostring(old_EAD)
	clean_string = rough_input.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ').replace('   ', ' ').replace('    ', ' ').replace('     ', ' ').replace('      ', ' ').replace('       ', ' ').replace('        ', ' ').replace('         ', ' ').replace('          ', ' ').replace('           ', ' ').replace('            ', ' ').replace('             ', ' ').replace('              ', ' ').replace('               ', ' ').replace('                ', ' ').replace('                 ', ' ').replace('                  ', ' ').replace('                   ', ' ').replace('                    ', ' ')
	clean_input = ET.ElementTree(ET.fromstring(clean_string))
	clean_EAD = clean_input.getroot()
	
	#removes namespaces and leading and trailing spaces
	old_namespaces = clean_EAD.tag
	clean_EAD.tag = "ead"
	for all_tags in clean_EAD.iter():
		all_tags.tag = str(all_tags.tag).split("}",1)[-1]
		if all_tags.text:
			all_tags.text = all_tags.text.strip()

	wx.CallAfter(pub.sendMessage, "update_spread", msg="Fixing Namespaces...")
	#adds ead as default namespace for EAD3
	if clean_EAD[0].tag == 'eadheader': #namespace for EAD 2002
		#comment below is for namespaces in EAD2002, which are not valid with the EAD DTD so it is omitted
		#ET.register_namespace('', 'http://www.loc.gov/ead')
		EAD = ET.Element('ead')
	elif clean_EAD[0].tag == 'control': #namespace for EAD3
		ET.register_namespace('', 'http://ead3.archivists.org/schema')
		EAD = ET.Element('{http://ead3.archivists.org/schema}ead')
	else:
		error("Template file does not contain <control> or <eadheader> in the correct location. Please enter a valid EAD Finding Aid.", True)
	
	for ead_child in clean_EAD:
		EAD.append(ead_child)
		EAD.attrib = clean_EAD.attrib
	
	FAFile = ET.ElementTree(file=resource_path("resources/FASheet.xml"))
	FASheet = FAFile.getroot()

	CSheet = FASheet.find('CollectionSheet')
	
	# Imports module for the <control/> or <eadheader/> section
	from func.eadheader import eadheader
	from func.control import control
	control_root = EAD[0] #the first child of <ead/> which should be <control/> or <eadheader/>
	if control_root.tag == "eadheader":
		eadheader(EAD, CSheet)
		version = "ead2002"
	elif control_root.tag == "control":
		control(EAD, CSheet)
		version = "ead3"
	else:
		error("Finding Aid does not contain <control> or <eadheader> in the correct location.", True)
	
	if version == "ead3":
		if EAD.find('control/filedesc/titlestmt/titleproper').text.strip() == EAD.find('archdesc/did/unittitle').text.strip():
			CSheet.find('CollectionName').text = EAD.find('archdesc/did/unittitle').text.strip()
		else:
			#error("If your EAD file, <titleproper> is not the same as the collection-level <unittitle>. For this and simmilar differences, the description within the <archdesc> will be used.", False)
			CSheet.find('CollectionName').text = EAD.find('archdesc/did/unittitle').text.strip()
	else:
		if EAD.find('eadheader/filedesc/titlestmt/titleproper').text.strip() == EAD.find('archdesc/did/unittitle').text.strip():
			CSheet.find('CollectionName').text = EAD.find('archdesc/did/unittitle').text.strip()
		else:
			#error("If your EAD file, <titleproper> is not the same as the collection-level <unittitle>. For this and simmilar differences, the description within the <archdesc> will be used.", False)
			CSheet.find('CollectionName').text = EAD.find('archdesc/did/unittitle').text.strip()
		
	# Collection ID 
	if version == "ead3":
		if EAD.find('control/recordid').text:
			CSheet.find('CollectionID').text = EAD.find('control/recordid').text
		elif 'identifier' in EAD.find('control/recordid').attrib:
			CSheet.find('CollectionID').text = EAD.find('control/recordid').attrib['identifier']
		elif 'id' in EAD.attrib:
			CSheet.find('CollectionID').text = EAD.attrib['id']
		else:
			CSheet.find('CollectionID').text = ""
	else:
		if EAD.find('eadheader/eadid').text:
			CSheet.find('CollectionID').text = EAD.find('eadheader/eadid').text
		elif 'identifier' in EAD.find('eadheader/eadid').attrib:
			CSheet.find('CollectionID').text = EAD.find('eadheader/eadid').attrib['identifier']
		elif 'id' in EAD.attrib:
			CSheet.find('CollectionID').text = EAD.attrib['id']
		else:
			CSheet.find('CollectionID').text = ""

	
	# Collection-level description section <archdesc>
	from func.archdesc import archdesc
	archdesc(EAD, FASheet, version)

	wx.CallAfter(pub.sendMessage, "update_spread", msg="Finalizing file...")
	
	rough_string = ET.tostring(FASheet)
	clean_string = rough_string.replace('&amp;#', "&#")
	#output = prettyprint(rough_string)
	
	return (clean_string)
	
	#output.write(input.find('CollectionSheet/CollectionID').text + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

	# prints a confirmation statement
	name = EAD.find('archdesc/did/unittitle')
	if name.text.startswith("The") or name.text.startswith("the"):
		print name.text + " has been converted to a file to be imported into the EADMachine spreadsheet."
	else:	
		print "The " + name.text + " has been converted to a file to be imported into the EADMachine spreadsheet."
