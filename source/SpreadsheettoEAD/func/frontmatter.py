# module for the <frontmatter> portion
import xml.etree.cElementTree as ET
import globals

def frontmatter(fm_root, CSheet):
	
	if fm_root.find('titlepage') is None:
		pass
	else:
		if fm_root.find('titlepage/titleproper') is None:
			pass
		else:
			fm_root.find('titlepage/titleproper').text = CSheet.find('CollectionName').text
			if fm_root.find('titlepage/titleproper/date') is None:
				pass
			else: 
				fm_root.find('titlepage/titleproper/date').text = CSheet.find('DateInclusive').text
				fm_root.find('titlepage/titleproper/date').set('type', 'inclusive')
				if CSheet.find('DateInclusiveNormal').text:
					fm_root.find('titlepage/titleproper/date').set('normal', CSheet.find('DateInclusiveNormal').text)
			if CSheet.find('Subtitle').text:
				if fm_root.find('titlepage/subtitle') is None:
					if "add_subtitle" in globals.new_elements or "add-all" in globals.add_all:
						subtitle_element = ET.Element('subtitle')
						last_title = fm_root.find('titlepage').getchildren().index(fm_root.find('titlepage/titleproper')) + 1
						fm_root.find('titlepage').insert(last_title, subtitle_element)
						subtitle_element.text = CSheet.find('Subtitle').text
				else:
					fm_root.find('titlepage/subtitle').text = CSheet.find('Subtitle').text
		if fm_root.find('titlepage/author') is None:
			pass
		else:
			fm_root.find('titlepage/author').text = CSheet.find('ProcessedBy').text
		if fm_root.find('titlepage/publisher') is None:
			pass
		else:
			fm_root.find('titlepage/publisher').text = CSheet.find('Publisher').text
		if fm_root.find('titlepage/date') is None:
			pass
		else:
			fm_root.find('titlepage/date').text = CSheet.find('PublicationDate').text
			if CSheet.find('PublicationDateNormal.text'):
				fm_root.find('titlepage/date').set('normal', CSheet.find('PublicationDateNormal').text)