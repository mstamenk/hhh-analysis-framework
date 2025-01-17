# Scritp to prepare jobs for plotting with make_histograms_rdataframe.py

import os, glob  
import ROOT
import math


current_path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/spanet-inference/'
#script = current_path + '/' + 'predict_spanet_classification_pnet_all_vars.py'
script = current_path + '/' + 'predict_spanet_classification_categorisation.py'

pwd = current_path + '/' + 'condor-xinyue/'
jobs_path = 'jobs'

submit="Universe   = vanilla\nrequest_memory = 7900\nExecutable = %s\nArguments  = $(ClusterId) $(ProcId)\nLog        = log/job_%s_%s_%s.log\nOutput     = output/job_%s_%s_%s.out\nError      = error/job_%s_%s_%s.error\nQueue 1"
job_cmd = '#! /bin/bash\n#SBATCH -p batch\n#SBATCH -n 1\n#SBATCH -t 03:00:00\n#SBATCH --mem=24g\n%s\nexit'
#job_cmd = '%s'


submit_all = 'submit_all.sh'
manual_all = 'manual_run_all.sh'

jobs = []
manual_jobs = []
#for year in ['2016','2016APV','2017','2018']:

year = '2018'
version = 'v31-parts-no-lhe'

# path_to_samples = '/eos/cms/store/group/phys_higgs/cmshhh/NanoAODv9PNetAK4/output_2017/TTHHTo4b_HEFT_c2-3_TuneCP5_13TeV-madgraph-pythia8/NanoAODv9_ParticleNetAK4_RunIISummer20UL17MiniAODv2-106X_v9-v2/240614_080534/0000'
path_to_samples = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/spanet-inference/nano_7.root'


regime = 'inclusive-weights'
batch_size = 50e3
#for year in ['2016','2016APV','2017','2018']:
for year in ['2018']:
    #path_to_samples = '/users/mstamenk/scratch/mstamenk//samples-%s-%s-nanoaod/'%(version,year)
    # path_to_samples = '/users/mstamenk/scratch/mstamenk//%s/mva-inputs-%s/%s/'%(version,year,regime)
    path_to_samples = '/eos/cms/store/group/phys_higgs/cmshhh/NanoAODv9PNetAK4/output_2017/TTHHTo4b_HEFT_c2-3_TuneCP5_13TeV-madgraph-pythia8/NanoAODv9_ParticleNetAK4_RunIISummer20UL17MiniAODv2-106X_v9-v2/240614_080534/0000/'

    print("111111111")

    files = glob.glob(path_to_samples+'*.root')
    print("2222222")
    #files = [f for f in files if 'TTToSemi' in f or 'W' in f or 'Z' in f]
    samples = [os.path.basename(s).replace('.root','') for s in files]
    print("33333")
    print(samples)
    for i in range(len(files)):
        f_in = samples[i]
        f = files[i]
        df = ROOT.RDataFrame("Events", f)
        entries = df.Count().GetValue()
        n_batches = math.floor(float(entries)/batch_size)
        for j in range(n_batches+1):
            filename = 'job_%s_%s_%d.sh'%(f_in,year,j)
            cmd = 'python3 %s --f_in %s --year %s --batch_size %d --batch_number %d --version %s'%(script,f_in,year,batch_size,j,version)

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

if len(manual_jobs) > 1000:
    cmd1 = '#!/bin/bash\n'
    for f in manual_jobs[:999]:
        cmd1+= 'sbatch %s/%s/%s\n'%(pwd,jobs_path,f)
    with open(manual_all,'w') as f:
        f.write(cmd1)

    cmd2 =  '#!/bin/bash\n'
    for f in manual_jobs[999:]:
        cmd2+= 'sbatch %s/%s/%s\n'%(pwd,jobs_path,f)
    with open(manual_all.replace('.sh','_2.sh'), 'w') as f:
        f.write(cmd2)

else:
    cmd = '#!/bin/bash\n'
    for f in manual_jobs:
        cmd += 'sbatch %s/%s/%s\n'%(pwd,jobs_path,f)

    with open(manual_all,'w') as f:
        f.write(cmd)
                        
