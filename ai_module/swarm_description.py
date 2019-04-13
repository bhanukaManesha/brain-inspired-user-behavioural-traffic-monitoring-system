SWARM_DESCRIPTION = {
"includedFields":[
{
    "fieldName" : "timestamp",
    "fieldType" : "datetime"
},
{
    "fieldName" : "total",
    "fieldType" : "int",
    "maxValue"  : 143909,
    "minValue"  : 187
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
        5
    ],
    "predictedField" : "total"
},
"iterationCount":-1,
"swarmSize":"medium"
}
