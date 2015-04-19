# module for the more complex elements of the collection-level <archdesc> element: <accessrestrict> and <userestrict>
import xml.etree.cElementTree as ET
import globals
from mixed_content import mixed_content

def access_use_restrict(arch_root, Input, element_name, name, version):
	if arch_root.find(element_name) is None:
		pass
	else:
		for restriction in arch_root:
			if restriction.tag == element_name:
				if arch_root.find(element_name).find('address') is None:
					pass
				else:
					for address_line in reversed(arch_root.find(element_name)):
						if address_line.tag == "address":
							Statement_element = ET.Element('Statement')
							Input.insert(0, Statement_element)
							Statement_element.text = mixed_content(address_line)
				if arch_root.find(element_name).find('p') is None:
					pass
				else:
					for simple_restrict in reversed(arch_root.find(element_name)):
						if simple_restrict.tag == "p":
							Statement_element = ET.Element('Statement')
							Input.insert(0, Statement_element)
							Statement_element.text = mixed_content(simple_restrict)
				if arch_root.find(element_name).find('list') is None:
					pass
				else:
					for empty_tag in Input.find('SpecificMaterialRestrictions'):
						if empty_tag.text:
							pass
						else:
							Input.find('SpecificMaterialRestrictions').remove(empty_tag)
					if version == "ead2002":
						if arch_root.find(element_name).find('list').attrib['type'] == "deflist":
							for item in arch_root.find(element_name).find('list'):
								if item.tag == "defitem":
									SpecificRestriction_element = ET.Element('SpecificRestriction')
									Input.find('SpecificMaterialRestrictions').append(SpecificRestriction_element)
									UnitID_element = ET.Element('UnitID')
									SpecificRestriction_element.append(UnitID_element)
									Material_element = ET.Element('Material')
									SpecificRestriction_element.append(Material_element)
									Restriction_element = ET.Element('Restriction')
									SpecificRestriction_element.append(Restriction_element)
									Material_element.text = item.find('label').text
									Restriction_element.text = item.find('item').text
					else:
						if arch_root.find(element_name).find('list').attrib['listtype'] == "deflist":
							for item in arch_root.find(element_name).find('list'):
								if item.tag == "defitem":
									SpecificRestriction_element = ET.Element('SpecificRestriction')
									Input.find('SpecificMaterialRestrictions').append(SpecificRestriction_element)
									UnitID_element = ET.Element('UnitID')
									SpecificRestriction_element.append(UnitID_element)
									Material_element = ET.Element('Material')
									SpecificRestriction_element.append(Material_element)
									Restriction_element = ET.Element('Restriction')
									SpecificRestriction_element.append(Restriction_element)
									Material_element.text = item.find('label').text
									Restriction_element.text = item.find('item').text
	for dumb_descgrp in arch_root:
		if dumb_descgrp.tag == "descgrp":
			if dumb_descgrp.find(element_name) is None:
				pass
			else:
				for restriction in dumb_descgrp:
					if restriction.tag == element_name:
						if restriction.find('address') is None:
							pass
						else:
							for address_line in reversed(restriction):
								if address_line.tag == "address":
									Statement_element = ET.Element('Statement')
									Input.insert(0, Statement_element)
									Statement_element.text = mixed_content(address_line)
						if restriction.find('p') is None:
							pass
						else:
							for simple_restrict in reversed(restriction):
								if simple_restrict.tag == "p":
									Statement_element = ET.Element('Statement')
									Input.insert(0, Statement_element)
									Statement_element.text = mixed_content(simple_restrict)
						if restriction.find('list') is None:
							pass
						else:
							for empty_tag in Input.find('SpecificMaterialRestrictions'):
								if empty_tag.text:
									pass
								else:
									Input.find('SpecificMaterialRestrictions').remove(empty_tag)
							if version == "ead2002":
								if restriction.find('list').attrib['type'] == "deflist":
									for item in restriction.find('list'):
										if item.tag == "defitem":
											SpecificRestriction_element = ET.Element('SpecificRestriction')
											Input.find('SpecificMaterialRestrictions').append(SpecificRestriction_element)
											UnitID_element = ET.Element('UnitID')
											SpecificRestriction_element.append(UnitID_element)
											Material_element = ET.Element('Material')
											SpecificRestriction_element.append(Material_element)
											Restriction_element = ET.Element('Restriction')
											SpecificRestriction_element.append(Restriction_element)
											Material_element.text = item.find('label').text
											Restriction_element.text = item.find('item').text
							else:
								if restriction.find('list').attrib['listtype'] == "deflist":
									for item in restriction.find('list'):
										if item.tag == "defitem":
											SpecificRestriction_element = ET.Element('SpecificRestriction')
											Input.find('SpecificMaterialRestrictions').append(SpecificRestriction_element)
											UnitID_element = ET.Element('UnitID')
											SpecificRestriction_element.append(UnitID_element)
											Material_element = ET.Element('Material')
											SpecificRestriction_element.append(Material_element)
											Restriction_element = ET.Element('Restriction')
											SpecificRestriction_element.append(Restriction_element)
											Material_element.text = item.find('label').text
											Restriction_element.text = item.find('item').text