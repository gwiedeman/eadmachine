#module for Edition Statement (<editionstmt>) for both <control> and <eadheader>
import xml.etree.cElementTree as ET
import globals

def editionstmt(control_root, CSheet):
	if CSheet.find('Edition').text:
		if control_root.find('filedesc/editionstmt') is None:
			if "add_edition" in globals.new_elements or "add-all" in globals.add_all:
				editionstmt_par = control_root.find('filedesc')
				if CSheet.find('Edition').text:
					editionstmt_tag = ET.Element('editionstmt')
					editionstmt_par.insert(1, editionstmt_tag)
					edition_par = editionstmt_par.find('editionstmt')
					edition_element = ET.Element('edition')
					edition_par.insert(0, edition_element)
					edition_element.text = CSheet.find('Edition').text
				for ed_p in CSheet:
					if ed_p.tag == "EditionP":
						if ed_p.text:
							editionp_par = control_root.find('filedesc/editionstmt')
							editionp_tag = ET.Element('p')
							editionp_par.append(editionp_tag)
							editionp_tag.text = ed_p.text
		else:
			if CSheet.find('Edition').text:
				if control_root.find('filedesc/editionstmt/edition') is None:
					edition_par = control_root.find('filedesc/editionstmt')
					edition_tag = ET.Element('edition')
					edition_par.insert(0, edition_tag)
					edition_par.find('edition').text = CSheet.find("Edition").text
				else:
					edition_par = control_root.find('filedesc/editionstmt')
					for old_ed in edition_par:
						if old_ed.tag == 'edition':
							edition_par.remove(old_ed)
					edition_element = ET.Element('edition')
					edition_par.insert(0, edition_element)
					edition_element.text = CSheet.find('Edition').text
			else:
				for old_edp in edition_par:
					if old_edp.tag == 'p':
						edition_par.remove(old_edp)
				for ed_p in CSheet:
					if ed_p.tag == "EditionP":
						if ed_p.text:
							editionp_par = control_root.find('filedesc/editionstmt')
							editionp_tag = ET.Element('p')
							editionp_par.append(editionp_tag)
							editionp_tag.text = ed_p.text
	else:
		if control_root.find('filedesc/editionstmt') is None:
			pass
		else:
			control_root.find('filedesc/editionstmt').clear()