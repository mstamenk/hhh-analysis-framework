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


def Unc_Shape(higgs1_path,higgs2_path,do_limit_input,Higgs_number):


    ROOT.gROOT.ProcessLine(".x /eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/shape_unc/lhcbStyle.C")
    
    # -------------------------------------------------------------- #
    # calculate corrected eff: 1D
    # -------------------------------------------------------------- #
  
    file_1Higgs = ROOT.TFile(higgs1_path)
    file_2Higgs = ROOT.TFile(higgs2_path)


    # ==== Readin original distributions
    Hist_Data_1Higgs = file_1Higgs.Get("data_obs").Clone()
    Hist_Data_1Higgs.SetName("Hist_Data_1Higgs")
    Hist_Data_2Higgs = file_2Higgs.Get("data_obs").Clone()
    Hist_Data_2Higgs.SetName("Hist_Data_2Higgs")

    Hist_BKG_1Higgs = file_1Higgs.Get("QCD_datadriven_data").Clone()
    Hist_BKG_1Higgs.SetName("Hist_BKG_1Higgs")
    Hist_BKG_2Higgs = file_2Higgs.Get("QCD_datadriven_data").Clone()
    Hist_BKG_2Higgs.SetName("Hist_BKG_2Higgs")


    # Hist_Data_1Higgs.Scale(1./Hist_Data_1Higgs.Integral())
    # Hist_Data_2Higgs.Scale(1./Hist_Data_2Higgs.Integral())
    # Hist_BKG_1Higgs.Scale(Hist_Data_1Higgs.Integral()/Hist_BKG_1Higgs.Integral())
    # Hist_BKG_2Higgs.Scale(Hist_Data_2Higgs.Integral()/Hist_BKG_2Higgs.Integral())
    
    # ==== Correction, Sigma_M (no correction), Sigma_P ( MC_2Higgs \times ratio^2 ) 
    file_save = ROOT.TFile(higgs2_path, "update")
    Hist_Corr_2Higgs = Hist_Data_2Higgs.Clone()
    Hist_Corr_2Higgs.SetName("QCD_datadriven_correct")
    Hist_Corr_2Higgs.SetTitle('QCD_datadriven_correct')

    
    Hist_Sigma_M_2Higgs = Hist_Data_2Higgs.Clone()
    Hist_Sigma_M_2Higgs.SetName("Hist_Sigma_M_2Higgs")

    Hist_Sigma_P_2Higgs = Hist_Data_2Higgs.Clone()
    Hist_Sigma_P_2Higgs.SetName("Hist_Sigma_P_2Higgs")

    list_sigma_M_2Higgs = []
    list_sigma_P_2Higgs = []
    list_corr_2Higgs    = []
    list_corr_M_2Higgs  = []
    list_corr_P_2Higgs  = []
    list_data           = []
    bin_Xaxis           = []

    Hist_Corr_2Higgs_M = Hist_Data_2Higgs.Clone()
    Hist_Corr_2Higgs_M.SetName("Hist_Corr_2Higgs_M")
    Hist_Corr_2Higgs_P = Hist_Data_2Higgs.Clone()
    Hist_Corr_2Higgs_P.SetName("Hist_Corr_2Higgs_P")

    #==== Fill hist

    for i in range(1, Hist_Data_1Higgs.GetNbinsX()+1):
        # read value and error
        data_1Higgs = Hist_Data_1Higgs.GetBinContent(i)
        data_2Higgs = Hist_Data_2Higgs.GetBinContent(i)
        list_data.append(data_2Higgs)
        qcd_1Higgs  = Hist_BKG_1Higgs.GetBinContent(i)
        qcd_2Higgs  = Hist_BKG_2Higgs.GetBinContent(i)

        e_data_1Higgs = Hist_Data_1Higgs.GetBinError(i)
        e_data_2Higgs = Hist_Data_2Higgs.GetBinError(i)
        e_qcd_1Higgs  = Hist_BKG_1Higgs.GetBinError(i)
        e_qcd_2Higgs  = Hist_BKG_2Higgs.GetBinError(i)

        # Correction : Hist_BKG_2Higgs * (Hist_Data_1Higgs / Hist_BKG_1Higgs)
        Corr_2Higgs = qcd_2Higgs * (data_1Higgs / qcd_1Higgs)
        Corr_err_2Higgs = Corr_2Higgs * np.sqrt(
                            (e_qcd_1Higgs / qcd_1Higgs)**2 + 
                            (e_qcd_2Higgs / qcd_2Higgs)**2 + 
                            (e_data_1Higgs / data_1Higgs)**2
                          )

        Hist_Corr_2Higgs.SetBinContent(i, Corr_2Higgs)
        Hist_Corr_2Higgs.SetBinError(i, Corr_err_2Higgs)
        
        bin_Xaxis.append(Hist_Data_1Higgs.GetBinCenter(i))
        list_corr_2Higgs.append(Corr_2Higgs)

        # Sigma_M : abs(Hist_Data_2Higgs - Hist_BKG_2Higgs) 
        sigma_M = -1. * ROOT.TMath.Abs(data_2Higgs - qcd_2Higgs)
        sigma_M_err = 0.
        Hist_Sigma_M_2Higgs.SetBinContent(i, sigma_M)
        Hist_Sigma_M_2Higgs.SetBinError(i, sigma_M_err)
        list_sigma_M_2Higgs.append(-1.* sigma_M)
        Hist_Corr_2Higgs_M.SetBinContent(i,Corr_2Higgs+ 1.* sigma_M)
        list_corr_M_2Higgs.append(Corr_2Higgs+ 1.* sigma_M)
        # list_corr_M_2Higgs.append(Hist_Corr_2Higgs_M_try.GetBinContent(i))
        
    
        # Sigma_P : Hist_BKG_2Higgs * ((Hist_Data_1Higgs / Hist_BKG_1Higgs))^2 
        sigma_P = 1. * Corr_2Higgs * (data_1Higgs / qcd_1Higgs)
        sigma_P_err = 0.
        Hist_Sigma_P_2Higgs.SetBinContent(i, sigma_P)
        Hist_Sigma_P_2Higgs.SetBinError(i, sigma_P_err)
        list_sigma_P_2Higgs.append(sigma_P)
        list_corr_P_2Higgs.append(Corr_2Higgs + sigma_P)
        # list_corr_P_2Higgs.append(Hist_Corr_2Higgs_P_try.GetBinContent(i))


        #####histograms#########
        Hist_Corr_2Higgs_M.SetBinContent(i,Corr_2Higgs+ 1.* sigma_M)
        Hist_Corr_2Higgs_P.SetBinContent(i,Corr_2Higgs + sigma_P)

        

    array_corr_2Higgs    = np.array(list_corr_2Higgs)
    array_sigma_M_2Higgs = np.array(list_sigma_M_2Higgs)
    array_sigma_P_2Higgs = np.array(list_sigma_P_2Higgs)
    array_corr_M_2Higgs  = np.array(list_corr_M_2Higgs)
    array_corr_P_2Higgs  = np.array(list_corr_P_2Higgs)
    array_bin_Xaxis      = np.array(bin_Xaxis)
    array_data           = np.array(list_data)

    #######write histograms##########
    f_out = ROOT.TFile(higgs2_path, 'update')
    print("Writing in %s" % higgs2_path)
    f_out.cd()
    Hist_Corr_2Higgs_M.SetTitle('QCD_datadriven_data_DataDriven_ShapeDown')
    Hist_Corr_2Higgs_M.SetName('QCD_datadriven_data_DataDriven_ShapeDown')
    Hist_Corr_2Higgs_P.SetTitle('QCD_datadriven_data_DataDriven_ShapeUp')
    Hist_Corr_2Higgs_P.SetName('QCD_datadriven_data_DataDriven_ShapeUp')

    # Hist_Corr_2Higgs_M.SetTitle('QCD_datadriven_correct_DataDriven_ShapeDown')
    # Hist_Corr_2Higgs_M.SetName('QCD_datadriven_correct_DataDriven_ShapeDown')
    # Hist_Corr_2Higgs_P.SetTitle('QCD_datadriven_correct_DataDriven_ShapeUp')
    # Hist_Corr_2Higgs_P.SetName('QCD_datadriven_correct_DataDriven_ShapeUp')
    Hist_Corr_2Higgs_M.Write()
    Hist_Corr_2Higgs_P.Write()
    f_out.Close()


    
    


    #==== Draw and save    
    ytitle   = "Arbitray scale"
    xtitle   = do_limit_input
    y_min = 0.0
    y_max = 0.35
    y_M_min = -0.05
    y_M_max = 0.25

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
    Hist_Data_2Higgs.SetYTitle(ytitle)
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
    leg.AddEntry(Hist_Data_2Higgs , "Data - 2 Higgs", "epl")
    leg.AddEntry(Hist_BKG_2Higgs , "BKG - 2 Higgs", "epl")    
    leg.AddEntry(Hist_Corr_2Higgs , "BKG_Corrected - 2Higgs", "epl")    
    Hist_Data_2Higgs.Draw()
    Hist_BKG_2Higgs.Draw("same")    
    Hist_Corr_2Higgs.Draw("same")    
    leg.Draw("same")

    ptext = ROOT.TPaveText(0.13, 0.58, 0.64, 0.86,"NDC")
    ptext.SetTextFont(132)
    ptext.AddText("#color[1]{Ratio (1 Higgs) = Data/BKG (1 Higgs) }")
    ptext.AddText("#color[4]{H_{Corr} (2 Higgs) = BKG (2 Higgs) #times Ratio (1 Higgs)}")
    ptext.AddText("#color[46]{Sigma_M (2 Higgs) = - | H_{Data} - H_{BKG} | (2 Higgs)}")
    ptext.AddText("#color[9]{Sigma_P (2 Higgs) = + H_{Corr} (2 Higgs) #times Ratio^{2} (1 Higgs)}")
    ptext.SetFillColor(ROOT.kWhite)
    ptext.SetTextAlign(11)
    ptext.Draw("same")

    cc.cd(2)
    gPad = cc.GetPad(2)
    gPad.SetTopMargin(0.05)
    gPad.SetBottomMargin(0.3)
    gPad.SetLeftMargin(0.12)
    gPad.SetRightMargin(0.07)
    gPad.SetPad(0.0,0.06,0.98,0.25)
  
    Hist_Sigma_P_2Higgs.SetXTitle("#scale[3.5]{#color[46]{Minus} / #color[9]{Plus} 1 Sigma}")
    Hist_Sigma_P_2Higgs.GetXaxis().SetTitleOffset(2.8)
    Hist_Sigma_P_2Higgs.SetLineColor(4)
    Hist_Sigma_P_2Higgs.SetFillColor(9)
    Hist_Sigma_P_2Higgs.SetLineWidth(2)
    Hist_Sigma_P_2Higgs.SetMarkerColor(4)
    Hist_Sigma_P_2Higgs.SetMarkerStyle(23)
    Hist_Sigma_P_2Higgs.SetAxisRange(y_M_min, y_M_max, "Y")
    Hist_Sigma_P_2Higgs.SetLabelSize(0.15,"X")
    Hist_Sigma_P_2Higgs.SetLabelSize(0.15,"Y")
    Hist_Sigma_M_2Higgs.SetLineColor(2)
    Hist_Sigma_M_2Higgs.SetFillColor(46)
    Hist_Sigma_P_2Higgs.Draw("hist")
    Hist_Sigma_M_2Higgs.Draw("hist && same")
    cc.SaveAs("Comp_2Higgs_correction.pdf")

    c2 = TCanvas( 'c2', 'A Simple Graph with error bars', 200, 10, 700, 500 )
    c2.SetGrid()
    c2.GetFrame().SetFillColor( 21 )
    
    c2.GetFrame().SetBorderSize( 12 )

    # array_corr_2Higgs    = np.array(list_corr_2Higgs)
    # array_sigma_M_2Higgs = np.array(list_sigma_M_2Higgs)
    # array_sigma_P_2Higgs = np.array(list_sigma_P_2Higgs)
    # array_corr_M_2Higgs  = np.array(list_corr_M_2Higgs)
    # array_corr_P_2Higgs  = np.array(list_corr_P_2Higgs)
    # array_bin_Xaxis      = np.array(bin_Xaxis)
    
    n   = Hist_Data_1Higgs.GetNbinsX()
    x   = array_bin_Xaxis
    exl = np.zeros(n)
    exh = np.zeros(n)
    y   = array_corr_2Higgs
    eyl = array_sigma_M_2Higgs
    eyh = array_sigma_P_2Higgs
    
    

    gr_Corr_2Higgs = TGraphAsymmErrors( n, x, y, exl, exh, eyl, eyh )
    # gr_Corr_2Higgs.SetTitle( 'TGraphErrors Example' )
    gr_Corr_2Higgs.GetXaxis().SetTitle(do_limit_input)
    gr_Corr_2Higgs.SetMarkerColor( 6 )
    gr_Corr_2Higgs.SetMarkerStyle( 21 )
    gr_Corr_2Higgs.Draw( 'ALP' )


    y_M = array_corr_M_2Higgs
    y_P = array_corr_P_2Higgs
    gr_Corr_M_2Higgs = TGraph(n,x,y_M)
    gr_Corr_M_2Higgs.SetLineColor(2)
    gr_Corr_M_2Higgs.SetLineWidth(2)
    gr_Corr_M_2Higgs.SetMarkerColor(2)
    gr_Corr_M_2Higgs.SetMarkerStyle(21)



    gr_Corr_P_2Higgs = TGraph(n,x,y_P)
    gr_Corr_P_2Higgs.SetLineColor(4)
    gr_Corr_P_2Higgs.SetLineWidth(2)
    gr_Corr_P_2Higgs.SetMarkerColor(4)
    gr_Corr_P_2Higgs.SetMarkerStyle(21)

    gr_data   = TGraph(n,x,array_data)
    gr_data.SetLineColor(8)
    gr_data.SetLineWidth(2)
    gr_data.SetMarkerColor(8)
    gr_data.SetMarkerStyle(21)

    gr_Corr_M_2Higgs.Draw("LP")

    gr_Corr_P_2Higgs.Draw("LP")
    gr_data.Draw("LP")
    

    leg2 = ROOT.TLegend(0.60, 0.725, 0.87, 0.925)
    leg2.AddEntry(gr_Corr_2Higgs   , "BKG_Corrected - {}".format(Higgs_number), "epl")
    leg2.AddEntry(gr_Corr_M_2Higgs , "BKG_Corrected_Down - {}".format(Higgs_number), "epl")    
    leg2.AddEntry(gr_Corr_P_2Higgs , "BKG_Corrected_Up - {}".format(Higgs_number), "epl")    
    leg2.AddEntry(gr_data , "data", "epl")    
    leg2.Draw("same")



    c2.SaveAs("Comp_{}_UP_DOWN.pdf".format(Higgs_number))

    file_save.Write()
    file_save.Close()


