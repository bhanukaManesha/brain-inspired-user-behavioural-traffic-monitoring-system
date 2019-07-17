
import importlib
import sys
import csv
import datetime
import os

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.frameworks.opf.prediction_metrics_manager import MetricsManager

import nupic_output

DESCRIPTION = ('Anomaly Detection for Network Activity')
SYSTEM_NAME = "network_anomaly"
DATA_DIR = "."
INPUT_FILE = "network.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
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

def initalizeModels():
  MODELS = []

  for index in range(len(MODEL_NAMES)):
    model = ModelFactory.create(getModelParamsFromName(MODEL_NAMES[index]))
    model.enableInference({"predictedField": MODEL_NAMES[index]})
    MODELS.append(model)
  return MODELS

def getModelParamsFromName(modelName):
    importName = "MODELS_PARAMS."+ modelName +"_model_params" 
    print("Importing model params from " + modelName)
    try:
      importedModelParams = importlib.import_module(importName).MODEL_PARAMS
    except ImportError:
      raise Exception("No model params exist for '%s'. Run swarm first!"
                      % importName)
    return importedModelParams

def runIoThroughNupic(inputData, MODELS, systemName):
  ANOMALY_LIKELIHOOD = [0.0 for i in range(len(MODEL_NAMES))]
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)

  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  output = nupic_output.NuPICFileOutput(systemName)
  counter = 0
  metricsManager = [0 for i in range(len(MODELS))]

  for row in csvReader:
    counter += 1
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    for model_index in range(len(MODELS)):
		data = float(row[model_index+1])
      		inference_type = MODEL_NAMES[model_index]

	      	result = MODELS[model_index].run({
          		"timestamp": timestamp,
          		inference_type : data
      			})

      		if counter % 20 == 0:
			      print(str(counter) + ":" + inference_type)

	      	result = shifter.shift(result)
      
	      	prediction = result.inferences["multiStepBestPredictions"][1]
      		anomalyScore = result.inferences["anomalyScore"]
      		anomalyLikelihood = output.get_anomaly_likelihood(timestamp, data, prediction ,anomalyScore)
			
      		ANOMALY_LIKELIHOOD[model_index] = anomalyLikelihood
  
    output.write(timestamp,ANOMALY_LIKELIHOOD)

  inputFile.close()
  output.close()

def loadModels(models,model_names):
  #m = [0 for i in range(len(model_names))]
  for index in range(len(model_names)):
    print("Loading " + model_names[index] + " ...")
    path = os.path.join(os.getcwd(), "saved models/" + model_names[index] + "/")
    models[index].readFromCheckpoint(path)
    #m[index] = ModelFactory.loadFromCheckpoint(path)
    models[index].enableLearning()
    print(model_names[index] + "model successfully loaded")
  return models

def saveModels(models,model_names):
  for i in range(len(models)):
    print("Saving " + model_names[i] + " ...")
    path = os.path.join(os.getcwd(), "saved models/" + model_names[i]+ "/")
    models[i].disableLearning()
    models[i].writeToCheckpoint(path)
    print(model_names[i] + " model saved")


def runModel(systemName,load=True):
  print "Creating models for %s..." % systemName
  MODELS = initalizeModels()
  if load:
      MODELS = loadModels(MODELS,MODEL_NAMES)
  inputData = "%s/csv/%s" % (DATA_DIR, INPUT_FILE)
  runIoThroughNupic(inputData, MODELS, systemName)
  saveModels(MODELS,MODEL_NAMES)


# if __name__ == "__main__":
#   print DESCRIPTION
#   runModel(SYSTEM_NAME)
