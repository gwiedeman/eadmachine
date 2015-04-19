# module for <archdesc> elements matched to lower levels of the <dsc> via a unitid
import xml.etree.cElementTree as ET
from mixed_content import mixed_content
from messages import error
import globals

def archdesc_lower(cmpnt_root, CSheet, version):
	
	access_use_lower(cmpnt_root, CSheet, "accessrestrict", "Access")
	simple_lower(cmpnt_root, CSheet, "accruals", "Accruals", "Accrual")
	simple_lower(cmpnt_root, CSheet, "altformavail", "AlternateForms", "Alternative")
	simple_lower(cmpnt_root, CSheet, "appraisal", "AppraisalInfo", "Appraisal")
	simple_lower(cmpnt_root, CSheet, "bioghist", "LowerLevelHist", "Details")
	simple_lower(cmpnt_root, CSheet, "custodhist", "CustodialHistory", "Event")
	simple_lower(cmpnt_root, CSheet, "legalstatus", "LegalStatus", "Status")
	simple_lower(cmpnt_root, CSheet, "originalsloc", "LocationOriginals", "Location")
	simple_lower(cmpnt_root, CSheet, "otherfindaid", "OtherFindingAids", "Other")
	simple_lower(cmpnt_root, CSheet, "phystech", "PhysicalTechnical", "Details")
	simple_lower(cmpnt_root, CSheet, "processinfo", "ProcessingInformation", "Details")
	
	#limits lower level scope notes to file/item level
	if cmpnt_root.find('c') is None and cmpnt_root.find('c01') is None and cmpnt_root.find('c02') is None and cmpnt_root.find('c03') is None and cmpnt_root.find('c04') is None and cmpnt_root.find('c05') is None and cmpnt_root.find('c06') is None and cmpnt_root.find('c07') is None and cmpnt_root.find('c08') is None and cmpnt_root.find('c09') is None and cmpnt_root.find('c10') is None and cmpnt_root.find('c11') is None and cmpnt_root.find('c12') is None:
		simple_lower(cmpnt_root, CSheet, "scopecontent", "LowerLevelScope", "Details")
	
	simple_lower(cmpnt_root, CSheet, "separatedmaterial", "SeparatedMaterial", "Material")
	access_use_lower(cmpnt_root, CSheet, "userestrict", "UseRestrictions")
	
	
	#<acquisitions>
	if cmpnt_root.find('acquisitions') is None:
		pass
	else:
		Acquis_element = ET.Element('Acquis')
		CSheet.find(SheetElement).append(Acquis_element)
		UnitID_element = ET.Element('UnitID')
		Acquis_element.append(UnitID_element)
		Event_element = ET.Element('Event')
		Acquis_element.append(Event_element)
		Date_element = ET.Element('Date')
		Acquis_element.append(Date_element)
		DateNormal_element = ET.Element('DateNormal')
		Acquis_element.append(DateNormal_element)
		if cmpnt_root.find('did/unitid') is None:
			if "id" in cmpnt_root.attrib:
				UnitID_element.text = cmpnt_root.attrib['id']
			else:
				if "id" in cmpnt_root.find('did').attrib:
					UnitID_element.text = cmpnt_root.find('did').attrib['id']
		else:
			UnitID_element.text = cmpnt_root.find('did/unitid').text
		if cmpnt_root.find('acquisitions').find('p') is None:
			if cmpnt_root.find('acquisitions').find('note') is None:
				pass
			else:
				Acquis_element.text = mixed_content(cmpnt_root.find('acquisitions').find('note'))
		else:
			Acquis_element.text = mixed_content(cmpnt_root.find('acquisitions').find('p'))
		if cmpnt_root.find('acquisitions').iter('date') is None:
			pass
		else:
			Date_element.text = cmpnt_root.find('acquisitions').iter('date').text
			if "normal" in cmpnt_root.find('acquisitions').iter('date').attrib:
				DateNormal_element.text = cmpnt_root.find('acquisitions').iter('date').attrib['normal']
			
	#<controlaccess>
	if cmpnt_root.find('controlaccess') is None:
		pass
	else:
		for subpoint in cmpnt_root.find('controlaccess'):
			if subpoint.tag == "p":
				pass
			elif subpoint.tag == "head":
				pass
			else:
				AccessPoint_element = ET.Element('AccessPoint')
				CSheet.find('ControlledAccess').append(AccessPoint_element)
				UnitID_element = ET.Element('UnitID')
				AccessPoint_element.append(UnitID_element)
				ElementName_element = ET.Element('ElementName')
				AccessPoint_element.append(ElementName_element)
				MARCEncoding_element = ET.Element('MARCEncoding')
				AccessPoint_element.append(MARCEncoding_element)
				Part_element = ET.Element('Part')
				AccessPoint_element.append(Part_element)
				Identifier_element = ET.Element('Identifier')
				AccessPoint_element.append(Identifier_element)
				Relator_element = ET.Element('Relator')
				AccessPoint_element.append(Relator_element)
				Normal_element = ET.Element('Normal')
				AccessPoint_element.append(Normal_element)
				Source_element = ET.Element('Source')
				AccessPoint_element.append(Source_element)
				ElementName_element.text = subpoint.tag
				if cmpnt_root.find('did/unitid') is None:
					if "id" in cmpnt_root.attrib:
						UnitID_element.text = cmpnt_root.attrib['id']
					else:
						if "id" in cmpnt_root.find('did').attrib:
							UnitID_element.text = cmpnt_root.find('did').attrib['id']
				else:
					UnitID_element.text = cmpnt_root.find('did/unitid').text				
				if "encodinganalog" in subpoint.attrib:
					MARCEncoding_element.text = subpoint.attrib['encodinganalog']
				if "normal" in subpoint.attrib:
					Normal_element.text = subpoint.attrib['normal']
				if "source" in subpoint.attrib:
					Source_element.text = subpoint.attrib['source']
				if version == "ead2002":
					if "id" in subpoint.attrib:
						Identifier_element.text = subpoint.attrib['id']
					if "role" in subpoint.attrib:
						Relator_element.text = subpoint.attrib['role']
					Part_element.text = mixed_content(subpoint)
				else:
					if "identifier " in subpoint.attrib:
						Identifier_element.text = subpoint.attrib['identifier ']
					if "relator" in subpoint.attrib:
						Relator_element.text = subpoint.attrib['relator']
					if subpoint.text:
						Part_element.text = subpoint.text
					for controlled in subpoint:
						if controlled.tag == "part":
							if Part_element.text:							
								Part_element.text = Part_element.text + controlled.text
							else:
								Part_element.text = controlled.text
								
	#<relatedmaterial>
	if cmpnt_root.find('relatedmaterial') is None:
		pass
	else:
		if cmpnt_root.find('relatedmaterial/bibref') is None:
			pass
		else:
			for bibref in cmpnt_root.find('relatedmaterial'):
				if bibref.tag == "bibref":
					Publication_element = ET.Element('Publication')
					CSheet.find('RelatedPublications').append(Publication_element)
					Author_element = ET.Element('Author')
					Publication_element.append(Author_element)
					Title_element = ET.Element('Title')
					Publication_element.append(Title_element)
					Citation_element = ET.Element('Citation')
					Publication_element.append(Citation_element)
					Date_element = ET.Element('Date')
					Publication_element.append(Date_element)
					NormalDate_element = ET.Element('NormalDate')
					Publication_element.append(NormalDate_element)
					Reference_element = ET.Element('Reference')
					Publication_element.append(Reference_element)
					ReferenceLink_element = ET.Element('ReferenceLink')
					Publication_element.append(ReferenceLink_element)
					if bibref.find('persname') is None and bibref.find('corpname') is None and bibref.find('famname') is None and bibref.find('name') is None:
						if bibref.text:
							Author_element.text = bibref.text
					else:
						if bibref.find('persname') is None:
							pass
						else:
							Author_element.text = bibref.find('persname').text
						if bibref.find('corpname') is None:
							pass
						else:
							Author_element.text = bibref.find('corpname').text
						if bibref.find('famname') is None:
							pass
						else:
							Author_element.text = bibref.find('famname').text
						if bibref.find('name') is None:
							pass
						else:
							Author_element.text = bibref.find('name').text
					if bibref.find('title') is None:
						Citation_element.text = mixed_content(bibref)
					else:
						Title_element.text = mixed_content(bibref.find('title'))
						if bibref.find('title').tail:
							Citation_element.text = bibref.find('title').tail
					if bibref.find('date') is None:
						pass
					else:
						Date_element.text = bibref.find('date').text
						if 'normal' in bibref.find('date').attrib:
							NormalDate_element.text = bibref.find('date').attrib['normal']
					if bibref.find('ref') is None:
						pass
					else:
						Reference_element.text = mixed_content(bibref.find('ref'))
						if 'href' in bibref.find('ref').attrib:
							ReferenceLink_element.text = bibref.find('ref').attrib['href']						
		if cmpnt_root.find('relatedmaterial/archref') is None:
			pass
		else:
			for archref in cmpnt_root.find('relatedmaterial'):
				if archref.tag == "archref":
					Manuscript_element = ET.Element('Manuscript')
					CSheet.find('RelatedManuscripts').append(Manuscript_element)
					Collection_element = ET.Element('Collection')
					Manuscript_element.append(Collection_element)
					UnitID_element = ET.Element('UnitID')
					Manuscript_element.append(UnitID_element)
					UnitTitle_element = ET.Element('UnitTitle')
					Manuscript_element.append(UnitTitle_element)
					Date_element = ET.Element('Date')
					Manuscript_element.append(Date_element)
					NormalDate_element = ET.Element('NormalDate')
					Manuscript_element.append(NormalDate_element)
					Reference_element = ET.Element('Reference')
					Manuscript_element.append(Reference_element)
					ReferenceLink_element = ET.Element('ReferenceLink')
					Manuscript_element.append(ReferenceLink_element)
					if archref.find('persname') is None and archref.find('corpname') is None and archref.find('famname') is None and archref.find('name') is None:
						if archref.text:
							Collection_element.text = archref.text
					else:
						if archref.find('persname') is None:
							pass
						else:
							Collection_element.text = archref.find('persname').text
						if archref.find('corpname') is None:
							pass
						else:
							Collection_element.text = archref.find('corpname').text
						if archref.find('famname') is None:
							pass
						else:
							Collection_element.text = archref.find('famname').text
						if archref.find('name') is None:
							pass
						else:
							Collection_element.text = archref.find('name').text
					if archref.find('title') is None:
						UnitTitle_element.text = mixed_content(archref)
					else:
						UnitTitle_element.text = mixed_content(archref.find('title'))
						if archref.find('title').tail:
							UnitID_element.text = archref.find('title').tail
					if archref.find('date') is None:
						pass
					else:
						Date_element.text = archref.find('date').text
						if 'normal' in archref.find('date').attrib:
							NormalDate_element.text = archref.find('date').attrib['normal']
					if archref.find('ref') is None:
						pass
					else:
						Reference_element.text = mixed_content(archref.find('ref'))
						if 'href' in archref.find('ref').attrib:
							ReferenceLink_element.text = archref.find('ref').attrib['href']
	
