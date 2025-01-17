import sympy as sp
import ROOT
from array import array
import numpy as np
import matplotlib.pyplot as plt
import re
from optparse import OptionParser
parser = OptionParser()

kl, kt, C2 = sp.symbols('kl kt C2')


cat_list = ["DY_multiDY","TT_multiTT","res1b_res1b","res2b_res2b"]
particle_list = ["eTau","muTau","tauTau"]
year_list = ["2016","2017","2018"]

type_list = ["alt","alt2","alt_BSM"]
for type in type_list:
    path_fit = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/fitdiagnose/bbtt/%s"%(type)
    path_plots = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/plots/bbtt/plots_%s_scale_fitbin_data"%(type)
    if type == "alt2":
        # path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/new_hist_alt2"
        path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbtt/new_hist_alt2_scale"
    else:
        # path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/new_hist_alt"
        path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbtt/new_hist_alt_scale"


    if type == "alt_BSM":
        file_fit = ROOT.TFile("%s/fitdiagnostics__unblinded__poi_r__params_r1.0_r_gghh1.0_r_qqhh0.0_kl-20.0_kt1.0_CV1.0_C2V1.0_C22.24__fromsnapshot.root"%(path_fit), "READ")
    else:
        file_fit = ROOT.TFile("%s/fitdiagnostics__unblinded__poi_r__params_r1.0_r_gghh1.0_r_qqhh1.0_kl-20.0_kt1.0_CV1.0_C2V1.0_C22.24__fromsnapshot.root"%(path_fit), "READ")




    for cat in cat_list:
        for par in particle_list:
            for year in year_list:

                dir_path = "shapes_prefit/%s_%s_%s"%(cat,par,year)
                if cat == "DY_multiDY":
                    cat_r = "classDY"
                elif cat == "TT_multiTT":
                    cat_r = "classTT"
                elif cat == "res1b_res1b":
                    cat_r = "res1b"
                elif cat == "res2b_res2b":
                    cat_r = "res2b"

                file_r = ROOT.TFile("%s/hh_%s_%s_%s_13TeV.input.root"%(path_r,cat_r,par,year), "READ")
                dic_fit = file_fit.Get(dir_path)

                if not dic_fit:
                    print(f"Directory {dir_path} not found in the file!")
                else:
                    hist_fit = dic_fit.Get("total_signal")

                    if not hist_fit:
                        print("Error: Could not find histogram in file_fit.")
                        print("shapes_prefit/%s_%s_%s in %s"%(cat,par,year,path_fit) )
                    
                hist_r = file_r.Get("ggHH_kl_m20p00_kt_1p00_c2_2p24_hbbhtt")
                if not hist_r:
                    print("Error: Could not find histogram in file_r.")
                    print("%s/hh_%s_%s_%s_13Tev.input.root"%(path_r,cat_r,par,year))

                print("%s/hh_%s_%s_%s_13TeV.input.root"%(path_r,cat_r,par,year))

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

                
                c1.SaveAs(f"{path_plots}/comparison_{cat}_{par}_{year}.pdf")

            file_r.Close()
                    
    file_fit.Close()
