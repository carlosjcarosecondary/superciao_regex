import csv
import re
import os


##############################################################################
#	1. Importing CSV file into a list
##############################################################################
def open_with_csv(file_name, d='\t'):
	data =[]
	with open(file_name, encoding = 'utf-8') as raw_data:
		reader = csv.reader(raw_data, delimiter = d)
		for line in reader:
			string_row = ''.join(line)
			data.append(string_row)
	return data

##############################################################################
#	4. Exporting RegEx outcome as a CSV
##############################################################################

def writing_csv(regex_list, outfilename='output.csv'):
	with open(outfilename, 'wb') as f:
		f.write(u'\ufeff'.encode('utf8')) # BOM
	with open(outfilename, 'a', encoding = 'utf-8') as f:
		writer = csv.writer(f, delimiter=';')
		writer.writerows(regex_list)

##############################################################################
#	2. Exporting file with UUID
##############################################################################

def exporting_index(data):
	index = []
	counter = 0
	for a in data:
		counter += 1
		temp_str = "SC_" + str(counter).zfill(6)
		index.append(str(temp_str))

	columns = zip(index, data)

	writing_csv(columns, 'source.csv')
	return index


##############################################################################
#	3. Building the RegEx
##############################################################################

#regex_test = re.findall(r'\b(Werkzeugk|N1|Note|Note 1|Zahlung|invest)\b', row, re.IGNORECASE)

def regex_filter(data, uuid):
	regex_clause = []
	regex_index = []

	counter = 0

	for row in data:
		regex_test = re.findall(r'(\b|\n)(\w{0,}bedarf\w{0,})(\b|\n)', row, re.IGNORECASE)
		if regex_test:
			regex_test = re.findall(r'(\b|\n)(EOP|End.of.Production|SOP|Start.of.production|Serie|Ersatzteil|OT|Originalteil\w{0,})(\b|\n)', row, re.IGNORECASE)
			if regex_test:
				regex_index.append(uuid[counter])
				regex_clause.append(row)
		counter += 1

	print(len(regex_clause))
	return zip(regex_index, regex_clause)


##############################################################################
#	Main
##############################################################################
column_clause = open_with_csv('Neue Daten Superciao 2013.csv')
column_uuid = exporting_index(column_clause)
regex_output = regex_filter(column_clause, column_uuid)
regex_csv = writing_csv(regex_output)