import csv
import datetime
import sys
import csv

csv.field_size_limit(sys.maxsize)

dataset = [];

readcsvfile = open('csv/test2.csv')
writecsv = open('csv/network.csv','w')

readCSV = csv.reader(readcsvfile, delimiter=',')
writeCSV = csv.writer(writecsv)

header = readCSV.next()
writeCSV.writerow(header[0:9])
writeCSV.writerow(["datetime","int","int","int","int","int","int","int","int"])
writeCSV.writerow(["T","","","","","","","",""])


for row in readCSV:
    timestamp = float(row[0])
    dt = datetime.datetime.fromtimestamp(timestamp)
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    updated_row = row
    updated_row[0] = dt
    final_output = updated_row[0:9];
    writeCSV.writerow(final_output)

def filter(astr):
    return astr.replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
