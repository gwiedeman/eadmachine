# module for the <eadheader/> or <control/> portion
import xml.etree.cElementTree as ET
import globals
from messages import error

def language(did_root, CSheet, version):
	if CSheet.find('Languages/Language/Lang').text:
		if version == "ead3":
			if did_root.find('langmaterial') is None:
				if "add_langmat" in globals.new_elements or "add-all" in globals.add_all:
					langmat_element = ET.Element('langmaterial')
					did_root.append(langmat_element)
					for new_lang in CSheet.find('Languages'):
						if new_lang.find('Lang').text:
							langset_element = ET.Element('languageset')
							langmat_element.append(langset_element)
							lang_element = ET.Element('language')
							langset_element.append(lang_element)
							lang_element.text = new_lang.find('Lang').text
							if new_lang.find('LangCode').text:
								lang_element.set('langcode', new_lang.find('LangCode').text)
							script_element = ET.Element('script')
							langset_element.append(script_element)
							script_element.text = new_lang.find('Script').text
							if new_lang.find('ScriptCode').text:
								script_element.set('scriptcode', new_lang.find('ScriptCode').text)
							if new_lang.find('LangNote').text:
								langnote_element = ET.Element('descriptivenote')
								langset_element.append(langnote_element)
								langnote_element.text = new_lang.find('LangNote').text
			else:
				did_root.find('langmaterial').clear()
				for new_lang in CSheet.find('Languages'):
					if new_lang.find('Lang').text:
						langset_element = ET.Element('languageset')
						did_root.find('langmaterial').append(langset_element)
						lang_element = ET.Element('language')
						langset_element.append(lang_element)
						lang_element.text = new_lang.find('Lang').text
						if new_lang.find('LangCode').text:
							lang_element.set('langcode', new_lang.find('LangCode').text)
						script_element = ET.Element('script')
						langset_element.append(script_element)
						script_element.text = new_lang.find('Script').text
						if new_lang.find('ScriptCode').text:
							script_element.set('scriptcode', new_lang.find('ScriptCode').text)
						if new_lang.find('LangNote').text:
							langnote_element = ET.Element('descriptivenote')
							langset_element.append(langnote_element)
							langnote_element.text = new_lang.find('LangNote').text
		else: #ead 2002
			if did_root.find('langmaterial') is None:
				if "add_langmat" in globals.new_elements or "add-all" in globals.add_all:
					langmat_element = ET.Element('langmaterial')
					did_root.append(langmat_element)
					for lang in CSheet.find('Languages'):
						if lang.find('Lang').text:
							lang_element = ET.Element('language')
							langmat_element.append(lang_element)
							lang_element.text = lang.find('Lang').text
							if lang.find('LangCode').text:
								lang_element.set('langcode', lang.find('LangCode').text)
					for lang in CSheet.find('Languages'): 
						if lang.find('LangNote').text:
							last_language = langmat_element.find('language[last()]')
							if last_language.tail:
								last_language.tail = last_language.tail + ", " + lang.find('LangNote').text
							else:
								last_language.tail = ", " + lang.find('LangNote').text
			else:
				if did_root.find('langmaterial/language') is None:
					for lang in CSheet.find('Languages'):
						if lang.find('Lang').text:
							lang_element = ET.Element('language')
							did_root.find('langmaterial').append(lang_element)
							lang_element.text = lang.find('Lang').text
							if lang.find('LangCode').text:
								lang_element.set('langcode', lang.find('LangCode').text)
					for lang in CSheet.find('Languages'): 
						if lang.find('LangNote').text:
							last_language = did_root.find('langmaterial/language[last()]')
							if last_language.tail:
								last_language.tail = last_language.tail + ", " + lang.find('LangNote').text
							else:
								last_language.tail = ", " + lang.find('LangNote').text
				else:
					did_root.find('langmaterial').clear()
					for lang in CSheet.find('Languages'):
						if lang.find('Lang').text:
							lang_element = ET.Element('language')
							did_root.find('langmaterial').append(lang_element)
							lang_element.text = lang.find('Lang').text
							if lang.find('LangCode').text:
								lang_element.set('langcode', lang.find('LangCode').text)
					for lang in CSheet.find('Languages'): 
						if lang.find('LangNote').text:
							last_language = did_root.find('langmaterial/language[last()]')
							if last_language.tail:
								last_language.tail = last_language.tail + ", " + lang.find('LangNote').text
							else:
								last_language.tail = ", " + lang.find('LangNote').text
	else:
		did_root.find('langmaterial').clear()
		if version == "ead3":
			error("You did not enter a collection language. <language> is required in EAD3, so your finding aid will not be valid.", False)
			language_element = ET.Element('language')
			did_root.find('langmaterial').append(language_element)