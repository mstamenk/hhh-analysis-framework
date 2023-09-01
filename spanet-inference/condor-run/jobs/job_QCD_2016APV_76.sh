#! /bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_12_5_2
cd CMSSW_12_5_2/src
cmsenv
ulimit -s unlimited
export MYROOT=$(pwd)
export PYTHONPATH=$PYTHONPATH:$MYROOT 
python3 /isilon/data/users/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework/spanet-inference//predict_spanet.py --f_in QCD --year 2016APV --batch_size 100000 --batch_number 76