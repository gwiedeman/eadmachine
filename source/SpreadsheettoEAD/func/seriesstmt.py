#module for Series Statement (<editionstmt>) for both <control> and <eadheader>
# Use when finding aid is part of a monograph series etc.
import xml.etree.cElementTree as ET
import globals

def seriesstmt(control_root, CSheet):
	if CSheet.find('PartofSeries').text or CSheet.find('NumberinSeries').text:
		if control_root.find('filedesc/seriesstmt') is None:
			if "add_seriesstmt" in globals.new_elements or "add-all" in globals.add_all:
				seriesstmt_par = control_root.find('filedesc')
				seriesstmt_element = ET.Element('seriesstmt')
				if control_root.find('filedesc/editionstmt') is None:
					if control_root.find('filedesc/publicationstmt') is None:
						series_index = 1
					else:
						series_index = 2
				else:
					if control_root.find('filedesc/publicationstmt') is None:
						series_index = 2
					else:
						series_index = 3
				seriesstmt_par.insert(series_index, seriesstmt_element)
				if CSheet.find('PartofSeries').text:
					series_title = ET.Element('titleproper')
					seriesstmt_element.append(series_title)
					series_title.text = CSheet.find('PartofSeries').text
				if CSheet.find('NumberinSeries').text:
					series_number = ET.Element('num')
					seriesstmt_element.append(series_number)
					series_number.text = CSheet.find('NumberinSeries').text
		else:
			if control_root.find('filedesc/seriesstmt/titleproper') is None or control_root.find('filedesc/seriesstmt/num') is None:
				if control_root.find('filedesc/seriesstmt/p') is None:
					if control_root.find('filedesc/seriesstmt/titleproper') is None:
						#<num> only
						if CSheet.find('NumberinSeries').text:
							if CSheet.find('PartofSeries').text:
								control_root.find('filedesc/seriesstmt/num').text = CSheet.find('NumberinSeries').text + " - " + CSheet.find('PartofSeries').text
							else:
								control_root.find('filedesc/seriesstmt/num').text = CSheet.find('NumberinSeries').text
						else:
							if CSheet.find('PartofSeries').text:
								control_root.find('filedesc/seriesstmt/num').text = CSheet.find('PartofSeries').text
							else:
								control_root.find('filedesc/seriesstmt/num').text = ""
					else:
						#<titleproper> only
						if CSheet.find('NumberinSeries').text:
							if CSheet.find('PartofSeries').text:
								control_root.find('filedesc/seriesstmt/titleproper').text = CSheet.find('NumberinSeries').text + " - " + CSheet.find('PartofSeries').text
							else:
								control_root.find('filedesc/seriesstmt/titleproper').text = CSheet.find('NumberinSeries').text
						else:
							if CSheet.find('PartofSeries').text:
								control_root.find('filedesc/seriesstmt/titleproper').text = CSheet.find('PartofSeries').text
							else:
								control_root.find('filedesc/seriesstmt/titleproper').text = ""
				else:
					if control_root.find('filedesc/seriesstmt/titleproper') is None:
						if control_root.find('filedesc/seriesstmt/num') is None:
							#<p> only
							if CSheet.find('NumberinSeries').text:
								if CSheet.find('PartofSeries').text:
									control_root.find('filedesc/seriesstmt/p').text = CSheet.find('NumberinSeries').text + " - " + CSheet.find('PartofSeries').text
								else:
									control_root.find('filedesc/seriesstmt/p').text = CSheet.find('NumberinSeries').text
							else:
								if CSheet.find('PartofSeries').text:
									control_root.find('filedesc/seriesstmt/p').text = CSheet.find('PartofSeries').text
								else:
									control_root.find('filedesc/seriesstmt/p').text = ""
						else:
							# <p> and <num>
							if CSheet.find('NumberinSeries').text:
								if CSheet.find('PartofSeries').text:
									control_root.find('filedesc/seriesstmt/num').text = CSheet.find('NumberinSeries').text
									control_root.find('filedesc/seriesstmt/p').text = CSheet.find('PartofSeries').text
								else:
									control_root.find('filedesc/seriesstmt/num').text = CSheet.find('NumberinSeries').text
									control_root.find('filedesc/seriesstmt/p').text = ""
							else:
								if CSheet.find('PartofSeries').text:
									control_root.find('filedesc/seriesstmt/num').text = ""
									control_root.find('filedesc/seriesstmt/p').text = CSheet.find('PartofSeries').text
								else:
									control_root.find('filedesc/seriesstmt/num').text = ""
									control_root.find('filedesc/seriesstmt/p').text = ""
					else:
						# <titleproper> and <p>
						if CSheet.find('PartofSeries').text:
							if CSheet.find('NumberinSeries').text:
								control_root.find('filedesc/seriesstmt/titleproper').text = CSheet.find('PartofSeries').text
								control_root.find('filedesc/seriesstmt/p').text = CSheet.find('NumberinSeries').text
							else:
								control_root.find('filedesc/seriesstmt/titleproper').text = CSheet.find('PartofSeries').text
								control_root.find('filedesc/seriesstmt/p').text = ""
						else:
							if CSheet.find('NumberinSeries').text:
								control_root.find('filedesc/seriesstmt/titleproper').text = ""
								control_root.find('filedesc/seriesstmt/p').text = CSheet.find('NumberinSeries').text
							else:
								control_root.find('filedesc/seriesstmt/titleproper').text = ""
								control_root.find('filedesc/seriesstmt/p').text = ""
			else:
				if control_root.find('filedesc/seriesstmt/p') is None:
					pass
				else:
					control_root.find('filedesc/seriesstmt/p').text = ""
				#uses both <titleproper> and <num>
				if CSheet.find('PartofSeries').text:
					if CSheet.find('NumberinSeries').text:
						control_root.find('filedesc/seriesstmt/titleproper').text = CSheet.find('PartofSeries').text
						control_root.find('filedesc/seriesstmt/num').text = CSheet.find('NumberinSeries').text
					else:
						control_root.find('filedesc/seriesstmt/titleproper').text = CSheet.find('PartofSeries').text
						control_root.find('filedesc/seriesstmt/num').text = ""
				else:
					if CSheet.find('NumberinSeries').text:
						control_root.find('filedesc/seriesstmt/titleproper').text = ""
						control_root.find('filedesc/seriesstmt/num').text = CSheet.find('NumberinSeries').text
					else:
						control_root.find('filedesc/seriesstmt/titleproper').text = ""
						control_root.find('filedesc/seriesstmt/num').text = ""
	else:
		if control_root.find('filedesc/seriesstmt') is None:
			pass
		else:
			control_root.find('filedesc/seriesstmt').clear()