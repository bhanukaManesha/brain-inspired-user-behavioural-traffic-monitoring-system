# Brain Inspired User Behavioural Traffic Monitoring System - MSC APICTA 2019
Numenta HTM model for Network Anomaly Detection


## Production Server Setup Process

```
# Build the docker image
docker build -t apicta .

# Run the production server inside the docker container
# This will run the server on port 3000
docker run -p 3000:80 apicta
```


## Accessing the API
Send a POST request this route to get the prediction
```
localhost:3000/data
```

Use this format for the api calls. 
```
{"data": [
    {
      "timestamp": 1331901000.0,
      "total": 17312,
      "total_tcp": 16891,
      "total_http": 422,
      "total_udp": 173,
      "size": 2558408,
      "size_tcp": 2528168,
      "size_http": 76414,
      "size_udp": 12279
    }
  ]
 }
```
Do note that mutiple time stamps are also valid
```
{"data": [
    {
      "timestamp": 1331901000.0,
      "total": 17312,
      "total_tcp": 16891,
      "total_http": 422,
      "total_udp": 173,
      "size": 2558408,
      "size_tcp": 2528168,
      "size_http": 76414,
      "size_udp": 12279
    },
    {
      "timestamp": 1331901000.0,
      "total": 17312,
      "total_tcp": 16891,
      "total_http": 422,
      "total_udp": 173,
      "size": 2558408,
      "size_tcp": 2528168,
      "size_http": 76414,
      "size_udp": 12279
    },
    {
      "timestamp": 1331901000.0,
      "total": 17312,
      "total_tcp": 16891,
      "total_http": 422,
      "total_udp": 173,
      "size": 2558408,
      "size_tcp": 2528168,
      "size_http": 76414,
      "size_udp": 12279
    }
  ]
 }
``
