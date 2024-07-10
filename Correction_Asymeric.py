import ROOT
import string
import vector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import array
from ROOT import TCanvas, TGraphErrors,TGraphAsymmErrors,TGraph
from ROOT import gROOT
from ROOT import Form


def code_for_plot(Hist_up,Hist_down,Hist_nom,pro,syst,path_for_plot):
    ROOT.gROOT.ProcessLine(".x /eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/shape_unc/lhcbStyle.C")

    xtitle   = 'ProbMultiH'
    y_max= Hist_up.GetMaximum()+0.2*Hist_up.GetMaximum()
    y_min = 0.0
    ROOT.gROOT.SetBatch(True)
    cc = ROOT.TCanvas("cc", "cc", 1000, 800)
    cc.SetTopMargin(0.1)
    cc.SetBottomMargin(0.1)
    cc.SetLeftMargin(0.12)
    cc.SetRightMargin(0.07)
    cc.SetPad(0.0,0.02,0.98,0.98)
    cc.SetGrid()
    Hist_nom.SetLineColor(1)
    Hist_nom.SetLineWidth(2)
    Hist_nom.SetMarkerColor(1)
    Hist_nom.SetMarkerStyle(23)
    Hist_nom.SetXTitle(xtitle)
    Hist_nom.GetXaxis().SetLabelSize(0.04)    
    Hist_nom.GetXaxis().SetTitleOffset(0.9)
    # Hist_nom.SetYTitle(ytitle)
    Hist_nom.SetAxisRange(y_min, y_max, "Y")
    Hist_nom.GetYaxis().SetLabelSize(0.04)

    Hist_up.SetLineColor(2)
    Hist_up.SetLineWidth(2)
    Hist_up.SetMarkerColor(2)
    Hist_up.SetMarkerStyle(23)

    Hist_down.SetLineColor(4)
    Hist_down.SetLineWidth(2)
    Hist_down.SetMarkerColor(4)
    Hist_down.SetMarkerStyle(23)

    leg = ROOT.TLegend(0.18, 0.67, 0.38, 0.87)
    leg.AddEntry(Hist_nom , "{}".format(pro), "epl")
    leg.AddEntry(Hist_up , "{}_{}_Up".format(pro,syst), "epl")    
    leg.AddEntry(Hist_down , "{}_{}_Down".format(pro,syst), "epl")   
    leg.SetTextSize(0.03) 
        
    Hist_nom.Draw()
    Hist_up.Draw("same")    
    Hist_down.Draw("same")    
    leg.Draw("same")


    cc.SaveAs("{}/UpDown_{}_{}.pdf".format(path_for_plot,pro,syst))




