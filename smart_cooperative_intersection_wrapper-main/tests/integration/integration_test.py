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

from numpy import allclose

from risk_model_wrapper.run_risk_model import (
    _annotate_input_data_with_risk,
    _extract_data_points,
    _load_input_data,
    predict_collisions,
)


def compare_risks(input1, input2) -> str:
    """Compares all risk values up to a certain accuracy."""
    error_str = ""
    for (_, entry1), (_, entry2) in zip(input1.items(), input2.items()):
        for data1, data2 in zip(entry1["data"], entry2["data"]):
            if not allclose(data1["risk"], data2["risk"], rtol=1e-10):
                error_str += f'ERROR in tracking id: {data1["tracking_id"]}, calulated: {data1["risk"]}, test_value: {data2["risk"]} \n'
    return error_str


def main() -> None:
    """Loads data from file, predicts risk, and compares it to previously stored data."""
    failed = False

    for path in Path("smart_cooperative_intersection_wrapper-main/data/Export_Honda").glob("*"):
        honda_export_file_path = path.joinpath("sample.json")
        processed_data_file_path = path.joinpath("processed_sample_data.json")
        
        print(f"Testing: {honda_export_file_path.as_posix()}")

        with processed_data_file_path.open() as file:
            processed_data = json.load(file)

        input_data = _load_input_data(honda_export_file_path.as_posix())
        annotated_input_data = deepcopy(input_data)

        for timestamp, sample in input_data.items():
            if len(sample["data"]) == 0:
                continue
            data_points = _extract_data_points(sample["data"])
            predicted_collisions = predict_collisions(data_points)
            annotated_input_data[timestamp] = _annotate_input_data_with_risk(sample, predicted_collisions)

        ret = compare_risks(annotated_input_data, processed_data)
        if ret != "":
            print(f"Failed for file: {honda_export_file_path.as_posix()}")
            print(ret)
            failed = True

    if failed:
        print("Integration test failed")
    else:
        print("Integration test successful")


if __name__ == "__main__":
    main()
