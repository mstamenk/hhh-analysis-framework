


import ROOT
import string
import vector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import array
from ROOT import TCanvas, TGraphErrors,TGraphAsymmErrors,TGraph
from ROOT import gROOT
from ROOT import Form

cat_list = ["HHH6b_0bh0h","HHH6b_1Higgs","HHH6b_2Higgs","HHH6b_3Higgs",
            "HHH6b_3bh0h","HHH6b_2bh1h","HHH6b_1bh2h","HHH6b_0bh3h",
            "HHH6b_2bh0h","HHH6b_1bh1h","HHH6b_0bh2h"]

samples_BSM = ["GluGluToHHTo4B_cHHH0","ggHH_kl_0_kt_1","GluGluToHHTo4B_cHHH5","ggHH_kl_5_kt_1",'HHHTo6B_c3_0_d4_99',"c3_0_d4_99",'HHHTo6B_c3_0_d4_minus1',"c3_0_d4_m1",'HHHTo6B_c3_19_d4_19',"c3_19_d4_19",'HHHTo6B_c3_1_d4_0',"c3_1_d4_0",'HHHTo6B_c3_1_d4_2',"c3_1_d4_2",'HHHTo6B_c3_2_d4_minus1',"c3_2_d4_m1",'HHHTo6B_c3_4_d4_9',"c3_4_d4_9",'HHHTo6B_c3_minus1_d4_0',"c3_m1_d4_0",'HHHTo6B_c3_minus1_d4_minus1',"c3_m1_d4_m1",'HHHTo6B_c3_minus1p5_d4_minus0p5',"c3_m1p5_d4_m0p5"]
samples_SM  = ["GluGluToHHTo4B_cHHH1","data_obs","GluGluToHHHTo6B_SM","QCD"]
# samples_SM  = ["GluGluToHHTo4B_cHHH1","ggHH_kl_1_kt_1","data_obs","GluGluToHHHTo6B_SM","c3_0_d4_0","QCD"]
# sample_list = ["GluGluToHHHTo6B_SM","GluGluToHHTo4B_cHHH0", "GluGluToHHTo4B_cHHH1", "GluGluToHHTo4B_cHHH5","HHHTo6B_c3_0_d4_99","HHHTo6B_c3_0_d4_minus1","HHHTo6B_c3_19_d4_19","HHHTo6B_c3_1_d4_0","HHHTo6B_c3_1_d4_2","HHHTo6B_c3_2_d4_minus1","HHHTo6B_c3_4_d4_9","HHHTo6B_c3_minus1_d4_0","HHHTo6B_c3_minus1_d4_minus1","HHHTo6B_c3_minus1p5_d4_minus0p5"]
# sample_list = ["data_obs","QCD","GluGluToHHTo4B_cHHH1","GluGluToHHHTo6B_SM"]
path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/run2/ProbHHH6b_0bh0h_inclusive_CR/histograms/kappa"
path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/run2"
path_Marko = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/Marko_sample_1Higgs"
for cat in cat_list:
    file_original=ROOT.TFile("%s/Prob%s_inclusive_CR/histograms/histograms_kappa.root"%(path,cat), "READ")
    file_Marko=ROOT.TFile("%s/Prob%s_inclusive_CR/histograms/histograms_ProbMultiH_fixAsy.root"%(path_Marko,cat), "READ")
    file_new = ROOT.TFile("%s/Prob%s_inclusive_CR/histograms/histograms_kappa_scale_Marko.root"%(path,cat),"RECREATE")
    print("%s"%(cat))

    for sample in samples_BSM:
            
        hist_BSM = file_original.Get("%s"%(sample))
        # integral = hist_BSM.Integral()
        hist_BSM.Scale(2.65)
      


        hist_BSM.Write()

    for sample in samples_SM:
        # print("%s"%(sample))

        hist_SM = file_Marko.Get("%s"%(sample))
        if sample == "GluGluToHHTo4B_cHHH1":
            hist_clone = hist_SM.Clone("ggHH_kl_1_kt_1")
            hist_clone.Write()
        if sample == "GluGluToHHHTo6B_SM":
            hist_clone = hist_SM.Clone("c3_0_d4_0")
            hist_clone.Write()

        # file_new.cd()
        hist_SM.Write()

    file_new.Close()