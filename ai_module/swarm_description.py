SWARM_DESCRIPTION = {
"includedFields":[
{
    "fieldName" : "timestamp",
    "fieldType" : "datetime"
},
{
    "fieldName" : "total_tcp",
    "fieldType" : "int",
    "maxValue"  : 143352,
    "minValue"  : 0
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
"inferenceType": "TemporalAnomaly",
"inferenceArgs": {
    "predictionSteps":[
        1
    ],
    "predictedField" : "total_tcp"
},
"iterationCount":-1,
"swarmSize":"medium"
}
