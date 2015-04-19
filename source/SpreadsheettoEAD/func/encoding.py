# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)
	
	
def escape_tag(string):
	lessthen = string.replace('&lt;', '')
	greaterthen = lessthen.replace('&gt;', '')
	lessthen2 = greaterthen.replace('<', '')
	greaterthen2 = lessthen2.replace('>', '')
	lessthen3 = greaterthen2.replace('\"', '')
	greaterthen3 = lessthen3.replace('\"', '')
	lessthen4 = greaterthen3.replace('&quot;', '')
	return lessthen4
	
def clear_tags(node):
	string = "".join(node.itertext())
	return string
	
def textify(old_string):
	lessthen = old_string.replace('&lt;', '<')
	greaterthen = lessthen.replace('&gt;', '>')
	parseable = "<open>" + greaterthen + "</open>"
	node = ET.fromstring(strip_non_ascii(parseable))
	string = ""
	if node.text:
		string = string + node.text
	for sub in node:
		if sub.text:
			string = string + sub.text
		for subsub in sub:
			if subsub.text:
				string = string + subsub.text
			for subsubsub in subsub:
				if subsubsub.text:
					string = string + subsubsub.text
				if subsubsub.tail:
					string = string + subsubsub.tail
			if subsub.tail:
				string = string + subsub.tail
		if sub.tail:
			string = string + sub.tail
	return string