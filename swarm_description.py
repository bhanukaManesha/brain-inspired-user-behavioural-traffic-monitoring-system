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
},
{
    "fieldName" : "total_tcp",
    "fieldType" : "int",
    "maxValue"  : 143352,
    "minValue"  : 0
},
{
    "fieldName" : "total_http",
    "fieldType" : "int",
    "maxValue"  : 7045,
    "minValue"  : 638
},
{
    "fieldName" : "total_udp",
    "fieldType" : "int",
    "maxValue"  : 638,
    "minValue"  : 11
},
{
    "fieldName" : "size",
    "fieldType" : "int",
    "maxValue"  : 15315931,
    "minValue"  : 13836
},
{
    "fieldName" : "size_tcp",
    "fieldType" : "int",
    "maxValue"  : 15278447,
    "minValue"  : 0
},
{
    "fieldName" : "size_http",
    "fieldType" : "int",
    "maxValue"  : 6090358,
    "minValue"  : 0
},
{
    "fieldName" : "size_udp",
    "fieldType" : "int",
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
        "source": "file://updated_test.csv",
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
"iterationCount":1,
"swarmSize":"small"
}