# path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/Marko_sample_1Higgs'
cat_list=  ["ProbHHH6b_2bh0h_inclusive_CR","ProbHHH6b_1bh1h_inclusive_CR","ProbHHH6b_0bh2h_inclusive_CR","ProbHHH6b_0bh0h_inclusive_CR","ProbHHH6b_3Higgs_inclusive_CR","ProbHHH6b_2Higgs_inclusive_CR","ProbHHH6b_1Higgs_inclusive_CR","ProbHHH6b_3bh0h_inclusive_CR","ProbHHH6b_2bh1h_inclusive_CR","ProbHHH6b_1bh2h_inclusive_CR","ProbHHH6b_0bh3h_inclusive_CR"]
pro_list = ["GluGluToHHHTo4B2Tau_SM","GluGluToHHHTo6B_SM","GluGluToHHTo4B_cHHH1"]
syst_list = ["PNetAK4_Stat","PNetAK4_FSR","PNetAK4_zjets_muF","PNetAK4_ISR","PNetAK4_ttbar_muR","PNetAK4_ttbar_muF","JES","PNetAK4_wjets_muR","PNetAK4_wjets_muF","JER","JMR","PileUp","l1Prefiring","PNetAK4_zjets_muR","PNetAK4_jetID","PNetAK4_wjets_c_xsec","PNetAK4_zjets_c_xsec"]
other_syst = ["MUR","MUF","PNetAK8","PNetAK4_zjets_b_xsec","FSR","ISR","PNetAK4_pileup","PNetAK4_wjets_b_xsec"]
year_list = ["2018","2017","2016_all"]
for year in year_list:

    path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new/%s'%(year)
    if year == '2016_all':
        year = '2016'


    for cat in cat_list:

        hist_path = path + '/' + cat + '/' + 'histograms/' +'histograms_ProbMultiH.root' 
        hist_path_corr = path + '/' + cat + '/' + 'histograms/' +'histograms_ProbMultiH_fixAsy.root'

        path_for_plot = path + '/' + cat + '/' + 'histograms/'


        file_o = ROOT.TFile(hist_path)
        Hist_Data = file_o.Get("data_obs").Clone()
        Hist_Data.SetName("data_obs"+ "_" + year)
        Hist_QCD = file_o.Get("QCD").Clone()
        Hist_QCD.SetName("QCD"+ "_" + year)
        Hist_4B2Tau = file_o.Get("GluGluToHHHTo4B2Tau_SM").Clone()
        Hist_4B2Tau.SetName("GluGluToHHHTo4B2Tau_SM"+ "_" + year)
        Hist_6b = file_o.Get("GluGluToHHHTo6B_SM").Clone()
        Hist_6b.SetName("GluGluToHHHTo6B_SM"+ "_" + year)
        Hist_4b = file_o.Get("GluGluToHHTo4B_cHHH1").Clone()
        Hist_4b.SetName("GluGluToHHTo4B_cHHH1"+ "_" + year)

        f_out = ROOT.TFile(hist_path_corr, 'recreate')
        Hist_Data.Write()
        Hist_4B2Tau.Write()
        Hist_6b.Write()
        Hist_4b.Write()
        Hist_QCD.Write()

        for pro in pro_list:
            for syst in syst_list:
                try:
                    Hist_nom = file_o.Get("%s"%(pro))
                except:
                    print("no %s"%pro)
                    continue

                Hist_up    = Hist_nom.Clone(Hist_nom.GetName() + "_" + year + '_' + syst + '_Up') # clone the histogram from nominal
                Hist_delta = Hist_nom.Clone(Hist_nom.GetName() + '_delta') # get the delta between nom and down
                # Hist_down  = file_o.Get("%s_%s_Down"%(pro,syst))
                Hist_down  = file_o.Get("%s_%s_Down"%(pro,syst))
                Hist_down.SetName(pro + "_" + year + '_' + syst + '_Down')
                if pro == "GluGluToHHHTo6B_SM" or pro == "GluGluToHHTo4B_cHHH1":
                    if syst in ["JES","JER","JMR"]:
                        Hist_down.SetName(pro + "_" + year + '_' + syst + '_'+ year + '_Down')
                        Hist_up.SetName(pro + "_" + year + '_' + syst + '_' + year + '_Up')
                if pro == "GluGluToHHHTo4B2Tau_SM":
                    if syst in ["JES","JER","JMR"]:
                        continue

                Hist_delta.Add(Hist_down,-1) # substracte nom - down
                Hist_up.Add(Hist_delta) # add difference to symmetrise
                # ==== Reading original distributions
                Hist_up.Write()
                Hist_down.Write()
                code_for_plot(Hist_up,Hist_down,Hist_nom,pro,syst,path_for_plot)
                
            for syst in other_syst:
                try:
                    Hist_nom = file_o.Get("%s"%(pro))
                except:
                    print("no %s"%pro)
                    continue

                Hist_up    = file_o.Get("%s_%s_Up"%(pro,syst))
                Hist_up.SetName(pro + "_" + year + '_' + syst + '_Up')
                 # clone the histogram from nominal
                Hist_down  = file_o.Get("%s_%s_Down"%(pro,syst))
                Hist_down.SetName(pro + "_" + year + '_' + syst + '_Down')

                Hist_up.Write()
                Hist_down.Write()
                code_for_plot(Hist_up,Hist_down,Hist_nom,pro,syst,path_for_plot)
            

        f_out.Close()


