# module for the simple elements of the collection-level <archdesc> element
import xml.etree.cElementTree as ET
import globals

def archdescsimple(arch_root, arch_element, parent, child, add):
	archelement_count = 0
	if child is None:
		pass
	else:
		if child.text:
			if arch_root.find(arch_element) is None:
				if add is True:
					add_element = ET.Element(arch_element)
					if arch_root.find('dsc') is None:
						arch_root.append(add_element)
					else: 
						element_index = arch_root.getchildren().index(arch_root.find('dsc'))
						arch_root.insert(element_index, add_element)
					for element in parent:
						if element.find('UnitID') is None:
							if element.text:
								p_element = ET.Element('p')
								add_element.append(p_element)
								p_element.text = element.text
						else:
							if element.find('UnitID').text:
								pass
							else:
								if element.find('Text').text:
									p_element = ET.Element('p')
									add_element.append(p_element)
									p_element.text = element.find('Text').text
			else:
				old_element = arch_root.find(arch_element).attrib
				old_head = arch_root.find(arch_element).find('head')
				arch_root.find(arch_element).clear()
				if old_head is None:
					pass
				else:
					arch_root.find(arch_element).append(old_head)
				for element in parent:
					if element.find('UnitID') is None:
						if element.text:
							archelement_count = archelement_count + 1
							p_element = ET.Element('p')
							arch_root.find(arch_element).append(p_element)
							p_element.text = element.text
					else:
						if element.find('UnitID').text:
							pass
						else:
							if element.find('Text').text:
								archelement_count = archelement_count + 1
								p_element = ET.Element('p')
								arch_root.find(arch_element).append(p_element)
								p_element.text = element.find('Text').text
				if old_element is None:
					pass
				else:
					arch_root.find(arch_element).attrib = old_element
	#removes element if no data is entered
	if archelement_count < 1:
		for empty_element in arch_root:
			if empty_element.tag == arch_element:
				arch_root.remove(empty_element)

def archdescsimple_lower(arch_root, input_element, tag_name, collectionID, series_separator):
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
			for info in input_element:
				if info.find('UnitID').text:
					if info.find('Text').text:
						if attribute_id == True:
							if c_numbers == True:
								# @id in <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.attrib['id'] == collectionID + info.find('UnitID').text:
											if match.find(tag_name) is None:
												newtag_element = ET.Element(tag_name)
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, newtag_element)
												p_element = ET.Element('p')
												newtag_element.append(p_element)
												p_element.text = info.find('Text').text
											else:
												p_element = ET.Element('p')
												match.find(tag_name).append(p_element)
												p_element.text = info.find('Text').text
							else:
								# @id in <c>:
								for match in arch_root.find('dsc').iter('c'):
									if "id" in match.attrib:
										if match.attrib['id'] == collectionID + info.find('UnitID').text:
											if match.find(tag_name) is None:
												newtag_element = ET.Element(tag_name)
												append_index = match.getchildren().index(match.find('did')) + 1
												match.insert(append_index, newtag_element)
												p_element = ET.Element('p')
												newtag_element.append(p_element)
												p_element.text = info.find('Text').text
											else:
												p_element = ET.Element('p')
												match.find(tag_name).append(p_element)
												p_element.text = info.find('Text').text
						else:
							if c_numbers == True:
								# <unitid> within <did> of <c01>, <c02>, etc.:
								for match in arch_root.find('dsc').iter():
									if match.tag.startswith('c0') or match.tag.startswith('c1'):
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + info.find('UnitID').text:
												if match.find(tag_name) is None:
													newtag_element = ET.Element(tag_name)
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, newtag_element)
													p_element = ET.Element('p')
													newtag_element.append(p_element)
													p_element.text = info.find('Text').text
												else:
													p_element = ET.Element('p')
													match.find(tag_name).append(p_element)
													p_element.text = info.find('Text').text
							else:
								# <unitid> within <did> of <c>:
								for match in arch_root.find('dsc').iter('c'):
									if match.find('did/unitid') is None:
										pass
									else:
										if match.find('did/unitid').text:
											if match.find('did/unitid').text == collectionID + info.find('UnitID').text:
												if match.find(tag_name) is None:
													newtag_element = ET.Element(tag_name)
													append_index = match.getchildren().index(match.find('did')) + 1
													match.insert(append_index, newtag_element)
													p_element = ET.Element('p')
													newtag_element.append(p_element)
													p_element.text = info.find('Text').text
												else:
													p_element = ET.Element('p')
													match.find(tag_name).append(p_element)
													p_element.text = info.find('Text').text