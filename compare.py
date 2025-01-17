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

year_list = ["2016","2016APV","2017","2018"]
cat = 
output_tree = //eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/compare/

for proctodo in procstodo :
    outtree = "{}/{}_{}/{}.root".format(output_tree,selection,additional_label,proctodo) ## make better, to not have to call it twice

    try :
        chunk_df = ROOT.RDataFrame(inputTree, outtree)
        # chunk_df.Filter("%s > %s"%(char_var,xmin))
    except :
        print("process %s has 0 entries, skipping doing the histogram" % proctodo)
        continue

    datahist = proctodo
    if proctodo == "data_obs" :
        if year == '2018' or year == '2016APV201620172018':
            datahist = 'JetHT'
        else:
            datahist = 'BTagCSV'
        
    
    char_var = var.c_str()
    try:
        #h_tmp = chunk_df.Fill(template, [char_var, 'totalWeight'])
        f_out.cd()
        print("2222222")
        h_tmp = chunk_df.Filter("%s > %s"%(char_var,xmin)).Histo1D((char_var,char_var,nbins,array('d',define_bins)),char_var,'totalWeight')
        print("33333333333")
        # h_tmp = chunk_df.Filter("%s > %s"%(char_var,xmin)).Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'totalWeight')
        if proctodo == "data_obs":
            data_value = h_tmp.Integral()
            print("already get the data value !!!!!!!!!!!!!")
            print(h_tmp.Integral())

        if proctodo == "QCD_datadriven_data":
            print(h_tmp.Integral())
            h_tmp.Scale(data_value/h_tmp.Integral())
            print("already scale the QCD !!!!!!!!!!!!!")
            print(h_tmp.Integral())


        h_tmp.SetTitle('%s_tmp'%(proctodo))
        h_tmp.SetName('%s_tmp'%(proctodo))
        h_uni = ROOT.TH1F(char_var,char_var,nbins,0,nbins)
        h_uni.SetTitle('%s'%(proctodo))
        h_uni.SetName('%s'%(proctodo))

        for i in range(1, h_uni.GetNbinsX()+1):
            data_tmp = h_tmp.GetBinContent(i)
            e_data_tmp = h_tmp.GetBinError(i)
            h_uni.SetBinContent(i, data_tmp)
            h_uni.SetBinError(i, e_data_tmp)
        h_uni.Write()

    except:
        print("%s likely has 0 events"%proctodo)

f_out.Close()
seconds = time.time()
print("Seconds to load : ", seconds-seconds0)
#print("Minutes to load : ", (seconds-seconds0)/60.0)

# def Unc_Shape(Marko_sample,xinyue_sample,var,cat,year):


#     ROOT.gROOT.ProcessLine(".x /eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/shape_unc/lhcbStyle.C")
    
#     # -------------------------------------------------------------- #
#     # calculate corrected eff: 1D
#     # -------------------------------------------------------------- #
#           file_1Higgs = "{}/ProbHHH6b_1Higgs_inclusive_/histograms/histograms_{}.root".format(path_to_histograms,do_limit_input)

#     file_1Higgs = ROOT.TFile(higgs1_path)
#     file_2Higgs = ROOT.TFile(higgs2_path)


#     # ==== Reading original distributions
#     Hist_Data_1Higgs = file_1Higgs.Get("data_obs").Clone()
#     Hist_Data_1Higgs.SetName("Hist_Data_1Higgs")
#     Hist_Data_2Higgs = file_2Higgs.Get("data_obs").Clone()
#     Hist_Data_2Higgs.SetName("Hist_Data_2Higgs")

#     Hist_BKG_1Higgs = file_1Higgs.Get("QCD").Clone()
#     Hist_BKG_1Higgs.SetName("Hist_BKG_1Higgs")
#     Hist_BKG_2Higgs = file_2Higgs.Get("QCD").Clone()
#     Hist_BKG_2Higgs.SetName("Hist_BKG_2Higgs")
#     bkg_max = Hist_BKG_2Higgs.GetMaximum()

