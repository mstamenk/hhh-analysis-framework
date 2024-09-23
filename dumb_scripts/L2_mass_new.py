import ROOT
import shutil
import sys, os, re, shlex
from Correction_new import Unc_Shape
from array import array
#from subprocess import Popen, PIPE
#ROOT.ROOT.EnableImplicitMT()
#os.environ["MKL_NUM_THREADS"] = "1"
#os.environ["OMP_NUM_THREADS"] = "1"
import shutil,subprocess
import time
import os.path
from os import path
#from root_numpy import tree2array, array2tree
#import numpy as np
#import pandas
import glob
import gc



import ROOT
from ROOT import RDF

getmax = '''
int get_max_eta(float h1_spanet_boosted_eta, float h2_spanet_boosted_eta, float h3_spanet_boosted_eta) {
    std::vector<float> etas = {h1_spanet_boosted_eta, h2_spanet_boosted_eta, h3_spanet_boosted_eta};

    auto it = std::max_element(etas.begin(), etas.end());
    int index = std::distance(etas.begin(), it);

    return index + 1;
}
'''

getmax_return_mass = '''
float get_max_return_mass(float h1_spanet_boosted_eta, float h1_spanet_boosted_mass, 
                          float h2_spanet_boosted_eta, float h2_spanet_boosted_mass, 
                          float h3_spanet_boosted_eta, float h3_spanet_boosted_mass) {
    if (h1_spanet_boosted_eta >= h2_spanet_boosted_eta && h1_spanet_boosted_eta >= h3_spanet_boosted_eta) {
        return h1_spanet_boosted_mass;
    } else if (h2_spanet_boosted_eta >= h1_spanet_boosted_eta && h2_spanet_boosted_eta >= h3_spanet_boosted_eta) {
        return h2_spanet_boosted_mass;
    } else {
        return h3_spanet_boosted_mass;
    }
}
'''
cut_list = {'ProbHHH6b_3bh0h_inclusive_CR' : 0.952,
            'ProbHHH6b_2bh1h_inclusive_CR' : 0.9825,
            'ProbHHH6b_1bh2h_inclusive_CR' : 0.981,
            'ProbHHH6b_0bh3h_inclusive_CR' : 0.9825,
            'ProbHHH6b_2bh0h_inclusive_CR' : 0.9825,
            'ProbHHH6b_1bh1h_inclusive_CR' : 0.983,
            'ProbHHH6b_0bh2h_inclusive_CR' : 0.9845,
            'ProbHHH6b_1Higgs_inclusive_CR': 0.9862, 
            'ProbHHH6b_0bh0h_inclusive_CR' : 0.982
}


ROOT.gInterpreter.Declare(getmax)
ROOT.gInterpreter.Declare(getmax_return_mass)

variables_list = ["totalWeight","max_eta", "h1_spanet_boosted_eta", "h1_spanet_boosted_mass", 
                     "h2_spanet_boosted_eta", "h2_spanet_boosted_mass", 
                     "h3_spanet_boosted_eta", "h3_spanet_boosted_mass","max_eta_Higgs_mass","ProbMultiH"]

# variables_to_save_vec = ROOT.std.vector('string')(variables_to_save)
path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new'
for era in ["2016","2016APV","2017","2018"]:
    # for cat in ['ProbHHH6b_2bh0h_inclusive_CR','ProbHHH6b_1bh1h_inclusive_CR','ProbHHH6b_0bh2h_inclusive_CR','ProbHHH6b_3bh0h_inclusive_CR','ProbHHH6b_2bh1h_inclusive_CR','ProbHHH6b_1bh2h_inclusive_CR','ProbHHH6b_0bh3h_inclusive_CR','ProbHHH6b_3Higgs_inclusive_CR','ProbHHH6b_2Higgs_inclusive_CR','ProbHHH6b_1Higgs_inclusive_CR','ProbHHH6b_0bh0h_inclusive_CR']:
    for cat in ['ProbHHH6b_2bh0h_inclusive_CR','ProbHHH6b_1bh1h_inclusive_CR','ProbHHH6b_0bh2h_inclusive_CR','ProbHHH6b_3bh0h_inclusive_CR','ProbHHH6b_2bh1h_inclusive_CR','ProbHHH6b_1bh2h_inclusive_CR','ProbHHH6b_0bh3h_inclusive_CR','ProbHHH6b_1Higgs_inclusive_CR','ProbHHH6b_0bh0h_inclusive_CR']:
        for sample in ["data_obs",'GluGluToHHTo4B_cHHH1','GluGluToHHTo2B2Tau_SM','GluGluToHHHTo4B2Tau_SM','GluGluToHHHTo6B_SM','QCD_datadriven']:
        # for sample in ['GluGluToHHTo2B2Tau_SM','GluGluToHHHTo4B2Tau_SM','GluGluToHHHTo6B_SM','QCD_datadriven']:
            proc = '%s/sample_cut/%s/%s/%s.root'%(path,era,cat,sample)
            df = ROOT.RDataFrame('Events', proc)
            
            try:
                # df = df.Define("max_eta", "get_max_eta(h1_spanet_boosted_eta, h2_spanet_boosted_eta, h3_spanet_boosted_eta)")
                df = df.Define("max_eta_Higgs_mass", "get_max_return_mass(h1_spanet_boosted_eta,h1_spanet_boosted_mass,h2_spanet_boosted_eta,h2_spanet_boosted_mass, h3_spanet_boosted_eta,h3_spanet_boosted_mass)")
            except:
                print("no %s"%proc)
                continue
            cut_before = df.Count().GetValue()

            cut_value = cut_list[cat]

            df_cut = df.Filter("ProbMultiH > %s"%cut_value )
            print("ProbMultiH > %s"%cut_value)

            cut_after = df_cut.Count().GetValue()
            

            output_file = '%s/sample_cut_slim/%s/%s/%s.root'%(path,era,cat,sample)
            output_folder1 = "{}/sample_cut_slim/{}/".format(path,era)
            if not os.path.exists(output_folder1) :
                procs=subprocess.Popen(['mkdir %s' % output_folder1],shell=True,stdout=subprocess.PIPE)
                out = procs.stdout.read()
                print("made directory %s" % output_folder1)

            output_folder2 = "{}/sample_cut_slim/{}/{}/".format(path,era,cat)
            if not os.path.exists(output_folder2) :
                procs=subprocess.Popen(['mkdir %s' % output_folder2],shell=True,stdout=subprocess.PIPE)
                out = procs.stdout.read()
                print("made directory %s" % output_folder2)

            variables_to_save = [str(el) for el in variables_list]

            df_cut.Snapshot('Events', output_file, variables_to_save)

            print(era,cat,sample, "aleady finished cut")
            print("cut before is %s, cut after is %s"%(cut_before,cut_after))



