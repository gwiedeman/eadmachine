# module for HTML <html> output
import xml.etree.cElementTree as ET
import globals
from encoding import escape_tag
from encoding import textify
from difflib import SequenceMatcher as SM

def html(input, html_root):
	CSheet = input.find('CollectionSheet')
	
	html_root.find('head/title').text = CSheet.find('CollectionName').text
	
	for series in CSheet.find('CollectionMap'):
		if series.find('ComponentLevel').text == "1":
			p_element = ET.Element('p')
			html_root.find('body/table/tr/td').append(p_element)
			p_element.set('style', 'margin-top:-5pt; margin-left:15pt; font-size:10pt')
			b_element = ET.Element('b')
			p_element.append(b_element)
			a_element = ET.Element('a')
			b_element.append(a_element)
			if series.find("ComponentNumber").text:
				anchor = "#series" + series.find("ComponentNumber").text
			else:
				cmpnt_anchor = series.find('ComponentName').text
				anchor = "#series" + escape_tag(cmpnt_anchor)
			a_element.set('href', anchor)
			for seriespage in input:
				if seriespage.find('SeriesNumber') is None:
					pass
				else:
					if seriespage.find('SeriesNumber').text == series.find("ComponentNumber").text:
						seriesinfo = seriespage
						if seriesinfo.find('SeriesDate').text:
							if "series" in series.find("ComponentName").text.lower():
								a_element.text = series.find("ComponentName").text + " " + seriesinfo.find('SeriesDate').text
							else:
								if series.find("ComponentNumber").text:
									a_element.text = "Series " + series.find("ComponentNumber").text + ": " + series.find("ComponentName").text + " " + seriesinfo.find('SeriesDate').text
								else:
									a_element.text = series.find("ComponentName").text + " " + seriesinfo.find('SeriesDate').text
						else:
							if "series" in series.find("ComponentName").text.lower():
								a_element.text = series.find("ComponentName").text
							else:
								if series.find("ComponentNumber").text:
									a_element.text = "Series " + series.find("ComponentNumber").text + ": " + series.find("ComponentName").text
								else:
									a_element.text = series.find("ComponentName").text
			
	if CSheet.find('CollectionName').text and CSheet.find('DateInclusive').text:
		html_root.find('body/table/tr/td/h2/a').text = CSheet.find('CollectionName').text + ", " + CSheet.find('DateInclusive').text
	else:
		if CSheet.find('CollectionName').text:
			html_root.find('body/table/tr/td/h2/a').text = CSheet.find('CollectionName').text
		if CSheet.find('DateInclusive').text:
			html_root.find('body/table/tr/td/h2/a').text = CSheet.find('DateInclusive').text
	html_root.find("body/table/tr/td/table/tr/td[@id='title']").text = CSheet.find('CollectionName').text
	html_root.find("body/table/tr/td/table/tr/td[@id='date']").text = CSheet.find('DateInclusive').text
	html_root.find("body/table/tr/td/table/tr/td[@id='physdesc']").text = ""
	for physdesc_display in CSheet.find("PhysicalDescriptionSet"):
		if physdesc_display.find('Quantity').text and physdesc_display.find('UnitType').text:
			html_root.find("body/table/tr/td/table/tr/td[@id='physdesc']").text = html_root.find("body/table/tr/td/table/tr/td[@id='physdesc']").text + physdesc_display.find('Quantity').text + " " + physdesc_display.find('UnitType').text + " "
		else:
			if physdesc_display.find('Quantity').text:
				html_root.find("body/table/tr/td/table/tr/td[@id='physdesc']").text = html_root.find("body/table/tr/td/table/tr/td[@id='physdesc']").text + physdesc_display.find('Quantity').text + " "
			if physdesc_display.find('UnitType').text:
				html_root.find("body/table/tr/td/table/tr/td[@id='physdesc']").text = html_root.find("body/table/tr/td/table/tr/td[@id='physdesc']").text + physdesc_display.find('UnitType').text + " "
	html_root.find("body/table/tr/td/table/tr/td[@id='abstract']").text = CSheet.find('Abstract').text
	html_root.find("body/table/tr/td/table/tr/td[@id='storage']").text == ""
	for location_display in CSheet.find("PhysicalLocationSet"):
		if location_display.find('Audience').text == "external":
			html_root.find("body/table/tr/td/table/tr/td[@id='storage']").text = html_root.find("body/table/tr/td/table/tr/td[@id='storage']").text + location_display.find('Location').text + " "
	html_root.find("body/table/tr/td/table/tr/td[@id='language']").text == ""
	for lang_display in CSheet.find("Languages"):
		if lang_display.find('Lang').text:
			html_root.find("body/table/tr/td/table/tr/td[@id='language']").text = html_root.find("body/table/tr/td/table/tr/td[@id='language']").text + lang_display.find('Lang').text + " "
	html_root.find("body/table/tr/td/table/tr/td[@id='repository']").text = CSheet.find('Repository/RepositoryName').text
	html_root.find("body/table/tr/td/h3[@id='bio']/a").text = CSheet.find('HistoricalNoteTitle').text
	bio_index = html_root.find("body/table/tr/td[@id='main']").getchildren().index(html_root.find("body/table/tr/td/h3[@id='bio']")) + 1
	for bio_display in reversed(CSheet.find('HistoricalNote')):
		p_element = ET.Element('p')
		html_root.find("body/table/tr/td[@id='main']").insert(bio_index, p_element)
		p_element.text = textify(bio_display.text)
		p_element.set('style', 'margin-left:25pt')
	scope_index = html_root.find("body/table/tr/td[@id='main']").getchildren().index(html_root.find("body/table/tr/td/h3[@id='scope']")) + 1
	for scope_display in reversed(CSheet.find('ScopeContent')):
		p_element = ET.Element('p')
		html_root.find("body/table/tr/td[@id='main']").insert(scope_index, p_element)
		p_element.text = textify(scope_display.text)
		p_element.set('style', 'margin-left:25pt')
	arrange_index = html_root.find("body/table/tr/td[@id='main']").getchildren().index(html_root.find("body/table/tr/td/h3[@id='arrange']")) + 1
	dupl_arrange = list()
	for arrange_list in reversed(CSheet.find('CollectionMap')):
		if arrange_list.find('ComponentName').text:
			if CSheet.find('CollectionMap/Component/ComponentName').text.lower() != "no series" or CSheet.find('CollectionMap/Component/ComponentName').text.lower() != "noseries":
				topdiv_element = ET.Element('div')
				html_root.find("body/table/tr/td[@id='main']").insert(arrange_index, topdiv_element)
				topdiv_element.set('style', 'margin-left:0pt')
				if arrange_list.find('ComponentLevel').text == "1":
					botdiv_element = ET.Element('div')
					topdiv_element.append(botdiv_element)
					botdiv_element.set('style', 'margin-left:25pt')
					b_element = ET.Element('b')
					botdiv_element.append(b_element)
					escaped_name = arrange_list.find('ComponentName').text
					if arrange_list.find('ComponentNumber').text:
						b_element.text = "Series " + arrange_list.find('ComponentNumber').text + " - " + escaped_name
						dupl_arrange.append(b_element.text.strip().lower())
					else:
						b_element.text = escaped_name
						dupl_arrange.append(b_element.text.strip().lower())
					for ComponentSheet in input:
						if "Series" in ComponentSheet.tag:
							if ComponentSheet.find('SeriesName') is None:
								if ComponentSheet.find('SeriesNumber') is None:
									pass
								else:
									if ComponentSheet.find('SeriesNumber').text == arrange_list.find('ComponentNumber').text:
										cmpnt_info = ComponentSheet
							elif ComponentSheet.find('SeriesName').text == arrange_list.find('ComponentName').text:
								cmpnt_info = ComponentSheet
					if cmpnt_info.find('SeriesDate').text:
						b_element.tail = ", " + cmpnt_info.find('SeriesDate').text
				elif arrange_list.find('ComponentLevel').text == "2":
					botdiv_element = ET.Element('div')
					topdiv_element.append(botdiv_element)
					botdiv_element.set('style', 'margin-left:50pt')
					for ComponentSheet in input:
						if ComponentSheet.find('SeriesName') is None:
							if ComponentSheet.find('SeriesNumber') is None:
								pass
							else:
								if ComponentSheet.find('SeriesNumber').text == arrange_list.find('ComponentNumber').text:
									cmpnt_info = ComponentSheet
						elif ComponentSheet.find('SeriesName').text == arrange_list.find('ComponentName').text:
							cmpnt_info = ComponentSheet
					if cmpnt_info.find('SeriesDate').text:
						if arrange_list.find('ComponentNumber').text:
							botdiv_element.text = "Subseries " + arrange_list.find('ComponentNumber').text + ":  " + arrange_list.find('ComponentName').text + ", " + cmpnt_info.find('SeriesDate').text
							dupl_arrange.append(botdiv_element.text.strip().lower())
						else:
							botdiv_element.text = "Subseries:  " + arrange_list.find('ComponentName').text + ", " + cmpnt_info.find('SeriesDate').text
							dupl_arrange.append(botdiv_element.text.strip().lower())
					else:
						if arrange_list.find('ComponentNumber').text:
							botdiv_element.text = "Subseries " + arrange_list.find('ComponentNumber').text + ":  " + arrange_list.find('ComponentName').text
							dupl_arrange.append(botdiv_element.text.strip().lower())
						else:
							botdiv_element.text = "Subseries:  " + arrange_list.find('ComponentName').text
							dupl_arrange.append(botdiv_element.text.strip().lower())
				else:
					botdiv_element = ET.Element('div')
					topdiv_element.append(botdiv_element)
					botdiv_element.set('style', 'margin-left:75pt')
					for ComponentSheet in input:
						if ComponentSheet.find('SeriesName') is None:
							if ComponentSheet.find('SeriesNumber') is None:
								pass
							else:
								if ComponentSheet.find('SeriesNumber').text == arrange_list.find('ComponentNumber').text:
									cmpnt_info = ComponentSheet
						elif ComponentSheet.find('SeriesName').text == arrange_list.find('ComponentName').text:
							cmpnt_info = ComponentSheet
					if cmpnt_info.find('SeriesDate').text:
						if arrange_list.find('ComponentNumber').text:
							botdiv_element.text = "Subseries " + arrange_list.find('ComponentNumber').text + ":  " + arrange_list.find('ComponentName').text + ", " + cmpnt_info.find('SeriesDate').text
							dupl_arrange.append(botdiv_element.text.strip().lower())
						else:
							botdiv_element.text = "Subseries:  " + arrange_list.find('ComponentName').text + ", " + cmpnt_info.find('SeriesDate').text
							dupl_arrange.append(botdiv_element.text.strip().lower())
					else:
						if arrange_list.find('ComponentNumber').text:
							botdiv_element.text = "Subseries " + arrange_list.find('ComponentNumber').text + ":  " + arrange_list.find('ComponentName').text
							dupl_arrange.append(botdiv_element.text.strip().lower())
						else:
							botdiv_element.text = "Subseries:  " + arrange_list.find('ComponentName').text
							dupl_arrange.append(botdiv_element.text.strip().lower())
	if CSheet.find('CollectionArrangement') is None:
		pass
	else:
		for arrange_display in reversed(CSheet.find('CollectionArrangement')):
			match_count = 0
			for line in dupl_arrange:
				match_ratio = 0
				if arrange_display.find('Text').text:
					match_ratio = SM(None,  arrange_display.find('Text').text.strip().lower(), line).ratio()
				if match_ratio > 0.3:
					match_count = match_count + 1
			if match_count < 1:
				p_element = ET.Element('p')
				html_root.find("body/table/tr/td[@id='main']").insert(arrange_index, p_element)
				p_element.text = arrange_display.find('Text').text
				p_element.set('style', 'margin-left:25pt')
	access_index = html_root.find("body/table/tr/td[@id='main']").getchildren().index(html_root.find("body/table/tr/td/h4[@id='access']")) + 1
	for access_display in reversed(CSheet.find('Access')):
		if access_display.tag == "Statement":
			p_element = ET.Element('p')
			html_root.find("body/table/tr/td[@id='main']").insert(access_index, p_element)
			p_element.text = access_display.text
			p_element.set('style', 'margin-left:50pt')
	use_index = html_root.find("body/table/tr/td[@id='main']").getchildren().index(html_root.find("body/table/tr/td/h4[@id='use']")) + 1
	for use_display in reversed(CSheet.find('UseRestrictions')):
		if use_display.tag == "Statement":
			p_element = ET.Element('p')
			html_root.find("body/table/tr/td[@id='main']").insert(use_index, p_element)
			p_element.text = use_display.text
			p_element.set('style', 'margin-left:50pt')
	
	if CSheet.find('ControlledAccess/AccessPoint/Part') is None:
		pass
	else:
		if CSheet.find('ControlledAccess/AccessPoint/Part').text:
			heading_index = html_root.find("body/table/tr/td[@id='main']").getchildren().index(html_root.find("body/table/tr/td/hr[@id='headings']")) + 1
			h3_element = ET.Element('h3')
			html_root.find("body/table/tr/td[@id='main']").insert(heading_index, h3_element)
			b_element = ET.Element('b')
			h3_element.append(b_element)
			a_element = ET.Element('a')
			b_element.append(a_element)
			a_element.set("name", "d0e112")
			a_element.text = "Subject Headings"
			main_div_element = ET.Element('div')
			html_root.find("body/table/tr/td[@id='main']").insert(heading_index + 1, main_div_element)
			persname = False
			corpname = False
			subject = False
			geogname = False
			famname = False
			occupation = False
			title = False
			name = False
			genreform = False
			for point in CSheet.find('ControlledAccess'):
				if point.find('ElementName').text == "persname":
					persname = True
				if point.find('ElementName').text == "corpname":
					corpname = True
				if point.find('ElementName').text == "subject":
					subject = True
				if point.find('ElementName').text == "geogname":
					geogname = True
				if point.find('ElementName').text == "famname":
					famname = True
				if point.find('ElementName').text == "occupation":
					occupation = True
				if point.find('ElementName').text == "title":
					title = True
				if point.find('ElementName').text == "name":
					name = True
				if point.find('ElementName').text == "genreform":
					genreform = True
			if persname == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Persons"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "persname":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
			if corpname == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Corporate Bodies"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "corpname":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
			if subject == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Subjects"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "subject":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
			if geogname == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Places"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "geogname":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
			if famname == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Family Names"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "famname":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
			if occupation == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Occupations"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "occupation":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
			if title == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Titles"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "title":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
			if name == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Names"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "name":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
			if genreform == True:
				h4_element = ET.Element('h4')
				main_div_element.append(h4_element)
				h4_element.set("style", "margin-left:25pt")
				b_element = ET.Element('b')
				h4_element.append(b_element)
				b_element.text = "Genres and Forms"
				for heading in CSheet.find('ControlledAccess'):
					if heading.find('ElementName').text.lower() == "genreform":
						div_element = ET.Element('div')
						main_div_element.append(div_element)
						div_element.text = heading.find('Part').text
						div_element.set("style", "margin-left:50pt")
					
	cite_index = html_root.find("body/table/tr/td[@id='main']").getchildren().index(html_root.find("body/table/tr/td/p[@id='cite']")) + 1
	for cite_display in CSheet.find('PreferredCitation'):
		p_element = ET.Element('p')
		html_root.find("body/table/tr/td[@id='main']").insert(cite_index, p_element)
		p_element.text = cite_display.text
		p_element.set('style', 'margin-left:50pt')
	
	prov_index = html_root.find("body/table/tr/td[@id='main']").getchildren().index(html_root.find("body/table/tr/td/h4[@id='prov']")) + 1
	if CSheet.find('AcquisitionInfo/Acquis') is None:
		pass
	else:
		for prov_display in reversed(CSheet.find('AcquisitionInfo')):
			if prov_display.find('Event').text:
				p_element = ET.Element('p')
				html_root.find("body/table/tr/td[@id='main']").insert(prov_index, p_element)
				if prov_display.find('Date').text:
					p_element.text = prov_display.find('Date').text + ": " + prov_display.find('Event').text
					p_element.set('style', 'margin-left:50pt')
				else:
					p_element.text = prov_display.find('Event').text
					p_element.set('style', 'margin-left:50pt')
	
	if CSheet.find('EADCreator').text:
		html_root.find("body/table/tr/td/p[@id='author']").text = "Created by: " + CSheet.find('EADCreator').text
	if CSheet.find('EADCreationDate').text:
		html_root.find("body/table/tr/td/p[@id='fadate']").text = "Creation Date: " + CSheet.find('EADCreationDate').text
	
	for revision in CSheet.find('Revisions'):
		html_root.find("body/table/tr/td/p[@id='revision']").text = "Revision history:"
		p_element = ET.Element('p')
		p_element.set("style", "margin-left:75pt")
		html_root.find("body/table/tr/td/p[@id='revision']").append(p_element)
		if revision.find('Type').text and revision.find('Date').text and revision.find('Description').text is None:
			p_element.text = " - "
		else:
			if revision.find('Type').text:
				p_element.text = revision.find('Type').text.title() + ","
			else:
				p_element.text = ""
			if revision.find('Date').text:
				p_element.text = p_element.text + " " + revision.find('Date').text
			if revision.find('Description').text:
				p_element.text = p_element.text + " - " + revision.find('Description').text
	
	table_columns = html_root.find("body/table/tr/td/table[@id='component']/tr[@id='columns']")
	column_labels = html_root.find("body/table/tr/td/table[@id='component']/tr[@id='column_labels']")
	return_link = html_root.find("body/table/tr/td/table[@id='component']/tr[@id='return_link']")
	main_root = html_root.find("body/table/tr/td[@id='main']")
	main_root.remove(main_root.find("table[@id='component']"))
	
	cmpnt_index = main_root.getchildren().index(html_root.find("body/table/tr/td/h3[@id='list']")) + 1
	for cmpnt in reversed(CSheet.find('CollectionMap')):
		make_table = False
		if cmpnt.find('ComponentLevel').text and cmpnt.find('ComponentNumber').text:
			make_table = True
		if cmpnt.find('ComponentName').text:
			if cmpnt.find('ComponentName').text.lower() == "no series" or cmpnt.find('ComponentName').text.lower() == "noseries":
				make_table = True
			elif cmpnt.find('ComponentName').text:
				make_table = True
		if make_table == True:
			for series_tag in input:
				if series_tag.find('SeriesName') is None:
					pass
				else:
					if series_tag.find('SeriesName').text:
						if series_tag.find('SeriesName').text.strip().lower() == cmpnt.find('ComponentName').text.strip().lower():
							cmpnt_info = series_tag
			if cmpnt.find('ComponentName').text:
				if cmpnt.find('ComponentName').text.lower() == "no series" or cmpnt.find('ComponentName').text.lower() == "noseries":
					cmpnt_info = input.find('Series1')
			table_element = ET.Element('table')
			main_root.insert(cmpnt_index, table_element)
			table_element.append(table_columns)
			tr_name_element = ET.Element('tr')
			table_element.append(tr_name_element)
			td_element = ET.Element('td')
			td_name_element = ET.Element('td')
			if cmpnt.find('ComponentLevel').text:
				if int(cmpnt.find('ComponentLevel').text) > 1:
					tr_name_element.append(td_element)
					tr_name_element.append(td_name_element)
					td_name_element.set("colspan", "11")
				else:
					tr_name_element.append(td_name_element)
					td_name_element.set("colspan", "12")
			else:
				tr_name_element.append(td_name_element)
				td_name_element.set("colspan", "12")
			b_name_element = ET.Element('b')
			td_name_element.append(b_name_element)
			b_name_element.set("width", "100%")
			b_name_element.set("position", "relative")
			a_name_element = ET.Element('a')
			b_name_element.append(a_name_element)
			if cmpnt_info.find('SeriesNumber').text:
				anchor = "series" + cmpnt_info.find('SeriesNumber').text
				a_name_element.set("name", anchor)
				a_name_element.set("style", "font-size: 18px")
			else:
				if cmpnt_info.find('SeriesName').text:
					anchor = "series" + escape_tag(cmpnt_info.find('SeriesName').text)
					a_name_element.set("name", anchor)
					a_name_element.set("style", "font-size: 18px")
					
			main_extent = ""
			for physdesc in reversed(cmpnt_info.find('PhysicalDescriptionSet')):
				if physdesc.find('Coverage') is None or physdesc.find('Type') is None or physdesc.find('Approximate') is None or physdesc.find('Quantity') is None or physdesc.find('UnitType') is None or physdesc.find('PhysicalFacet') is None or physdesc.find('Dimensions') is None or physdesc.find('DimensionsUnit') is None or physdesc.find('PhysDescNote') is None: 
					pass
				else:
					if physdesc.find('Coverage').text:
						if physdesc.find('Coverage').text.lower() == "whole":
							if physdesc.find('Quantity').text and physdesc.find('UnitType').text:
								main_extent = physdesc.find('Quantity').text + " " + physdesc.find('UnitType').text
							elif physdesc.find('Dimensions').text and physdesc.find('DimensionsUnit').text:
								main_extent = physdesc.find('Dimensions').text + " " + physdesc.find('DimensionsUnit').text
							elif physdesc.find('Quantity').text:
								main_extent = physdesc.find('Quantity').text
					else:
						if physdesc.find('Quantity').text and physdesc.find('UnitType').text:
							main_extent = physdesc.find('Quantity').text + " " + physdesc.find('UnitType').text
						elif physdesc.find('Dimensions').text and physdesc.find('DimensionsUnit').text:
							main_extent = physdesc.find('Dimensions').text + " " + physdesc.find('DimensionsUnit').text
						elif physdesc.find('Quantity').text:
							main_extent = physdesc.find('Quantity').text
			if cmpnt.find('ComponentLevel').text:
				if int(cmpnt.find('ComponentLevel').text) > 1:
					label = "Subseries"
				else:
					label = "Series"
				if cmpnt_info.find('SeriesName').text:
					if cmpnt.find('SeriesDate') is None:
						if len(main_extent) == 0:
							if label.lower() in cmpnt_info.find('SeriesName').text.lower():
								a_name_element.text = cmpnt_info.find('SeriesName').text
							else:
								if cmpnt_info.find('SeriesNumber').text:
									a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text
								else:
									a_name_element.text = cmpnt_info.find('SeriesName').text
						else:
							if label.lower() in cmpnt_info.find('SeriesName').text.lower():
								if cmpnt_info.find('SeriesNumber').text:
									a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text
								else:
									a_name_element.text = cmpnt_info.find('SeriesName').text
							else:
								if cmpnt_info.find('SeriesNumber').text:
									a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text 	+ " (" + main_extent + ")"
								else:
									a_name_element.text = cmpnt_info.find('SeriesName').text 	+ " (" + main_extent + ")"
					else:
						if cmpnt.find('SeriesDate').text:
							if len(main_extent) == 0:
								if label.lower() in cmpnt_info.find('SeriesName').text.lower():
									a_name_element.text = cmpnt_info.find('SeriesName').text + ", " + cmpnt_info.find('SeriesDate').text
								else:
									if cmpnt_info.find('SeriesNumber').text:
										a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text + ", " + cmpnt_info.find('SeriesDate').text
									else:
										a_name_element.text = cmpnt_info.find('SeriesName').text + ", " + cmpnt_info.find('SeriesDate').text
							else:
								if label.lower() in cmpnt_info.find('SeriesName').text.lower():
									if cmpnt_info.find('SeriesNumber').text:
										a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text + ", " + cmpnt_info.find('SeriesDate').text
									else:
										a_name_element.text = cmpnt_info.find('SeriesName').text + ", " + cmpnt_info.find('SeriesDate').text
								else:
									if cmpnt_info.find('SeriesNumber').text:
										a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text + ", " + cmpnt_info.find('SeriesDate').text 	+ " (" + main_extent + ")"
									else:
										a_name_element.text = cmpnt_info.find('SeriesName').text + ", " + cmpnt_info.find('SeriesDate').text 	+ " (" + main_extent + ")"
						else:
							if len(main_extent) == 0:
								if label.lower() in cmpnt_info.find('SeriesName').text.lower():
									a_name_element.text = cmpnt_info.find('SeriesName').text
								else:
									if cmpnt_info.find('SeriesNumber').text:
										a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text
									else:
										a_name_element.text = cmpnt_info.find('SeriesName').text
							else:
								if label.lower() in cmpnt_info.find('SeriesName').text.lower():
									if cmpnt_info.find('SeriesNumber').text:
										a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text
									else:
										a_name_element.text = cmpnt_info.find('SeriesName').text
								else:
									if cmpnt_info.find('SeriesNumber').text:
										a_name_element.text = label + " " + cmpnt_info.find('SeriesNumber').text + ": " + cmpnt_info.find('SeriesName').text 	+ " (" + main_extent + ")"
									else:
										a_name_element.text = cmpnt_info.find('SeriesName').text 	+ " (" + main_extent + ")"
			# Arrangement
			if cmpnt_info.find('Arrangement/p'):
				for arrange in cmpnt_info.find('Arrangement'):
					if arrange.text is None:
						pass
					else:
						tr_arr_element = ET.Element('tr')
						td_element = ET.Element('td')
						td_arr_element = ET.Element('td')
						table_element.append(tr_arr_element)
						if int(cmpnt.find('ComponentLevel').text) > 1:
							tr_arr_element.append(td_element)
							tr_arr_element.append(td_arr_element)
							td_arr_element.set("colspan", "11")
						else:
							tr_arr_element.append(td_arr_element)
							td_arr_element.set("colspan", "12")
						td_arr_element.text = arrange.text
			
			# Series Scope and Content
			for scope in cmpnt_info.find('Description'):
				if scope.text is None:
					pass
				else:
					tr_acope_element = ET.Element('tr')
					td_element = ET.Element('td')
					td_scope_element = ET.Element('td')
					table_element.append(tr_acope_element)
					if int(cmpnt.find('ComponentLevel').text) > 1:
						tr_acope_element.append(td_element)
						tr_acope_element.append(td_scope_element)
						td_scope_element.set("colspan", "11")
					else:
						tr_acope_element.append(td_scope_element)
						td_scope_element.set("colspan", "12")
					td_scope_element.text = scope.text
			
			table_element.append(column_labels)
			
			for record in cmpnt_info:
				if record.tag == "Record":
					if record.find('UnitTitle').text:
						#print record.find('UnitTitle').text
						#Record level physdesc
						record_extent = ""
						if record.find('Quantity').text and record.find('UnitType').text:
							if record.find('Dimensions').text and record.find('DimensionsUnit').text:
								record_extent = record.find('Quantity').text + " " + record.find('UnitType').text + ", " + record.find('Dimensions').text + " " + record.find('DimensionsUnit').text
							elif record.find('Dimensions').text:
								record_extent = record.find('Quantity').text + " " + record.find('UnitType').text + ", " + record.find('Dimensions').text
							else:
								record_extent = record.find('Quantity').text + " " + record.find('UnitType').text
						elif record.find('Dimensions').text and record.find('DimensionsUnit').text:
							record_extent = record.find('Dimensions').text + " " + record.find('DimensionsUnit').text
						elif record.find('Quantity').text:
							if record.find('Dimensions').text:
								record_extent = record.find('Quantity').text + ", " + record.find('Dimensions').text
							else:
								record_extent = record.find('Quantity').text
						elif record.find('Dimensions').text:
							record_extent = record.find('Dimensions').text
						if record.find('PhysicalFacet').text:
							record_extent = record_extent + " (" + record.find('PhysicalFacet').text + ")"
						
						tr_record_element = ET.Element('tr')
						table_element.append(tr_record_element)
						td_box = ET.Element('td')
						tr_record_element.append(td_box)
						td_box.set("valign", "top")
						if record.find('BoxName').text:
							if record.find('BoxName').text.lower() == 'box':
								td_box.text = record.find('BoxNumber').text
							elif record.find('BoxNumber').text:
								td_box.text = record.find('BoxName').text + " " + record.find('BoxNumber').text
						elif record.find('BoxNumber').text:
							td_box.text = record.find('BoxNumber').text
						td_folder = ET.Element('td')
						tr_record_element.append(td_folder)
						td_folder.set("valign", "top")
						if record.find('Unit').text:
							if record.find('Unit').text.lower() == 'folder' or  record.find('Unit').text.lower() == 'file':
								td_folder.text = record.find('UnitNumber').text
							elif record.find('UnitNumber').text:
								td_folder.text = record.find('Unit').text + " " + record.find('UnitNumber').text
						elif record.find('UnitNumber').text:
							td_folder.text = record.find('UnitNumber').text
						td_title = ET.Element('td')
						tr_record_element.append(td_title)
						td_title.set("valign", "top")
						if len(record_extent) == 0:
							td_title.set("colspan", "10")
						else:
							td_title.set("colspan", "9")
						if record.find('DigitalObjectLink').text:
							link_element = ET.Element('a')
							td_title.append(link_element)
							if record.find('DigitalObjectLink').text.startswith('http'):
								link_element.set('href', record.find('DigitalObjectLink').text)
							else:
								link_element.set('href', "http://" + record.find('DigitalObjectLink').text)
							link_element.text = record.find('UnitTitle').text
							link_element.tail = ""
							if record.find('Date1').text:
								link_element.tail = link_element.tail + ", " + record.find('Date1').text
							if record.find('Date2').text:
								link_element.tail = link_element.tail + ", " + record.find('Date2').text
							if record.find('Date3').text:
								link_element.tail = link_element.tail + ", " + record.find('Date3').text
							if record.find('Date4').text:
								link_element.tail = link_element.tail + ", " + record.find('Date4').text
							if record.find('Date5').text:
								link_element.tail = link_element.tail + ", " + record.find('Date5').text
						else:
							td_title.text = record.find('UnitTitle').text
							if record.find('Date1').text:
								td_title.text = td_title.text + ", " + record.find('Date1').text
							if record.find('Date2').text:
								td_title.text = td_title.text + ", " + record.find('Date2').text
							if record.find('Date3').text:
								td_title.text = td_title.text + ", " + record.find('Date3').text
							if record.find('Date4').text:
								td_title.text = td_title.text + ", " + record.find('Date4').text
							if record.find('Date5').text:
								td_title.text = td_title.text + ", " + record.find('Date5').text
						
						# Physdesc
						if len(record_extent) == 0:
							pass
						else:
							td_physdesc_element = ET.Element('td')
							td_physdesc_element.set("valign", "top")
							tr_record_element.append(td_physdesc_element)
							td_physdesc_element.text = record_extent
						
			table_element.append(return_link)
			hr_element = ET.Element('hr')
			table_element.append(hr_element)
						
					
	
	return html_root