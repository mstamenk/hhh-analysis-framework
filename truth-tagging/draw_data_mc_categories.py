# Script to plot data / mc from processed files 

import os, ROOT
import tdrstyle,CMS_lumi

from utils import labels, binnings

ROOT.gROOT.SetBatch(ROOT.kTRUE)

#tdrstyle.setTDRStyle()

#CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
#CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
#CMS_lumi.writeExtraText = 1
#CMS_lumi.extraText = "Internal"

def get_sig(h_sig, h_bkg):
    z = 0.
    for i in range(h_sig.GetNbinsX()):
        #print(h_sig.GetBin(i))
        s = h_sig.GetBinContent(i) / 1000.
        b = h_bkg.GetBinContent(i)
        #print(s,b)
        if (s+b) > 0:
            z += s*s / ((s+b))
            #print(z)
    return ROOT.TMath.Sqrt(z)

hist_properties = {'JetHT' : [ROOT.kBlack, 0.8, 0, 'Data', True] , # [color, marker size, line size, legend label , add in legend]
                   'JetHT-btagSF' : [ROOT.kBlack, 0.8, 0, 'Data', True],
                   'BTagCSV' : [ROOT.kBlack, 0.8, 0, 'Data', True],
                   'QCD'   : [ROOT.kOrange, 0, 2, 'QCD', True], 
                   'QCD_bEnriched'   : [ROOT.kOrange, 0, 2, 'QCD b-enriched', True], 
                   'QCD6B'   : [ROOT.kOrange + 2, 0, 2, 'QCD6B', True], 
                   'QCD6B_bEnriched'   : [ROOT.kOrange + 2, 0, 2, 'QCD6B b-enriched', True], 
                   'ZJetsToQQ'   : [ROOT.kCyan, 0, 2, 'V+jets', True], 
                   'WJetsToQQ'   : [ROOT.kCyan, 0, 2, 'V+jets', False], 
                   'ZZTo4Q' : [ROOT.kGray, 0, 2, 'VV', True], 
                   'WWTo4Q' : [ROOT.kGray, 0, 2, 'VV', False], 
                   'ZZZ' : [ROOT.kRed, 0, 2, 'VVV', True], 
                   'WWW' : [ROOT.kRed, 0, 2, 'VVV', False], 
                   'WZZ' : [ROOT.kRed, 0, 2, 'VVV', False], 
                   'WWZ' : [ROOT.kRed, 0, 2, 'VVV', False], 
                   'TT' : [ROOT.kBlue, 0,2, 't#bar{t}', True],
                   'GluGluToHHHTo6B_SM' : [ROOT.kRed, 0,2, 'SM HHH x 1000', True],
        } 


#iPos = 11
#if( iPos==0 ): CMS_lumi.relPosX = 0.12

iPeriod = 0
c = ROOT.TCanvas()
p1 = ROOT.TPad("c_1","",0,0,1,0.3)
p2 = ROOT.TPad("c_2","", 0,0.3,1,1)

s = 'MMMMMM'
year = '2017'
version = 'v24'