#     Hist_norm_BKG_1Higgs = Hist_BKG_1Higgs.Clone()
#     Hist_norm_BKG_1Higgs.SetName("Hist_norm_BKG_1Higgs")
#     Hist_norm_BKG_2Higgs = Hist_BKG_2Higgs.Clone()
#     Hist_norm_BKG_2Higgs.SetName("Hist_norm_BKG_2Higgs")
#     Hist_norm_BKG_1Higgs.Scale(1.0/Hist_BKG_1Higgs.Integral())
#     Hist_norm_BKG_2Higgs.Scale(1.0/Hist_BKG_2Higgs.Integral())



# ########QCD already scaled to the data, if not you can use line below
#     # Hist_BKG_2Higgs.Scale(Hist_Data_2Higgs.Integral()/Hist_BKG_2Higgs.Integral())
    
#     # ==== Correction, Sigma_M (no correction), Sigma_P ( MC_2Higgs \times ratio^2 ) 
#     # file_save = ROOT.TFile(higgs2_path, "update")
#     Hist_Corr_2Higgs = Hist_Data_2Higgs.Clone()
#     Hist_Corr_2Higgs.SetName("QCD_correct")
#     Hist_Corr_2Higgs.SetTitle('QCD_correct')

# ####### sigma_M_2Higgs is uncertainties
#     # Hist_Sigma_M_2Higgs = Hist_Data_2Higgs.Clone()
#     # Hist_Sigma_M_2Higgs.SetName("Hist_Sigma_M_2Higgs")

#     # Hist_Sigma_P_2Higgs = Hist_Data_2Higgs.Clone()
#     # Hist_Sigma_P_2Higgs.SetName("Hist_Sigma_P_2Higgs")

#     Hist_ratio_bkg = Hist_Data_2Higgs.Clone()
#     Hist_ratio_bkg.SetName("Hist_ratio_bkg")

#     Hist_ratio_corr = Hist_Data_2Higgs.Clone()
#     Hist_ratio_corr.SetName("Hist_ratio_corr")

#     Hist_ratio = Hist_Data_2Higgs.Clone()
#     Hist_ratio.SetName("Hist_ratio")

#     # list_sigma_M_2Higgs = []
#     # list_sigma_P_2Higgs = []
#     # list_corr_2Higgs    = []
#     # list_corr_M_2Higgs  = []
#     # list_corr_P_2Higgs  = []
#     # list_data           = []
#     # bin_Xaxis           = []

# #######  Hist_Corr_2Higgs_M is histograms down
#     Hist_Corr_2Higgs_M = Hist_Data_2Higgs.Clone()
#     Hist_Corr_2Higgs_M.SetName("Hist_Corr_2Higgs_M")
#     Hist_Corr_2Higgs_P = Hist_Data_2Higgs.Clone()
#     Hist_Corr_2Higgs_P.SetName("Hist_Corr_2Higgs_P")

#     #==== Fill hist

#     for i in range(1, Hist_Data_1Higgs.GetNbinsX()+1):
#         # read value and error
#         data_1Higgs     = Hist_Data_1Higgs.GetBinContent(i)
#         data_2Higgs     = Hist_Data_2Higgs.GetBinContent(i)
#         bkg_1Higgs      = Hist_BKG_1Higgs.GetBinContent(i)
#         bkg_2Higgs      = Hist_BKG_2Higgs.GetBinContent(i)
#         norm_bkg_1Higgs = Hist_norm_BKG_1Higgs.GetBinContent(i)
#         norm_bkg_2Higgs = Hist_norm_BKG_2Higgs.GetBinContent(i)

