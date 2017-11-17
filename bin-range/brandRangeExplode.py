import csv
import string
import re

file=open('excplodedBins.sql','w')

with open('bins-to-explode.csv', 'rb') as f:
	reader = csv.reader(f, delimiter=' ')
	brand = "";
	for row in reader:
		if not row:
			continue;
		if re.search('[\-]', row[0]):
			continue;
		if re.search('[a-zA-Z]', row[0]):
			brand = row[0];
			continue;
		rangeStart = long(row[0]);
		rangeEnd = long(row[1]);
		#print rangeStart;
		#print rangeEnd;
		for x in range(rangeStart, rangeEnd+1):
			insert = "insert into dbo.IssuerIdentificationNumber (pattern, brand_id) select '" + str(x) + "%', id  from Brand where label = '" + brand + "'\n";
			file.write(insert);

file.close();
