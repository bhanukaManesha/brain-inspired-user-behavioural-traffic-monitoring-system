import nupic_output
import csv
import datetime
# from nupic.data.inference_shifter import InferenceShifter

GYM_NAME = "network"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


inputFile = open("network_out.csv", "r")
csvReader = csv.reader(inputFile)
# skip header rows
next(csvReader)
next(csvReader)
next(csvReader)

output = nupic_output.NuPICPlotOutput([GYM_NAME])

counter = 0
for row in csvReader:
  counter += 1

  timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
  total = row[1]
  prediction = row[2]
  output.write([timestamp], [total], [prediction])
  output.refreshGUI()

inputFile.close()
output.close()
