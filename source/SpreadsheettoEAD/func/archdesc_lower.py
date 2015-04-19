# module for <archdesc> elements matched to lower levels of the <dsc> via a unitid
import xml.etree.cElementTree as ET

def acquisitions_lower(arch_root, input_element, version, tag_name, collectionID, series_separator):
	if arch_root.find('dsc/c01') is None and arch_root.find('dsc/c') is None:
		pass
	else:
		if arch_root.find('dsc/c01') is None:
			if arch_root.find('dsc/c') is None:
				pass
			else:
				c_numbers = False
				if "id" in arch_root.find('dsc/c').attrib:
					attribute_id = True
				else:
					attribute_id = False
		else:
			c_numbers = True
			if "id" in arch_root.find('dsc/c01').attrib:
				attribute_id = True
			else:
				attribute_id = False
		if input_element is None:
			pass
		else:
			for acquis in input_element:
				if acquis.find('UnitID').text:
					if acquis.find('Event').text:
						if attribute_id == True:
							if c_numbers == True:
								# @id in <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.attrib['id'] == collectionID + acquis.find('UnitID').text:
											if match.find(tag_name) is None:
												# if there is no <aquis> element
												acquis_element = ET.Element(tag_name)
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, acquis_element)
												chronlist_element = ET.Element('chronlist')
												acquis_element.append(chronlist_element)
												chronitem_element = ET.Element('chronitem')
												chronlist_element.append(chronitem_element)
												event_element = ET.Element('event')
												chronitem_element.append(event_element)
												event_element.text = acquis.find('Event').text
												if version == "ead2002":
													date_element = ET.Element('date')
													chronitem_element.append(date_element)
													date_element.text = acquis.find('Date').text
													date_element.set('normal', acquis.find('DateNormal').text)
												else:
													from date import basic_date
													chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
											else:
												# if there is already an <acquis> element
												chronitem_element = ET.Element('chronitem')
												match.find('acqinfo').append(chronitem_element)
												event_element = ET.Element('event')
												chronitem_element.append(event_element)
												event_element.text = acquis.find('Event').text
												if version == "ead2002":
													date_element = ET.Element('date')
													chronitem_element.append(date_element)
													date_element.text = acquis.find('Date').text
													date_element.set('normal', acquis.find('DateNormal').text)
												else:
													from date import basic_date
													chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
							else:
								# @id in <c>:
								for match in arch_root.find('dsc').iter('c'):
									if match.attrib['id'] == collectionID + acquis.find('UnitID').text:
										if match.find(tag_name) is None:
											# if there is no <aquis> element
											acquis_element = ET.Element(tag_name)
											match.append(acquis_element)
											chronlist_element = ET.Element('chronlist')
											append_index = match.getchildren().index(match.find('did')) + 1
											match.insert(append_index, acquis_element)
											chronitem_element = ET.Element('chronitem')
											chronlist_element.append(chronitem_element)
											event_element = ET.Element('event')
											chronitem_element.append(event_element)
											event_element.text = acquis.find('Event').text
											if version == "ead2002":
												date_element = ET.Element('date')
												chronitem_element.append(date_element)
												date_element.text = acquis.find('Date').text
												date_element.set('normal', acquis.find('DateNormal').text)
											else:
												from date import basic_date
												chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
										else:
											# if there is already an <acquis> element
											chronitem_element = ET.Element('chronitem')
											match.find('acqinfo').append(chronitem_element)
											event_element = ET.Element('event')
											chronitem_element.append(event_element)
											event_element.text = acquis.find('Event').text
											if version == "ead2002":
												date_element = ET.Element('date')
												chronitem_element.append(date_element)
												date_element.text = acquis.find('Date').text
												date_element.set('normal', acquis.find('DateNormal').text)
											else:
												from date import basic_date
												chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
						else:
							if c_numbers == True:
								# <unitid> within <did> of <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + acquis.find('UnitID').text:
												if match.find(tag_name) is None:
													# if there is no <aquis> element
													acquis_element = ET.Element(tag_name)
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, acquis_element)
													chronlist_element = ET.Element('chronlist')
													acquis_element.append(chronlist_element)
													chronitem_element = ET.Element('chronitem')
													chronlist_element.append(chronitem_element)
													event_element = ET.Element('event')
													chronitem_element.append(event_element)
													event_element.text = acquis.find('Event').text
													if version == "ead2002":
														date_element = ET.Element('date')
														chronitem_element.append(date_element)
														date_element.text = acquis.find('Date').text
														date_element.set('normal', acquis.find('DateNormal').text)
													else:
														from date import basic_date
														chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
												else:
													# if there is already an <acquis> element
													chronitem_element = ET.Element('chronitem')
													match.find('acqinfo').append(chronitem_element)
													event_element = ET.Element('event')
													chronitem_element.append(event_element)
													event_element.text = acquis.find('Event').text
													if version == "ead2002":
														date_element = ET.Element('date')
														chronitem_element.append(date_element)
														date_element.text = acquis.find('Date').text
														date_element.set('normal', acquis.find('DateNormal').text)
													else:
														from date import basic_date
														chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
							else:
								# <unitid> within <did> of <c> or no series:
								for match in arch_root.find('dsc').iter('c'):
									if match.find('did/unitid') is None:
										pass
									else:
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + acquis.find('UnitID').text:
												if match.find(tag_name) is None:
													# if there is no <aquis> element
													acquis_element = ET.Element(tag_name)
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, acquis_element)
													chronlist_element = ET.Element('chronlist')
													acquis_element.append(chronlist_element)
													chronitem_element = ET.Element('chronitem')
													chronlist_element.append(chronitem_element)
													event_element = ET.Element('event')
													chronitem_element.append(event_element)
													event_element.text = acquis.find('Event').text
													if version == "ead2002":
														date_element = ET.Element('date')
														chronitem_element.append(date_element)
														date_element.text = acquis.find('Date').text
														date_element.set('normal', acquis.find('DateNormal').text)
													else:
														from date import basic_date
														chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
												else:
													# if there is already an <acquis> element
													chronitem_element = ET.Element('chronitem')
													match.find('acqinfo').append(chronitem_element)
													event_element = ET.Element('event')
													chronitem_element.append(event_element)
													event_element.text = acquis.find('Event').text
													if version == "ead2002":
														date_element = ET.Element('date')
														chronitem_element.append(date_element)
														date_element.text = acquis.find('Date').text
														date_element.set('normal', acquis.find('DateNormal').text)
													else:
														from date import basic_date
														chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
												
												
