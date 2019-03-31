import csv
import datetime
import sys
import csv

csv.field_size_limit(sys.maxsize)

dataset = [];

readcsvfile = open('test.csv')
writecsv = open('updated_test.csv','w')

readCSV = csv.reader(readcsvfile, delimiter=',')
writeCSV = csv.writer(writecsv)

header = readCSV.next()
writeCSV.writerow(header[0:9])

for row in readCSV:
    timestamp = float(row[0])
    dt = datetime.datetime.fromtimestamp(timestamp).isoformat()
    updated_row = row
    updated_row[0] = dt
    final_output = updated_row[0:9];
    writeCSV.writerow(final_output)

def filter(astr):
    return astr.replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