####################################################################################################
	
def access_use_lower(cmpnt_root, CSheet, ElementName, SheetElement):
	if cmpnt_root.find(ElementName) is None:
		pass
	else:
		SpecificRestriction_element = ET.Element('SpecificRestriction')
		CSheet.find(SheetElement).find('SpecificMaterialRestrictions').append(SpecificRestriction_element)
		UnitID_element = ET.Element('UnitID')
		SpecificRestriction_element.append(UnitID_element)
		Material_element = ET.Element('Material')
		SpecificRestriction_element.append(Material_element)
		Restriction_element = ET.Element('Restriction')
		SpecificRestriction_element.append(Restriction_element)
		if cmpnt_root.find('did/unitid') is None:
			if "id" in cmpnt_root.attrib:
				UnitID_element.text = cmpnt_root.attrib['id']
			else:
				if "id" in cmpnt_root.find('did').attrib:
					UnitID_element.text = cmpnt_root.find('did').attrib['id']
		else:
			UnitID_element.text = cmpnt_root.find('did/unitid').text
		
		if cmpnt_root.find('did/unittitle') is None:
			pass
		else:
			Material_element.text = mixed_content(cmpnt_root.find('did/unittitle'))
		
		if cmpnt_root.find(ElementName).find('p') is None:
			if cmpnt_root.find(ElementName).find('note') is None:
				pass
			else:
				Restriction_element.text = mixed_content(cmpnt_root.find(ElementName).find('note'))
		else:
			Restriction_element.text = mixed_content(cmpnt_root.find(ElementName).find('p'))

			
def simple_lower(cmpnt_root, CSheet, ElementName, SheetElement, ElementChild):
	if cmpnt_root.find(ElementName) is None:
		pass
	else:
		ElementChild_element = ET.Element(ElementChild)
		CSheet.find(SheetElement).append(ElementChild_element)
		UnitID_element = ET.Element('UnitID')
		ElementChild_element.append(UnitID_element)
		Text_element = ET.Element('Text')
		ElementChild_element.append(Text_element)
		
		if cmpnt_root.find('did/unitid') is None:
			if "id" in cmpnt_root.attrib:
				UnitID_element.text = cmpnt_root.attrib['id']
			else:
				if "id" in cmpnt_root.find('did').attrib:
					UnitID_element.text = cmpnt_root.find('did').attrib['id']
		else:
			UnitID_element.text = cmpnt_root.find('did/unitid').text
		
		
		if cmpnt_root.find(ElementName).find('p') is None:
			if cmpnt_root.find(ElementName).find('note') is None:
				pass
			else:
				Text_element.text = mixed_content(cmpnt_root.find(ElementName).find('note'))
		else:
			Text_element.text = mixed_content(cmpnt_root.find(ElementName).find('p'))