def controlaccess_lower(arch_root, input_element, version, tag_name, collectionID, series_separator):
	if arch_root.find('dsc/c01') is None and arch_root.find('dsc/c') is None:
		pass
	else:
		if arch_root.find('dsc/c01') is None:
			if arch_root.find('dsc/c') is None:
				pass
			else:
				c_numbers = False
				if "id" in arch_root.find('dsc/c').attrib:
					attribute_id = True
				else:
					attribute_id = False
		else:
			c_numbers = True
			if "id" in arch_root.find('dsc/c01').attrib:
				attribute_id = True
			else:
				attribute_id = False
		for heading in input_element:
			if heading.find('UnitID').text:
				if heading.find('Part').text:
					if heading.find('ElementName').text:
						if attribute_id == True:
							if c_numbers == True:
								# @id in <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.attrib['id'] == collectionID + heading.find('UnitID').text:
											if match.find(tag_name) is None:
												# if there is no <controlaccess> element
												controlaccess_element = ET.Element('controlaccess')
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, controlaccess_element)
												new_element = ET.Element(heading.find('ElementName').text)
												controlaccess_element.append(new_element)
												part_element = ET.Element('part')
												new_element.append(part_element)
												part_element.text = heading.find('Part').text
												if heading.find('MARCEncoding').text:
													new_element.set('encodinganalog', heading.find('MARCEncoding').text)
												if heading.find('Identifier').text:
													if version == "ead3":
														new_element.set('identifier', heading.find('Identifier').text)
													else:
														new_element.set('id', heading.find('Identifier').text)
												if heading.find('Relator').text:
													if version == "ead3":
														new_element.set('relator', heading.find('Relator').text)
													else:
														new_element.set('role', heading.find('Relator').text)
												if heading.find('Normal').text:
													new_element.set('normal', heading.find('Normal').text)
												if heading.find('Source').text:
													new_element.set('source', heading.find('Source').text)
											else:
												# if there is already an <controlaccess> element
												new_element = ET.Element(heading.find('ElementName').text)
												match.find('controlaccess').append(new_element)
												part_element = ET.Element('part')
												new_element.append(part_element)
												part_element.text = heading.find('Part').text
												if heading.find('MARCEncoding').text:
													new_element.set('encodinganalog', heading.find('MARCEncoding').text)
												if heading.find('Identifier').text:
													if version == "ead3":
														new_element.set('identifier', heading.find('Identifier').text)
													else:
														new_element.set('id', heading.find('Identifier').text)
												if heading.find('Relator').text:
													if version == "ead3":
														new_element.set('relator', heading.find('Relator').text)
													else:
														new_element.set('role', heading.find('Relator').text)
												if heading.find('Normal').text:
													new_element.set('normal', heading.find('Normal').text)
												if heading.find('Source').text:
													new_element.set('source', heading.find('Source').text)
							else:
								# @id in <c>:
								for match in arch_root.find('dsc').iter('c'):
									if match.attrib['id'] == collectionID + heading.find('UnitID').text:
										if match.find(tag_name) is None:
											# if there is no <controlaccess> element
											controlaccess_element = ET.Element('controlaccess')
											append_index = match.getchildren().index(match.find('did')) + 1
											match.insert(append_index, controlaccess_element)
											new_element = ET.Element(heading.find('ElementName').text)
											controlaccess_element.append(new_element)
											part_element = ET.Element('part')
											new_element.append(part_element)
											part_element.text = heading.find('Part').text
											if heading.find('MARCEncoding').text:
												new_element.set('encodinganalog', heading.find('MARCEncoding').text)
											if heading.find('Identifier').text:
												if version == "ead3":
													new_element.set('identifier', heading.find('Identifier').text)
												else:
													new_element.set('id', heading.find('Identifier').text)
											if heading.find('Relator').text:
												if version == "ead3":
													new_element.set('relator', heading.find('Relator').text)
												else:
													new_element.set('role', heading.find('Relator').text)
											if heading.find('Normal').text:
												new_element.set('normal', heading.find('Normal').text)
											if heading.find('Source').text:
												new_element.set('source', heading.find('Source').text)
										else:
											# if there is already an <controlaccess> element
											new_element = ET.Element(heading.find('ElementName').text)
											match.find('controlaccess').append(new_element)
											part_element = ET.Element('part')
											new_element.append(part_element)
											part_element.text = heading.find('Part').text
											if heading.find('MARCEncoding').text:
												new_element.set('encodinganalog', heading.find('MARCEncoding').text)
											if heading.find('Identifier').text:
												if version == "ead3":
													new_element.set('identifier', heading.find('Identifier').text)
												else:
													new_element.set('id', heading.find('Identifier').text)
											if heading.find('Relator').text:
												if version == "ead3":
													new_element.set('relator', heading.find('Relator').text)
												else:
													new_element.set('role', heading.find('Relator').text)
											if heading.find('Normal').text:
												new_element.set('normal', heading.find('Normal').text)
											if heading.find('Source').text:
												new_element.set('source', heading.find('Source').text)
						else:
							if c_numbers == True:
								# <unitid> within <did> of <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + heading.find('UnitID').text:
												if match.find(tag_name) is None:
													# if there is no <controlaccess> element
													controlaccess_element = ET.Element('controlaccess')
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, controlaccess_element)
													new_element = ET.Element(heading.find('ElementName').text)
													controlaccess_element.append(new_element)
													part_element = ET.Element('part')
													new_element.append(part_element)
													part_element.text = heading.find('Part').text
													if heading.find('MARCEncoding').text:
														new_element.set('encodinganalog', heading.find('MARCEncoding').text)
													if heading.find('Identifier').text:
														if version == "ead3":
															new_element.set('identifier', heading.find('Identifier').text)
														else:
															new_element.set('id', heading.find('Identifier').text)
													if heading.find('Relator').text:
														if version == "ead3":
															new_element.set('relator', heading.find('Relator').text)
														else:
															new_element.set('role', heading.find('Relator').text)
													if heading.find('Normal').text:
														new_element.set('normal', heading.find('Normal').text)
													if heading.find('Source').text:
														new_element.set('source', heading.find('Source').text)
												else:
													# if there is already an <controlaccess> element
													new_element = ET.Element(heading.find('ElementName').text)
													match.find('controlaccess').append(new_element)
													part_element = ET.Element('part')
													new_element.append(part_element)
													part_element.text = heading.find('Part').text
													if heading.find('MARCEncoding').text:
														new_element.set('encodinganalog', heading.find('MARCEncoding').text)
													if heading.find('Identifier').text:
														if version == "ead3":
															new_element.set('identifier', heading.find('Identifier').text)
														else:
															new_element.set('id', heading.find('Identifier').text)
													if heading.find('Relator').text:
														if version == "ead3":
															new_element.set('relator', heading.find('Relator').text)
														else:
															new_element.set('role', heading.find('Relator').text)
													if heading.find('Normal').text:
														new_element.set('normal', heading.find('Normal').text)
													if heading.find('Source').text:
														new_element.set('source', heading.find('Source').text)			
							else:
								# <unitid> within <did> of <c>:
								for match in arch_root.find('dsc').iter('c'):
									if match.find('did/unitid') is None:
										pass
									else:
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + heading.find('UnitID').text:
												if match.find(tag_name) is None:
													# if there is no <controlaccess> element
													controlaccess_element = ET.Element('controlaccess')
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, controlaccess_element)
													new_element = ET.Element(heading.find('ElementName').text)
													controlaccess_element.append(new_element)
													part_element = ET.Element('part')
													new_element.append(part_element)
													part_element.text = heading.find('Part').text
													if heading.find('MARCEncoding').text:
														new_element.set('encodinganalog', heading.find('MARCEncoding').text)
													if heading.find('Identifier').text:
														if version == "ead3":
															new_element.set('identifier', heading.find('Identifier').text)
														else:
															new_element.set('id', heading.find('Identifier').text)
													if heading.find('Relator').text:
														if version == "ead3":
															new_element.set('relator', heading.find('Relator').text)
														else:
															new_element.set('role', heading.find('Relator').text)
													if heading.find('Normal').text:
														new_element.set('normal', heading.find('Normal').text)
													if heading.find('Source').text:
														new_element.set('source', heading.find('Source').text)
												else:
													# if there is already an <controlaccess> element
													new_element = ET.Element(heading.find('ElementName').text)
													match.find('controlaccess').append(new_element)
													part_element = ET.Element('part')
													new_element.append(part_element)
													part_element.text = heading.find('Part').text
													if heading.find('MARCEncoding').text:
														new_element.set('encodinganalog', heading.find('MARCEncoding').text)
													if heading.find('Identifier').text:
														if version == "ead3":
															new_element.set('identifier', heading.find('Identifier').text)
														else:
															new_element.set('id', heading.find('Identifier').text)
													if heading.find('Relator').text:
														if version == "ead3":
															new_element.set('relator', heading.find('Relator').text)
														else:
															new_element.set('role', heading.find('Relator').text)
													if heading.find('Normal').text:
														new_element.set('normal', heading.find('Normal').text)
													if heading.find('Source').text:
														new_element.set('source', heading.find('Source').text)						
					else:
						#Error message for no element name
						from messages import error
						error("Controlled Access Heading," + heading.find('Part').text + " does not have an Element Name. It will not be encoded.", False)


		
