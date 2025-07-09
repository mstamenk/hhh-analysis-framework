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


def Unc_Shape(higgs1_path,higgs2_path,do_limit_input,path,Higgs_number,year):


    ROOT.gROOT.ProcessLine(".x /eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/shape_unc/lhcbStyle.C")
    
    # -------------------------------------------------------------- #
    # calculate corrected eff: 1D
    # -------------------------------------------------------------- #
  
    file_1Higgs = ROOT.TFile(higgs1_path)
    file_2Higgs = ROOT.TFile(higgs2_path)


    # ==== Reading original distributions
    Hist_Data_1Higgs = file_1Higgs.Get("data_obs").Clone()
    Hist_Data_1Higgs.SetName("Hist_Data_1Higgs")
    Hist_Data_2Higgs = file_2Higgs.Get("data_obs").Clone()
    Hist_Data_2Higgs.SetName("Hist_Data_2Higgs")

    Hist_BKG_1Higgs = file_1Higgs.Get("QCD").Clone()
    Hist_BKG_1Higgs.SetName("Hist_BKG_1Higgs")
    Hist_BKG_2Higgs = file_2Higgs.Get("QCD").Clone()
    Hist_BKG_2Higgs.SetName("Hist_BKG_2Higgs")
    bkg_max = Hist_BKG_2Higgs.GetMaximum()

    Hist_norm_BKG_1Higgs = Hist_BKG_1Higgs.Clone()
    Hist_norm_BKG_1Higgs.SetName("Hist_norm_BKG_1Higgs")
    Hist_norm_BKG_2Higgs = Hist_BKG_2Higgs.Clone()
    Hist_norm_BKG_2Higgs.SetName("Hist_norm_BKG_2Higgs")
    Hist_norm_BKG_1Higgs.Scale(1.0/Hist_BKG_1Higgs.Integral())
    Hist_norm_BKG_2Higgs.Scale(1.0/Hist_BKG_2Higgs.Integral())



    Hist_Corr_2Higgs = Hist_Data_2Higgs.Clone()
    Hist_Corr_2Higgs.SetName("QCD_correct")
    Hist_Corr_2Higgs.SetTitle('QCD_correct')


    Hist_ratio_bkg = Hist_Data_2Higgs.Clone()
    Hist_ratio_bkg.SetName("Hist_ratio_bkg")

    Hist_ratio_corr = Hist_Data_2Higgs.Clone()
    Hist_ratio_corr.SetName("Hist_ratio_corr")

    Hist_ratio = Hist_Data_2Higgs.Clone()
    Hist_ratio.SetName("Hist_ratio")

