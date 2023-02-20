#!/bin/bash
#
#  Unit testing with pytest
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

python tests/integration/integration_test.py