def relatedmaterial_lower(arch_root, pub_element, man_element, version, tag_name, collectionID, series_separator):
	if arch_root.find('dsc/c01') is None and arch_root.find('dsc/c') is None:
		pass
	else:
		if arch_root.find('dsc/c01') is None:
			if arch_root.find('dsc/c') is None:
				pass
			else:
				c_numbers = False
				if "id" in arch_root.find('dsc/c').attrib:
					attribute_id = True
				else:
					attribute_id = False
		else:
			c_numbers = True
			if "id" in arch_root.find('dsc/c01').attrib:
				attribute_id = True
			else:
				attribute_id = False
		if pub_element is None:
			pass
		else:
			for publication in pub_element:
				if publication.find('UnitID') is None:
					pass
				else:
					if publication.find('UnitID').text:
						if attribute_id == True:
							if c_numbers == True:
								# @id in <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.attrib['id'] == collectionID + publication.find('UnitID').text:
											if match.find(tag_name) is None:
												# if there is no <relatedmaterial> element
												relatedmaterial_element = ET.Element('relatedmaterial')
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, relatedmaterial_element)
												bibref_element = ET.Element('bibref')
												relatedmaterial_element.append(bibref_element)
												if publication.find('Author').text:
													bibref_element.text = publication.find('Author').text + ", "
												if publication.find('Title').text:
													title_element = ET.Element('title')
													bibref_element.append(title_element)
													title_element.text = publication.find('Title').text
												if publication.find('Citation').text:
													title_element.tail = " " + publication.find('Citation').text + ", "
												if publication.find('Date').text:
													date_element = ET.Element('date')
													bibref_element.append(date_element)
													date_element.text = publication.find('Date').text
													if publication.find('NormalDate').text:
														date_element.set("normal", publication.find('NormalDate').text)
												if publication.find('Reference').text:
													ref_element = ET.Element('ref')
													bibref_element.append(ref_element)
													ref_element.text = publication.find('Reference').text
													if publication.find('ReferenceLink').text:
														ref_element.set('ref', publication.find('ReferenceLink').text)
											else:
												# if there is already an <relatedmaterial> element
												bibref_element = ET.Element('bibref')
												march.find('relatedmaterial').append(bibref_element)
												if publication.find('Author').text:
													bibref_element.text = publication.find('Author').text + ", "
												if publication.find('Title').text:
													title_element = ET.Element('title')
													bibref_element.append(title_element)
													title_element.text = publication.find('Title').text
												if publication.find('Citation').text:
													title_element.tail = " " + publication.find('Citation').text + ", "
												if publication.find('Date').text:
													date_element = ET.Element('date')
													bibref_element.append(date_element)
													date_element.text = publication.find('Date').text
													if publication.find('NormalDate').text:
														date_element.set("normal", publication.find('NormalDate').text)
												if publication.find('Reference').text:
													ref_element = ET.Element('ref')
													bibref_element.append(ref_element)
													ref_element.text = publication.find('Reference').text
													if publication.find('ReferenceLink').text:
														ref_element.set('ref', publication.find('ReferenceLink').text)
							else:
								# @id in <c>:
								for match in arch_root.find('dsc').iter('c'):
									if match.attrib['id'] == collectionID + publication.find('UnitID').text:
										if match.find(tag_name) is None:
											# if there is no <relatedmaterial> element
											relatedmaterial_element = ET.Element('relatedmaterial')
											append_index = match.getchildren().index(match.find('did')) + 1
											match.insert(append_index, relatedmaterial_element)
											bibref_element = ET.Element('bibref')
											relatedmaterial_element.append(bibref_element)
											if publication.find('Author').text:
												bibref_element.text = publication.find('Author').text + ", "
											if publication.find('Title').text:
												title_element = ET.Element('title')
												bibref_element.append(title_element)
												title_element.text = publication.find('Title').text
											if publication.find('Citation').text:
												title_element.tail = " " + publication.find('Citation').text + ", "
											if publication.find('Date').text:
												date_element = ET.Element('date')
												bibref_element.append(date_element)
												date_element.text = publication.find('Date').text
												if publication.find('NormalDate').text:
													date_element.set("normal", publication.find('NormalDate').text)
											if publication.find('Reference').text:
												ref_element = ET.Element('ref')
												bibref_element.append(ref_element)
												ref_element.text = publication.find('Reference').text
												if publication.find('ReferenceLink').text:
													ref_element.set('ref', publication.find('ReferenceLink').text)
										else:
											# if there is already an <relatedmaterial> element
											bibref_element = ET.Element('bibref')
											march.find('relatedmaterial').append(bibref_element)
											if publication.find('Author').text:
												bibref_element.text = publication.find('Author').text + ", "
											if publication.find('Title').text:
												title_element = ET.Element('title')
												bibref_element.append(title_element)
												title_element.text = publication.find('Title').text
											if publication.find('Citation').text:
												title_element.tail = " " + publication.find('Citation').text + ", "
											if publication.find('Date').text:
												date_element = ET.Element('date')
												bibref_element.append(date_element)
												date_element.text = publication.find('Date').text
												if publication.find('NormalDate').text:
													date_element.set("normal", publication.find('NormalDate').text)
											if publication.find('Reference').text:
												ref_element = ET.Element('ref')
												bibref_element.append(ref_element)
												ref_element.text = publication.find('Reference').text
												if publication.find('ReferenceLink').text:
													ref_element.set('ref', publication.find('ReferenceLink').text)
						else:
							if c_numbers == True:
								# <unitid> within <did> of <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.find('did/unitid') is None:
											pass
										else:
											if match.find('did/unitid').text:
												if match.find('did/unitid').text == collectionID + publication.find('UnitID').text:
													if match.find(tag_name) is None:
														# if there is no <relatedmaterial> element
														relatedmaterial_element = ET.Element('relatedmaterial')
														append_index = match.getchildren().index(match.find('did')) + 1
														match.insert(append_index, relatedmaterial_element)
														bibref_element = ET.Element('bibref')
														relatedmaterial_element.append(bibref_element)
														if publication.find('Author').text:
															bibref_element.text = publication.find('Author').text + ", "
														if publication.find('Title').text:
															title_element = ET.Element('title')
															bibref_element.append(title_element)
															title_element.text = publication.find('Title').text
														if publication.find('Citation').text:
															title_element.tail = " " + publication.find('Citation').text + ", "
														if publication.find('Date').text:
															date_element = ET.Element('date')
															bibref_element.append(date_element)
															date_element.text = publication.find('Date').text
															if publication.find('NormalDate').text:
																date_element.set("normal", publication.find('NormalDate').text)
														if publication.find('Reference').text:
															ref_element = ET.Element('ref')
															bibref_element.append(ref_element)
															ref_element.text = publication.find('Reference').text
															if publication.find('ReferenceLink').text:
																ref_element.set('ref', publication.find('ReferenceLink').text)
													else:
														# if there is already an <relatedmaterial> element
														bibref_element = ET.Element('bibref')
														march.find('relatedmaterial').append(bibref_element)
														if publication.find('Author').text:
															bibref_element.text = publication.find('Author').text + ", "
														if publication.find('Title').text:
															title_element = ET.Element('title')
															bibref_element.append(title_element)
															title_element.text = publication.find('Title').text
														if publication.find('Citation').text:
															title_element.tail = " " + publication.find('Citation').text + ", "
														if publication.find('Date').text:
															date_element = ET.Element('date')
															bibref_element.append(date_element)
															date_element.text = publication.find('Date').text
															if publication.find('NormalDate').text:
																date_element.set("normal", publication.find('NormalDate').text)
														if publication.find('Reference').text:
															ref_element = ET.Element('ref')
															bibref_element.append(ref_element)
															ref_element.text = publication.find('Reference').text
															if publication.find('ReferenceLink').text:
																ref_element.set('ref', publication.find('ReferenceLink').text)
							else:
								# <unitid> within <did> of <c>:
								for match in arch_root.find('dsc').iter('c'):
									if match.find('did/unitid') is None:
										pass
									else:
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + publication.find('UnitID').text:
												print "test9"
												if match.find(tag_name) is None:
													print "test10"
													# if there is no <relatedmaterial> element
													relatedmaterial_element = ET.Element('relatedmaterial')
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, relatedmaterial_element)
													bibref_element = ET.Element('bibref')
													relatedmaterial_element.append(bibref_element)
													if publication.find('Author').text:
														bibref_element.text = publication.find('Author').text + ", "
													if publication.find('Title').text:
														title_element = ET.Element('title')
														bibref_element.append(title_element)
														title_element.text = publication.find('Title').text
													if publication.find('Citation').text:
														title_element.tail = " " + publication.find('Citation').text + ", "
													if publication.find('Date').text:
														date_element = ET.Element('date')
														bibref_element.append(date_element)
														date_element.text = publication.find('Date').text
														if publication.find('NormalDate').text:
															date_element.set("normal", publication.find('NormalDate').text)
													if publication.find('Reference').text:
														ref_element = ET.Element('ref')
														bibref_element.append(ref_element)
														ref_element.text = publication.find('Reference').text
														if publication.find('ReferenceLink').text:
															ref_element.set('ref', publication.find('ReferenceLink').text)
												else:
													# if there is already an <relatedmaterial> element
													bibref_element = ET.Element('bibref')
													march.find('relatedmaterial').append(bibref_element)
													if publication.find('Author').text:
														bibref_element.text = publication.find('Author').text + ", "
													if publication.find('Title').text:
														title_element = ET.Element('title')
														bibref_element.append(title_element)
														title_element.text = publication.find('Title').text
													if publication.find('Citation').text:
														title_element.tail = " " + publication.find('Citation').text + ", "
													if publication.find('Date').text:
														date_element = ET.Element('date')
														bibref_element.append(date_element)
														date_element.text = publication.find('Date').text
														if publication.find('NormalDate').text:
															date_element.set("normal", publication.find('NormalDate').text)
													if publication.find('Reference').text:
														ref_element = ET.Element('ref')
														bibref_element.append(ref_element)
														ref_element.text = publication.find('Reference').text
														if publication.find('ReferenceLink').text:
															ref_element.set('ref', publication.find('ReferenceLink').text)
		if man_element is None:
			pass
		else:
			for manuscript in man_element:
				if manuscript.find('UnitID') is None:
					pass
				else:
					if manuscript.find('UnitID').text:
						if attribute_id == True:
							if c_numbers == True:
								# @id in <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.attrib['id'] == collectionID + manuscript.find('UnitID').text:
											if match.find(tag_name) is None:
												# if there is no <relatedmaterial> element
												relatedmaterial_element = ET.Element('relatedmaterial')
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, relatedmaterial_element)
												archref_element = ET.Element('archref')
												relatedmaterial_element.append(archref_element)
												if manuscript.find('Collection').text:
													archref_element.text = manuscript.find('Collection').text + ", "
												if manuscript.find('UnitTitle').text:
													title_element = ET.Element('title')
													archref_element.append(title_element)
													title_element.text = manuscript.find('UnitTitle').text
												if manuscript.find('UnitID').text:
													title_element.tail = " " + manuscript.find('UnitID').text + ", "
												if manuscript.find('Date').text:
													date_element = ET.Element('date')
													archref_element.append(date_element)
													date_element.text = manuscript.find('Date').text
													if manuscript.find('NormalDate').text:
														date_element.set("normal", manuscript.find('NormalDate').text)
												if manuscript.find('Reference').text:
													ref_element = ET.Element('ref')
													archref_element.append(ref_element)
													ref_element.text = manuscript.find('Reference').text
													if manuscript.find('ReferenceLink').text:
														ref_element.set('ref', manuscript.find('ReferenceLink').text)
											else:
												# if there is already an <relatedmaterial> element
												archref_element = ET.Element('archref')
												match.find('relatedmaterial').append(archref_element)
												if manuscript.find('Collection').text:
													archref_element.text = manuscript.find('Collection').text + ", "
												if manuscript.find('UnitTitle').text:
													title_element = ET.Element('title')
													archref_element.append(title_element)
													title_element.text = manuscript.find('UnitTitle').text
												if manuscript.find('UnitID').text:
													title_element.tail = " " + manuscript.find('UnitID').text + ", "
												if manuscript.find('Date').text:
													date_element = ET.Element('date')
													archref_element.append(date_element)
													date_element.text = manuscript.find('Date').text
													if manuscript.find('NormalDate').text:
														date_element.set("normal", manuscript.find('NormalDate').text)
												if manuscript.find('Reference').text:
													ref_element = ET.Element('ref')
													archref_element.append(ref_element)
													ref_element.text = manuscript.find('Reference').text
													if manuscript.find('ReferenceLink').text:
														ref_element.set('ref', manuscript.find('ReferenceLink').text)
							else:
								# @id in <c>:
								for match in arch_root.find('dsc').iter('c'):
									if "id" in match.attrib:
										if match.attrib['id'] == collectionID + manuscript.find('UnitID').text:
											if match.find(tag_name) is None:
												# if there is no <relatedmaterial> element
												relatedmaterial_element = ET.Element('relatedmaterial')
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, relatedmaterial_element)
												archref_element = ET.Element('archref')
												relatedmaterial_element.append(archref_element)
												if manuscript.find('Collection').text:
													archref_element.text = manuscript.find('Collection').text + ", "
												if manuscript.find('UnitTitle').text:
													title_element = ET.Element('title')
													archref_element.append(title_element)
													title_element.text = manuscript.find('UnitTitle').text
												if manuscript.find('UnitID').text:
													title_element.tail = " " + manuscript.find('UnitID').text + ", "
												if manuscript.find('Date').text:
													date_element = ET.Element('date')
													archref_element.append(date_element)
													date_element.text = manuscript.find('Date').text
													if manuscript.find('NormalDate').text:
														date_element.set("normal", manuscript.find('NormalDate').text)
												if manuscript.find('Reference').text:
													ref_element = ET.Element('ref')
													archref_element.append(ref_element)
													ref_element.text = manuscript.find('Reference').text
													if manuscript.find('ReferenceLink').text:
														ref_element.set('ref', manuscript.find('ReferenceLink').text)
											else:
												# if there is already an <relatedmaterial> element
												archref_element = ET.Element('archref')
												match.find('relatedmaterial').append(archref_element)
												if manuscript.find('Collection').text:
													archref_element.text = manuscript.find('Collection').text + ", "
												if manuscript.find('UnitTitle').text:
													title_element = ET.Element('title')
													archref_element.append(title_element)
													title_element.text = manuscript.find('UnitTitle').text
												if manuscript.find('UnitID').text:
													title_element.tail = " " + manuscript.find('UnitID').text + ", "
												if manuscript.find('Date').text:
													date_element = ET.Element('date')
													archref_element.append(date_element)
													date_element.text = manuscript.find('Date').text
													if manuscript.find('NormalDate').text:
														date_element.set("normal", manuscript.find('NormalDate').text)
												if manuscript.find('Reference').text:
													ref_element = ET.Element('ref')
													archref_element.append(ref_element)
													ref_element.text = manuscript.find('Reference').text
													if manuscript.find('ReferenceLink').text:
														ref_element.set('ref', manuscript.find('ReferenceLink').text)
						else:
							if c_numbers == True:
								# <unitid> within <did> of <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + manuscript.find('UnitID').text:
												if match.find(tag_name) is None:
													# if there is no <relatedmaterial> element
													relatedmaterial_element = ET.Element('relatedmaterial')
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, relatedmaterial_element)
													archref_element = ET.Element('archref')
													relatedmaterial_element.append(archref_element)
													if manuscript.find('Collection').text:
														archref_element.text = manuscript.find('Collection').text + ", "
													if manuscript.find('UnitTitle').text:
														title_element = ET.Element('title')
														archref_element.append(title_element)
														title_element.text = manuscript.find('UnitTitle').text
													if manuscript.find('UnitID').text:
														title_element.tail = " " + manuscript.find('UnitID').text + ", "
													if manuscript.find('Date').text:
														date_element = ET.Element('date')
														archref_element.append(date_element)
														date_element.text = manuscript.find('Date').text
														if manuscript.find('NormalDate').text:
															date_element.set("normal", manuscript.find('NormalDate').text)
													if manuscript.find('Reference').text:
														ref_element = ET.Element('ref')
														archref_element.append(ref_element)
														ref_element.text = manuscript.find('Reference').text
														if manuscript.find('ReferenceLink').text:
															ref_element.set('ref', manuscript.find('ReferenceLink').text)
												else:
													# if there is already an <relatedmaterial> element
													archref_element = ET.Element('archref')
													match.find('relatedmaterial').append(archref_element)
													if manuscript.find('Collection').text:
														archref_element.text = manuscript.find('Collection').text + ", "
													if manuscript.find('UnitTitle').text:
														title_element = ET.Element('title')
														archref_element.append(title_element)
														title_element.text = manuscript.find('UnitTitle').text
													if manuscript.find('UnitID').text:
														title_element.tail = " " + manuscript.find('UnitID').text + ", "
													if manuscript.find('Date').text:
														date_element = ET.Element('date')
														archref_element.append(date_element)
														date_element.text = manuscript.find('Date').text
														if manuscript.find('NormalDate').text:
															date_element.set("normal", manuscript.find('NormalDate').text)
													if manuscript.find('Reference').text:
														ref_element = ET.Element('ref')
														archref_element.append(ref_element)
														ref_element.text = manuscript.find('Reference').text
														if manuscript.find('ReferenceLink').text:
															ref_element.set('ref', manuscript.find('ReferenceLink').text)
							else:
								# <unitid> within <did> of <c>:
								for match in arch_root.find('dsc').iter('c'):
									if match.find('did/unitid') is None:
										pass
									else:
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + manuscript.find('UnitID').text:
												if match.find(tag_name) is None:
													# if there is no <relatedmaterial> element
													relatedmaterial_element = ET.Element('relatedmaterial')
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, relatedmaterial_element)
													archref_element = ET.Element('archref')
													relatedmaterial_element.append(archref_element)
													if manuscript.find('Collection').text:
														archref_element.text = manuscript.find('Collection').text + ", "
													if manuscript.find('UnitTitle').text:
														title_element = ET.Element('title')
														archref_element.append(title_element)
														title_element.text = manuscript.find('UnitTitle').text
													if manuscript.find('UnitID').text:
														title_element.tail = " " + manuscript.find('UnitID').text + ", "
													if manuscript.find('Date').text:
														date_element = ET.Element('date')
														archref_element.append(date_element)
														date_element.text = manuscript.find('Date').text
														if manuscript.find('NormalDate').text:
															date_element.set("normal", manuscript.find('NormalDate').text)
													if manuscript.find('Reference').text:
														ref_element = ET.Element('ref')
														archref_element.append(ref_element)
														ref_element.text = manuscript.find('Reference').text
														if manuscript.find('ReferenceLink').text:
															ref_element.set('ref', manuscript.find('ReferenceLink').text)
												else:
													# if there is already an <relatedmaterial> element
													archref_element = ET.Element('archref')
													match.find('relatedmaterial').append(archref_element)
													if manuscript.find('Collection').text:
														archref_element.text = manuscript.find('Collection').text + ", "
													if manuscript.find('UnitTitle').text:
														title_element = ET.Element('title')
														archref_element.append(title_element)
														title_element.text = manuscript.find('UnitTitle').text
													if manuscript.find('UnitID').text:
														title_element.tail = " " + manuscript.find('UnitID').text + ", "
													if manuscript.find('Date').text:
														date_element = ET.Element('date')
														archref_element.append(date_element)
														date_element.text = manuscript.find('Date').text
														if manuscript.find('NormalDate').text:
															date_element.set("normal", manuscript.find('NormalDate').text)
													if manuscript.find('Reference').text:
														ref_element = ET.Element('ref')
														archref_element.append(ref_element)
														ref_element.text = manuscript.find('Reference').text
														if manuscript.find('ReferenceLink').text:
															ref_element.set('ref', manuscript.find('ReferenceLink').text)


