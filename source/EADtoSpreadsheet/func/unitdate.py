#Module for <unitdate> both within the collection-level <did> and within lower components
def unitdate(did_root, CSheet, level, version):
	if level == "collection":
		# collection-level unitdate
		Inclusive = "DateInclusive"
		InclusiveNormal = "DateInclusiveNormal"
		Bulk = "DateBulk"
		BulkNormal = "DateBulkNormal"
	elif level == "series":
		# series-level unitdate
		Inclusive = "SeriesDate"
		InclusiveNormal = "SeriesDateNormal"
		Bulk = "SeriesBulkDate"
		BulkNormal = "SeriesBulkDateNormal"
	
	if version == "ead2002":
		if did_root.find('unittitle/unitdate') is None:
			if did_root.find('unitdate') is None:
				date_root = did_root
			else:
				date_root = did_root
		else:
			date_root = did_root.find('unittitle')
		if date_root.find("unitdate[@type='bulk']") is None:
			if date_root.find("unitdate[@type='inclusive']") is None:
				if date_root.find("unitdate") is None:
					pass
				else:
					CSheet.find(Inclusive).text = date_root.find('unitdate').text
					if 'normal' in date_root.find('unitdate').attrib:
						CSheet.find(InclusiveNormal).text = date_root.find('unitdate').attrib['normal']
			else:
				CSheet.find(Inclusive).text = date_root.find("unitdate[@type='inclusive']").text
				if 'normal' in date_root.find("unitdate[@type='inclusive']").attrib:
					CSheet.find(InclusiveNormal).text = date_root.find("unitdate[@type='inclusive']").attrib['normal']
		else:
			CSheet.find(Bulk).text = date_root.find("unitdate[@type='bulk']").text
			if 'normal' in date_root.find("unitdate[@type='bulk']").attrib:
					CSheet.find(BulkNormal).text = date_root.find("unitdate[@type='bulk']").attrib['normal']
			if date_root.find("unitdate[@type='inclusive']") is None:
				pass
			else:
				CSheet.find(Inclusive).text = date_root.find("unitdate[@type='inclusive']").text
				if 'normal' in date_root.find("unitdate[@type='inclusive']").attrib:
					CSheet.find(InclusiveNormal).text = date_root.find("unitdate[@type='inclusive']").attrib['normal']
	else:
		#EAD3
		if did_root.find('unitdatestructured') is None:
			if did_root.find('unitdate') is None:
				pass
			else:
				if did_root.find("unitdate[@type='bulk']") is None:
					if did_root.find("unitdate[@type='inclusive']") is None:
						CSheet.find(Inclusive).text = did_root.find('unitdate').text
						if 'normal' in did_root.find('unitdate').attrib:
							CSheet.find(InclusiveNormal).text = did_root.find('unitdate').attrib['normal']
					else:
						CSheet.find(Inclusive).text = did_root.find("unitdate[@type='inclusive']").text
						if 'normal' in did_root.find("unitdate[@type='inclusive']").attrib:
							CSheet.find(InclusiveNormal).text = did_root.find("unitdate[@type='inclusive']").attrib['normal']
				else:
					CSheet.find(Bulk).text = did_root.find("unitdate[@type='bulk']").text
					if 'normal' in did_root.find("unitdate[@type='bulk']").attrib:
							CSheet.find(BulkNormal).text = did_root.find("unitdate[@type='bulk']").attrib['normal']
					if did_root.find("unitdate[@type='inclusive']") is None:
						pass
					else:
						CSheet.find(Inclusive).text = did_root.find("unitdate[@type='inclusive']").text
						if 'normal' in did_root.find("unitdate[@type='inclusive']").attrib:
							CSheet.find(InclusiveNormal).text = did_root.find("unitdate[@type='inclusive']").attrib['normal']
		else:
			#unitdatestructured
			if did_root.find("unitdatestructured[@unitdatetype='bulk']") is None:
				if did_root.find("unitdatestructured[@unitdatetype='inclusive']") is None:
					if did_root.find("unitdatestructured/datesingle") is None:
						if did_root.find("unitdatestructured/daterange") is None:
							if did_root.find("unitdatestructured/dateset") is None:
								pass
							else:
								for dateset in did_root.find("unitdatestructured/dateset"):
									if dateset.tag == "datesingle":
										if CSheet.find(Inclusive).text:
											CSheet.find(Inclusive).text = CSheet.find(Inclusive).text + ", " + dateset.find("datesingle").text
											if "standarddate" in dateset.find("datesingle").attrib:
												CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("datesingle").attrib['standarddate']
										else:
											CSheet.find(Inclusive).text = dateset.find("datesingle").text
											if "standarddate" in dateset.find("datesingle").attrib:
												CSheet.find(InclusiveNormal).text = dateset.find("datesingle").attrib['standarddate']
									elif dateset.tag == "daterange":
										if CSheet.find(Inclusive).text:
											CSheet.find(Inclusive).text = CSheet.find(Inclusive).text + ", " + dateset.find("daterange/fromdate").text + "-" + dateset.find("daterange/todate").text
											if "standarddate" in dateset.find("daterange/fromdate").attrib:
												if "standarddate" in dateset.find("daterange/todate").attrib:
													CSheet.find(InclusiveNormal).text = dateset.find("daterange/fromdate").attrib['standarddate'] + "/" + dateset.find("daterange/todate").attrib['standarddate']
												else:
													CSheet.find(InclusiveNormal).text = dateset.find("daterange/fromdate").attrib['standarddate']
										else:
											CSheet.find(Inclusive).text = dateset.find("daterange/fromdate").text + "-" + dateset.find("daterange/todate").text
											if "standarddate" in dateset.find("daterange/fromdate").attrib:
												if "standarddate" in dateset.find("daterange/todate").attrib:
													CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("daterange/fromdate").attrib['standarddate'] + "/" + dateset.find("daterange/todate").attrib['standarddate']
												else:
													CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("daterange/fromdate").attrib['standarddate']
						else:
							CSheet.find(Inclusive).text = did_root.find("unitdatestructured/daterange/fromdate").text + "-" + did_root.find("unitdatestructured/daterange/todate").text
							if "standarddate" in did_root.find("unitdatestructured/daterange/fromdate").attrib:
								if "standarddate" in did_root.find("unitdatestructured/daterange/todate").attrib:
									CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured/daterange/fromdate").attrib['standarddate'] + "/" + did_root.find("unitdatestructured/daterange/todate").attrib['standarddate']
								else:
									CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured/daterange/fromdate").attrib['standarddate']
					else:
						CSheet.find(Inclusive).text = did_root.find("unitdatestructured/datesingle").text
						if "standarddate" in did_root.find("unitdatestructured/datesingle").attrib:
							CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured/datesingle").attrib['standarddate']
				else:
					if did_root.find("unitdatestructured[@unitdatetype='inclusive']/datesingle") is None:
						if did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange") is None:
							if did_root.find("unitdatestructured[@unitdatetype='inclusive']/dateset") is None:
								pass
							else:
								for dateset in did_root.find("unitdatestructured[@unitdatetype='inclusive']/dateset"):
									if dateset.tag == "datesingle":
										if CSheet.find(Inclusive).text:
											CSheet.find(Inclusive).text = CSheet.find(Inclusive).text + ", " + dateset.find("datesingle").text
											if "standarddate" in dateset.find("datesingle").attrib:
												CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("datesingle").attrib['standarddate']
										else:
											CSheet.find(Inclusive).text = dateset.find("datesingle").text
											if "standarddate" in dateset.find("datesingle").attrib:
												CSheet.find(InclusiveNormal).text = dateset.find("datesingle").attrib['standarddate']
									elif dateset.tag == "daterange":
										if CSheet.find(Inclusive).text:
											CSheet.find(Inclusive).text = CSheet.find(Inclusive).text + ", " + dateset.find("daterange/fromdate").text + "-" + dateset.find("daterange/todate").text
											if "standarddate" in dateset.find("daterange/fromdate").attrib:
												if "standarddate" in dateset.find("daterange/todate").attrib:
													CSheet.find(InclusiveNormal).text = dateset.find("daterange/fromdate").attrib['standarddate'] + "/" + dateset.find("daterange/todate").attrib['standarddate']
												else:
													CSheet.find(InclusiveNormal).text = dateset.find("daterange/fromdate").attrib['standarddate']
										else:
											CSheet.find(Inclusive).text = dateset.find("daterange/fromdate").text + "-" + dateset.find("daterange/todate").text
											if "standarddate" in dateset.find("daterange/fromdate").attrib:
												if "standarddate" in dateset.find("daterange/todate").attrib:
													CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("daterange/fromdate").attrib['standarddate'] + "/" + dateset.find("daterange/todate").attrib['standarddate']
												else:
													CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("daterange/fromdate").attrib['standarddate']
						else:
							CSheet.find(Inclusive).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/fromdate").text + "-" + did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/todate").text
							if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/fromdate").attrib:
								if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/todate").attrib:
									CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/fromdate").attrib['standarddate'] + "/" + did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/todate").attrib['standarddate']
								else:
									CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/fromdate").attrib['standarddate']
					else:
						CSheet.find(Inclusive).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/datesingle").text
						if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='inclusive']/datesingle").attrib:
							CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/datesingle").attrib['standarddate']
			else:
				#bulk unitdatestructured
				if did_root.find("unitdatestructured[@unitdatetype='bulk']/datesingle") is None:
					if did_root.find("unitdatestructured[@unitdatetype='bulk']/daterange") is None:
						if did_root.find("unitdatestructured[@unitdatetype='bulk']/dateset") is None:
							pass
						else:
							for dateset in did_root.find("unitdatestructured[@unitdatetype='bulk']/dateset"):
								if dateset.tag == "datesingle":
									if CSheet.find(Bulk).text:
										CSheet.find(Bulk).text = CSheet.find(Bulk).text + ", " + dateset.find("datesingle").text
										if "standarddate" in dateset.find("datesingle").attrib:
											CSheet.find(BulkNormal).text = CSheet.find(BulkNormal).text + ", " + dateset.find("datesingle").attrib['standarddate']
									else:
										CSheet.find(Bulk).text = dateset.find("datesingle").text
										if "standarddate" in dateset.find("datesingle").attrib:
											CSheet.find(BulkNormal).text = dateset.find("datesingle").attrib['standarddate']
								elif dateset.tag == "daterange":
									if CSheet.find(Bulk).text:
										CSheet.find(Bulk).text = CSheet.find(Bulk).text + ", " + dateset.find("daterange/fromdate").text + "-" + dateset.find("daterange/todate").text
										if "standarddate" in dateset.find("daterange/fromdate").attrib:
											if "standarddate" in dateset.find("daterange/todate").attrib:
												CSheet.find(BulkNormal).text = dateset.find("daterange/fromdate").attrib['standarddate'] + "/" + dateset.find("daterange/todate").attrib['standarddate']
											else:
												CSheet.find(BulkNormal).text = dateset.find("daterange/fromdate").attrib['standarddate']
									else:
										CSheet.find(Bulk).text = dateset.find("daterange/fromdate").text + "-" + dateset.find("daterange/todate").text
										if "standarddate" in dateset.find("daterange/fromdate").attrib:
											if "standarddate" in dateset.find("daterange/todate").attrib:
												CSheet.find(BulkNormal).text = CSheet.find(BulkNormal).text + ", " + dateset.find("daterange/fromdate").attrib['standarddate'] + "/" + dateset.find("daterange/todate").attrib['standarddate']
											else:
												CSheet.find(BulkNormal).text = CSheet.find(BulkNormal).text + ", " + dateset.find("daterange/fromdate").attrib['standarddate']
					else:
						CSheet.find(Bulk).text = did_root.find("unitdatestructured[@unitdatetype='bulk']/daterange/fromdate").text + "-" + did_root.find("unitdatestructured[@unitdatetype='bulk']/daterange/todate").text
						if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='bulk']/daterange/fromdate").attrib:
							if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='bulk']/daterange/todate").attrib:
								CSheet.find(BulkNormal).text = did_root.find("unitdatestructured[@unitdatetype='bulk']/daterange/fromdate").attrib['standarddate'] + "/" + did_root.find("unitdatestructured[@unitdatetype='bulk']/daterange/todate").attrib['standarddate']
							else:
								CSheet.find(BulkNormal).text = did_root.find("unitdatestructured[@unitdatetype='bulk']/daterange/fromdate").attrib['standarddate']
				else:
					CSheet.find(Bulk).text = did_root.find("unitdatestructured[@unitdatetype='bulk']/datesingle").text
					if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='bulk']/datesingle").attrib:
						CSheet.find(BulkNormal).text = did_root.find("unitdatestructured[@unitdatetype='bulk']/datesingle").attrib['standarddate']				
				if did_root.find("unitdatestructured[@unitdatetype='inclusive']") is None:
					pass
				else:
					if did_root.find("unitdatestructured[@unitdatetype='inclusive']/datesingle") is None:
						if did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange") is None:
							if did_root.find("unitdatestructured[@unitdatetype='inclusive']/dateset") is None:
								pass
							else:
								for dateset in did_root.find("unitdatestructured[@unitdatetype='inclusive']/dateset"):
									if dateset.tag == "datesingle":
										if CSheet.find(Inclusive).text:
											CSheet.find(Inclusive).text = CSheet.find(Inclusive).text + ", " + dateset.find("datesingle").text
											if "standarddate" in dateset.find("datesingle").attrib:
												CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("datesingle").attrib['standarddate']
										else:
											CSheet.find(Inclusive).text = dateset.find("datesingle").text
											if "standarddate" in dateset.find("datesingle").attrib:
												CSheet.find(InclusiveNormal).text = dateset.find("datesingle").attrib['standarddate']
									elif dateset.tag == "daterange":
										if CSheet.find(Inclusive).text:
											CSheet.find(Inclusive).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("daterange/fromdate").text + "-" + dateset.find("daterange/todate").text
											if "standarddate" in dateset.find("daterange/fromdate").attrib:
												if "standarddate" in dateset.find("daterange/todate").attrib:
													CSheet.find(InclusiveNormal).text = dateset.find("daterange/fromdate").attrib['standarddate'] + "/" + dateset.find("daterange/todate").attrib['standarddate']
												else:
													CSheet.find(InclusiveNormal).text = dateset.find("daterange/fromdate").attrib['standarddate']
										else:
											CSheet.find(Inclusive).text = dateset.find("daterange/fromdate").text + "-" + dateset.find("daterange/todate").text
											if "standarddate" in dateset.find("daterange/fromdate").attrib:
												if "standarddate" in dateset.find("daterange/todate").attrib:
													CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("daterange/fromdate").attrib['standarddate'] + "/" + dateset.find("daterange/todate").attrib['standarddate']
												else:
													CSheet.find(InclusiveNormal).text = CSheet.find(InclusiveNormal).text + ", " + dateset.find("daterange/fromdate").attrib['standarddate']
						else:
							CSheet.find(Inclusive).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/fromdate").text + "-" + did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/todate").text
							if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/fromdate").attrib:
								if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/todate").attrib:
									CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/fromdate").attrib['standarddate'] + "/" + did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/todate").attrib['standarddate']
								else:
									CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/daterange/fromdate").attrib['standarddate']
					else:
						CSheet.find(Inclusive).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/datesingle").text
						if "standarddate" in did_root.find("unitdatestructured[@unitdatetype='inclusive']/datesingle").attrib:
							CSheet.find(InclusiveNormal).text = did_root.find("unitdatestructured[@unitdatetype='inclusive']/datesingle").attrib['standarddate']