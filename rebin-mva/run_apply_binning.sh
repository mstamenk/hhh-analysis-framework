#!/bin/bash
# Author: Yuhao Wang (Chuyi)
# Wrapper script to enter CMS environment and run apply_binning_xinyue.py

set -e  # Exit on error

# Paths (modify if needed)
WORKDIR="/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework"

# Arguments
SCRIPT_PATH=$1     # Path to apply_binning_xinyue.py
YEAR=$2            # e.g., 2016, 2016APV, etc.
PROB=$3            # e.g., ProbHHH6b
VAR=$4             # e.g., ProbMultiH
VERSION=$5         # e.g., v34

# Go to working directory and load CMS environment
cd "$WORKDIR"
source setup.sh
cmssw-el7
cmsenv

# Run the Python script with the provided arguments
python3 "$SCRIPT_PATH" \
    --year "$YEAR" \
    --path_year "$YEAR" \
    --prob "$PROB" \
    --var "$VAR" \
    --version "$VERSION" \
    --doSyst
