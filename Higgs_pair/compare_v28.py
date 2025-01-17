import sympy as sp
import ROOT
from array import array
import numpy as np
import matplotlib.pyplot as plt
from utils import histograms_dict, hist_properties, addLabel_CMS_preliminary, luminosities
ROOT.gROOT.SetBatch(True)

path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v28/2018/boost_resolved/ProbHHH6b_0bh3h_inclusive_"
path_for_plots = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/plots/v28_compare"
# file_list = ["data_obs","QCD","GluGluToHHHTo6B_SM","GluGluToHHTo4B_cHHH1"]
file_list = ["GluGluToHHHTo6B_SM"]
var_list = ["h1","h2","h3","h"]
for file in file_list:
    file_open = ROOT.TFile("%s/%s_new.root"%(path,file), "READ")
    tree = file_open.Get("Events")
    for var in var_list:
        if var == "h":
            var_new = "%s_mass"%(var)
            var_original = "%s_fit_mass"%(var)
        else:
            var_new  = "%s_mass"%(var)
            var_original = "%s_t3_mass"%(var)   

        try :
            histograms_dict[var_new]
            histograms_dict[var_original]
        except :
            print("Will skip draw %s and %s, if you want to draw the should be added in utils" %(var_new,var_original))
            continue

        nbins = histograms_dict[var_new]["nbins"]
        xmin = histograms_dict[var_new]["xmin"]
        xmax = histograms_dict[var_new]["xmax"]
        hist_new = ROOT.TH1F(var_new,var_new,nbins,xmin,xmax)
        hist_original = ROOT.TH1F(var_original,var_original,nbins,xmin,xmax)

        
        tree.Draw(f"{var_new} >> {hist_new.GetName()}")  # 动态引用 var_new 变量
        tree.Draw(f"{var_original} >> {hist_original.GetName()}")  # 提取 branch_2 的数据并填充 hist_original

        canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)
        hist_new.SetLineColor(ROOT.kRed)  # 设置 hist_new 的线条颜色为红色
        hist_original.SetLineColor(ROOT.kBlue)  # 设置 hist_original 的线条颜色为蓝色

        all_max = max(hist_new.GetMaximum(), hist_original.GetMaximum())        
        hist_new.SetMaximum(all_max * 1.1)
        hist_new.SetStats(False)

        hist_new.Draw()  # 绘制 hist1（branch_1 的数据）
        hist_original.Draw("SAME")  # 绘制 hist2（branch_2 的数据），并在同一张图上叠加
        # hist_original.Draw()  # 绘制 hist1（branch_1 的数据）
        # hist_new.Draw("SAME")  # 绘制 hist2（branch_2 的数据），并在同一张图上叠加

        # 6. 添加图例（可选）
        legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
        legend.AddEntry(hist_new, "new chi2", "l")  # "l" 表示线条
        legend.AddEntry(hist_original, "original chi2", "l")  # "l" 表示线条
        legend.Draw()


        canvas.SaveAs("%s/comparison_%s_%s.pdf"%(path_for_plots,file,var))

    file_open.Close()
