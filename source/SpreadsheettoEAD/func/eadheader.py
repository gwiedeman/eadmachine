# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals
from messages import error

def eadheader(eadheader_root, CSheet):
	
	#update GUI progress bar
	if "ask_gui" in globals.new_elements: 
		import wx
		from wx.lib.pubsub import pub
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <eadheader>...")
	
	# <eadheader> @findaidstatus
	if CSheet.find('DraftStatus').text:
		eadheader_root.set('findaidstatus', CSheet.find('DraftStatus').text)
	elif "findaidstatus" in eadheader_root.attrib:
		eadheader_root.set('findaidstatus', "")
	
	#<eadid>
	if eadheader_root.find('eadid') is None:
		error("The EAD template you used does not contained an <eadid> tag. Since this is a required element in EAD2002, one will be added.", False)
		eadid_element = ET.Element('eadid')
		eadheader_root.insert(0, eadid_element)
	template_id = eadheader_root.find('eadid')
	if CSheet.find('CollectionID').text:
		template_id.text = CSheet.find('CollectionID').text
	else:
		error("You did not enter a CollectionID. The <eadid> tag will be empty.", False)
		template_id.text = ""
	if CSheet.find('URL').text:
		template_id.set('url', CSheet.find('URL').text)
	elif "url" in template_id.attrib:
		template_id.set('url', "")
	if CSheet.find('CountryCode').text:
		template_id.set('countrycode', CSheet.find('CountryCode').text)
	
	#<filedesc>
	if eadheader_root.find('filedesc') is None:
		error("The EAD template you used does not contain a <filedesc> tag. Since this is a required element in EAD2002, one will be added.", False)
		filedesc_element = ET.Element('filedesc')
		eadheader_root.insert(1, filedesc_element)
	#<titlestmt>
	if eadheader_root.find('filedesc/titlestmt') is None:
		error("The EAD template you used does not contain a <titlestmt> tag. Since this is a required element in EAD2002, one will be added.", False)
		titlestmt_element = ET.Element('titlestmt')
		eadheader_root.find('filedesc').insert(0, titlestmt_element)
	#<titleproper>
	if eadheader_root.find('filedesc/titlestmt/titleproper') is None:
		error("The EAD template you used does not contain a <titleproper> tag. Since this is a required element in EAD2002, one will be added.", False)
		titleproper_element = ET.Element('titleproper')
		eadheader_root.find('filedesc/titlestmt').insert(0, titleproper_element)
	template_titleproper = eadheader_root.find('filedesc/titlestmt/titleproper')
	if CSheet.find('CollectionName').text:
		if "ask_ualbany" in globals.new_elements:
			if "nam_" in CSheet.find('CollectionID').text:
				CID_only = CSheet.find('CollectionID').text.split('_')[1]
			else:
				CID_only = CSheet.find('CollectionID').text
			if CID_only.lower().startswith('ua'):
				Coll_number = CID_only.replace('ua', '')
				display_CID = "UA-" +  Coll_number
			elif CID_only.lower().startswith('apap'):
				Coll_number = CID_only.replace('apap', '')
				display_CID = "APAP-" +  Coll_number
			elif CID_only.lower().startswith('mss'):
				Coll_number = CID_only.replace('mss', '')
				display_CID = "MSS-" +  Coll_number
			elif CID_only.lower().startswith('ger'):
				Coll_number = CID_only.replace('ger', '')
				display_CID = "GER-" +  Coll_number
			else:
				display_CID = CID_only
			ualbany_titleproper = CSheet.find('CollectionName').text.upper() + " (" + display_CID.upper() + "),"
			template_titleproper.text = ualbany_titleproper
		else:
			template_titleproper.text = CSheet.find('CollectionName').text
	else:
		template_titleproper.text  = ""
		
	#<date>
	if eadheader_root.find('filedesc/titlestmt/titleproper/date') is None:
		pass
	else:
		template_date = eadheader_root.find('filedesc/titlestmt/titleproper/date')
		if CSheet.find('DateInclusive').text:
			template_date.text = CSheet.find('DateInclusive').text
			if CSheet.find('DateInclusiveNormal').text:
				template_date.attrib['normal'] = CSheet.find('DateInclusiveNormal').text
			else:
				template_date.attrib['normal'] = CSheet.find('DateInclusive').text
		else:
			if eadheader_root.find('filedesc/titlestmt/titleproper/date') is None:
				pass
			else:
				eadheader_root.find('filedesc/titlestmt/titleproper/date').text = ""
			
	#<subtitle>
	if CSheet.find('Subtitle').text:
		if eadheader_root.find('filedesc/titlestmt/subtitle') is None:
			if "add_subtitle" in globals.new_elements or "add-all" in globals.add_all:
				subtitle_element = ET.Element('subtitle')
				eadheader_root.find('filedesc/titlestmt').insert(1, subtitle_element)
				subtitle_element.text = CSheet.find('Subtitle').text
		else:
			old_sub_list = eadheader_root.find('filedesc/titlestmt').findall('subtitle')
			for old_sub in old_sub_list:
				eadheader_root.find('filedesc/titlestmt').remove(old_sub)
			subtitle_element = ET.Element('subtitle')
			eadheader_root.find('filedesc/titlestmt').insert(1, subtitle_element)
			subtitle_element.text = CSheet.find('Subtitle').text
	else:
		old_sub_list = eadheader_root.find('filedesc/titlestmt').findall('subtitle')
		for old_sub in old_sub_list:
			eadheader_root.find('filedesc/titlestmt').remove(old_sub)
	
	#<author>
	if CSheet.find('ProcessedBy').text:
		if eadheader_root.find('filedesc/titlestmt/author') is None:
			if "add_author" in globals.new_elements or "add-all" in globals.add_all:
				author_element = ET.Element('author')
				if eadheader_root.find('filedesc/titlestmt/subtitle') is None:
					author_index = 1
				else:
					author_index = 2
				eadheader_root.find('filedesc/titlestmt').insert(author_index, author_element)
				author_element.text = CSheet.find('ProcessedBy').text
		else:
			eadheader_root.find('filedesc/titlestmt/author').text = CSheet.find('ProcessedBy').text
	else:
		old_auth_list = eadheader_root.find('filedesc/titlestmt').findall('author')
		for old_auth in old_auth_list:
			eadheader_root.find('filedesc/titlestmt').remove(old_auth)
	
	#<sponsor>
	if CSheet.find('Sponsor').text:
		if eadheader_root.find('filedesc/titlestmt/sponsor') is None:
			if "add_sponsor" in globals.new_elements or "add-all" in globals.add_all:
				sponsor_element = ET.Element('sponsor')
				eadheader_root.find('filedesc/titlestmt').append(sponsor_element)
				sponsor_element.text = CSheet.find('Sponsor').text
		else:
			eadheader_root.find('filedesc/titlestmt/sponsor').text = CSheet.find("Sponsor").text
	else:
		old_spon_list = eadheader_root.find('filedesc/titlestmt').findall('sponsor')
		for old_spon in old_spon_list:
			eadheader_root.find('filedesc/titlestmt').remove(old_spon)
            
	
	# Edition Statement Section
	from editionstmt import editionstmt
	editionstmt(eadheader_root, CSheet)
	
	# Publication Statement Section
	from publicationstmt import publicationstmt
	publicationstmt(eadheader_root, CSheet)
	
	# Series Statement Section
	from seriesstmt import seriesstmt
	seriesstmt(eadheader_root, CSheet)
	
	# Note Statement Section
	if CSheet.find('NoteStatements/NoteStatement') is None:
		pass
	else:
		if CSheet.find('NoteStatements/NoteStatement').text:
			if eadheader_root.find('filedesc/notestmt') is None:
				if "add_notestmt" in globals.new_elements or "add-all" in globals.add_all:
					notestmt_element = ET.Element('notestmt')
					eadheader_root.find('filedesc').append(notestmt_element)
					notestmt = eadheader_root.find('filedesc/notestmt')
					for note_info in CSheet.find('NoteStatements'):
						cnote_element = ET.Element('note')
						p_element = ET.Element('p')
						notestmt.append(cnote_element)
						cnote_element.append(p_element)
						p_element.text = note_info.text
			else:
				notestmt = eadheader_root.find('filedesc/notestmt')
				notestmt.clear()
				for note_info in CSheet.find('NoteStatements'):
					cnote_element = ET.Element('note')
					p_element = ET.Element('p')
					notestmt.append(cnote_element)
					cnote_element.append(p_element)
					p_element.text = note_info.text
	
	# Profile Description
	if CSheet.find('EADCreator').text or CSheet.find('EADCreationDate').text or CSheet.find('FindingAidLanguages/FALanguage/Lang').text or CSheet.find('StandardConventions/Convention/Citation').text or CSheet.find('LocalConventions/Convention/Citation').text:
		if eadheader_root.find('profiledesc') is None:
			if "add_profile" in globals.new_elements or "add-all" in globals.add_all:
				profile_element = ET.Element('profiledesc')
				last_filedesc = eadheader_root.getchildren().index(eadheader_root.find('filedesc')) + 1
				eadheader_root.insert(last_filedesc, profile_element)
	else:
		if eadheader_root.find('profiledesc') is None:
			pass
		else:
			eadheader_root.find('profiledesc').clear()

	# EAD creation and EAD creation date
	if CSheet.find('EADCreator').text or CSheet.find('EADCreationDate').text:
		if eadheader_root.find('profiledesc') is None:
			pass
		else:
			if eadheader_root.find('profiledesc/creation') is None:
				if "add_eadcre" in globals.new_elements or "add-all" in globals.add_all:
					creator_element = ET.Element('creation')
					eadheader_root.find('profiledesc').insert(0, creator_element)
					if CSheet.find('EADCreator').text:
						creator_element.text = CSheet.find('EADCreator').text
					if CSheet.find('EADCreationDate').text:
						credate_element = ET. Element('date')
						creator_element.append(credate_element)
						credate_element.text = CSheet.find('EADCreationDate').text
						if CSheet.find('EADCreationDateNormal').text is None:
							credate_element.attrib['normal'] = CSheet.find('EADCreationDate').text
						else:
							credate_element.attrib['normal'] = CSheet.find('EADCreationDateNormal').text
			else:
				template_creator = eadheader_root.find('profiledesc/creation')
				if CSheet.find('EADCreator').text:
					template_creator.text = CSheet.find('EADCreator').text
				if CSheet.find('EADCreationDate').text:
					if template_creator.find('date') is None:
						template_creator.text = template_creator.text + " - " + CSheet.find('EADCreationDate').text
					else:
						template_creatordate = template_creator.find('date')
						template_creatordate.text = CSheet.find('EADCreationDate').text
						if CSheet.find('EADCreationDateNormal').text is None:
							template_creatordate.attrib['normal'] = CSheet.find('EADCreationDate').text
						else:
							template_creatordate.attrib['normal'] = CSheet.find('EADCreationDateNormal').text
	
	# Languages
	if CSheet.find('FindingAidLanguages/FALanguage/Lang').text:
		if eadheader_root.find('profiledesc') is None:
			pass
		else:
			if eadheader_root.find('profiledesc/langusage') is None:
				if "add_lang1" in globals.new_elements or "add-all" in globals.add_all:
					langusage_element = ET.Element('langusage')
					eadheader_root.find('profiledesc').append(langusage_element)
					for lang in CSheet.find('FindingAidLanguages'):
						if lang.find('Lang').text:
							lang_element = ET.Element('language')
							eadheader_root.find('profiledesc/langusage').append(lang_element)
							lang_element.text = lang.find('Lang').text
							if lang.find('LangCode').text:
								lang_element.set('langcode', lang.find('LangCode').text)
							if lang.find('LangNote').text:
								lang_element.tail =  ", " + lang.find('LangNote').text
			else:
				if eadheader_root.find('profiledesc/langusage/language') is None:
					for lang in CSheet.find('FindingA:idLanguages'):
						if lang.find('Lang').text:
							lang_element = ET.Element('language')
							eadheader_root.find('profiledesc/langusage').append(lang_element)
							lang_element.text = lang.find('Lang').text
							if lang.find('LangCode').text:
								lang_element.set('langcode', lang.find('LangCode').text)
							if lang.find('LangNote').text:
								lang_element.tail =  ", " + lang.find('LangNote').text
				else:
					lang_attrib = eadheader_root.find('profiledesc/langusage/language').attrib.get("encodinganalog", None)
					eadheader_root.find('profiledesc/langusage').clear()
					for lang in CSheet.find('FindingAidLanguages'):
						if lang.find('Lang').text:
							lang_element = ET.Element('language')
							if lang_attrib is None:
								pass
							else:
								if len(lang_attrib) > 0:
									lang_element.set('encodinganalog', lang_attrib)
							eadheader_root.find('profiledesc/langusage').append(lang_element)
							lang_element.text = lang.find('Lang').text
							if lang.find('LangCode').text:
								lang_element.set('langcode', lang.find('LangCode').text)
							if lang.find('LangNote').text:
								lang_element.tail =  ", " + lang.find('LangNote').text
	
	#update GUI progress bar
	if "ask_gui" in globals.new_elements: 
		import wx
		from wx.lib.pubsub import pub
		wx.CallAfter(pub.sendMessage, "update", msg="Writing description rules...")

	# Description Rules
	if CSheet.find('StandardConventions/Convention/Citation').text or CSheet.find('LocalConventions/Convention/Citation').text:
		if eadheader_root.find('profiledesc') is None:
			pass
		else:
			if eadheader_root.find('profiledesc/descrules') is None:
				if "add_descrule" in globals.new_elements or "add-all" in globals.add_all:
					descrule_element = ET.Element('descrules')
					eadheader_root.find('profiledesc').append(descrule_element)
					for rule in CSheet.find('StandardConventions'):
						if rule.find('Citation').text:
							if rule.find('Abbreviation').text:
								if eadheader_root.find('profiledesc/descrules').text:
									eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ", " + rule.find('Citation').text + " (" + rule.find('Abbreviation').text + ")"
								else:
									eadheader_root.find('profiledesc/descrules').text = rule.find('Citation').text + " (" + rule.find('Abbreviation').text + ")"
							else:
								if eadheader_root.find('profiledesc/descrules').text:
									eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ", " + rule.find('Citation').text
								else:
									eadheader_root.find('profiledesc/descrules').text = rule.find('Citation').text
							if rule.find('ConventionLink').text:
								eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ": " + rule.find('ConventionLink').text
					for rule in CSheet.find('LocalConventions'):
						if rule.find('Citation').text:
							if rule.find('Abbreviation').text:
								if eadheader_root.find('profiledesc/descrules').text:
									eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ", " + rule.find('Citation').text + " (" + rule.find('Abbreviation').text + ")"
								else:
									eadheader_root.find('profiledesc/descrules').text = rule.find('Citation').text + " (" + rule.find('Abbreviation').text + ")"
							else:
								if eadheader_root.find('profiledesc/descrules').text:
									eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ", " + rule.find('Citation').text
								else:
									eadheader_root.find('profiledesc/descrules').text = rule.find('Citation').text
							if rule.find('ConventionLink').text:
								eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ": " + rule.find('ConventionLink').text
			else:
				eadheader_root.find('profiledesc/descrules').clear()
				for rule in CSheet.find('StandardConventions'):
					if rule.find('Citation').text:
						if rule.find('Abbreviation').text:
							if eadheader_root.find('profiledesc/descrules').text:
								eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ", " + rule.find('Citation').text + " (" + rule.find('Abbreviation').text + ")"
							else:
								eadheader_root.find('profiledesc/descrules').text = rule.find('Citation').text + " (" + rule.find('Abbreviation').text + ")"
						else:
							if eadheader_root.find('profiledesc/descrules').text:
								eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ", " + rule.find('Citation').text
							else:
								eadheader_root.find('profiledesc/descrules').text = rule.find('Citation').text
						if rule.find('ConventionLink').text:
							eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ": " + rule.find('ConventionLink').text
				for rule in CSheet.find('LocalConventions'):
					if rule.find('Citation').text:
						if rule.find('Abbreviation').text:
							if eadheader_root.find('profiledesc/descrules').text:
								eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ", " + rule.find('Citation').text + " (" + rule.find('Abbreviation').text + ")"
							else:
								eadheader_root.find('profiledesc/descrules').text = rule.find('Citation').text + " (" + rule.find('Abbreviation').text + ")"
						else:
							if eadheader_root.find('profiledesc/descrules').text:
								eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ", " + rule.find('Citation').text
							else:
								eadheader_root.find('profiledesc/descrules').text = rule.find('Citation').text
						if rule.find('ConventionLink').text:
							eadheader_root.find('profiledesc/descrules').text = eadheader_root.find('profiledesc/descrules').text + ": " + rule.find('ConventionLink').text
	
	if "ask_gui" in globals.new_elements: 
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <revisiondesc>...")
	# revision
	if CSheet.find('Revisions/Event/Date') is None:
		pass
	else:
		if CSheet.find('Revisions/Event/Date').text:
			if eadheader_root.find('revisiondesc') is None:
				if "add_revisions" in globals.new_elements or "add-all" in globals.add_all:
					rev_element = ET.Element('revisiondesc')
					if eadheader_root.find('profiledesc') is None:
						revision_place = 2
					else:
						revision_place = 3
					eadheader_root.insert(revision_place, rev_element)
					revision_root = eadheader_root.find('revisiondesc')
					for event in CSheet.find('Revisions'):
						change_element = ET.Element('change')
						revision_root.append(change_element)
						date_element = ET.Element('date')
						change_element.append(date_element)
						date_element.text = event.find('Date').text
						if event.find('DateNormal').text:
							date_element.set('normal', event.find('DateNormal').text)
						else:
							date_element.set('normal', event.find('Date').text)
						item_element = ET.Element('item')
						change_element.append(item_element)
						if event.find('Type').text:
							item_element.text = event.find('Type').text
							if event.find('Description').text:
								item_element.text = item_element.text +': ' + event.find('Description').text
								if event.find('Agent').text:
									item_element.text = item_element.text + ' (' + event.find('Agent').text + ')'
						elif event.find('Description').text:
							item_element.text = event.find('Description').text
							if event.find('Agent').text:
								item_element.text = item_element.text + ' (' + event.find('Agent').text + ')'
			else:
				revision_root = eadheader_root.find('revisiondesc')
				if revision_root.find('list') is None and revision_root.find('change') is None: #if nothing
					for event in CSheet.find('Revisions'):
						change_element = ET.Element('change')
						revision_root.append(change_element)
						date_element = ET.Element('date')
						change_element.append(date_element)
						date_element.text = event.find('Date').text
						if event.find('DateNormal').text:
							date_element.set('normal', event.find('DateNormal').text)
						item_element = ET.Element('item')
						change_element.append(item_element)
						if event.find('Type').text:
							item_element.text = event.find('Type').text
							if event.find('Description').text:
								item_element.text = item_element.text +': ' + event.find('Description').text
								if event.find('Agent').text:
									item_element.text = item_element.text + ' (' + event.find('Agent').text + ')'
						elif event.find('Description').text:
							item_element.text = event.find('Description').text
							if event.find('Agent').text:
								item_element.text = item_element.text + ' (' + event.find('Agent').text + ')'
				elif revision_root.find('change') is None: #if list
					revision_root.find('list').clear()
					for event in CSheet.find('Revisions'):
						item_element = ET.Element('item')
						revision_root.find('list').append(item_element)
						date_element = ET.Element('date')
						item_element.append(date_element)
						date_element.text = event.find('Date').text
						if event.find('DateNormal').text:
							date_element.set('normal', event.find('DateNormal').text)
						if event.find('Type').text:
							item_element.text = event.find('Type').text
							if event.find('Description').text:
								item_element.text = item_element.text +': ' + event.find('Description').text
								if event.find('Agent').text:
									item_element.text = item_element.text + ' (' + event.find('Agent').text + ')'
						elif event.find('Description').text:
							item_element.text = event.find('Description').text
							if event.find('Agent').text:
								item_element.text = item_element.text + ' (' + event.find('Agent').text + ')'
				else: # if change
					revision_root.clear()
					for event in CSheet.find('Revisions'):
						change_element = ET.Element('change')
						revision_root.append(change_element)
						date_element = ET.Element('date')
						change_element.append(date_element)
						date_element.text = event.find('Date').text
						if event.find('DateNormal').text:
							date_element.set('normal', event.find('DateNormal').text)
						item_element = ET.Element('item')
						change_element.append(item_element)
						if event.find('Type').text:
							item_element.text = event.find('Type').text
							if event.find('Description').text:
								item_element.text = item_element.text +': ' + event.find('Description').text
								if event.find('Agent').text:
									item_element.text = item_element.text + ' (' + event.find('Agent').text + ')'
						elif event.find('Description').text:
							item_element.text = event.find('Description').text
							if event.find('Agent').text:
								item_element.text = item_element.text + ' (' + event.find('Agent').text + ')'			
