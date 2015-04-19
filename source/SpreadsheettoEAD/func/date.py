#module for structured dates in EAD3 (<datesingle> and <daterange>)
import xml.etree.cElementTree as ET

#creates EAD3-style <unitdatestructured> for the collection and series-level dates from a date field and a normal date field
def magic_date(date_field, normal_date, type):
	date_structured_element = ET.Element('unitdatestructured')
	if type.lower() == 'bulk':
		date_structured_element.set('unitdatetype', 'bulk')
	if date_field.lower().startswith('circa') or date_field.lower().startswith('ca.'):
		date_structured_element.set('certainty', 'circa')
	else:
		date_structured_element.set('unitdatetype', type)
	if "-" not in date_field: # Single Dates
		if "circa" in date_field.lower() or "ca." in date_field.lower():
			datesingle_element = ET.Element('datesingle')
			datesingle_element.text = date_field.split(" ",1)[1]
			if normal_date:
				datesingle_element.set('standarddate', normal_date)
				if "/" in normal_date:
					datesingle_element.set('notbefore', normal_date.rsplit("/",1)[0])
					datesingle_element.set('notafter', normal_date.split("/",1)[1])
			else:
				datesingle_element.set('standarddate', date_field.split(" ",1)[1])
			date_structured_element.append(datesingle_element)
		else:
			datesingle_element = ET.Element('datesingle')
			datesingle_element.text = date_field
			if normal_date:
				datesingle_element.set('standarddate', normal_date)
			else:
				datesingle_element.set('standarddate', date_field)
			date_structured_element.append(datesingle_element)
	else: # Date Ranges
		if "-" in date_field:
			if "circa" in date_field.lower() or "ca." in date_field.lower():
				daterange_element = ET.Element('daterange')
				fromdate_element = ET.Element('fromdate')
				todate_element = ET.Element('todate')
				daterange_element.append(fromdate_element)
				with_circa = date_field.rsplit("-",1)[0] 
				fromdate_element.text = with_circa.split(" ",1)[1] 
				if normal_date:
					fromdate_element.set('notbefore', normal_date.rsplit("/",1)[0])
					fromdate_element.set('standarddate', normal_date.rsplit("/",1)[0])
				daterange_element.append(todate_element)
				todate_element.text = date_field.split("-",1)[1] 
				if normal_date:
					todate_element.set('notafter', normal_date.split("/",1)[1])
					todate_element.set('standarddate', normal_date.split("/",1)[1])
				date_structured_element.append(daterange_element)
			else:
				daterange_element = ET.Element('daterange')
				daterange_element = ET.Element('daterange')
				fromdate_element = ET.Element('fromdate')
				todate_element = ET.Element('todate')
				daterange_element.append(fromdate_element)
				fromdate_element.text = date_field.rsplit("-",1)[0] 
				if normal_date:
					fromdate_element.set('standarddate', normal_date.rsplit("/",1)[0])
				daterange_element.append(todate_element)
				todate_element.text = date_field.split("-",1)[1] 
				if normal_date:
					todate_element.set('standarddate', normal_date.split("/",1)[1] )
				date_structured_element.append(daterange_element)
		else:
			if "circa" in date_field.lower() or "ca." in date_field.lower():
				daterange_element = ET.Element('daterange')
				fromdate_element = ET.Element('fromdate')
				todate_element = ET.Element('todate')
				daterange_element.append(fromdate_element)
				with_circa = date_field.rsplit("-",1)[0] 
				fromdate_element.text = with_circa.split(" ",1)[1] 
				if normal_date:
					fromdate_element.set('notbefore', normal_date.rsplit("/",1)[0])
					fromdate_element.set('standarddate', normal_date.rsplit("/",1)[0])
				daterange_element.append(todate_element)
				todate_element.text = date_field.split("-",1)[1] 
				if normal_date:
					todate_element.set('notafter', normal_date.split("/",1)[1])
					todate_element.set('standarddate', normal_date.split("/",1)[1])
				date_structured_element.append(daterange_element)
			else:
				daterange_element = ET.Element('daterange')
				daterange_element = ET.Element('daterange')
				fromdate_element = ET.Element('fromdate')
				todate_element = ET.Element('todate')
				daterange_element.append(fromdate_element)
				fromdate_element.text = date_field.rsplit("-",1)[0] 
				if normal_date:
					fromdate_element.set('standarddate', normal_date.rsplit("/",1)[0])
				daterange_element.append(todate_element)
				todate_element.text = date_field.split("-",1)[1] 
				if normal_date:
					todate_element.set('standarddate', normal_date.split("/",1)[1] )
				date_structured_element.append(daterange_element)
	return date_structured_element


#creates EAD3-style <datesingle> or <daterange> from a date field and a normal date field
def basic_date(date_field, normal_date, type):
	if "-" in date_field:
		#date range
		date_element = ET.Element('daterange')
		fromdate_element = ET.Element('fromdate')
		todate_element = ET.Element('todate')
		date_element.append(fromdate_element)
		fromdate_element.text = date_field.rsplit("-",1)[0] 
		if normal_date:
			fromdate_element.set('standarddate', normal_date.rsplit("/",1)[0])
		date_element.append(todate_element)
		todate_element.text = date_field.split("-",1)[1] 
		if normal_date:
			todate_element.set('standarddate', normal_date.split("/",1)[1] )
	else:
		#date single
		date_element = ET.Element('datesingle')
		date_element.text = date_field
		if normal_date:
			date_element.set('standarddate', normal_date)

	return date_element
	