#         e_data_1Higgs     = Hist_Data_1Higgs.GetBinError(i)
#         e_data_2Higgs     = Hist_Data_2Higgs.GetBinError(i)
#         e_bkg_1Higgs      = Hist_BKG_1Higgs.GetBinError(i)
#         e_bkg_2Higgs      = Hist_BKG_2Higgs.GetBinError(i)
#         e_norm_bkg_1Higgs = Hist_norm_BKG_1Higgs.GetBinError(i)
#         e_norm_bkg_2Higgs = Hist_norm_BKG_2Higgs.GetBinError(i)


#         # Correction : Hist_BKG_2Higgs * (Hist_Data_1Higgs / Hist_BKG_1Higgs)
#         Corr_2Higgs = bkg_2Higgs * (norm_bkg_1Higgs / norm_bkg_2Higgs)
#         # Corr_err_2Higgs = Corr_2Higgs * np.sqrt(
#         #                     (e_bkg_2Higgs / bkg_2Higgs)**2 + 
#         #                     (e_norm_bkg_1Higgs / norm_bkg_1Higgs)**2 + 
#         #                     (e_norm_bkg_2Higgs / norm_bkg_2Higgs)**2
#         #                   )

#         Corr_err_2Higgs = Corr_2Higgs - bkg_2Higgs
#         Hist_Corr_2Higgs.SetBinContent(i, Corr_2Higgs)
#         Hist_Corr_2Higgs.SetBinError(i, 1.0*Corr_err_2Higgs)

#         # ratio_bkg  = bkg_2Higgs/data_2Higgs
#         # ratio_corr = Corr_2Higgs/data_2Higgs
#         ratio      = Corr_2Higgs/bkg_2Higgs

#         # n = Hist_Data_1Higgs.GetNbinsX()+1
#         # if i >= 0.7*n :
#         #     ratio_bkg=10001
#         #     ratio_corr=10001

#         # Hist_ratio_bkg.SetBinContent(i, ratio_bkg)
#         # Hist_ratio_bkg.SetBinError(i, 0.)
#         # Hist_ratio_corr.SetBinContent(i, ratio_corr)
#         # Hist_ratio_corr.SetBinError(i, 0.)
#         Hist_ratio.SetBinContent(i, ratio)
#         Hist_ratio.SetBinError(i, 0.)

        


#         # Sigma_M : abs(Hist_Data_2Higgs - Hist_BKG_2Higgs) 
#         sigma_M = -1.0 * Corr_err_2Higgs
#         sigma_M_err = 0.
#         # Hist_Sigma_M_2Higgs.SetBinContent(i, sigma_M)
#         # Hist_Sigma_M_2Higgs.SetBinError(i, sigma_M_err)
#         Hist_Corr_2Higgs_M.SetBinContent(i,bkg_2Higgs + 1.* sigma_M)
#         Hist_Corr_2Higgs_M.SetBinError(i,sigma_M_err)
#         # list_corr_M_2Higgs.append(Corr_2Higgs+ 1.* sigma_M)
#         # list_corr_M_2Higgs.append(Hist_Corr_2Higgs_M_try.GetBinContent(i))
        
    
#         # Sigma_P : Hist_BKG_2Higgs * ((Hist_Data_1Higgs / Hist_BKG_1Higgs))^2 
#         sigma_P = Corr_err_2Higgs
#         sigma_P_err = 0.
#         # Hist_Sigma_P_2Higgs.SetBinContent(i, sigma_P)
#         # Hist_Sigma_P_2Higgs.SetBinError(i, sigma_P_err)
#         Hist_Corr_2Higgs_P.SetBinContent(i,bkg_2Higgs + sigma_P)
#         Hist_Corr_2Higgs_P.SetBinError(i,sigma_P_err)

#         # list_sigma_P_2Higgs.append(sigma_P)
#         # list_corr_P_2Higgs.append(Corr_2Higgs + sigma_P)
#         # list_corr_P_2Higgs.append(Hist_Corr_2Higgs_P_try.GetBinContent(i))


#         #####histograms#########

        

