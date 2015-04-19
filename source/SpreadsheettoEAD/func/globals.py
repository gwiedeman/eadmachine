# This file checks if data from the input spreadsheet does not fit into the selected EAD template
# It will ask a series of prompts to see if a user wants to add tags to fit this data or ignore items

def init():
	global new_elements
	global add_all
	new_elements = ["ask_gui", "add_author", "add_subtitle", "add_sponsor", "add_edition", "add_publication", "add_seriesstmt", "add_notestmt", "add_profile", "add_eadcre", "add_lang1", "add_descrule", "add_revisions", "add_otherid", "add_rep", "add_pubstatus", "add_langdec", "add_stancon", "add_localcon", "add_localctr", "add_sources", "add_relation", "add_bulkdate", "add_abstract", "add_origin", "add_physdesc", "add_langmat", "add_accessrestrict", "add_accruals", "add_acq", "add_altforms", "add_appraisal", "add_arrange", "add_biblio", "add_bio", "add_controlaccess", "add_custhistory", "add_legalstatus", "add_otherfa", "add_phystech", "add_prefcite", "add_processinfo", "add_related", "add_scope", "add_sepmat", "add_userestrict"]
	add_all = []