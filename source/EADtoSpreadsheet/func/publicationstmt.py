#module for Publication Statement (<editionstmt>) for both <control> and <eadheader>
import xml.etree.cElementTree as ET
import globals

def publicationstmt(control_root, CSheet):
	if control_root.find('filedesc/publicationstmt') is None:
		pass
	else:
		if control_root.find('filedesc/publicationstmt/publisher') is None:
			pass
		else:
			CSheet.find('Publisher/PublisherName').text = control_root.find('filedesc/publicationstmt/publisher').text
		if control_root.find('filedesc/publicationstmt/address') is None:
			pass
		else:
			if control_root.find('filedesc/publicationstmt/address/addressline') is None:
				pass
			else:
				for addressline in control_root.find('filedesc/publicationstmt/address'):
					addressline_element = ET.Element('AddressLine')
					CSheet.find('Publisher').append(addressline_element)
					addressline_element.text = addressline.text
		if control_root.find('filedesc/publicationstmt/date') is None:
			pass
		else:
			CSheet.find('PublicationDate').text = control_root.find('filedesc/publicationstmt/date').text
			if 'normal' in control_root.find('filedesc/publicationstmt/date').attrib:
				CSheet.find('PublicationDateNormal').text = control_root.find('filedesc/publicationstmt/date').attrib['normal']