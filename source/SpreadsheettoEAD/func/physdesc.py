# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals
from messages import error

def simple(did_root, CSheet, version):
	if version == "ead2002":
		if did_root.find('physdesc') is None:
			for simple_physdesc in CSheet.find('PhysicalDescriptionSet'):
				if simple_physdesc.find('Quantity').text or simple_physdesc.find('Dimensions').text or simple_physdesc.find('PhysicalFacet').text or simple_physdesc.find('PhysDescNote').text:
					physdesc_element = ET.Element('physdesc')
					did_root.append(physdesc_element)
					if simple_physdesc.find('Quantity').text:
						extent_element = ET.Element('extent')
						physdesc_element.append(extent_element)
						extent_element.text = simple_physdesc.find('Quantity').text
						if simple_physdesc.find('UnitType') is None:
							pass
						else:
							if simple_physdesc.find('UnitType').text:
								extent_element.set('unit', simple_physdesc.find('UnitType').text)
					if simple_physdesc.find('PhysicalFacet').text:
						physfacet_element = ET.Element('physfacet')
						physdesc_element.append(physfacet_element)
						physfacet_element.text = simple_physdesc.find('PhysicalFacet').text
					if simple_physdesc.find('Dimensions').text:
						dimensions_element = ET.Element('dimensions')
						physdesc_element.append(dimensions_element)
						dimensions_element.text = simple_physdesc.find('Dimensions').text
						if simple_physdesc.find('DimensionsUnit').text:
							dimensions_element.set('unit', simple_physdesc.find('DimensionsUnit').text)
					if simple_physdesc.find('PhysDescNote').text:
						physdesc_element.text = simple_physdesc.find('PhysDescNote').text
		else:
			old_physdesc = did_root.find('physdesc')
			old_extent = old_physdesc.find('extent')
			old_physfacet = old_physdesc.find('physfacet')
			old_dimensions = old_physdesc.find('dimensions')
			for delete_physdesc in did_root:
				if delete_physdesc.tag == "physdesc":
					did_root.remove(delete_physdesc)	
			if old_physdesc.text:
				if old_physdesc.find('extent') is None:
					for simple_physdesc in CSheet.find('PhysicalDescriptionSet'):
						if simple_physdesc.find('Quantity').text or simple_physdesc.find('Dimensions').text or simple_physdesc.find('PhysicalFacet').text or simple_physdesc.find('PhysDescNote').text:
							new_physdesc = ET.Element('physdesc')
							did_root.append(new_physdesc)
							if old_physdesc.attrib:
								new_physdesc.attrib = old_physdesc.attrib
							if simple_physdesc.find('Quantity').text:
								new_physdesc.text = simple_physdesc.find('Quantity').text
								if simple_physdesc.find('UnitType').text:
									new_physdesc.text = new_physdesc.text + " " + simple_physdesc.find('UnitType').text
							if simple_physdesc.find('PhysicalFacet').text:
								physfacet_element = ET.Element('physfacet')
								new_physdesc.append(physfacet_element)
								physfacet_element.text = simple_physdesc.find('PhysicalFacet').text
								if old_physfacet is None:
									pass
								else:
									if old_physfacet.attrib:
										physfacet_element.attrib = old_physfacet.attrib
							if simple_physdesc.find('Dimensions').text:
								dimensions_element = ET.Element('dimensions')
								new_physdesc.append(dimensions_element)
								dimensions_element.text = simple_physdesc.find('Dimensions').text
								if old_dimensions is None:
									pass
								else:
									if old_dimensions.attrib:
										dimensions_element.attrib = old_dimensions.attrib
								if simple_physdesc.find('DimensionsUnit').text:
									dimensions_element.set('unit', simple_physdesc.find('DimensionsUnit').text)
							if simple_physdesc.find('PhysDescNote').text:
								new_physdesc.text = new_physdesc.text + " - Note: " + simple_physdesc.find('PhysDescNote').text
				else:
					for simple_physdesc in CSheet.find('PhysicalDescriptionSet'):
						if simple_physdesc.find('Quantity').text or simple_physdesc.find('Dimensions').text or simple_physdesc.find('PhysicalFacet').text or simple_physdesc.find('PhysDescNote').text:
							new_physdesc = ET.Element('physdesc')
							did_root.append(new_physdesc)
							if old_physdesc.attrib:
								new_physdesc.attrib = old_physdesc.attrib
							if simple_physdesc.find('Quantity').text:
								quantity_element = ET.Element('extent')
								new_physdesc.append(quantity_element)
								quantity_element.text = simple_physdesc.find('Quantity').text
								#if old_extent.attrib:
									#quantity_element.attrib = old_extent.attrib
								if simple_physdesc.find('UnitType') is None:
									pass
								else:
									if simple_physdesc.find('UnitType').text:
										if "unit" not in old_extent.attrib:
											quantity_element.text = quantity_element.text + " " + simple_physdesc.find('UnitType').text
										else:
											quantity_element.set('unit', simple_physdesc.find('UnitType').text)
							if simple_physdesc.find('PhysicalFacet').text:
								physfacet_element = ET.Element('physfacet')
								new_physdesc.append(physfacet_element)
								physfacet_element.text = simple_physdesc.find('PhysicalFacet').text
								if old_physfacet is None:
									pass
								else:
									if old_physfacet.attrib:
										physfacet_element.attrib = old_physfacet.attrib
							if simple_physdesc.find('Dimensions').text:
								dimensions_element = ET.Element('dimensions')
								new_physdesc.append(dimensions_element)
								dimensions_element.text = simple_physdesc.find('Dimensions').text
								if old_dimensions is None:
									pass
								else:
									if old_dimensions.attrib:
										dimensions_element.attrib = old_dimensions.attrib
								if simple_physdesc.find('DimensionsUnit').text:
									dimensions_element.set('unit', simple_physdesc.find('DimensionsUnit').text)
							if simple_physdesc.find('PhysDescNote').text:
								new_physdesc.text = "Note: " + simple_physdesc.find('PhysDescNote').text 
			else:
				for simple_physdesc in CSheet.find('PhysicalDescriptionSet'):
					if simple_physdesc.find('Quantity').text or simple_physdesc.find('Dimensions').text or simple_physdesc.find('PhysicalFacet').text or simple_physdesc.find('PhysDescNote').text:
						new_physdesc = ET.Element('physdesc')
						did_root.append(new_physdesc)
						if old_physdesc.attrib:
							new_physdesc.attrib = old_physdesc.attrib
						if simple_physdesc.find('Quantity').text:
							quantity_element = ET.Element('extent')
							new_physdesc.append(quantity_element)
							quantity_element.text = simple_physdesc.find('Quantity').text
							#if old_extent.attrib:
								#quantity_element.attrib = old_extent.attrib
							if simple_physdesc.find('UnitType') is None:
								pass
							else:
								if simple_physdesc.find('UnitType').text:
									if old_extent is None:
										pass
									else:
										if old_extent.attrib is None:
											quantity_element.text = quantity_element.text + " " + simple_physdesc.find('UnitType').text
										else:
											if "unit" not in old_extent.attrib:
												quantity_element.text = quantity_element.text + " " + simple_physdesc.find('UnitType').text
											else:
												quantity_element.set('unit', simple_physdesc.find('UnitType').text)
						if simple_physdesc.find('PhysicalFacet').text:
							physfacet_element = ET.Element('physfacet')
							new_physdesc.append(physfacet_element)
							physfacet_element.text = simple_physdesc.find('PhysicalFacet').text
							if old_physfacet is None:
								pass
							else:
								if old_physfacet.attrib:
									physfacet_element.attrib = old_physfacet.attrib
						if simple_physdesc.find('Dimensions').text:
							dimensions_element = ET.Element('dimensions')
							new_physdesc.append(dimensions_element)
							dimensions_element.text = simple_physdesc.find('Dimensions').text
							if old_dimensions is None:
								pass
							else:
								if old_dimensions.attrib:
									dimensions_element.attrib = old_dimensions.attrib
							if simple_physdesc.find('DimensionsUnit').text:
								dimensions_element.set('unit', simple_physdesc.find('DimensionsUnit').text)
						if simple_physdesc.find('PhysDescNote').text:
							new_physdesc.text = "Note: " + simple_physdesc.find('PhysDescNote').text 
	else: #ead3 simple physdesc
		old_physdesc = did_root.find('physdesc')
		for delete_physdesc in did_root:
			if delete_physdesc.tag == "physdesc":
				did_root.remove(delete_physdesc)
		for simple_physdesc in CSheet.find('PhysicalDescriptionSet'):
			if simple_physdesc.find('Quantity').text or simple_physdesc.find('Dimensions').text or simple_physdesc.find('PhysicalFacet').text or simple_physdesc.find('PhysDescNote').text:
				new_physdesc = ET.Element('physdesc')
				did_root.append(new_physdesc)
				if old_physdesc is None:
					pass
				else:
					if old_physdesc.attrib is None:
						pass
					else:
						new_physdesc.attrib = old_physdesc.attrib
					if simple_physdesc.find('Quantity').text:
						new_physdesc.text = simple_physdesc.find('Quantity').text
					if simple_physdesc.find('UnitType').text:
						new_physdesc.text = new_physdesc.text + " " + simple_physdesc.find('UnitType').text
					if simple_physdesc.find('PhysicalFacet').text:
						new_physdesc.text = new_physdesc.text + " - " + simple_physdesc.find('PhysicalFacet').text
					if simple_physdesc.find('Dimensions').text:
						new_physdesc.text = new_physdesc.text + " - " + simple_physdesc.find('Dimensions').text
						if simple_physdesc.find('DimensionsUnit').text:
							new_physdesc.text = new_physdesc.text + " " + simple_physdesc.find('DimensionsUnit').text
					if simple_physdesc.find('PhysDescNote').text:
						new_physdesc.text = new_physdesc.text + " - Note: " + simple_physdesc.find('PhysDescNote').text

					
