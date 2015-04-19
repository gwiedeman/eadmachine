# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals

def simple_unitdate(did_root, CSheet):
	if did_root.find("unitdate[@type='bulk']") is None or did_root.find("unitdate[@type='inclusive']") is None:
		if did_root.find("unitdate[@type='inclusive']") is None:
			if did_root.find("unitdate") is None:
				if CSheet.find('DateInclusive').text:
					unitdate_element = ET.Element('unitdate')
					did_root.append(unitdate_element)
					unitdate_element.set('type', 'inclusive')
					unitdate_element.text = CSheet.find('DateInclusive').text
					if CSheet.find('DateInclusiveNormal').text:
						did_root.find("unitdate").set('normal', CSheet.find('DateInclusiveNormal').text)
					else:
						did_root.find("unitdate").set('normal', CSheet.find('DateInclusive').text)
			else:
				did_root.find("unitdate").text = CSheet.find('DateInclusive').text
				did_root.find("unitdate").set('type', 'inclusive')
				if CSheet.find('DateInclusiveNormal').text:
					did_root.find("unitdate").set('normal', CSheet.find('DateInclusiveNormal').text)
				else:
					did_root.find("unitdate").set('normal', CSheet.find('DateInclusive').text)
			if CSheet.find('DateBulk').text:
				if "add_bulkdate" in globals.new_elements or "add-all" in globals.add_all:
					bulk_element = ET.Element('unitdate')
					bulk_element.set('type', 'bulk')
					last_unitdate = did_root.getchildren().index(did_root.find('unitdate')) + 1
					did_root.insert(last_unitdate, bulk_element)
					bulk_element.text = CSheet.find('DateBulk').text
					if CSheet.find('DateBulkNormal').text:
						did_root.find("unitdate[@type='bulk']").set('normal', CSheet.find('DateBulkNormal').text)
					else:
						did_root.find("unitdate[@type='bulk']").set('normal', CSheet.find('DateBulk').text)
		else:
			did_root.find("unitdate[@type='inclusive']").text = CSheet.find('DateInclusive').text
			if CSheet.find('DateInclusiveNormal').text:
				did_root.find("unitdate[@type='inclusive']").set('normal', CSheet.find('DateInclusiveNormal').text)
			else:
				did_root.find("unitdate[@type='inclusive']").set('normal', CSheet.find('DateInclusive').text)
			if CSheet.find('DateBulk').text:
				if "add_bulkdate" in globals.new_elements or "add-all" in globals.add_all:
					bulk_element = ET.Element('unitdate')
					bulk_element.set('type', 'bulk')
					last_unitdate = did_root.getchildren().index(did_root.find('unitdate')) + 1
					did_root.insert(last_unitdate, bulk_element)
					bulk_element.text = CSheet.find('DateBulk').text
					bulk_element.text = CSheet.find('DateBulk').text
					if CSheet.find('DateBulkNormal').text:
						did_root.find("unitdate[@type='bulk']").set('normal', CSheet.find('DateBulkNormal').text)
					else:
						did_root.find("unitdate[@type='bulk']").set('normal', CSheet.find('DateBulk').text)
	else:
		if CSheet.find('DateInclusive').text:
			did_root.find("unitdate[@type='inclusive']").text = CSheet.find('DateInclusive').text
			if CSheet.find('DateInclusiveNormal').text:
				did_root.find("unitdate[@type='inclusive']").set('normal', CSheet.find('DateInclusiveNormal').text)
			else:
				did_root.find("unitdate[@type='inclusive']").set('normal', CSheet.find('DateInclusive').text)
		if CSheet.find('DateBulk').text:
			did_root.find("unitdate[@type='bulk']").text = CSheet.find('DateBulk').text
			if CSheet.find('DateBulkNormal').text:
				did_root.find("unitdate[@type='bulk']").set('normal', CSheet.find('DateBulkNormal').text)
			else:
				did_root.find("unitdate[@type='bulk']").set('normal', CSheet.find('DateBulk').text)
		else:
			if did_root.find("unitdate[@type='bulk']") is None:
				pass
			else:
				old_bulk = did_root.find("unitdate[@type='bulk']")
				did_root.remove(old_bulk)
			
