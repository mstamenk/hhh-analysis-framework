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


# cat_list = ["GGFcateg1_2016","GGFcateg1_20172018","GGFcateg2_2016","GGFcateg2_20172018","VBFcateg1_2016","VBFcateg1_20172018"]
cat_list = ["GGFcateg1_2016","GGFcateg2_2016","VBFcateg1_2016"]
# cat_list = ["GGFcateg2_2016"]
# type_list = ["alt","alt2"]
type_list = ["alt"]
for type in type_list:
    path_fit = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/fitdiagnose/bbbb"
    path_plots = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/plots/bbbb/plots_%s_rebin"%(type)
    if type == "alt2":
        path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbbb/new_hist_alt2_rebin"
    else:
        path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbbb/new_hist_alt_rebin"

    file_fit = ROOT.TFile("%s/rebin_fitdiagnostics__unblinded__poi_r__params_r1.0_r_gghh1.0_r_qqhh0.0_kl-20.0_kt1.0_CV1.0_C2V1.0_C22.24__fromsnapshot.root"%(path_fit), "READ")

    for cat in cat_list:
        dir_path = "bbbb_%s"%(cat)
        if cat == "GGFcateg1_2016":
            cat_r = "GGFcateg1"
        elif cat == "GGFcateg1_20172018":
            cat_r = "GGFcateg1_1"
        elif cat == "GGFcateg2_2016":
            cat_r = "GGFcateg2"
        elif cat == "GGFcateg2_20172018":
            cat_r = "GGFcateg2_1"
        elif cat == "VBFcateg1_2016":
            cat_r = "VBFcateg1"
        elif cat == "VBFcateg1_20172018":
            cat_r = "VBFcateg1_1"
        
        if "_1" in cat_r:
            year_list = ["2017","2018"]
        else:
            year_list = ["2016"]

        file_r = ROOT.TFile("%s/outPlotter_%s.root"%(path_r,cat_r), "READ")
        dic_fit = file_fit.Get(dir_path)

        if not dic_fit:
            print(f"Directory {dir_path} not found in the file!")
        else:
            hist_fit = dic_fit.Get("total_signal_rebin")

            if not hist_fit:
                print("Error: Could not find histogram in file_fit.")
                print("shapes_prefit/bbbb_%s in %s"%(cat,path_fit) )
        

        if "2016" in cat:
            hist_r = file_r.Get("ggHH_kl_m20p00_kt_1p00_c2_2p24_2016_hbbhbb")
        else :
            hist_1 = file_r.Get("ggHH_kl_m20p00_kt_1p00_c2_2p24_2017_hbbhbb")
            hist_2 = file_r.Get("ggHH_kl_m20p00_kt_1p00_c2_2p24_2018_hbbhbb")
            hist_r = hist_1.Clone("ggHH_kl_m20p00_kt_1p00_c2_2p24_20172018_hbbhbb")
            hist_r.Add(hist_2)



        if not hist_r:
            print("Error: Could not find histogram in %s/outPlotter_%s.root"%(path_r,cat_r))

        print("%s/outPlotter_%s.root"%(path_r,cat_r))

        num_bins = hist_fit.GetNbinsX()
        bin_edges = [hist_fit.GetXaxis().GetBinLowEdge(i) for i in range(1, num_bins + 2)]  
        # 打印 bin 边界信息
        print("Bin edges:", bin_edges)

        fit_title = hist_fit.GetTitle()
        fit_xaixs_title = hist_fit.GetXaxis().GetTitle()


        # Step 2: 创建一个新的不均匀分 bin 直方图
        hist_target = ROOT.TH1F("hist_target", "Histogram with Non-Uniform Bins", num_bins, array('d', bin_edges))
        hist_target.SetTitle(fit_title)
        hist_target.GetXaxis().SetTitle(fit_xaixs_title)

        # Step 3: 将均匀分 bin 直方图的数据填充到不均匀分 bin 直方图
        for i in range(1, num_bins + 1):
            content = hist_r.GetBinContent(i)
            error = hist_r.GetBinError(i)
            hist_target.SetBinContent(i, content)
            hist_target.SetBinError(i, error)


        if not hist_target.GetSumw2N():
            hist_target.Sumw2()
        if not hist_fit.GetSumw2N():
            hist_fit.Sumw2()


        c1 = ROOT.TCanvas("c1", "Comparison of Histograms", 800, 800)

        pad1 = ROOT.TPad("pad1", "Pad for Histograms", 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()

        # 绘制直方图
        x_min = hist_target.GetXaxis().GetXmin()
        x_max = hist_target.GetXaxis().GetXmax()
        hist_target.GetXaxis().SetRangeUser(x_min, x_max)
        hist_target.GetXaxis().SetRangeUser(x_min, x_max)

        hist_fit.SetLineColor(ROOT.kRed)
        hist_target.SetLineColor(ROOT.kBlue)
        all_max = max(hist_target.GetMaximum(), hist_fit.GetMaximum())
        all_min = min(hist_target.GetMinimum(), hist_fit.GetMinimum())
        

        hist_target.SetMaximum(all_max * 1.1)
        hist_target.SetMinimum(all_min - 0.5 )
        hist_target.SetStats(False)

        # hist_target.Draw("E HIST")
        # hist_r.Draw("E HIST SAME")
        hist_target.Draw("HIST")
        hist_fit.Draw("HIST SAME")
        line_zero_pad1 = ROOT.TLine(hist_target.GetXaxis().GetXmin(), 0, hist_target.GetXaxis().GetXmax(), 0)
        line_zero_pad1.SetLineColor(ROOT.kBlack)
        line_zero_pad1.SetLineStyle(2)
        line_zero_pad1.Draw()

        # 创建图例
    
        legend = ROOT.TLegend(0.85, 0.85, 0.99, 0.99)
        legend.AddEntry(hist_target,"reweight" , "l")
        legend.AddEntry(hist_fit,"fit", "l")
        legend.Draw()

        c1.cd()

        pad2 = ROOT.TPad("pad2", "Pad for Ratio", 0, 0.05, 1, 0.25)
        pad2.SetTopMargin(0.05)
        pad2.SetBottomMargin(0.3)
        pad2.Draw()
        pad2.cd()

        # 计算比值并处理除零问题
        ratio = hist_target.Clone("ratio")
        ratio.SetLineColor(ROOT.kBlack)
        ratio.SetTitle("")
        for bin in range(1, ratio.GetNbinsX() + 1):
            if hist_fit.GetBinContent(bin) == 0:
                hist_fit.SetBinContent(bin, 1e-6)  # 避免除零错误
        ratio.Divide(hist_fit)
        ratio.SetStats(0)

        ratio.GetYaxis().SetTitle("Ratio")
        ratio.GetYaxis().SetNdivisions(505)
        ratio.GetYaxis().SetTitleSize(20)
        ratio.GetYaxis().SetTitleFont(43)
        ratio.GetYaxis().SetTitleOffset(1.55)
        ratio.GetYaxis().SetLabelFont(43)
        ratio.GetYaxis().SetLabelSize(15)

        ratio.GetXaxis().SetTitleSize(20)
        ratio.GetXaxis().SetTitleFont(43)
        ratio.GetXaxis().SetTitleOffset(4.0)
        ratio.GetXaxis().SetLabelFont(43)
        ratio.GetXaxis().SetLabelSize(15) 
        ratio.SetMaximum(2.0)
        ratio.SetMinimum(0.0)

        ratio.Draw("E")

        # 绘制 y = 1 的参考线
        line = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1)
        line.SetLineColor(ROOT.kRed)
        line.SetLineStyle(2)
        line.Draw()

        # 返回主Canvas，更新绘图
        c1.Update()
        c1.Draw()

        
        c1.SaveAs(f"{path_plots}/comparison_{cat}.pdf")

        file_r.Close()
            
    file_fit.Close()
