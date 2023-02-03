#!/bin/bash
#
#  Pylint checks
#
#  Copyright (C)
#  Honda Research Institute Europe GmbH
#  Carl-Legien-Str. 30
#  63073 Offenbach/Main
#  Germany
#
#  UNPUBLISHED PROPRIETARY MATERIAL.
#  ALL RIGHTS RESERVED.
#
#

set -euo pipefail

source "$(poetry -q run poetry env info --path)"/bin/activate

pylint -f "${1:-colorized}" src/*
