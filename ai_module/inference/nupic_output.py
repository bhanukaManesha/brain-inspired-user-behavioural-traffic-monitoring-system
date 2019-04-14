"""
Provides two classes with the same signature for writing data out of NuPIC
models.
(This is a component of the One Hot Gym Anomaly Tutorial.)
"""
import csv
from collections import deque
from abc import ABCMeta, abstractmethod
from nupic.algorithms import anomaly_likelihood
# Try to import matplotlib, but we don't have to.
try:
  import matplotlib
  matplotlib.use('TKAgg')
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
  from matplotlib.dates import date2num, DateFormatter
except ImportError:
  pass


MODEL_NAMES = [
	"total",
	"total_tcp",
	"total_http",
	"total_udp",
	"size",
	"size_tcp",
	"size_http",
	"size_udp"
]

class NuPICOutput(object):

  __metaclass__ = ABCMeta


  def __init__(self, name):
    self.name = name
    self.anomalyLikelihoodHelper = anomaly_likelihood.AnomalyLikelihood()


  @abstractmethod
  def write(self, timestamp, value, predicted, anomalyScore):
    pass


  @abstractmethod
  def close(self):
    pass




class NuPICFileOutput(NuPICOutput):


  def __init__(self, *args, **kwargs):
    super(NuPICFileOutput, self).__init__(*args, **kwargs)
    self.outputFiles = []
    self.outputWriters = []
    self.lineCount = 0
        

    headerRow = ['timestamp']
    for item in MODEL_NAMES:
        headerRow.append(item)

    outputFileName = "%s_out.csv" % self.name
    print "Preparing to output %s data to %s" % (self.name, outputFileName)
    self.outputFile = open(outputFileName, "w")
    self.outputWriter = csv.writer(self.outputFile)
    self.outputWriter.writerow(headerRow)


  def get_anomaly_likelihood(self,timestamp, value, predicted, anomalyScore):
    if timestamp is not None:
      	anomalyLikelihood = self.anomalyLikelihoodHelper.anomalyProbability(value, anomalyScore, timestamp)
        return anomalyLikelihood


  def write(self, timestamp, anomaly_likelihood):
      outputRow = [timestamp]
      for item in anomaly_likelihood:
        outputRow.append(item)

      self.outputWriter.writerow(outputRow)
      self.lineCount += 1

  def close(self):
    self.outputFile.close()
    print "Done. Wrote %i data lines to %s." % (self.lineCount, self.name)

NuPICOutput.register(NuPICFileOutput)
