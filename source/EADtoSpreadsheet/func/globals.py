# This file checks if data from the input spreadsheet does not fit into the selected EAD template
# It will ask a series of prompts to see if a user wants to add tags to fit this data or ignore items

def init():
	global new_elements
	global add_all
	new_elements = ["ask_gui"]
	add_all = []