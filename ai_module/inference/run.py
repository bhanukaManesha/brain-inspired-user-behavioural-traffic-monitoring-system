
import importlib
import sys
import csv
import datetime
import os
import cPickle as pickle

from preprocessing import json2csv,removeTimeStamp,csv2json
from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.frameworks.opf.prediction_metrics_manager import MetricsManager

import nupic_output

DESCRIPTION = ('Anomaly Detection for Network Activity')
SYSTEM_NAME = "network_anomaly"
DATA_DIR = "."
INPUT_FILE = "filtered_data.csv"
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

def getModelParamsFromName(modelName):
    importName = "MODELS_PARAMS."+ modelName +"_model_params" 
    print("Importing model params from " + modelName)
    try:
      importedModelParams = importlib.import_module(importName).MODEL_PARAMS
    except ImportError:
      raise Exception("No model params exist for '%s'. Run swarm first!"
                      % importName)
    return importedModelParams

def runDataThroughNupic(MODELS, anomaly_helper, inputData, systemName):

  ANOMALY_OBJ = nupic_output.NuPICFileOutput(systemName)

  ANOMALY_OBJ.anomalyLikelihoodHelper = anomaly_helper
  ANOMALY_LIKELIHOOD = [0.0 for i in range(len(MODEL_NAMES))]
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)

  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  
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
        anomalyLikelihood = ANOMALY_OBJ.get_anomaly_likelihood(timestamp, data, prediction ,anomalyScore)
        
        ANOMALY_LIKELIHOOD[model_index] = anomalyLikelihood
  
    ANOMALY_OBJ.write(timestamp,ANOMALY_LIKELIHOOD)

  inputFile.close()
  ANOMALY_OBJ.close()
  print("Saving Anomaly Object")

  path = os.path.join(os.getcwd(), "objects/")
  if os.path.isdir(path) is False:
    os.mkdir('objects')

  with open('objects/anomaly_object.pkl', 'wb') as o:
    pickle.dump(ANOMALY_OBJ.anomalyLikelihoodHelper, o)

def loadModels(models,model_names):
  for index in range(len(model_names)):
    print("Loading " + model_names[index] + " ...")
    path = os.path.join(os.getcwd(), "saved models/" + model_names[index] + "/")
    # models[index].load(path)
    models[index].readFromCheckpoint(path)
    print(model_names[index] + "model successfully loaded")

  with open('objects/anomaly_object.pkl', 'rb') as f:
    anomaly_obj = pickle.load(f)
  
  return models,anomaly_obj

def initalizeModels():
  MODELS = []

  for index in range(len(MODEL_NAMES)):
    model = ModelFactory.create(getModelParamsFromName(MODEL_NAMES[index]))
    model.enableInference({"predictedField": MODEL_NAMES[index]})
    MODELS.append(model)
  anomaly = nupic_output.NuPICFileOutput(SYSTEM_NAME)
  ANOMALY_OBJ = anomaly.anomalyLikelihoodHelper

  return MODELS,ANOMALY_OBJ

def saveModels(models,model_names,anomaly_obj):
  for i in range(len(models)):
    print("Saving " + model_names[i] + " ...")
    path = os.path.join(os.getcwd(), "saved models/" + model_names[i]+ "/")
    models[i].writeToCheckpoint(path)
    # models[i].save(path)
    print(model_names[i] + " model saved")


def runModel(systemName):
  print "Creating models for %s..." % systemName
  MODELS,ANOMALY_OBJ = initalizeModels()
  path = os.path.join(os.getcwd(), "saved models/")
  if os.path.isdir(path):
      MODELS,ANOMALY_OBJ = loadModels(MODELS,MODEL_NAMES)
  inputData = "%s/data/%s" % (DATA_DIR, INPUT_FILE)
  runDataThroughNupic(MODELS,ANOMALY_OBJ, inputData, systemName)
  saveModels(MODELS,MODEL_NAMES,ANOMALY_OBJ)

#################################################

def inference_data(json):
    json2csv(json,"data/data.csv",True)
    removeTimeStamp("data/data.csv","data/filtered_data.csv")

    # Run the model
    runModel(SYSTEM_NAME)
    return csv2json()

#################################################

#!flask/bin/python

from flask import Flask, jsonify,request
from waitress import serve
app = Flask(__name__)

@app.route('/', methods=['GET'])
def app_index():
    return "Please use the POST request with extension : data"

@app.route('/data', methods=['POST'])
def receive_data():
    content = request.get_json()
    data = inference_data(content["data"])
    return jsonify(data)

def create_app():
    serve(app, host="0.0.0.0",port=80)