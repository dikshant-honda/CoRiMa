import json
import time

dictionary = {}

trials = 2

for _ in range(trials):
    dictionary.update({str(time.time()):
    {"data":[
        {
            "type":"object",
            "position":[1,2,3],
            "velocity":[0,0,0],
            "label_id": 14,
            "label_name": "car",
            "tracking_id": 14
        },
        {
            "type":"object",
            "position":[4,2,3],
            "velocity":[0,0,0],
            "label_id": 7,
            "label_name": "car",
            "tracking_id": 7
        }
        ]
    }})

json_object = json.dumps(dictionary, indent = 4) 

with open("sample.json", "w") as outfile:
    outfile.write(json_object)