#     # array_corr_2Higgs    = np.array(list_corr_2Higgs)
#     # array_sigma_M_2Higgs = np.array(list_sigma_M_2Higgs)
#     # array_sigma_P_2Higgs = np.array(list_sigma_P_2Higgs)
#     # array_corr_M_2Higgs  = np.array(list_corr_M_2Higgs)
#     # array_corr_P_2Higgs  = np.array(list_corr_P_2Higgs)
#     # array_bin_Xaxis      = np.array(bin_Xaxis)
#     # array_data           = np.array(list_data)

#     #######write histograms##########
#     f_out = ROOT.TFile(higgs2_path, 'update')
#     print("Writing in %s" % higgs2_path)
#     f_out.cd()
#     f_out.Delete(Form("QCD_DataDriven_Shape_{}Down;1".format(Higgs_number)))
#     f_out.Delete(Form("QCD_DataDriven_Shape_{}Up;1".format(Higgs_number)))
#     f_out.Delete(Form("QCD_correct;1"))
#     f_out.Delete(Form("QCD_DataDriven_Shape_Down;1"))
#     f_out.Delete(Form("QCD_DataDriven_Shape_Up;1"))
#     # f_out.Delete(Form("Hist_Corr_2Higgs_P;1"))
#     # if f_out.IsZombie():
#     #     print("Error: Unable to open the ROOT file.")
#     # # else:
#     # keys = f_out.GetListOfKeys()
#     # strings_to_remove = ["QCD_correct", "Hist_Corr_2Higgs_","DataDriven_Shape"]
#     # for key in keys:
#     #     obj = key.ReadObj()
#     #     deleted = False
#     #     for string in strings_to_remove:
#     #         if string in obj.GetName():
#     #             f_out.Delete(Form("%s;%s" % (obj.GetName(), obj.ClassName())))
#     #             print("deleted successfully.")
#     #             deleted = True
#     #             break
#     #     if deleted:
#             # keys = list(f_out.GetListOfKeys())
#             # continue  
#     # f_out.Write()
#     # f_out.Close()
#     print("No datadriven_shape need to delete now")
#     # if Higgs_number == '3Higgs':

#     #     # Hist_Corr_2Higgs_M.SetTitle('QCD_DataDriven_Shape_3H6b_{}Down'.format(year))
#     #     # Hist_Corr_2Higgs_M.SetName('QCD_DataDriven_Shape_3H6b_{}Down'.format(year))
#     #     # Hist_Corr_2Higgs_P.SetTitle('QCD_DataDriven_Shape_3H6b_{}Up'.format(year))
#     #     # Hist_Corr_2Higgs_P.SetName('QCD_DataDriven_Shape_3H6b_{}Up'.format(year))

#     #     Hist_Corr_2Higgs_M.SetTitle('QCD_DataDriven_Shape_3H6bDown')
#     #     Hist_Corr_2Higgs_M.SetName('QCD_DataDriven_Shape_3H6bDown')
#     #     Hist_Corr_2Higgs_P.SetTitle('QCD_DataDriven_Shape_3H6bUp')
#     #     Hist_Corr_2Higgs_P.SetName('QCD_DataDriven_Shape_3H6bUp')
#     Hist_Corr_2Higgs_M.SetTitle('QCD_DataDriven_Shape_{}Down'.format(Higgs_number))
#     Hist_Corr_2Higgs_M.SetName('QCD_DataDriven_Shape_{}Down'.format(Higgs_number))
#     Hist_Corr_2Higgs_P.SetTitle('QCD_DataDriven_Shape_{}Up'.format(Higgs_number))
#     Hist_Corr_2Higgs_P.SetName('QCD_DataDriven_Shape_{}Up'.format(Higgs_number))


