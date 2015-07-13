# module for the more complex elements of the collection-level <archdesc> element: <accessrestrict> and <userestrict>
import xml.etree.cElementTree as ET
import globals

def access_use_restrict(arch_root, Input, element_name, name, add):
	if Input.find('Statement') is None:
		if Input.find('SpecificMaterialRestrictions/SpecificRestriction/Material') is None:
			restrict_data = False
		else:
			if Input.find('SpecificMaterialRestrictions/SpecificRestriction/Material').text:
				restrict_data = True
			else:
				restrict_data = False
	else:
		if Input.find('Statement').text or Input.find('SpecificMaterialRestrictions/SpecificRestriction/Material').text:
			restrict_data = True
		else:
			restrict_data = False
	
	if restrict_data == True:
		if arch_root.find(element_name) is None:
			if add is True:
				new_element = ET.Element(element_name)
				arch_root.insert(1, new_element)
				for statement in Input:
					if statement.tag == "Statement":
						p_element = ET.Element('p')
						arch_root.find(element_name).append(p_element)
						p_element.text = statement.text
				restrict_count = 0
				for spec_restrict in Input.find('SpecificMaterialRestrictions'):
					if spec_restrict.find('Material') is None or spec_restrict.find('Restriction') is None:
						pass
					else:
						if spec_restrict.find('Material').text or spec_restrict.find('Restriction').text:
							restrict_count = restrict_count + 1
				if restrict_count > 0:
					list_element = ET. Element('list')
					arch_root.find(element_name).append(list_element)
					list_element.set('listtype', 'deflist')
					listhead_element = ET.Element('listhead')
					list_element.append(listhead_element)
					head01_element = ET.Element('head01')
					listhead_element.append(head01_element)
					head02_element = ET.Element('head02')
					listhead_element.append(head02_element)
					head01_element.text = "Material"
					head02_element.text = name + " Restrictions"
					for specific_restr in Input.find('SpecificMaterialRestrictions'):
						if specific_restr.find('Material') is None or specific_restr.find('Restriction') is None:
							pass
						else:
							if specific_restr.find('Material').text and specific_restr.find('Restriction').text:
								defitem_element = ET.Element('defitem')
								list_element.append(defitem_element)
								if  specific_restr.find('UnitID').text:
									defitem_element.set('id', specific_restr.find('UnitID').text)
								label_element = ET.Element('label')
								item_element = ET.Element('item')
								defitem_element.append(label_element)
								defitem_element.append(item_element)
								if specific_restr.find('Material').text:
									label_element.text = specific_restr.find('Material').text
								if specific_restr.find('Restriction').text:
									item_element.text = specific_restr.find('Restriction').text
		else:
			old_restrict = arch_root.find(element_name).attrib
			old_head = arch_root.find(element_name).find('head')
			old_listhead1 = arch_root.find(element_name).find('list/listhead/head01')
			old_listhead2 = arch_root.find(element_name).find('list/listhead/head02')
			arch_root.find(element_name).clear()
			if old_head is None:
				pass
			else:
				arch_root.find(element_name).append(old_head)
			for statement in Input:
				if statement.tag == "Statement":
					p_element = ET.Element('p')
					arch_root.find(element_name).append(p_element)
					p_element.text = statement.text
			if old_restrict is None:
				pass
			else:
				arch_root.find(element_name).attrib = old_restrict
			restrict_count = 0
			for spec_restrict in Input.find('SpecificMaterialRestrictions'):
				if spec_restrict.find('Material') is None or spec_restrict.find('Restriction') is None:
					pass
				else:
					if spec_restrict.find('Material').text or spec_restrict.find('Restriction').text:
						restrict_count = restrict_count + 1
			if restrict_count > 0:
				list_element = ET. Element('list')
				arch_root.find(element_name).append(list_element)
				list_element.set('listtype', 'deflist')
				listhead_element = ET.Element('listhead')
				list_element.append(listhead_element)
				head01_element = ET.Element('head01')
				listhead_element.append(head01_element)
				head02_element = ET.Element('head02')
				listhead_element.append(head02_element)
				if old_listhead1 is None:
					head01_element.text = "Material"
				else:
					head01_element.text = old_listhead1.text
				if old_listhead2 is None:
					head02_element.text = name + " Restrictions"
				else:
					head02_element.text = old_listhead2.text
				for specific_restr in Input.find('SpecificMaterialRestrictions'):
					if specific_restr.find('Material') is None or specific_restr.find('Restriction') is None:
						pass
					else:
						if specific_restr.find('Material').text and specific_restr.find('Restriction').text:
							defitem_element = ET.Element('defitem')
							list_element.append(defitem_element)
							if  specific_restr.find('UnitID').text:
								defitem_element.set('id', specific_restr.find('UnitID').text)
							label_element = ET.Element('label')
							item_element = ET.Element('item')
							defitem_element.append(label_element)
							defitem_element.append(item_element)
							if specific_restr.find('Material').text:
								label_element.text = specific_restr.find('Material').text
							if specific_restr.find('Restriction').text:
								item_element.text = specific_restr.find('Restriction').text
	else:
		for empty_restrict in arch_root:
			if empty_restrict.tag == element_name:
				arch_root.remove(empty_restrict)
						

