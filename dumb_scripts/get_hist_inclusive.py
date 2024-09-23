import ROOT
import shutil
import sys, os, re, shlex
from Correction_new import Unc_Shape
from array import array
import time
import os.path
from os import path
import glob
import gc

# 定义要处理的过程
procstodo = ["GluGluToHHTo4B_cHHH1", "data_obs", "GluGluToHHHTo6B_SM", "QCD_datadriven", 
             "GluGluToHHHTo4B2Tau_SM", "GluGluToHHTo2B2Tau_SM", "HHHTo6B_c3_0_d4_99", 
             "HHHTo6B_c3_0_d4_minus1", "HHHTo6B_c3_19_d4_19", "HHHTo6B_c3_1_d4_0", 
             "HHHTo6B_c3_1_d4_2", "HHHTo6B_c3_2_d4_minus1", "HHHTo6B_c3_4_d4_9", 
             "HHHTo6B_c3_minus1_d4_0", "HHHTo6B_c3_minus1_d4_minus1", "HHHTo6B_c3_minus1p5_d4_minus0p5"]

procskappa = ["HHHTo6B_c3_0_d4_99", "HHHTo6B_c3_0_d4_minus1", "HHHTo6B_c3_19_d4_19", 
              "HHHTo6B_c3_1_d4_0", "HHHTo6B_c3_1_d4_2", "HHHTo6B_c3_2_d4_minus1", 
              "HHHTo6B_c3_4_d4_9", "HHHTo6B_c3_minus1_d4_0", "HHHTo6B_c3_minus1_d4_minus1", 
              "HHHTo6B_c3_minus1p5_d4_minus0p5"]

output_dict = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/inclusive"

year_list = ["2018","2017","2016","2016APV"]
var_list = ["h1_spanet_boosted_mass","h2_spanet_boosted_mass","h3_spanet_boosted_mass"]

# 定义不同年份的亮度
luminosities = {
    '2016APV': 19207.0,
    '2016PostAPV': 17122.0,
    '2016': 17122.0,
    '2017': 41480.0,
    '2018': 59830.0,
    'run2': 137639.0
}

inputTree = 'Events'
for year in year_list:
    output_tree = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights/"%year
    output_tree_kappa = "/eos/cms/store/group/phys_higgs/cmshhh/v33-additional-samples/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights/"%year

    proctodo = "GluGluToHHHTo6B_SM"  # 初始过程
    outtree = f"{output_tree}/{proctodo}.root"
    chunk_df = ROOT.RDataFrame(inputTree, outtree)
    
    for var in var_list:  # 定义变量范围
        nbins = 30
        xmin = 0
        xmax = 300

        nameout = f"{output_dict}/{year}/histograms_{var}.root"
        f_out = ROOT.TFile(nameout, 'recreate')
        print(f"Writing in {nameout}")

        f_out.cd()
        
        for proctodo in procstodo:
            print(proctodo)

            # 获取列名，检查权重变量是否存在
            variables = chunk_df.GetColumnNames()
            required_vars = ['xsecWeight', 'l1PreFiringWeight', 'puWeight', 'genWeight', 'triggerSF']
            missing_vars = [var for var in required_vars if var not in variables]
            
            if missing_vars:
                print(f"Warning: Variables {missing_vars} are missing in {proctodo}")
            
            if proctodo == "data_obs":
                if year in ['2018', '2016', '2016APV']:
                    proctodo = 'JetHT'
                else:
                    proctodo = 'BTagCSV'

                datahist = 'data_obs'
            else: datahist = 'other'

            # 对于 Kappa 相关的过程，调整输出路径
            if proctodo in procskappa:
                outtree = f"{output_tree_kappa}/{proctodo}.root"
            else:
                outtree = f"{output_tree}/{proctodo}.root"

            try:
                chunk_df = ROOT.RDataFrame(inputTree, outtree)
            except Exception as e:
                print(f"Process {proctodo} has 0 entries, skipping histogram creation. Error: {e}")
                continue

            lumi = luminosities[year]

            # 根据不同的数据集设置不同的 cutWeight
            if 'QCD_datadriven' in proctodo or 'JetHT' in proctodo or 'BTagCSV' in proctodo:
                cutWeight = '1'
            else:
                cutWeight = f"({lumi} * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF)"

            print("CutWeight expression: ", cutWeight)
            
            # 定义 totalWeight
            try:
                chunk_df = chunk_df.Define("totalWeight", cutWeight)
            except Exception as e:
                print(f"Error defining totalWeight for {proctodo}: {e}")
                continue

            # 生成直方图
            char_var = var
            if proctodo == "HHHTo6B_c3_0_d4_minus1":
                proctodo = "c3_0_d4_m1"
            elif proctodo == "HHHTo6B_c3_19_d4_19":
                    proctodo = "c3_19_d4_19"
            elif proctodo == "HHHTo6B_c3_1_d4_0":
                    proctodo = "c3_1_d4_0"
            elif proctodo == "HHHTo6B_c3_1_d4_2":
                    proctodo = "c3_1_d4_2"
            elif proctodo == "HHHTo6B_c3_2_d4_minus1":
                    proctodo = "c3_2_d4_m1"
            elif proctodo == "HHHTo6B_c3_4_d4_9":
                    proctodo = "c3_4_d4_9"
            elif proctodo == "HHHTo6B_c3_minus1_d4_0":
                    proctodo = "c3_m1_d4_0"
            elif proctodo == "HHHTo6B_c3_minus1_d4_minus1":
                    proctodo = "c3_m1_d4_m1"
            elif proctodo == "HHHTo6B_c3_minus1p5_d4_minus0p5":
                    proctodo = "c3_m1p5_d4_m0p5"
            elif proctodo == "HHHTo6B_c3_0_d4_99":
                    proctodo = "c3_0_d4_99"
            elif proctodo == "GluGluToHHHTo6B_SM":
                    proctodo = "c3_0_d4_0"

            try:
                h_tmp = chunk_df.Filter(f"{char_var} > {xmin}").Histo1D((char_var, char_var, nbins, xmin, xmax), char_var, 'totalWeight')
                f_out.cd()
                if datahist == "data_obs":
                    h_tmp.SetTitle('%s'%(data_obs))
                    h_tmp.SetName('%s'%(data_obs))

                h_tmp.SetTitle('%s'%(proctodo))
                h_tmp.SetName('%s'%(proctodo))
                h_tmp.Write()
            except Exception as e:
                print(f"Error processing {proctodo}: {e}")
                continue

            # 特定过程的处理
            if datahist == "data_obs":
                data_value = h_tmp.Integral()
                print(f"Data value: {data_value}")

            if proctodo == "QCD_datadriven":
                h_tmp.Scale(data_value / h_tmp.Integral())
                print(f"Scaled QCD, new integral: {h_tmp.Integral()}")

            # 处理其他过程
            scale_factors = {
                "c3_0_d4_m1": 2.73,
                "c3_19_d4_19": 2.73,
                "c3_1_d4_0": 2.73,
                "c3_1_d4_2": 2.73,
                "c3_2_d4_m1": 2.73,
                "c3_4_d4_9": 2.73,
                "c3_m1_d4_0": 2.73,
                "c3_m1_d4_m1": 2.73,
                "c3_m1p5_d4_m0p5": 2.73,
            }

            if proctodo in scale_factors:
                h_tmp.Scale(scale_factors[proctodo])
                print(f"Scaled {proctodo}, new integral: {h_tmp.Integral()}")
            
            

        f_out.Close()
        print(f"File {nameout} closed.")
