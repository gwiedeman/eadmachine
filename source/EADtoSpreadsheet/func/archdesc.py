# module for the <archdesc/> or collection-level description
import xml.etree.cElementTree as ET
from archdescsimple import archdescsimple
from access_use_restrict import access_use_restrict
import globals
from mixed_content import mixed_content
import wx


def archdesc(EAD, FASheet, version):
	from wx.lib.pubsub import pub
	wx.CallAfter(pub.sendMessage, "update_spread", msg="Reading <archdesc>...")
	
	arch_root = EAD.find('archdesc')
	CSheet = FASheet[0]
	
	wx.CallAfter(pub.sendMessage, "update_spread", msg="Reading collection-level <did>...")
	#collection-level did
	from collection_did import collection_did
	cdid_root = arch_root.find('did')
	collection_did(cdid_root, CSheet, version)
		
	#Access Restrictions Section
	access_use_restrict(arch_root, CSheet.find('Access'), "accessrestrict", "Access", version)
	
	#Accruals Section
	archdescsimple(arch_root, "accruals", CSheet.find('Accruals'), 'Accrual', version)
	
	#Acquisitions Information Section
	if arch_root.find('acqinfo') is None:
		pass
	else:
		if arch_root.find('acqinfo/p') is None and arch_root.find('acqinfo/list') is None and arch_root.find('acqinfo/chronlist') is None:
			pass
		else:
			CSheet.find('AcquisitionInfo').clear()
			for acqinfo_entry in arch_root.find('acqinfo'):
				if acqinfo_entry.tag == "p":
					Acquis_element = ET.Element('Acquis')
					CSheet.find('AcquisitionInfo').append(Acquis_element)
					UnitID_element = ET.Element('UnitID')
					Acquis_element.append(UnitID_element)
					Event_element = ET.Element('Event')
					Acquis_element.append(Event_element)
					Date_element = ET.Element('Date')
					Acquis_element.append(Date_element)
					DateNormal_element = ET.Element('DateNormal')
					Acquis_element.append(DateNormal_element)
					if acqinfo_entry.find('date') is None:
						Event_element.text = mixed_content(acqinfo_entry)
					else:
						Event_element.text = mixed_content(acqinfo_entry)
						Date_element.text = acqinfo_entry.find('date').text
						if 'normal' in acqinfo_entry.find('date').attrib:
							DateNormal_element.text = acqinfo_entry.find('date').attrib['normal']
				if acqinfo_entry.tag == "list":
					if 'type' in acqinfo_entry.attrib:
						if acqinfo_entry.attrib['type'] == "deflist":
							for deflist_entry in acqinfo_entry:
								if deflist_entry.tag == "defitem":
									Acquis_element = ET.Element('Acquis')
									CSheet.find('AcquisitionInfo').append(Acquis_element)
									UnitID_element = ET.Element('UnitID')
									Acquis_element.append(UnitID_element)
									Event_element = ET.Element('Event')
									Acquis_element.append(Event_element)
									Date_element = ET.Element('Date')
									Acquis_element.append(Date_element)
									DateNormal_element = ET.Element('DateNormal')
									Acquis_element.append(DateNormal_element)
									if deflist_entry.find('label') is None or deflist_entry.find('item') is None:
										Event_element.text = mixed_content(deflist_entry)
									else:
										if len(deflist_entry.find('item')) >= len(deflist_entry.find('label')):
											Event_element.text =  mixed_content(deflist_entry.find('item'))
											Date_element.text = mixed_content(deflist_entry.find('label'))
										else:
											Event_element.text = mixed_content(deflist_entry.find('label'))
											Date_element.text = mixed_content(deflist_entry.find('item'))
						else:
							for list_entry in acqinfo_entry:
								Acquis_element = ET.Element('Acquis')
								CSheet.find('AcquisitionInfo').append(Acquis_element)
								UnitID_element = ET.Element('UnitID')
								Acquis_element.append(UnitID_element)
								Event_element = ET.Element('Event')
								Acquis_element.append(Event_element)
								Date_element = ET.Element('Date')
								Acquis_element.append(Date_element)
								DateNormal_element = ET.Element('DateNormal')
								Acquis_element.append(DateNormal_element)
								if list_entry.find('date') is None:
									Event_element.text = mixed_content(list_entry)
								else:
									Event_element.text = mixed_content(list_entry.text) + list_entry.find('date').text + mixed_content(list_entry.tail)
									Date_element.text = list_entry.find('date').text
									if 'normal' in list_entry.find('date').attrib:
										DateNormal_element.text = list_entry.find('date').attrib['normal']
					else:
						for list_entry in acqinfo_entry:
							Acquis_element = ET.Element('Acquis')
							CSheet.find('AcquisitionInfo').append(Acquis_element)
							UnitID_element = ET.Element('UnitID')
							Acquis_element.append(UnitID_element)
							Event_element = ET.Element('Event')
							Acquis_element.append(Event_element)
							Date_element = ET.Element('Date')
							Acquis_element.append(Date_element)
							DateNormal_element = ET.Element('DateNormal')
							Acquis_element.append(DateNormal_element)
							if list_entry.find('date') is None:
								Event_element.text = mixed_content(list_entry)
							else:
								Event_element.text = mixed_content(list_entry.text) + list_entry.find('date').text + mixed_content(list_entry.tail)
								Date_element.text = list_entry.find('date').text
								if 'normal' in list_entry.find('date').attrib:
									DateNormal_element.text = list_entry.find('date').attrib['normal']
				if acqinfo_entry.tag == "chronlist":
					for chron_entry in acqinfo_entry:
						if chron_entry.find('eventgrp') is None:
							Acquis_element = ET.Element('Acquis')
							CSheet.find('AcquisitionInfo').append(Acquis_element)
							UnitID_element = ET.Element('UnitID')
							Acquis_element.append(UnitID_element)
							Event_element = ET.Element('Event')
							Acquis_element.append(Event_element)
							Date_element = ET.Element('Date')
							Acquis_element.append(Date_element)
							DateNormal_element = ET.Element('DateNormal')
							Acquis_element.append(DateNormal_element)
							Event_element.text = mixed_content(chron_entry.find('event'))
							if version == "ead2002":
								Date_element.text = mixed_content(chron_entry.find('date'))
								if 'normal' in chron_entry.find('date').attrib:
									DateNormal_element.text = chron_entry.find('date').attrib['normal']
							else:
								if chron_entry.find('datesingle') is None:
									if chron_entry.find('daterange') is None:
										if chron_entry.find('dateset') is None:
											pass
										else:
											Date_element.text = mixed_content(chron_entry.find('dateset'))
									else:
										Date_element.text = chron_entry.find('daterange/fromdate').text + "-" + chron_entry.find('daterange/todate').text
										if 'standarddate' in chron_entry.find('daterange/fromdate').attrib:
											if 'standarddate' in chron_entry.find('daterange/fromdate').attrib:
												DateNormal_element.text = chron_entry.find('daterange/fromdate').attrib['standarddate'] + "/" + chron_entry.find('daterange/todate').attrib['standarddate']
								else:
									Date_element.text = chron_entry.find('datesingle').text
									if 'standarddate' in chron_entry.find('datesingle').attrib:
										DateNormal_element.text = chron_entry.find('datesingle').attrib['standarddate']
						else:
							for event_group in chron_entry:
								Acquis_element = ET.Element('Acquis')
								CSheet.find('AcquisitionInfo').append(Acquis_element)
								UnitID_element = ET.Element('UnitID')
								Acquis_element.append(UnitID_element)
								Event_element = ET.Element('Event')
								Acquis_element.append(Event_element)
								Date_element = ET.Element('Date')
								Acquis_element.append(Date_element)
								DateNormal_element = ET.Element('DateNormal')
								Acquis_element.append(DateNormal_element)
								Event_element.text = mixed_content(event_group.find('event'))
								if version == "ead2002":
									Date_element.text = mixed_content(chron_entry.find('date'))
									if 'normal' in chron_entry.find('date').attrib:
										DateNormal_element.text = chron_entry.find('date').attrib['normal']
								else:
									if chron_entry.find('datesingle') is None:
										if chron_entry.find('daterange') is None:
											if chron_entry.find('dateset') is None:
												pass
											else:
												Date_element.text = mixed_content(chron_entry.find('dateset'))
										else:
											Date_element.text = chron_entry.find('daterange/fromdate').text + "-" + chron_entry.find('daterange/todate').text
											if 'standarddate' in chron_entry.find('daterange/fromdate').attrib:
												if 'standarddate' in chron_entry.find('daterange/fromdate').attrib:
													DateNormal_element.text = chron_entry.find('daterange/fromdate').attrib['standarddate'] + "/" + chron_entry.find('daterange/todate').attrib['standarddate']
									else:
										Date_element.text = chron_entry.find('datesingle').text
										if 'standarddate' in chron_entry.find('datesingle').attrib:
											DateNormal_element.text = chron_entry.find('datesingle').attrib['standarddate']
		for dumb_descgrp in arch_root:
			if dumb_descgrp.tag == "descgrp":
				if dumb_descgrp.find('acqinfo') is None:
					pass
				else:
					if dumb_descgrp.find('acqinfo/p') is None and dumb_descgrp.find('acqinfo/list') is None and dumb_descgrp.find('acqinfo/chronlist') is None:
						pass
					else:
						CSheet.find('AcquisitionInfo').clear()
						for acqinfo_entry in dumb_descgrp.find('acqinfo'):
							if acqinfo_entry.tag == "p":
								Acquis_element = ET.Element('Acquis')
								CSheet.find('AcquisitionInfo').append(Acquis_element)
								UnitID_element = ET.Element('UnitID')
								Acquis_element.append(UnitID_element)
								Event_element = ET.Element('Event')
								Acquis_element.append(Event_element)
								Date_element = ET.Element('Date')
								Acquis_element.append(Date_element)
								DateNormal_element = ET.Element('DateNormal')
								Acquis_element.append(DateNormal_element)
								if acqinfo_entry.find('date') is None:
									Event_element.text = mixed_content(acqinfo_entry)
								else:
									Event_element.text = mixed_content(acqinfo_entry)
									Date_element.text = acqinfo_entry.find('date').text
									if 'normal' in acqinfo_entry.find('date').attrib:
										DateNormal_element.text = acqinfo_entry.find('date').attrib['normal']
							if acqinfo_entry.tag == "list":
								if 'type' in acqinfo_entry.attrib:
									if acqinfo_entry.attrib['type'] == "deflist":
										for deflist_entry in acqinfo_entry:
											if deflist_entry.tag == "defitem":
												Acquis_element = ET.Element('Acquis')
												CSheet.find('AcquisitionInfo').append(Acquis_element)
												UnitID_element = ET.Element('UnitID')
												Acquis_element.append(UnitID_element)
												Event_element = ET.Element('Event')
												Acquis_element.append(Event_element)
												Date_element = ET.Element('Date')
												Acquis_element.append(Date_element)
												DateNormal_element = ET.Element('DateNormal')
												Acquis_element.append(DateNormal_element)
												if deflist_entry.find('label') is None or deflist_entry.find('item') is None:
													Event_element.text = mixed_content(deflist_entry)
												else:
													if len(deflist_entry.find('item')) >= len(deflist_entry.find('label')):
														Event_element.text =  mixed_content(deflist_entry.find('item'))
														Date_element.text = mixed_content(deflist_entry.find('label'))
													else:
														Event_element.text = mixed_content(deflist_entry.find('label'))
														Date_element.text = mixed_content(deflist_entry.find('item'))
									else:
										for list_entry in acqinfo_entry:
											Acquis_element = ET.Element('Acquis')
											CSheet.find('AcquisitionInfo').append(Acquis_element)
											UnitID_element = ET.Element('UnitID')
											Acquis_element.append(UnitID_element)
											Event_element = ET.Element('Event')
											Acquis_element.append(Event_element)
											Date_element = ET.Element('Date')
											Acquis_element.append(Date_element)
											DateNormal_element = ET.Element('DateNormal')
											Acquis_element.append(DateNormal_element)
											if list_entry.find('date') is None:
												Event_element.text = mixed_content(list_entry)
											else:
												Event_element.text = mixed_content(list_entry.text) + list_entry.find('date').text + mixed_content(list_entry.tail)
												Date_element.text = list_entry.find('date').text
												if 'normal' in list_entry.find('date').attrib:
													DateNormal_element.text = list_entry.find('date').attrib['normal']
								else:
									for list_entry in acqinfo_entry:
										Acquis_element = ET.Element('Acquis')
										CSheet.find('AcquisitionInfo').append(Acquis_element)
										UnitID_element = ET.Element('UnitID')
										Acquis_element.append(UnitID_element)
										Event_element = ET.Element('Event')
										Acquis_element.append(Event_element)
										Date_element = ET.Element('Date')
										Acquis_element.append(Date_element)
										DateNormal_element = ET.Element('DateNormal')
										Acquis_element.append(DateNormal_element)
										if list_entry.find('date') is None:
											Event_element.text = mixed_content(list_entry)
										else:
											Event_element.text = mixed_content(list_entry.text) + list_entry.find('date').text + mixed_content(list_entry.tail)
											Date_element.text = list_entry.find('date').text
											if 'normal' in list_entry.find('date').attrib:
												DateNormal_element.text = list_entry.find('date').attrib['normal']
							if acqinfo_entry.tag == "chronlist":
								for chron_entry in acqinfo_entry:
									if chron_entry.find('eventgrp') is None:
										Acquis_element = ET.Element('Acquis')
										CSheet.find('AcquisitionInfo').append(Acquis_element)
										UnitID_element = ET.Element('UnitID')
										Acquis_element.append(UnitID_element)
										Event_element = ET.Element('Event')
										Acquis_element.append(Event_element)
										Date_element = ET.Element('Date')
										Acquis_element.append(Date_element)
										DateNormal_element = ET.Element('DateNormal')
										Acquis_element.append(DateNormal_element)
										Event_element.text = mixed_content(chron_entry.find('event'))
										Date_element.text = mixed_content(chron_entry.find('date'))
										if 'normal' in chron_entry.find('date').attrib:
											DateNormal_element.text = chron_entry.find('date').attrib['normal']
									else:
										for event_group in chron_entry:
											Acquis_element = ET.Element('Acquis')
											CSheet.find('AcquisitionInfo').append(Acquis_element)
											UnitID_element = ET.Element('UnitID')
											Acquis_element.append(UnitID_element)
											Event_element = ET.Element('Event')
											Acquis_element.append(Event_element)
											Date_element = ET.Element('Date')
											Acquis_element.append(Date_element)
											DateNormal_element = ET.Element('DateNormal')
											Acquis_element.append(DateNormal_element)
											Event_element.text = mixed_content(event_group.find('event'))
											Date_element.text = mixed_content(chron_entry.find('date'))
											if 'normal' in chron_entry.find('date').attrib:
												DateNormal_element.text = chron_entry.find('date').attrib['normal']
					
	# Alternate Forms Available Section <altformavail>
	archdescsimple(arch_root, "altformavail", CSheet.find('AlternateForms'), 'Alternative', version)
	
	# Appraisal Section <appraisal>
	archdescsimple(arch_root, "appraisal", CSheet.find('AppraisalInfo'), 'Appraisal', version)
	
	# Arrangement Section <arrangement>
	if arch_root.find('arrangement') is None:
		pass
	else:
		CSheet.find('CollectionArrangement').clear()
		for arrange in arch_root:
			if arrange.tag == 'arrangement':
				for para in arrange:
					if para.tag == "p":
						if para.find('list') is None:
							Arrangement_element = ET.Element('Arrangement')
							CSheet.find('CollectionArrangement').append(Arrangement_element)
							UnitID_element = ET.Element('UnitID')
							Arrangement_element.append(UnitID_element)
							Text_element = ET.Element('Text')
							Arrangement_element.append(Text_element)
							Text_element.text = mixed_content(para)
						else:
							if para.text:
								if len(para.text.strip()) >= 1:
									Arrangement_element = ET.Element('Arrangement')
									CSheet.find('CollectionArrangement').append(Arrangement_element)
									UnitID_element = ET.Element('UnitID')
									Arrangement_element.append(UnitID_element)
									Text_element = ET.Element('Text')
									Arrangement_element.append(Text_element)
									Text_element.text = para.text
							for list in para:
								if list.tag == "list":
									for listitem in list:
										Arrangement_element = ET.Element('Arrangement')
										CSheet.find('CollectionArrangement').append(Arrangement_element)
										UnitID_element = ET.Element('UnitID')
										Arrangement_element.append(UnitID_element)
										Text_element = ET.Element('Text')
										Arrangement_element.append(Text_element)
										Text_element.text = mixed_content(listitem)
							if para.tail:
								if len(para.tail.strip()) >= 1:
									Arrangement_element = ET.Element('Arrangement')
									CSheet.find('CollectionArrangement').append(Arrangement_element)
									UnitID_element = ET.Element('UnitID')
									Arrangement_element.append(UnitID_element)
									Text_element = ET.Element('Text')
									Arrangement_element.append(Text_element)
									Text_element.text = para.tail
					elif para.tag == "list":
						for listitem in para:
							Arrangement_element = ET.Element('Arrangement')
							CSheet.find('CollectionArrangement').append(Arrangement_element)
							UnitID_element = ET.Element('UnitID')
							Arrangement_element.append(UnitID_element)
							Text_element = ET.Element('Text')
							Arrangement_element.append(Text_element)
							Text_element.text = mixed_content(listitem)
	for dumb_descgrp in arch_root:
		if dumb_descgrp.tag == "descgrp":
			if dumb_descgrp.find('arrangement') is None:
				pass
			else:
				CSheet.find('CollectionArrangement').clear()
				for arrange in dumb_descgrp:
					if arrange.tag == 'arrangement':
						for para in arrange:
							if para.tag == "p":
								if para.find('list') is None:
									Arrangement_element = ET.Element('Arrangement')
									CSheet.find('CollectionArrangement').append(Arrangement_element)
									UnitID_element = ET.Element('UnitID')
									Arrangement_element.append(UnitID_element)
									Text_element = ET.Element('Text')
									Arrangement_element.append(Text_element)
									Text_element.text = mixed_content(para)
								else:
									if para.text:
										Arrangement_element = ET.Element('Arrangement')
										CSheet.find('CollectionArrangement').append(Arrangement_element)
										UnitID_element = ET.Element('UnitID')
										Arrangement_element.append(UnitID_element)
										Text_element = ET.Element('Text')
										Arrangement_element.append(Text_element)
										Text_element.text = mixed_content(para)
									for listitem in para:
										if listitem.tag == "list":
											Arrangement_element = ET.Element('Arrangement')
											CSheet.find('CollectionArrangement').append(Arrangement_element)
											UnitID_element = ET.Element('UnitID')
											Arrangement_element.append(UnitID_element)
											Text_element = ET.Element('Text')
											Arrangement_element.append(Text_element)
											Text_element.text = mixed_content(listitem)
									if para.tail:
										Arrangement_element = ET.Element('Arrangement')
										CSheet.find('CollectionArrangement').append(Arrangement_element)
										UnitID_element = ET.Element('UnitID')
										Arrangement_element.append(UnitID_element)
										Text_element = ET.Element('Text')
										Arrangement_element.append(Text_element)
										Text_element.text = mixed_content(para)
							elif para.tag == "list":
								for listitem in para:
									Arrangement_element = ET.Element('Arrangement')
									CSheet.find('CollectionArrangement').append(Arrangement_element)
									UnitID_element = ET.Element('UnitID')
									Arrangement_element.append(UnitID_element)
									Text_element = ET.Element('Text')
									Arrangement_element.append(Text_element)
									Text_element.text = mixed_content(listitem)
	
	# Bibliography Section <bibliography>
	biblio_parent = 0
	if arch_root.find('bibliography') is None:
		for dumb_descgrp in arch_root:
			if dumb_descgrp.tag == "descgrp":
				if dumb_descgrp.find('bibliography') is None:
					pass
				else:
					biblio_parent = dumb_descgrp
	else:
		biblio_parent = arch_root
	if biblio_parent == 0:
		pass
	else:
		if biblio_parent.find('bibliography/p') is None:
			pass
		else:
			CSheet.find('BibliographyNote').text = mixed_content(biblio_parent.find('bibliography/p'))
		if biblio_parent.find('bibliography/bibref') is None:
			if biblio_parent.find('bibliography/list') is None:
				pass
			else:
				CSheet.find('PublicationBibliography').clear()
				for bib_item in biblio_parent.find('bibliography/list'):
					bibref = bib_item.find('bibref')
					if bibref.tag == "bibref":
						Publication_element = ET.Element('Publication')
						CSheet.find('PublicationBibliography').append(Publication_element)
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
		else:
			CSheet.find('PublicationBibliography').clear()
			for bibref in biblio_parent.find('bibliography'):
				if bibref.tag == "bibref":
					Publication_element = ET.Element('Publication')
					CSheet.find('PublicationBibliography').append(Publication_element)
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
		if biblio_parent.find('bibliography/archref') is None:
			pass
		else:
			CSheet.find('ManuscriptBibliography').clear()
			for archref in biblio_parent.find('bibliography'):
				if archref.tag == "archref":
					Manuscript_element = ET.Element('Manuscript')
					CSheet.find('ManuscriptBibliography').append(Manuscript_element)
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
						
	# Biographical or Administrative History Section <bioghist>
	biohist_parent = 0
	if arch_root.find('bioghist') is None:
		for dumb_descgrp in arch_root:
			if dumb_descgrp.tag == "descgrp":
				if dumb_descgrp.find('bioghist') is None:
					pass
				else:
					biohist_parent = dumb_descgrp
	else:
		biohist_parent = arch_root
	if biohist_parent == 0:
		pass
	else:
		if biohist_parent.find('bioghist/head') is None:
			pass
		else:
			CSheet.find('HistoricalNoteTitle').text = biohist_parent.find('bioghist/head').text
		if biohist_parent.find('bioghist/bioghist') is None:
			if biohist_parent.find('bioghist/chronlist') is None:
				CSheet.find('HistoricalNote').clear()
				for content in biohist_parent.find('bioghist'):
					if content.tag == "p":
						p_element = ET.Element('p')
						CSheet.find('HistoricalNote').append(p_element)
						p_element.text = mixed_content(content)
			else:
				CSheet.find('HistoricalNote').clear()
				for chrono_item in biohist_parent.find('bioghist/chronlist'):
					if chrono_item.tag == "chronitem":
						p_element = ET.Element('p')
						CSheet.find('HistoricalNote').append(p_element)
						p_element.text = mixed_content(chrono_item)
		else:
			CSheet.find('HistoricalNote').clear()
			for content in biohist_parent.find('bioghist').iter():
				if content.text:
					if len(content.text.strip()) >= 1:
						p_element = ET.Element('p')
						CSheet.find('HistoricalNote').append(p_element)
						p_element.text = content.text
						
	wx.CallAfter(pub.sendMessage, "update_spread", msg="Reading <controlaccess>...")
	# Controlled Access Headings <controlaccess>
	access_parent = 0
	if arch_root.find('controlaccess') is None:
		for dumb_descgrp in arch_root:
			if dumb_descgrp.tag == "descgrp":
				if dumb_descgrp.find('controlaccess') is None:
					pass
				else:
					access_parent = dumb_descgrp
	else:
		access_parent = arch_root
	if access_parent == 0:
		pass
	else:
		CSheet.find('ControlledAccess').clear()
		for access in access_parent:
			if access.tag == "controlaccess":
				for point in access:
					if point.tag == "p":
						pass
					elif point.tag == "head":
						pass
					elif point.tag =="controlaccess":
						for subpoint in point:
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
											Part_element.text = Part_element.text + controlled.text
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
						ElementName_element.text = point.tag
						if "encodinganalog" in point.attrib:
							MARCEncoding_element.text = point.attrib['encodinganalog']
						if "normal" in point.attrib:
							Normal_element.text = point.attrib['normal']
						if "source" in point.attrib:
							Source_element.text = point.attrib['source']
						if version == "ead2002":
							if "id" in point.attrib:
								Identifier_element.text = point.attrib['id']
							if "role" in point.attrib:
								Relator_element.text = point.attrib['role']
							Part_element.text = mixed_content(point)
						else:
							if "identifier " in point.attrib:
								Identifier_element.text = point.attrib['identifier ']
							if "relator" in point.attrib:
								Relator_element.text = point.attrib['relator']
							if point.text:
								Part_element.text = point.text
							for controlled in point:
								if controlled.tag == "part":
									if Part_element.text:
										Part_element.text = Part_element.text + controlled.text
		
	# Custodial History section <custodhist>
	archdescsimple(arch_root, "custodhist", CSheet.find('CustodialHistory'), 'Event', version)
	
	# Legal Status <legalstatus>
	archdescsimple(arch_root, "legalstatus", CSheet.find('LegalStatus'), 'Status', version)
	
	# Location of Originals when collection contains photocopies, etc. <originalsloc>
	archdescsimple(arch_root, "originalsloc", CSheet.find('LocationOriginals'), 'Location', version)
	
	# Other Finding Aids <otherfindaid>
	archdescsimple(arch_root, "otherfindaid", CSheet.find('OtherFindingAids'), 'Other', version)
	
	# Physical or technical details or requirements <phystech>
	archdescsimple(arch_root, "phystech", CSheet.find('PhysicalTechnical'), 'Details', version)
	
	# Preferred Citation <prefercite>
	archdescsimple(arch_root, "prefercite", CSheet.find('PreferredCitation'), 'Example', version)
	
	# Processing Information <processinfo>
	archdescsimple(arch_root, "processinfo", CSheet.find('ProcessingInformation'), 'Details', version)
	
	# Related Material <relatedmaterial>
	related_parent = 0
	if arch_root.find('relatedmaterial') is None:
		for dumb_descgrp in arch_root:
			if dumb_descgrp.tag == "descgrp":
				if dumb_descgrp.find('relatedmaterial') is None:
					pass
				else:
					related_parent = dumb_descgrp
	else:
		related_parent = arch_root
	if related_parent == 0:
		pass
	else:
		if related_parent.find('relatedmaterial/p') is None and related_parent.find('relatedmaterial/list') is None:
			pass
		else:
			CSheet.find('RelatedMaterialNotes').clear()
			for related_note in related_parent.find('relatedmaterial'):
				if related_note.tag == "p":
					if related_note.find('list') is None:
						RelatedMaterialNote_element = ET.Element('RelatedMaterialNote')
						CSheet.find('RelatedMaterialNotes').append(RelatedMaterialNote_element)
						RelatedMaterialNote_element.text = mixed_content(related_note)
					else:
						for related_list in related_note:
							if related_list.tag == "list":
								for related_item in related_list:
									if related_item.tag == "item":
										RelatedMaterialNote_element = ET.Element('RelatedMaterialNote')
										CSheet.find('RelatedMaterialNotes').append(RelatedMaterialNote_element)
										RelatedMaterialNote_element.text = mixed_content(related_item)
				elif related_note.tag == "list":
					for related_item in related_note:
						if related_item.tag == "item":
							RelatedMaterialNote_element = ET.Element('RelatedMaterialNote')
							CSheet.find('RelatedMaterialNotes').append(RelatedMaterialNote_element)
							RelatedMaterialNote_element.text = mixed_content(related_item)
		if related_parent.find('relatedmaterial/bibref') is None:
			pass
		else:
			CSheet.find('RelatedPublications').clear()
			for bibref in related_parent.find('relatedmaterial'):
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
		if related_parent.find('relatedmaterial/archref') is None:
			pass
		else:
			CSheet.find('RelatedManuscripts').clear()
			for archref in related_parent.find('relatedmaterial'):
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
	
	#relations
	if version == "ead3":
		if arch_root.find('relations') is None:
			pass
		else:
			for relation in arch_root.find('relations'):
				if relation.tag == "relation":
					CSheet.find('Relations').clear()
					Relation_element = ET.Element('Relation')
					CSheet.find('Relations').append(Relation_element)
					UnitID_element = ET.Element('UnitID')
					Relation_element.append(UnitID_element)
					RelationID_element = ET.Element('RelationID')
					Relation_element.append(RelationID_element)
					RelationType_element = ET.Element('RelationType')
					Relation_element.append(RelationType_element)
					RelationLink_element = ET.Element('RelationLink')
					Relation_element.append(RelationLink_element)
					RelationEntry_element = ET.Element('RelationEntry')
					Relation_element.append(RelationEntry_element)
					RelationDate_element = ET.Element('RelationDate')
					Relation_element.append(RelationDate_element)
					RelationDateNormal_element = ET.Element('RelationDateNormal')
					Relation_element.append(RelationDateNormal_element)
					RelationPlace_element = ET.Element('RelationPlace')
					Relation_element.append(RelationPlace_element)
					RelationNote_element = ET.Element('RelationNote')
					Relation_element.append(RelationNote_element)
					if "id" in relation.attrib:
						RelationID_element.text = relation.attrib['id']
					if "relationtype" in relation.attrib:
						RelationType_element.text = relation.attrib['relationtype']
					if "href" in relation.attrib:
						RelationLink_element.text = relation.attrib['href']
					if relation.find('relationentry') is None:
						pass
					else:
						RelationEntry_element.text = mixed_content(relation.find('relationentry'))
					if relation.find('datesingle') is None and relation.find('daterange') is None and relation.find('dateset') is None:
						pass
					else:
						if relation.find('datesingle') is None:
							if relation.find('daterange') is None:
								if relation.find('dateset') is None:
									pass
								else:
									for date in relation.find('dateset'):
										if date.tag == "datesingle":
											RelationDate_element.text = RelationDate_element.text + date.text + ", "
											if "standarddate" in date.attrib:
												RelationDateNormal_element.text = RelationDateNormal_element.text + date.attrib['standarddate'] + ", "
										if date.tag == "daterange":
											RelationDate_element.text = RelationDate_element.text + date.find('fromdate').text + "/" + date.find('todate').text + ", "
											if "standarddate" in date.find('fromdate').attrib:
												if "standarddate" in date.find('todate').attrib:
													RelationDateNormal_element.text = RelationDateNormal_element.text + date.find('fromdate').attrib['standarddate'] + "/" + date.find('todate').attrib['standarddate'] + ", "
							else:
								RelationDate_element.text = relation.find('daterange/fromdate').text + "-" + relation.find('daterange/todate').text
								if "standarddate" in relation.find('daterange/fromdate').attrib:
									if "standarddate" in relation.find('daterange/todate').attrib:
										RelationDateNormal_element.text = relation.find('daterange/fromdate').attrib['standarddate'] + "/" + relation.find('daterange/todate').attrib['standarddate']
						else:
							RelationDate_element.text = relation.find('datesingle').text
							if "standarddate" in relation.find('datesingle').attrib:
								RelationDateNormal_element.text = relation.find('datesingle').attrib['standarddate']
					if relation.find('geogname') is None:
						pass
					else:
						RelationPlace_element.text = mixed_content(relation.find('geogname'))
					if relation.find('descriptivenote') is None:
						pass
					else:
						RelationNote_element.text = mixed_content(relation.find('descriptivenote/p'))	
	
	# Scope and Content Note <scopecontent>
	scope_parent = 0
	if arch_root.find('scopecontent') is None:
		for dumb_descgrp in arch_root:
			if dumb_descgrp.tag == "descgrp":
				if dumb_descgrp.find('scopecontent') is None:
					pass
				else:
					scope_parent = dumb_descgrp
	else:
		scope_parent = arch_root
	if scope_parent == 0:
		pass
	else:
		if scope_parent.find('scopecontent/scopecontent') is None:
			CSheet.find('ScopeContent').clear()
			for content in scope_parent.find('scopecontent'):
				if content.tag == "p":
					p_element = ET.Element('p')
					CSheet.find('ScopeContent').append(p_element)
					p_element.text = mixed_content(content)
		else:
			CSheet.find('ScopeContent').clear()
			for content in scope_parent.find('scopecontent').iter():
				if content.text:
					if len(content.text.strip()) >= 1:
						p_element = ET.Element('p')
						CSheet.find('ScopeContent').append(p_element)
						p_element.text = content.text
	
	# Separated Materials <separatedmaterial>
	archdescsimple(arch_root, "separatedmaterial", CSheet.find('SeparatedMaterial'), 'Material', version)
	
	# Use Restrictions <userestrict>
	access_use_restrict(arch_root, CSheet.find('UseRestrictions'), "userestrict", "Use", version)
	
	#dsc
	from dsc import dsc
	dsc(arch_root.find('dsc'), FASheet, version)