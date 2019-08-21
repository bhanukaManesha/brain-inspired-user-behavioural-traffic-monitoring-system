import json
import requests
import csv

def json2csv(json_data,file_name,new_file=False):
    if new_file:
        f = csv.writer(open(file_name, "w+"))
        f.writerow(["datetime","total","total_tcp","total_http","total_udp","size","size_tcp","size_http","size_udp"])
    else:
        f = csv.writer(open(file_name, "a"))

    for line in json_data:
        f.writerow([
            line["datetime"],
            line["total"],
            line["total_tcp"],
            line["total_http"],
            line["total_udp"],
            line["size"],
            line["size_tcp"],
            line["size_http"],
            line["size_udp"]
            ])

if __name__ == '__main__':
        url = "http://0.0.0.0:5000/data"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        file_name = 'one'
        count = 0
        with open('test_file/'+ file_name + '.csv','rt')as f:
                s = csv.reader(f)
                next(s)
                largeL = []
                for row in s:
                        count += 1
                        obj = {"timestamp":float(row[0]),
                                "total": float(row[1]),
                                "total_tcp": float(row[2]),
                                "total_http": float(row[3]),
                                "total_udp": float(row[4]),
                                "size": float(row[5]),
                                "size_tcp": float(row[6]),
                                "size_http": float(row[7]),
                                "size_udp": float(row[8])}
                        
                        
                        largeL.append(obj)
                        if count % 2000 == 0:
                                data={'data': largeL}
                                r = requests.post(url, data=json.dumps(data), headers=headers)    
                                largeL = []

                                data = json.loads(r.content)

                                path = 'test_file/output/'+ file_name + '_out.csv'
                                json2csv(data,path,new_file=False)