#     # Hist_Corr_2Higgs_M.SetTitle('QCD_DataDriven_Shape_Down')
#     # Hist_Corr_2Higgs_M.SetName('QCD_DataDriven_Shape_Down')
#     # Hist_Corr_2Higgs_P.SetTitle('QCD_DataDriven_Shape_Up')
#     # Hist_Corr_2Higgs_P.SetName('QCD_DataDriven_Shape_Up')

#     # if Higgs_number == '2Higgs':
#     #     # Hist_Corr_2Higgs_M.SetTitle('QCD_datadriven_correct_DataDriven_Shape_2H6b_{}Down'.format(year))
#     #     # Hist_Corr_2Higgs_M.SetName('QCD_datadriven_correct_DataDriven_Shape_2H6b_{}Down'.format(year))
#     #     # Hist_Corr_2Higgs_P.SetTitle('QCD_datadriven_correct_DataDriven_Shape_2H6b_{}Up'.format(year))
#     #     # Hist_Corr_2Higgs_P.SetName('QCD_datadriven_correct_DataDriven_Shape_2H6b_{}Up'.format(year))
        
#     #     # Hist_Corr_2Higgs_M.SetTitle('QCD_DataDriven_Shape_2H6b_{}Down'.format(year))
#     #     # Hist_Corr_2Higgs_M.SetName('QCD_DataDriven_Shape_2H6b_{}Down'.format(year))
#     #     # Hist_Corr_2Higgs_P.SetTitle('QCD_DataDriven_Shape_2H6b_{}Up'.format(year))
#     #     # Hist_Corr_2Higgs_P.SetName('QCD_DataDriven_Shape_2H6b_{}Up'.format(year))
#     #     Hist_Corr_2Higgs_M.SetTitle('QCD_DataDriven_Shape_2H6bDown')
#     #     Hist_Corr_2Higgs_M.SetName('QCD_DataDriven_Shape_2H6bDown')
#     #     Hist_Corr_2Higgs_P.SetTitle('QCD_DataDriven_Shape_2H6bUp')
#     #     Hist_Corr_2Higgs_P.SetName('QCD_DataDriven_Shape_2H6bUp')

#     # f_out = ROOT.TFile(higgs2_path, 'update')
#     # f_out.cd()
#     Hist_Corr_2Higgs_M.Write()
#     Hist_Corr_2Higgs_P.Write()
#     Hist_Corr_2Higgs.Write()
#     f_out.Close()


    
    


#     #==== Draw compared plot and save    
#     # ytitle   = "Arbitray scale"
#     xtitle   = do_limit_input
#     data_max        = Hist_Data_2Higgs.GetMaximum()
#     # bkg_max         = Hist_Bkg_2Higgs.GetMaximum()
#     correct_bkg_max = Hist_Corr_2Higgs.GetMaximum()
#     y_max= max(data_max, bkg_max, correct_bkg_max)+20
#     y_min = 0.0
#     # y_max = 250
#     # y_values_bkg  = [value for value in Hist_ratio_bkg if value <= 1000]
#     # y_values_corr = [value for value in Hist_ratio_corr if value <= 1000]
#     # y_values_bkg_max  = max(y_values_bkg)
#     # y_values_corr_max = max(y_values_corr)
#     # y_pad_max = max(y_values_bkg_max,y_values_corr_max)
#     y_error_max_before = abs(Hist_ratio.GetMaximum()-1.0)
#     y_error_min_before = abs(Hist_ratio.GetMinimum()-1.0)
#     y_error_max = max(y_error_max_before,y_error_min_before)
#     y_M_min = -1.0* y_error_max +1.0 -0.2
#     y_M_max = 1.0*y_error_max + 1.0 +0.2
#     # Hist_Data_2Higgs.GetYaxis().SetRangeUser(Hist_Data_2Higgs.GetMinimum(), Hist_Data_2Higgs.GetMaximum())
#     # Hist_Data_2Higgs.GetXaxis().SetRangeUser(Hist_Data_2Higgs.GetXaxis().GetXmin(), Hist_Data_2Higgs.GetXaxis().GetXmax())

