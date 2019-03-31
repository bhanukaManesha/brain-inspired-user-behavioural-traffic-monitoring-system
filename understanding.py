
import csv
import datetime
import sys
import csv


csv.field_size_limit(sys.maxsize)

readcsvfile = open('updated_test.csv')
readCSV = csv.reader(readcsvfile, delimiter=',')
header = readCSV.next()
print(header)

# for row in readCSV:
#     print(row[22][0])
#     x = row[22].replace("[","")
#     x = x.replace("]","")
#     x = x.replace(" ","")
#     x = x.replace("'","")
#     x = x.split(",")
#     print(len(x))
#
#     break
#
# for item in x:
#     print(item)





def filter(astr):
    return astr.replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
