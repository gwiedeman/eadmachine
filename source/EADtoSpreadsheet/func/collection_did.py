# module for the collection-level <did>
import xml.etree.cElementTree as ET
import globals
from messages import error
from mixed_content import mixed_content

def collection_did(did_root, CSheet, version):
	
	from unitdate import unitdate
	unitdate(did_root, CSheet, "collection", version)
	
	# Abstract for both EAD 2002 and EAD3
	if did_root.find('abstract') is None:
		pass
	else:
		CSheet.find('Abstract').text = mixed_content(did_root.find('abstract'))
		
	# Collection Language Material
	from collection_language import language
	language(did_root, CSheet, version)
	
	# Origination Section
	if did_root.find('origination') is None:
		pass
	else:
		CSheet.find('Origins').clear()
		for creator in did_root.find('origination'):
			Origination_element = ET.Element('Origination')
			CSheet.find('Origins').append(Origination_element)
			ElementName_element = ET.Element('ElementName')
			Origination_element.append(ElementName_element)
			MARCEncoding_element = ET.Element('MARCEncoding')
			Origination_element.append(MARCEncoding_element)
			Part_element = ET.Element('Part')
			Origination_element.append(Part_element)
			Identifier_element = ET.Element('Identifier')
			Origination_element.append(Identifier_element)
			Relator_element = ET.Element('Relator')
			Origination_element.append(Relator_element)
			Normal_element = ET.Element('Normal')
			Origination_element.append(Normal_element)
			Source_element = ET.Element('Source')
			Origination_element.append(Source_element)
			ElementName_element.text = creator.tag
			if 'encodinganalog' in creator.attrib:
				MARCEncoding_element.text = creator.attrib['encodinganalog']
			Part_element.text = creator.text
			if version == "ead2002":
				if 'id' in creator.attrib:
					Identifier_element.text = creator.attrib['id']
				if 'role' in creator.attrib:
					Relator_element.text = creator.attrib['role']
			else:
				if 'identifier' in creator.attrib:
					Identifier_element.text = creator.attrib['identifier']
				if 'relator' in creator.attrib:
					Relator_element.text = creator.attrib['relator']
			if 'normal' in creator.attrib:
				Normal_element.text = creator.attrib['normal']
			if 'source' in creator.attrib:
				Source_element.text = creator.attrib['source']
	
	#PhysicalDescription section
	from physdesc import simple
	from physdesc import structured
	
	if did_root.find('physdesc') is None:
		pass
	else:
		if version == "ead2002":
			simple(did_root, CSheet, version)
		else:
			if did_root.find('physdescstructured') is None and did_root.find('physdescstructuredset') is None:
				simple(did_root, CSheet, version)
			else:
				structured(did_root, CSheet)
				
	# Physical Location Section, same for both EAD2002 and EAD3
	if did_root.find('physloc') is None:
		pass
	else:
		CSheet.find('PhysicalLocationSet').clear()
		for physloc in did_root:
			if physloc.tag == "physloc":
				PhysicalLocation_element = ET.Element('PhysicalLocation')
				CSheet.find('PhysicalLocationSet').append(PhysicalLocation_element)
				Location_element = ET.Element('Location')
				PhysicalLocation_element.append(Location_element)
				Audience_element = ET.Element('Audience')
				PhysicalLocation_element.append(Audience_element)
				Location_element.text = mixed_content(physloc)
				if 'audience' in physloc.attrib:
					Audience_element.text = physloc.attrib['audience']
	
	# Repository Section
	if did_root.find('repository') is None:
		pass
	else:
		if did_root.find('repository/corpname') is None:
			if did_root.find('repository/famname') is None:
				if did_root.find('repository/name') is None:
					if did_root.find('repository/persname') is None:
						if did_root.find('repository').text:
							CSheet.find('Repository/RepositoryName').text = mixed_content(did_root.find('repository'))
							if 'id' in did_root.find('repository').attrib:
								CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
					else:
						CSheet.find('Repository/ElementName').text = "persname"
						CSheet.find('Repository/RepositoryName').text = mixed_content(did_root.find('repository/persname'))
						if "encodinganalog" in did_root.find('repository/persname').attrib:
							CSheet.find('Repository/MARCEncoding').text = did_root.find('repository/persname').attrib['encodinganalog']
						if "source" in did_root.find('repository/persname').attrib:
							CSheet.find('Source').text = did_root.find('repository/persname').attrib['source']
						if "normal" in did_root.find('repository/persname').attrib:
							CSheet.find('Repository/Normal').text = did_root.find('repository/persname').attrib['normal']
						if version == "ead2002":
							if "id" in did_root.find('repository/persname').attrib:
								CSheet.find('Repository/Identifier').text = did_root.find('repository/persname').attrib['id']
							else:
								if 'id' in did_root.find('repository').attrib:
									CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
							if "role" in did_root.find('repository/persname').attrib:
								CSheet.find('Repository/Relator').text = did_root.find('repository/persname').attrib['role']
						else:
							if "identifier" in did_root.find('repository/persname').attrib:
								CSheet.find('Repository/Identifier').text = did_root.find('repository/persname').attrib['identifier']
							else:
								if 'id' in did_root.find('repository').attrib:
									CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
							if "relator" in did_root.find('repository/persname').attrib:
								CSheet.find('Repository/Relator').text = did_root.find('repository/persname').attrib['relator']
				else:
					CSheet.find('Repository/ElementName').text = "name"
					CSheet.find('Repository/RepositoryName').text = mixed_content(did_root.find('repository/name'))
					if "encodinganalog" in did_root.find('repository/name').attrib:
						CSheet.find('Repository/MARCEncoding').text = did_root.find('repository/name').attrib['encodinganalog']
					if "source" in did_root.find('repository/name').attrib:
						CSheet.find('Repository/Source').text = did_root.find('repository/name').attrib['source']
					if "normal" in did_root.find('repository/name').attrib:
						CSheet.find('Repository/Normal').text = did_root.find('repository/name').attrib['normal']
					if version == "ead2002":
						if "id" in did_root.find('repository/name').attrib:
							CSheet.find('Repository/Identifier').text = did_root.find('repository/name').attrib['id']
						else:
							if 'id' in did_root.find('repository').attrib:
								CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
						if "role" in did_root.find('repository/name').attrib:
							CSheet.find('Repository/Relator').text = did_root.find('repository/name').attrib['role']
					else:
						if "identifier" in did_root.find('repository/name').attrib:
							CSheet.find('Repository/Identifier').text = did_root.find('repository/name').attrib['identifier']
						else:
							if 'id' in did_root.find('repository').attrib:
								CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
						if "relator" in did_root.find('repository/name').attrib:
							CSheet.find('Repository/Relator').text = did_root.find('repository/name').attrib['relator']
			else:
				CSheet.find('Repository/ElementName').text = "famname"
				CSheet.find('Repository/RepositoryName').text = mixed_content(did_root.find('repository/famname'))
				if "encodinganalog" in did_root.find('repository/famname').attrib:
					CSheet.find('Repository/MARCEncoding').text = did_root.find('repository/famname').attrib['encodinganalog']
				if "source" in did_root.find('repository/famname').attrib:
					CSheet.find('Repository/Source').text = did_root.find('repository/famname').attrib['source']
				if "normal" in did_root.find('repository/famname').attrib:
					CSheet.find('Repository/Normal').text = did_root.find('repository/famname').attrib['normal']
				if version == "ead2002":
					if "id" in did_root.find('repository/famname').attrib:
						CSheet.find('Repository/Identifier').text = did_root.find('repository/famname').attrib['id']
					else:
						if 'id' in did_root.find('repository').attrib:
							CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
					if "role" in did_root.find('repository/famname').attrib:
						CSheet.find('Repository/Relator').text = did_root.find('repository/famname').attrib['role']
				else:
					if "identifier" in did_root.find('repository/famname').attrib:
						CSheet.find('Repository/Identifier').text = did_root.find('repository/famname').attrib['identifier']
					else:
						if 'id' in did_root.find('repository').attrib:
							CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
					if "relator" in did_root.find('repository/famname').attrib:
						CSheet.find('Repository/Relator').text = did_root.find('repository/famname').attrib['relator']
		else:
			CSheet.find('Repository/ElementName').text = "corpname"
			CSheet.find('Repository/RepositoryName').text = mixed_content(did_root.find('repository/corpname'))
			if "encodinganalog" in did_root.find('repository/corpname').attrib:
				CSheet.find('Repository/MARCEncoding').text = did_root.find('repository/corpname').attrib['encodinganalog']
			if "source" in did_root.find('repository/corpname').attrib:
				CSheet.find('Repository/Source').text = did_root.find('repository/corpname').attrib['source']
			if "normal" in did_root.find('repository/corpname').attrib:
				CSheet.find('Repository/Normal').text = did_root.find('repository/corpname').attrib['normal']
			if version == "ead2002":
				if "id" in did_root.find('repository/corpname').attrib:
					CSheet.find('Repository/Identifier').text = did_root.find('repository/corpname').attrib['id']
				else:
					if 'id' in did_root.find('repository').attrib:
						CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
				if "role" in did_root.find('repository/corpname').attrib:
					CSheet.find('Repository/Relator').text = did_root.find('repository/corpname').attrib['role']
			else:
				if "identifier" in did_root.find('repository/corpname').attrib:
					CSheet.find('Repository/Identifier').text = did_root.find('repository/corpname').attrib['identifier']
				else:
					if 'id' in did_root.find('repository').attrib:
						CSheet.find('Repository/Identifier').text = did_root.find('repository').attrib['id']
				if "relator" in did_root.find('repository/corpname').attrib:
					CSheet.find('Repository/Relator').text = did_root.find('repository/corpname').attrib['relator']
		if did_root.find('repository/subarea') is None:
			pass
		else:
			for subarea in did_root.find('repository'):
				if subarea.tag == "subarea":
					AddressLine_element = ET.Element('AddressLine')
					CSheet.find('Repository').append(AddressLine_element)
					AddressLine_element.text = subarea.text
		if did_root.find('repository/address') is None:
			pass
		else:
			for addressline in did_root.find('repository/address'):
				AddressLine_element = ET.Element('AddressLine')
				CSheet.find('Repository').append(AddressLine_element)
				AddressLine_element.text = addressline.text