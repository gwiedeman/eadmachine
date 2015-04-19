# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals
from messages import error
from mixed_content import mixed_content

def control(EAD, CSheet):

	#update GUI progress bar
	from wx.lib.pubsub import pub
	wx.CallAfter(pub.sendMessage, "update_spread", msg="Reading <control>...")

	control_root = EAD.find('control')

	#<recordid>
	if control_root.find('recordid') is None:
		error("Your finding aid does not include a <recordid> element, a mandatory element in EAD3. If you do not add an ID, your finding aid will not be valid.", False)
	else:
		CSheet.find('CollectionID').text = control_root.find('recordid').text
		if "instanceurl" in control_root.find('recordid').attrib:
			CSheet.find('URL').text = control_root.find('recordid').attrib['instanceurl']
	
	# <otherrecordid>
	if control_root.find('otherrecordid') is None:
		pass
	else:
		for old_otherid in CSheet:
			if old_otherid.tag == "OtherID":
				CSheet.remove(old_otherid)
		for other_id in reversed(control_root):
			if other_id.tag == "otherrecordid":
				OtherID_element = ET.Element('OtherID')
				CSheet.insert(5, OtherID_element)
				LocalType_element = ET.Element('LocalType')
				OtherID_element.append(LocalType_element)
				ID_element = ET.Element('ID')
				OtherID_element.append(ID_element)
				if other_id.text:
					ID_element.text = other_id.text
				if "localtype" in other_id.attrib:
					LocalType_element.text = other_id.attrib['localtype']			
		
	# <representation>, for HTML derivatives, etc.
	if control_root.find('representation') is None:
		pass
	else:
		for old_represent in CSheet:
			if old_represent.tag == "Representation":
				CSheet.remove(old_represent)
		for otherid_find in CSheet:
			if otherid_find.tag == "OtherID":
				otherid_index = control_root.getchildren().index(control_root.find(otherid_find)) + 1
		for represent in reversed(control_root):
			if represent.tag == "representation":
				Representation_element = ET.Element('Representation')
				CSheet.insert(otherid_index, Representation_element)
				Link_element = ET.Element('Link')
				Representation_element.append(Link_element)
				RepName_element = ET.Element('RepName')
				Representation_element.append(RepName_element)
				Show_element = ET.Element('Show')
				Representation_element.append(Show_element)
				if "href" in represent.attrib:
					Link_element.text = represent.attrib['href']
				if "linktitle" in represent.attrib:
					RepName_element.text = represent.attrib['linktitle']
				if "show" in represent.attrib:
					Show_element.text = represent.attrib['show']
	
	#<filedesc>
	if control_root.find('filedesc') is None:
		error("Your EAD finding aid does not contain a <filedesc> tag. Since this is a required element in EAD3, EADMachine is unable to convert the file. Please correct your EAD file and try again.", True)
		
	#<titlestmt>
	if control_root.find('filedesc/titlestmt') is None:
		error("Your EAD finding aid does not contain a <titlestmt> tag. Since this is a required element in EAD3, EADMachine is unable to convert the file. Please correct your EAD file and try again.", True)
	
	#<titleproper>
	if control_root.find('filedesc/titlestmt/titleproper') is None:
		error("Your finding aid does not have a <titleproper> element. This element is mandatory in EAD3, so you must add a Collection Name or your finding aid will not be valid.", False)
	
	#<subtitle>
	if control_root.find('filedesc/titlestmt/subtitle') is None:
		pass
	else:
		CSheet.find('Subtitle').text = control_root.find('filedesc/titlestmt/subtitle').text
		
	#<author>
	if control_root.find('filedesc/titlestmt/author') is None:
		pass
	else:
		CSheet.find('ProcessedBy').text = control_root.find('filedesc/titlestmt/author').text
	
	#<sponsor>
	if control_root.find('filedesc/titlestmt/sponsor') is None:
		pass
	else:
		CSheet.find('Sponsor').text = control_root.find('filedesc/titlestmt/sponsor').text
	
            
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
	if control_root.find('filedesc/notestmt') is None:
		pass
	else:
		for note in control_root.find('filedesc/notestmt').iter('p'):
			if note.text:
				note_element = ET.Element('NoteStatement')
				CSheet.find('NoteStatements').append(note_element)
				note_element.text = note.text
	
	# <maintenancestatus>
	if control_root.find('maintenancestatus') is None:
		pass
	else:
		if "value" in control_root.find('maintenancestatus').attrib:
			CSheet.find('DraftStatus').text = control_root.find('maintenancestatus').attrib['value']
	
	# <publicationstatus>
	if control_root.find('publicationstatus') is None:
		pass
	else:
		if "value" in control_root.find('publicationstatus').attrib:
			CSheet.find('PublicationStatus').text = control_root.find('publicationstatus').attrib['value']
	
	# Maintenance Agency section
	if control_root.find('maintenanceagency') is None:
		pass
	else:
		if control_root.find('maintenanceagency/agencyname') is None:
			pass
		else:
			CSheet.find('MaintenanceAgency').text = control_root.find('maintenanceagency/agencyname').text
		if control_root.find('maintenanceagency/agencycode') is None:
			pass
		else:
			CSheet.find('MaintenanceAgencyCode').text = control_root.find('maintenanceagency/agencycode').text
		
	# Language Declaration section
	if control_root.find('languagedeclaration') is None:
		pass
	else:
		CSheet.find('FindingAidLanguages').clear()
		script_count = 0
		note_count = 0
		for lang in control_root.find('languagedeclaration'):
			if lang.tag == "language":
				FALanguage_element = ET.Element('FALanguage')
				CSheet.find('FindingAidLanguages').append(FALanguage_element)
				Lang_element = ET.Element('Lang')
				FALanguage_element.append(Lang_element)
				LangCode_element = ET.Element('LangCode')
				FALanguage_element.append(LangCode_element)
				Script_element = ET.Element('Script')
				FALanguage_element.append(Script_element)
				ScriptCode_element = ET.Element('ScriptCode')
				FALanguage_element.append(ScriptCode_element)
				LangNote_element = ET.Element('LangNote')
				FALanguage_element.append(LangNote_element)
				FALanguage_element.text = lang.text
				if "langcode" in lang.attrib:
					LangCode_element.text = lang.attrib['langcode']
		for script in control_root.find('languagedeclaration'):
			if script.tag == "script":
				lang_order = CSheet.find('FindingAidLanguages')[script_count]
				script_count = script_count + 1
				lang_order.find('Script').text = script.text
				if "scriptcode" in script.attrib:
					lang_order.find('ScriptCode').text = script.attrib['scriptcode']
		for langnote in control_root.find('languagedeclaration'):
			if langnote.tag == "descriptivenote":
				langnote_order = CSheet.find('FindingAidLanguages')[note_count]
				note_count = note_count + 1
				for langnote_p in langnote:
					if langnote_order.find('LangNote').text:
						langnote_order.find('LangNote').text = langnote_order.find('LangNote').text + ", " + langnote_p.text
					else:
						langnote_order.find('LangNote').text = langnote_p.text
	
	# Convention Declaration section
	if control_root.find('conventiondeclaration') is None:
		pass
	else:
		CSheet.find('StandardConventions').clear()
		for con_dec in control_root:
			if con_dec.tag == "conventiondeclaration":
				Convention_element = ET.Element('Convention')
				CSheet.find('StandardConventions').append(Convention_element)
				Abbreviation_element = ET.Element('Abbreviation')
				Convention_element.append(Abbreviation_element)
				Citation_element = ET.Element('Citation')
				Convention_element.append(Citation_element)
				ConventionLink_element = ET.Element('ConventionLink')
				Convention_element.append(ConventionLink_element)
				Verified_element = ET.Element('Verified')
				Convention_element.append(Verified_element)
				LinkTitle_element = ET.Element('LinkTitle')
				Convention_element.append(LinkTitle_element)
				Actuate_element = ET.Element('Actuate')
				Convention_element.append(Actuate_element)
				Show_element = ET.Element('Show')
				Convention_element.append(Show_element)
				ConventionNote_element = ET.Element('ConventionNote')
				Convention_element.append(ConventionNote_element)
				if con_dec.find('abbr') is None:
					pass
				else:
					Abbreviation_element.text = con_dec.find('abbr').text
				if con_dec.find('citation') is None:
					pass
				else:
					Citation_element.text = mixed_content(con_dec.find('citation'))
				if "href" in con_dec.find('citation').attrib:
					ConventionLink_element.text = con_dec.find('citation').attrib['href']
				if "lastdatetimeverified" in con_dec.find('citation').attrib:
					Verified_element.text = con_dec.find('citation').attrib['lastdatetimeverified']
				if "linktitle" in con_dec.find('citation').attrib:
					LinkTitle_element.text = con_dec.find('citation').attrib['linktitle']
				if "actuate" in con_dec.find('citation').attrib:
					Actuate_element.text = con_dec.find('citation').attrib['actuate']
				if "show" in con_dec.find('citation').attrib:
					Show_element.text = con_dec.find('citation').attrib['show']
				if con_dec.find('descriptivenote') is None:
					pass
				else:
					for descnote in con_dec.find('descriptivenote'):
						if Convention_element.text:
							Convention_element.text = Convention_element.text + ", " + descnote.text
						else:
							Convention_element.text = descnote.text
	
	# Local Type Declaration section
	if control_root.find('localtypedeclaration') is None:
		pass
	else:
		CSheet.find('LocalConventions').clear()
		for local_dec in control_root:
			if local_dec.tag == "localtypedeclaration":
				Convention_element = ET.Element('Convention')
				CSheet.find('LocalConventions').append(Convention_element)
				Abbreviation_element = ET.Element('Abbreviation')
				Convention_element.append(Abbreviation_element)
				Citation_element = ET.Element('Citation')
				Convention_element.append(Citation_element)
				ConventionLink_element = ET.Element('ConventionLink')
				Convention_element.append(ConventionLink_element)
				Verified_element = ET.Element('Verified')
				Convention_element.append(Verified_element)
				LinkTitle_element = ET.Element('LinkTitle')
				Convention_element.append(LinkTitle_element)
				Actuate_element = ET.Element('Actuate')
				Convention_element.append(Actuate_element)
				Show_element = ET.Element('Show')
				Convention_element.append(Show_element)
				ConventionNote_element = ET.Element('ConventionNote')
				Convention_element.append(ConventionNote_element)
				if local_dec.find('abbr') is None:
					pass
				else:
					Abbreviation_element.text = local_dec.find('abbr').text
				if local_dec.find('citation') is None:
					pass
				else:
					Citation_element.text = mixed_content(local_dec.find('citation'))
				if "href" in local_dec.find('citation').attrib:
					ConventionLink_element.text = local_dec.find('citation').attrib['href']
				if "lastdatetimeverified" in local_dec.find('citation').attrib:
					Verified_element.text = local_dec.find('citation').attrib['lastdatetimeverified']
				if "linktitle" in local_dec.find('citation').attrib:
					LinkTitle_element.text = local_dec.find('citation').attrib['linktitle']
				if "actuate" in local_dec.find('citation').attrib:
					Actuate_element.text = local_dec.find('citation').attrib['actuate']
				if "show" in local_dec.find('citation').attrib:
					Show_element.text = local_dec.find('citation').attrib['show']
				if local_dec.find('descriptivenote') is None:
					pass
				else:
					for descnote in local_dec.find('descriptivenote'):
						if Convention_element.text:
							Convention_element.text = Convention_element.text + ", " + mixed_content(descnote)
						else:
							Convention_element.text = mixed_content(descnote)
					
	# Local Control Section
	if control_root.find('localcontrol') is None:
		pass
	else:
		CSheet.find('LocalControls').clear()
		for local_cont in control_root:
			if local_cont.tag == "localcontrol":
				Control_element = ET.Element('Control')
				CSheet.find('LocalControls').append(Control_element)
				Term_element = ET.Element('Term')
				Control_element.append(Term_element)
				LocalType_element = ET.Element('LocalType')
				Control_element.append(LocalType_element)
				Date_element = ET.Element('Date')
				Control_element.append(Term_element)
				DateNormal_element = ET.Element('DateNormal')
				Control_element.append(DateNormal_element)
				if local_cont.find('term') is None:
					pass
				else:
					Term_element.text = local_cont.find('term').text
				if "localtype" in local_cont.attrib:
					LocalType_element.text = local_cont.attrib['localtype']
				if local_cont.find('datesingle') is None:
					pass
				else:
					Date_element.text = local_cont.find('datesingle').text
					if "standarddate" in local_cont.find('datesingle').attrib:
						DateNormal_element.text = local_cont.find('datesingle').attrib['standarddate']
				if local_cont.find('daterange') is None:
					pass
				else:
					Date_element.text = local_cont.find('daterange/fromdate').text + "-" + local_cont.find('daterange/todate').text
					if "standarddate" in local_cont.find('daterange/fromdate').attrib and "standarddate" in local_cont.find('daterange/todate').attrib:
						DateNormal_element.text = local_cont.find('daterange/fromdate').attrib['standarddate'] + "/" + local_cont.find('daterange/todate').attrib['standarddate']
	
	
					
	# Maintenance History / Revisions
	if control_root.find('maintenancehistory') is None:
		pass
	else:
		CSheet.find('Revisions').clear()
		for main in control_root.find('maintenancehistory'):
			Event_element = ET.Element('Event')
			CSheet.find('Revisions').append(Event_element)
			Type_element = ET.Element('Type')
			Event_element.append(Type_element)
			Date_element = ET.Element('Date')
			Event_element.append(Date_element)
			DateNormal_element = ET.Element('DateNormal')
			Event_element.append(DateNormal_element)
			AgentType_element = ET.Element('AgentType')
			Event_element.append(AgentType_element)
			Agent_element = ET.Element('Agent')
			Event_element.append(Agent_element)
			Description_element = ET.Element('Description')
			Event_element.append(Description_element)
			if main.find('eventtype') is None:
				pass
			else:
				if "value" in main.find('eventtype').attrib:
					Type_element.text = main.find('eventtype').attrib['value']
			if main.find('eventdatetime') is None:
				pass
			else:
				Date_element.text = main.find('eventdatetime').text
				if "standarddatetime" in main.find('eventdatetime').attrib:
					DateNormal_element.text = main.find('eventdatetime').attrib['standarddatetime']
			if main.find('agenttype') is None:
				pass
			else:
				if "value" in main.find('agenttype').attrib:
					AgentType_element.text = main.find('agenttype').attrib['value']
			if main.find('agent') is None:
				pass
			else:
				Agent_element.text = main.find('agent').text
			if main.find('eventdescription') is None:
				pass
			else:
				Description_element.text = main.find('eventdescription').text
	
	# Sources section
	if control_root.find('sources') is None:
		pass
	else:
		CSheet.find('OutsideSources').clear()
		for source in control_root.find('sources'):
			Source_element = ET.Element('Source')
			CSheet.find('OutsideSources').append(Source_element)
			SourceName_element = ET.Element('SourceName')
			Source_element.append(SourceName_element)
			SourceLink_element = ET.Element('SourceLink')
			Source_element.append(SourceLink_element)
			SourceCreator_element = ET.Element('SourceCreator')
			Source_element.append(SourceCreator_element)
			SourceDate_element = ET.Element('SourceDate')
			Source_element.append(SourceDate_element)
			SourceID_element = ET.Element('SourceID')
			Source_element.append(SourceID_element)
			SourceDesc_element = ET.Element('SourceDesc')
			Source_element.append(SourceDesc_element)
			if source.find('sourceentry') is None:
				pass
			else:
				SourceName_element.text = source.find('sourceentry').text
			if source.find('objectxmlwrap') is None:
				pass
			else:
				if source.find('objectxmlwrap/{http://purl.org/DC/elements/1.0/}title') is None:
					pass
				else:
					SourceLink_element.text = source.find('objectxmlwrap/{http://purl.org/DC/elements/1.0/}title').text
				if source.find('objectxmlwrap/{http://purl.org/DC/elements/1.0/}creator') is None:
					pass
				else:
					SourceCreator_element.text = source.find('objectxmlwrap/{http://purl.org/DC/elements/1.0/}creator').text
				if source.find('objectxmlwrap/{http://purl.org/DC/elements/1.0/}date') is None:
					pass
				else:
					SourceDate_element.text = source.find('objectxmlwrap/{http://purl.org/DC/elements/1.0/}date').text
				if source.find('objectxmlwrap/{http://purl.org/DC/elements/1.0/}identifier') is None:
					pass
				else:
					SourceID_element.text = source.find('objectxmlwrap/{http://purl.org/DC/elements/1.0/}identifier').text
			if source.find('descriptivenote') is None:
				pass
			else:
				for descnote in source.find('descriptivenote'):
					if SourceDesc_element.text:
						SourceDesc_element.text = SourceDesc_element + ", " + mixed_content(descnote)
					else:
						SourceDesc_element.text = mixed_content(descnote)