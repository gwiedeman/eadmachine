#module for Edition Statement (<editionstmt>) for both <control> and <eadheader>
import xml.etree.cElementTree as ET
import globals

def editionstmt(control_root, CSheet):
	if control_root.find('filedesc/editionstmt') is None:
		pass
	else:
		if control_root.find('filedesc/editionstmt/edition') is None:
			pass
		else:
			CSheet.find('Edition').text = control_root.find('filedesc/editionstmt/edition').text
		if control_root.find('filedesc/editionstmt/p') is None:
			pass
		else:
			edition_index = CSheet.getchildren().index(CSheet.find('Edition')) + 1
			for edition_p in reversed(control_root.find('filedesc/editionstmt')):
				if edition_p.tag == 'p':
					editionp_element = ET.Element('EditionP')
					CSheet.insert(edition_index, editionp_element)
					editionp_element.text = edition_p.text