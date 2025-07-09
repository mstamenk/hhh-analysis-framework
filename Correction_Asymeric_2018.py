import ROOT
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
parser.add_argument('--path_hist_folder', type=str, required=True)
args = parser.parse_args()

path_hist_folder = args.path_hist_folder


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




# path_hist = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/Marko_sample_1Higgs'
# cat_list=  ["ProbHHH6b_2bh0h_inclusive_CR","ProbHHH6b_1bh1h_inclusive_CR","ProbHHH6b_0bh2h_inclusive_CR","ProbHHH6b_0bh0h_inclusive_CR","ProbHHH6b_1Higgs_inclusive_CR","ProbHHH6b_3bh0h_inclusive_CR","ProbHHH6b_2bh1h_inclusive_CR","ProbHHH6b_1bh2h_inclusive_CR","ProbHHH6b_0bh3h_inclusive_CR"]
# cat_list=  ["ProbHH4b_2bh0h_inclusive_CR","ProbHH4b_1bh1h_inclusive_CR","ProbHH4b_0bh2h_inclusive_CR","ProbHH4b_0bh0h_inclusive_CR","ProbHH4b_1Higgs_inclusive_CR","ProbHH4b_3bh0h_inclusive_CR","ProbHH4b_2bh1h_inclusive_CR","ProbHH4b_1bh2h_inclusive_CR","ProbHH4b_0bh3h_inclusive_CR","ProbHHH6b_2bh0h_inclusive_CR","ProbHHH6b_1bh1h_inclusive_CR","ProbHHH6b_0bh2h_inclusive_CR","ProbHHH6b_0bh0h_inclusive_CR","ProbHHH6b_1Higgs_inclusive_CR","ProbHHH6b_3bh0h_inclusive_CR","ProbHHH6b_2bh1h_inclusive_CR","ProbHHH6b_1bh2h_inclusive_CR","ProbHHH6b_0bh3h_inclusive_CR"]


cat_list=  ["ProbHHH6b_2bh0h_inclusive_CR","ProbHHH6b_1bh1h_inclusive_CR","ProbHHH6b_0bh2h_inclusive_CR","ProbHHH6b_0bh0h_inclusive_CR","ProbHHH6b_1Higgs_inclusive_CR","ProbHHH6b_1bh0h_inclusive_CR","ProbHHH6b_0bh1h_inclusive_CR","ProbHHH6b_3bh0h_inclusive_CR","ProbHHH6b_2bh1h_inclusive_CR","ProbHHH6b_1bh2h_inclusive_CR","ProbHHH6b_0bh3h_inclusive_CR"]
# cat_list=  ["ProbHHH6b_0bh1h_inclusive_CR","ProbHHH6b_1bh0h_inclusive_CR"]

