# module for components <c> or <c01>, <c02>, etc.
import xml.etree.cElementTree as ET
from archdesc_lower import archdesc_lower
import globals
from mixed_content import mixed_content
import wx
from wx.lib.pubsub import pub

def components(cmpnt_root, CSheet, SeriesSheet, level, child_tag, version):
	
	#<unittitle>
	if cmpnt_root.find('did/unittitle') is None:
		pass
	else:
		SeriesSheet.find('SeriesName').text = mixed_content(cmpnt_root.find('did/unittitle'))
	
	#<unitid>
	if cmpnt_root.find('did/unitid') is None:
		if "id" in cmpnt_root.attrib:
			SeriesSheet.find('SeriesNumber').text = cmpnt_root.attrib['id']
		else:
			if cmpnt_root.find('did') is None:
				pass
			else:
				if "id" in cmpnt_root.find('did').attrib:
					SeriesSheet.find('SeriesNumber').text = cmpnt_root.find('did').attrib['id']
	else:
		SeriesSheet.find('SeriesNumber').text = mixed_content(cmpnt_root.find('did/unitid'))
	SeriesSheet.find('SeriesLevel').text = level
	
	#<unitdate> and <unitdatestructured>
	from unitdate import unitdate
	if cmpnt_root.find('did') is None:
		pass
	else:
		unitdate(cmpnt_root.find('did'), SeriesSheet, "series", version)
	
	#<physdesc> and <physdescstructured>
	if cmpnt_root.find('physdesc') is None:
		pass
	else:
		from physdesc import simple
		simple(cmpnt_root, SeriesSheet, version)
	if cmpnt_root.find('physdescstructured') is None:
		pass
	else:
		from physdesc import structured
		structured(cmpnt_root, SeriesSheet)
	
	#<arrangement>
	if cmpnt_root.find('arrangement') is None:
		pass
	else:
		SeriesSheet.find('Arrangement').clear()
		for arr_para in cmpnt_root.find('arrangement'):
			if arr_para.tag == "p":
				p_element = ET.Element('p')
				SeriesSheet.find('Arrangement').append(p_element)
				p_element.text = mixed_content(arr_para)				
	
	#<scopecontent>
	if cmpnt_root.find('scopecontent') is None:
		pass
	else:
		SeriesSheet.find('Description').clear()
		for arr_para in cmpnt_root.find('scopecontent'):
			if arr_para.tag == "p":
				p_element = ET.Element('p')
				SeriesSheet.find('Description').append(p_element)
				p_element.text = mixed_content(arr_para)		
	
	#<archdesc> elements at series level
	archdesc_lower(cmpnt_root, CSheet, version)
		
	if child_tag == "c":
		pass
	else:
		if "level" in cmpnt_root.find(child_tag).attrib:
			SeriesSheet.find('DescriptionLevel').text =  cmpnt_root.find(child_tag).attrib['level']
		
	for old_record in SeriesSheet.findall('Record'):
		SeriesSheet.remove(old_record)
	
	next_level_name = child_tag[1:]
	if len(next_level_name) > 1:
		if int(next_level_name) < 10:
			next_level = "c0" + str(int(next_level_name) + 1)
		else:
			next_level = "c" + str(int(next_level_name) + 1)
	else:
		next_level = "c"
	
	for file_root in cmpnt_root:
		if file_root.tag == child_tag or file_root.tag == "c" or file_root.tag == "c01":
			if file_root.find(next_level) is None:
				Record_element = ET.Element('Record')
				SeriesSheet.append(Record_element)
				RecordID_element = ET.Element('RecordID')
				Record_element.append(RecordID_element)
				BoxName_element = ET.Element('BoxName')
				Record_element.append(BoxName_element)
				BoxNumber_element = ET.Element('BoxNumber')
				Record_element.append(BoxNumber_element)
				Unit_element = ET.Element('Unit')
				Record_element.append(Unit_element)
				UnitNumber_element = ET.Element('UnitNumber')
				Record_element.append(UnitNumber_element)
				UnitTitle_element = ET.Element('UnitTitle')
				Record_element.append(UnitTitle_element)
				Date1_element = ET.Element('Date1')
				Record_element.append(Date1_element)
				Date1Normal_element = ET.Element('Date1Normal')
				Record_element.append(Date1Normal_element)
				Date2_element = ET.Element('Date2')
				Record_element.append(Date2_element)
				Date2Normal_element = ET.Element('Date2Normal')
				Record_element.append(Date2Normal_element)
				Date3_element = ET.Element('Date3')
				Record_element.append(Date3_element)
				Date3Normal_element = ET.Element('Date3Normal')
				Record_element.append(Date3Normal_element)
				Date4_element = ET.Element('Date4')
				Record_element.append(Date4_element)
				Date4Normal_element = ET.Element('Date4Normal')
				Record_element.append(Date4Normal_element)
				Date5_element = ET.Element('Date5')
				Record_element.append(Date5_element)
				Date5Normal_element = ET.Element('Date5Normal')
				Record_element.append(Date5Normal_element)
				Coverage_element = ET.Element('Coverage')
				Record_element.append(Coverage_element)
				Type_element = ET.Element('Type')
				Record_element.append(Type_element)
				Approximate_element = ET.Element('Approximate')
				Record_element.append(Approximate_element)
				Quantity_element = ET.Element('Quantity')
				Record_element.append(Quantity_element)
				UnitType_element = ET.Element('UnitType')
				Record_element.append(UnitType_element)
				PhysicalFacet_element = ET.Element('PhysicalFacet')
				Record_element.append(PhysicalFacet_element)
				Dimensions_element = ET.Element('Dimensions')
				Record_element.append(Dimensions_element)
				DimensionsUnit_element = ET.Element('DimensionsUnit')
				Record_element.append(DimensionsUnit_element)
				PhysDescNote_element = ET.Element('PhysDescNote')
				Record_element.append(PhysDescNote_element)
				DigitalObjectType_element = ET.Element('DigitalObjectType')
				Record_element.append(DigitalObjectType_element)
				DigitalObjectID_element = ET.Element('DigitalObjectID')
				Record_element.append(DigitalObjectID_element)
				DigitalObjectLink_element = ET.Element('DigitalObjectLink')
				Record_element.append(DigitalObjectLink_element)
				DigitalObjectLocalName_element = ET.Element('DigitalObjectLocalName')
				Record_element.append(DigitalObjectLocalName_element)
				DigitalObjectNote_element = ET.Element('DigitalObjectNote')
				Record_element.append(DigitalObjectNote_element)
				
				
				if len(file_root.findall('did/container')) == 2:
					BoxNumber_element.text = file_root.find('did/container[1]').text
					if "type" in file_root.find('did/container[1]').attrib:
						BoxName_element.text = file_root.find('did/container[1]').attrib['type']
					UnitNumber_element.text = file_root.find('did/container[2]').text
					if "type" in file_root.find('did/container[2]').attrib:
						Unit_element.text = file_root.find('did/container[2]').attrib['type']
					if file_root.find('did/unitid') is None:
						if "id" in file_root.attrib:
							RecordID_element.text = file_root.attrib['id']
					else:
						RecordID_element.text = file_root.find('did/unitid').text
				elif len(file_root.findall('did/container')) == 1:
					if file_root.find('did/physloc') is None:
						if "type" in file_root.find('did/container').attrib:
							if file_root.find('did/container').attrib['type'].lower() == "oversized" or "artifact-box" or "flat-file":
								BoxNumber_element.text = file_root.find('did/container').text
								if "type" in file_root.find('did/container').attrib:
									BoxName_element.text = file_root.find('did/container').attrib['type']
								if file_root.find('did/unitid') is None:
									if "id" in file_root.attrib:
										RecordID_element.text = file_root.attrib['id']
								else:
									RecordID_element.text = file_root.find('did/unitid').text
							else:
								UnitNumber_element.text = file_root.find('did/container').text
								if "type" in file_root.find('did/container').attrib:
									Unit_element.text = file_root.find('did/container').attrib['type']
								if file_root.find('did/unitid') is None:
									if "id" in file_root.attrib:
										RecordID_element.text = file_root.attrib['id']
								else:
									RecordID_element.text = file_root.find('did/unitid').text
						else:
							UnitNumber_element.text = file_root.find('did/container').text
							if "type" in file_root.find('did/container').attrib:
								Unit_element.text = file_root.find('did/container').attrib['type']
							if file_root.find('did/unitid') is None:
								if "id" in file_root.attrib:
									RecordID_element.text = file_root.attrib['id']
							else:
								RecordID_element.text = file_root.find('did/unitid').text
					else:
						if file_root.find('did/unitid') is None:
							if "id" in file_root.attrib:
								#physloc, container, id
								RecordID_element.text = file_root.attrib['id']
								BoxNumber_element.text = file_root.find('did/container').text
								if "type" in file_root.find('did/container').attrib:
									BoxName_element.text = file_root.find('did/container').attrib['type']
								UnitNumber_element.text = file_root.find('did/physloc').text
							else:
								#physloc, container
								BoxNumber_element.text = file_root.find('did/container').text
								if "type" in file_root.find('did/container').attrib:
									BoxName_element.text = file_root.find('did/container').attrib['type']
								UnitNumber_element.text = file_root.find('did/physloc').text
						else:
							#physloc, container and unitid
							if "id" in file_root.attrib:
								RecordID_element.text = file_root.attrib['id']
								BoxNumber_element.text = file_root.find('did/container').text
								if "type" in file_root.find('did/container').attrib:
									BoxName_element.text = file_root.find('did/container').attrib['type']
								Unit_element.text = file_root.find('did/physloc').text
								UnitNumber_element.text = file_root.find('did/unitid').text
							else:
								RecordID_element.text = file_root.find('did/physloc').text
								BoxNumber_element.text = file_root.find('did/container').text
								if "type" in file_root.find('did/container').attrib:
									BoxName_element.text = file_root.find('did/container').attrib['type']
								UnitNumber_element.text = file_root.find('did/unitid').text
				elif len(file_root.findall('did/container')) == 0:
					if "id" in file_root.attrib:
						RecordID_element.text = file_root.attrib['id']
					if file_root.find('did/unitid') is None:
						pass
					else:
						UnitNumber_element.text = file_root.find('did/unitid').text
				
				#Container IDs
				if file_root.find('did/container') is None:
					pass
				else:
					for cont in file_root.find('did'):
						if cont.tag == 'container':
							if "id" in cont.attrib:
								if file_root.find('did/unitid') is None:
									if "id" in file_root.attrib:
										parent_id = file_root.attrib['id']
									else:
										parent_id = ""
								else:
									parent_id = file_root.find('did/unitid').text
								if "type" in file_root.find('did/container').attrib:
									cont_label = file_root.find('did/container').attrib['type']
								else:
									cont_label = ""
								cont_num = cont.text
								match_count = 0
								for Cont_Sheet in CSheet.find('ContainerData'):
									if len(parent_id) > 0  and Cont_Sheet.find('ContainerParent').text:
										if parent_id == Cont_Sheet.find('ContainerParent').text:
											if len(cont_num) > 0 and Cont_Sheet.find('ContainerNumber').text:
												if cont_num == Cont_Sheet.find('ContainerNumber').text:
													if len(cont_label) > 1 and Cont_Sheet.find('ContainerLabel').text:
														if  cont_label.lower() == Cont_Sheet.find('ContainerLabel').text.lower():
															pass
														else:
															match_count = match_count + 1
													else:
														match_count = match_count + 1
									else:
										if len(cont_num) > 0 and Cont_Sheet.find('ContainerNumber').text:
											if cont_num == Cont_Sheet.find('ContainerNumber').text:
												if len(cont_label) > 1 and Cont_Sheet.find('ContainerLabel').text:
													if  cont_label.lower() == Cont_Sheet.find('ContainerLabel').text.lower():
														pass
													else:
														match_count = match_count + 1
												else:
													match_count = match_count + 1
								if match_count < 1:
									Container_element = ET.Element('Container')
									CSheet.find('ContainerData').append(Container_element)
									ContainerParent_element = ET.Element('ContainerParent')
									Container_element.append(ContainerParent_element)
									ContainerLabel_element = ET.Element('ContainerLabel')
									Container_element.append(ContainerLabel_element)
									ContainerNumber_element = ET.Element('ContainerNumber')
									Container_element.append(ContainerNumber_element)
									ContainerID_element = ET.Element('ContainerID')
									Container_element.append(ContainerID_element)
									ContainerParent_element.text = parent_id
									ContainerLabel_element.text = cont_label
									ContainerNumber_element.text = cont_num
									ContainerID_element.text = cont.attrib['id']
				
				#<unitdate>
				if file_root.find('did/unittitle/unitdate') is None:
					pass
				else:
					Date1_element.text = file_root.find('did/unittitle/unitdate').text
					if "normal" in file_root.find('did/unittitle/unitdate').attrib:
						Date1Normal_element.text = file_root.find('did/unittitle/unitdate').attrib['normal']
				
				if file_root.find('did/unittitle') is None:
					if file_root.find('did/odd/p') is None:
						pass
					else:
						UnitTitle_element.text = mixed_content(file_root.find('did/odd/p'))
				else:
					if file_root.find('did/unittitle/unitdate') is None:
						UnitTitle_element.text = mixed_content(file_root.find('did/unittitle'))
					else:
						file_root.find('did/unittitle').remove(file_root.find('did/unittitle/unitdate'))
						UnitTitle_element.text = mixed_content(file_root.find('did/unittitle'))
						
				date_count = 0
				for date in file_root.find('did'):
					if date.tag == "unitdate":
						date_count = date_count + 1
						if date_count == 1:
							Date1_element.text = date.text
							if "normal" in date.attrib:
								Date1Normal_element.text = date.attrib['normal']
						if date_count == 2:
							Date2_element.text = date.text
							if "normal" in date.attrib:
								Date2Normal_element.text  = date.attrib['normal']
						if date_count == 3:
							Date3_element.text = date.text
							if "normal" in date.attrib:
								Date3Normal_element.text  = date.attrib['normal']
						if date_count == 4:
							Date4_element.text = date.text
							if "normal" in date.attrib:
								Date4Normal_element.text  = date.attrib['normal']
						if date_count == 5:
							Date5_element.text = date.text
							if "normal" in date.attrib:
								Date5Normal_element.text  = date.attrib['normal']
						if date_count > 5:
							Date5_element.text = Date5_element.text + ", " + date.text
							if "normal" in date.attrib:
								Date5Normal_element.text  = Date5Normal_element.text + "," + date.attrib['normal']
			
				#<physdesc>			
				if file_root.find('did/physdesc') is None:
					pass
				else:
					if file_root.find('did/physdesc/extent') is None:
						Quantity_element.text = file_root.find('did/physdesc').text
					else:
						Quantity_element.text = file_root.find('did/physdesc/extent').text
						if "unit" in file_root.find('did/physdesc/extent').attrib:
							UnitType_element.text = file_root.find('did/physdesc/extent').attrib['unit']
					if file_root.find('did/physdesc/dimensions') is None:
						pass
					else:
						Dimensions_element.text = file_root.find('did/physdesc/dimensions').text
						if "unit" in file_root.find('did/physdesc/dimensions').attrib:
							DimensionsUnit_element.text = file_root.find('did/physdesc/dimensions').attrib['unit']
					if file_root.find('did//physdesc/physfacet') is None:
						pass
					else:
						PhysicalFacet_element.text = file_root.find('did/physdesc/physfacet').text
				
				#<physdescstructured>
				if version == "ead3":
					if file_root.find('did/physdescstructured') is None:
						pass
					else:
						if "coverage" in file_root.find('did/physdescstructured').attrib:
							Coverage_element.text = file_root.find('did/physdescstructured').attrib['coverage']
						if "physdescstructuredtype" in file_root.find('did/physdescstructured').attrib:
							Type_element.text = file_root.find('did/physdescstructured').attrib['physdescstructuredtype']
						if file_root.find('did/physdescstructured/quantity') is None:
							pass
						else:
							Quantity_element.text = file_root.find('did/physdescstructured/quantity').text
							if "approximate" in file_root.find('did/physdescstructured/quantity').attrib:
								Approximate_element.text = file_root.find('did/physdescstructured/quantity').attrib['approximate']
						if file_root.find('did/physdescstructured/unittype') is None:
							pass
						else:
							UnitType_element = file_root.find('did/physdescstructured/unittype').text
						if file_root.find('did/physdescstructured/dimensions') is None:
							pass
						else:
							Dimensions_element.text = file_root.find('did/physdescstructured/dimensions').text
						if "unit" in file_root.find('did/physdescstructured/dimensions').attrib:
							DimensionsUnit_element.text = file_root.find('did/physdescstructured/dimensions').attrib['unit']
						if file_root.find('did/physdescstructured/physfacet') is None:
							pass
						else:
							PhysicalFacet_element.text = file_root.find('did/physdescstructured/physfacet').text
							
				#notes
				if file_root.find('did/note/p') is None:
					pass
				else:
					PhysDescNote_element.text = mixed_content(file_root.find('did/note/p'))
				
				#digital objects
				if file_root.find('did/dao') is None:
					pass
				else:
					if "daotype" in file_root.find('did/dao').attrib:
						DigitalObjectType_element.text = file_root.find('did/dao').attrib['daotype']
					if 'identifier' in file_root.find('did/dao').attrib:
						DigitalObjectID_element.text = file_root.find('did/dao').attrib['identifier']
					if 'id' in file_root.find('did/dao').attrib:
						DigitalObjectID_element.text = file_root.find('did/dao').attrib['id']
					if 'href' in file_root.find('did/dao').attrib:
						DigitalObjectLink_element.text = file_root.find('did/dao').attrib['href']
					if 'localtype' in file_root.find('did/dao').attrib:
						DigitalObjectLocalName_element.text = file_root.find('did/dao').attrib['localtype']
					if 'title' in file_root.find('did/dao').attrib:
						DigitalObjectLocalName_element.text = file_root.find('did/dao').attrib['title']
					if file_root.find('did/dao/daodesc/p') is None:
						pass
					else:
						DigitalObjectNote_element.text = mixed_content(file_root.find('did/dao/daodesc/p'))
					if file_root.find('did/dao/descriptivenote/p') is None:
						pass
					else:
						DigitalObjectNote_element.text = mixed_content(file_root.find('did/dao/descriptivenote/p'))
				if file_root.find('did/daogrp') is None:
					pass
				else:
					if 'id' in file_root.find('did/daogrp').attrib:
						DigitalObjectID_element.text = file_root.find('did/daogrp').attrib['id']
					if file_root.find('did/daogrp/daoloc') is None:
						pass
					else:
						if 'href' in file_root.find('did/daogrp/daoloc').attrib:
							DigitalObjectLink_element.text = file_root.find('did/daogrp/daoloc').attrib['href']
					if 'title' in file_root.find('did/daogrp').attrib:
						DigitalObjectLocalName_element.text = file_root.find('did/daogrp').attrib['title']
					if file_root.find('did/dao/daodesc/p') is None:
						pass
					else:
						DigitalObjectNote_element.text = mixed_content(file_root.find('did/dao/daodesc/p'))
					if file_root.find('did/dao/descriptivenote/p') is None:
						pass
					else:
						DigitalObjectNote_element.text = mixed_content(file_root.find('did/dao/descriptivenote/p'))
				
				#lower level <archdesc> elements
				archdesc_lower(cmpnt_root, CSheet, version)
				