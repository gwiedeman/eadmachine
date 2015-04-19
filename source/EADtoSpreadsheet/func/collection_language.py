# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals
from messages import error

def language(did_root, CSheet, version):
	if did_root.find('langmaterial') is None:
		pass
	else:
		if version == "ead3":
			if did_root.find('langmaterial/languageset') is None:
				if did_root.find('langmaterial/language') is None:
					CSheet.find('Languages').clear()
					for lang in did_root.find('langmaterial'):
						if lang.tag == "language":
							Language_element = ET.Element('Language')
							CSheet.find('Languages').append(Language_element)
							Lang_element = ET.Element('Lang')
							Language_element.append(Lang_element)
							Lang_element.text = lang.text
							LangCode_element = ET.Element('LangCode')
							Language_element.append(LangCode_element)
							if "langcode" in lang.attrib:
								LangCode_element.text = lang.attrib['langcode']
							Script_element = ET.Element('Script')
							Language_element.append(Script_element)
							ScriptCode_element = ET.Element('ScriptCode')
							Language_element.append(ScriptCode_element)
							LangNote_element = ET.Element('LangNote')
							Language_element.append(LangNote_element)
			else:
				CSheet.find('Languages').clear()
				for lang in did_root.find('langmaterial'):
					if lang.tag == "languageset":
						Language_element = ET.Element('Language')
						CSheet.find('Languages').append(Language_element)
						Lang_element = ET.Element('Lang')
						Language_element.append(Lang_element)
						Lang_element.text = lang.find('language').text
						LangCode_element = ET.Element('LangCode')
						Language_element.append(LangCode_element)
						if "langcode" in lang.find('language').attrib:
							LangCode_element.text = lang.find('language').attrib['langcode']
						Script_element = ET.Element('Script')
						Language_element.append(Script_element)
						ScriptCode_element = ET.Element('ScriptCode')
						Language_element.append(ScriptCode_element)
						if lang.find('script') is None:
							pass
						else:
							Script_element.text = lang.find('script').text
							if "scriptcode" in lang.find('script').attrib:
								ScriptCode_element.text = lang.find('script').attrib['scriptcode']
						LangNote_element = ET.Element('LangNote')
						Language_element.append(LangNote_element)
						if lang.find('descriptivenote') is None:
							pass
						else:
							LangNote_element.text = lang.find('descriptivenote').text
		else:
			if did_root.find('langmaterial/language') is None:
				if did_root.find('langusage').text:
					CSheet.find('Languages/Language/Lang').text = did_root.find('langmaterial').text
			else:
				CSheet.find('Languages').clear()
				for lang in did_root.find('langmaterial'):
					if lang.tag == "language":
						Language_element = ET.Element('Language')
						CSheet.find('Languages').append(Language_element)
						Lang_element = ET.Element('Lang')
						Language_element.append(Lang_element)
						Lang_element.text = lang.text
						LangCode_element = ET.Element('LangCode')
						Language_element.append(LangCode_element)
						if "langcode" in lang.attrib:
							LangCode_element.text = lang.attrib['langcode']
						Script_element = ET.Element('Script')
						Language_element.append(Script_element)
						ScriptCode_element = ET.Element('ScriptCode')
						Language_element.append(ScriptCode_element)
						LangNote_element = ET.Element('LangNote')
						Language_element.append(LangNote_element)
						if did_root.find('langmaterial').text:
							LangNote_element.text = did_root.find('langmaterial').text
						if len(did_root.find('langmaterial').tail.strip()) >= 1:
							LangNote_element.text = LangNote_element.text + did_root.find('langmaterial').tail