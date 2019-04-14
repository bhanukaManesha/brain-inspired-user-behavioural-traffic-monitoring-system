
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


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
GYM_NAME = "network"  # or use "rec-center-every-15m-large"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"

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

def createModel():
  model = ModelFactory.create(model_params.MODEL_PARAMS)
  model.enableInference({"predictedField": "total"})
  return model



def getModelParamsFromName(gymName):
  importName = "model_params.%s_model_params" % (
    gymName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % gymName)
  return importedModelParams



def runIoThroughNupic(inputData, model, gymName, plot):
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  if plot:
    output = nupic_output.NuPICPlotOutput([gymName])
  else:
    output = nupic_output.NuPICFileOutput([gymName])

  metricsManager = MetricsManager(_METRIC_SPECS, model.getFieldInfo(),
                                  model.getInferenceType())

  counter = 0
  for row in csvReader:
    counter += 1

    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    total = float(row[1])
    
    result = model.run({
      "timestamp": timestamp,
      "total": total
      })

    result.metrics = metricsManager.update(result)

    if counter % 100 == 0:
      print "Read %i lines..." % counter
      print ("After %i records, 1-step altMAPE=%f" % (counter,
              result.metrics["multiStepBestPredictions:multiStep:"
                             "errorMetric='altMAPE':steps=1:window=1000:"
                             "field=total"]))


    result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    output.write([timestamp], [total], [prediction])

    if plot and counter % 2 == 0:
        output.refreshGUI()

  inputFile.close()
  output.close()



def runModel(gymName, plot=False):
  print "Creating model from %s..." % gymName
  model = createModel()
  inputData = "%s/csv/%s.csv" % (DATA_DIR, gymName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, gymName, plot)



if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]
  if "--plot" in args:
    plot = True
  runModel(GYM_NAME, plot=plot)
