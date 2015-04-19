# module Relations in EAD3 <relations>
import xml.etree.cElementTree as ET

def relations(arch_root, Relations_Sheet):
	old_relation = arch_root.find('relations/relation')
	if arch_root.find('relations') is None:
		pass
	else:
		arch_root.find('relations').clear()
	for relation in Relations_Sheet:
		if relation.find('RelationEntry').text:
			if relation.find('UnitID').text:
				pass # for relations at lower levels
			else:
				relations_parent = arch_root
				if relations_parent.find('relations') is None:
					if "add_relation" in globals.new_elements or "add-all" in globals.add_all:
						relations_element = ET.Element('relations')
						relations_index = relations_parent.getchildren().index(relations_parent.find('dsc'))
						relations_parent.insert(relations_index, relations_element)
				else:
					relations_parent.find('relations').clear()
					relations_element = relations_parent.find('relations')
				relation_element = ET.Element('relation')
				if old_relation is None:
					pass
				else:
					relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
					relation_element.attrib['show'] =old_relation.attrib['show']
				relations_parent.find('relations').append(relation_element)
				if 	relation.find('RelationID').text:
					relation_element.set('id', relation.find('RelationID').text)
				if relation.find('RelationType').text:
					relation_element.set('relationtype', relation.find('RelationType').text)
				if relation.find('RelationLink').text:
					relation_element.set('href', relation.find('RelationLink').text)
				if relation.find('RelationEntry').text:
					entry_element = ET.Element('relationentry')
					relation_element.append(entry_element)
					entry_element.text = relation.find('RelationEntry').text
				if relation.find('RelationDate').text:
					from date import basic_date				
					relation_element.append(basic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
				if relation.find('RelationPlace').text:
					geogname_element = ET.Element('geogname')
					relation_element.append(geogname_element)
					geogname_element.text = relation.find('RelationPlace').text
				if relation.find('RelationNote').text:
					descriptivenote_element = ET.Element('descriptivenote')
					relation_element.append(descriptivenote_element)
					p_element = ET.Element('p')
					descriptivenote_element.append(p_element)
					p_element.text = relation.find('RelationNote').text
		
		
			
def relations_lower(arch_root, input_element, version, tag_name, collectionID, series_separator):
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
		old_relation = arch_root.find('relations/relation')
		for relation in input_element:
			if relation.find('UnitID').text:
				if relation.find('RelationEntry').text:
					if attribute_id == True:
						if c_numbers == True:
							# @id in <c01>, <c02>, etc.:
							for match in arch_root.find('dsc').iter():
								if match.tag.startswith('c0') or match.tag.startswith('c1'):
									if match.attrib['id'] == collectionID + relation.find('UnitID').text:
										if match.find(tag_name) is None:
											# if there is no <relations> element
											relations_element = ET.Element('relations')
											append_index = match.getchildren().index(match.find('did')) + 1
											match.insert(append_index, relations_element)
											relation_element = ET.Element('relation')
											relations_element.append(relation_element)
											if old_relation is None:
												pass
											else:
												relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
												relation_element.attrib['show'] =old_relation.attrib['show']
											if 	relation.find('RelationID').text:
												relation_element.set('id', relation.find('RelationID').text)
											if relation.find('RelationType').text:
												relation_element.set('relationtype', relation.find('RelationType').text)
											if relation.find('RelationLink').text:
												relation_element.set('href', relation.find('RelationLink').text)
											if relation.find('RelationEntry').text:
												entry_element = ET.Element('relationentry')
												relation_element.append(entry_element)
												entry_element.text = relation.find('RelationEntry').text
											if relation.find('RelationDate').text:
												from date import magic_date				
												relation_element.append(magic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
											if relation.find('RelationPlace').text:
												geogname_element = ET.Element('geogname')
												relation_element.append(geogname_element)
												geogname_element.text = relation.find('RelationPlace').text
											if relation.find('RelationNote').text:
												descriptivenote_element = ET.Element('descriptivenote')
												relation_element.append(descriptivenote_element)
												p_element = ET.Element('p')
												descriptivenote_element.append(p_element)
												p_element.text = relation.find('RelationNote').text
										else:
											# if there is already an <controlaccess> element
											relation_element = ET.Element('relation')
											match.find('relations').append(relation_element)
											if old_relation is None:
												pass
											else:
												relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
												relation_element.attrib['show'] =old_relation.attrib['show']
											if 	relation.find('RelationID').text:
												relation_element.set('id', relation.find('RelationID').text)
											if relation.find('RelationType').text:
												relation_element.set('relationtype', relation.find('RelationType').text)
											if relation.find('RelationLink').text:
												relation_element.set('href', relation.find('RelationLink').text)
											if relation.find('RelationEntry').text:
												entry_element = ET.Element('relationentry')
												relation_element.append(entry_element)
												entry_element.text = relation.find('RelationEntry').text
											if relation.find('RelationDate').text:
												from date import magic_date				
												relation_element.append(magic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
											if relation.find('RelationPlace').text:
												geogname_element = ET.Element('geogname')
												relation_element.append(geogname_element)
												geogname_element.text = relation.find('RelationPlace').text
											if relation.find('RelationNote').text:
												descriptivenote_element = ET.Element('descriptivenote')
												relation_element.append(descriptivenote_element)
												p_element = ET.Element('p')
												descriptivenote_element.append(p_element)
												p_element.text = relation.find('RelationNote').text				
						else:
							# @id in <c>:
							for match in arch_root.find('dsc').iter('c'):
								if match.attrib['id'] == collectionID + relation.find('UnitID').text:
									if match.find(tag_name) is None:
										# if there is no <relations> element
										relations_element = ET.Element('relations')
										append_index = match.getchildren().index(match.find('did')) + 1
										match.insert(append_index, relations_element)
										relation_element = ET.Element('relation')
										relations_element.append(relation_element)
										if old_relation is None:
											pass
										else:
											relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
											relation_element.attrib['show'] =old_relation.attrib['show']
										if 	relation.find('RelationID').text:
											relation_element.set('id', relation.find('RelationID').text)
										if relation.find('RelationType').text:
											relation_element.set('relationtype', relation.find('RelationType').text)
										if relation.find('RelationLink').text:
											relation_element.set('href', relation.find('RelationLink').text)
										if relation.find('RelationEntry').text:
											entry_element = ET.Element('relationentry')
											relation_element.append(entry_element)
											entry_element.text = relation.find('RelationEntry').text
										if relation.find('RelationDate').text:
											from date import magic_date				
											relation_element.append(magic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
										if relation.find('RelationPlace').text:
											geogname_element = ET.Element('geogname')
											relation_element.append(geogname_element)
											geogname_element.text = relation.find('RelationPlace').text
										if relation.find('RelationNote').text:
											descriptivenote_element = ET.Element('descriptivenote')
											relation_element.append(descriptivenote_element)
											p_element = ET.Element('p')
											descriptivenote_element.append(p_element)
											p_element.text = relation.find('RelationNote').text
									else:
										# if there is already an <controlaccess> element
										relation_element = ET.Element('relation')
										match.find('relations').append(relation_element)
										if old_relation is None:
											pass
										else:
											relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
											relation_element.attrib['show'] =old_relation.attrib['show']
										if 	relation.find('RelationID').text:
											relation_element.set('id', relation.find('RelationID').text)
										if relation.find('RelationType').text:
											relation_element.set('relationtype', relation.find('RelationType').text)
										if relation.find('RelationLink').text:
											relation_element.set('href', relation.find('RelationLink').text)
										if relation.find('RelationEntry').text:
											entry_element = ET.Element('relationentry')
											relation_element.append(entry_element)
											entry_element.text = relation.find('RelationEntry').text
										if relation.find('RelationDate').text:
											from date import magic_date				
											relation_element.append(magic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
										if relation.find('RelationPlace').text:
											geogname_element = ET.Element('geogname')
											relation_element.append(geogname_element)
											geogname_element.text = relation.find('RelationPlace').text
										if relation.find('RelationNote').text:
											descriptivenote_element = ET.Element('descriptivenote')
											relation_element.append(descriptivenote_element)
											p_element = ET.Element('p')
											descriptivenote_element.append(p_element)
											p_element.text = relation.find('RelationNote').text	
					else:
						if c_numbers == True:
							# <unitid> within <did> of <c01>, <c02>, etc.:
							for match in arch_root.find('dsc').iter():
								if match.tag.startswith('c0') or match.tag.startswith('c1'):
									if match.find('did/unitid').text:
										if match.find('did/unitid').text == collectionID + relation.find('UnitID').text:
											if match.find(tag_name) is None:
												# if there is no <relations> element
												relations_element = ET.Element('relations')
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, relations_element)
												relation_element = ET.Element('relation')
												relations_element.append(relation_element)
												if old_relation is None:
													pass
												else:
													relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
													relation_element.attrib['show'] =old_relation.attrib['show']
												if 	relation.find('RelationID').text:
													relation_element.set('id', relation.find('RelationID').text)
												if relation.find('RelationType').text:
													relation_element.set('relationtype', relation.find('RelationType').text)
												if relation.find('RelationLink').text:
													relation_element.set('href', relation.find('RelationLink').text)
												if relation.find('RelationEntry').text:
													entry_element = ET.Element('relationentry')
													relation_element.append(entry_element)
													entry_element.text = relation.find('RelationEntry').text
												if relation.find('RelationDate').text:
													from date import magic_date				
													relation_element.append(magic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
												if relation.find('RelationPlace').text:
													geogname_element = ET.Element('geogname')
													relation_element.append(geogname_element)
													geogname_element.text = relation.find('RelationPlace').text
												if relation.find('RelationNote').text:
													descriptivenote_element = ET.Element('descriptivenote')
													relation_element.append(descriptivenote_element)
													p_element = ET.Element('p')
													descriptivenote_element.append(p_element)
													p_element.text = relation.find('RelationNote').text
											else:
												# if there is already an <controlaccess> element
												relation_element = ET.Element('relation')
												match.find('relations').append(relation_element)
												if old_relation is None:
													pass
												else:
													relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
													relation_element.attrib['show'] =old_relation.attrib['show']
												if 	relation.find('RelationID').text:
													relation_element.set('id', relation.find('RelationID').text)
												if relation.find('RelationType').text:
													relation_element.set('relationtype', relation.find('RelationType').text)
												if relation.find('RelationLink').text:
													relation_element.set('href', relation.find('RelationLink').text)
												if relation.find('RelationEntry').text:
													entry_element = ET.Element('relationentry')
													relation_element.append(entry_element)
													entry_element.text = relation.find('RelationEntry').text
												if relation.find('RelationDate').text:
													from date import magic_date				
													relation_element.append(magic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
												if relation.find('RelationPlace').text:
													geogname_element = ET.Element('geogname')
													relation_element.append(geogname_element)
													geogname_element.text = relation.find('RelationPlace').text
												if relation.find('RelationNote').text:
													descriptivenote_element = ET.Element('descriptivenote')
													relation_element.append(descriptivenote_element)
													p_element = ET.Element('p')
													descriptivenote_element.append(p_element)
													p_element.text = relation.find('RelationNote').text	
						else:
							# <unitid> within <did> of <c>:
							for match in arch_root.find('dsc').iter('c'):
								if match.find('did/unitid').text:
									if match.find('did/unitid').text == collectionID + relation.find('UnitID').text:
										if match.find(tag_name) is None:
											# if there is no <relations> element
											relations_element = ET.Element('relations')
											append_index = match.getchildren().index(match.find('did')) + 1
											match.insert(append_index, relations_element)
											relation_element = ET.Element('relation')
											relations_element.append(relation_element)
											if old_relation is None:
												pass
											else:
												relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
												relation_element.attrib['show'] = old_relation.attrib['show']
											if 	relation.find('RelationID').text:
												relation_element.set('id', relation.find('RelationID').text)
											if relation.find('RelationType').text:
												relation_element.set('relationtype', relation.find('RelationType').text)
											if relation.find('RelationLink').text:
												relation_element.set('href', relation.find('RelationLink').text)
											if relation.find('RelationEntry').text:
												entry_element = ET.Element('relationentry')
												relation_element.append(entry_element)
												entry_element.text = relation.find('RelationEntry').text
											if relation.find('RelationDate').text:
												from date import magic_date				
												relation_element.append(magic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
											if relation.find('RelationPlace').text:
												geogname_element = ET.Element('geogname')
												relation_element.append(geogname_element)
												geogname_element.text = relation.find('RelationPlace').text
											if relation.find('RelationNote').text:
												descriptivenote_element = ET.Element('descriptivenote')
												relation_element.append(descriptivenote_element)
												p_element = ET.Element('p')
												descriptivenote_element.append(p_element)
												p_element.text = relation.find('RelationNote').text
										else:
											# if there is already an <controlaccess> element
											relation_element = ET.Element('relation')
											match.find('relations').append(relation_element)
											if old_relation is None:
												pass
											else:
												relation_element.attrib['actuate'] = old_relation.attrib['actuate'] 
												relation_element.attrib['show'] =old_relation.attrib['show']
											if 	relation.find('RelationID').text:
												relation_element.set('id', relation.find('RelationID').text)
											if relation.find('RelationType').text:
												relation_element.set('relationtype', relation.find('RelationType').text)
											if relation.find('RelationLink').text:
												relation_element.set('href', relation.find('RelationLink').text)
											if relation.find('RelationEntry').text:
												entry_element = ET.Element('relationentry')
												relation_element.append(entry_element)
												entry_element.text = relation.find('RelationEntry').text
											if relation.find('RelationDate').text:
												from date import magic_date				
												relation_element.append(magic_date(relation.find('RelationDate').text, relation.find('RelationDateNormal').text, 'inclusive'))
											if relation.find('RelationPlace').text:
												geogname_element = ET.Element('geogname')
												relation_element.append(geogname_element)
												geogname_element.text = relation.find('RelationPlace').text
											if relation.find('RelationNote').text:
												descriptivenote_element = ET.Element('descriptivenote')
												relation_element.append(descriptivenote_element)
												p_element = ET.Element('p')
												descriptivenote_element.append(p_element)
												p_element.text = relation.find('RelationNote').text	