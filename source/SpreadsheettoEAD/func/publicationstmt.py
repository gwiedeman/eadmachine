#module for Publication Statement (<editionstmt>) for both <control> and <eadheader>
import xml.etree.cElementTree as ET
import globals

def publicationstmt(control_root, CSheet):
	if CSheet.find('Publisher/AddressLine') is None:
		if CSheet.find('Publisher/PublisherName').text:
			pub_data = True
		else:
			pub_data = False
	else:
		if CSheet.find('Publisher/PublisherName').text or CSheet.find('Publisher/AddressLine').text:
			pub_data = True
		else:
			pub_data = False
			
	if pub_data == True:
		if control_root.find('filedesc/publicationstmt') is None:
			if "add_publication" in globals.new_elements or "add-all" in globals.add_all:
				pubstmt_element = ET.Element('publicationstmt')
				if control_root.find('filedesc/editionstmt') is None:
					pub_index = 1
				else:
					pub_index = 2
				control_root.find('filedesc').insert(pub_index, pubstmt_element)
				if CSheet.find('Publisher/PublisherName').text:
					publisher_element = ET.Element('publisher')
					pubstmt_element.append(publisher_element)
					publisher_element.text = CSheet.find('Publisher/PublisherName').text
				if CSheet.find('PublicationDate').text:
					date_element = ET.Element('date')
					pubstmt_element.append(date_element)
					date_element.text = CSheet.find('PublicationDate').text
					if CSheet.find('PublicationDateNormal').text:
						date_element.set('normal', CSheet.find('PublicationDateNormal').text)
					else:
						date_element.set('normal', CSheet.find('PublicationDate').text)
				if CSheet.find('Publisher/AddressLine') is None:
					pass
				else:
					if CSheet.find('Publisher/AddressLine').text:
						address_element = ET.Element('address')
						pubstmt_element.append(address_element)
					for new_line in CSheet.find('Publisher'):
						if new_line.tag == "AddressLine":
							if new_line.text:
								new_tag = ET.Element("addressline")
								address_element.append(new_tag)
								new_tag.text = new_line.text
		else:
			pubstmt_element = control_root.find('filedesc/publicationstmt')
			if control_root.find('filedesc/publicationstmt/publisher') is None:
				if CSheet.find('Publisher/PublisherName').text:
					publisher_element = ET.Element('publisher')
					pubstmt_element.append(publisher_element)
					publisher_element.text = CSheet.find('Publisher/PublisherName').text
			else:
				if CSheet.find('Publisher/PublisherName').text:
					control_root.find('filedesc/publicationstmt/publisher').text = CSheet.find('Publisher/PublisherName').text
				else:
					control_root.find('filedesc/publicationstmt/publisher').text = ""
			if control_root.find('filedesc/publicationstmt/date') is None:
				if CSheet.find('PublicationDate').text:
					date_element = ET.Element('date')
					pubstmt_element.append(date_element)
					date_element.text = CSheet.find('PublicationDate').text
					if CSheet.find('PublicationDateNormal').text:
						date_element.set('normal', CSheet.find('PublicationDateNormal').text)
					else:
						date_element.set('normal', CSheet.find('PublicationDate').text)
			else:
				if CSheet.find('PublicationDate').text:
					control_root.find('filedesc/publicationstmt/date').text = CSheet.find('PublicationDate').text
					if CSheet.find('PublicationDateNormal').text:
						control_root.find('filedesc/publicationstmt/date').set('normal', CSheet.find('PublicationDateNormal').text)
					else:
						control_root.find('filedesc/publicationstmt/date').set('normal', CSheet.find('PublicationDate').text)
				else:
					control_root.find('filedesc/publicationstmt/date').text = ""
			if control_root.find('filedesc/publicationstmt/address') is None:
				if CSheet.find('Publisher/AddressLine') is None:
					pass
				else:
					if CSheet.find('Publisher/AddressLine').text:
						address_element = ET.Element('address')
						pubstmt_element.append(address_element)
						for new_line in CSheet.find('Publisher'):
							if new_line.tag == "AddressLine":
								if new_line.text:
									new_tag = ET.Element("addressline")
									address_element.append(new_tag)
									new_tag.text = new_line.text
			else:
				template_address = control_root.find('filedesc/publicationstmt/address')
				if template_address.find('addressline') is None:
					for new_line in CSheet.find('Publisher'):
						if new_line.tag == "AddressLine":
							if new_line.text:
								new_tag = ET.Element("addressline")
								template_address.append(new_tag)
								new_tag.text = new_line.text
				else:
					template_address.clear()
					for new_line in CSheet.find('Publisher'):
						if new_line.tag == "AddressLine":
							if new_line.text:
								new_tag = ET.Element("addressline")
								template_address.append(new_tag)
								new_tag.text = new_line.text
	else:
		if control_root.find('filedesc/publicationstmt') is None:
			pass
		else:
			control_root.find('filedesc/publicationstmt').clear()