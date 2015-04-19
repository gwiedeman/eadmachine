import globals

# This file checks if data from the input spreadsheet does not fit into the selected EAD template
# It will ask a series of prompts to see if a user wants to add tags to fit this data or ignore items

def add_element(template, input):
	if input.find('CollectionSheet/OtherID').text:
		if template.find('control/otherrecordid') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_otherid = raw_input("You entered one or more Other IDs for this collection but there is no <otherrecordid> tags in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_otherid.lower() == 'yes' or add_otherid.lower() == 'y':
					globals.new_elements.append('add_otherid')
				elif add_otherid.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/Representation').text:
		if template.find('control/representation') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_rep = raw_input("You entered one or more Representations for this collection but there is no <representation> tags in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_rep.lower() == 'yes' or add_rep.lower() == 'y':	
					globals.new_elements.append('add_rep')
				elif add_rep.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/Subtitle').text:
		if template.find('eadheader/filedesc/titlestmt/subtitle') is None or template.find('frontmatter/titlepage/subtitle') is None:
			if template.find('control/filedesc/titlestmt/subtitle') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_subtitle = raw_input("You entered a Subtitle but there is no <subtitle> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_subtitle.lower() == 'yes' or add_subtitle.lower() == 'y':
						globals.new_elements.append('add_subtitle')
					elif add_subtitle.lower() == 'yesall':
						globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/ProcessedBy').text:
		if template.find('eadheader/filedesc/titlestmt/author') is None or template.find('frontmatter/titlepage/author') is None:
			if template.find('control/filedesc/titlestmt/author') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_subtitle = raw_input("You entered an author (Processed By field) but there is no <author> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_author.lower() == 'yes' or add_author.lower() == 'y':
						globals.new_elements.append('add_author')
					elif add_author.lower() == 'yesall':
						globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/Sponsor').text:
		if template.find('control/filedesc/titlestmt/sponsor') is None and template.find('eadheader/filedesc/titlestmt/sponsor') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_sponsor = raw_input("You entered a Sponsor but there is no <sponsor> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_sponsor.lower() == 'yes' or add_sponsor.lower() == 'y':
					globals.new_elements.append('add_sponsor')
				elif add_sponsor.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/Edition').text:
		if template.find('control/filedesc/editionstmt') is None and template.find('eadheader/filedesc/editionstmt') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_edition = raw_input("You entered a Edition statement but there is no <editionstmt> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_edition.lower() == 'yes' or add_edition.lower() == 'y':
					globals.new_elements.append('add_edition')
				elif add_edition.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/Publisher/PublisherName').text or input.find('CollectionSheet/Publisher/AddressLine').text:
		if template.find('control/filedesc/publicationstmt/publisher') is None and template.find('eadheader/filedesc/publicationstmt/publisher') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_publication = raw_input("You entered a Publisher or Publisher Address but there is no <publicationstmt> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_publication.lower() == 'yes' or add_publication.lower() == 'y':
					globals.new_elements.append('add_publication')
				elif add_publication.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/PartofSeries').text:
		if template.find('control/filedesc/seriesstmt') is None and template.find('eadheader/filedesc/seriesstmt') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_seriesstmt = raw_input("You entered a Series statement but there is no <seriesstmt> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_seriesstmt.lower() == 'yes' or add_seriesstmt.lower() == 'y':
					globals.new_elements.append('add_seriesstmt')
				elif add_seriesstmt.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/NoteStatements/NoteStatement').text:
		if template.find('control/filedesc/notestmt') is None and template.find('eadheader/filedesc/notestmt') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_notestmt = raw_input("You entered a Note Statement but there is no <notestmt> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_notestmt.lower() == 'yes' or add_notestmt.lower() == 'y':
					globals.new_elements.append('add_notestmt')
				elif add_notestmt.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	
	#ead2002 only questions
	if template.find('eadheader') is None:
		pass
	else:
		
		if input.find('CollectionSheet/EADCreator').text or input.find('CollectionSheet/FindingAidLanguages/FALanguage/Lang').text:
			if template.find('eadheader/profiledesc') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_profile = raw_input("You entered EAD languages and/or creation date but there is no <profiledesc> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_profile.lower() == 'yes' or add_profile.lower() == 'y':
						globals.new_elements.append('add_profile')
					elif add_profile.lower() == 'yesall':
						globals.add_all.append('add-all')
						
		if input.find('CollectionSheet/EADCreator').text:
			if template.find('eadheader/profiledesc/creation') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_eadcre = raw_input("You entered an EAD creator but there is no <creation> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_eadcre.lower() == 'yes' or add_eadcre.lower() == 'y':
						globals.new_elements.append('add_eadcre')
					elif add_eadcre.lower() == 'yesall':
						globals.add_all.append('add-all')
		
		if input.find('CollectionSheet/FindingAidLanguages/FALanguage/Lang').text:
			if template.find('eadheader/profiledesc/langusage') is None or template.find('eadheader/profiledesc/langusage/language') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_eadcre = raw_input("You entered a EAD Languages but there is no <langusage> or <language> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_lang1.lower() == 'yes' or add_lang1.lower() == 'y':
						globals.new_elements.append('add_lang1')
					elif add_lang1.lower() == 'yesall':
						globals.add_all.append('add-all')
	
		if input.find('CollectionSheet/StandardConventions/Convention/Citation').text or CSheet.find('LocalConventions/Convention/Citation').text:
			if template.find('eadheader/profiledesc/descrules') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_descrule = raw_input("You entered Descriptive Rules but there is no <descrules> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_descrule.lower() == 'yes' or add_descrule.lower() == 'y':
						globals.new_elements.append('add_descrule')
					elif add_descrule.lower() == 'yesall':
						globals.add_all.append('add-all')
						
		if input.find('CollectionSheet/Revisions/Event/Date').text:
			if template.find('eadheader/revisiondesc') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_revisions = raw_input("You entered revisions but there is no <revisiondesc> tag in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_revisions.lower() == 'yes' or add_revisions.lower() == 'y':
						globals.new_elements.append('add_lang1')
					elif add_revisions.lower() == 'yesall':
						globals.add_all.append('add-all')
						
						
	#ead3 only questions
	if template.find('control') is None:
		pass
	else:
	
		if input.find('CollectionSheet/PublicationStatus').text:
			if template.find('control/publicationstatus') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_pubstatus = raw_input("You entered a Publication Status but there is no <publicationstatus> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_pubstatus.lower() == 'yes' or add_pubstatus.lower() == 'y':
						globals.new_elements.append('add_pubstatus')
					elif add_pubstatus.lower() == 'yesall':
						globals.add_all.append('add-all')
						
		if input.find('CollectionSheet/FindingAidLanguages/FALanguage/Lang').text:
			if template.find('control/languagedeclaration') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_langdec = raw_input("You entered a Finding Aid Language  or a Language Description but there is no <languagedeclaration> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_langdec.lower() == 'yes' or add_langdec.lower() == 'y':
						globals.new_elements.append('add_langdec')
					elif add_langdec.lower() == 'yesall':
						globals.add_all.append('add-all')
						
		if input.find('CollectionSheet/StandardConventions/Convention/Citation').text:
			if template.find('control/conventiondeclaration') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_stancon = raw_input("You entered a Standard Convention but there is no <conventiondeclaration> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_stancon.lower() == 'yes' or add_stancon.lower() == 'y':
						globals.new_elements.append('add_stancon')
					elif add_stancon.lower() == 'yesall':
						globals.add_all.append('add-all')
						
		if input.find('CollectionSheet/LocalConventions/Convention/Citation').text:
			if template.find('control/localtypedeclaration') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_localcon = raw_input("You entered a Local Convention but there is no <localtypedeclaration> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_localcon.lower() == 'yes' or add_localcon.lower() == 'y':
						globals.new_elements.append('add_localcon')
					elif add_localcon.lower() == 'yesall':
						globals.add_all.append('add-all')
						
		if input.find('CollectionSheet/LocalControls/Control/Term').text:
			if template.find('control/localcontrol') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_localctr = raw_input("You entered a Local Control but there is no <localcontrol> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_localctr.lower() == 'yes' or add_localctr.lower() == 'y':
						globals.new_elements.append('add_localctr')
					elif add_localctr.lower() == 'yesall':
						globals.add_all.append('add-all')
						
						
		if input.find('CollectionSheet/OutsideSources/Source/SourceName').text:
			if template.find('control/sources') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_sources = raw_input("You entered a external sources but there is no <sources> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_sources.lower() == 'yes' or add_sources.lower() == 'y':
						globals.new_elements.append('add_sources')
					elif add_sources.lower() == 'yesall':
						globals.add_all.append('add-all')
						
		if input.find('CollectionSheet/Relations/Relation/RelationEntry').text or input.find('CollectionSheet/Relations/Relation/RelationLink').text or input.find('CollectionSheet/Relations/Relation/RelationNote').text:
			if template.find('relations') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_relation = raw_input("You entered Relations but there is no <relations> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_relation.lower() == 'yes' or add_relation.lower() == 'y':
						globals.new_elements.append('add_relation')
					elif add_relation.lower() == 'yesall':
						globals.add_all.append('add-all')
	

	# archdesc questions
		#did
	
	if input.find('CollectionSheet/CollectionID').text:
		if template.find("archdesc/did/unitid") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_unitid = raw_input("Your EAD template does not contain a <unitid> within the collection-level <did>. EADMachine recommends that you add a <unitid> here. Would you like to do so? ('y', 'n' or 'yesall')")
				if add_unitid.lower() == 'yes' or add_unitid.lower() == 'y':
					globals.new_elements.append('add_unitid')
				elif add_unitid.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/DateBulk').text:
		if template.find("archdesc/did/unitdate[@type='bulk']") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_bulkdate = raw_input("You entered a collection-level bulk date for this collection but there is no <unitdate type='bulk'> tags in you EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_bulkdate.lower() == 'yes' or add_bulkdate.lower() == 'y':
					globals.new_elements.append('add_bulkdate')
				elif add_bulkdate.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/Abstract').text:
		if template.find("archdesc/did/abstract") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_abstract = raw_input("You entered an Abstract but your EAD template does not contain an <abstract> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_abstract.lower() == 'yes' or add_abstract.lower() == 'y':
					globals.new_elements.append('add_abstract')
				elif add_abstract.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/Origins/Origination/Part').text:
		if template.find('archdesc/did/origination') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_origin = raw_input("You entered Origination information but your EAD template does not contain an <origination> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_origin.lower() == 'yes' or add_origin.lower() == 'y':
					globals.new_elements.append('add_origin')
				elif add_origin.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	#did/physdesc and physdescstructured
	if template.find('control') is None:
		if input.find('CollectionSheet/PhysicalDescriptionSet/PhysicalDescription/Quantity').text or input.find('CollectionSheet/PhysicalDescriptionSet/PhysicalDescription/Dimensions').text:
			if template.find('archdesc/did/physdesc') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_physdesc = raw_input("You entered collection-level Physical Description but your EAD template does not contain a <physdesc> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_physdesc.lower() == 'yes' or add_physdesc.lower() == 'y':
						globals.new_elements.append('add_physdesc')
					elif add_physdesc.lower() == 'yesall':
						globals.add_all.append('add-all')
	else:
		if input.find('CollectionSheet/PhysicalDescriptionSet/PhysicalDescription/Quantity').text or input.find('CollectionSheet/PhysicalDescriptionSet/PhysicalDescription/Dimensions').text:
			if template.find('archdesc/did/physdescstructured') is None:
				if "add-all" in globals.add_all:
					pass
				else:
					add_physdesc = raw_input("You entered collection-level Physical Description but your EAD template does not contain a <physdesc> or <physdescstructured> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
					if add_physdesc.lower() == 'yes' or add_physdesc.lower() == 'y':
						globals.new_elements.append('add_physdesc')
					elif add_physdesc.lower() == 'yesall':
						globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/Languages/Language/Lang').text:
		if template.find("archdesc/did/langmaterial") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_langmat = raw_input("You entered a Collection Language  or a Language Description but there is no <languagematerial> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_langmat.lower() == 'yes' or add_langmat.lower() == 'y':
					globals.new_elements.append('add_langmat')
				elif add_langmat.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/Access/Statement').text or input.find('CollectionSheet/Access/SpecificMaterialRestrictions/SpecificRestriction/Restriction').text:
		if template.find("archdesc/accessrestrict") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_accessrestrict = raw_input("You entered Access Restrictions but there is no <accessrestrict> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_accessrestrict.lower() == 'yes' or add_accessrestrict.lower() == 'y':
					globals.new_elements.append('add_accessrestrict')
				elif add_accessrestrict.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/Accruals/Accrual').text:
		if template.find("archdesc/accruals") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_accruals = raw_input("You entered Accruals but there is no <accruals> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_accruals.lower() == 'yes' or add_accruals.lower() == 'y':
					globals.new_elements.append('add_accruals')
				elif add_accruals.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/AcquisitionInfo/Acquis/Event').text:
		if template.find("archdesc/acqinfo") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_acq = raw_input("You entered Acquisition Information but there is no <acqinfo> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_acq.lower() == 'yes' or add_acq.lower() == 'y':
					globals.new_elements.append('add_acq')
				elif add_acq.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/AlternateForms/Alternative').text:
		if template.find("archdesc/altformavail") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_altforms = raw_input("You entered Alternate Forms or Copies but there is no <altformavail> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_altforms.lower() == 'yes' or add_altforms.lower() == 'y':
					globals.new_elements.append('add_altforms')
				elif add_altforms.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/AppraisalInfo/Appraisal').text:
		if template.find("archdesc/appraisal") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_appraisal = raw_input("You entered Appraisal information but there is no <appraisal> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_appraisal.lower() == 'yes' or add_appraisal.lower() == 'y':
					globals.new_elements.append('add_appraisal')
				elif add_appraisal.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/CollectionArrangement/Arrangement').text:
		if template.find("archdesc/arrangement") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_arrange = raw_input("You entered Arrangement information but there is no <arrangement> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_arrange.lower() == 'yes' or add_arrange.lower() == 'y':
					globals.new_elements.append('add_arrange')
				elif add_arrange.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/PublicationBibliography/Publication/Title').text or CSheet.find('CollectionSheet/ManuscriptBibliography/Manuscript/UnitTitle').text:
		if template.find('archdesc/bibliography') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_biblio = raw_input("You entered a Bibliography but there is no <bibliography> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_biblio.lower() == 'yes' or add_biblio.lower() == 'y':
					globals.new_elements.append('add_biblio')
				elif add_biblio.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/HistoricalNote/p').text:
		if template.find('archdesc/bioghist') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_bio = raw_input("You entered a Historical Note but there is no <bioghist> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_bio.lower() == 'yes' or add_bio.lower() == 'y':
					globals.new_elements.append('add_bio')
				elif add_bio.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/ControlledAccess/AccessPoint/Part').text and input.find('CollectionSheet/ControlledAccess/AccessPoint/ElementName').text:
		if template.find('archdesc/controlaccess') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_controlaccess = raw_input("You entered Controlled Access points but your EAD template does not contain a <controlaccess> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_controlaccess.lower() == 'yes' or add_controlaccess.lower() == 'y':
					globals.new_elements.append('add_controlaccess')
				elif add_controlaccess.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/CustodialHistory/Event').text:
		if template.find('archdesc/custodhist') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_custhistory = raw_input("You entered Custodial History but your EAD template does not contain a <custodhist> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_custhistory.lower() == 'yes' or add_custhistory.lower() == 'y':
					globals.new_elements.append('add_custhistory')
				elif add_custhistory.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/LegalStatus/Status').text:
		if template.find('archdesc/legalstatus') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_legalstatus = raw_input("You entered Legal Status information but your EAD template does not contain a <legalstatus> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_legalstatus.lower() == 'yes' or add_legalstatus.lower() == 'y':
					globals.new_elements.append('add_legalstatus')
				elif add_legalstatus.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/OtherFindingAids/Other').text:
		if template.find('archdesc/otherfindaid') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_otherfa = raw_input("You entered Other Finding Aids but your EAD template does not contain an <otherfindaid> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_otherfa.lower() == 'yes' or add_otherfa.lower() == 'y':
					globals.new_elements.append('add_otherfa')
				elif add_otherfa.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/PhysicalTechnical/Details').text:
		if template.find('archdesc/phystech') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_phystech = raw_input("You entered Physical or Technical details but your EAD template does not contain a <phystech> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_phystech.lower() == 'yes' or add_phystech.lower() == 'y':
					globals.new_elements.append('add_phystech')
				elif add_phystech.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/PreferredCitation/Example').text:
		if template.find('archdesc/prefercite') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_prefcite = raw_input("You entered a Preferred Citation but your EAD template does not contain a <prefercite> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_prefcite.lower() == 'yes' or add_prefcite.lower() == 'y':
					globals.new_elements.append('add_prefcite')
				elif add_prefcite.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/ProcessingInformation/Details').text:
		if template.find('archdesc/processinfo') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_processinfo = raw_input("You entered Processing information but your EAD template does not contain a <processinfo> element, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_processinfo.lower() == 'yes' or add_processinfo.lower() == 'y':
					globals.new_elements.append('add_processinfo')
				elif add_processinfo.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/RelatedPublications/Publication/Title').text or CSheet.find('CollectionSheet/RelatedManuscripts/Manuscript/UnitTitle').text:
		if template.find('archdesc/relatedmaterial') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_related = raw_input("You entered Related Material but there is no <relatedmaterial> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_related.lower() == 'yes' or add_related.lower() == 'y':
					globals.new_elements.append('add_related')
				elif add_related.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/ScopeContent/p').text:
		if template.find('archdesc/scopecontent') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_scope = raw_input("You entered a Scope note but there is no <scopecontent> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_scope.lower() == 'yes' or add_scope.lower() == 'y':
					globals.new_elements.append('add_scope')
				elif add_scope.lower() == 'yesall':
					globals.add_all.append('add-all')
					
	if input.find('CollectionSheet/SeparatedMaterial/Material').text:
		if template.find('archdesc/separatedmaterial') is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_sepmat = raw_input("You entered Separated Material but there is no <separatedmaterial> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_sepmat.lower() == 'yes' or add_sepmat.lower() == 'y':
					globals.new_elements.append('add_sepmat')
				elif add_sepmat.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	if input.find('CollectionSheet/UseRestrictions/Statement').text or input.find('CollectionSheet/UseRestrictions/SpecificMaterialRestrictions/SpecificRestriction/Restriction').text:
		if template.find("archdesc/userestrict") is None:
			if "add-all" in globals.add_all:
				pass
			else:
				add_userestrict = raw_input("You entered Use Restrictions but there is no <userestrict> tag in your EAD template, would you like EADMachine to add one for this collection? ('y', 'n' or 'yesall')")
				if add_userestrict.lower() == 'yes' or add_userestrict.lower() == 'y':
					globals.new_elements.append('add_userestrict')
				elif add_userestrict.lower() == 'yesall':
					globals.add_all.append('add-all')
	
	# HTML export question
	ask_html = raw_input("Do you want to create a single-page HTML <html> file for this collection?")
	if ask_html.lower() == 'yes' or ask_html.lower() == 'y':
		globals.new_elements.append('ask_html')