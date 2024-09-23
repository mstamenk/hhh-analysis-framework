import ROOT
import string
# import vector
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import array
from ROOT import TCanvas, TGraphErrors,TGraphAsymmErrors,TGraph
from ROOT import gROOT
from ROOT import Form
path_for_plot = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/plots_addmva/v33"

# cat_list = ["3bh0h","2bh1h","1bh2h","0bh3h"]
cat_list = ["3Higgs"]
sample_list = ["GluGluToHHHTo6B_SM","data_obs","GluGluToHHTo4B_cHHH1","QCD"]

scale = 0

for cat in cat_list:

    xinyue_path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/run2/ProbHHH6b_%s_inclusive_CR/histograms"%(cat)
    Marko_path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/Marko_sample_1Higgs/ProbHHH6b_%s_inclusive_CR/histograms"%(cat)

    file_xinyue=ROOT.TFile("%s/histograms_kappa_scale.root"%(xinyue_path), "READ")
    file_Marko=ROOT.TFile("%s/histograms_ProbMultiH.root"%(Marko_path), "READ")
    for sample in sample_list:
        hist_xinyue = file_xinyue.Get("%s"%(sample))
        hist_Marko = file_Marko.Get("%s"%(sample))

        if scale:
            integral_x = hist_xinyue.Integral()
            integral_M = hist_Marko.Integral()
            hist_xinyue.Scale(1./integral_x)
            hist_Marko.Scale(1./integral_M)

        xtitle   = 'ProbMultiH'
        max_1 = hist_xinyue.GetMaximum()
        max_2 = hist_Marko.GetMaximum()
        y_max = max(max_1,max_2)*1.3
        y_min = 0.0
        ROOT.gROOT.SetBatch(True)
        cc = ROOT.TCanvas("cc", "cc", 1000, 800)
        cc.SetTopMargin(0.1)
        cc.SetBottomMargin(0.1)
        cc.SetLeftMargin(0.12)
        cc.SetRightMargin(0.07)
        cc.SetPad(0.0,0.02,0.98,0.98)
        cc.SetGrid()
        hist_xinyue.SetLineColor(1)
        hist_xinyue.SetLineWidth(2)
        hist_xinyue.SetMarkerColor(1)
        hist_xinyue.SetMarkerStyle(23)
        hist_xinyue.SetXTitle(xtitle)
        hist_xinyue.GetXaxis().SetLabelSize(0.04)    
        hist_xinyue.GetXaxis().SetTitleOffset(0.9)
        # hist_xinyue.SetYTitle(ytitle)
        hist_xinyue.SetAxisRange(y_min, y_max, "Y")
        hist_xinyue.GetYaxis().SetLabelSize(0.04)
        hist_xinyue.SetTitle("{}:{}".format(cat,sample))
        hist_xinyue.SetStats(0)

        hist_Marko.SetLineColor(2)
        hist_Marko.SetLineWidth(2)
        hist_Marko.SetMarkerColor(2)
        hist_Marko.SetMarkerStyle(23)
        hist_Marko.SetTitle("{}:{}".format(cat,sample))

        hist_Marko.SetStats(0)


        leg = ROOT.TLegend(0.60, 0.80, 0.999, 0.92)
        leg.AddEntry(hist_xinyue , "hist from xinyue", "epl")
        leg.AddEntry(hist_Marko , "hist from Marko", "epl")    
        leg.SetTextSize(0.03) 

        hist_xinyue.Draw()

        hist_Marko.Draw("same")    

        leg.Draw("same")

        if scale :
            cc.SaveAs("{}/Compare_{}_{}_scale.pdf".format(path_for_plot,cat,sample))

        else:
            cc.SaveAs("{}/Compare_{}_{}.pdf".format(path_for_plot,cat,sample))