# cat_list=  ["ProbHH4b_2bh0h_inclusive_CR","ProbHH4b_1bh1h_inclusive_CR","ProbHH4b_0bh2h_inclusive_CR","ProbHH4b_0bh0h_inclusive_CR","ProbHH4b_1Higgs_inclusive_CR","ProbHH4b_3bh0h_inclusive_CR","ProbHH4b_2bh1h_inclusive_CR","ProbHH4b_1bh2h_inclusive_CR","ProbHH4b_0bh3h_inclusive_CR"]
# cat_list=  ["ProbHHH6b_2bh0h_inclusive_CR","ProbHHH6b_1bh1h_inclusive_CR","ProbHHH6b_0bh2h_inclusive_CR"]
pro_list = ["GluGluToHHHTo6B_SM","GluGluToHHTo4B_cHHH1"]
syst_list = ["PNetAK4_Stat","PNetAK4_FSR","PNetAK4_zjets_muF","PNetAK4_ISR","PNetAK4_ttbar_muR","PNetAK4_ttbar_muF","PNetAK4_wjets_muR","PNetAK4_wjets_muF","PileUp","l1Prefiring","PNetAK4_zjets_muR","PNetAK4_jetID","PNetAK4_wjets_c_xsec","PNetAK4_zjets_c_xsec","JES","JER","JMR"]
other_syst = ["MUR","MUF","PNetAK8","PNetAK4_zjets_b_xsec","FSR","ISR","PNetAK4_pileup","PNetAK4_wjets_b_xsec"]
year_list = ["2018","2017","2016_all"]
# year_list = ["2018"]
for year in year_list:

    # path_hist = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new/%s'%(year)
    # path_hist = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/cat_new_boosted_prio/%s'%(year)
    # path_hist = '/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34_AN_HHH6b/%s'%(year)
    path_hist = '%s/%s'%(path_hist_folder,year)
    

    # path_hist = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new/run2'

    if year == '2016_all':
        year = '2016'


    for cat in cat_list:

        hist_path = path_hist + '/' + cat + '/' + 'histograms/' +'histograms_ProbMultiH.root' 
        if not path.exists(hist_path):
            print(f"[SKIP] Missing input file: {hist_path}, skipping category {cat} for year {year}")
            continue  # skip 当前cat，进入下一个cat循环
        # hist_path = path_hist + '/' + cat + '/' + 'histograms/' +'histograms_ProbMultiH_v34.root' 
        hist_path_corr = path_hist + '/' + cat + '/' + 'histograms/' +'histograms_ProbMultiH_fixAsy.root'

        path_for_plot = path_hist + '/' + cat + '/' + 'plots/'
        if not path.exists(path_for_plot) :
            procs=subprocess.Popen(['mkdir %s' % path_for_plot],shell=True,stdout=subprocess.PIPE)
            out = procs.stdout.read()
            print("made directory %s" % path_for_plot)


        file_o = ROOT.TFile(hist_path)
        Hist_Data_ptr = file_o.Get("data_obs")
        if not Hist_Data_ptr or not isinstance(Hist_Data_ptr, ROOT.TH1):
            print(f"[WARN] Missing 'data_obs' in {hist_path}, skipping category {cat}, year {year}")
            continue
        Hist_Data_o = file_o.Get("data_obs").Clone()
        Hist_Data_o.SetName("data_obs")
        Hist_Data = file_o.Get("data_obs").Clone()
        Hist_Data.SetName("data_obs"+ "_" + year)
        Hist_QCD_o = file_o.Get("QCD").Clone()
        Hist_QCD_o.SetName("QCD")
        Hist_QCD = file_o.Get("QCD").Clone()
        Hist_QCD.SetName("QCD"+ "_" + year)
        # Hist_4B2Tau = file_o.Get("GluGluToHHHTo4B2Tau_SM").Clone()
        # Hist_4B2Tau.SetName("GluGluToHHHTo4B2Tau_SM" + "_" + year)
        

        Hist_6b = file_o.Get("GluGluToHHHTo6B_SM").Clone()
        Hist_6b.SetName("GluGluToHHHTo6B_SM"+ "_" + year)
        # Hist_4b = file_o.Get("GluGluToHHTo4B_cHHH1").Clone()
        # Hist_4b.SetName("GluGluToHHTo4B_cHHH1"+ "_" + year)
        Hist_4b = file_o.Get("GluGluToHHTo4B_cHHH1").Clone()
        Hist_4b.SetName("GluGluToHHTo4B_cHHH1" + "_" + year)


        f_out = ROOT.TFile(hist_path_corr, 'recreate')
        Hist_Data.Write()
        Hist_Data_o.Write()
        Hist_6b.Write()
        Hist_QCD_o.Write()
        # Hist_4B2Tau.Write()
        Hist_4b.Write()
        Hist_QCD.Write()

        for pro in pro_list:
            for syst in syst_list:
                try:
                    Hist_nom = file_o.Get("%s"%(pro))
                except:
                    print("no %s"%pro)
                    continue

                Hist_up    = Hist_nom.Clone(Hist_nom.GetName() + "_" + year + '_' + syst + '_Up') 
                Hist_delta = Hist_nom.Clone(Hist_nom.GetName() + '_delta') # get the delta between nom and down
                # Hist_down  = file_o.Get("%s_%s_Down"%(pro,syst))
                Hist_down  = file_o.Get("%s_%s_Down"%(pro,syst))
                print(f"Processing {pro}, {syst}, {year},{cat}")
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
                Hist_down  = file_o.Get("%s_%s_Down"%(pro,syst))

                if not Hist_up or not isinstance(Hist_up, ROOT.TH1):
                    print(f"[WARN] Missing Up variation: {pro}_{syst}_Up in {cat}, {year}")
                    continue
                if not Hist_down or not isinstance(Hist_down, ROOT.TH1):
                    print(f"[WARN] Missing Down variation: {pro}_{syst}_Down in {cat}, {year}")
                    continue
                Hist_up.SetName(pro + "_" + year + '_' + syst + '_Up')
                 # clone the histogram from nominal
                Hist_down.SetName(pro + "_" + year + '_' + syst + '_Down')

                Hist_up.Write()
                Hist_down.Write()
                code_for_plot(Hist_up,Hist_down,Hist_nom,pro,syst,path_for_plot)
            

        f_out.Close()


