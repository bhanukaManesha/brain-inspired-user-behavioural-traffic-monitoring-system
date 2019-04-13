SWARM_DESCRIPTION = {
"includedFields":[
{
    "fieldName" : "timestamp",
    "fieldType" : "datetime"
},
{
    "fieldName" : "total",
    "fieldType" : "float",
    "maxValue"  : 143909.0,
    "minValue"  : 187.0
}
],
"streamDef":
{
    "info" : "network",
    "version": 1,
    "streams" : [
        {
        "info" : "Network 1",
        "source": "file://csv/network.csv",
        "columns":[
            "*"
            ]
        }
    ]
},
"inferenceType": "TemporalMultiStep",
"inferenceArgs": {
    "predictionSteps":[
        1
    ],
    "predictedField" : "total"
},
"iterationCount":-1,
"swarmSize":"medium"
}
