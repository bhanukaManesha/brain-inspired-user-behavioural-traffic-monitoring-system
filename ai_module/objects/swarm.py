# #!usr/bin/env python
# import os
# import pprint
# import logging

# from nupic.swarming import permutations_runner
# from swarm_description import SWARM_DESCRIPTION
# logging.basicConfig()

# def writeModelParams(modelParams):
#     outDir = os.path.join(os.getcwd(),"model_params")
#     if not os.path.exists(outDir):
#         os.mkdir(outDir)
#     outPath = os.path.join(outDir, "model_params.py")

#     pp = pprint.PrettyPrinter(indent=2)
#     with open(outPath,"wb") as outFile:
#         modelParamsString = pp.pformat(modelParams)
#         outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
#     return outPath


# def swarm(inputFile):

#     swarmWorkDir = os.path.abspath("swarm")
#     if not os.path.exists(swarmWorkDir):
#         os.mkdir(swarmWorkDir)

#     modelParams = permutations_runner.runWithConfig(
#         SWARM_DESCRIPTION,
#         {'maxWorkers': 4, 'overwrite': True},
#         outputLabel = "network_output",
#         outDir=swarmWorkDir,
#         permWorkDir=swarmWorkDir
#     )

#     writeModelParams(modelParams)


# if __name__ == "__main__":
#     swarm("updated_test.csv")

import os
import pprint

# add logging to output errors to stdout
import logging
logging.basicConfig()

from nupic.swarming import permutations_runner
from swarm_description import SWARM_DESCRIPTION

INPUT_FILE = "csv/test_large.csv"
DESCRIPTION = (
  "This script runs a swarm on the input data (test_large.csv) and\n"
  "creates a model parameters file in the `model_params` directory containing\n"
  "the best model found by the swarm. Dumps a bunch of crud to stdout because\n"
  "that is just what swarming does at this point. You really don't need to\n"
  "pay any attention to it.\n"
  )



def modelParamsToString(modelParams):
  pp = pprint.PrettyPrinter(indent=2)
  return pp.pformat(modelParams)



def writeModelParamsToFile(modelParams, name):
  cleanName = name.replace(" ", "_").replace("-", "_")
  paramsName = "%s_model_params.py" % cleanName
  outDir = os.path.join(os.getcwd(), 'model_params')
  if not os.path.isdir(outDir):
    os.mkdir(outDir)
  # Create an __init__.py so the params are recognized.
  initPath = os.path.join(outDir, '__init__.py')
  open(initPath, 'a').close()
  outPath = os.path.join(os.getcwd(), 'model_params', paramsName)
  with open(outPath, "wb") as outFile:
    modelParamsString = modelParamsToString(modelParams)
    outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
  return outPath



def swarmForBestModelParams(swarmConfig, name, maxWorkers=4):
  outputLabel = name
  permWorkDir = os.path.abspath('swarm')
  if not os.path.exists(permWorkDir):
    os.mkdir(permWorkDir)
  modelParams = permutations_runner.runWithConfig(
    swarmConfig,
    {"maxWorkers": maxWorkers, "overwrite": True},
    outputLabel=outputLabel,
    outDir=permWorkDir,
    permWorkDir=permWorkDir,
    verbosity=0
  )
  modelParamsFile = writeModelParamsToFile(modelParams, name)
  return modelParamsFile



def printSwarmSizeWarning(size):
  if size is "small":
    print "= THIS IS A DEBUG SWARM. DON'T EXPECT YOUR MODEL RESULTS TO BE GOOD."
  elif size is "medium":
    print "= Medium swarm. Sit back and relax, this could take awhile."
  else:
    print "= LARGE SWARM! Might as well load up the Star Wars Trilogy."



def swarm(filePath):
  name = os.path.splitext(os.path.basename(filePath))[0]
  print "================================================="
  print "= Swarming on %s data..." % name
  printSwarmSizeWarning(SWARM_DESCRIPTION["swarmSize"])
  print "================================================="
  modelParams = swarmForBestModelParams(SWARM_DESCRIPTION, name)
  print "\nWrote the following model param files:"
  print "\t%s" % modelParams



if __name__ == "__main__":
  print DESCRIPTION
  swarm(INPUT_FILE)