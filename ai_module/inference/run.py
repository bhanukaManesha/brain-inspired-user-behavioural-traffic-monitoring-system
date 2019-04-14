
import importlib
import sys
import csv
import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.frameworks.opf.prediction_metrics_manager import MetricsManager

import nupic_output

from model_params import model_params


DESCRIPTION = ('Anomaly Detection')
SYSTEM_NAME = "network_anomaly"
DATA_DIR = "."
INPUT_FILE = "network.csv"

timestamp,total,total_tcp,total_http,total_udp,size,size_tcp,size_http,size_udp

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

#  MODEL_PARAMS_DIR = "./model_params"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_METRIC_SPECS = (
    MetricSpec(field='total', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
    MetricSpec(field='total', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
    MetricSpec(field='total', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
    MetricSpec(field='total', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
)

def initalizeModels():
  MODELS = []

  for name in MODEL_NAMES:
    model = ModelFactory.create(model_params.MODEL_PARAMS)
    model.enableInference({"predictedField": name})
    MODELS.append(model)
  
  return MODELS



# def getModelParamsFromName(gymName):
#   importName = "model_params.%s_model_params" % (
#     gymName.replace(" ", "_").replace("-", "_")
#   )
#   print "Importing model params from %s" % importName
#   try:
#     importedModelParams = importlib.import_module(importName).MODEL_PARAMS
#   except ImportError:
#     raise Exception("No model params exist for '%s'. Run swarm first!"
#                     % gymName)
#   return importedModelParams



def runIoThroughNupic(inputData, MODELS, systemName):
  ANOMALY_LIKELIHOOD = [0.0 for i in range(len(MODEL_NAMES))]


  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()

  output = nupic_output.NuPICFileOutput(systemName,MODEL_NAMES)

  

  counter = 0
  for row in csvReader:
    counter += 1
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)

    for model_index in range(len(MODELS)):
      metricsManager = MetricsManager(_METRIC_SPECS, MODELS[model_index].getFieldInfo(),
                                  MODELS[model_index].getInferenceType())

      data = float(row[model_index+1])
    
      result = MODELS[model_index].run({
          "timestamp": timestamp,
          MODEL_NAMES[model_index]: data
      })

      result.metrics = metricsManager.update(result)

      if counter % 20 == 0:
      print "Read %i lines..." % counter
      print ("After %i records, 1-step altMAPE=%f" % (counter,
              result.metrics["multiStepBestPredictions:multiStep:"
                             "errorMetric='altMAPE':steps=1:window=1000:"
                             "field=total"]))

      result = shifter.shift(result)
      
      prediction = result.inferences["multiStepBestPredictions"][1]
      anomalyScore = result.inferences["anomalyScore"]
      anomalyLikelihood = output.get_anomaly_likelihood(timestamp, data, prediction , anomalyScore)
      
      ANOMALY_LIKELIHOOD[model_index] = anomalyLikelihood
  
  output.write(timestamp,ANOMALY_LIKELIHOOD)


  inputFile.close()
  output.close()


def runModel(systemName):
  print "Creating models for %s..." % systemName
  MODELS = initalizeModels()
  inputData = "%s/csv/%s" % (DATA_DIR, INPUT_FILE)
  runIoThroughNupic(inputData, MODELS, systemName)

  # model.save()



if __name__ == "__main__":
  print DESCRIPTION
  args = sys.argv[1:]
  runModel(SYSTEM_NAME)
