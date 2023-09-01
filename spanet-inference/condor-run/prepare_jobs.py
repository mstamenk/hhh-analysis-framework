# Scritp to prepare jobs for plotting with make_histograms_rdataframe.py

import os, glob  
import ROOT
import math


current_path = '/isilon/data/users/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework/spanet-inference/'
script = current_path + '/' + 'predict_spanet.py'

pwd = current_path + '/' + 'condor-run/'
jobs_path = 'jobs'

submit="Universe   = vanilla\nrequest_memory = 7900\nExecutable = %s\nArguments  = $(ClusterId) $(ProcId)\nLog        = log/job_%s_%s_%s.log\nOutput     = output/job_%s_%s_%s.out\nError      = error/job_%s_%s_%s.error\nQueue 1"
job_cmd = '#! /bin/bash\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\ncmsrel CMSSW_12_5_2\ncd CMSSW_12_5_2/src\ncmsenv\nulimit -s unlimited\nexport MYROOT=$(pwd)\nexport PYTHONPATH=$PYTHONPATH:$MYROOT \n%s'
#job_cmd = '%s'


submit_all = 'submit_all.sh'
manual_all = 'manual_run_all.sh'

jobs = []
manual_jobs = []
#for year in ['2016','2016APV','2017','2018']:

year = '2018'
version = 'v27'



batch_size = 100e3
for year in ['2016','2016APV','2017','2018']:
    path_to_samples = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-nanoaod/'%(version,year)
    files = glob.glob(path_to_samples+'*.root')
    samples = [os.path.basename(s).replace('.root','') for s in files]
    for i in range(len(files)):
        f_in = samples[i]
        # Re-submit data
        if 'JetHT' not in f_in and 'BTagCSV' not in f_in and 'SingleMuon' not in f_in: continue
        f = files[i]
        df = ROOT.RDataFrame("Events", f)
        entries = df.Count().GetValue()
        n_batches = math.floor(float(entries)/batch_size)
        for j in range(n_batches+1):
            filename = 'job_%s_%s_%d.sh'%(f_in,year,j)
            cmd = 'python3 %s --f_in %s --year %s --batch_size %d --batch_number %d'%(script,f_in,year,batch_size,j)

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
                        
