# module for the Container List <dsc>
import xml.etree.cElementTree as ET
from components import components
import globals
import wx
from messages import error
from mixed_content import mixed_content

def dsc(dsc_root, FASheet, version):
	from wx.lib.pubsub import pub
	wx.CallAfter(pub.sendMessage, "update_spread", msg="Reading <dsc>...")

	if dsc_root.find('c/c') is None:
		if dsc_root.find('c01/c02') is None:
			number = "noseries"
		else:
			number = "c01"
	else:
		number = "c"
	"""
	for top_series in dsc_root:
		if top_series.find('did/unittitle') is None:
			wx.CallAfter(pub.sendMessage, "update_spread", msg="Reading series...")
		else:
			wx.CallAfter(pub.sendMessage, "update_spread", msg="Reading " + top_series.find('did/unittitle').text + "...")
	"""
	if number == "c":
		child_tag = "c"
		cmpnt_count = 0
		if dsc_root.iterfind('c/c') is None:
			#Collection does not have series
			FASheet.find('CollectionSheet/CollectionMap/Component/ComponentName').text = "noseries"
			cmpnt_count = cmpnt_count + 1
			level = "1"
			components(dsc_root, FASheet.find('CollectionSheet'), FASheet.find('Series' + str(cmpnt_count)), level, child_tag, version)
		else:
			#Collection has series
			FASheet.find('CollectionSheet/CollectionMap').clear()
			for component in dsc_root.iter('c'):
				if component.find('c') is None:
					pass
				else:
					cmpnt_count = cmpnt_count + 1
					Component_element = ET.Element('Component')
					FASheet.find('CollectionSheet/CollectionMap').append(Component_element)
					ComponentLevel_element = ET.Element('ComponentLevel')
					Component_element.append(ComponentLevel_element)
					ComponentNumber_element = ET.Element('ComponentNumber')
					Component_element.append(ComponentNumber_element)
					ComponentName_element = ET.Element('ComponentName')
					Component_element.append(ComponentName_element)
					if component in dsc_root.iterfind('c'):
						level = "1"
					elif component in dsc_root.iterfind('c/c'):
						level = "2"
					elif component in dsc_root.iterfind('c/c/c'):
						level = "3"
					elif component in dsc_root.iterfind('c/c/c'):
						level = "4"
					elif component in dsc_root.iterfind('c/c/c/c'):
						level = "5"
					elif component in dsc_root.iterfind('c/c/c/c/c'):
						level = "6"
					elif component in dsc_root.iterfind('c/c/c/c/c/c'):
						level = "7"
					elif component in dsc_root.iterfind('c/c/c/c/c/c/c'):
						level = "8"
					elif component in dsc_root.iterfind('c/c/c/c/c/c/c/c'):
						level = "9"
					elif component in dsc_root.iterfind('c/c/c/c/c/c/c/c/c'):
						level = "10"
					elif component in dsc_root.iterfind('c/c/c/c/c/c/c/c/c/c'):
						level = "11"
					elif component in dsc_root.iterfind('c/c/c/c/c/c/c/c/c/c/c'):
						level = "12"
					ComponentLevel_element.text = level
					if component.find('did') is None:
						pass
					else:
						if component.find('did/unitid') is None:
							if "id" in component.attrib:
								ComponentNumber_element.text = component.attrib['id']
							elif "id" in component.find('did').attrib:
								ComponentNumber_element.text = component.find('did').attrib['id']
						else:
							ComponentNumber_element.text = mixed_content(component.find('did/unitid'))
						if component.find('did/unittitle') is None:
							pass
						else:
							ComponentName_element.text = mixed_content(component.find('did/unittitle'))
					if cmpnt_count > 51:
						pass
					elif cmpnt_count == 51:
						error("EADMachine can only read up to 50 series and subseries. Since your collection has more than 50 series and subseries, only the first 50 will be read.", False)
					else:
						components(component, FASheet.find('CollectionSheet'), FASheet.find('Series' + str(cmpnt_count)), level, child_tag, version)
	elif number == "c01":
		cmpnt_count = 0
		if dsc_root.iter('c02') is None:
			#Collection does not have series
			FASheet.find('CollectionSheet/CollectionMap/Component/ComponentName').text = "noseries"
			cmpnt_count = cmpnt_count + 1
			level = "1"
			components(dsc_root, FASheet.find('CollectionSheet'), FASheet.find('Series' + str(cmpnt_count)), level, child_tag, version)
		else:
			#Collection has series
			FASheet.find('CollectionSheet/CollectionMap').clear()
			for component in dsc_root.iter():
				if component.tag == 'c01' or component.tag == 'c02' or component.tag == 'c03' or component.tag == 'c04' or component.tag == 'c05' or component.tag == 'c06' or component.tag == 'c07' or component.tag == 'c08' or component.tag == 'c09' or component.tag == 'c10' or component.tag == 'c11' or component.tag == 'c12':
					child_tag_name = component.tag[1:]
					if int(child_tag_name) < 10:
						child_tag = "c0" + str(int(child_tag_name) + 1)
					else:
						child_tag = "c" + str(int(child_tag_name) + 1)
					if component.find(child_tag) is None:
						pass
					else:
						cmpnt_count = cmpnt_count + 1
						Component_element = ET.Element('Component')
						FASheet.find('CollectionSheet/CollectionMap').append(Component_element)
						ComponentLevel_element = ET.Element('ComponentLevel')
						Component_element.append(ComponentLevel_element)
						ComponentNumber_element = ET.Element('ComponentNumber')
						Component_element.append(ComponentNumber_element)
						ComponentName_element = ET.Element('ComponentName')
						Component_element.append(ComponentName_element)
						level = "0"
						if component.tag == 'c01':
							level = "1"
						elif component.tag == 'c02':
							level = "2"
						elif component.tag == 'c03':
							level = "3"
						elif component.tag == 'c04':
							level = "4"
						elif component.tag == 'c05':
							level = "5"
						elif component.tag == 'c06':
							level = "6"
						elif component.tag == 'c07':
							level = "7"
						elif component.tag == 'c08':
							level = "8"
						elif component.tag == 'c09':
							level = "9"
						elif component.tag == 'c10':
							level = "10"
						elif component.tag == 'c11':
							level = "11"
						elif component.tag == 'c12':
							level = "12"
						ComponentLevel_element.text = level
						if component.find('did') is None:
							pass
						else:
							if component.find('did/unitid') is None:
								if "id" in component.attrib:
									ComponentNumber_element.text = component.attrib['id']
								elif "id" in component.find('did').attrib:
									ComponentNumber_element.text = component.find('did').attrib['id']
							else:
								ComponentNumber_element.text = mixed_content(component.find('did/unitid'))
							if component.find('did/unittitle') is None:
								pass
							else:
								ComponentName_element.text = mixed_content(component.find('did/unittitle'))
						if cmpnt_count > 51:
							pass
						elif cmpnt_count == 51:
							error("EADMachine can only read up to 50 series and subseries. Since your collection has more than 50 series and subseries, only the first 50 will be read.", False)
						else:
							components(component, FASheet.find('CollectionSheet'), FASheet.find('Series' + str(cmpnt_count)), level, child_tag, version)
	elif number == "noseries":
		cmpnt_count = 0
		#Collection does not have series
		FASheet.find('CollectionSheet/CollectionMap/Component/ComponentName').text = "noseries"
		cmpnt_count = 1
		level = "1"
		components(dsc_root, FASheet.find('CollectionSheet'), FASheet.find('Series' + str(cmpnt_count)), level, "c", version)