#     ROOT.gROOT.SetBatch(True)

#     cc = ROOT.TCanvas("cc", "cc", 1000, 800)
#     cc.Divide(1,2,0,0,0) 

#     cc.cd(1)
#     gPad = cc.GetPad(1)
#     gPad.SetTopMargin(0.1)
#     gPad.SetBottomMargin(0.1)
#     gPad.SetLeftMargin(0.12)
#     gPad.SetRightMargin(0.07)
#     gPad.SetPad(0.0,0.25,0.98,0.98)
#     gPad.SetGrid()
#     Hist_Data_2Higgs.SetLineColor(1)
#     Hist_Data_2Higgs.SetLineWidth(2)
#     Hist_Data_2Higgs.SetMarkerColor(1)
#     Hist_Data_2Higgs.SetMarkerStyle(23)
#     Hist_Data_2Higgs.SetXTitle(xtitle)
#     Hist_Data_2Higgs.GetXaxis().SetLabelSize(0.04)    
#     Hist_Data_2Higgs.GetXaxis().SetTitleOffset(0.9)
#     # Hist_Data_2Higgs.SetYTitle(ytitle)
#     Hist_Data_2Higgs.SetAxisRange(y_min, y_max, "Y")
#     Hist_Data_2Higgs.GetYaxis().SetLabelSize(0.04)

#     Hist_BKG_2Higgs.SetLineColor(2)
#     Hist_BKG_2Higgs.SetLineWidth(2)
#     Hist_BKG_2Higgs.SetMarkerColor(2)
#     Hist_BKG_2Higgs.SetMarkerStyle(23)

#     Hist_Corr_2Higgs.SetLineColor(4)
#     Hist_Corr_2Higgs.SetLineWidth(2)
#     Hist_Corr_2Higgs.SetMarkerColor(4)
#     Hist_Corr_2Higgs.SetMarkerStyle(23)

#     leg = ROOT.TLegend(0.65, 0.67, 0.92, 0.87)
#     leg.AddEntry(Hist_Data_2Higgs , "Data - {}".format(Higgs_number), "epl")
#     leg.AddEntry(Hist_BKG_2Higgs , "BKG - {}".format(Higgs_number), "epl")    
#     leg.AddEntry(Hist_Corr_2Higgs , "BKG_Corrected - {}".format(Higgs_number), "epl")    
#     leg.AddEntry(Hist_ratio , "corr_bkg/bkg (pad below)", "epl")    
      
#     Hist_Data_2Higgs.Draw()
#     Hist_BKG_2Higgs.Draw("same")    
#     Hist_Corr_2Higgs.Draw("same")    
#     leg.Draw("same")

#     # ptext = ROOT.TPaveText(0.13, 0.58, 0.64, 0.86,"NDC")
#     # ptext.SetTextFont(132)
#     # ptext.AddText("#color[1]{Ratio (1 Higgs) = Data/BKG (1 Higgs) }")
#     # ptext.AddText("#color[4]{H_{Corr} (2 Higgs) = BKG (2 Higgs) #times Ratio (1 Higgs)}")
#     # ptext.AddText("#color[46]{Sigma_M (2 Higgs) = - | H_{Data} - H_{BKG} | (2 Higgs)}")
#     # ptext.AddText("#color[9]{Sigma_P (2 Higgs) = + H_{Corr} (2 Higgs) #times Ratio^{2} (1 Higgs)}")
#     # ptext.SetFillColor(ROOT.kWhite)
#     # ptext.SetTextAlign(11)
#     # ptext.Draw("same")

#     cc.cd(2)
#     gPad = cc.GetPad(2)
#     gPad.SetTopMargin(0.05)
#     gPad.SetBottomMargin(0.3)
#     gPad.SetLeftMargin(0.12)
#     gPad.SetRightMargin(0.07)
#     gPad.SetPad(0.0,0.06,0.98,0.25)
  
