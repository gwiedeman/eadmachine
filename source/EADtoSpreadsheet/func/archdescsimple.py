# module for the simple elements of the collection-level <archdesc> element
import xml.etree.cElementTree as ET
import globals
from mixed_content import mixed_content

def archdescsimple(arch_root, arch_element, parent, child_tagname, version):
	if arch_root.find(arch_element) is None:
		pass
	else:
		parent.clear()
		for simple_archelement in arch_root:
			if simple_archelement.tag == arch_element:
				for para in simple_archelement:
					if para.tag == "p":
						child_element = ET.Element(child_tagname)
						parent.append(child_element)
						UnitID_element = ET.Element('UnitID')
						child_element.append(UnitID_element)
						Text_element = ET.Element('Text')
						child_element.append(Text_element)
						Text_element.text = mixed_content(para)
	for dumb_descgrp in arch_root:
		if dumb_descgrp.tag == "descgrp":
			if dumb_descgrp.find(arch_element) is None:
				pass
			else:
				parent.clear()
				for simple_archelement in dumb_descgrp:
					if simple_archelement.tag == arch_element:
						for para in simple_archelement:
							if para.tag == "p":
								child_element = ET.Element(child_tagname)
								parent.append(child_element)
								UnitID_element = ET.Element('UnitID')
								child_element.append(UnitID_element)
								Text_element = ET.Element('Text')
								child_element.append(Text_element)
								Text_element.text = mixed_content(para)