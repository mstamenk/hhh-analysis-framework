import argparse
import yaml
import os
import time
import ROOT
import subprocess
import math
import glob
import sys
import shutil
from os import path
def check_jobs(path):
    files = glob.glob(path + '/*')
    ok = 0
    fail = 0
    run = 0
    running = []
    failed = []
    for f in files:
        with open(f,'r') as f_in:
            text = f_in.read()
        if 'Normal termination' in text:
            if 'return value 0' in text:
                ok += 1 
            else:
                fail += 1
                failed.append(f)
        else:
            run += 1
            running.append(f)
    return ok,fail,run,failed

def load_input(input_file):
    with open(input_file, 'r') as file:
        return yaml.safe_load(file)

def runCmd(cmd):
    print("Running command: %s" % cmd)    
    try:
        proc = subprocess.Popen(
            [cmd],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        return_code = proc.wait()
        if return_code == 0:
            print("%s running successfully" % cmd)
            return True
        else:
            print("%s failed" % cmd)
            return False
    except OSError as e:
        print("OSError:", e)
        return False

datas = {'2018' : 'JetHT', 
         '2017' : 'BTagCSV',
         '2016' : 'JetHT',
         '2016APV' : 'JetHT'}

config = load_input('config.yaml')
pwd = "/afs/cern.ch/user/x/xiangran/CMSSW_13_3_0/src/condor-unified/"

if not path.exists(config['outputdir']):
    procs=subprocess.Popen(['mkdir %s' % config['outputdir']],shell=True,stdout=subprocess.PIPE)
    out = procs.stdout.read()
if not path.exists(config['outputdir']+"/inclusive-weights/"):
    procs=subprocess.Popen(['mkdir %s' % config['outputdir']+"/inclusive-weights/"],shell=True,stdout=subprocess.PIPE)
    out = procs.stdout.read()
if not path.exists(config['outputdir']+"/temp/"):
    procs=subprocess.Popen(['mkdir %s' % config['outputdir']+"/temp/"],shell=True,stdout=subprocess.PIPE)
    out = procs.stdout.read()

apply_training = config['apply_training']
qcd_datadriven = config['qcd_datadriven']
datadriven_retrain = config['datadriven_retrain']
skimm_tree = config['skimm_tree']
apply_binning = config['apply_binning']
QCD_shapeUnc = config['QCD_shapeUnc']

if apply_training:
    script = config["scriptsdir"] + '/' + apply_training

    jobs_path = 'jobs'
    submit="Universe   = vanilla\nrequest_memory = 7900\nExecutable = %s\nArguments  = $(ClusterId) $(ProcId)\nLog        = log/job_%s_%s_%s.log\nOutput     = output/job_%s_%s_%s.out\nError      = error/job_%s_%s_%s.error\n+MaxRuntime = 24*60*60\nQueue 1"
    job_cmd = '#! /bin/bash\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\ncmsrel CMSSW_13_3_0\ncd CMSSW_13_3_0/src\ncmsenv\nulimit -s unlimited\nexport MYROOT=$(pwd)\nexport PYTHONPATH=$PYTHONPATH:$MYROOT \n%s'

    submit_all = 'submit_all.sh'
    manual_all = 'manual_run_all.sh'
    jobs = []
    manual_jobs = []
    path_to_samples = config['inputdir']+'/inclusive-weights/'
    for f_in in config['procstodo']:
        if "data_obs" in f_in:
            f_in = datas[config['year']]
        file = path_to_samples+'/' + f_in +".root"
        df = ROOT.RDataFrame("Events", file)
        batch_start = int(df.Count().GetValue()*config['remove_ratio'])
        entries = df.Count().GetValue()-batch_start
        n_batches = math.floor(float(entries)/config['batch_size'])
        for j in range(n_batches+1):
            filename = 'job_%s_%s_%d.sh'%(f_in,config['year'],j)
            cmd = 'python3 %s  -v %s --f_in %s --year %s --batch_size %d --batch_number %d --batch_start %d --inputdir %s --outputdir %s'%(script,config['version'],f_in,config['year'],config['batch_size'],j,batch_start,path_to_samples,config['outputdir']+"/temp/")

            print("Writing %s"%filename)
            with open(jobs_path + '/' + filename, 'w') as f:
                f.write(job_cmd%cmd)
            manual_jobs.append(filename)

            submit_file = 'submit_%s_%s_%s'%(f_in,config['year'],j)
            print('Writing %s/%s'%(jobs_path, submit_file))
            with open(jobs_path + '/' + submit_file, 'w') as f:
                f.write(submit%(jobs_path+'/'+filename,f_in,config['year'],j,f_in,config['year'],j,f_in,config['year'],j))
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
    
    runCmd("bash submit_all.sh")
    while True:
        ok, fail,run,failed = check_jobs(pwd + '/log')
        if run == 0:
            if fail == 0:
                print("ALL JOBS PASSED,starting to merge")
                for f_in in config["procstodo"]:
                    if "data_obs" in f_in:
                        f_in = datas[config['year']]
                    cmd = 'hadd  %s/%s.root %s/%s*.root' %(config['outputdir']+"/inclusive-weights/",f_in,config['outputdir']+"/temp/",f_in)
                    runCmd(cmd)
            else:
                print("Failed jobs:")
                for el in failed:
                    print(el)
                qcd_datadriven = False
            break
        print("Please wait 5 mins...")
        time.sleep(5 * 60)



if qcd_datadriven:
    script = config["scriptsdir"] + '/' + config['qcd_datadriven']
    cmd_resolved = 'python3 %s --year %s --version %s --type %s --path %s' %(script,config['year'],config['version'],"resolved",config['outputdir'])
    cmd_boosted = 'python3 %s --year %s --version %s --type %s --path %s' %(script,config['year'],config['version'],"boosted",config['outputdir'])
    resolved=runCmd(cmd_resolved)
    boosted=runCmd(cmd_boosted)
    if resolved and boosted :
        datadriven_retrain = True
    else:
        datadriven_retrain = False
        print("Datadriven model production failed, please check the logs.")

if datadriven_retrain:
    script = config["scriptsdir"] + '/' + config['datadriven_retrain']

    jobs_path = 'jobs'
    submit="Universe   = vanilla\nrequest_memory = 7900\nExecutable = %s\nArguments  = $(ClusterId) $(ProcId)\nLog        = log/job_%s_%s_%s.log\nOutput     = output/job_%s_%s_%s.out\nError      = error/job_%s_%s_%s.error\n+MaxRuntime = 24*60*60\nQueue 1"
    job_cmd = '#! /bin/bash\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\ncmsrel CMSSW_13_3_0\ncd CMSSW_13_3_0/src\ncmsenv\nulimit -s unlimited\nexport MYROOT=$(pwd)\nexport PYTHONPATH=$PYTHONPATH:$MYROOT \n%s'

    submit_all = 'submit_all.sh'
    manual_all = 'manual_run_all.sh'
    jobs = []
    manual_jobs = []
    path_to_samples = config['outputdir']
    for f_in in ["QCD_datadriven_resolved","QCD_datadriven_boosted"]:
        file = path_to_samples+'/' + f_in +".root"
        df = ROOT.RDataFrame("Events", file)
        batch_start = 0
        entries = df.Count().GetValue()
        n_batches = math.floor(float(entries)/config['batch_size'])
        for j in range(n_batches+1):
            filename = 'job_%s_%s_%d.sh'%(f_in,config['year'],j)
            cmd = 'python3 %s  -v %s --f_in %s --year %s --batch_size %d --batch_number %d --batch_start %d --inputdir %s --outputdir %s'%(script,config['version'],f_in,config['year'],config['batch_size'],j,batch_start,path_to_samples,config['outputdir']+"/temp/")

            print("Writing %s"%filename)
            with open(jobs_path + '/' + filename, 'w') as f:
                f.write(job_cmd%cmd)
            manual_jobs.append(filename)

            submit_file = 'submit_%s_%s_%s'%(f_in,config['year'],j)
            print('Writing %s/%s'%(jobs_path, submit_file))
            with open(jobs_path + '/' + submit_file, 'w') as f:
                f.write(submit%(jobs_path+'/'+filename,f_in,config['year'],j,f_in,config['year'],j,f_in,config['year'],j))
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
    
    cmd = 'bash submit_all.sh'
    runCmd(cmd)
    while True:
        ok, fail,run,failed = check_jobs(pwd + '/log')
        if run == 0:
            if fail == 0:
                print("ALL JOBS PASSED,starting to merge")
                cmd = 'hadd  %s/QCD_datadriven.root %s/QCD_datadriven*' %(config['outputdir']+"/inclusive-weights/",config['outputdir']+"/temp/")
                runCmd(cmd)
            else:
                print("Failed jobs:")
                for el in failed:
                    print(el)
                skimm_tree = False
            break
        print("Please wait 5 mins...")
        time.sleep(5 * 60)

if skimm_tree:
    script = config["scriptsdir"] + '/' + config['skimm_tree']
    for f_in in config["procstodo"]:
        cmd = 'python3 %s --base_folder %s --process %s --run_all_categories --do_CR' %(script,config['outputdir'],f_in)
        runCmd(cmd)
    if datadriven_retrain:
        f_in ='QCD_datadriven'
        cmd = 'python3 %s --base_folder %s --process %s --run_all_categories --do_CR' %(script,config['outputdir'],f_in)
        runCmd(cmd)

# if apply_binning:
#     script = config["scriptsdir"] + '/' + 'binning.py'
#     cmd = 'python3 %s --year %s --version %s --inputdir %s --outputdir %s' %(script,config['year'],config['version'],config['outputdir']+"/inclusive-weights/",config['outputdir'])
#     runCmd(cmd)
# if QCD_shapeUnc:
#     script = config["scriptsdir"] + '/' + 'QCD_shapeUnc.py'
#     cmd = 'python3 %s --year %s --version %s --inputdir %s --outputdir %s' %(script,config['year'],config['version'],config['outputdir']+"/inclusive-weights/",config['outputdir'])
#     runCmd(cmd)