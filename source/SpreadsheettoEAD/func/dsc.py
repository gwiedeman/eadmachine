# module for the Container List <dsc>
import xml.etree.cElementTree as ET
from components import components
import globals
import wx

def dsc(dsc_root, input_data, version):
	from wx.lib.pubsub import pub
	if "ask_gui" in globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Writing <dsc>...")
	
	collectionID = ""
	collectionID = input_data.find('CollectionSheet/CollectionID').text
	old_head = dsc_root.find('head')
	old_attrib = dsc_root.attrib
	if dsc_root.find('c'):
		number = False
	elif dsc_root.find('c01'):
		number = True
	if dsc_root.find('c01/did'):
		old_did = dsc_root.find('c01/did')
	elif dsc_root.find('c/did'):
		old_did = dsc_root.find('c/did')
	arr_head = ""
	sc_head = ""
	if dsc_root.find('c01') is None:
		if dsc_root.find('c') is None:
			old_ser = ET.Element('old_ser')
		else:
			old_ser = dsc_root.find('c')
	else:
		old_ser = dsc_root.find('c01')
	if dsc_root.find('c01/c02') is None:
		if dsc_root.find('c/c') is None:
			old_cmpt = ET.Element('old_cmpt')
		else:
			old_cmpt = dsc_root.find('c/c')
	else:
		old_cmpt = dsc_root.find('c01/c02')
	if dsc_root.find('c01/arrangement/head') is None:
		pass
	else:
		arr_head = dsc_root.find('c01/arrangement/head')
	if dsc_root.find('c/arrangement/head') is None:
		pass
	else:
		arr_head = dsc_root.find('c/arrangement/head')
	if dsc_root.find('c01/scopecontent/head') is None:
		pass
	else:
		sc_head = dsc_root.find('c01/scopecontent/head')
	if dsc_root.find('c/scopecontent/head') is None:
		pass
	else:
		sc_head = dsc_root.find('c/scopecontent/head')
	old_physdesc = ""
	if dsc_root.iter('physdesc') is None:
		pass
	else:
		old_physdesc = dsc_root.find('.//physdesc')
	if dsc_root.find('c/did/physdescstructuredset') and dsc_root.find('c/did/physdescstructured') and dsc_root.find('c01/did/physdescstructuredset') and dsc_root.find('c01/did/physdescstructured') is None:
		old_physdescstructured = False
	else:
		old_physdescstructured = True
	component_era = ""
	component_cal = ""
	if dsc_root.find('c/did/unittitle/unitdate') is None:
		if dsc_root.find('c/did/unitdate') is None:
			if dsc_root.find('c01/did/unittitle/unitdate') is None:
				if dsc_root.find('c01/did/unitdate') is None:
					pass
				else:
					if 'era' in dsc_root.find('c01/did/unitdate').attrib:
						component_era = dsc_root.find('c01/did/unitdate').attrib['era']
					if 'calendar' in dsc_root.find('c01/did/unitdate').attrib:
						component_cal = dsc_root.find('c01/did/unitdate').attrib['calendar']
			else:
				if 'era' in dsc_root.find('c01/did/unittitle/unitdate').attrib:
					component_era = dsc_root.find('c01/did/unittitle/unitdate').attrib['era']
				if 'calendar' in dsc_root.find('c01/did/unittitle/unitdate').attrib:
					component_cal = dsc_root.find('c01/did/unittitle/unitdate').attrib['calendar']
		else:
			if 'era' in dsc_root.find('c/did/unitdate').attrib:
				component_era = dsc_root.find('c/did/unitdate').attrib['era']
			if 'calendar' in dsc_root.find('c/did/unitdate').attrib:
				component_cal = dsc_root.find('c/did/unitdate').attrib['calendar']
	else:
		if 'era' in dsc_root.find('c/did/unittitle/unitdate').attrib:
			component_era = dsc_root.find('c/did/unittitle/unitdate').attrib['era']
		if 'calendar' in dsc_root.find('c/did/unittitle/unitdate').attrib:
			component_cal = dsc_root.find('c/did/unittitle/unitdate').attrib['calendar']
	dsc_root.clear()
	if old_attrib is None:
		pass
	else:
		dsc_root.attrib = old_attrib
	if old_head is None:
		pass
	else:
		dsc_root.append(old_head)
	if "ask_gui" in globals.new_elements:
		wx.CallAfter(pub.sendMessage, "update", msg="Writing Container List...")
	if input_data.find('CollectionSheet/CollectionMap/Component/ComponentName').text:
		if input_data.find('CollectionSheet/CollectionMap/Component/ComponentName').text.lower() == "no series" or  input_data.find('CollectionSheet/CollectionMap/Component/ComponentName').text.lower() == "noseries":
			if number == True:
				c_element = ET.Element('c01')
			else:
				c_element = ET.Element('c')
			from components import no_series
			no_series(c_element, input_data.find('Series1'), version, dsc_root, input_data, old_cmpt, collectionID, component_era, component_cal, old_did)
		else:
			collection_map = input_data.find('CollectionSheet/CollectionMap')
			for level1 in collection_map:
				if level1.find('ComponentLevel').text == '1':
					cmpnt_num = level1.find('ComponentNumber').text
					cmpnt_name = level1.find('ComponentName').text
					for ComponentSheet in input_data:
						if ComponentSheet.find('SeriesNumber') is None:
							pass
						else:
							if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
								cmpnt_info = ComponentSheet 
							elif ComponentSheet.find('SeriesName') is None:
								pass
							else:
								if ComponentSheet.find('SeriesName').text == cmpnt_name:
									cmpnt_info = ComponentSheet
					if number == True:
						c_element = ET.Element('c01')
					else:
						c_element = ET.Element('c')
					dsc_root.append(c_element)
					c_element.set('level', 'series')
					components(c_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
					level1_index = collection_map.getchildren().index(level1)
					for level2 in collection_map:
						level2_index = collection_map.getchildren().index(level2)
						if level2_index > level1_index:
							if level2.find('ComponentLevel').text:
								if int(level2.find('ComponentLevel').text) < 2:
									break
								elif level2.find('ComponentLevel').text == '2':			
									if number == True:
										c2_element = ET.Element('c02')
									else:
										c2_element = ET.Element('c')
									c_element.append(c2_element)
									cmpnt_num = level2.find('ComponentNumber').text
									cmpnt_name = level2.find('ComponentName').text
									for ComponentSheet in input_data:
										if ComponentSheet.find('SeriesNumber') is None:
											pass
										else:
											if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
												cmpnt_info = ComponentSheet 
											elif ComponentSheet.find('SeriesName') is None:
												pass
											else:
												if ComponentSheet.find('SeriesName').text == cmpnt_name:
													cmpnt_info = ComponentSheet
									c2_element.set('level', 'subseries')
									components(c2_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
									for level3 in collection_map:
										level3_index = collection_map.getchildren().index(level3)
										if level3_index > level2_index:
											if level3.find('ComponentLevel').text:
												if int(level3.find('ComponentLevel').text) < 3:
													break
												elif level3.find('ComponentLevel').text == '3':			
													if number == True:
														c3_element = ET.Element('c03')
													else:
														c3_element = ET.Element('c')
													c_element.append(c3_element)
													cmpnt_num = level3.find('ComponentNumber').text
													cmpnt_name = level3.find('ComponentName').text
													for ComponentSheet in input_data:
														if ComponentSheet.find('SeriesNumber') is None:
															pass
														else:
															if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																cmpnt_info = ComponentSheet 
															elif ComponentSheet.find('SeriesName') is None:
																pass
															else:
																if ComponentSheet.find('SeriesName').text == cmpnt_name:
																	cmpnt_info = ComponentSheet
													c3_element.set('level', 'subseries')
													components(c3_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
													for level4 in collection_map:
														level4_index = collection_map.getchildren().index(level4)
														if level4_index > level3_index:
															if level4.find('ComponentLevel').text:
																if int(level4.find('ComponentLevel').text) < 4:
																	break
																elif level4.find('ComponentLevel').text == '4':			
																	if number == True:
																		c4_element = ET.Element('c04')
																	else:
																		c4_element = ET.Element('c')
																	c_element.append(c4_element)
																	cmpnt_num = level4.find('ComponentNumber').text
																	cmpnt_name = level4.find('ComponentName').text
																	for ComponentSheet in input_data:
																		if ComponentSheet.find('SeriesNumber') is None:
																			pass
																		else:
																			if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																				cmpnt_info = ComponentSheet 
																			elif ComponentSheet.find('SeriesName') is None:
																				pass
																			else:
																				if ComponentSheet.find('SeriesName').text == cmpnt_name:
																					cmpnt_info = ComponentSheet
																	c4_element.set('level', 'subseries')
																	components(c4_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
																	for level5 in collection_map:
																		level5_index = collection_map.getchildren().index(level5)
																		if level5_index > level4_index:
																			if level5.find('ComponentLevel').text:
																				if int(level5.find('ComponentLevel').text) < 5:
																					break
																				elif level5.find('ComponentLevel').text == '5':			
																					if number == True:
																						c5_element = ET.Element('c05')
																					else:
																						c5_element = ET.Element('c')
																					c_element.append(c5_element)
																					cmpnt_num = level5.find('ComponentNumber').text
																					cmpnt_name = level5.find('ComponentName').text
																					for ComponentSheet in input_data:
																						if ComponentSheet.find('SeriesNumber') is None:
																							pass
																						else:
																							if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																								cmpnt_info = ComponentSheet 
																							elif ComponentSheet.find('SeriesName') is None:
																								pass
																							else:
																								if ComponentSheet.find('SeriesName').text == cmpnt_name:
																									cmpnt_info = ComponentSheet
																					c5_element.set('level', 'subseries')
																					components(c5_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
																					for level6 in collection_map:
																						level6_index = collection_map.getchildren().index(level6)
																						if level6_index > level5_index:
																							if level6.find('ComponentLevel').text:
																								if int(level6.find('ComponentLevel').text) < 6:
																									break
																								elif level6.find('ComponentLevel').text == '6':			
																									if number == True:
																										c6_element = ET.Element('c06')
																									else:
																										c6_element = ET.Element('c')
																									c_element.append(c6_element)
																									cmpnt_num = level6.find('ComponentNumber').text
																									cmpnt_name = level6.find('ComponentName').text
																									for ComponentSheet in input_data:
																										if ComponentSheet.find('SeriesNumber') is None:
																											pass
																										else:
																											if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																												cmpnt_info = ComponentSheet 
																											elif ComponentSheet.find('SeriesName') is None:
																												pass
																											else:
																												if ComponentSheet.find('SeriesName').text == cmpnt_name:
																													cmpnt_info = ComponentSheet
																									c6_element.set('level', 'subseries')
																									components(c6_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
																									for level7 in collection_map:
																										level7_index = collection_map.getchildren().index(level7)
																										if level7_index > level6_index:
																											if level7.find('ComponentLevel').text:
																												if int(level7.find('ComponentLevel').text) < 7:
																													break
																												elif level7.find('ComponentLevel').text == '7':			
																													if number == True:
																														c7_element = ET.Element('c07')
																													else:
																														c7_element = ET.Element('c')
																													c_element.append(c7_element)
																													cmpnt_num = level7.find('ComponentNumber').text
																													cmpnt_name = level7.find('ComponentName').text
																													for ComponentSheet in input_data:
																														if ComponentSheet.find('SeriesNumber') is None:
																															pass
																														else:
																															if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																																cmpnt_info = ComponentSheet 
																															elif ComponentSheet.find('SeriesName') is None:
																																pass
																															else:
																																if ComponentSheet.find('SeriesName').text == cmpnt_name:
																																	cmpnt_info = ComponentSheet
																													c7_element.set('level', 'subseries')
																													components(c7_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
																													for level8 in collection_map:
																														level8_index = collection_map.getchildren().index(level8)
																														if level8_index > level7_index:
																															if level8.find('ComponentLevel').text:
																																if int(level8.find('ComponentLevel').text) < 8:
																																	break
																																elif level8.find('ComponentLevel').text == '8':			
																																	if number == True:
																																		c8_element = ET.Element('c08')
																																	else:
																																		c8_element = ET.Element('c')
																																	c_element.append(c8_element)
																																	cmpnt_num = level8.find('ComponentNumber').text
																																	cmpnt_name = level8.find('ComponentName').text
																																	for ComponentSheet in input_data:
																																		if ComponentSheet.find('SeriesNumber') is None:
																																			pass
																																		else:
																																			if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																																				cmpnt_info = ComponentSheet 
																																			elif ComponentSheet.find('SeriesName') is None:
																																				pass
																																			else:
																																				if ComponentSheet.find('SeriesName').text == cmpnt_name:
																																					cmpnt_info = ComponentSheet
																																	c8_element.set('level', 'subseries')
																																	components(c8_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
																																	for level9 in collection_map:
																																		level9_index = collection_map.getchildren().index(level9)
																																		if level9_index > level8_index:
																																			if level9.find('ComponentLevel').text:
																																				if int(level9.find('ComponentLevel').text) < 9:
																																					break
																																				elif level9.find('ComponentLevel').text == '9':			
																																					if number == True:
																																						c9_element = ET.Element('c09')
																																					else:
																																						c9_element = ET.Element('c')
																																					c_element.append(c9_element)
																																					cmpnt_num = level9.find('ComponentNumber').text
																																					cmpnt_name = level9.find('ComponentName').text
																																					for ComponentSheet in input_data:
																																						if ComponentSheet.find('SeriesNumber') is None:
																																							pass
																																						else:
																																							if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																																								cmpnt_info = ComponentSheet 
																																							elif ComponentSheet.find('SeriesName') is None:
																																								pass
																																							else:
																																								if ComponentSheet.find('SeriesName').text == cmpnt_name:
																																									cmpnt_info = ComponentSheet
																																					c9_element.set('level', 'subseries')
																																					components(c9_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
																																					for level10 in collection_map:
																																						level10_index = collection_map.getchildren().index(level10)
																																						if level10_index > level9_index:
																																							if level10.find('ComponentLevel').text:
																																								if int(level10.find('ComponentLevel').text) < 10:
																																									break
																																								elif level10.find('ComponentLevel').text == '10':			
																																									if number == True:
																																										c10_element = ET.Element('c10')
																																									else:
																																										c10_element = ET.Element('c')
																																									c_element.append(c10_element)
																																									cmpnt_num = level10.find('ComponentNumber').text
																																									cmpnt_name = level10.find('ComponentName').text
																																									for ComponentSheet in input_data:
																																										if ComponentSheet.find('SeriesNumber') is None:
																																											pass
																																										else:
																																											if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																																												cmpnt_info = ComponentSheet 
																																											elif ComponentSheet.find('SeriesName') is None:
																																												pass
																																											else:
																																												if ComponentSheet.find('SeriesName').text == cmpnt_name:
																																													cmpnt_info = ComponentSheet
																																									c10_element.set('level', 'subseries')
																																									components(c10_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
																																									for level11 in collection_map:
																																										level11_index = collection_map.getchildren().index(level11)
																																										if level11_index > level10_index:
																																											if level11.find('ComponentLevel').text:
																																												if int(level11.find('ComponentLevel').text) < 11:
																																													break
																																												elif level11.find('ComponentLevel').text == '11':			
																																													if number == True:
																																														c11_element = ET.Element('c11')
																																													else:
																																														c11_element = ET.Element('c')
																																													c_element.append(c11_element)
																																													cmpnt_num = level11.find('ComponentNumber').text
																																													cmpnt_name = level11.find('ComponentName').text
																																													for ComponentSheet in input_data:
																																														if ComponentSheet.find('SeriesNumber') is None:
																																															pass
																																														else:
																																															if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																																																cmpnt_info = ComponentSheet 
																																															elif ComponentSheet.find('SeriesName') is None:
																																																pass
																																															else:
																																																if ComponentSheet.find('SeriesName').text == cmpnt_name:
																																																	cmpnt_info = ComponentSheet
																																													c11_element.set('level', 'subseries')
																																													components(c11_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)
																																													for level12 in collection_map:
																																														level12_index = collection_map.getchildren().index(level12)
																																														if level12_index > level11_index:
																																															if level12.find('ComponentLevel').text:
																																																if int(level12.find('ComponentLevel').text) < 12:
																																																	break
																																																elif level12.find('ComponentLevel').text == '12':			
																																																	if number == True:
																																																		c12_element = ET.Element('c12')
																																																	else:
																																																		c12_element = ET.Element('c')
																																																	c_element.append(c12_element)
																																																	cmpnt_num = level12.find('ComponentNumber').text
																																																	cmpnt_name = level12.find('ComponentName').text
																																																	for ComponentSheet in input_data:
																																																		if ComponentSheet.find('SeriesNumber') is None:
																																																			pass
																																																		else:
																																																			if ComponentSheet.find('SeriesNumber').text == cmpnt_name:
																																																				cmpnt_info = ComponentSheet 
																																																			elif ComponentSheet.find('SeriesName') is None:
																																																				pass
																																																			else:
																																																				if ComponentSheet.find('SeriesName').text == cmpnt_name:
																																																					cmpnt_info = ComponentSheet
																																																	c12_element.set('level', 'subseries')
																																																	components(c12_element, cmpnt_info, version, arr_head, sc_head, old_physdesc, old_physdescstructured, component_era, component_cal, old_did, collectionID, input_data, old_cmpt, old_ser)