#     # Hist_Sigma_P_2Higgs.SetXTitle("#scale[3.5]{#color[46]{Minus} / #color[9]{Plus} 1 Sigma}")
#     # Hist_Sigma_P_2Higgs.GetXaxis().SetTitleOffset(2.8)
#     # Hist_Sigma_P_2Higgs.SetLineColor(4)
#     # Hist_Sigma_P_2Higgs.SetFillColor(9)
#     # Hist_Sigma_P_2Higgs.SetLineWidth(2)
#     # Hist_Sigma_P_2Higgs.SetMarkerColor(4)
#     # Hist_Sigma_P_2Higgs.SetMarkerStyle(23)
#     # Hist_Sigma_P_2Higgs.SetAxisRange(y_M_min, y_M_max, "Y")
#     # Hist_Sigma_P_2Higgs.SetLabelSize(0.15,"X")
#     # Hist_Sigma_P_2Higgs.SetLabelSize(0.15,"Y")
#     # Hist_Sigma_P_2Higgs.GetYaxis().SetNdivisions(505)
#     # Hist_Sigma_M_2Higgs.SetLineColor(2)
#     # Hist_Sigma_M_2Higgs.SetFillColor(46)
#     # Hist_Sigma_P_2Higgs.Draw("hist")
#     # Hist_Sigma_M_2Higgs.Draw("hist && same")

#     # Hist_ratio_bkg.GetXaxis().SetTitleOffset(2.8)
#     # Hist_ratio_bkg.SetLineColor(2)
#     # # Hist_ratio_bkg.SetFillColor(9)
#     # Hist_ratio_bkg.SetLineWidth(2)
#     # Hist_ratio_bkg.SetMarkerColor(2)
#     # Hist_ratio_bkg.SetMarkerStyle(23)
#     # Hist_ratio_bkg.SetAxisRange(y_M_min, y_M_max, "Y")
#     # Hist_ratio_bkg.SetLabelSize(0.15,"X")
#     # Hist_ratio_bkg.SetLabelSize(0.15,"Y")
#     # Hist_ratio_bkg.GetYaxis().SetNdivisions(505)
#     # Hist_ratio_corr.SetLineColor(4)
#     # leg2 = ROOT.TLegend(0.65, 0.67, 0.92, 0.87)
#     # leg2.AddEntry(Hist_ratio_bkg , "bkg/data ", "epl")    
#     # leg2.AddEntry(Hist_ratio_corr , "corr_bkg/data", "epl")  
#     # # Hist_ratio_corr.SetFillColor(46)
#     # # Hist_ratio_bkg.Draw("hist")
#     # Hist_ratio_bkg.Draw("ep")
#     # Hist_ratio_corr.Draw("ep & same")
#     # # leg2.Draw()

#     Hist_ratio.SetLineColor(2)
#     Hist_ratio.SetLineWidth(2)
#     Hist_ratio.SetMarkerColor(2)
#     Hist_ratio.SetMarkerStyle(23)
#     Hist_ratio.SetAxisRange(y_M_min, y_M_max, "Y")
#     Hist_ratio.SetLabelSize(0.15,"X")
#     Hist_ratio.SetLabelSize(0.15,"Y")
#     Hist_ratio.GetYaxis().SetNdivisions(505)
#     Hist_ratio.Draw("hist")
#     line = ROOT.TLine(0,1,10,1)
#     line.SetLineColor(6)
#     line.SetLineStyle(ROOT.kDashed)
#     line.SetLineWidth(1)
#     line.Draw("same")
#     cc.SaveAs("{}/Comp_{}_{}_correction.pdf".format(path,Higgs_number,do_limit_input))





    

#     c2 = ROOT.TCanvas("c2", "c2", 1000, 800)
#     c2.Divide(1,2,0,0,0) 

