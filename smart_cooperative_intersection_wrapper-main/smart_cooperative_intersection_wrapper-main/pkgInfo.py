# -*- coding: utf-8 -*-
#
#  Custom package settings
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

name = "risk_model_wrapper"
sqLevel = "advanced"

sqOptOutRules = [
    "C10",
    "GEN07",
    "PY05",
    "DOC03",
]
sqComments = {
    "C10": "Omitting C/C++ files",
    "GEN07": "tests present",
    "PY05": "Using pylint for static code analysis",
    "DOC03": "Examples listed in README.md",
}

sqOptOutDirs = [".venv"]

scripts = {"unittest": "ci-unit-test.sh"}
