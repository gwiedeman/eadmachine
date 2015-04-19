#module for Series Statement (<editionstmt>) for both <control> and <eadheader>
# Use when finding aid is part of a monograph series etc.
import xml.etree.cElementTree as ET
import globals

def seriesstmt(control_root, CSheet):
	if control_root.find('filedesc/seriesstmt') is None:
		pass
	else:
		if control_root.find('filedesc/seriesstmt/num') is None:
			pass
		else:
			CSheet.find('NumberinSeries').text = control_root.find('filedesc/seriesstmt/num').text
		if control_root.find('filedesc/seriesstmt/titleproper') is None:
			if control_root.find('filedesc/seriesstmt/p') is None:
				pass
			else:
				CSheet.find('PartofSeries').text = control_root.find('filedesc/seriesstmt/p').text
		else:
			if control_root.find('filedesc/seriesstmt/p') is None:
				CSheet.find('PartofSeries').text = control_root.find('filedesc/seriesstmt/titleproper').text
			else:
				CSheet.find('PartofSeries').text = control_root.find('filedesc/seriesstmt/titleproper').text  + ", " + control_root.find('filedesc/seriesstmt/p').text