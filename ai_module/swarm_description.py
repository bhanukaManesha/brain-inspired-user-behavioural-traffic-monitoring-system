SWARM_DESCRIPTION = {
"includedFields":[
{
    "fieldName" : "timestamp",
    "fieldType" : "datetime"
},
{
    "fieldName" : "size_udp",
    "fieldType" : "float",
    "maxValue"  : 68596,
    "minValue"  : 1024
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
    "predictedField" : "size_udp"
},
"iterationCount":-1,
"swarmSize":"medium"
}