#creates EAD3-style <unitdatestructured> for the record-level dates from a set of date fields and normal date fields
def record_magic_date(did_root, Record_parent):
	datecount_exact = 0
	datecount_circa = 0
	for date in Record_parent:
		if date.tag.startswith("Date"):
			if not date.tag.endswith("Normal"):
				if date.text:
					if date.text.lower().startswith('circa') or date.text.lower().startswith('ca.'):
						datecount_circa = datecount_circa + 1
					else:
						datecount_exact = datecount_exact + 1
	if datecount_exact >= 1:
		unitdatestructured_element = ET.Element('unitdatestructured')
		did_root.append(unitdatestructured_element)
		unitdatestructured_element.set('certainty', 'exact')
		if datecount_exact > 1:
			dateset_element = ET.Element('dateset')
			unitdatestructured_element.append(dateset_element)
	if datecount_circa >= 1:
		unitdatestructured_element = ET.Element('unitdatestructured')
		did_root.append(unitdatestructured_element)
		unitdatestructured_element.set('certainty', 'circa')
		if datecount_circa > 1:
			dateset_element = ET.Element('dateset')
			unitdatestructured_element.append(dateset_element)
	for date in Record_parent:
		if date.tag.startswith("Date"):
			if not date.tag.endswith("Normal"):
				if date.text:
					if date.text.lower().startswith('circa') or date.text.lower().startswith('ca.'):
						if "-" in date.text:
							daterange_element = ET.Element('daterange')
							if did_root.find("unitdatestructured[@certainty='circa']").find('dateset') is None:
								did_root.find("unitdatestructured[@certainty='circa']").append(daterange_element)
							else:
								did_root.find("unitdatestructured[@certainty='circa']").find('dateset').append(daterange_element)
							fromdate_element = ET.Element('fromdate')
							todate_element = ET.Element('todate')
							daterange_element.append(fromdate_element)
							daterange_element.append(todate_element)
							print date.text
							with_circa = date.text.rsplit("-",1)[0] 
							fromdate_element.text = with_circa.split(" ",1)[1] 
							todate_element.text = date.text.split("-",1)[1] 
							if Record_parent.find(date.tag + "Normal").text:
								normal_date = Record_parent.find(date.tag + "Normal").text
								fromdate_element.set('notbefore', normal_date.rsplit("/",1)[0])
								fromdate_element.set('standarddate', normal_date.rsplit("/",1)[0])
								todate_element.set('notafter', normal_date.split("/",1)[1])
								todate_element.set('standarddate', normal_date.split("/",1)[1])
							else:
								fromdate_element.set('notbefore', date.text.rsplit("-",1)[0])
								fromdate_element.set('standarddate', date.text.rsplit("-",1)[0])
								todate_element.set('notafter', date.text.split("-",1)[1])
								todate_element.set('standarddate', date.text.split("-",1)[1])
						else:
							datesingle_element = ET.Element('datesingle')
							if did_root.find("unitdatestructured[@certainty='circa']").find('dateset') is None:
								did_root.find("unitdatestructured[@certainty='circa']").append(datesingle_element)
							else:
								did_root.find("unitdatestructured[@certainty='circa']").find('dateset').append(datesingle_element)
							datesingle_element.text = date.text						
							if Record_parent.find(date.tag + "Normal").text:
								datesingle_element.set('standarddate', Record_parent.find(date.tag + "Normal").text)
							else:
								datesingle_element.set('standarddate', date.text.rsplit(' ', 1))
					else:
						if "-" in date.text:
							daterange_element = ET.Element('daterange')
							if did_root.find("unitdatestructured[@certainty='exact']").find('dateset') is None:
								did_root.find("unitdatestructured[@certainty='exact']").append(daterange_element)
							else:
								did_root.find("unitdatestructured[@certainty='exact']").find('dateset').append(daterange_element)
							fromdate_element = ET.Element('fromdate')
							todate_element = ET.Element('todate')
							daterange_element.append(fromdate_element)
							daterange_element.append(todate_element)
							fromdate_element.text = date.text.rsplit("-",1)[0] 
							todate_element.text = date.text.split("-",1)[1] 
							if Record_parent.find(date.tag + "Normal").text:
								normal_date = Record_parent.find(date.tag + "Normal").text
								fromdate_element.set('standarddate', normal_date.rsplit("/",1)[0])
								todate_element.set('standarddate', normal_date.split("/",1)[1] )
							else:
								fromdate_element.set('standarddate', date.text.rsplit("-",1)[0])
								todate_element.set('standarddate', date.text.split("-",1)[1])
						else:
							datesingle_element = ET.Element('datesingle')
							if did_root.find("unitdatestructured[@certainty='exact']").find('dateset') is None:
								did_root.find("unitdatestructured[@certainty='exact']").append(datesingle_element)
							else:
								did_root.find("unitdatestructured[@certainty='exact']").find('dateset').append(datesingle_element)
							datesingle_element.text = date.text						
							if Record_parent.find(date.tag + "Normal").text:
								datesingle_element.set('standarddate', Record_parent.find(date.tag + "Normal").text)
							else:
								datesingle_element.set('standarddate', date.text)