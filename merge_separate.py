import ROOT
import os
import string
# import vector
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import array
import os.path
from os import path
from ROOT import TCanvas, TGraphErrors,TGraphAsymmErrors,TGraph
from ROOT import gROOT
from ROOT import Form
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path_hist', type=str, required=True)
args = parser.parse_args()

path_hist = args.path_hist
# 定义输入文件路径和输出文件路径
# path_hist = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34_final_marko"
cat_list=  ["ProbHHH6b_2bh0h_inclusive_CR","ProbHHH6b_1bh1h_inclusive_CR","ProbHHH6b_0bh2h_inclusive_CR","ProbHHH6b_0bh0h_inclusive_CR","ProbHHH6b_3bh0h_inclusive_CR","ProbHHH6b_2bh1h_inclusive_CR","ProbHHH6b_1bh2h_inclusive_CR","ProbHHH6b_0bh3h_inclusive_CR","ProbHHH6b_1bh0h_inclusive_CR","ProbHHH6b_0bh1h_inclusive_CR","ProbHHH6b_1Higgs_inclusive_CR"]
# cat_list=  ["ProbHHH6b_1bh0h_inclusive_CR","ProbHHH6b_0bh1h_inclusive_CR"]
# cat_list=  ["ProbHH4b_2bh0h_inclusive_CR","ProbHH4b_1bh1h_inclusive_CR","ProbHH4b_0bh2h_inclusive_CR","ProbHH4b_0bh0h_inclusive_CR","ProbHH4b_1Higgs_inclusive_CR","ProbHH4b_2Higgs_inclusive_CR","ProbHH4b_3Higgs_inclusive_CR","ProbHH4b_3bh0h_inclusive_CR","ProbHH4b_2bh1h_inclusive_CR","ProbHH4b_1bh2h_inclusive_CR","ProbHH4b_0bh3h_inclusive_CR"]
# cat_list=  ["ProbHH4b_2bh0h_inclusive_CR","ProbHH4b_1bh1h_inclusive_CR","ProbHH4b_0bh2h_inclusive_CR","ProbHH4b_0bh0h_inclusive_CR","ProbHH4b_1Higgs_inclusive_CR","ProbHH4b_3bh0h_inclusive_CR","ProbHH4b_2bh1h_inclusive_CR","ProbHH4b_1bh2h_inclusive_CR","ProbHH4b_0bh3h_inclusive_CR"]
# cat_list=  ["ProbHH4b_2Higgs_inclusive_CR"]
for cat in cat_list:
    # path_for_hist = "%s/%year/%s/histograms/histograms_ProbMultiH_fixAsy.root"%(path_hist,cat)
    input_files = [
        "%s/2016_all/%s/histograms/histograms_ProbMultiH_fixAsy.root"%(path_hist,cat),  # 替换为你的ROOT文件路径
        "%s/2017/%s/histograms/histograms_ProbMultiH_fixAsy.root"%(path_hist,cat),  # 替换为你的ROOT文件路径
        "%s/2018/%s/histograms/histograms_ProbMultiH_fixAsy.root"%(path_hist,cat)  # 替换为你的ROOT文件路径
    ]
    existing_input_files = []
    for file_name in input_files:
        if os.path.exists(file_name):
            existing_input_files.append(file_name)
        else:
            print(f"[SKIP] Missing input file: {file_name}")

    # 如果没有任何存在的文件，整个 cat 跳过
    if len(existing_input_files) == 0:
        print(f"[WARN] No valid input files found for {cat}, skipping this category.")
        continue
    outfolder = "%s/run2_separate"%(path_hist)
    if not path.exists(outfolder) :
        procs=subprocess.Popen(['mkdir %s' % outfolder],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % outfolder)
    outfolder1 = "%s/run2_separate/%s"%(path_hist,cat)
    if not path.exists(outfolder1) :
        procs=subprocess.Popen(['mkdir %s' % outfolder1],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % outfolder1)
    outfolder2 = "%s/run2_separate/%s/histograms"%(path_hist,cat)
    if not path.exists(outfolder2) :
        procs=subprocess.Popen(['mkdir %s' % outfolder2],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % outfolder2)
    output_file = "%s/run2_separate/%s/histograms/histograms_ProbMultiH_fixAsy.root"%(path_hist,cat)  # 替换为你的ROOT文件路径
    # 打开输出文件
    output_root = ROOT.TFile(output_file, "RECREATE")

    # 用于合并的直方图集合
    histograms_to_merge = {}

    # 遍历所有输入文件
    for file_name in input_files:
        # 打开输入文件
        input_root = ROOT.TFile(file_name, "READ")
        
        # 获取文件中的所有对象（假设是TH1类直方图）
        keys = input_root.GetListOfKeys()
        for key in keys:
            obj = key.ReadObj()
            if isinstance(obj, ROOT.TH1):  # 检查是否是直方图类型
                # 检查是否需要合并，例如名字以 "QCD" 开头
                if obj.GetName() == "QCD":
                    if "QCD" not in histograms_to_merge:
                        # 如果尚未创建合并的直方图，则复制第一个对象
                        histograms_to_merge["QCD"] = obj.Clone("QCD")
                        histograms_to_merge["QCD"].SetDirectory(0)  # 取消关联文件
                    else:
                        # 如果已存在，累加到合并直方图中
                        histograms_to_merge["QCD"].Add(obj)

                    
                elif  obj.GetName() == "data_obs":
                    output_root.cd()
                    # obj.Write()
                    if "data_obs" not in histograms_to_merge:
                        # 如果尚未创建合并的直方图，则复制第一个对象
                        histograms_to_merge["data_obs"] = obj.Clone("data_obs")
                        histograms_to_merge["data_obs"].SetDirectory(0)  # 取消关联文件
                    else:
                        # 如果已存在，累加到合并直方图中
                        histograms_to_merge["data_obs"].Add(obj)

                else:
                    # 如果不是需要合并的对象，则直接写入
                    output_root.cd()
                    obj.Write()
        
        # 关闭当前输入文件
        input_root.Close()

    # 将合并后的直方图写入输出文件
    for hist_name, hist in histograms_to_merge.items():
        output_root.cd()
        hist.Write()

    # 关闭输出文件
    output_root.Close()
    print(histograms_to_merge)

    print(f"All histograms have been written to {output_file}.")
