# module for components <c> or <c01>, <c02>, etc.
import xml.etree.cElementTree as ET
import globals
from date import magic_date
from date import record_magic_date

def components(c_root, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser):
	if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text:
		pass
	else:
		input_data.find('CollectionSheet/IDModel/CollectionSeparator').text = ""
	if input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
		pass
	else:
		 input_data.find('CollectionSheet/IDModel/SeriesSeparator').text = ""
	did_element = ET.Element('did')
	c_root.append(did_element)
	if cmpnt_info.find('SeriesName').text:
		unittitle_element = ET.Element('unittitle')
		did_element.append(unittitle_element)
		unittitle_element.text = cmpnt_info.find('SeriesName').text
	if cmpnt_info.find('SeriesNumber').text:
		if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text:
			if cmpnt_info.find('SeriesNumber').text.startswith(collectionID):
				if "id" in old_ser.attrib:
					c_root.set('id', cmpnt_info.find('SeriesNumber').text)
				else:
					unitid_element = ET.Element('unitid')
					did_element.append(unitid_element)
					unitid_element.text = cmpnt_info.find('SeriesNumber').text
			else:
				if "id" in old_ser.attrib:
					c_root.set('id', collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + cmpnt_info.find('SeriesNumber').text)
				else:
					unitid_element = ET.Element('unitid')
					did_element.append(unitid_element)
					unitid_element.text = collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + cmpnt_info.find('SeriesNumber').text
		else:
			if "id" in old_ser.attrib:
				c_root.set('id', cmpnt_info.find('SeriesNumber').text)
			else:
				unitid_element = ET.Element('unitid')
				did_element.append(unitid_element)
				unitid_element.text = cmpnt_info.find('SeriesNumber').text
	if old_did.find('unittitle/unitdate') is None:
		if cmpnt_info.find('SeriesDate').text:
			unitdate_element = ET.Element('unitdate')
			if len(component_era) < 1:
				pass
			else:
				unitdate_element.attrib['era'] = component_era
			if len(component_cal) < 1:
				pass
			else:
				unitdate_element.attrib['calendar'] = component_cal
			did_element.append(unitdate_element)
			unitdate_element.text = cmpnt_info.find('SeriesDate').text
			if version == "ead2002":
				unitdate_element.set('type', 'inclusive')
			else:
				unitdate_element.set('unitdatetype', 'inclusive')
			if cmpnt_info.find('SeriesDate').text.lower().startswith("ca.") or cmpnt_info.find('SeriesDate').text.lower().startswith("circa"):
					unitdate_element.set('certainty', 'circa')
			if cmpnt_info.find('SeriesDateNormal').text:
				unitdate_element.set('normal', cmpnt_info.find('SeriesDateNormal').text)
			else:
				unitdate_element.set('normal', cmpnt_info.find('SeriesDate').text)
			if version == "ead3":
				did_element.append(magic_date(cmpnt_info.find('SeriesDate').text, cmpnt_info.find('SeriesDateNormal').text, 'inclusive'))
	else:
		if cmpnt_info.find('SeriesDate').text:
			unitdate_element = ET.Element('unitdate')
			if len(component_era) < 1:
				pass
			else:
				unitdate_element.attrib['era'] = component_era
			if len(component_cal) < 1:
				pass
			else:
				unitdate_element.attrib['calendar'] = component_cal
			if old_did.find('../c02/did/unitdate') is None:
				unittitle_element.append(unitdate_element)
			else:
				did_element.append(unitdate_element)
			unitdate_element.text = cmpnt_info.find('SeriesDate').text
			if version == "ead2002":
				unitdate_element.set('type', 'inclusive')
			else:
				unitdate_element.set('unitdatetype', 'inclusive')
				if cmpnt_info.find('SeriesDate').text.lower().startswith("ca.") or cmpnt_info.find('SeriesDate').text.lower().startswith("circa"):
					unitdate_element.set('certainty', 'circa')
			if cmpnt_info.find('SeriesDateNormal').text:
				unitdate_element.set('normal', cmpnt_info.find('SeriesDateNormal').text)
			else:
				unitdate_element.set('normal', cmpnt_info.find('SeriesDate').text)
	if old_did.find('unittitle/unitdate') is None:
		if cmpnt_info.find('SeriesBulkDate').text:
			unitdate_element = ET.Element('unitdate')
			if len(component_era) < 1:
				pass
			else:
				unitdate_element.attrib['era'] = component_era
			if len(component_cal) < 1:
				pass
			else:
				unitdate_element.attrib['calendar'] = component_cal
			did_element.append(unitdate_element)
			unitdate_element.text = cmpnt_info.find('SeriesBulkDate').text
			if version == "ead2002":
				unitdate_element.set('type', 'bulk')
			else:
				unitdate_element.set('unitdatetype', 'bulk')
				if cmpnt_info.find('SeriesBulkDate').text.lower().startswith("ca.") or cmpnt_info.find('SeriesBulkDate').text.lower().startswith("circa"):
					unitdate_element.set('certainty', 'circa')
			if cmpnt_info.find('SeriesBulkDateNormal').text:
				unitdate_element.set('normal', cmpnt_info.find('SeriesBulkDateNormal').text)
			else:
				unitdate_element.set('normal', cmpnt_info.find('SeriesBulkDate').text)
			if version == "ead3":
				did_element.append(magic_date(cmpnt_info.find('SeriesBulkDate').text, cmpnt_info.find('SeriesBulkDateNormal').text, 'bulk'))
	else:
		if cmpnt_info.find('SeriesBulkDate').text:
			unitdate_element = ET.Element('unitdate')
			if len(component_era) < 1:
				pass
			else:
				unitdate_element.attrib['era'] = component_era
			if len(component_cal) < 1:
				pass
			else:
				unitdate_element.attrib['calendar'] = component_cal
			if old_did.find('../c02/did/unitdate') is None:
				unittitle_element.append(unitdate_element)
			else:
				did_element.append(unitdate_element)
			unitdate_element.text = cmpnt_info.find('SeriesBulkDate').text
			if version == "ead2002":
				unitdate_element.set('type', 'bulk')
			else:
				unitdate_element.set('unitdatetype', 'bulk')
				if cmpnt_info.find('SeriesBulkDate').text.lower().startswith("ca.") or cmpnt_info.find('SeriesBulkDate').text.lower().startswith("circa"):
					unitdate_element.set('certainty', 'circa')
			if cmpnt_info.find('SeriesBulkDateNormal').text:
				unitdate_element.set('normal', cmpnt_info.find('SeriesBulkDateNormal').text)
			else:
				unitdate_element.set('normal', cmpnt_info.find('SeriesBulkDate').text)
	
	#physdesc and physdescstructured
	from physdesc import simple
	from physdesc import structured
	if old_physdesc is None:
		old_physdesc = ""
	if len(old_physdesc) < 1:
		simple(did_element, cmpnt_info, version)
	else:
		did_element.append(old_physdesc)
		simple(did_element, cmpnt_info, version)
	if version == "ead3":
		if old_physdescstructured == True:
			temp_structured_element = ET.Element('physdescstructured')
			did_element.append(temp_structured_element)
			structured(did_element, cmpnt_info)
			
	if cmpnt_info.find('Arrangement/p') is None:
		pass
	else:
		if cmpnt_info.find('Arrangement/p').text:
			arr_element = ET.Element('arrangement')
			c_root.append(arr_element)
			if len(arr_head) < 1:
				pass
			else:
				arr_element.append(arr_head)
			for arrange in cmpnt_info.find('Arrangement'):
				p_element = ET.Element('p')
				arr_element.append(p_element)
				p_element.text = arrange.text
	if cmpnt_info.find('Description/p') is None:
		pass
	else:
		if cmpnt_info.find('Description/p').text:
			sc_element = ET.Element('scopecontent')
			c_root.append(sc_element)
			if len(sc_head) < 1:
				pass
			else:
				sc_element.append(sc_head)
			for scope in cmpnt_info.find('Description'):
				p_element = ET.Element('p')
				sc_element.append(p_element)
				p_element.text = scope.text
			
	if c_root.tag == "c":
		file_tag = "c"
	else:
		if int(c_root.tag[1:]) > 9:
			file_tag = "c" + str(int(c_root.tag[1:]) + 1)
			digi_tag = "c" + str(int(c_root.tag[1:]) + 2)
		else:
			file_tag = "c0" + str(int(c_root.tag[1:]) + 1)
			digi_tag = "c0" + str(int(c_root.tag[1:]) + 2)
	
	container_element = ""
	
	for record in cmpnt_info:
		if record.tag == "Record":
			if record.find('UnitTitle').text or record.find('UnitNumber').text or record.find('BoxNumber').text:
				file_element = ET.Element(file_tag)
				c_root.append(file_element)
				if cmpnt_info.find('DescriptionLevel').text:
					if "ask_ualbany" in globals.new_elements:
						pass
					else:
						file_element.set('level', cmpnt_info.find('DescriptionLevel').text.lower())
				did_element = ET.Element('did')
				file_element.append(did_element)
				if record.find('BoxNumber').text:
					container_element = ET.Element('container')
					did_element.append(container_element)
					container_element.text = record.find('BoxNumber').text
					if version == "ead2002":
						if record.find('BoxName').text:
							container_element.set('type', record.find('BoxName').text)
						if input_data.find('CollectionSheet/ContainerData') is None:
							pass
						else:
							for container in input_data.find('CollectionSheet/ContainerData'):
								if container.find('ContainerNumber').text == record.find('BoxNumber').text:
									if record.find('BoxName').text:
										if container.find('ContainerLabel').text == record.find('BoxName').text:
											if record.find('BoxName').text.lower() == "box":
												if container.find('ContainerParent').text == cmpnt_info.find('SeriesNumber').text:
													if container.find('ContainerID').text:
														container_element.set('id', container.find('ContainerID').text)
											else:
												if container.find('ContainerID').text:
													container_element.set('id', container.find('ContainerID').text)                                
					else:
						if record.find('BoxName').text:
							container_element.set('localtype', record.find('BoxName').text)
						for container in input_data.find('CollectionSheet/ContainerData'):
							if container.find('ContainerNumber').text == record.find('BoxNumber').text:
								if record.find('BoxName').text:
									if container.find('ContainerLabel').text == record.find('BoxName').text:
										if record.find('BoxName').text.lower() == "box":
											if container.find('ContainerParent').text == cmpnt_info.find('SeriesNumber').text:
												if container.find('ContainerID').text:
													container_element.set('containerid', container.find('ContainerID').text)
										else:
											if container.find('ContainerID').text:
												container_element.set('containerid', container.find('ContainerID').text)
				if record.find('UnitNumber').text:
					folder_element = ET.Element('container')
					did_element.append(folder_element)
					folder_element.text = record.find('UnitNumber').text
					if record.find('Unit').text:
						if version == "ead2002":
							folder_element.set('type', record.find('Unit').text)
						else:
							folder_element.set('localtype', record.find('Unit').text)
					if len(container_element) < 1:
						pass
					else:
						if "id" in container_element.attrib:
							folder_element.set('parent', container_element.attrib['id'])
						elif "containerid" in container_element.attrib:
							folder_element.set('parent', container_element.attrib['containerid'])
				if record.find('UnitTitle').text:
					unittitle_element = ET.Element('unittitle')
					did_element.append(unittitle_element)
					unittitle_element.text = record.find('UnitTitle').text
					
				
				
				# <unitid>
				if record.find('RecordID').text:
					if record.find('RecordID').text != ".":
						if "id" in old_cmpt.attrib:
							if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and input_data.find('CollectionSheet/IDModel/SeriesSeparator').text and cmpnt_info.find('SeriesNumber').text:
								if record.find('RecordID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
									file_element.set('id', record.find('RecordID').text)
								else:
									file_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + record.find('RecordID').text)
							else:
								if input_data.find('CollectionSheet/IDModel/SeriesSeparator').text and cmpnt_info.find('SeriesNumber').text :
									if record.find('RecordID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
										file_element.set('id', record.find('RecordID').text)
									else:
										file_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + record.find('RecordID').text)
								elif input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and cmpnt_info.find('SeriesNumber').text :
									if record.find('RecordID').text.startswith(cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
										file_element.set('id', record.find('RecordID').text)
									else:
										file_element.set('id', cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text)
								else:
									file_element.set('id', record.find('RecordID').text)
						elif old_cmpt.find('did/unitid') is None:
							if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and input_data.find('CollectionSheet/IDModel/SeriesSeparator').text and cmpnt_info.find('SeriesNumber').text:
								if record.find('RecordID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
									file_element.set('id', record.find('RecordID').text)
								else:
									file_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + record.find('RecordID').text)
							else:
								if input_data.find('CollectionSheet/IDModel/SeriesSeparator').text and cmpnt_info.find('SeriesNumber').text :
									if record.find('RecordID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
										file_element.set('id', record.find('RecordID').text)
									else:
										file_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + record.find('RecordID').text)
								elif input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and cmpnt_info.find('SeriesNumber').text :
									if record.find('RecordID').text.startswith(cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
										file_element.set('id', record.find('RecordID').text)
									else:
										file_element.set('id', cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text)
								else:
									file_element.set('id', record.find('RecordID').text)
						else:
							unitid_element = ET.Element('unitid')
							did_element.append(unitid_element)
							if input_data.find('CollectionSheet/IDModel/SeriesSeparator').text and input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and cmpnt_info.find('SeriesNumber').text:
								if record.find('RecordID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
									unitid_element.text = record.find('RecordID').text	
								else:
									unitid_element.text = collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + record.find('RecordID').text
							else:
								if input_data.find('CollectionSheet/IDModel/SeriesSeparator').text and cmpnt_info.find('SeriesNumber').text:
									if record.find('RecordID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
										unitid_element.text = record.find('RecordID').text	
									else:
										unitid_element.text = collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + record.find('RecordID').text
								elif input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and cmpnt_info.find('SeriesNumber').text:
									if record.find('RecordID').text.startswith(cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
										unitid_element.text = record.find('RecordID').text	
									else:
										unitid_element.text = cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text
								else:
									unitid_element.text = record.find('RecordID').text	
				# <unitdate>
				if version == "ead2002":
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									unitdate_element = ET.Element('unitdate')
									if len(component_era) < 1:
										pass
									else:
										unitdate_element.attrib['era'] = component_era
									if len(component_cal) < 1:
										pass
									else:
										unitdate_element.attrib['calendar'] = component_cal
									unitdate_element.text = date.text
									normal_element = date.tag + "Normal"
									if record.find(normal_element).text:
										unitdate_element.set('normal', record.find(normal_element).text)
									else:
										unitdate_element.set('normal', date.text)
									if old_did.find('unittitle/unitdate') is None:
										did_element.append(unitdate_element)
									else:
										if old_did.find('../c01/c02/did/unitdate') is None:
											unittitle_element.append(unitdate_element)
										else:
											did_element.append(unitdate_element)
					if record.find('Quantity').text or record.find('Dimensions').text:
						physdesc_element = ET.Element('physdesc')
						did_element.append(physdesc_element)
						if record.find('Quantity').text:
							extent_element = ET.Element('extent')
							physdesc_element.append(extent_element)
							extent_element.text = record.find('Quantity').text
							if record.find('UnitType').text:
								extent_element.set('unit', record.find('UnitType').text)
						if record.find('PhysicalFacet').text:
							physfacet_element = ET.Element('physfacet')
							physdesc_element.append(physfacet_element)
							physfacet_element.text = record.find('PhysicalFacet').text
						if record.find('Dimensions').text:
							dimensions_element = ET.Element('dimensions')
							physdesc_element.append(dimensions_element)
							dimensions_element.text = record.find('Dimensions').text
							if record.find('DimensionsUnit').text:
								dimensions_element.set('unit', record.find('DimensionsUnit').text)
				else:
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									unitdate_element = ET.Element('unitdate')
									if len(component_era) < 1:
										pass
									else:
										unitdate_element.attrib['era'] = component_era
									if len(component_cal) < 1:
										pass
									else:
										unitdate_element.attrib['calendar'] = component_cal
									unitdate_element.text = date.text
									if date.text.lower().startswith("ca.") or date.text.lower().startswith("circa"):
										unitdate_element.set('certainty', 'circa')
									normal_element = date.tag + "Normal"
									if record.find(normal_element).text:
										unitdate_element.set('normal', record.find(normal_element).text)
									else:
										unitdate_element.set('normal', date.text)
									if old_did.find('unittitle/unitdate') is None:
										did_element.append(unitdate_element)
									else:
										if old_did.find('../c01/c02/did/unitdate') is None:
											unittitle_element.append(unitdate_element)
										else:
											did_element.append(unitdate_element)
					#unitdatestructured
					record_magic_date(did_element, record)
					
				if record.find('DigitalObjectID').text or record.find('DigitalObjectLink').text:
					dao_element = ET. Element('dao')
					did_element.append(dao_element)
					if record.find('DigitalObjectLink').text:
						dao_element.set('href', record.find('DigitalObjectLink').text)
					if version == "ead2002":
						dao_element.set('linktype', 'simple')
						dao_element.set('actuate', 'onrequest')
						dao_element.set('show', 'new')
						if record.find('DigitalObjectID').text:
							
							if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
								if record.find('DigitalObjectID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
									dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
								else:
									dao_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + record.find('RecordID').text+ "." + record.find('DigitalObjectID').text)
							else:
								if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text:
									if record.find('DigitalObjectID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
										dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
									else:
										dao_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
								elif input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
									if record.find('RecordID').text.startswith(cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
										dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
									else:
										dao_element.set('id', cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text)
								else:
									dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
							
						if record.find('DigitalObjectLocalName').text:
							dao_element.set('title', record.find('DigitalObjectLocalName').text)
						if record.find('DigitalObjectNote').text:
							daodesc_element = ET.Element('daodesc')
							dao_element.append(daodesc_element)
							p_element = ET.Element('p')
							daodesc_element.append(p_element)
							p_element.text = record.find('DigitalObjectNote').text
					else:
						if record.find('DigitalObjectType').text:
							dao_element.set('daotype ', record.find('DigitalObjectType').text)
						else:
							from messages import error
							error("You failed to enter a Digital Object Type for record " + record.find('RecordID').text + ". @daotype is required in EAD3, so your finding aid will not be valid.", False)
						dao_element.set('actuate', 'onrequest')
						dao_element.set('show', 'new')
						if record.find('DigitalObjectID').text:
							
							if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
								if record.find('DigitalObjectID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
									dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
								else:
									dao_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + record.find('RecordID').text+ "." + record.find('DigitalObjectID').text)
							else:
								if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text:
									if record.find('DigitalObjectID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
										dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
									else:
										dao_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
								elif input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
									if record.find('RecordID').text.startswith(cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
										dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
									else:
										dao_element.set('id', cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text)
								else:
									dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
							
						if record.find('DigitalObjectLocalName').text:
							dao_element.set('localtype', record.find('DigitalObjectLocalName').text)
						if record.find('DigitalObjectNote').text:
							descriptivenote_element = ET.Element('descriptivenote')
							dao_element.append(descriptivenote_element)
							p_element = ET.Element('p')
							descriptivenote_element.append(p_element)
							p_element.text = record.find('DigitalObjectNote').text

				if record.find('PhysDescNote').text:
					note_element = ET.Element("note")
					did_element.append(note_element)
					p_element = ET.Element('p')
					note_element.append(p_element)
					p_element.text = record.find('PhysDescNote').text
			
			#multiple digital objects
			elif record.find('DigitalObjectLink').text or record.find('DigitalObjectID').text or record.find('DigitalObjectLocalName').text:
				#sub file-level or sub item-level digital objects
				digi_element = ET.Element(digi_tag)
				file_element.append(digi_element)
				did_element = ET.Element("did")
				digi_element.append(did_element)
				if record.find('DigitalObjectID').text:
					if 'id' in file_element.attrib:
						dao_element.set('id', file_element.attrib['id'] + "." + record.find('DigitalObjectID').text)
					else:
						dao_element.set('id', record.find('DigitalObjectID').text)
				unittitle_element = ET.Element('unittitle')
				did_element.append(unittitle_element)
				if record.find('DigitalObjectLocalName').text:
					unittitle_element.text = record.find('DigitalObjectLocalName').text
				else:
					unittitle_element.text = "Digital object"
				
				# <unitdate>
				if version == "ead2002":
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									unitdate_element = ET.Element('unitdate')
									if len(component_era) < 1:
										pass
									else:
										unitdate_element.attrib['era'] = component_era
									if len(component_cal) < 1:
										pass
									else:
										unitdate_element.attrib['calendar'] = component_cal
									unitdate_element.text = date.text
									normal_element = date.tag + "Normal"
									if record.find(normal_element).text:
										unitdate_element.set('normal', record.find(normal_element).text)
									else:
										unitdate_element.set('normal', date.text)
									if old_did.find('unittitle/unitdate') is None:
										did_element.append(unitdate_element)
									else:
										if old_did.find('../c01/c02/did/unitdate') is None:
											unittitle_element.append(unitdate_element)
										else:
											did_element.append(unitdate_element)
				else:
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									unitdate_element = ET.Element('unitdate')
									if len(component_era) < 1:
										pass
									else:
										unitdate_element.attrib['era'] = component_era
									if len(component_cal) < 1:
										pass
									else:
										unitdate_element.attrib['calendar'] = component_cal
									unitdate_element.text = date.text
									if date.text.lower().startswith("ca.") or date.text.lower().startswith("circa"):
										unitdate_element.set('certainty', 'circa')
									normal_element = date.tag + "Normal"
									if record.find(normal_element).text:
										unitdate_element.set('normal', record.find(normal_element).text)
									else:
										unitdate_element.set('normal', date.text)
									if old_did.find('unittitle/unitdate') is None:
										did_element.append(unitdate_element)
									else:
										if old_did.find('../c01/c02/did/unitdate') is None:
											unittitle_element.append(unitdate_element)
										else:
											did_element.append(unitdate_element)
					#unitdatestructured
					record_magic_date(did_element, record)
				
				#physdesc for digital object
				if record.find('Quantity').text or record.find('Dimensions').text:
					physdesc_element = ET.Element('physdesc')
					did_element.append(physdesc_element)
					if record.find('Quantity').text:
						extent_element = ET.Element('extent')
						physdesc_element.append(extent_element)
						extent_element.text = record.find('Quantity').text
						if record.find('UnitType').text:
							extent_element.set('unit', record.find('UnitType').text)
					if record.find('PhysicalFacet').text:
						physfacet_element = ET.Element('physfacet')
						physdesc_element.append(physfacet_element)
						physfacet_element.text = record.find('PhysicalFacet').text
					if record.find('Dimensions').text:
						dimensions_element = ET.Element('dimensions')
						physdesc_element.append(dimensions_element)
						dimensions_element.text = record.find('Dimensions').text
						if record.find('DimensionsUnit').text:
							dimensions_element.set('unit', record.find('DimensionsUnit').text)
				
				if record.find('DigitalObjectNote').text:
					descriptivenote_element = ET.Element('note')
					did_element.append(descriptivenote_element)
					p_element = ET.Element('p')
					descriptivenote_element.append(p_element)
					p_element.text = record.find('DigitalObjectNote').text
				
			

def no_series(c_element, cmpnt_info, version, dsc_root, input_data, old_cmpt, collectionID, component_era, component_cal, old_did):
	if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text:
		pass
	else:
		input_data.find('CollectionSheet/IDModel/CollectionSeparator').text = ""
	if input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
		pass
	else:
		 input_data.find('CollectionSheet/IDModel/SeriesSeparator').text = ""
	for record in cmpnt_info:
		if record.tag == "Record":
			if record.find('UnitTitle').text or record.find('UnitNumber').text or record.find('Date1').text or record.find('Quantity').text:
				file_element = ET.Element(c_element.tag)
				dsc_root.append(file_element)
				if cmpnt_info.find('DescriptionLevel').text:
					if "ask_ualbany" in globals.new_elements:
						pass
					else:
						file_element.set('level', cmpnt_info.find('DescriptionLevel').text.lower())
				did_element = ET.Element('did')
				file_element.append(did_element)
				if record.find('BoxNumber').text:
					container_element = ET.Element('container')
					did_element.append(container_element)
					container_element.text = record.find('BoxNumber').text
					if version == "ead2002":
						if record.find('BoxName').text:
							container_element.set('type', record.find('BoxName').text)
						for container in input_data.find('CollectionSheet/ContainerData'):
							if container.find('ContainerNumber').text == record.find('BoxNumber').text:
								if record.find('BoxName').text:
									if container.find('ContainerLabel').text == record.find('BoxName').text:
										if record.find('BoxName').text.lower() == "box":
											if container.find('ContainerParent').text == cmpnt_info.find('SeriesNumber').text:
												if container.find('ContainerID').text:
													container_element.set('id', container.find('ContainerID').text)
										else:
											if container.find('ContainerID').text:
												container_element.set('id', container.find('ContainerID').text)                                
					else:
						if record.find('BoxName').text:
							container_element.set('localtype', record.find('BoxName').text)
						for container in input_data.find('CollectionSheet/ContainerData'):
							if container.find('ContainerNumber').text == record.find('BoxNumber').text:
								if record.find('BoxName').text:
									if container.find('ContainerLabel').text == record.find('BoxName').text:
										if record.find('BoxName').text.lower() == "box":
											if container.find('ContainerParent').text == cmpnt_info.find('SeriesNumber').text:
												if container.find('ContainerID').text:
													container_element.set('containerid', container.find('ContainerID').text)
										else:
											if container.find('ContainerID').text:
												container_element.set('containerid', container.find('ContainerID').text)
				if record.find('UnitNumber').text:
					folder_element = ET.Element('container')
					did_element.append(folder_element)
					folder_element.text = record.find('UnitNumber').text
					if record.find('Unit').text:
						if version == "ead2002":
							folder_element.set('type', record.find('Unit').text)
						else:
							folder_element.set('localtype', record.find('Unit').text)
					if container_element is None:
						pass
					else:
						if "id" in container_element.attrib:
							folder_element.set('parent', container_element.attrib['id'])
						elif "containerid" in container_element.attrib:
							folder_element.set('parent', container_element.attrib['containerid'])
				if record.find('UnitTitle').text:
					unittitle_element = ET.Element('unittitle')
					did_element.append(unittitle_element)
					unittitle_element.text = record.find('UnitTitle').text
				if record.find('RecordID').text:
					if record.find('RecordID').text.startswith(collectionID):
						uid = record.find('RecordID').text
					else:
						uid = collectionID + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + record.find('RecordID').text
					if old_cmpt.find('did/unitid') is None:
						file_element.set('id', uid)
					else:
						unitid_element = ET.Element('unitid')
						did_element.append(unitid_element)
						unitid_element.text = uid
				if version == "ead2002":
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									unitdate_element = ET.Element('unitdate')
									if len(component_era) < 1:
										pass
									else:
										unitdate_element.attrib['era'] = component_era
									if len(component_cal) < 1:
										pass
									else:
										unitdate_element.attrib['calendar'] = component_cal
									unitdate_element.text = date.text
									normal_element = date.tag + "Normal"
									if record.find(normal_element).text:
										unitdate_element.set('normal', record.find(normal_element).text)
									else:
										unitdate_element.set('normal', date.text)
									if old_did.find('unittitle/unitdate') is None:
										did_element.append(unitdate_element)
									else:
										if old_did.find('../c01/c02/did/unitdate') is None:
											unittitle_element.append(unitdate_element)
										else:
											did_element.append(unitdate_element)
					if record.find('Quantity').text or record.find('Dimensions').text:
						physdesc_element = ET.Element('physdesc')
						did_element.append(physdesc_element)
						if record.find('Quantity').text:
							extent_element = ET.Element('extent')
							physdesc_element.append(extent_element)
							extent_element.text = record.find('Quantity').text
							if record.find('UnitType').text:
								extent_element.set('unit', record.find('UnitType').text)
						if record.find('PhysicalFacet').text:
							physfacet_element = ET.Element('physfacet')
							physdesc_element.append(physfacet_element)
							physfacet_element.text = record.find('PhysicalFacet').text
						if record.find('Dimensions').text:
							dimensions_element = ET.Element('dimensions')
							physdesc_element.append(dimensions_element)
							dimensions_element.text = record.find('Dimensions').text
							if record.find('DimensionsUnit').text:
								dimensions_element.set('unit', record.find('DimensionsUnit').text)
				else:
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									unitdate_element = ET.Element('unitdate')
									if len(component_era) < 1:
										pass
									else:
										unitdate_element.attrib['era'] = component_era
									if len(component_cal) < 1:
										pass
									else:
										unitdate_element.attrib['calendar'] = component_cal
									unitdate_element.text = date.text
									if date.text.lower().startswith("ca.") or date.text.lower().startswith("circa"):
										unitdate_element.set('certainty', 'circa')
									normal_element = date.tag + "Normal"
									if record.find(normal_element).text:
										unitdate_element.set('normal', record.find(normal_element).text)
									else:
										unitdate_element.set('normal', date.text)
									if old_did.find('unittitle/unitdate') is None:
										did_element.append(unitdate_element)
									else:
										if old_did.find('../c01/c02/did/unitdate') is None:
											unittitle_element.append(unitdate_element)
										else:
											did_element.append(unitdate_element)
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									date_normal = record.find(date.tag + "Normal")
									did_element.append(magic_date(date.text, date_normal.text, 'inclusive'))
					
				if record.find('DigitalObjectID').text or record.find('DigitalObjectLink').text:
					dao_element = ET. Element('dao')
					did_element.append(dao_element)
					if record.find('DigitalObjectLink').text:
						dao_element.set('href', record.find('DigitalObjectLink').text)
					if version == "ead2002":
						dao_element.set('linktype', 'simple')
						dao_element.set('actuate', 'onrequest')
						dao_element.set('show', 'new')
						if record.find('DigitalObjectID').text:
							
							if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
								if record.find('DigitalObjectID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
									dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
								else:
									dao_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + record.find('RecordID').text+ "." + record.find('DigitalObjectID').text)
							else:
								if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text:
									if record.find('DigitalObjectID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
										dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
									else:
										dao_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
								elif input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
									if record.find('RecordID').text.startswith(cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
										dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
									else:
										dao_element.set('id', cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text)
								else:
									dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
							
						if record.find('DigitalObjectLocalName').text:
							dao_element.set('title', record.find('DigitalObjectLocalName').text)
						if record.find('DigitalObjectNote').text:
							daodesc_element = ET.Element('daodesc')
							dao_element.append(daodesc_element)
							p_element = ET.Element('p')
							daodesc_element.append(p_element)
							p_element.text = record.find('DigitalObjectNote').text
					else:
						if record.find('DigitalObjectType').text:
							dao_element.set('daotype ', record.find('DigitalObjectType').text)
						else:
							from messages import error
							error("You failed to enter a Digital Object Type for record " + record.find('RecordID').text + ". @daotype is required in EAD3, so your finding aid will not be valid.", False)
						dao_element.set('actuate', 'onrequest')
						dao_element.set('show', 'new')
						if record.find('DigitalObjectID').text:
							
							if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text and input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
								if record.find('DigitalObjectID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
									dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
								else:
									dao_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text + record.find('RecordID').text+ "." + record.find('DigitalObjectID').text)
							else:
								if input_data.find('CollectionSheet/IDModel/CollectionSeparator').text:
									if record.find('DigitalObjectID').text.startswith(collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text):
										dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
									else:
										dao_element.set('id', collectionID + input_data.find('CollectionSheet/IDModel/CollectionSeparator').text + record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
								elif input_data.find('CollectionSheet/IDModel/SeriesSeparator').text:
									if record.find('RecordID').text.startswith(cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text):
										dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
									else:
										dao_element.set('id', cmpnt_info.find('SeriesNumber').text + input_data.find('CollectionSheet/IDModel/SeriesSeparator').text)
								else:
									dao_element.set('id', record.find('RecordID').text + "." + record.find('DigitalObjectID').text)
							
						if record.find('DigitalObjectLocalName').text:
							dao_element.set('localtype', record.find('DigitalObjectLocalName').text)
						if record.find('DigitalObjectNote').text:
							descriptivenote_element = ET.Element('descriptivenote')
							dao_element.append(descriptivenote_element)
							p_element = ET.Element('p')
							descriptivenote_element.append(p_element)
							p_element.text = record.find('DigitalObjectNote').text

				if record.find('PhysDescNote').text:
					note_element = ET.Element("note")
					did_element.append(note_element)
					p_element = ET.Element('p')
					note_element.append(p_element)
					p_element.text = record.find('PhysDescNote').text
					
			#multiple digital objects
			elif record.find('DigitalObjectLink').text or record.find('DigitalObjectID').text or record.find('DigitalObjectLocalName').text:
				#sub file-level or sub item-level digital objects
				digi_element = ET.Element(digi_tag)
				file_element.append(digi_element)
				did_element = ET.Element("did")
				digi_element.append(did_element)
				if record.find('DigitalObjectID').text:
					if 'id' in file_element.attrib:
						dao_element.set('id', file_element.attrib['id'] + "." + record.find('DigitalObjectID').text)
					else:
						dao_element.set('id', record.find('DigitalObjectID').text)
				unittitle_element = ET.Element('unittitle')
				did_element.append(unittitle_element)
				if record.find('DigitalObjectLocalName').text:
					unittitle_element.text = record.find('DigitalObjectLocalName').text
				else:
					unittitle_element.text = "Digital object"
				
				# <unitdate>
				if version == "ead2002":
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									unitdate_element = ET.Element('unitdate')
									if len(component_era) < 1:
										pass
									else:
										unitdate_element.attrib['era'] = component_era
									if len(component_cal) < 1:
										pass
									else:
										unitdate_element.attrib['calendar'] = component_cal
									unitdate_element.text = date.text
									normal_element = date.tag + "Normal"
									if record.find(normal_element).text:
										unitdate_element.set('normal', record.find(normal_element).text)
									else:
										unitdate_element.set('normal', date.text)
									if old_did.find('unittitle/unitdate') is None:
										did_element.append(unitdate_element)
									else:
										if old_did.find('../c01/c02/did/unitdate') is None:
											unittitle_element.append(unitdate_element)
										else:
											did_element.append(unitdate_element)
				else:
					for date in record:
						if date.text:
							if date.tag.startswith("Date"):
								if not date.tag.endswith("Normal"):
									unitdate_element = ET.Element('unitdate')
									if len(component_era) < 1:
										pass
									else:
										unitdate_element.attrib['era'] = component_era
									if len(component_cal) < 1:
										pass
									else:
										unitdate_element.attrib['calendar'] = component_cal
									unitdate_element.text = date.text
									if date.text.lower().startswith("ca.") or date.text.lower().startswith("circa"):
										unitdate_element.set('certainty', 'circa')
									normal_element = date.tag + "Normal"
									if record.find(normal_element).text:
										unitdate_element.set('normal', record.find(normal_element).text)
									else:
										unitdate_element.set('normal', date.text)
									if old_did.find('unittitle/unitdate') is None:
										did_element.append(unitdate_element)
									else:
										if old_did.find('../c01/c02/did/unitdate') is None:
											unittitle_element.append(unitdate_element)
										else:
											did_element.append(unitdate_element)
					#unitdatestructured
					record_magic_date(did_element, record)
				
				#physdesc for digital object
				if record.find('Quantity').text or record.find('Dimensions').text:
					physdesc_element = ET.Element('physdesc')
					did_element.append(physdesc_element)
					if record.find('Quantity').text:
						extent_element = ET.Element('extent')
						physdesc_element.append(extent_element)
						extent_element.text = record.find('Quantity').text
						if record.find('UnitType').text:
							extent_element.set('unit', record.find('UnitType').text)
					if record.find('PhysicalFacet').text:
						physfacet_element = ET.Element('physfacet')
						physdesc_element.append(physfacet_element)
						physfacet_element.text = record.find('PhysicalFacet').text
					if record.find('Dimensions').text:
						dimensions_element = ET.Element('dimensions')
						physdesc_element.append(dimensions_element)
						dimensions_element.text = record.find('Dimensions').text
						if record.find('DimensionsUnit').text:
							dimensions_element.set('unit', record.find('DimensionsUnit').text)
				
				if record.find('DigitalObjectNote').text:
					descriptivenote_element = ET.Element('note')
					did_element.append(descriptivenote_element)
					p_element = ET.Element('p')
					descriptivenote_element.append(p_element)
					p_element.text = record.find('DigitalObjectNote').text