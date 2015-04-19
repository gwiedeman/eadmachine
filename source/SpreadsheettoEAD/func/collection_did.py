# module for the collection-level <did>
import xml.etree.cElementTree as ET
from date import magic_date
import globals
from messages import error

def collection_did(did_root, CSheet, version):

	did_root.find('unittitle').text = CSheet.find('CollectionName').text
	if did_root.find('unitid') is None:
		if "add_unitid" in globals.new_elements or "add-all" in globals.add_all:
			unitid_element = ET.Element('unitid')
			last_unittitle = did_root.getchildren().index(did_root.find('unittitle')) + 1
			did_root.insert(last_unittitle, unitid_element)
			unitid_element.text = CSheet.find('CollectionID').text
	else:
		did_root.find('unitid').text = CSheet.find('CollectionID').text
	
	# collection-level unitdate
	from collection_unitdate import simple_unitdate
	from collection_unitdate import ead3simple_unitdate
	if version == "ead2002":
		if did_root.find('unittitle/unitdate') is None:
			simple_unitdate(did_root, CSheet)
		else:
			simple_unitdate(did_root.find('unittitle'), CSheet)
	else:
		if did_root.find('unitdate') is None:
			pass
		else:
			ead3simple_unitdate(did_root, CSheet)
		if did_root.find('unitdatestructured') is None:
			pass
		else:
			unitdatestructured = did_root.find('unitdatestructured')
			unitdatestructured_index = did_root.getchildren().index(unitdatestructured)
			unitdatestructured_list = did_root.findall('unitdatestructured')
			for unitdatestructured in reversed(unitdatestructured_list):
				did_root.remove(unitdatestructured)
			if CSheet.find('DateInclusive').text:
				did_root.insert(unitdatestructured_index, magic_date(CSheet.find('DateInclusive').text, CSheet.find('DateInclusiveNormal').text, 'inclusive'))
			if CSheet.find('DateBulk').text:
				did_root.insert(unitdatestructured_index, magic_date(CSheet.find('DateBulk').text, CSheet.find('DateBulkNormal').text, 'bulk'))
			else:
				if "add_bulkdate" in globals.new_elements or "add-all" in globals.add_all:
					did_root.insert(unitdatestructured_index, magic_date(CSheet.find('DateBulk').text, CSheet.find('DateBulkNormal').text, 'bulk'))
	
	# Abstract for both EAD 2002 and EAD3
	if CSheet.find('Abstract').text:
		if did_root.find('abstract') is None:
			if "add_abstract" in globals.new_elements or "add-all" in globals.add_all:
				abstract_element = ET.Element('abstract')
				did_root.append(abstract_element)
				abstract_element.text = CSheet.find('Abstract').text
		else:
			did_root.find('abstract').text = CSheet.find('Abstract').text
	
	
	# Collection Language Material
	from collection_language import language
	language(did_root, CSheet, version)
	
	# Origination Section
	old_origin = did_root.find('origination')
	origin_count = 0
	for origination in CSheet.find('Origins'):
		if origination.find('Part').text:
			origin_count = origin_count + 1
			if did_root.find('origination') is None and did_root.find('neworigination') is None:
				if "add_origin" in globals.new_elements or "add-all" in globals.add_all:
					origination_element = ET.Element('neworigination')
					did_root.append(origination_element)
					new_element = ET.Element(origination.find('ElementName').text)
					origination_element.append(new_element)
					if version == "ead2002":
						new_element.text = origination.find('Part').text
					else:
						part_element = ET.Element('part')
						new_element.append(part_element)
						part_element.text = origination.find('Part').text
					if origination.find('MARCEncoding').text:
						new_element.set('encodinganalog', origination.find('MARCEncoding').text)
					if origination.find('Identifier').text:
						if version == "ead3":
							new_element.set('identifier', origination.find('Identifier').text)
						else:
							new_element.set('id', origination.find('Identifier').text)
					if origination.find('Relator').text:
						if version == "ead3":
							new_element.set('relator', origination.find('Relator').text)
						else:
							new_element.set('role', origination.find('Relator').text)
					if origination.find('Normal').text:
						new_element.set('normal', origination.find('Normal').text)
					if origination.find('Source').text:
						new_element.set('source', origination.find('Source').text)
			else:
				old_origin_list = did_root.findall('origination')
				for old_origin_ele in old_origin_list:
					did_root.remove(old_origin_ele)
				origination_element = ET.Element('neworigination')
				did_root.append(origination_element)
				if old_origin is None:
					pass
				else:
					origination_element.attrib = old_origin.attrib
				new_element = ET.Element(origination.find('ElementName').text)
				origination_element.append(new_element)
				if version == "ead2002":
					new_element.text = origination.find('Part').text
				else:
					part_element = ET.Element('part')
					new_element.append(part_element)
					part_element.text = origination.find('Part').text
				if origination.find('MARCEncoding').text:
					new_element.set('encodinganalog', origination.find('MARCEncoding').text)
				if origination.find('Identifier').text:
					if version == "ead3":
						new_element.set('identifier', origination.find('Identifier').text)
					else:
						new_element.set('id', origination.find('Identifier').text)
				if origination.find('Relator').text:
					if version == "ead3":
						new_element.set('relator', origination.find('Relator').text)
					else:
						new_element.set('role', origination.find('Relator').text)
				if origination.find('Normal').text:
					new_element.set('normal', origination.find('Normal').text)
				if origination.find('Source').text:
					new_element.set('source', origination.find('Source').text)
		
	# Changes <neworigination> tags to <origination> tags
	for wrongtag in did_root:
		if wrongtag.tag == 'neworigination':
			wrongtag.tag = 'origination'
	
	# Removes all <origination> if no origination is entered
	if origin_count < 1:
		for empty_origin in did_root:
			if empty_origin.tag == "origination":
				did_root.remove(empty_origin)
	
	#PhysicalDescription section
	from physdesc import simple
	from physdesc import structured
	
	if did_root.find('physdesc') is None:
		if did_root.find('physdescstructured') is None and did_root.find('physdescstructuredset') is None:
			if CSheet.find('PhysicalDescriptionSet/PhysicalDescription/Quantity').text or CSheet.find('PhysicalDescriptionSet/PhysicalDescription/Dimensions').text:
				if version == "ead2002":
					if "add_physdesc" in globals.new_elements or "add-all" in globals.add_all:
						simple(did_root, CSheet, version)
				else:
					if "add_physdesc" in globals.new_elements or "add-all" in globals.add_all:
						simple(did_root, CSheet, version)
						structured(did_root, CSheet)
		else:
			structured(did_root, CSheet)
	else:
		if did_root.find('physdescstructured') is None and did_root.find('physdescstructuredset') is None:
			simple(did_root, CSheet, version)
		else:
			simple(did_root, CSheet, version)
			structured(did_root, CSheet)
	
	# Physical Location Section, same for both EAD2002 and EAD3
	if did_root.find('physloc') is None:
		old_physloc_test = 0
	else:
		old_physloc_test = 1
		old_physloc = did_root.find('physloc')
	for old_physloc_list in did_root.findall('physloc'):
		did_root.remove(old_physloc_list)
	for physloc in CSheet.find('PhysicalLocationSet'):
		if physloc.find('Location').text:
			physloc_element = ET.Element('physloc')
			did_root.append(physloc_element)
			physloc_element.text = physloc.find('Location').text
			if old_physloc_test == 1:
				if old_physloc.attrib is None:
					pass
				else:
					physloc_element.attrib = old_physloc.attrib
			if physloc.find('Audience').text:
				physloc_element.set('audience', physloc.find('Audience').text)	
	
	# Repository Section
	old_repository = did_root.find('repository')
	old_corpname = did_root.find('repository/corpname')
	old_address = did_root.find('repository/address')
	for old_rep_list in did_root.findall('repository'):
		did_root.remove(old_rep_list)
	repository_element = ET.Element('repository')
	did_root.append(repository_element)
	if old_repository is None:
		pass
	else:
		if old_repository.attrib is None:
			pass
		else:
			repository_element.attrib = old_repository.attrib
	if CSheet.find('Repository/RepositoryName').text:
		if version == "ead3":
			if CSheet.find('Repository/ElementName').text:
				corpname_element = ET.Element(CSheet.find('Repository/ElementName').text)
			else:
				corpname_element = ET.Element('corpname')
		else:
			corpname_element = ET.Element('corpname')
		repository_element.append(corpname_element)
		corpname_element.text = CSheet.find('Repository/RepositoryName').text
		if old_corpname is None:
			pass
		else:
			if old_corpname.attrib is None:
				pass
			else:
				corpname_element.attrib = old_corpname.attrib
	if CSheet.find('Repository/MARCEncoding').text:
		corpname_element.set('encodinganalog', CSheet.find('Repository/MARCEncoding').text)
	if CSheet.find('Repository/Identifier').text:
		if version == "ead3":
			corpname_element.set('identifier', CSheet.find('Repository/Identifier').text)
		else:
			corpname_element.set('id', CSheet.find('Repository/Identifier').text)
	if CSheet.find('Repository/Relator').text:
		if version == "ead3":
			corpname_element.set('relator', CSheet.find('Repository/Relator').text)
		else:
			corpname_element.set('role', CSheet.find('Repository/Relator').text)
	if CSheet.find('Repository/Normal').text:
		corpname_element.set('normal', CSheet.find('Repository/Normal').text)
	if CSheet.find('Repository/Source').text:
		corpname_element.set('source', CSheet.find('Repository/Source').text)
	if CSheet.find('Repository/AddressLine') is None:
		pass
	else:
		if CSheet.find('Repository/AddressLine').text:
			address_element = ET.Element('address')
			repository_element.append(address_element)
			if old_address is None:
				pass
			else:
				if old_address.attrib is None:
					pass
				else:
					repository_element.attrib = old_address.attrib
	for rep in CSheet.find('Repository'):
		if rep.tag == "AddressLine":
			addressline_element = ET.Element('addressline')
			address_element.append(addressline_element)
			addressline_element.text = rep.text