def structured(did_root, CSheet):
	coverage_warning = 0
	unittype1_warning = 0
	unittype2_warning = 0
	quantity_warning = 0
	if did_root.find('physdescstructuredset') is None:
		if did_root.find('physdescstructured') is None:
			pass
		else:
			did_root.remove(did_root.find('physdescstructured'))
	elif did_root.find('physdescstructured') is None:
		did_root.remove(did_root.find('physdescstructuredset'))
	else:
		did_root.remove(did_root.find('physdescstructured'))
		did_root.remove(did_root.find('physdescstructuredset'))
	whole_list = []
	for physdesc in CSheet.find('PhysicalDescriptionSet'):
		if physdesc.find('Quantity').text or physdesc.find('Dimensions').text:
			if physdesc.find('Coverage').text:
				if physdesc.find('Coverage').text.lower() == "whole":
					whole_list.append('x')
				else:
					coverage_warning = coverage_warning + 1
					if coverage_warning <= 1:
						error("@Coverage is required for <physdescstructured> in EAD3. Value must be 'whole' or 'part.' Your Finding Aid will not be valid.", False)
	if len(whole_list) > 1:
		whole_element = ET.Element('physdescstructuredset')
		whole_element.set('coverage', 'whole')
		did_root.append(whole_element)
	for physdesc in CSheet.find('PhysicalDescriptionSet'):
		if physdesc.find('Quantity').text or physdesc.find('Dimensions').text or physdesc.find('PhysicalFacet').text or physdesc.find('PhysDescNote').text:
			if physdesc.find('UnitType') is None:
				pass
			else:
				if physdesc.find('UnitType').text:
					pass
				else:
					#Error message for no element name
					unittype1_warning = unittype1_warning + 1
					if unittype1_warning <= 1:
						error("Your EAD3 template uses <physdescstructured> but you did not enter a <unittype>, so your finding aid will not be valid.", False)
			if physdesc.find('Coverage').text:
				if physdesc.find('Coverage').text.lower() == "whole":
					physdescwhole_element = ET.Element('physdescstructured')
					physdescwhole_element.set('coverage', 'whole')
					if did_root.find("physdescstructuredset[@coverage='whole']") is None:
						did_root.append(physdescwhole_element)
					else:
						did_root.find('physdescstructuredset').append(physdescwhole_element)
					if physdesc.find('Type').text:
						physdescwhole_element.set('physdescstructuredtype', physdesc.find('Type').text.lower())
					if physdesc.find('Quantity').text:
						quantity_element = ET.Element('quantity')
						physdescwhole_element.append(quantity_element)
						quantity_element.text = physdesc.find('Quantity').text
					else:
						quantity_warning = quantity_warning + 1
						if quantity_warning <= 1:
							error("No Quantity was entered. <physdescstructured> requires a <quantity>. The ead file for his collection will not be valid.", False)
					if physdesc.find('Approximate').text:
						quantity_element.set('approximate', physdesc.find('Approximate').text.lower())
					if physdesc.find('UnitType').text:
						unittype_element = ET.Element('unittype')
						physdescwhole_element.append(unittype_element)
						unittype_element.text = physdesc.find('UnitType').text
					else:
						unittype2_warning = unittype2_warning + 1
						if unittype2_warning <=1:
							error("No Unit Type was entered. <physdescstructured> requires a <unittype>. The ead file for his collection will not be valid.", False)
					if physdesc.find('PhysicalFacet').text:
						physfacet_element = ET.Element('physfacet')
						physdescwhole_element.append(physfacet_element)
						physfacet_element.text = physdesc.find('PhysicalFacet').text
					if physdesc.find('Dimensions').text:
						dimensions_element = ET.Element('dimensions')
						physdescwhole_element.append(dimensions_element)
						dimensions_element.text = physdesc.find('Dimensions').text
						if physdesc.find('DimensionsUnit').text:
							dimensions_element.set('unit', physdesc.find('DimensionsUnit').text)
					if physdesc.find('PhysDescNote').text:
						physnote_element = ET.Element('descriptivenote')
						physdescwhole_element.append(physnote_element)
						p_element = ET.Element('p')
						physnote_element.append(p_element)
						p_element.text = physdesc.find('PhysDescNote').text
				elif physdesc.find('Coverage').text.lower() == "part":
					pass
				else: 
					error("@Coverage is required for <physdescstructured> in EAD3. Value must be 'whole' or 'part.' Your Finding Aid will not be valid.", False)
			else:
				error("@Coverage is required for <physdescstructured> in EAD3. Value must be 'whole' or 'part.' Your Finding Aid will not be valid.", False)
	part_list = []
	for physdesc in CSheet.find('PhysicalDescriptionSet'):
		if physdesc.find('Quantity').text or physdesc.find('Dimensions').text:
			if physdesc.find('Coverage').text:
				if physdesc.find('Coverage').text.lower() == "part":
					part_list.append('y')
			else:
				error("@Coverage is required for <physdescstructured> in EAD3. Value must be 'whole' or 'part.' Your Finding Aid will not be valid.", False)
	if len(part_list) > 1:
		part_element = ET.Element('physdescstructuredset')
		part_element.set('coverage', 'part')
		did_root.append(part_element)
	for physdesc in CSheet.find('PhysicalDescriptionSet'):
		if physdesc.find('Quantity').text or physdesc.find('Dimensions').text or physdesc.find('PhysicalFacet').text or physdesc.find('PhysDescNote').text:
			if physdesc.find('Coverage').text:
				if physdesc.find('Coverage').text.lower() == "part":
					physdescpart_element = ET.Element('physdescstructured')
					physdescpart_element.set('coverage', 'part')
					if did_root.find("physdescstructuredset[@coverage='part']") is None:
						did_root.append(physdescpart_element)
					else:
						did_root.find('physdescstructuredset').append(physdescpart_element)
					physdescpart_element.set('physdescstructuredtype', physdesc.find('Type').text)
					if physdesc.find('Quantity').text:
						quantity_element = ET.Element('quantity')
						physdescpart_element.append(quantity_element)
						quantity_element.text = physdesc.find('Quantity').text
					else:
						error("No Quantity was entered. <physdescstructured> requires a <quantity>. The ead file for his collection will not be valid.", False)
					if physdesc.find('Approximate').text:
						quantity_element.set('approximate', physdesc.find('Approximate').text.lower())
					if physdesc.find('UnitType').text:
						unittype_element = ET.Element('unittype')
						physdescpart_element.append(unittype_element)
						unittype_element.text = physdesc.find('UnitType').text
					else:
						error("No Unit Type was entered. <physdescstructured> requires a <unittype>. The ead file for his collection will not be valid.", False)
					if physdesc.find('PhysicalFacet').text:
						physfacet_element = ET.Element('physfacet')
						physdescpart_element.append(physfacet_element)
						physfacet_element.text = physdesc.find('PhysicalFacet').text
					if physdesc.find('Dimensions').text:
						dimensions_element = ET.Element('dimensions')
						physdescpart_element.append(dimensions_element)
						dimensions_element.text = physdesc.find('Dimensions').text
						if physdesc.find('DimensionsUnit').text:
							dimensions_element.set('unit', physdesc.find('DimensionsUnit').text)
					if physdesc.find('PhysDescNote').text:
						physnote_element = ET.Element('descriptivenote')
						physdescpart_element.append(physnote_element)
						p_element = ET.Element('p')
						physnote_element.append(p_element)
						p_element.text = physdesc.find('PhysDescNote').text
				elif physdesc.find('Coverage').text.lower() == "whole":
					pass
				else: 
					error("Structured Physical Description (<physdescstructured>) coverage must be 'whole' or 'part.' no <physdescstructured> element will be created for this collection", False)
			else:
				error("@Coverage is required for <physdescstructured> in EAD3. Value must be 'whole' or 'part.' Your Finding Aid will not be valid.", False)