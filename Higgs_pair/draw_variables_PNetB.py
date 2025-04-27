import ROOT
from utils import  luminosities,histograms_dict
#from utils import wps_years
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

# 打开 ROOT 文件
path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/categorization/2018"
file = ROOT.TFile("%s/GluGluToHHHTo6B_SM.root"%(path))

# 创建 RDataFrame
df = ROOT.RDataFrame("Events", file)
lumi = luminosities['2018']
cutWeight = '(%f * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF)'%(lumi)
df = df.Define('totalWeight', cutWeight)
# 遍历 jet1 到 jet10，创建 jetXPassBtag branch
for i in range(1, 11):  # 遍历 jet1 到 jet10
    # 定义变量名
    pnet_b_plus_c = f"jet{i}PNetBPlusC"
    pnet_b_vs_c = f"jet{i}PNetBVsC"
    pass_btag_branch = f"jet{i}PassBtag"

    # 添加新的 branch，判断是否满足 Btag 条件
    # df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.96) ? 1 : 0")
    # df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.70) ? 1 : 0")
    df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.40) ? 1 : 0")

# 对 fatJet1 创建 PassBtag branch
for i in range(1, 5):  # 遍历 fatJet1 到 fatJet4
    # 定义变量名
    pnet_xbb = f"fatJet{i}PNetXbb"
    pass_btag_branch = f"fatJet{i}PassBtag"

    # 添加新的 branch，判断是否满足 Btag 条件
    # df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.9734) ? 1 : 0")
    # df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.90) ? 1 : 0")
    df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.641) ? 1 : 0")


# 计算通过条件的 jet 和 fatJet 数量
df = df.Define('nJetsPassed', 'jet1PassBtag + jet2PassBtag + jet3PassBtag + jet4PassBtag + jet5PassBtag + jet6PassBtag + jet7PassBtag + jet8PassBtag + jet9PassBtag + jet10PassBtag')
df = df.Define('nFatJetsPassed', 'fatJet1PassBtag + fatJet2PassBtag + fatJet3PassBtag + fatJet4PassBtag')


# 定义类别及对应的颜色
category_map = {1: '3bh0h', 2: '2bh1h', 3: '1bh2h', 4: '0bh3h'}
colors = {1: ROOT.kRed, 2: ROOT.kBlue, 3: ROOT.kGreen, 4: ROOT.kMagenta}

# 定义需要绘制的变量
# variables = [f"jet{i}PNetBPlusC" for i in range(1, 11)] + \
            # [f"jet{i}PNetBVsC" for i in range(1, 11)] + \
            # [f"fatJet{i}PNetXbb" for i in range(1, 5)] + \
            # ["nJetsPassed", "nFatJetsPassed","hhh_mass1","hhh_mass2"]

# variables = ["nJetsPassed", "nFatJetsPassed"]

variables =[f"fatJet{i}PNetXbb" for i in range(1, 5)] 

# 创建画布
for var in variables:

    canvas = ROOT.TCanvas("canvas", "%s"%var, 800, 600)

    # 创建空的列表存储直方图
    histograms = []
    xmin = histograms_dict[var]["xmin"]
    xmax = histograms_dict[var]["xmax"]
    nbins = histograms_dict[var]["nbins"]
    max_value = 0   
    char_var = var
    # 遍历不同类别并绘制
    for category_id, category_name in category_map.items():
        color = colors[category_id]  # 从 colors 字典中获取对应的颜色
        print("category_id:", category_id)
        print("category_name:", category_name)
        print("color:", color)
        # 筛选数据并绘制直方图
        # hist = df.Filter(f"categorisation == {category_id}").Histo1D(('hhh_mass2','hhh_mass2',nbins,xmin,xmax),'hhh_mass2', 'totalWeight')
        hist = df.Filter(f"categorisation == {category_id}").Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'totalWeight')
        max_value = max(max_value, hist.GetMaximum())


        
        # 设置直方图的颜色
        hist.SetLineColor(color)
        
        # 将直方图加入到列表
        histograms.append(hist)

    # 绘制所有直方图
    histograms[0].SetMaximum(1.2 * max_value)
    histograms[0].SetStats(0)
    histograms[0].Draw()  

    # 绘制第一个直方图
    for hist in histograms[1:]:
        hist.Draw("SAME")  
        # 其他的直方图加在同一个画布上

    # 设置标题
    canvas.SetTitle("%s Distribution by Category"%(var))

    # 设置图例


    legend = ROOT.TLegend(0.85, 0.85, 0.99, 0.99)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)  # 缩小图例文字的大小
    legend.SetTextFont(42) 
    for num, category_name in category_map.items():
        legend.AddEntry(histograms[num-1].GetValue(), category_name, "l")
     # 设置图例字体
    legend.Draw()

    # 显示图形
    canvas.SaveAs("%s.pdf"%var)