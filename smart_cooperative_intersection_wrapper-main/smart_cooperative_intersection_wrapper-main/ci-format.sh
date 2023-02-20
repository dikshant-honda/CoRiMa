#!/bin/bash
#
#  Format check using black
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

if [[ ${1:-} == "--check" ]]; then
    isort_options="--check-only"
    black_options="--check --diff"
fi

EXIT_CODE=0

# shellcheck disable=SC2248
isort --quiet ${isort_options:-} ./ || EXIT_CODE=1
# shellcheck disable=SC2086
black ${black_options:-} */ || EXIT_CODE=1

exit "${EXIT_CODE}"
