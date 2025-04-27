import ROOT
from utils import  luminosities
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

# 定义类别及对应的颜色
# 定义数字类别与名称的对应关系
category_map = {1: '3bh0h', 2: '2bh1h', 3: '1bh2h', 4: '0bh3h'}
colors = {1: ROOT.kRed, 2: ROOT.kBlue, 3: ROOT.kGreen, 4: ROOT.kMagenta}

# 创建画布
canvas = ROOT.TCanvas("canvas", "mHHH Distribution", 800, 600)

# 创建空的列表存储直方图
histograms = []

xmin = 0
xmax = 1000
bin_width = 20
nbins = int((xmax - xmin) / bin_width)
max_value = 0   
var = 'hhh_mass1'
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
canvas.SetTitle("mHHH Distribution by Category")

# 设置图例
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
for num, category_name in category_map.items():
    legend.AddEntry(histograms[num-1].GetValue(), category_name, "l")
legend.SetBorderSize(0)
legend.Draw()

# 显示图形
canvas.SaveAs("output_mHHH_distribution.pdf")