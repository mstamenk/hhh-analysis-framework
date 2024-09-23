import ROOT
import shutil
import sys, os, re, shlex
import shutil,subprocess
import time
import os.path
from os import path
import gc

yield_table = {
    "ggHH_kl_1_kt_1"        : "0.031047",
    "ggHH_kl_0_kt_1"        : "0.069725",
    "ggHH_kl_5_kt_1"        : "0.091172",
    "c3_0_d4_0"             : "0.03274*1e-3",
    "c3_0_d4_99"            : "5.243*1e-3",
    "c3_0_d4_m1"            : "0.03624*1e-3",
    "c3_19_d4_19"           : "131.8*1e-3",
    "c3_1_d4_0"             : "0.02567*1e-3",
    "c3_1_d4_2"             : "0.01415*1e-3",
    "c3_2_d4_m1"            : "0.0511*1e-3",
    "c3_4_d4_9"             : "0.2182*1e-3",
    "c3_m1_d4_0"            : "0.1004*1e-3",
    "c3_m1_d4_m1"           : "0.09674*1e-3",
    "c3_m1p5_d4_m0p5"       : "0.1723*1e-3"
}

bsm_yield   = eval(yield_table["%s"%(sample)])

path_for_hist = "/eos/user/x/xgeng/workspace/HHH/CMSSW_11_3_4/src/datacards_maker_hhh/teste_datacards/v33/kappa_run2_scale/HHH_HH"
cat_list = ["3Higgs"]
sample_list = ["ggHH_kl_1_kt_1","ggHH_kl_0_kt_1","ggHH_kl_5_kt_1","c3_0_d4_0","c3_0_d4_99","c3_0_d4_m1","c3_19_d4_19","c3_1_d4_0","c3_1_d4_2","c3_2_d4_m1","c3_4_d4_9","c3_m1_d4_0","c3_m1_d4_m1","c3_m1p5_d4_m0p5"]
for cat in cat_list:
    file_kappa=ROOT.TFile("%s/histograms_ProbMultiHProbHHH6b_%s.root"%(path_for_hist,cat), "READ")
    diction_kappa = file_kappa.Get("HHH_kappa")
    for sample in sample_list:
        hist = diction_kappa.Get("%s"%(sample))
        integral = hist.Integral()
        xs = eval(yield_table["%s"%(sample)])



