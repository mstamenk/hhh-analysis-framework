import sympy as sp
import ROOT
import numpy as np
import matplotlib.pyplot as plt


br = 0.5823
k_factor = 2.73
lumi = 137639.0
yield_table = {
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

cat_list = ['0bh3h','1bh2h','2bh1h','3bh0h']
for cat in cat_list:
    print(cat)
    path_for_histograms = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/run2/ProbHHH6b_%s_inclusive_CR/histograms"%(cat)
    var_list = ["h1_spanet_boosted_mass","h2_spanet_boosted_mass","h3_spanet_boosted_mass","ProbMultiH_regubin"]
    for var in  var_list:
        print(var)
        file = ROOT.TFile("%s/histograms_%s.root"%(path_for_histograms,var),"READ")
        for kappa_name in yield_table:                
            hist_kappa = file.Get(kappa_name)
            xs = eval(yield_table[kappa_name])*(br**3)*k_factor
            sum_weight = hist_kappa.Integral()
            # print(sum_weight)
            eff = sum_weight/(xs *lumi)

            print("{} : {:.6g}".format(kappa_name, eff))

        file.Close()


                




