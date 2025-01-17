import ROOT
import matplotlib.pyplot as plt
import sympy as sp
from optparse import OptionParser
parser = OptionParser()

k4, k3 = sp.symbols('k4 k3')
parser.add_option("--scale", action="store_true", dest="use_scale", help="BSM sample scale by 2.73...", default=False)

(options, args) = parser.parse_args()

use_scale      = options.use_scale 

# var_list = ["h1_spanet_boosted_mass","h2_spanet_boosted_mass","h3_spanet_boosted_mass","ProbMultiH_regubin"]
var_list = ["kappa_scale"]
hist_list = ['c3_1_d4_2','c3_2_d4_m1','c3_0_d4_m1','c3_0_d4_99','c3_19_d4_19','c3_1_d4_0','c3_4_d4_9','c3_m1_d4_0','c3_m1_d4_m1','c3_m1p5_d4_m0p5','c3_0_d4_0']
# hist_list = ['c3_0_d4_m1','c3_m1_d4_0']


cat_list = ['0bh3h','1bh2h','2bh1h','3bh0h']
# cat_list = ['0bh3h']
for cat in cat_list:
    path_o = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/run2/ProbHHH6b_%s_inclusive_CR/histograms"%(cat)
    path_plots = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/run2/ProbHHH6b_%s_inclusive_CR/plots"%(cat)
    # path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_11_3_4/src/datacards_maker_hhh/teste_datacards/v33/kappa_reweight/HHH_only"
    for var in var_list:
        if use_scale:
            # file_o = ROOT.TFile("%s/histograms_%s_scale.root"%(path_o,var), "READ")
            # file_r = ROOT.TFile("%s/histograms_%s_scale_reweight.root"%(path_o,var), "READ")
            file_o = ROOT.TFile("%s/histograms_%s_scale2.root"%(path_o,var), "READ")
            file_r = ROOT.TFile("%s/histograms_%s_scale2_reweight.root"%(path_o,var), "READ")
        else:
            file_o = ROOT.TFile("%s/histograms_%s.root"%(path_o,var), "READ")
            file_r = ROOT.TFile("%s/histograms_%s_reweight.root"%(path_o,var), "READ")



        print(file_o)
        print(file_r)
    # file_r = ROOT.TFile("%s/histograms_3Higgs_reweight.root"%(path_r), "READ")


        for hist_name in hist_list:
            hist_o = file_o.Get(hist_name)
            hist_r = file_r.Get(hist_name)  

            if not hist_o:
                print("Error: Could not find histogram in file_o.")
                print(file_o)
                print(hist_name)
            else : print("sucess!")
            if not hist_r:
                print("Error: Could not find histogram in file_r.")
                print(file_o)
                print(hist_name)


            # 启用误差计算
            if not hist_o.GetSumw2N():
                hist_o.Sumw2()
            if not hist_r.GetSumw2N():
                hist_r.Sumw2()
            # hist_o.Sumw2()
            # hist_r.Sumw2()

            # 创建主Canvas
            c1 = ROOT.TCanvas("c1", "Comparison of Histograms", 800, 800)

            # 创建两个TPad，一个用于原始直方图，另一个用于比值图
            pad1 = ROOT.TPad("pad1", "Pad for Histograms", 0, 0.3, 1, 1.0)
            pad1.SetBottomMargin(0.02)
            pad1.Draw()
            pad1.cd()

            # 绘制直方图
            hist_o.SetLineColor(ROOT.kRed)
            hist_r.SetLineColor(ROOT.kBlue)
            all_max = max(hist_o.GetMaximum(), hist_r.GetMaximum())
            all_min = min(hist_o.GetMinimum(), hist_r.GetMinimum())

            hist_o.SetMaximum(all_max * 1.1)
            hist_o.SetMinimum(all_min * 0.9)
            hist_o.SetStats(False)

            hist_o.Draw("E HIST")
            hist_r.Draw("E HIST SAME")

            # 创建图例
            if cat == '0bh3h':
                legend = ROOT.TLegend(0.7, 0.75, 0.9, 0.9)
            else :
                legend = ROOT.TLegend(0.15, 0.75, 0.35, 0.9)  # 调整图例位置
            legend.AddEntry(hist_o, "madgraph", "l")
            legend.AddEntry(hist_r, "reweight", "l")
            legend.Draw()

            # 返回主Canvas，创建下方的pad用于比值图
            c1.cd()

            pad2 = ROOT.TPad("pad2", "Pad for Ratio", 0, 0.05, 1, 0.25)
            pad2.SetTopMargin(0.03)
            pad2.SetBottomMargin(0.3)
            pad2.Draw()
            pad2.cd()

            # 计算比值并处理除零问题
            ratio = hist_o.Clone("ratio")
            ratio.SetLineColor(ROOT.kBlack)
            ratio.SetTitle("")
            for bin in range(1, ratio.GetNbinsX() + 1):
                if hist_r.GetBinContent(bin) == 0:
                    hist_r.SetBinContent(bin, 1e-6)  # 避免除零错误
            ratio.Divide(hist_r)
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
            if use_scale:
                ratio.SetMaximum(2.0)
            else: 
                ratio.SetMaximum(5.5)
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

            # 保存绘图结果
            if use_scale:
                c1.SaveAs(f"{path_plots}/hist_comparison_{hist_name}_{var}_scale2.pdf")
            else:
                c1.SaveAs(f"{path_plots}/hist_comparison_{hist_name}_{var}.pdf")

       
        file_o.Close()
        file_r.Close()
