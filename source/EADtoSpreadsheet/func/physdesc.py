# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals
from messages import error
from mixed_content import mixed_content

def simple(did_root, CSheet, version):
	if did_root.find('physdesc/extent') is None:
		if did_root.find('physdesc').text:
			CSheet.find('PhysicalDescriptionSet/PhysicalDescription/Quantity').text = mixed_content(did_root.find('physdesc'))
			if 'unit' in did_root.find('physdesc').attrib:
				CSheet.find('PhysicalDescriptionSet/PhysicalDescription/UnitType').text = did_root.find('physdesc').attrib['unit']
	else:
		CSheet.find('PhysicalDescriptionSet/PhysicalDescription/Quantity').text = did_root.find('physdesc/extent').text
		if 'unit' in did_root.find('physdesc/extent').attrib:
			CSheet.find('PhysicalDescriptionSet/PhysicalDescription/UnitType').text = did_root.find('physdesc/extent').attrib['unit']
		if did_root.find('physdesc').text:
			CSheet.find('PhysicalDescriptionSet/PhysicalDescription/PhysDescNote').text = did_root.find('physdesc').text
		if len(did_root.find('physdesc').tail.strip()) >= 1:
			CSheet.find('PhysicalDescriptionSet/PhysicalDescription/PhysDescNote').text = CSheet.find('PhysicalDescriptionSet/PhysicalDescription/PhysDescNote').text + did_root.find('physdesc').tail
	if did_root.find('physdesc/dimensions') is None:
		pass
	else:
		CSheet.find('PhysicalDescriptionSet/PhysicalDescription/Dimensions').text = did_root.find('physdesc/dimensions').text
		if 'unit' in did_root.find('physdesc/dimensions').attrib:
			CSheet.find('PhysicalDescriptionSet/PhysicalDescription/DimensionsUnit').text = did_root.find('physdesc/dimensions').attrib['unit']
	if did_root.find('physdesc/physfacet') is None:
		pass
	else:
		CSheet.find('PhysicalDescriptionSet/PhysicalDescription/PhysicalFacet').text = did_root.find('physdesc/physfacet').text

					
def structured(did_root, CSheet):
	CSheet.find('PhysicalDescriptionSet').clear()
	for physdesc in did_root.iter('physdescstructured'):
		PhysicalDescription_element = ET.Element('PhysicalDescription')
		CSheet.find('PhysicalDescriptionSet').append(PhysicalDescription_element)
		Coverage_element = ET.Element('Coverage')
		PhysicalDescription_element.append(Coverage_element)
		Type_element = ET.Element('Type')
		PhysicalDescription_element.append(Type_element)
		Approximate_element = ET.Element('Approximate')
		PhysicalDescription_element.append(Approximate_element)
		Quantity_element = ET.Element('Quantity')
		PhysicalDescription_element.append(Quantity_element)
		UnitType_element = ET.Element('UnitType')
		PhysicalDescription_element.append(UnitType_element)
		PhysicalFacet_element = ET.Element('PhysicalFacet')
		PhysicalDescription_element.append(PhysicalFacet_element)
		Dimensions_element = ET.Element('Dimensions')
		PhysicalDescription_element.append(Dimensions_element)
		DimensionsUnit_element = ET.Element('DimensionsUnit')
		PhysicalDescription_element.append(DimensionsUnit_element)
		PhysDescNote_element = ET.Element('PhysDescNote')
		PhysicalDescription_element.append(PhysDescNote_element)
		if 'coverage' in physdesc.attrib:
			Coverage_element.text = physdesc.attrib['coverage']
		if 'physdescstructuredtype' in physdesc.attrib:
			Type_element.text = physdesc.attrib['physdescstructuredtype']
		if 'approximate' in physdesc.find('quantity').attrib:
			Approximate_element.text = physdesc.find('quantity').attrib['approximate']
		Quantity_element.text = physdesc.find('quantity').text
		UnitType_element.text = physdesc.find('unittype').text
		if physdesc.find('physfacet') is None:
			pass
		else:
			PhysicalFacet_element.text = physdesc.find('physfacet').text
		if physdesc.find('dimensions') is None:
			pass
		else:
			Dimensions_element.text = physdesc.find('dimensions').text
			if 'unit' in physdesc.find('dimensions').attrib:
				DimensionsUnit_element.text = physdesc.find('dimensions').attrib['unit']
		if physdesc.find('descriptivenote') is None:
			pass
		else:
			PhysDescNote_element.text = physdesc.find('descriptivenote/p').text