def access_use_lower(arch_root, input_element, tag_name, collectionID, series_separator):
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
		if input_element.find('SpecificMaterialRestrictions') is None:
			pass
		else:
			for restriction in input_element.find('SpecificMaterialRestrictions'):
				if restriction.find('UnitID').text:
					if restriction.find('Restriction').text:
						if attribute_id == True:
							if c_numbers == True:
								# @id in <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.attrib['id'] == restriction.find('UnitID').text:
											if match.find(tag_name) is None:
												restrict_element = ET.Element(tag_name)
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, restrict_element)
												p_element = ET.Element('p')
												restrict_element.append(p_element)
												p_element.text = restriction.find('Restriction').text
											else:
												p_element = ET.Element('p')
												match.find(tag_name).append(p_element)
												p_element.text = restriction.find('Restriction').text
							else:
								# @id in <c>:
								for match in arch_root.find('dsc').iter('c'):
									if "id" in match.attrib:
										if match.attrib['id'] == restriction.find('UnitID').text or match.attrib['id'] == restriction.find('UnitID').text:
											if match.find(tag_name) is None:
												restrict_element = ET.Element(tag_name)
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, restrict_element)
												p_element = ET.Element('p')
												restrict_element.append(p_element)
												p_element.text = restriction.find('Restriction').text
											else:
												p_element = ET.Element('p')
												match.find(tag_name).append(p_element)
												p_element.text = restriction.find('Restriction').text
						else:
							if c_numbers == True:
								# <unitid> within <did> of <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.find('did/unitid') is None:
											pass
										else:
											if match.find('did/unitid').text:
												if match.find('did/unitid').text == restriction.find('UnitID').text:
													if match.find(tag_name) is None:
														restrict_element = ET.Element(tag_name)
														append_index = match.getchildren().index(match.find('did')) + 1
														match.insert(append_index, restrict_element)
														p_element = ET.Element('p')
														restrict_element.append(p_element)
														p_element.text = restriction.find('Restriction').text
													else:
														p_element = ET.Element('p')
														match.find(tag_name).append(p_element)
														p_element.text = restriction.find('Restriction').text
							else:
								# <unitid> within <did> of <c> or no series:
								for match in arch_root.find('dsc').iter('c'):
									if match.find('did/unitid') is None:
										pass
									else:
										if match.find('did/unitid') is None:
											pass
										else:
											if match.find('did/unitid').text:
												if match.find('did/unitid').text == restriction.find('UnitID').text:
													if match.find(tag_name) is None:
														restrict_element = ET.Element(tag_name)
														append_index = match.getchildren().index(match.find('did')) + 1
														match.insert(append_index, restrict_element)
														p_element = ET.Element('p')
														restrict_element.append(p_element)
														p_element.text = restriction.find('Restriction').text
													else:
														p_element = ET.Element('p')
														match.find(tag_name).append(p_element)
														p_element.text = restriction.find('Restriction').text