#######  Hist_Corr_2Higgs_M is histograms down
    Hist_Corr_2Higgs_M = Hist_Data_2Higgs.Clone()
    Hist_Corr_2Higgs_M.SetName("Hist_Corr_2Higgs_M")
    Hist_Corr_2Higgs_P = Hist_Data_2Higgs.Clone()
    Hist_Corr_2Higgs_P.SetName("Hist_Corr_2Higgs_P")

    #==== Fill hist

    for i in range(1, Hist_Data_1Higgs.GetNbinsX()+1):
        data_1Higgs     = Hist_Data_1Higgs.GetBinContent(i)
        data_2Higgs     = Hist_Data_2Higgs.GetBinContent(i)
        bkg_1Higgs      = Hist_BKG_1Higgs.GetBinContent(i)
        bkg_2Higgs      = Hist_BKG_2Higgs.GetBinContent(i)
        norm_bkg_1Higgs = Hist_norm_BKG_1Higgs.GetBinContent(i)
        norm_bkg_2Higgs = Hist_norm_BKG_2Higgs.GetBinContent(i)

        e_data_1Higgs     = Hist_Data_1Higgs.GetBinError(i)
        e_data_2Higgs     = Hist_Data_2Higgs.GetBinError(i)
        e_bkg_1Higgs      = Hist_BKG_1Higgs.GetBinError(i)
        e_bkg_2Higgs      = Hist_BKG_2Higgs.GetBinError(i)
        e_norm_bkg_1Higgs = Hist_norm_BKG_1Higgs.GetBinError(i)
        e_norm_bkg_2Higgs = Hist_norm_BKG_2Higgs.GetBinError(i)


        if abs(norm_bkg_2Higgs) < 1e-10:
            print(f"[WARN] Bin {i}: norm_bkg_2Higgs == 0 → skip this bin")
            Corr_2Higgs = 0.
        else:
            Corr_2Higgs = bkg_2Higgs * (norm_bkg_1Higgs / norm_bkg_2Higgs)



        # Corr_2Higgs = bkg_2Higgs * (norm_bkg_1Higgs / norm_bkg_2Higgs)

        Corr_err_2Higgs = abs(Corr_2Higgs - bkg_2Higgs)
        Hist_Corr_2Higgs.SetBinContent(i, Corr_2Higgs)
        Hist_Corr_2Higgs.SetBinError(i, 1.0*Corr_err_2Higgs)
        ratio = Corr_2Higgs / bkg_2Higgs if bkg_2Higgs != 0 else 0.

        Hist_ratio.SetBinContent(i, ratio)
        Hist_ratio.SetBinError(i, 0.)

        # Down variation
        sigma_M = -1.0 * Corr_err_2Higgs
        value_M = bkg_2Higgs + sigma_M
        if value_M < 0:
            Hist_Corr_2Higgs_M.SetBinContent(i, 0.000001)
            Corr_err_2Higgs = bkg_2Higgs - 0.0000001
        else:
            Hist_Corr_2Higgs_M.SetBinContent(i, value_M)
        Hist_Corr_2Higgs_M.SetBinError(i, 0.)

        # Up variation
        sigma_P = Corr_err_2Higgs
        value_P = bkg_2Higgs + sigma_P
        Hist_Corr_2Higgs_P.SetBinContent(i, value_P)
        Hist_Corr_2Higgs_P.SetBinError(i, 0.)

    f_out = ROOT.TFile(higgs2_path, 'update')
    print("Writing in %s" % higgs2_path)
    f_out.cd()
    f_out.Delete(Form("QCD_DataDriven_Shape_{}Down;1".format(Higgs_number)))
    f_out.Delete(Form("QCD_DataDriven_Shape_{}Up;1".format(Higgs_number)))
    f_out.Delete(Form("QCD_correct;1"))
    f_out.Delete(Form("QCD_DataDriven_Shape_Down;1"))
    f_out.Delete(Form("QCD_DataDriven_Shape_Up;1"))
    print("No datadriven_shape need to delete now")
    Hist_Corr_2Higgs_M.SetTitle('QCD_DataDriven_Shape_{}Down'.format(Higgs_number))
    Hist_Corr_2Higgs_M.SetName('QCD_DataDriven_Shape_{}Down'.format(Higgs_number))
    Hist_Corr_2Higgs_P.SetTitle('QCD_DataDriven_Shape_{}Up'.format(Higgs_number))
    Hist_Corr_2Higgs_P.SetName('QCD_DataDriven_Shape_{}Up'.format(Higgs_number))


    Hist_Corr_2Higgs_M.Write()
    Hist_Corr_2Higgs_P.Write()
    Hist_Corr_2Higgs.Write()
    f_out.Close()


    xtitle   = do_limit_input
    data_max        = Hist_Data_2Higgs.GetMaximum()
    correct_bkg_max = Hist_Corr_2Higgs.GetMaximum()
    y_max= max(data_max, bkg_max, correct_bkg_max)+20
    y_min = 0.0
    y_error_max_before = abs(Hist_ratio.GetMaximum()-1.0)
    y_error_min_before = abs(Hist_ratio.GetMinimum()-1.0)
    y_error_max = max(y_error_max_before,y_error_min_before)
    y_M_min = -1.0* y_error_max +1.0 -0.2
    y_M_max = 1.0*y_error_max + 1.0 +0.2
    ROOT.gROOT.SetBatch(True)

    cc = ROOT.TCanvas("cc", "cc", 1000, 800)
    cc.Divide(1,2,0,0,0) 

    cc.cd(1)
    gPad = cc.GetPad(1)
    gPad.SetTopMargin(0.1)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.12)
    gPad.SetRightMargin(0.07)
    gPad.SetPad(0.0,0.25,0.98,0.98)
    gPad.SetGrid()
    Hist_Data_2Higgs.SetLineColor(1)
    Hist_Data_2Higgs.SetLineWidth(2)
    Hist_Data_2Higgs.SetMarkerColor(1)
    Hist_Data_2Higgs.SetMarkerStyle(23)
    Hist_Data_2Higgs.SetXTitle(xtitle)
    Hist_Data_2Higgs.GetXaxis().SetLabelSize(0.04)    
    Hist_Data_2Higgs.GetXaxis().SetTitleOffset(0.9)
    Hist_Data_2Higgs.SetAxisRange(y_min, y_max, "Y")
    Hist_Data_2Higgs.GetYaxis().SetLabelSize(0.04)

    Hist_BKG_2Higgs.SetLineColor(2)
    Hist_BKG_2Higgs.SetLineWidth(2)
    Hist_BKG_2Higgs.SetMarkerColor(2)
    Hist_BKG_2Higgs.SetMarkerStyle(23)

    Hist_Corr_2Higgs.SetLineColor(4)
    Hist_Corr_2Higgs.SetLineWidth(2)
    Hist_Corr_2Higgs.SetMarkerColor(4)
    Hist_Corr_2Higgs.SetMarkerStyle(23)

    leg = ROOT.TLegend(0.65, 0.67, 0.92, 0.87)
    leg.AddEntry(Hist_Data_2Higgs , "Data - {}".format(Higgs_number), "epl")
    leg.AddEntry(Hist_BKG_2Higgs , "BKG - {}".format(Higgs_number), "epl")    
    leg.AddEntry(Hist_Corr_2Higgs , "BKG_Corrected - {}".format(Higgs_number), "epl")    
    leg.AddEntry(Hist_ratio , "corr_bkg/bkg (pad below)", "epl")    
      
    Hist_Data_2Higgs.Draw()
    Hist_BKG_2Higgs.Draw("same")    
    Hist_Corr_2Higgs.Draw("same")    
    leg.Draw("same")



    cc.cd(2)
    gPad = cc.GetPad(2)
    gPad.SetTopMargin(0.05)
    gPad.SetBottomMargin(0.3)
    gPad.SetLeftMargin(0.12)
    gPad.SetRightMargin(0.07)
    gPad.SetPad(0.0,0.06,0.98,0.25)
  
    

    Hist_ratio.SetLineColor(2)
    Hist_ratio.SetLineWidth(2)
    Hist_ratio.SetMarkerColor(2)
    Hist_ratio.SetMarkerStyle(23)
    Hist_ratio.SetAxisRange(y_M_min, y_M_max, "Y")
    Hist_ratio.SetLabelSize(0.15,"X")
    Hist_ratio.SetLabelSize(0.15,"Y")
    Hist_ratio.GetYaxis().SetNdivisions(505)
    Hist_ratio.Draw("hist")
    line = ROOT.TLine(0,1,10,1)
    line.SetLineColor(6)
    line.SetLineStyle(ROOT.kDashed)
    line.SetLineWidth(1)
    line.Draw("same")
    cc.SaveAs("{}/Comp_{}_{}_correction.pdf".format(path,Higgs_number,do_limit_input))





    

    c2 = ROOT.TCanvas("c2", "c2", 1000, 800)
    c2.Divide(1,2,0,0,0) 

    c2.cd(1)
    gPad = c2.GetPad(1)
    gPad.SetTopMargin(0.1)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.12)
    gPad.SetRightMargin(0.07)
    gPad.SetPad(0.0,0.25,0.98,0.98)
    gPad.SetGrid()
    Hist_BKG_2Higgs.SetLineColor(1)
    Hist_BKG_2Higgs.SetLineWidth(2)
    Hist_BKG_2Higgs.SetMarkerColor(1)
    Hist_BKG_2Higgs.SetMarkerStyle(23)
    Hist_BKG_2Higgs.SetXTitle(xtitle)
    Hist_BKG_2Higgs.GetXaxis().SetLabelSize(0.04)    
    Hist_BKG_2Higgs.GetXaxis().SetTitleOffset(0.9)
    Hist_BKG_2Higgs.SetAxisRange(y_min, y_max, "Y")
    Hist_BKG_2Higgs.GetYaxis().SetLabelSize(0.04)

    Hist_BKG_2Higgs.SetLineColor(2)
    Hist_BKG_2Higgs.SetLineWidth(2)
    Hist_BKG_2Higgs.SetMarkerColor(2)
    Hist_BKG_2Higgs.SetMarkerStyle(23)

    Hist_Corr_2Higgs_M.SetLineColor(861)
    Hist_Corr_2Higgs_M.SetLineWidth(2)
    Hist_Corr_2Higgs_M.SetMarkerColor(861)
    Hist_Corr_2Higgs_M.SetMarkerStyle(23)
    Hist_Corr_2Higgs_P.SetLineColor(800-3)
    Hist_Corr_2Higgs_P.SetLineWidth(2)
    Hist_Corr_2Higgs_P.SetMarkerColor(800-3)
    Hist_Corr_2Higgs_P.SetMarkerStyle(23)

    leg = ROOT.TLegend(0.65, 0.67, 0.92, 0.87)
    leg.AddEntry(Hist_Corr_2Higgs_P , "histogram_up", "epl")
    leg.AddEntry(Hist_BKG_2Higgs , "BKG - {}".format(Higgs_number), "epl")    
    leg.AddEntry(Hist_Corr_2Higgs_M , "histogram_down", "epl")    
    leg.AddEntry(Hist_ratio , "corr_bkg/bkg (pad below)", "epl")    
    Hist_BKG_2Higgs.Draw()
    Hist_Corr_2Higgs_P.Draw("same")
    Hist_Corr_2Higgs_M.Draw("same")    
    leg.Draw("same")



    c2.cd(2)
    gPad = c2.GetPad(2)
    gPad.SetTopMargin(0.05)
    gPad.SetBottomMargin(0.3)
    gPad.SetLeftMargin(0.12)
    gPad.SetRightMargin(0.07)
    gPad.SetPad(0.0,0.06,0.98,0.25)
  
    Hist_ratio.SetLineColor(2)
    Hist_ratio.SetLineWidth(2)
    Hist_ratio.SetMarkerColor(2)
    Hist_ratio.SetMarkerStyle(23)
    Hist_ratio.SetAxisRange(y_M_min, y_M_max, "Y")
    Hist_ratio.SetLabelSize(0.15,"X")
    Hist_ratio.SetLabelSize(0.15,"Y")
    Hist_ratio.GetYaxis().SetNdivisions(505)
    Hist_ratio.Draw("hist")
    line = ROOT.TLine(0,1,10,1)
    line.SetLineColor(6)
    line.SetLineStyle(ROOT.kDashed)
    line.SetLineWidth(1)
    line.Draw("same")
    c2.SaveAs("{}/UpDown_{}_{}_correction.pdf".format(path,Higgs_number,do_limit_input))

