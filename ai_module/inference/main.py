from preprocessing import json2csv,removeTimeStamp
from run import runModel

SYSTEM_NAME = "network_anomaly"

def inference_data(json):
    # print(json)
    json2csv(json,"../ai_module/inference/data/data.csv",True)
    removeTimeStamp("../ai_module/inference/data/data.csv","../ai_module/inference/data/filtered_data.csv")


    # Run the model
    runModel(SYSTEM_NAME)







