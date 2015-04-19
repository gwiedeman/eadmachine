import xml.etree.cElementTree as ET

#copies the contents of a node that might have mixed content using the raw string
def mixed_content(node):
   raw_string = ET.tostring(node)
   no_namespace = raw_string.replace('ns0:', '')
   if "<" in no_namespace:
	   no_open_tag = no_namespace.split('>', 1)[1]
	   close_tag_index = no_open_tag.rfind("<")
	   no_close_tag = no_open_tag[:close_tag_index]
	   return no_close_tag
   else:
	   return no_namespace