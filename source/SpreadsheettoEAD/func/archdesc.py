# module for the <archdesc/> or collection-level description
import xml.etree.cElementTree as ET
from archdescsimple import archdescsimple
from access_use_restrict import access_use_restrict
import globals
import wx



def archdesc(arch_root, CSheet, version, input_data):
	from wx.lib.pubsub import pub
	
	#update GUI progress bar
	if "ask_gui" in globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <archdesc>...")
	
	#collection-level did
	if "ask_gui" in globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Writing collection-level <did>...")
	from collection_did import collection_did
	cdid_root = arch_root.find('did')
	collection_did(cdid_root, CSheet, version)
	
	
	if "ask_gui" in globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <archdesc> elements...")
	
	#Access Restrictions Section
	if "add_accessrestrict" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	access_use_restrict(arch_root, CSheet.find('Access'), "accessrestrict", "Access", add)
			
	#Accruals Section
	if "add_accruals" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "accruals", CSheet.find('Accruals'), CSheet.find('Accruals/Accrual'), add)
		
	#Acquisitions Information Section
	if CSheet.find('AcquisitionInfo/Acquis/Event') is None:
		pass
	else:
		if CSheet.find('AcquisitionInfo/Acquis/Event').text:
			if arch_root.find('acqinfo') is None:
				if "add_acq" in globals.new_elements or "add-all" in globals.add_all:
					acq_element = ET.Element('acqinfo')
					arch_root.insert(1, acq_element)
					count = 0
					for acquis in CSheet.find('AcquisitionInfo'):
						if acquis.find('Event').text and acquis.find('Date').text:
							count = count + 1
					if count > 1:
						chronlist_element = ET.Element('chronlist')
						arch_root.find('acqinfo').append(chronlist_element)
						for acquis in CSheet.find('AcquisitionInfo'):
							if acquis.find('Event').text:
								chronitem_element = ET.Element('chronitem')
								chronlist_element.append(chronitem_element)
								event_element = ET.Element('event')
								chronitem_element.append(event_element)
								event_element.text = acquis.find('Event').text
								if version == "ead3":
									if acquis.find('Date').text:
										from date import basic_date
										chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
								else:
									date_element = ET.Element('date')
									if acquis.find('Date').text:
										chronitem_element.append(date_element)
										date_element.text = acquis.find('Date').text
										if acquis.find('DateNormal').text:
											date_element.set('normal', acquis.find('DateNormal').text)
										else:
											date_element.set('normal', acquis.find('Date').text)
					else:
						for acquis in CSheet.find('AcquisitionInfo'):
							if acquis.find('Event').text:
								p_element = ET.Element('p')
								arch_root.find('acqinfo').append(p_element)
								p_element.text = acquis.find('Event').text
								date_element = ET.Element('date')
								if acquis.find('Date').text:
									p_element.append(date_element)
									date_element.text = acquis.find('Date').text
									if acquis.find('DateNormal').text:
										date_element.set('normal', acquis.find('DateNormal').text)
									else:
										date_element.set('normal', acquis.find('Date').text)
			else:
				old_acquis = arch_root.find('acqinfo').attrib
				old_head = arch_root.find('acqinfo/head')
				arch_root.find('acqinfo').clear()
				if old_acquis is None:
					pass
				else:
					arch_root.find('acqinfo').attrib = old_acquis
				if old_head is None:
					pass
				else:
					arch_root.find('acqinfo').append(old_head)
				count = 0
				for acquis in CSheet.find('AcquisitionInfo'):
					if acquis.find('Event').text and acquis.find('Date').text:
						count = count + 1
				if count > 1:
					chronlist_element = ET.Element('chronlist')
					arch_root.find('acqinfo').append(chronlist_element)
					for acquis in CSheet.find('AcquisitionInfo'):
						if acquis.find('Event').text:
							chronitem_element = ET.Element('chronitem')
							chronlist_element.append(chronitem_element)
							event_element = ET.Element('event')
							chronitem_element.append(event_element)
							event_element.text = acquis.find('Event').text
							if version == "ead3":
								if acquis.find('Date').text:
									from date import basic_date
									chronitem_element.append(basic_date(acquis.find('Date').text, acquis.find('DateNormal').text, 'inclusive'))
							else:
								date_element = ET.Element('date')
								if acquis.find('Date').text:
									chronitem_element.append(date_element)
									date_element.text = acquis.find('Date').text
									if acquis.find('DateNormal').text:
										date_element.set('normal', acquis.find('DateNormal').text)
									else:
										date_element.set('normal', acquis.find('Date').text)
				else:
					for acquis in CSheet.find('AcquisitionInfo'):
						if acquis.find('Event').text:
							p_element = ET.Element('p')
							arch_root.find('acqinfo').append(p_element)
							p_element.text = acquis.find('Event').text
							date_element = ET.Element('date')
							if acquis.find('Date').text:
								p_element.append(date_element)
								date_element.text = acquis.find('Date').text
								if acquis.find('DateNormal').text:
									date_element.set('normal', acquis.find('DateNormal').text)
								else:
									date_element.set('normal', acquis.find('Date').text)
		else:
			for empty_acquis in arch_root:
				if empty_acquis.tag == "acqinfo":
					arch_root.remove(empty_acquis)
					
	# Alternate Forms Available Section <altformavail>
	if "add_altforms" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "altformavail", CSheet.find('AlternateForms'), CSheet.find('AlternateForms/Alternative'), add)
	
	# Appraisal Section <appraisal>
	if "add_appraisal" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "appraisal", CSheet.find('AppraisalInfo'), CSheet.find('AppraisalInfo/Appraisal'), add)
	
	# Arrangement Section <arrangement>
	if "add_arrange" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	if arch_root.find('arrangement/list') is None:
		arrange_list = False
	else:
		arrange_list = True
	archdescsimple(arch_root, "arrangement", CSheet.find('CollectionArrangement'), CSheet.find('CollectionArrangement/Arrangement'), add)
	if arrange_list == True:
		if CSheet.find('CollectionMap/Component/ComponentName').text:
			if CSheet.find('CollectionMap/Component/ComponentName').text.lower() == "no series" or CSheet.find('CollectionMap/Component/ComponentName').text.lower() == "noseries":
				pass
			else:
				list_element = ET.Element('list')
				if arch_root.find('arrangement') is None:
					arrangement_element = ET.Element('arrangement')
					arr_index =  arch_root.getchildren().index(arch_root.find('dsc')) - 1
					arch_root.insert(arr_index, arrangement_element)
					arrangement_element.append(list_element)
				else:
					arch_root.find('arrangement').append(list_element)
				list_element.set('type', 'simple')
				for cmpnt in CSheet.find('CollectionMap'):
					if cmpnt.find('ComponentName').text:
						item_element = ET.Element('item')
						list_element.append(item_element)
						if cmpnt.find('ComponentLevel').text == "1":
							emph_element = ET.Element('emph')
							item_element.append(emph_element)
							emph_element.set('render', 'bold')
							if cmpnt.find('ComponentNumber').text:
								emph_element.text = "Series " + cmpnt.find('ComponentNumber').text + " - " + cmpnt.find('ComponentName').text
							else: 
								emph_element.text = "Series" + " - " + cmpnt.find('ComponentName').text
							cmpnt_num = cmpnt.find('ComponentNumber').text
							for ComponentSheet in input_data:
								if ComponentSheet.find('SeriesNumber') is None:
									pass
								elif ComponentSheet.find('SeriesNumber').text == cmpnt_num:
									cmpnt_info = ComponentSheet
									if cmpnt_info.find('SeriesDate').text:
										emph_element.tail = ", " + cmpnt_info.find('SeriesDate').text
						else:
							if cmpnt.find('ComponentNumber').text:
								item_element.text = "Subseries " + cmpnt.find('ComponentNumber').text + ": " + cmpnt.find('ComponentName').text
							else:
								item_element.text = "Subseries" + ": " + cmpnt.find('ComponentName').text
							cmpnt_num = cmpnt.find('ComponentNumber').text
							for ComponentSheet in input_data:
								if ComponentSheet.find('SeriesNumber') is None:
									pass
								elif ComponentSheet.find('SeriesNumber').text == cmpnt_num:
									cmpnt_info = ComponentSheet
									if cmpnt_info.find('SeriesDate').text:
										emph_element.tail = ", " + cmpnt_info.find('SeriesDate').text
	
	# Bibliography Section <bibliography>
	if CSheet.find('PublicationBibliography/Publication/Title').text or CSheet.find('ManuscriptBibliography/Manuscript/UnitTitle').text:
		if arch_root.find('bibliography') is None:
			if "add_biblio" in globals.new_elements or "add-all" in globals.add_all:
				biblio_element = ET.Element('bibliography')
				biblio_index = arch_root.getchildren().index(arch_root.find('dsc'))
				arch_root.insert(biblio_index, biblio_element)
				if CSheet.find('BibliographyNote').text:
					p_element = ET.Element('p')
					biblio_element.append(p_element)
					p_element.text = CSheet.find('BibliographyNote').text
				for pub in CSheet.find('PublicationBibliography'):
					if pub.find('Author').text or pub.find('Title').text or pub.find('Citation').text:
						bibref_element = ET.Element('bibref')
						biblio_element.append(bibref_element)
						if pub.find('Author').text:
							bibref_element.text = pub.find('Author').text + ", "
						if pub.find('Title').text:
							title_element = ET.Element('title')
							bibref_element.append(title_element)
							title_element.text = pub.find('Title').text
						if pub.find('Citation').text:
							title_element.tail = " " + pub.find('Citation').text + ", "
						if pub.find('Date').text:
							date_element = ET.Element('date')
							bibref_element.append(date_element)
							date_element.text = pub.find('Date').text
							if pub.find('NormalDate').text:
								date_element.set("normal", pub.find('NormalDate').text)
						if pub.find('Reference').text:
							ref_element = ET.Element('ref')
							bibref_element.append(ref_element)
							ref_element.text = pub.find('Reference').text
							if pub.find('ReferenceLink').text:
								ref_element.set('href', pub.find('ReferenceLink').text)
				for man in CSheet.find('ManuscriptBibliography'):
					if man.find('Collection').text or man.find('UnitID').text or man.find('UnitID').text:
						archref_element = ET.Element('archref')
						arch_root.find('bibliography').append(archref_element)
						if man.find('Collection').text:
							archref_element.text = man.find('Collection').text + ", "
						if man.find('UnitTitle').text:
							title_element = ET.Element('title')
							archref_element.append(title_element)
							title_element.text = man.find('UnitTitle').text
						if man.find('UnitID').text:
							title_element.tail = " " + man.find('UnitID').text + ", "
						if man.find('Date').text:
							date_element = ET.Element('date')
							archref_element.append(date_element)
							date_element.text = man.find('Date').text
							if man.find('NormalDate').text:
								date_element.set("normal", man.find('NormalDate').text)
						if man.find('Reference').text:
							ref_element = ET.Element('ref')
							archref_element.append(ref_element)
							ref_element.text = man.find('Reference').text
							if man.find('ReferenceLink').text:
								ref_element.set('href', man.find('ReferenceLink').text)
		else:
			old_biblio = arch_root.find('bibliography').attrib
			old_head = arch_root.find('bibliography/head')
			arch_root.find('bibliography').clear()
			if old_biblio is None:
				pass
			else:
				arch_root.find('bibliography').attrib = old_biblio
			if old_head is None:
				pass
			else:
				arch_root.find('bibliography').append(old_head)
			if CSheet.find('BibliographyNote').text:
				p_element = ET.Element('p')
				arch_root.find('bibliography').append(p_element)
				p_element.text = CSheet.find('BibliographyNote').text
			for pub in CSheet.find('PublicationBibliography'):
				if pub.find('Author').text or pub.find('Title').text or pub.find('Citation').text:
					bibref_element = ET.Element('bibref')
					arch_root.find('bibliography').append(bibref_element)
					if pub.find('Author').text:
						bibref_element.text = pub.find('Author').text + ", "
					if pub.find('Title').text:
						title_element = ET.Element('title')
						bibref_element.append(title_element)
						title_element.text = pub.find('Title').text
					if pub.find('Citation').text:
						title_element.tail = " " + pub.find('Citation').text + ", "
					if pub.find('Date').text:
						date_element = ET.Element('date')
						bibref_element.append(date_element)
						date_element.text = pub.find('Date').text
						if pub.find('NormalDate').text:
							date_element.set("normal", pub.find('NormalDate').text)
					if pub.find('Reference').text:
						ref_element = ET.Element('ref')
						bibref_element.append(ref_element)
						ref_element.text = pub.find('Reference').text
						if pub.find('ReferenceLink').text:
							ref_element.set('href', pub.find('ReferenceLink').text)
			for man in CSheet.find('ManuscriptBibliography'):
				if man.find('Collection').text or man.find('UnitID').text or man.find('UnitID').text:
					archref_element = ET.Element('archref')
					arch_root.find('bibliography').append(archref_element)
					if man.find('Collection').text:
						archref_element.text = man.find('Collection').text + ", "
					if man.find('UnitTitle').text:
						title_element = ET.Element('title')
						archref_element.append(title_element)
						title_element.text = man.find('UnitTitle').text
					if man.find('UnitID').text:
						title_element.tail = " " + man.find('UnitID').text + ", "
					if man.find('Date').text:
						date_element = ET.Element('date')
						archref_element.append(date_element)
						date_element.text = man.find('Date').text
						if man.find('NormalDate').text:
							date_element.set("normal", man.find('NormalDate').text)
					if man.find('Reference').text:
						ref_element = ET.Element('ref')
						archref_element.append(ref_element)
						ref_element.text = man.find('Reference').text
						if man.find('ReferenceLink').text:
							ref_element.set('href', man.find('ReferenceLink').text)
	else:
		old_biblio_list = arch_root.findall('bibliography')
		for old_biblio in old_biblio_list:
			arch_root.remove(old_biblio)
						
	# Biographical or Administrative History Section<bioghist>
	if CSheet.find('HistoricalNote/p') is None:
		pass
	else:
		if CSheet.find('HistoricalNote/p').text:
			if arch_root.find('bioghist') is None:
				if "add_bio" in globals.new_elements or "add-all" in globals.add_all:
					bio_element = ET.Element('bioghist')
					bio_index = arch_root.getchildren().index(arch_root.find('dsc'))
					arch_root.insert(bio_index, bio_element)
					if CSheet.find('HistoricalNoteTitle').text:
						head_element = ET.Element('head')
						arch_root.find('bioghist').append(head_element)
						head_element.text = CSheet.find('HistoricalNoteTitle').text
					for para in CSheet.find('HistoricalNote'):
						p_element = ET.Element('p')
						bio_element.append(p_element)
						p_element.text = para.text
			else:
				arch_root.find('bioghist').clear()
				if CSheet.find('HistoricalNoteTitle').text:
					head_element = ET.Element('head')
					arch_root.find('bioghist').append(head_element)
					head_element.text = CSheet.find('HistoricalNoteTitle').text
				for para in CSheet.find('HistoricalNote'):
					p_element = ET.Element('p')
					arch_root.find('bioghist').append(p_element)
					p_element.text = para.text
		else:
			old_hist_list = arch_root.findall('bioghist')
			for old_hist in old_hist_list:
				arch_root.remove(old_hist)
	
	# Controlled Access Headings <controlaccess>
	old_access = arch_root.find('controlaccess')
	if CSheet.find('ControlledAccess/AccessPoint/Part') is None or CSheet.find('ControlledAccess/AccessPoint/ElementName') is None:
		pass
	else:
		if CSheet.find('ControlledAccess/AccessPoint/Part').text and CSheet.find('ControlledAccess/AccessPoint/ElementName').text:
			if arch_root.find('controlaccess') is None:
				if "add_controlaccess" in globals.new_elements or "add-all" in globals.add_all:
					access_element = ET.Element('controlaccess')
					access_index = arch_root.getchildren().index(arch_root.find('dsc'))
					arch_root.insert(access_index, access_element)
					for access in CSheet.find('ControlledAccess'):
						if access.find('UnitID').text:
							pass
						else:
							if access.find('Part').text and access.find('ElementName').text:
								new_element = ET.Element(access.find('ElementName').text)
								access_element.append(new_element)
								if version == "ead2002":
									new_element.text = access.find('Part').text
								else:
									part_element = ET.Element('part')
									new_element.append(part_element)
									part_element.text = access.find('Part').text
								if access.find('MARCEncoding').text:
									new_element.set('encodinganalog', access.find('MARCEncoding').text)
								if access.find('Identifier').text:
									if version == "ead3":
										new_element.set('identifier', access.find('Identifier').text)
									else:
										new_element.set('id', access.find('Identifier').text)
								if access.find('Relator').text:
									if version == "ead3":
										new_element.set('relator', access.find('Relator').text)
									else:
										new_element.set('role', access.find('Relator').text)
								if access.find('Normal').text:
									new_element.set('normal', access.find('Normal').text)
								if access.find('Source').text:
									new_element.set('source', access.find('Source').text)
							else:
								if access.find('Part').text or access.find('ElementName').text:
									from messages import error
									error("All Access Headings must have both an Element Name and a Heading, headings without these fields will not be encoded.", False)
			else:
				old_access = arch_root.find('controlaccess').attrib
				old_access_list = arch_root.findall('controlaccess')
				for old_access_ele in old_access_list:
					arch_root.remove(old_access_ele)
				access_element = ET.Element('controlaccess')
				access_index = arch_root.getchildren().index(arch_root.find('dsc'))
				arch_root.insert(access_index, access_element)
				if old_access is None:
					pass
				else:
					access_element.attrib = old_access
				for access in CSheet.find('ControlledAccess'):
					if access.find('UnitID').text:
						pass
					else:
						if access.find('Part').text and access.find('ElementName').text:
							new_element = ET.Element(access.find('ElementName').text)
							access_element.append(new_element)
							if version == "ead2002":
								new_element.text = access.find('Part').text
							else:
								part_element = ET.Element('part')
								new_element.append(part_element)
								part_element.text = access.find('Part').text
							if access.find('MARCEncoding').text:
								new_element.set('encodinganalog', access.find('MARCEncoding').text)
							if access.find('Identifier').text:
								if version == "ead3":
									new_element.set('identifier', access.find('Identifier').text)
								else:
									new_element.set('id', access.find('Identifier').text)
							if access.find('Relator').text:
								if version == "ead3":
									new_element.set('relator', access.find('Relator').text)
								else:
									new_element.set('role', access.find('Relator').text)
							if access.find('Normal').text:
								new_element.set('normal', access.find('Normal').text)
							if access.find('Source').text:
									new_element.set('source', access.find('Source').text)
						else:
							if access.find('Part').text or access.find('ElementName').text:
								from messages import error
								error("All Access Headings must have both an Element Name and a Heading, headings without these fields will not be encoded.", False)
		else:
			old_ca_list = arch_root.findall('controlaccess')
			for old_ca in old_ca_list:
				arch_root.remove(old_ca)
		
	# Custodial History section <custodhist>
	if "add_custhistory" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "custodhist", CSheet.find('CustodialHistory'), CSheet.find('CustodialHistory/Event'), add)
	
	# Legal Status <legalstatus>
	if "add_legalstatus" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "legalstatus", CSheet.find('LegalStatus'), CSheet.find('LegalStatus/Status'), add)
	
	# Location of Originals when collection contains photocopies, etc. <originalsloc>
	if "add_originalsloc" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "originalsloc", CSheet.find('LocationOriginals'), CSheet.find('LocationOriginals/Location'), add)
	
	# Other Finding Aids <otherfindaid>
	if "add_otherfa" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "otherfindaid", CSheet.find('OtherFindingAids'), CSheet.find('OtherFindingAids/Other'), add)
	
	# Physical or technical details or requirements <phystech>
	if "add_phystech" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "phystech", CSheet.find('PhysicalTechnical'), CSheet.find('PhysicalTechnical/Details'), add)
	
	# Preferred Citation <prefercite>
	if "add_prefcite" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "prefercite", CSheet.find('PreferredCitation'), CSheet.find('PreferredCitation/Example'), add)
	
	# Processing Information <processinfo>
	if "add_processinfo" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "processinfo", CSheet.find('ProcessingInformation'), CSheet.find('ProcessingInformation/Details'), add)
	
	# Related Material <relatedmaterial>
	if CSheet.find('RelatedPublications/Publication/Title') is None or CSheet.find('RelatedManuscripts/Manuscript/UnitTitle') is None:
		pass
	else:
		if CSheet.find('RelatedPublications/Publication/Title').text or CSheet.find('RelatedManuscripts/Manuscript/UnitTitle').text:
			if arch_root.find('relatedmaterial') is None:
				if "add_related" in globals.new_elements or "add-all" in globals.add_all:
					related_element = ET.Element('relatedmaterial')
					related_index = arch_root.getchildren().index(arch_root.find('dsc'))
					arch_root.insert(related_index, related_element)
					if CSheet.find('RelatedMaterialNotes') is None:
						pass
					else:
						for note in CSheet.find('RelatedMaterialNotes'):
							if note.text:
								p_element = ET.Element('p')
								related_element.append(p_element)
								p_element.text = note.text
					for related in CSheet.find('RelatedPublications'):
						if related.find('UnitID') is None:
							pass
						else:
							if related.find('UnitID').text:
								pass
							else:
								if related.find('Author').text or related.find('Title').text or related.find('Citation').text:
									bibref_element = ET.Element('bibref')
									related_element.append(bibref_element)
									if related.find('Author').text:
										bibref_element.text = related.find('Author').text + ", "
									if related.find('Title').text:
										title_element = ET.Element('title')
										bibref_element.append(title_element)
										title_element.text = related.find('Title').text
									if related.find('Citation').text:
										title_element.tail = " " + related.find('Citation').text + ", "
									if related.find('Date').text:
										date_element = ET.Element('date')
										bibref_element.append(date_element)
										date_element.text = related.find('Date').text
										if related.find('NormalDate').text:
											date_element.set("normal", related.find('NormalDate').text)
									if related.find('Reference').text:
										ref_element = ET.Element('ref')
										bibref_element.append(ref_element)
										ref_element.text = related.find('Reference').text
										if related.find('ReferenceLink').text:
											ref_element.set('href', related.find('ReferenceLink').text)
					for relatedman in CSheet.find('RelatedManuscripts'):
						if related.find('UnitID') is None:
							pass
						else:
							if related.find('UnitID').text:
								pass
							else:
								if relatedman.find('Collection').text or relatedman.find('UnitTitle').text or relatedman.find('MaterialID').text:
									archref_element = ET.Element('archref')
									arch_root.find('relatedmaterial').append(archref_element)
									if relatedman.find('Collection').text:
										archref_element.text = relatedman.find('Collection').text + ", "
									if relatedman.find('UnitTitle').text:
										title_element = ET.Element('title')
										archref_element.append(title_element)
										title_element.text = relatedman.find('UnitTitle').text
									if relatedman.find('MaterialID').text:
										title_element.tail = " " + relatedman.find('MaterialID').text + ", "
									if relatedman.find('Date').text:
										date_element = ET.Element('date')
										archref_element.append(date_element)
										date_element.text = relatedman.find('Date').text
										if relatedman.find('NormalDate').text:
											date_element.set("normal", relatedman.find('NormalDate').text)
									if relatedman.find('Reference').text:
										ref_element = ET.Element('ref')
										archref_element.append(ref_element)
										ref_element.text = relatedman.find('Reference').text
										if relatedman.find('ReferenceLink').text:
											ref_element.set('href', relatedman.find('ReferenceLink').text)
			else:
				old_related = arch_root.find('relatedmaterial').attrib
				old_head = arch_root.find('relatedmaterial/head')
				arch_root.find('relatedmaterial').clear()
				if old_related is None:
					pass
				else:
					arch_root.find('relatedmaterial').attrib = old_related
				if old_head is None:
					pass
				else:
					arch_root.find('relatedmaterial').append(old_head)
				for note in CSheet.find('RelatedMaterialNotes'):
					if note.text:
						p_element = ET.Element('p')
						arch_root.find('relatedmaterial').append(p_element)
						p_element.text = note.text
				for related in CSheet.find('RelatedPublications'):
					if related.find('UnitID') is None:
						pass
					else:
						if related.find('UnitID').text:
							pass
						else:
							if related.find('Author').text or related.find('Title').text or related.find('Citation').text:
								bibref_element = ET.Element('bibref')
								arch_root.find('relatedmaterial').append(bibref_element)
								if related.find('Author').text:
									bibref_element.text = related.find('Author').text + ", "
								if related.find('Title').text:
									title_element = ET.Element('title')
									bibref_element.append(title_element)
									title_element.text = related.find('Title').text
								if related.find('Citation').text:
									title_element.tail = " " + related.find('Citation').text + ", "
								if related.find('Date').text:
									date_element = ET.Element('date')
									bibref_element.append(date_element)
									date_element.text = related.find('Date').text
									if related.find('NormalDate').text:
										date_element.set("normal", related.find('NormalDate').text)
								if related.find('Reference').text:
									ref_element = ET.Element('ref')
									bibref_element.append(ref_element)
									ref_element.text = related.find('Reference').text
									if related.find('ReferenceLink').text:
										ref_element.set('href', related.find('ReferenceLink').text)
				for relatedman in CSheet.find('RelatedManuscripts'):
					if related.find('UnitID') is None:
						pass
					else:
						if related.find('UnitID').text:
							pass
						else:
							if relatedman.find('Collection').text or relatedman.find('UnitTitle').text or relatedman.find('MaterialID').text:
								archref_element = ET.Element('archref')
								arch_root.find('relatedmaterial').append(archref_element)
								if relatedman.find('Collection').text:
									archref_element.text = relatedman.find('Collection').text + ", "
								if relatedman.find('UnitTitle').text:
									title_element = ET.Element('title')
									archref_element.append(title_element)
									title_element.text = relatedman.find('UnitTitle').text
								if relatedman.find('MaterialID').text:
									title_element.tail = " " + relatedman.find('MaterialID').text + ", "
								if relatedman.find('Date').text:
									date_element = ET.Element('date')
									archref_element.append(date_element)
									date_element.text = relatedman.find('Date').text
									if relatedman.find('NormalDate').text:
										date_element.set("normal", relatedman.find('NormalDate').text)
								if relatedman.find('Reference').text:
									ref_element = ET.Element('ref')
									archref_element.append(ref_element)
									ref_element.text = relatedman.find('Reference').text
									if relatedman.find('ReferenceLink').text:
										ref_element.set('href', relatedman.find('ReferenceLink').text)
		else:
			old_related_list = arch_root.findall('relatedmaterial')
			for old_related in old_related_list:
				arch_root.remove(old_related)
	
	
	#relations
	from relations import relations
	if version == "ead3":
		relations(arch_root, CSheet.find('Relations'))
	
	# Scope and Content Note <scopecontent>
	if "add_scope" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "scopecontent", CSheet.find('ScopeContent'), CSheet.find('ScopeContent/p'), add)
	
	# Separated Materials <separatedmaterial>
	if "add_sepmat" in globals.new_elements or "add-all" in globals.add_all:
		add = True
	else:
		add = False
	archdescsimple(arch_root, "separatedmaterial", CSheet.find('SeparatedMaterial'), CSheet.find('SeparatedMaterial/Material'), add)
	
	# Use Restrictions <userestrict>
	if "add_userestrict" in globals.new_elements or "add-all" in globals.add_all:
		add is True
	else:
		add is False
	access_use_restrict(arch_root, CSheet.find('UseRestrictions'), "userestrict", "Use", add)
	
	#dsc
	from dsc import dsc
	dsc(arch_root.find('dsc'), input_data, version)
	
	
	##################################################################################################################
	#archdesc elements matched to lower levels:
	##################################################################################################################
	from wx.lib.pubsub import pub
	if "ask_gui" in globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <archdesc> elements to lower levels...")
	
	#Access and Use Restricitons matched to lower levels:
	from access_use_restrict import access_use_lower
	if CSheet.find('CollectionID').text and CSheet.find('IDModel/CollectionSeparator').text:
		collectionID = CSheet.find('CollectionID').text + CSheet.find('IDModel/CollectionSeparator').text
	else:
		if CSheet.find('CollectionID').text:
			collectionID = CSheet.find('CollectionID').text
		else:
			collectionID = ""
	series_separator = CSheet.find('IDModel/SeriesSeparator').text
	access_use_lower(arch_root, CSheet.find('Access'), "accessrestrict", collectionID, series_separator)
	access_use_lower(arch_root, CSheet.find('UseRestrictions'), "userestrict", collectionID, series_separator)
	
	#Acquisitions matched to lower levels:
	from archdesc_lower import acquisitions_lower
	acquisitions_lower(arch_root, CSheet.find('AcquisitionInfo'), version, "acqinfo", collectionID, series_separator)
	
	#Controlled Access Headings matched to lower levels:
	from archdesc_lower import controlaccess_lower
	controlaccess_lower(arch_root, CSheet.find('ControlledAccess'), version, "controlaccess", collectionID, series_separator)
	
	#Related Material matched to lower levels:
	from archdesc_lower import relatedmaterial_lower
	relatedmaterial_lower(arch_root, CSheet.find('RelatedPublications'), CSheet.find('RelatedManuscripts'), version, "relatedmaterial", collectionID, series_separator)
	
	#Relations matched to lower levels:
	if version == "ead3":
		from relations import relations_lower
		relations_lower(arch_root, CSheet.find('Relations'), version, "relations", collectionID, series_separator)
	
	#Simple archdesc elements matched to lower levels:
	from archdescsimple import archdescsimple_lower
	if CSheet.find('CollectionID').text and CSheet.find('IDModel/CollectionSeparator').text:
		collectionID = CSheet.find('CollectionID').text + CSheet.find('IDModel/CollectionSeparator').text
	else:
		if CSheet.find('CollectionID').text:
			collectionID = CSheet.find('CollectionID').text
		else:
			collectionID = ""
	series_separator = CSheet.find('IDModel/SeriesSeparator').text
	archdescsimple_lower(arch_root, CSheet.find('Accruals'), "accruals", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('AlternateForms'), "altformavail", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('AppraisalInfo'), "appraisal", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('LowerLevelHist'), "bioghist", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('CollectionArrangement'), "arrangement", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('CustodialHistory'), "custodhist", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('LegalStatus'), "legalstatus", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('LocationOriginals'), "originalsloc", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('OtherFindingAids'), "otherfindaid", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('PhysicalTechnical'), "phystech", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('ProcessingInformation'), "processinfo", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('LowerLevelScope'), "scopecontent", collectionID, series_separator)
	archdescsimple_lower(arch_root, CSheet.find('SeparatedMaterial'), "separatedmaterial", collectionID, series_separator)