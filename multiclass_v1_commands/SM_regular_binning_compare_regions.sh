#!/bin/bash
echo "Version: " $1
echo "extra options" $2

law run PlotUpperLimitsAtPoint \
  --version $1 \
  --pois r \
  --multi-datacards $HHH:$HH:$HHH,$HH:$HHH,$HH,$CR \
  --datacard-names "HHH6b SR-only","HH4b SR-only","HHH+HH SR-only","HHH+HH SR+CR" \
  --sort-by expected \
  --campaign run2 \
  --x-log \
  --h-lines 1 \
  --hh-model "model_dummy.model_dummy" \
  --workers 4 \
  $2

#  --use-snapshot \
#--UpperLimits-workflow htcondor \
#--CreateWorkspace-workflow htcondor \
#--Snapshot-workflow htcondor \
#  --UpperLimits-max-runtime 30h \
#  --Snapshot-max-runtime 48h \
#  --CreateWorkspace-max-runtime 48h \
#  --CreateWorkspace-test-timming \
#  --CreateWorkspace-custom-args "${CreateWSArgs}" \