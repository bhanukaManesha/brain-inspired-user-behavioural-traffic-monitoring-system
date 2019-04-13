import csv
import datetime
import sys
import csv

csv.field_size_limit(sys.maxsize)

dataset = [];

readcsvfile = open('csv/test.csv')
writecsv = open('csv/network.csv','w')

readCSV = csv.reader(readcsvfile, delimiter=',')
writeCSV = csv.writer(writecsv)

header = readCSV.next()
writeCSV.writerow(header[0:9])
<<<<<<< Updated upstream:ai_module/preprocessing.py
writeCSV.writerow(["datetime","float","float","float","float","float","float","float","float"])
writeCSV.writerow(["T","","","","","","","",""])

for row in readCSV:

    for i in range(0,9):
        row[i] = float(row[i])

    dt = datetime.datetime.fromtimestamp(row[0])
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')

    updated_row = row
    updated_row[0] = dt
    final_output = updated_row[0:9]
    writeCSV.writerow(final_output)

def filter(astr):
    return astr.replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
