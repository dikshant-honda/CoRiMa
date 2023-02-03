#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Integration test executing prediction and comparing it to original values
#
# Copyright (C)
# Honda Research Institute Europe GmbH
# Carl-Legien-Str. 30
# 63073 Offenbach/Main
# Germany
#
# UNPUBLISHED PROPRIETARY MATERIAL.
# ALL RIGHTS RESERVED.
#
#

import json
import sys
from copy import deepcopy
from pathlib import Path
import time
import numpy as np

from numpy import allclose

from risk_model_wrapper.run_risk_model import (
    _annotate_input_data_with_risk,
    _extract_data_points,
    _load_input_data,
    predict_collisions,
)

dictionary = {}

x1 = np.linspace(0, 20, 100)
y1 = 4*x1
y2 = 2*x1 + 30

for i in range(len(x1)):
    dictionary.update(
        {str(time.time()):
            {"data":[
                    {
                        "type":"object",
                        "position":[x1[i], y1[i], 0],
                        "velocity":[2, 2, 0],
                        "label_id": 14,
                        "label_name": "car",
                        "tracking_id": 14
                    },
                    {
                        "type":"object",
                        "position":[x1[i], y2[i], 0],
                        "velocity":[2, 2, 0],
                        "label_id": 7,
                        "label_name": "car",
                        "tracking_id": 7
                    }
                ]
            }
        }
    )

json_object = json.dumps(dictionary, indent = 4) 

with open("/home/dikshant/catkin_ws/src/CoRiMa/smart_cooperative_intersection_wrapper-main/data/Export_Honda/example1/sample.json", "w") as outfile:
    outfile.write(json_object)

for path in Path("smart_cooperative_intersection_wrapper-main/data/Export_Honda").glob("*"):
    honda_export_file_path = path.joinpath("sample.json")

    print(f"Testing: {honda_export_file_path.as_posix()}")

    input_data = _load_input_data(honda_export_file_path.as_posix())
    annotated_input_data = deepcopy(input_data)

    for timestamp, sample in input_data.items():
        if len(sample["data"]) == 0:
            continue
        data_points = _extract_data_points(sample["data"])
        predicted_collisions = predict_collisions(data_points)
        annotated_input_data[timestamp] = _annotate_input_data_with_risk(sample, predicted_collisions)

json_object_2 = json.dumps(annotated_input_data, indent = 4) 

with open("/home/dikshant/catkin_ws/src/CoRiMa/smart_cooperative_intersection_wrapper-main/data/Export_Honda/example1/processed_sample_data.json", "w") as outfile:
    outfile.write(json_object_2)