#     c2.cd(1)
#     gPad = c2.GetPad(1)
#     gPad.SetTopMargin(0.1)
#     gPad.SetBottomMargin(0.1)
#     gPad.SetLeftMargin(0.12)
#     gPad.SetRightMargin(0.07)
#     gPad.SetPad(0.0,0.25,0.98,0.98)
#     gPad.SetGrid()
#     Hist_BKG_2Higgs.SetLineColor(1)
#     Hist_BKG_2Higgs.SetLineWidth(2)
#     Hist_BKG_2Higgs.SetMarkerColor(1)
#     Hist_BKG_2Higgs.SetMarkerStyle(23)
#     Hist_BKG_2Higgs.SetXTitle(xtitle)
#     Hist_BKG_2Higgs.GetXaxis().SetLabelSize(0.04)    
#     Hist_BKG_2Higgs.GetXaxis().SetTitleOffset(0.9)
#     Hist_BKG_2Higgs.SetAxisRange(y_min, y_max, "Y")
#     Hist_BKG_2Higgs.GetYaxis().SetLabelSize(0.04)

#     Hist_BKG_2Higgs.SetLineColor(2)
#     Hist_BKG_2Higgs.SetLineWidth(2)
#     Hist_BKG_2Higgs.SetMarkerColor(2)
#     Hist_BKG_2Higgs.SetMarkerStyle(23)

#     Hist_Corr_2Higgs_M.SetLineColor(861)
#     Hist_Corr_2Higgs_M.SetLineWidth(2)
#     Hist_Corr_2Higgs_M.SetMarkerColor(861)
#     Hist_Corr_2Higgs_M.SetMarkerStyle(23)
#     Hist_Corr_2Higgs_P.SetLineColor(800-3)
#     Hist_Corr_2Higgs_P.SetLineWidth(2)
#     Hist_Corr_2Higgs_P.SetMarkerColor(800-3)
#     Hist_Corr_2Higgs_P.SetMarkerStyle(23)

#     leg = ROOT.TLegend(0.65, 0.67, 0.92, 0.87)
#     leg.AddEntry(Hist_Corr_2Higgs_P , "histogram_up", "epl")
#     leg.AddEntry(Hist_BKG_2Higgs , "BKG - {}".format(Higgs_number), "epl")    
#     leg.AddEntry(Hist_Corr_2Higgs_M , "histogram_down", "epl")    
#     leg.AddEntry(Hist_ratio , "corr_bkg/bkg (pad below)", "epl")    
#     Hist_BKG_2Higgs.Draw()
#     Hist_Corr_2Higgs_P.Draw("same")
#     Hist_Corr_2Higgs_M.Draw("same")    
#     leg.Draw("same")



#     c2.cd(2)
#     gPad = c2.GetPad(2)
#     gPad.SetTopMargin(0.05)
#     gPad.SetBottomMargin(0.3)
#     gPad.SetLeftMargin(0.12)
#     gPad.SetRightMargin(0.07)
#     gPad.SetPad(0.0,0.06,0.98,0.25)
  
#     Hist_ratio.SetLineColor(2)
#     Hist_ratio.SetLineWidth(2)
#     Hist_ratio.SetMarkerColor(2)
#     Hist_ratio.SetMarkerStyle(23)
#     Hist_ratio.SetAxisRange(y_M_min, y_M_max, "Y")
#     Hist_ratio.SetLabelSize(0.15,"X")
#     Hist_ratio.SetLabelSize(0.15,"Y")
#     Hist_ratio.GetYaxis().SetNdivisions(505)
#     Hist_ratio.Draw("hist")
#     line = ROOT.TLine(0,1,10,1)
#     line.SetLineColor(6)
#     line.SetLineStyle(ROOT.kDashed)
#     line.SetLineWidth(1)
#     line.Draw("same")
#     c2.SaveAs("{}/UpDown_{}_{}_correction.pdf".format(path,Higgs_number,do_limit_input))

