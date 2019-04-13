import nupic_output
import csv
import datetime
# from nupic.data.inference_shifter import InferenceShifter

GYM_NAME = "network"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


inputFile = open("network_out.csv", "rb")
csvReader = csv.reader(inputFile)
# skip header rows
csvReader.next()
csvReader.next()
csvReader.next()

output = nupic_output.NuPICPlotOutput([GYM_NAME])

# metricsManager = MetricsManager(_METRIC_SPECS, model.getFieldInfo(),
#                                 model.getInferenceType())

counter = 0
for row in csvReader:
  counter += 1

  timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
  total = float(row[1])
  prediction = float(row[2])
  # total_tcp = int(row[2])
  # total_http = int(row[3])
  # total_udp = int(row[4])
  # size = int(row[5])
  # size_tcp = int(row[6])
  # size_http = int(row[7])
  # size_udp = int(row[8])
  #
  # result = model.run({
  #   "timestamp": timestamp,
  #   "total": total,
  #   "total_tcp" : total_tcp,
  #   "total_http" : total_http,
  #   "total_udp" : total_udp,
  #   "size" : size,
  #   "size_tcp" : size_tcp,
  #   "size_http" : size_http,
  #   "size_udp" : size_udp
  # })

  output.write([timestamp], [total], [prediction])
  output.refreshGUI()

inputFile.close()
output.close()