for year in ['2016APV','2016','2017','2018']:
#for year in ['2017','2018']:
    if '2018' in year:
        datahist = 'JetHT'
    else:
        datahist = 'BTagCSV'

    histo_path = 'histograms-%s-optimised/'%(version)
    file_data = ROOT.TFile(histo_path + '/' + '%s_%s.root'%(datahist,year))
    file_signal = ROOT.TFile(histo_path + '/' + '%s_%s.root'%('GluGluToHHHTo6B_SM',year))
    files_bkg = {}
    for bkg in ['QCD_bEnriched','QCD6B_bEnriched','ZJetsToQQ','WJetsToQQ','WWW','WZZ','ZZTo4Q', 'TT']:
    #for bkg in ['QCD','QCD6B','ZJetsToQQ','WJetsToQQ','WWW','WZZ','ZZTo4Q', 'TT']:
    #for bkg in ['QCD6B']:
        f_tmp = ROOT.TFile(histo_path + '/' + '%s_%s.root'%(bkg,year))
        if f_tmp.IsOpen():
            files_bkg[bkg] = f_tmp

    for s in ['LLLLLL','MMMMMM','TTTTTT']:
    #for s in ['LLLLLL']:

        eos_plots = 'plot-data-mc-%s-%s-%s-optimised-b-enriched'%(year,s,version)

        if not os.path.isdir(eos_plots):
            os.mkdir(eos_plots)


        # ['JetHT','WWTo4Q','WWZ','ZJetsToQQ','ZZZ','QCD','WJetsToQQ','WWW','WZZ','ZZTo4Q', 'TT']:



        tagging = 'TT'
        for tagging in ['DT','TT']:

            var_name = 'mva'
            for var_name in ['h_fit_mass','mva']:
                var = '%s_%s_%s'%(var_name,s,tagging)

                print(var)

                legend = ROOT.TLegend(0.6,0.6,.9,0.9)
                legend.SetBorderSize(0)
                print(datahist)
                var_data = '%s_%s_%s'%(var_name,s,'DT')
                h_data = file_data.Get(var_data)
                #h_data.SetDirectory(0)
                h_data.SetMarkerColor(ROOT.kBlack)
                h_data.SetLineColor(ROOT.kBlack)
                h_data.SetMarkerSize(100)
                h_data.SetLineWidth(2)
                h_data.SetStats(0)
                h_data.GetXaxis().SetTitle(labels[var_name])
                h_data.SetTitle('')
                #h_data.Sumw2()
                legend.AddEntry(h_data, hist_properties['JetHT'][3])

                # blinding 
                if 'mass' in var:
                    for mass_value in [100,110,120,130]:
                        bin_m = h_data.FindBin(mass_value)
                        h_data.SetBinContent(bin_m,-0.0000001)
                        h_data.SetBinError(bin_m,0)

                if 'bdt' in var or 'mva' in var:
                #if 'bdt' in var :
                    blind_bdt = [x*0.05 + 0.2 for x in range(20)]
                    for value in blind_bdt:
                        bin_blind = h_data.FindBin(value)
                        h_data.SetBinContent(bin_blind,-0.0000001)
                        h_data.SetBinError(bin_blind,0)

                h_signal = file_signal.Get(var)
                h_signal.SetDirectory(0)
                h_signal.SetMarkerColor(hist_properties['GluGluToHHHTo6B_SM'][0])
                h_signal.SetLineColor(hist_properties['GluGluToHHHTo6B_SM'][0])
                h_signal.SetMarkerSize(hist_properties['GluGluToHHHTo6B_SM'][1])
                h_signal.SetLineWidth(hist_properties['GluGluToHHHTo6B_SM'][2])
                #h_signal.Sumw2()
                h_signal.Scale(1000.)
                legend.AddEntry(h_signal, hist_properties['GluGluToHHHTo6B_SM'][3], 'l')

                h_stack = ROOT.THStack()

                h_bkg = ROOT.TH1F(var+"bkg", var+"bkg", h_data.GetXaxis().GetNbins(), h_data.GetXaxis().GetXmin(), h_data.GetXaxis().GetXmax())


                for bkg in files_bkg:#['QCD','ZJetsToQQ','WJetsToQQ','ZZTo4Q', 'WWTo4Q', 'ZZZ' ,'WWW', 'WZZ', 'WWZ', 'TT']:
                #for bkg in ['QCD6B']:
                    f_bkg = files_bkg[bkg]
                    h_tmp = f_bkg.Get(var)
                    #h_tmp.Sumw2()
                    binining = binnings[var_name]
                    try:
                        h_tmp.SetDirectory(0)
                      
                    except: continue
                    #if 'QCD' in bkg and year == '2018':
                    #    h_tmp.Scale(2.93)
                    h_bkg.Add(h_tmp)

                    h_tmp.SetFillColor(hist_properties[bkg][0])
                    h_tmp.SetMarkerSize(hist_properties[bkg][1])
                    h_tmp.SetLineColor(hist_properties[bkg][0])
                    #h_tmp.SetLineSize(hist_properties[bkg][2])
                    if hist_properties[bkg][4]:
                        legend.AddEntry(h_tmp, hist_properties[bkg][3], 'f')
                    h_stack.Add(h_tmp)

                   
                #maxi = max(h_data.GetMaximum(), h_bkg.GetMaximum())

                #h_data.SetMaximum(maxi)

                h_div = h_data.Clone(var+'_ratio')
                h_div.Divide(h_bkg)

                h_div.GetYaxis().SetTitle('Data / MC')

                h_div.GetXaxis().SetTitleSize(0.11)
                h_div.GetXaxis().SetTitleOffset(1.35)
                h_div.GetXaxis().SetLabelSize(0.11)
                h_div.GetXaxis().SetLabelOffset(0.03)
                h_div.GetYaxis().SetTitleSize(0.11)
                h_div.GetYaxis().SetTitleOffset(0.35)
                h_div.GetYaxis().SetLabelSize(0.11)
                h_div.GetYaxis().SetLabelOffset(0.001)
                h_div.GetYaxis().SetMaxDigits(0)
                h_div.GetYaxis().SetNdivisions(4,8,0,ROOT.kTRUE)

                h_div.GetYaxis().SetRangeUser(0.1,2.)

                # set bin error to the value of data

                h_mc_stat = h_bkg.Clone(h_bkg.GetName()+'_mcstat')
                h_mc_stat.Divide(h_bkg)

                h_mc_stat.SetFillColor(ROOT.kBlue)
                h_mc_stat.SetFillStyle(3244)

                h_data.GetXaxis().SetLabelOffset(999)
                h_data.GetXaxis().SetLabelSize(0)
                c.cd()

                p1.Draw()
                p2.Draw()

                p1.SetBottomMargin(0.3)
                p1.SetTopMargin(0.05)
                p1.SetRightMargin(0.05)
                p2.SetTopMargin(0.05)
                p2.SetBottomMargin(0.02)
                p2.SetRightMargin(0.05)

                h_data.SetMinimum(0.0001)
                h_data.SetMaximum(1.5*h_data.GetMaximum())

                p2.cd()

                h_data.Draw('e')
                h_stack.Draw('hist e same')
                h_signal.Draw('hist e same')
                h_data.Draw('e same')
                legend.Draw()
                #CMS_lumi.CMS_lumi(c, iPeriod, iPos)

                p1.cd()
                p1.SetGridy()
                h_div.Draw('e')
                h_mc_stat.Draw('e2 same')
                c.cd()
                c.Update()
                c.RedrawAxis()

                c.Print(eos_plots + '/' + var +  '.pdf')
                print("Data")
                z_data = get_sig(h_signal,h_data)
                print("MC")
                z_bkg = get_sig(h_signal,h_bkg)
                print("Dat sig", z_data, 1+1.64*1./z_data)
                print("MC sig", z_bkg, 1 + 1.64*1./z_bkg )

    file_data.Close()
    file_signal.Close()

    for fi in files_bkg:
        files_bkg[fi].Close()

