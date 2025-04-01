# Scritp to prepare jobs for plotting with make_histograms_rdataframe.py

import os, glob

years = ['2016','2016APV','2018']

version = 'v31'

current_path = '/isilon/data/users/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework/'
script = current_path + '/' + 'process_qcd_sample_no_trigger.py'
#script = current_path + '/' + 'prepare_inclusive_samples.py'

pwd = current_path + '/' + 'condor-inclusive-samples/'
jobs_path = 'jobs'

submit="Universe   = vanilla\nExecutable = %s\nArguments  = $(ClusterId) $(ProcId)\nLog        = log/job_%s_%s_%s.log\nOutput     = output/job_%s_%s_%s.out\nError      = error/job_%s_%s_%s.error\nQueue 1"
job_cmd = '#! /bin/bash\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\ncmsrel CMSSW_12_5_2\ncd CMSSW_12_5_2/src\ncmsenv\nulimit -s unlimited\nexport MYROOT=$(pwd)\nexport PYTHONPATH=$PYTHONPATH:$MYROOT \n%s'
#job_cmd = '%s'


submit_all = 'submit_all.sh'
manual_all = 'manual_run_all.sh'

jobs = []
manual_jobs = []
for year in ['2018','2017','2016','2016APV']:
#for year in years:
    #path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-spanet-boosted-classification-variables-pnet-v4-nanoaod'%(version,year)
    #path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-spanet-boosted-classification-variables-nanoaod'%(version,year)
    #path = '/isilon/data/users/mstamenk/eos-triple-h/%s/mva-inputs-%s/inclusive_resolved/'%(version,year)
    path = '/isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/condor/%s_ak8_option4_%s/*/parts/'%(version,year)
    files = glob.glob(path + '/*.root')
    files = [f for f in files if 'QCD' in f]
    for f_in in files:
        f_name = os.path.basename(f_in).replace('.root','')
        filename = 'job_%s_%s_%s.sh'%(f_name,year,version)
        cmd = 'python3 %s --f_in %s --year %s --version %s '%(script,f_in,year,version)

        print("Writing %s"%filename)
        with open(jobs_path + '/' + filename, 'w') as f:
            f.write(job_cmd%cmd)
        manual_jobs.append(filename)

        submit_file = 'submit_%s_%s_%s'%(f_name,year,version)
        print('Writing %s/%s'%(jobs_path, submit_file))
        with open(jobs_path + '/' + submit_file, 'w') as f:
            f.write(submit%(jobs_path+'/'+filename,f_name,year,version,f_name,year,version,f_name,year,version))
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
                        
