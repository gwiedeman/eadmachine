# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals
from messages import error

def control(control_root, CSheet):

	#update GUI progress bar
	if "ask_gui" in globals.new_elements: 
		import wx
		from wx.lib.pubsub import pub
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <control>...")
	
	#<recordid>
	if control_root.find('recordid') is None:
		error("Your template does not include a <recordid> element. This element is mandatory in EAD3, so your finding aid will not be valid.", False)
	template_id = control_root.find('recordid')
	template_id.text = CSheet.find('CollectionID').text
	if CSheet.find('URL').text:
		template_id.set('instanceurl', CSheet.find('URL').text)
	else:
		template_id.set('instanceurl', "")
	
	# Other Record IDs Section
	if CSheet.find('OtherID/ID').text:
		if control_root.find('otherrecordid') is None:
			if "add_otherid" in globals.new_elements or "add-all" in globals.add_all:
				for new_otherid in reversed(CSheet):
					if new_otherid.tag == "OtherID":
						otherid_element = ET.Element('otherrecordid')
						last_recordid = control_root.getchildren().index(control_root.find('recordid')) + 1
						control_root.insert(last_recordid, otherid_element)
						otherid_element.text = new_otherid.find('ID').text
						otherid_element.set('localtype', new_otherid.find('LocalType').text)
		else:
			old_otherid_list = control_root.findall('otherrecordid')
			for old_otherid in old_otherid_list:
				control_root.remove(old_otherid)
			for new_otherid in reversed(CSheet):
				if new_otherid.tag == "OtherID":
					otherid_element = ET.Element('otherrecordid')
					last_recordid = control_root.getchildren().index(control_root.find('recordid')) + 1
					control_root.insert(last_recordid, otherid_element)
					otherid_element.text = new_otherid.find('ID').text
					otherid_element.set('localtype', new_otherid.find('LocalType').text)
	else:
		old_otherid_list = control_root.findall('otherrecordid')
		for old_otherid in old_otherid_list:
			control_root.remove(old_otherid)
		
	# Representations Section, for HTML derivatives, etc.
	if CSheet.find('Representation/RepName').text:
		if control_root.find('representation') is None:
			if "add_rep" in globals.new_elements or "add-all" in globals.add_all:
				for new_rep in reversed(CSheet):
					if new_rep.tag == "Representation":
						rep_element = ET.Element('representation')
						if control_root.find('otherrecordid') is None:
							before_element = 'recordid'
						else:
							before_element = 'otherrecordid'
						last_id = control_root.getchildren().index(control_root.find(before_element)) + 1
						control_root.insert(last_id, rep_element)
						rep_element.set('href', new_rep.find('Link').text)
						rep_element.set('linktitle', new_rep.find('RepName').text)
						rep_element.set('show', new_rep.find('Show').text)
		else:
			old_rep_list = control_root.findall('representation')
			for old_rep in old_rep_list:
				control_root.remove(old_rep)
			for new_rep in reversed(CSheet):
				if new_rep.tag == "Representation":
					rep_element = ET.Element('representation')
					if control_root.find('otherrecordid') is None:
						before_element = 'recordid'
					else:
						before_element = 'otherrecordid'
					last_id = control_root.getchildren().index(control_root.find(before_element)) + 1
					control_root.insert(last_id, rep_element)
					rep_element.set('href', new_rep.find('Link').text)
					rep_element.set('linktitle', new_rep.find('RepName').text)
					rep_element.set('show', new_rep.find('Show').text)
	else:
		old_rep_list = control_root.findall('representation')
		for old_rep in old_rep_list:
			control_root.remove(old_rep)

	template_titleproper = control_root.find('filedesc/titlestmt/titleproper')
	if CSheet.find('CollectionName').text:
		template_titleproper.text = CSheet.find('CollectionName').text
	else:
		template_titleproper.text = ""
		error("You did not enter a Collection Name. <titleproper> is mandatory in EAD3, so your finding aid will not be valid.", False)
	
	# <subtitle>
	if CSheet.find('Subtitle').text:
		if control_root.find('filedesc/titlestmt/subtitle') is None:
			if "add_subtitle" in globals.new_elements or "add-all" in globals.add_all:
				subtitle_element = ET.Element('subtitle')
				control_root.find('filedesc/titlestmt').insert(1, subtitle_element)
				subtitle_element.text = CSheet.find('Subtitle').text
		else:
			old_sub_list = control_root.find('filedesc/titlestmt').findall('subtitle')
			for old_sub in old_sub_list:
				control_root.find('filedesc/titlestmt').remove(old_sub)
			subtitle_element = ET.Element('subtitle')
			control_root.find('filedesc/titlestmt').insert(1, subtitle_element)
			subtitle_element.text = CSheet.find('Subtitle').text
	else:
		old_sub_list = control_root.find('filedesc/titlestmt').findall('subtitle')
		for old_sub in old_sub_list:
			control_root.find('filedesc/titlestmt').remove(old_sub)
	
	#<author>
	if CSheet.find('ProcessedBy').text:
		if control_root.find('filedesc/titlestmt/author') is None:
			if "add_author" in globals.new_elements or "add-all" in globals.add_all:
				author_element = ET.Element('author')
				if control_root.find('filedesc/titlestmt/subtitle') is None:
					author_index = 1
				else:
					author_index = 2
				control_root.find('filedesc/titlestmt').insert(author_index, author_element)
				author_element.text = CSheet.find('ProcessedBy').text
		else:
			control_root.find('filedesc/titlestmt/author').text = CSheet.find('ProcessedBy').text
	else:
		old_auth_list = control_root.find('filedesc/titlestmt').findall('author')
		for old_auth in old_auth_list:
			control_root.find('filedesc/titlestmt').remove(old_auth)
	
	# <sponsor>
	if CSheet.find('Sponsor').text:
		if control_root.find('filedesc/titlestmt/sponsor') is None:
			if "add_sponsor" in globals.new_elements or "add-all" in globals.add_all:
				sponsor_par = control_root.find('filedesc/titlestmt')
				sponsor_element = ET.Element('sponsor')
				sponsor_par.append(sponsor_element)
				sponsor_element.text = CSheet.find('Sponsor').text
		else:
			template_sponsor = control_root.find('filedesc/titlestmt/sponsor')
			template_sponsor.text = CSheet.find("Sponsor").text
	else:
		old_spon_list = control_root.find('filedesc/titlestmt').findall('sponsor')
		for old_spon in old_spon_list:
			control_root.find('filedesc/titlestmt').remove(old_spon)
	
	# Edition Statement Section
	from editionstmt import editionstmt
	editionstmt(control_root, CSheet)
	
	# Publication Statement Section
	from publicationstmt import publicationstmt
	publicationstmt(control_root, CSheet)
	
	# Series Statement Section
	from seriesstmt import seriesstmt
	seriesstmt(control_root, CSheet)
	
	# Note Statement Section
	if CSheet.find('NoteStatements/NoteStatement') is None:
		pass
	else:
		if CSheet.find('NoteStatements/NoteStatement').text:
			if control_root.find('filedesc/notestmt') is None:
				if "add_notestmt" in globals.new_elements or "add-all" in globals.add_all:
					notestmt_element = ET.Element('notestmt')
					control_root.find('filedesc').append(notestmt_element)
					notestmt = control_root.find('filedesc/notestmt')
					for note_info in CSheet.find('NoteStatements'):
						cnote_element = ET.Element('controlnote')
						p_element = ET.Element('p')
						notestmt.append(cnote_element)
						cnote_element.append(p_element)
						p_element.text = note_info.text
			else:
				notestmt = control_root.find('filedesc/notestmt')
				notestmt.clear()
				for note_info in CSheet.find('NoteStatements'):
					cnote_element = ET.Element('controlnote')
					p_element = ET.Element('p')
					notestmt.append(cnote_element)
					cnote_element.append(p_element)
					p_element.text = note_info.text
	
	# <maintenancestatus>
	if CSheet.find('DraftStatus').text:
		draft = CSheet.find('DraftStatus').text
		if draft == "revised" or  draft == "deleted" or draft == "new" or draft =="deletedsplit" or draft == "deletedmerged" or draft =="deletedreplaced" or draft == "cancelled" or draft == "derived":
			template_draft_status = control_root.find('maintenancestatus')
			template_draft_status.set('value', CSheet.find('DraftStatus').text)
		else:
			error("Maintenance Status must be one of the following: revised, deleted, new, deletedsplit, deletedmerged, deletedreplaced, cancelled, or derived.", False)
	else:
		error("Maintenance Status <maintenancestatus> @value is required in EAD3, Draft Status must be entered or finding aid will not be valid.", False)
		template_draft_status = control_root.find('maintenancestatus')
		template_draft_status.set('value', "")
	
	# <publicationstatus>
	if CSheet.find('PublicationStatus').text:
		if control_root.find('publicationstatus') is None:
			if "add_pubstatus" in globals.new_elements or "add-all" in globals.add_all:
				pub_element = ET.Element('publicationstatus')
				control_root.insert(3, pub_element)
				pub_element.set('value', CSheet.find('PublicationStatus').text)
		else:
			template_pub_status = control_root.find('publicationstatus')
			template_pub_status.set('value', CSheet.find('PublicationStatus').text)
	else:
		old_pubstatus_list = control_root.findall('publicationstatus')
		for old_pubstatus in old_pubstatus_list:
			control_root.remove(old_pubstatus)
	
	# Maintenance Agency section
	if CSheet.find('MaintenanceAgency').text:
		if control_root.find('maintenanceagency') is None:
			main_agency_element = ET.Element('maintenanceagency')
			if control_root.find('publicationstatus') is None:
				main_agency_index = control_root.getchildren().index(control_root.find('maintenancestatus')) + 1
			else:
				main_agency_index = control_root.getchildren().index(control_root.find('publicationstatus')) + 1
			control_root.insert(main_agency_index, main_agency_element)
			agency_name = ET.Element('agencyname')
			main_agency_element.append(agency_name)
			agency_name.text = CSheet.find('MaintenanceAgency').text
			if CSheet.find('MaintenanceAgencyCode').text:
				agency_code = ET.Element('agencycode')
				main_agency_element.append(agency_code)
				agency_code.text = CSheet.find('MaintenanceAgencyCode').text
		else:
			agency_name = control_root.find('maintenanceagency/agencyname')
			agency_name.text = CSheet.find('MaintenanceAgency').text
			if CSheet.find('MaintenanceAgencyCode').text:
				control_root.find('maintenanceagency/agencycode').text = CSheet.find('MaintenanceAgencyCode').text

	else:
		error("Maintenance Agency <MaintenanceAgency> is required in EAD3, Maintenance Agency must be entered or finding aid will not be valid.", False)
		control_root.find('maintenanceagency').clear()
		agency_name = ET.Element('agencyname')
		control_root.find('maintenanceagency').append(agency_name)
		
		
	# Language Declaration section
	if CSheet.find('FindingAidLanguages/FALanguage/Lang').text:
		if control_root.find('languagedeclaration') is None:
			if "add_langdec" in globals.new_elements or "add-all" in globals.add_all:
				for new_lang in reversed(CSheet.find('FindingAidLanguages')):
					langdec_element = ET.Element('languagedeclaration')
					last_maint = control_root.getchildren().index(control_root.find('maintenanceagency')) + 1
					control_root.insert(last_maint, langdec_element)
					lang_element = ET.Element('language')
					langdec_element.insert(0, lang_element)
					lang_element.text = new_lang.find('Lang').text
					if new_lang.find('LangCode').text:
						lang_element.set('langcode', new_lang.find('LangCode').text)
					script_element = ET.Element('script')
					lang_element.append(script_element)
					script_element.text = new_lang.find('Script').text
					if new_lang.find('ScriptCode').text:
						script_element.set('scriptcode', new_lang.find('ScriptCode').text)
					if new_lang.find('LangNote').text:
						langnote_element = ET.Element('descriptivenote')
						lang_element.append(langnote_element)
						langnote_element.text = new_lang.find('LangNote').text
		else:
			old_lang_list = control_root.findall('languagedeclaration')
			for old_lang in old_lang_list:
				control_root.remove(old_lang)
			for new_lang in reversed(CSheet.find('FindingAidLanguages')):
				if new_lang.find('Lang').text:
					langdec_element = ET.Element('languagedeclaration')
					last_maint = control_root.getchildren().index(control_root.find('maintenanceagency'))+ 1
					control_root.insert(last_maint, langdec_element)
					lang_element = ET.Element('language')
					langdec_element.insert(0, lang_element)
					lang_element.text = new_lang.find('Lang').text
					if new_lang.find('LangCode').text:
						lang_element.set('langcode', new_lang.find('LangCode').text)
					script_element = ET.Element('script')
					lang_element.append(script_element)
					script_element.text = new_lang.find('Script').text
					if new_lang.find('ScriptCode').text:
						script_element.set('scriptcode', new_lang.find('ScriptCode').text)
					if new_lang.find('LangNote').text:
						langnote_element = ET.Element('descriptivenote')
						lang_element.append(langnote_element)
						langnote_element.text = new_lang.find('LangNote').text
	else:
		old_lang_list = control_root.findall('languagedeclaration')
		for old_lang in old_lang_list:
			control_root.remove(old_lang)
	
	# Convention Declaration section
	if "ask_gui" in globals.new_elements: 
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <conventiondeclaration> and <localtypedeclaration>...")
	if CSheet.find('StandardConventions/Convention/Citation').text:
		if control_root.find('conventiondeclaration') is None:
			if "add_stancon" in globals.new_elements or "add-all" in globals.add_all:
				for stancon in reversed(CSheet.find('StandardConventions')):
					stancon_element = ET.Element('conventiondeclaration')
					if control_root.find('languagedeclaration') is None:
						before_element = 'maintenanceagency'
					else:
						before_element = 'languagedeclaration'
					last_lang = control_root.getchildren().index(control_root.find(before_element)) + 1
					control_root.insert(last_lang, stancon_element)
					if stancon.find('Abbreviation').text:
						abbr_element = ET.Element('abbr')
						stancon_element.insert(0, abbr_element)
						abbr_element.text = stancon.find('Abbreviation').text
					citation_element = ET.Element('citation')
					stancon_element.append(citation_element)
					citation_element.text = stancon.find('Citation').text
					if stancon.find('ConventionLink').text:
						citation_element.set('href', stancon.find('ConventionLink').text)
					if stancon.find('Verified').text:
						citation_element.set('lastdatetimeverified', stancon.find('Verified').text)
					if stancon.find('LinkTitle').text:
						citation_element.set('linktitle', stancon.find('LinkTitle').text)
					if stancon.find('Actuate').text:
						citation_element.set('actuate', stancon.find('Actuate').text)
					if stancon.find('Show').text:
						citation_element.set('show', stancon.find('Show').text)
					if stancon.find('ConventionNote').text:
						stadesc_element = ET.Element('descriptivenote')
						stancon_element.append(stadesc_element)
						stap_element = ET.Element('p')
						stadesc_element.insert(0, stap_element)
						stap_element.text = stancon.find('ConventionNote').text
		else:
			old_conv_list = control_root.findall('conventiondeclaration')
			for old_conv in old_conv_list:
				control_root.remove(old_conv)
			for stancon in reversed(CSheet.find('StandardConventions')):
				stancon_element = ET.Element('conventiondeclaration')
				if control_root.find('languagedeclaration') is None:
					before_element = 'maintenanceagency'
				else:
					before_element = 'languagedeclaration'
				last_lang = control_root.getchildren().index(control_root.find(before_element)) + 1
				control_root.insert(last_lang, stancon_element)
				if stancon.find('Abbreviation').text:
					abbr_element = ET.Element('abbr')
					stancon_element.insert(0, abbr_element)
					abbr_element.text = stancon.find('Abbreviation').text
				citation_element = ET.Element('citation')
				stancon_element.append(citation_element)
				citation_element.text = stancon.find('Citation').text
				if stancon.find('ConventionLink').text:
					citation_element.set('href', stancon.find('ConventionLink').text)
				if stancon.find('Verified').text:
					citation_element.set('lastdatetimeverified', stancon.find('Verified').text)
				if stancon.find('LinkTitle').text:
					citation_element.set('linktitle', stancon.find('LinkTitle').text)
				if stancon.find('Actuate').text:
					citation_element.set('actuate', stancon.find('Actuate').text)
				if stancon.find('Show').text:
					citation_element.set('show', stancon.find('Show').text)
				if stancon.find('ConventionNote').text:
					stadesc_element = ET.Element('descriptivenote')
					stancon_element.append(stadesc_element)
					stap_element = ET.Element('p')
					stadesc_element.insert(0, stap_element)
					stap_element.text = stancon.find('ConventionNote').text
	else:
		old_condec_list = control_root.findall('conventiondeclaration')
		for old_condec in old_condec_list:
			control_root.remove(old_condec)
	
	# Local Type Declaration section
	if CSheet.find('LocalConventions/Convention/Citation').text:
		if control_root.find('localtypedeclaration') is None:
			if "add_localcon" in globals.new_elements or "add-all" in globals.add_all:
				for localcon in reversed(CSheet.find('LocalConventions')):
					localcon_element = ET.Element('localtypedeclaration')
					if control_root.find('conventiondeclaration') is None:
						if control_root.find('languagedeclaration') is None:
							before_element = 'maintenanceagency'
						else:	
							before_element = 'languagedeclaration'
					else:
						before_element = 'conventiondeclaration'
					last_stancon =control_root.getchildren().index(control_root.find(before_element)) + 1
					control_root.insert(last_stancon, localcon_element)
					if localcon.find('Abbreviation').text:
						abbr_element = ET.Element('abbr')
						localcon_element.insert(0, abbr_element)
						abbr_element.text = localcon.find('Abbreviation').text
					citation_element = ET.Element('citation')
					localcon_element.append(citation_element)
					citation_element.text = localcon.find('Citation').text
					if localcon.find('ConventionLink').text:
						citation_element.set('href', localcon.find('ConventionLink').text)
					if localcon.find('LinkTitle').text:
						citation_element.set('linktitle', localcon.find('LinkTitle').text)
					if localcon.find('Actuate').text:
						citation_element.set('actuate', localcon.find('Actuate').text)
					if localcon.find('Show').text:
						citation_element.set('show', localcon.find('Show').text)
					if localcon.find('ConventionNote').text:
						stadesc_element = ET.Element('descriptivenote')
						localcon_element.append(stadesc_element)
						stap_element = ET.Element('p')
						stadesc_element.insert(0, stap_element)
						stap_element.text = localcon.find('ConventionNote').text
		else:
			old_localconv_list = control_root.findall('localtypedeclaration')
			for old_localconv in old_localconv_list:
				control_root.remove(old_localconv)
			for localcon in reversed(CSheet.find('LocalConventions')):
				localcon_element = ET.Element('localtypedeclaration')
				if control_root.find('conventiondeclaration') is None:
					if control_root.find('languagedeclaration') is None:
						before_element = 'maintenanceagency'
					else:	
						before_element = 'languagedeclaration'
				else:
					before_element = 'conventiondeclaration'
				last_stancon = control_root.getchildren().index(control_root.find(before_element)) + 1
				control_root.insert(last_stancon, localcon_element)
				if localcon.find('Abbreviation').text:
					abbr_element = ET.Element('abbr')
					localcon_element.insert(0, abbr_element)
					abbr_element.text = localcon.find('Abbreviation').text
				citation_element = ET.Element('citation')
				localcon_element.append(citation_element)
				citation_element.text = localcon.find('Citation').text
				if localcon.find('ConventionLink').text:
					citation_element.set('href', localcon.find('ConventionLink').text)
				if localcon.find('LinkTitle').text:
					citation_element.set('linktitle', localcon.find('LinkTitle').text)
				if localcon.find('Actuate').text:
					citation_element.set('actuate', localcon.find('Actuate').text)
				if localcon.find('Show').text:
					citation_element.set('show', localcon.find('Show').text)
				if localcon.find('ConventionNote').text:
					stadesc_element = ET.Element('descriptivenote')
					localcon_element.append(stadesc_element)
					stap_element = ET.Element('p')
					stadesc_element.insert(0, stap_element)
					stap_element.text = localcon.find('ConventionNote').text
	else:
		old_localcon_list = control_root.findall('localtypedeclaration')
		for old_localcon in old_localcon_list:
			control_root.remove(old_localcon)
					
	# Local Control Section
	if CSheet.find('LocalControls/Control/Term').text:
		if control_root.find('localcontrol') is None:
			if "add_localctr" in globals.new_elements or "add-all" in globals.add_all:
				for localctr in reversed(CSheet.find('LocalControls')):
					localctr_element = ET.Element('localcontrol')
					if control_root.find('localtypedeclaration') is None:
						if control_root.find('conventiondeclaration') is None:
							if control_root.find('languagedeclaration') is None:
								before_element = 'maintenanceagency'
							else:	
								before_element = 'languagedeclaration'
						else:
							before_element = 'conventiondeclaration'
					else:
						before_element = 'localtypedeclaration'
					last_localcon = control_root.getchildren().index(control_root.find(before_element)) + 1
					control_root.insert(last_localcon, localctr_element)
					term_element = ET.Element('term')
					localctr_element.insert(0, term_element)
					term_element.text = localctr.find('Term').text
					if localctr.find('LocalType').text:
						localctr_element.set('localtype', localctr.find('LocalType').text)
					if localctr.find('Date').text:
						from date import magic_date
						localctr_element.append(magic_date(localctr.find('Date').text, localctr.find('DateNormal').text, 'inclusive'))
		else:
			old_localcont_list = control_root.findall('localcontrol')
			for old_localcont in old_localcont_list:
				control_root.remove(old_localcont)
			for localctr in reversed(CSheet.find('LocalControls')):
				localctr_element = ET.Element('localcontrol')
				if control_root.find('localtypedeclaration') is None:
					if control_root.find('conventiondeclaration') is None:
						if control_root.find('languagedeclaration') is None:
							before_element = 'maintenanceagency'
						else:	
							before_element = 'languagedeclaration'
					else:
						before_element = 'conventiondeclaration'
				else:
					before_element = 'localtypedeclaration'
				last_localcon = control_root.getchildren().index(control_root.find(before_element)) + 1
				control_root.insert(last_localcon, localctr_element)
				term_element = ET.Element('term')
				localctr_element.insert(0, term_element)
				term_element.text = localctr.find('Term').text
				if localctr.find('LocalType').text:
					localctr_element.set('localtype', localctr.find('LocalType').text)
				if localctr.find('Date').text:
					from date import magic_date
					localctr_element.append(magic_date(localctr.find('Date').text, localctr.find('DateNormal').text, 'inclusive'))
	else:
		old_localcont_list = control_root.findall('localcontrol')
		for old_localcont in old_localcont_list:
			control_root.remove(old_localcont)
					
	# Maintenance History / Revisions
	if "ask_gui" in globals.new_elements: 
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <maintenancehistory>...")
	alert_count = 0
	control_root.find('maintenancehistory').clear()
	for event in CSheet.find('Revisions'):
		if event.find('Type').text and event.find('Date').text and event.find('AgentType').text and event.find('Agent').text:
			if control_root.find('maintenancehistory') is None:
				maintenancehistory_element = ET.Element('maintenancehistory')
				if control_root.find('localcontrol') is None:
					if control_root.find('localtypedeclaration') is None:
						if control_root.find('conventiondeclaration') is None:
							if control_root.find('languagedeclaration') is None:
								if control_root.find('maintenanceagency') is None:
									error("Maintenance Agency <MaintenanceAgency> is required in EAD3, Maintenance Agency must be entered or finding aid will not be valid.", False)
									maintenancehistory_index = control_root.getchildren().index(control_root.find('filedesc')) + 1
								else:
									maintenancehistory_index = control_root.getchildren().index(control_root.find('maintenanceagency')) + 1
							else:
								maintenancehistory_index = control_root.getchildren().index(control_root.find('languagedeclaration')) + 1
						else:
							maintenancehistory_index = control_root.getchildren().index(control_root.find('conventiondeclaration')) + 1
					else:
						maintenancehistory_index = control_root.getchildren().index(control_root.find('localtypedeclaration')) + 1
				else:
					maintenancehistory_index = control_root.getchildren().index(control_root.find('localcontrol')) + 1
				control_root.insert(maintenancehistory_index, maintenancehistory_element)				
			for event in CSheet.find('Revisions'):
				main_event_element = ET.Element('maintenanceevent')
				control_root.find('maintenancehistory').append(main_event_element)
				type_element = ET.Element('eventtype')
				main_event_element.append(type_element)
				type_element.set('value', event.find('Type').text)
				date_element = ET.Element('eventdatetime')
				main_event_element.append(date_element)
				date_element.text = event.find('Date').text
				if event.find('DateNormal').text:
					date_element.set('standarddatetime', event.find('DateNormal').text)
				atype_element = ET.Element('agenttype')
				main_event_element.append(atype_element)
				atype_element.set('value', event.find('AgentType').text)
				agent_element = ET.Element('agent')
				main_event_element.append(agent_element)
				agent_element.text = event.find('Agent').text
				if event.find('Description').text:
					desc_element = ET.Element('eventdescription')
					main_event_element.append(desc_element)
					desc_element.text = event.find('Description').text
		else:
			if alert_count > 1:
				error("Maintenance History <maintenancehistory> section is incomplete: <eventtype>, <eventdatetime>, <agenttype>, and <agent> are all required elements.", False)
			alert_count = alert_count + 1
	
	# Sources section
	if CSheet.find('OutsideSources/Source/SourceName').text:
		if control_root.find('sources') is None:
			if "add_sources" in globals.new_elements or "add-all" in globals.add_all:
				sources_element = ET.Element('sources')
				control_root.append(sources_element)
				for new_source in CSheet.find('OutsideSources'):
					source_element = ET.Element('source')
					control_root.find('sources').append(source_element)
					if new_source.find('SourceLink').text:
						ource_element.set('href', new_source.find('SourceLink').text)
					if new_source.find('SourceName').text:
						sourceentry_element = ET.Element('sourceentry')
						if first_source.find('sourceentry') is None:
							source_element.append(sourceentry_element)
							first_source.find('sourceentry').text = new_source.find('SourceName').text
						else: 
							source_element.append(sourceentry_element)
							source_element.find('sourceentry').text = new_source.find('SourceName').text
					if new_source.find('SourceCreator').text or new_source.find('SourceDate').text or new_source.find('SourceID').text:
						xmlwrap_element = ET.Element('objectxmlwrap')
						source_element.append(xmlwrap_element)
						if new_source.find('SourceName').text:
							xmltitle = ET.Element('{http://purl.org/DC/elements/1.0/}title')
							xmlwrap_element.append(xmltitle)
							xmltitle.text = new_source.find('SourceName').text
						if new_source.find('SourceCreator').text:
							xmlcreator = ET.Element('{http://purl.org/DC/elements/1.0/}creator')
							xmlwrap_element.append(xmlcreator)
							xmlcreator.text = new_source.find('SourceCreator').text
						if new_source.find('SourceDate').text:
							xmldate = ET.Element('{http://purl.org/DC/elements/1.0/}date')
							xmlwrap_element.append(xmldate)
							xmldate.text = new_source.find('SourceDate').text
						if new_source.find('SourceID').text:
							xmlid = ET.Element('{http://purl.org/DC/elements/1.0/}identifier')
							xmlwrap_element.append(xmlid)
							xmlid.text = new_source.find('SourceID').text
					if new_source.find('SourceDesc').text:
						sourcedesc_element = ET.Element('descriptivenote')
						source_element.append(sourcedesc_element)
						sourcep_element = ET.Element('p')
						sourcedesc_element.append(sourcep_element)
						sourcep_element.text = new_source.find('SourceDesc').text
						sourcep_element.text = new_source.find('SourceDesc').text
		else:
			source_root = control_root.find('sources')
			old_source_list = source_root.findall('source')
			first_source = old_source_list[0]
			for old_source in old_source_list:
				source_root.remove(old_source)
			for new_source in CSheet.find('OutsideSources'):
				source_element = ET.Element('source')
				control_root.find('sources').append(source_element)
				if new_source.find('SourceLink').text:
					source_element.set('href', new_source.find('SourceLink').text)
				if new_source.find('SourceName').text:
					sourceentry_element = ET.Element('sourceentry')
					if first_source.find('sourceentry') is None:
						source_element.append(sourceentry_element)
						first_source.find('sourceentry').text = new_source.find('SourceName').text
					else: 
						source_element.append(sourceentry_element)
						source_element.find('sourceentry').text = new_source.find('SourceName').text
				if new_source.find('SourceCreator').text or new_source.find('SourceDate').text or new_source.find('SourceID').text:
					xmlwrap_element = ET.Element('objectxmlwrap')
					source_element.append(xmlwrap_element)
					if new_source.find('SourceName').text:
						xmltitle = ET.Element('{http://purl.org/DC/elements/1.0/}title')
						xmlwrap_element.append(xmltitle)
						xmltitle.text = new_source.find('SourceName').text
					if new_source.find('SourceCreator').text:
						xmlcreator = ET.Element('{http://purl.org/DC/elements/1.0/}creator')
						xmlwrap_element.append(xmlcreator)
						xmlcreator.text = new_source.find('SourceCreator').text
					if new_source.find('SourceDate').text:
						xmldate = ET.Element('{http://purl.org/DC/elements/1.0/}date')
						xmlwrap_element.append(xmldate)
						xmldate.text = new_source.find('SourceDate').text
					if new_source.find('SourceID').text:
						xmlid = ET.Element('{http://purl.org/DC/elements/1.0/}identifier')
						xmlwrap_element.append(xmlid)
						xmlid.text = new_source.find('SourceID').text
				if new_source.find('SourceDesc').text:
					sourcedesc_element = ET.Element('descriptivenote')
					source_element.append(sourcedesc_element)
					sourcep_element = ET.Element('p')
					sourcedesc_element.append(sourcep_element)
					sourcep_element.text = new_source.find('SourceDesc').text
					sourcep_element.text = new_source.find('SourceDesc').text
	else:
		source_root = control_root.find('sources')
		old_source_list = source_root.findall('source')
		for old_source in old_source_list:
			source_root.remove(old_source)