#! /bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_12_5_2
cd CMSSW_12_5_2/src
cmsenv
ulimit -s unlimited
export MYROOT=$(pwd)
export PYTHONPATH=$PYTHONPATH:$MYROOT 
python3 /isilon/data/users/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework//process_qcd_sample_no_trigger.py --f_in /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/condor/v31_ak8_option4_2018/mc/parts/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8_tree_10.root --year 2018 --version v31 