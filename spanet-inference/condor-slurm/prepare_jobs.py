# Scritp to prepare jobs for plotting with make_histograms_rdataframe.py

import os, glob  
import ROOT
import math


import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--doCat', action='store_true') # doCat
parser.add_argument('--afterCat', action='store_true') # doCat
parser.add_argument('--secondInference', action='store_true') # doCat
parser.add_argument('--version', default = 'v34') # doCat
parser.add_argument('--year', default = '2017') # doCat
args = parser.parse_args()




current_path = '/users/mstamenk/hhh-analysis-framework/spanet-inference/'

#script = current_path + '/' + 'predict_spanet_classification_pnet_all_vars_v34.py'
script = current_path + '/' + 'predict_spanet_classification_pnet_all_vars.py'
if args.afterCat:
    #script = current_path + '/' + 'predict_spanet_classification_pnet_all_vars_v37.py'
    script = current_path + '/' + 'predict_classification_v34_run2.py'
#script = current_path + '/' + 'predict_spanet_classification_pnet_all_vars_masked.py'
if args.secondInference:
    script = current_path + '/' + 'predict_classification_v34_run2_3Higgs.py'

#script = current_path + '/' + 'predict_spanet_classification_pnet.py'
if args.doCat:
    #script = current_path + '/' + 'predict_spanet_classification_categorisation_v34.py'
    script = current_path + '/' + 'predict_spanet_classification_categorisation.py'
    #script = current_path + '/' + 'predict_classification_v34_run2.py'

pwd = current_path + '/' + 'condor-slurm/'
jobs_path = 'jobs'

submit="Universe   = vanilla\nrequest_memory = 7900\nExecutable = %s\nArguments  = $(ClusterId) $(ProcId)\nLog        = log/job_%s_%s_%s.log\nOutput     = output/job_%s_%s_%s.out\nError      = error/job_%s_%s_%s.error\nQueue 1"
job_cmd = '#! /bin/bash\n#SBATCH -p batch\n#SBATCH -n 1\n#SBATCH -t 03:00:00\n#SBATCH --mem=32g\n%s\nexit'
#job_cmd = '%s'


submit_all = 'submit_all.sh'
manual_all = 'manual_run_all.sh'

jobs = []
manual_jobs = []
#for year in ['2016','2016APV','2017','2018']:

year = '2018'
version = args.version


regime = 'inclusive-weights'
batch_size = 50e3
for year in [args.year]:
#for year in ['2016','2016APV','2017','2018']:
    #path_to_samples = '/users/mstamenk/scratch/mstamenk//samples-%s-%s-nanoaod/'%(version,year)
    path_to_samples = '/users/mstamenk/scratch/mstamenk//%s/mva-inputs-%s/%s/'%(version,year,regime)
    if args.doCat:
        path_to_samples = '/users/mstamenk/scratch/mstamenk//%s/mva-inputs-%s-spanet-boosted-classification/%s/'%(version,year,regime)

    if args.afterCat:
        path_to_samples = '/users/mstamenk/scratch/mstamenk//%s/mva-inputs-%s-categorisation-spanet-boosted-classification/%s/'%(version,year,regime)
    if args.secondInference: 
        path_to_samples = '/users/mstamenk/scratch/mstamenk//%s/mva-inputs-%s-spanet-boosted-classification-categorisation-spanet-boosted-classification/%s/'%(version,year,regime)
    files = glob.glob(path_to_samples+'*.root')
    #files = [f for f in files if 'TTToSemi' in f or 'W' in f or 'Z' in f]
    samples = [os.path.basename(s).replace('.root','') for s in files]
    for i in range(len(files)):
        f_in = samples[i]
        f = files[i]
        df = ROOT.RDataFrame("Events", f)
        entries = df.Count().GetValue()
        n_batches = math.floor(float(entries)/batch_size)
        for j in range(n_batches+1):
            filename = 'job_%s_%s_%d.sh'%(f_in,year,j)
            cmd = 'python3 %s --f_in %s --year %s --batch_size %d --batch_number %d --version %s '%(script,f_in,year,batch_size,j,version)
            if args.afterCat:
                cmd = 'python3 %s --f_in %s --year %s --batch_size %d --batch_number %d --version %s --afterCat'%(script,f_in,year,batch_size,j,version)
            if args.secondInference:
                cmd = 'python3 %s --f_in %s --year %s --batch_size %d --batch_number %d --version %s --secondInference'%(script,f_in,year,batch_size,j,version)

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


#with open(submit_all, 'w') as f:
#    f.write(cmd)
#
#    cmd1 = '#!/bin/bash\n'
#    for f in manual_jobs:
#        cmd1+= 'sbatch %s/%s/%s\n'%(pwd,jobs_path,f)
#    with open(manual_all,'w') as f:
#        f.write(cmd1)


if len(manual_jobs) > 2000:
    cmd1 = '#!/bin/bash\n'
    for f in manual_jobs[:999]:
        cmd1+= 'sbatch %s/%s/%s\n'%(pwd,jobs_path,f)
    with open(manual_all,'w') as f:
        f.write(cmd1)

    cmd2 =  '#!/bin/bash\n'
    for f in manual_jobs[999:1999]:
        cmd2+= 'sbatch %s/%s/%s\n'%(pwd,jobs_path,f)
    with open(manual_all.replace('.sh','_2.sh'), 'w') as f:
        f.write(cmd2)

    cmd3 =  '#!/bin/bash\n'
    for f in manual_jobs[1999:]:
        cmd3+= 'sbatch %s/%s/%s\n'%(pwd,jobs_path,f)
    with open(manual_all.replace('.sh','_3.sh'), 'w') as f:
        f.write(cmd3)



elif len(manual_jobs) > 1000 and len(manual_jobs) < 2000:
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
                       
