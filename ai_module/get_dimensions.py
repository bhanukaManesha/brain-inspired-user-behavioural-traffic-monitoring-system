import csv
import datetime
import sys
import csv

def filter_str(astr):
    return astr.replace("[","").replace("]","").replace("\'","").replace(" ","").split(",")


csv.field_size_limit(sys.maxsize)

dataset = [];

readcsvfile = open('test.csv')
writecsv = open('dimensions.csv','w')

readCSV = csv.reader(readcsvfile, delimiter=',')
writeCSV = csv.writer(writecsv)

header = readCSV.next()
writeCSV.writerow(header)

for row in readCSV:
    print(row[11])
    outstr = []
    for i in range(25):
        alist = filter_str(row[i])
        outstr.append(len(alist))

    break
    writeCSV.writerow(outstr)
