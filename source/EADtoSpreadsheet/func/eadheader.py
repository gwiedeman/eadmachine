# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals
from messages import error
from mixed_content import mixed_content
import wx

def eadheader(EAD, CSheet):
	eadheader_root = EAD[0]
	
	#update GUI progress bar
	from wx.lib.pubsub import pub
	wx.CallAfter(pub.sendMessage, "update_spread", msg="Reading <eadheader>...")
	
	# <eadheader> @findaidstatus
	if "findaidstatus" in eadheader_root.attrib:
		CSheet.find('DraftStatus').text = eadheader_root.attrib['findaidstatus']
	
	#<eadid> @countrycode and @url
	if 'countrycode' in eadheader_root.find('eadid').attrib:
		CSheet.find('CountryCode').text = eadheader_root.find('eadid').attrib['countrycode']
	if 'url' in eadheader_root.find('eadid').attrib:
		CSheet.find('URL').text = eadheader_root.find('eadid').attrib['url']

	
	#<filedesc>
	if eadheader_root.find('filedesc') is None:
		error("Your EAD finding aid does not contain a <filedesc> tag. Since this is a required element in EAD2002, EADMachine is unable to convert the file. Please correct your EAD file and try again.", True)
		
	#<titlestmt>
	if eadheader_root.find('filedesc/titlestmt') is None:
		error("Your EAD finding aid does not contain a <titlestmt> tag. Since this is a required element in EAD2002, EADMachine is unable to convert the file. Please correct your EAD file and try again.", True)
		titlestmt_element = ET.Element('titlestmt')

	#<titleproper>
	if eadheader_root.find('filedesc/titlestmt/titleproper') is None:
		error("Your EAD finding aid does not contain a <titleproper> tag. Since this is a required element in EAD2002, EADMachine is unable to convert the file. Please correct your EAD file and try again.", True)
		
	#<date>
	if eadheader_root.find('filedesc/titlestmt/titleproper/date') is None:
		pass
	else:
		if 'type' in eadheader_root.find('filedesc/titlestmt/titleproper/date').attrib:
			if eadheader_root.find('filedesc/titlestmt/titleproper/date').attrib['type'].lower() == 'bulk':
				CSheet.find('DateBulk').text = eadheader_root.find('filedesc/titlestmt/titleproper/date').text
				if 'normal' in eadheader_root.find('filedesc/titlestmt/titleproper/date').attrib:
					CSheet.find('DateBulkNormal').text = eadheader_root.find('filedesc/titlestmt/titleproper/date').attrib['normal']
			else:
				CSheet.find('DateInclusive').text = eadheader_root.find('filedesc/titlestmt/titleproper/date').text
				if 'normal' in eadheader_root.find('filedesc/titlestmt/titleproper/date').attrib:
					CSheet.find('DateInclusiveNormal').text = eadheader_root.find('filedesc/titlestmt/titleproper/date').attrib['normal']
		else:
			CSheet.find('DateInclusive').text = eadheader_root.find('filedesc/titlestmt/titleproper/date').text
			if 'normal' in eadheader_root.find('filedesc/titlestmt/titleproper/date').attrib:
				CSheet.find('DateInclusiveNormal').text = eadheader_root.find('filedesc/titlestmt/titleproper/date').attrib['normal']
			
	#<subtitle>
	if eadheader_root.find('filedesc/titlestmt/subtitle') is None:
		if EAD.find('frontmatter/titlepage/subtitle') is None:
			pass
		else:
			CSheet.find('Subtitle').text = EAD.find('frontmatter/titlepage/subtitle').text
	else:
		CSheet.find('Subtitle').text = eadheader_root.find('filedesc/titlestmt/subtitle').text
		
	#<author>
	if eadheader_root.find('filedesc/titlestmt/author') is None:
		if EAD.find('frontmatter/titlepage/author') is None:
			pass
		else:
			CSheet.find('ProcessedBy').text = EAD.find('frontmatter/titlepage/author').text
	else:
		CSheet.find('ProcessedBy').text = eadheader_root.find('filedesc/titlestmt/author').text
	
	#<sponsor>
	if eadheader_root.find('filedesc/titlestmt/sponsor') is None:
		if EAD.find('frontmatter/titlepage/sponsor') is None:
			pass
		else:
			CSheet.find('Sponsor').text = EAD.find('frontmatter/titlepage/sponsor').text
	else:
		CSheet.find('Sponsor').text = eadheader_root.find('filedesc/titlestmt/sponsor').text
	
            
	# Edition Statement Section
	from editionstmt import editionstmt
	editionstmt(eadheader_root, CSheet)
	
	# Publication Statement Section
	from publicationstmt import publicationstmt
	publicationstmt(eadheader_root, CSheet)
	if CSheet.find('Publisher/PublisherName') is None:
		if EAD.find('frontmatter/titlepage/publisher') is None:
			pass
		else:
			if EAD.find('frontmatter/titlepage/publisher').text:
				CSheet.find('Publisher/PublisherName').text = EAD.find('frontmatter/titlepage/publisher').text
	else:
		if CSheet.find('Publisher/PublisherName').text:
			pass
		else:
			if EAD.find('frontmatter/titlepage/publisher') is None:
				pass
			else:
				CSheet.find('Publisher/PublisherName').text = EAD.find('frontmatter/titlepage/publisher').text
	if CSheet.find('PublicationDate').text:
		pass
	else:
		if EAD.find('frontmatter/titlepage/date') is None:
			pass
		else:
			CSheet.find('PublicationDate').text = EAD.find('frontmatter/titlepage/date').text
			if 'normal' in EAD.find('frontmatter/titlepage/date').attrib:
				CSheet.find('PublicationDateNormal').text = EAD.find('frontmatter/titlepage/date').attrib['normal']
			
	# Series Statement Section
	from seriesstmt import seriesstmt
	seriesstmt(eadheader_root, CSheet)
	
	
	# Note Statement Section
	if eadheader_root.find('filedesc/notestmt') is None:
		pass
	else:
		for note in eadheader_root.find('filedesc/notestmt').iter('p'):
			if note.text:
				note_element = ET.Element('NoteStatement')
				CSheet.find('NoteStatements').append(note_element)
				note_element.text = note.text
	
	# Profile Description
	if eadheader_root.find('profiledesc') is None:
		pass
	else:
		# EAD creation and EAD creation date
		if eadheader_root.find('profiledesc/creation') is None:
			pass
		else:
			CSheet.find('EADCreator').text = eadheader_root.find('profiledesc/creation').text
			if eadheader_root.find('profiledesc/creation/date') is None:
				pass
			else:
				if eadheader_root.find('profiledesc/creation/date').tail:
					CSheet.find('EADCreator').text = CSheet.find('EADCreator').text + eadheader_root.find('profiledesc/creation/date').tail
				CSheet.find('EADCreationDate').text = eadheader_root.find('profiledesc/creation/date').text
				if 'normal' in eadheader_root.find('profiledesc/creation/date').attrib:
					CSheet.find('EADCreationDateNormal').text = eadheader_root.find('profiledesc/creation/date').attrib['normal']
		# Finding Aid Languages
		if eadheader_root.find('profiledesc/langusage') is None:
			pass
		else:
			if eadheader_root.find('profiledesc/langusage/language') is None:
				if eadheader_root.find('profiledesc/langusage').text:
					CSheet.find('FindingAidLanguages/FALanguage/Lang').text = eadheader_root.find('profiledesc/langusage').text
			else:
				CSheet.find('FindingAidLanguages').clear()
				for lang in eadheader_root.find('profiledesc/langusage'):
					if lang.tag == "language":
						FALanguage_element = ET.Element('FALanguage')
						CSheet.find('FindingAidLanguages').append(FALanguage_element)
						Lang_element = ET.Element('Lang')
						FALanguage_element.append(Lang_element)
						Lang_element.text = lang.text
						LangCode_element = ET.Element('LangCode')
						FALanguage_element.append(LangCode_element)
						if "langcode" in lang.attrib:
							LangCode_element.text = lang.attrib['langcode']
						Script_element = ET.Element('Script')
						FALanguage_element.append(Script_element)
						ScriptCode_element = ET.Element('ScriptCode')
						FALanguage_element.append(ScriptCode_element)
						LangNote_element = ET.Element('LangNote')
						FALanguage_element.append(LangNote_element)
						if eadheader_root.find('profiledesc/langusage').text:
							LangNote_element.text = eadheader_root.find('profiledesc/langusage').text
						if len(eadheader_root.find('profiledesc/langusage').tail.strip()) >= 1:
							LangNote_element.text = LangNote_element.text + eadheader_root.find('profiledesc/langusage').tail
		
		# Description Rules
		if eadheader_root.find('profiledesc/descrules') is None:
			pass
		else:
			CSheet.find('LocalConventions/Convention/Citation').text = mixed_content(eadheader_root.find('profiledesc/descrules'))
			
	
	# Revisions
	if eadheader_root.find('revisiondesc') is None:
		pass
	else:
		revision_root = eadheader_root.find('revisiondesc')
		if revision_root.find('change') is None: 
			if revision_root.find('list') is None:
				pass
			else: #if list
				CSheet.find('Revisions').clear()
				for item in revision_root.find('list'):
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
					if item.find('date') is None:
						pass
					else:
						Date_element.text = item.find('date').text
						if 'normal' in item.find('date').attrib:
							DateNormal_element.text = item.find('date').attrib['normal']
					if item.text:
						Description_element.text = item.text
					if item.tail:
						Description_element.text = Description_element.text + item.tail
		else: # if change
			if revision_root.find('list') is None:
				CSheet.find('Revisions').clear()
				for change in revision_root:
					if change.tag == "change":
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
						if change.find('date') is None:
							pass
						else:
							Date_element.text = change.find('date').text
							if 'normal' in change.find('date').attrib:
								DateNormal_element.text = change.find('date').attrib['normal']
						if change.find('item') is None:
							pass
						else:
							Description_element.text = change.find('item').text
			else: #if list and change
				CSheet.find('Revisions').clear()
				for change in revision_root.find('change'):
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
					if change.find('date') is None:
						pass
					else:
						Date_element.text = change.find('date').text
						if 'normal' in change.find('date').attrib:
							DateNormal_element.text = change.find('date').attrib['normal']
					if change.find('item') is None:
						pass
					else:
						Description_element.text = change.find('item').text
				for item in revision_root.find('list'):
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
					if item.find('date') is None:
						pass
					else:
						Date_element.text = item.find('date').text
						if 'normal' in item.find('date').attrib:
							DateNormal_element.text = item.find('date').attrib['normal']
					if item.text:
						Description_element.text = item.text
					if item.tail:
						Description_element.text = Description_element.text + item.tail