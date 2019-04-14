
import importlib
import sys
import csv
import datetime

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
          metricsManager[model_index] = MetricsManager(_METRIC_SPECS, MODELS[model_index].getFieldInfo(),
                                  MODELS[model_index].getInferenceType())

          data = float(row[model_index+1])
      		inference_type = MODEL_NAMES[model_index]

	      	result = MODELS[model_index].run({
          		"timestamp": timestamp,
          		inference_type : data
      			})

      		result.metrics = metricsManager[model_index].update(result)

      		if counter % 20 == 0:
		      	print ("%s: After %i records, 1-step altMAPE=%f" % (inference_type,counter, 
                  result.metrics["multiStepBestPredictions:multiStep:""errorMetric='altMAPE':steps=1:window=1000:""field=total"]))

	      	result = shifter.shift(result)
      
	      	prediction = result.inferences["multiStepBestPredictions"][1]
      		anomalyScore = result.inferences["anomalyScore"]
      		anomalyLikelihood = output.get_anomaly_likelihood(timestamp, data, prediction ,anomalyScore)
			
      		ANOMALY_LIKELIHOOD[model_index] = anomalyLikelihood
  
      	output.write(timestamp,ANOMALY_LIKELIHOOD)

  inputFile.close()
  output.close()

def loadModels(model_names):
  m = [o for i in range(len(model_names))]
  for index in range(model_names):
    path = os.path.join(os.getcwd(), model_names(name))
    m[index] = ModelFactory.loadFromCheckpoint(path)
  return m

def saveModels(models,model_names):
  for i in range(len(models)):
    path = os.path.join(os.getcwd(), model_names(name))
    models[i].save(path)


def runModel(systemName,intialize = False):
  print "Creating models for %s..." % systemName
  if intialize :
    MODELS = initalizeModels()
  else:
    MODELS = loadModels(MODEL_NAMES)  
  inputData = "%s/csv/%s" % (DATA_DIR, INPUT_FILE)
  runIoThroughNupic(inputData, MODELS, systemName)
  saveModels(MODELS,MODEL_NAMES)


if __name__ == "__main__":
  print DESCRIPTION
  runModel(SYSTEM_NAME)
