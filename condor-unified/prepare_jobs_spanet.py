# Scritp to prepare jobs for plotting with make_histograms_rdataframe.py

import os, glob  
import ROOT
import math

current_path = '/eos/home-x/xiangran/CMSSW_12_5_2/src/hhh-analysis-framework/'
script = current_path + '/' + 'spanet-inference/predict_spanet_merge.py'

# pwd = '/afs/cern.ch/user/x/xiangran/CMSSW_13_3_0/src/condor-run/'
jobs_path = 'jobs'

submit="Universe   = vanilla\nrequest_memory = 7900\nExecutable = %s\nArguments  = $(ClusterId) $(ProcId)\nLog        = log/job_%s_%s_%s.log\nOutput     = output/job_%s_%s_%s.out\nError      = error/job_%s_%s_%s.error\n+MaxRuntime = 24*60*60\nQueue 1"
job_cmd = '#! /bin/bash\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\ncmsrel CMSSW_13_3_0\ncd CMSSW_13_3_0/src\ncmsenv\nulimit -s unlimited\nexport MYROOT=$(pwd)\nexport PYTHONPATH=$PYTHONPATH:$MYROOT \n%s'

submit_all = 'submit_all.sh'
manual_all = 'manual_run_all.sh'

jobs = []
manual_jobs = []

version = 'v34'
batch_size = 5000

procstodo = [
    # "JetHT",
    # "HHHTo6B_c3_0_d4_0",
    # "GluGluToHHTo4B_cHHH1",
    # "GluGluToHHTo4B_cHHH1JERDOWN",
    # "GluGluToHHTo4B_cHHH1JESUP",  
    # "GluGluToHHTo4B_cHHH1JERUP",  
    # "GluGluToHHTo4B_cHHH1JMRDOWN",
    # "GluGluToHHTo4B_cHHH1JESDOWN",
    # "GluGluToHHTo4B_cHHH1JMRUP",  
    # "HHHTo6B_c3_0_d4_0JERUP",  
    # "HHHTo6B_c3_0_d4_0JESUP",
    # "HHHTo6B_c3_0_d4_0JESDOWN",
    # "HHHTo6B_c3_0_d4_0JERDOWN",
    # "HHHTo6B_c3_0_d4_0JMRDOWN",
    # "HHHTo6B_c3_0_d4_0JMRUP",
    "QCD_datadriven"
]
for year in ['2016',"2016APV"]:#,'2018']:
    # path_to_samples = '/eos/cms/store/group/phys_higgs/cmshhh/%s_ak8_option4_%s/mva-inputs-%s/inclusive-weights/'%(version,year,year)
    path_to_samples = '/eos/home-x/xiangran/samples/%s_%s/inclusive-weights/'%(year,version)
    for f_in in procstodo:
        file = path_to_samples+'/' + f_in +".root"
        df = ROOT.RDataFrame("Events", file)
        batch_start = int(df.Count().GetValue()*remove_ratio)
        entries = df.Count().GetValue()-batch_start
        n_batches = math.floor(float(entries)/batch_size)
        for j in range(n_batches+1):
            filename = 'job_%s_%s_%d.sh'%(f_in,year,j)
            cmd = 'python3 %s  -v %s --f_in %s --year %s --batch_size %d --batch_number %d --batch_start'%(script,version,f_in,year,batch_size,j,batch_start)

            print("Writing %s"%filename)
            with open(jobs_path + '/' + filename, 'w') as f:
                f.write(job_cmd%cmd)
            manual_jobs.append(filename)

            submit_file = 'submit_%s_%s_%s'%(f_in,year,j)
            print('Writing %s/%s'%(jobs_path, submit_file))
            with open(jobs_path + '/' + submit_file, 'w') as f:
                f.write(submit%(jobs_path+'/'+filename,f_in,year,j,f_in,year,j,f_in,year,j))
            jobs.append(submit_file)

cmd = '#!/bin/bash\n'
for j in jobs:
    cmd += 'condor_submit %s/%s \n'%(jobs_path, j)


with open(submit_all, 'w') as f:
    f.write(cmd)


cmd = '#!/bin/bash\n'
for f in manual_jobs:
    cmd += 'source %s/%s/%s\n'%(pwd,jobs_path,f)

with open(manual_all,'w') as f:
    f.write(cmd)
                        
