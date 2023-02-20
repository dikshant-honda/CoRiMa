# -*- coding: utf-8 -*-
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

from __future__ import annotations

from risk_model import Probability, Trajectory, UncertaintyConfig, compute_survival
from risk_model.event_calculators.overlap_calculator import calculate_overlaps

from .config import UNCERTAINTY_CONFIG, ObjectType
from .model import DataPoint


def _find_config(config_type: str) -> UncertaintyConfig:
    object_type = {
        "person": ObjectType.PEDESTRIAN,
        "car": ObjectType.CAR,
        "bus": ObjectType.TRUCK,
        "bicycle": ObjectType.BICYCLE,
    }.get(config_type, ObjectType.PEDESTRIAN)
    return UNCERTAINTY_CONFIG[object_type]


def predict_collisions(
    datapoints: list[DataPoint],
    delta_t: float = 0.05,
    trajectory_length: int = 240,
    with_types: bool = True,
) -> list[tuple[DataPoint, Probability]]:
    """Predict collision risks with a static ego."""

    uncertain_ego_trajectory = Trajectory.static_ego(delta_t=delta_t, trajectory_length=trajectory_length).uncertain(
        UNCERTAINTY_CONFIG[ObjectType.PEDESTRIAN]
    )

    uncertain_trajectories = [
        Trajectory.linear_prediction(
            trajectory_id=datapoint.id,
            position=datapoint.position,
            velocity=datapoint.velocity,
            delta_t=delta_t,
            trajectory_length=trajectory_length,
        ).uncertain(_find_config(datapoint.type) if with_types else _find_config("car"))
        for datapoint in datapoints
    ]

    events = calculate_overlaps(uncertain_ego_trajectory, uncertain_trajectories)

    return list(zip(datapoints, compute_survival(events, delta_t=delta_t)))
