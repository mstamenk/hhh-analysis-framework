import sympy as sp
import ROOT
from array import array
import numpy as np
import matplotlib.pyplot as plt
import re
from optparse import OptionParser
ROOT.gROOT.SetBatch(True) 
parser = OptionParser()


kl, kt, C2 = sp.symbols('kl kt C2')


cat_list = ["GGFcateg1","GGFcateg1_1","GGFcateg2","GGFcateg2_1","VBFcateg1","VBFcateg1_1"]
sample_list = ["qqHH_CV_1_C2V_1_kl_2","qqHH_CV_1_C2V_1_kl_1","qqHH_CV_1_C2V_0_kl_1","qqHH_CV_1_C2V_2_kl_1","qqHH_CV_1p5_C2V_1_kl_1","qqHH_CV_1_C2V_1_kl_0"]
sample_dict = {
    "sample_kl" :["qqHH_CV_1_C2V_1_kl_2","qqHH_CV_1_C2V_1_kl_1","qqHH_CV_1_C2V_1_kl_0"],
    "sample_c" :["qqHH_CV_1_C2V_0_kl_1","qqHH_CV_1_C2V_2_kl_1","qqHH_CV_1p5_C2V_1_kl_1"]

}
color_list = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta, ROOT.kCyan]

path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/cards_histograms_original_4b"
path_plots = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/plots/VBF_comparison"

for cat in cat_list:

    file = ROOT.TFile("%s/outPlotter_%s.root"%(path,cat), "READ")

    if "_1" in cat:
        year_list = ["2017","2018"]
    else:
        year_list = ["2016"]

    

    for year in year_list:
        for sample_key in sample_dict:
            print("sample is")
            print(sample_key)
            sample_list = sample_dict[sample_key]
            canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)
            canvas.SetGrid()
            color_idx = 0

            legend = ROOT.TLegend(0.75, 0.77, 0.99, 0.99)  # 设置图例的位置，(x1, y1, x2, y2)
            legend.SetBorderSize(0)  # 设置图例无边框
            legend.SetFillStyle(0)  # 设置图例无填充背景
            legend.SetTextSize(0.02)  # 设置图例文本大小

            max_y_value = 0  # 记录最大Y值
            # max_y_kl = 0  # 记录最大Y值
            # max_y_c = 0  # 记录最大Y值

            for sample in sample_list:
                hist = file.Get("%s_%s_hbbhbb"%(sample,year))
                integral = hist.Integral()
                hist.Scale(1./integral)
                y_max = hist.GetMaximum()
                if y_max > max_y_value:
                    max_y_value = y_max

            # for sample in sample_c:
            #     hist = file.Get("%s_%s_hbbhbb"%(sample,year))
            #     integral = hist.Integral()
            #     hist.Scale(1./integral)
            #     y_max = hist.GetMaximum()
            #     if y_max > max_y_c:
            #         max_y_c = y_max

            for sample in sample_list:
                hist = file.Get("%s_%s_hbbhbb"%(sample,year))
                if not hist:
                    print("Error: Could not find histogram in %s/outPlotter_%s.root"%(path,cat))

                if sample == sample_list[0]:
                    hist.SetLineColor(color_list[color_idx])  # 设置颜色
                    hist.SetStats(0)
                    hist.SetLineWidth(2)  # 设置线宽
                    hist.SetMaximum(max_y_value * 1.3)
                    hist.SetMinimum(0)
                    hist.SetTitle(f"VBF comparison for {cat}{year}")
                    hist.Draw()  # 绘制第一个直方图
                    # 为图例添加项
                    legend.AddEntry(hist, sample, "l")  # "l" 表示线型
                else:
                    hist.SetLineColor(color_list[color_idx])  # 设置颜色
                    hist.SetLineWidth(2)  # 设置线宽
                    # integral = hist.Integral()
                    # hist.Scale(1./integral)
                    hist.Draw("same")  # 叠加绘制其余直方图
                    # 为图例添加项
                    legend.AddEntry(hist, sample, "l")  # "l" 表示线型
                color_idx += 1  
            

            legend.Draw()

            # 更新画布显示
            canvas.Update()

        # 保存图像（如果需要）
            if sample_key == "sample_kl":
                canvas.SaveAs("%s/shape_kl_%s_%s.png"%(path_plots,cat,year))
            else:
                canvas.SaveAs("%s/shape_c_%s_%s.png"%(path_plots,cat,year))




                