def ead3simple_unitdate(did_root, CSheet):
	for unitdates in did_root:
		if unitdates.tag == 'unitdate':
			if 'certainty' in unitdates.attrib:
				unitdates.attrib.pop('certainty')
	if did_root.find('unitdate') is None:
		if CSheet.find('DateInclusive').text:
			inclusive_element = ET.Element('unitdate')
			inclusive_element.set('unitdatetype', 'inclusive')
			if did_root.find('unittitle') is None:
				last_unittitle = 0
			else:
				last_unittitle = did_root.getchildren().index(did_root.find('unittitle')) + 1
			did_root.insert(last_unittitle, inclusive_element)
			inclusive_element.text = CSheet.find('DateInclusive').text
			if inclusive_element.text.lower().startswith('circa') or inclusive_element.text.lower().startswith('ca.'):
				inclusive_element.set('certainty', 'circa')
			if CSheet.find('DateBulkNormal').text:
				inclusive_element.set('normal', CSheet.find('DateBulkNormal').text)
			else:
				inclusive_element.set('normal', CSheet.find('DateBulk').text)
		if CSheet.find('DateBulk').text:
			if "add_bulkdate" in globals.new_elements or "add-all" in globals.add_all:
				bulk_element = ET.Element('unitdate')
				bulk_element.set('unitdatetype', 'bulk')
				last_unitdate = did_root.getchildren().index(did_root.find('unitdate')) + 1
				did_root.insert(last_unitdate, bulk_element)
				bulk_element.text = CSheet.find('DateBulk').text
				if bulk_element.text.lower().startswith('circa') or bulk_element.text.lower().startswith('ca.'):
					bulk_element.set('certainty', 'circa')
				if CSheet.find('DateBulkNormal').text:
					bulk_element.set('normal', CSheet.find('DateBulkNormal').text)
				else:
					bulk_element.set('normal', CSheet.find('DateBulk').text)
	else:
		if did_root.find("unitdate[@unitdatetype='bulk']") is None or did_root.find("unitdate[@unitdatetype='inclusive']") is None:
			# not both inclusive and bulk
			if did_root.find("unitdate[@unitdatetype='inclusive']") is None:
				# no inclusive
				if CSheet.find('DateInclusive').text:
					did_root.find("unitdate").text = CSheet.find('DateInclusive').text
					did_root.find("unitdate").set('unitdatetype', 'inclusive')
					if did_root.find("unitdate[@unitdatetype='inclusive']").text.lower().startswith('circa') or did_root.find("unitdate[@unitdatetype='inclusive']").text.lower().startswith('ca.'):
						did_root.find("unitdate[@unitdatetype='inclusive']").set('certainty', 'circa')
					if CSheet.find('DateInclusiveNormal').text:
						did_root.find("unitdate[@unitdatetype='inclusive']").set('normal', CSheet.find('DateInclusiveNormal').text)
					else:
						did_root.find("unitdate[@unitdatetype='inclusive']").set('normal', CSheet.find('DateInclusive').text)
				if did_root.find("unitdate[@unitdatetype='bulk']") is None:
					# no bulk
					if CSheet.find('DateBulk').text:
						if "add_bulkdate" in globals.new_elements or "add-all" in globals.add_all:
							bulk_element = ET.Element('unitdate')
							bulk_element.set('unitdatetype', 'bulk')
							last_unitdate = did_root.getchildren().index(did_root.find('unitdate')) + 1
							did_root.insert(last_unitdate, bulk_element)
							bulk_element.text = CSheet.find('DateBulk').text
							if bulk_element.text.lower().startswith('circa') or bulk_element.text.lower().startswith('ca.'):
								bulk_element.set('certainty', 'circa')
							if CSheet.find('DateBulkNormal').text:
								bulk_element.set('normal', CSheet.find('DateBulkNormal').text)
							else:
								bulk_element.set('normal', CSheet.find('DateBulk').text)
				else:
					#bulk
					if CSheet.find('DateBulk').text:
						did_root.find("unitdate[@unitdatetype='bulk']").text = CSheet.find('DateBulk').text
						if did_root.find("unitdate[@unitdatetype='bulk']").text.lower().startswith('circa') or did_root.find("unitdate[@unitdatetype='bulk']").text.lower().startswith('ca.'):
							did_root.find("unitdate[@unitdatetype='bulk']").set('certainty', 'circa')
						if CSheet.find('DateBulkNormal').text:
							did_root.find("unitdate[@unitdatetype='bulk']").set('normal', CSheet.find('DateBulkNormal').text)
						else:
							did_root.find("unitdate[@unitdatetype='bulk']").set('normal', CSheet.find('DateBulk').text)
					else:
						did_root.find("unitdate[@unitdatetype='bulk']").clear()
			else:
				# inclusive no bulk
				if CSheet.find('DateInclusive').text:
					unitdate_element = ET.Element('unitdate')
					did_root.append(unitdate_element)
					unitdate_element.set('unitdatetype', 'inclusive')
					unitdate_element.text = CSheet.find('DateInclusive').text
					if did_root.find("unitdate[@unitdatetype='inclusive']").text:
						if did_root.find("unitdate[@unitdatetype='inclusive']").text.lower().startswith('circa') or did_root.find("unitdate[@unitdatetype='inclusive']").text.lower().startswith('ca.'):
							did_root.find("unitdate[@unitdatetype='inclusive']").set('certainty', 'circa')
					did_root.find("unitdate[@unitdatetype='inclusive']").set('normal', CSheet.find('DateInclusiveNormal').text)
					if CSheet.find('DateInclusiveNormal').text:
						did_root.find("unitdate[@unitdatetype='inclusive']").set('normal', CSheet.find('DateInclusiveNormal').text)
					else:
						did_root.find("unitdate[@unitdatetype='inclusive']").set('normal', CSheet.find('DateInclusive').text)
				else:
					did_root.find("unitdate[@unitdatetype='inclusive']").clear()
				if CSheet.find('DateBulk').text:
					if "add_bulkdate" in globals.new_elements or "add-all" in globals.add_all:
						bulk_element = ET.Element('unitdate')
						bulk_element.set('unitdatetype', 'bulk')
						last_unitdate = did_root.getchildren().index(did_root.find('unitdate')) + 1
						did_root.insert(last_unitdate, bulk_element)
						bulk_element.text = CSheet.find('DateBulk').text
						if bulk_element.text.lower().startswith('circa') or bulk_element.text.lower().startswith('ca.'):
							bulk_element.set('certainty', 'circa')
						if CSheet.find('DateBulkNormal').text:
							bulk_element.set('normal', CSheet.find('DateBulkNormal').text)
						else:
							bulk_element.set('normal', CSheet.find('DateBulk').text)
		else:
			# both inclusive and bulk
			if CSheet.find('DateInclusive').text:
				did_root.find("unitdate[@unitdatetype='inclusive']").text = CSheet.find('DateInclusive').text
				if did_root.find("unitdate[@unitdatetype='inclusive']").text.lower().startswith('circa') or did_root.find("unitdate").text.lower().startswith('ca.'):
					did_root.find("unitdate[@unitdatetype='inclusive']").set('certainty', 'circa')
				if CSheet.find('DateInclusiveNormal').text:
					did_root.find("unitdate[@unitdatetype='inclusive']").set('normal', CSheet.find('DateInclusiveNormal').text)
				else:
					did_root.find("unitdate[@unitdatetype='inclusive']").set('normal', CSheet.find('DateInclusive').text)
			if CSheet.find('DateBulk').text:
				did_root.find("unitdate[@unitdatetype='bulk']").text = CSheet.find('DateBulk').text
				if did_root.find("unitdate[@unitdatetype='bulk']").text.lower().startswith('circa') or did_root.find("unitdate[@unitdatetype='bulk']").text.lower().startswith('ca.'):
					did_root.find("unitdate[@unitdatetype='bulk']").set('certainty', 'circa')
				if CSheet.find('DateBulkNormal').text:
					did_root.find("unitdate[@unitdatetype='bulk']").set('normal', CSheet.find('DateBulkNormal').text)
				else:
					did_root.find("unitdate[@unitdatetype='bulk']").set('normal', CSheet.find('DateBulk').text)
			else:
				did_root.remove(did_root.find("unittitle/unitdate[@unitdatetype='bulk']"))