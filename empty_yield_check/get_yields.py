import sympy as sp
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import json  # 导入 JSON 模块

br = 0.5823
k_factor = 2.73
lumi = 137639.0
yield_table = {
    "c3_0_d4_0": "0.03274*1e-3",
    "c3_0_d4_99": "5.243*1e-3",
    "c3_0_d4_m1": "0.03624*1e-3",
    "c3_19_d4_19": "131.8*1e-3",
    "c3_1_d4_0": "0.02567*1e-3",
    "c3_1_d4_2": "0.01415*1e-3",
    "c3_2_d4_m1": "0.0511*1e-3",
    "c3_4_d4_9": "0.2182*1e-3",
    "c3_m1_d4_0": "0.1004*1e-3",
    "c3_m1_d4_m1": "0.09674*1e-3",
    "c3_m1p5_d4_m0p5": "0.1723*1e-3"
}

yield_table = {
    "c3_m14_d4_m101", 
    "c3_m11_d4_99",  
    "c3_m5_d4_m21",
    "c3_m6_d4_29", 
    "c3_2_d4_m61", 
    "c3_7_d4_49", 
    "c3_7_d4_m21",  
    "c3_15_d4_m81",  
    "c3_0_d4_0"
#     "c3_2_d4_3",
#     "c3_2_d4_m1", 
#     "c3_19_d4_19", 
#     "c3_0_d4_m1",
#     "c3_0_d4_99",
#     "c3_19_d4_19",
#     "c3_1_d4_0",
#     "c3_4_d4_9",
#     "c3_m1_d4_0", 
#     "c3_m1_d4_m1",
#     "c3_m1p5_d4_m0p5",
#     "c3_0_d4_0"
}

cat_list = ['0bh3h', '1bh2h', '2bh1h', '3bh0h']
var_list = ["ProbMultiH_regubin"]

# result = {cat: {} for cat in cat_list}  # 创建一个空字典
# for kappa_name in yield_table:
result = {kappa_name: {} for kappa_name in yield_table}  # 创建一个空字典

for kappa_name in yield_table:
    for var in var_list:
        for cat in cat_list:
            path_for_histograms = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/run2/ProbHHH6b_%s_inclusive_CR/histograms" % (cat)
            # file = ROOT.TFile("%s/histograms_%s.root" % (path_for_histograms, var), "READ")
            # file = ROOT.TFile("%s/histograms_%s_reweight.root" % (path_for_histograms, var), "READ")
            # file = ROOT.TFile("%s/histograms_%s_scale_reweight.root" % (path_for_histograms, var), "READ")
            file = ROOT.TFile("%s/histograms_%s_scale2_reweight.root" % (path_for_histograms, var), "READ")

            hist_kappa = file.Get(kappa_name)
            yield_kappa = hist_kappa.Integral()

            if cat not in result[kappa_name]:
                result[kappa_name][cat] = {"nominal": {"run2": []}}

            result[kappa_name][cat]["nominal"]["run2"].append(yield_kappa)

        file.Close()

# 保存结果为 JSON 文件
with open('kappa_fix_reweight_new.json', 'w') as json_file:
    json.dump(result, json_file, indent=4)




