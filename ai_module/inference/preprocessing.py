import csv
import datetime
import sys
import json


def json2csv(json_data,file_name,new_file=False):
    if new_file:
        f = csv.writer(open(file_name, "w+"))
        f.writerow(["datetime","total","total_tcp","total_http","total_udp","size","size_tcp","size_http","size_udp"])
    else:
        f = csv.writer(open(file_name, "a"))

    for line in json_data:
        f.writerow([
            line["timestamp"],
            line["total"],
            line["total_tcp"],
            line["total_http"],
            line["total_udp"],
            line["size"],
            line["size_tcp"],
            line["size_http"],
            line["size_udp"]
            ])

def csv2json():
    csvfile = open('file.csv', 'r')
    jsonfile = open('file.json', 'w')

    fieldnames = ("datetime","total","total_tcp","total_http","total_udp","size","size_tcp","size_http","size_udp")
    reader = csv.DictReader( csvfile, fieldnames)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')


def removeTimeStamp(input_filename,output_filename):
    csv.field_size_limit(sys.maxsize)
    readcsvfile = open(input_filename)
    writecsv = open(output_filename,'w')

    readCSV = csv.reader(readcsvfile, delimiter=',')
    writeCSV = csv.writer(writecsv)

    header = next(readCSV)
    writeCSV.writerow(header[0:9])
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

