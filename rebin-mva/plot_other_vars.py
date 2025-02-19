# Script to plot other vars in SR

import os, ROOT

ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)

from utils import histograms_dict

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v33')
parser.add_argument('--year', default='2016APV201620172018')
parser.add_argument('--prob', default='ProbHHH6b')
parser.add_argument('--cat', default='3Higgs')
parser.add_argument('--var', default = 'ProbMultiH')
args = parser.parse_args()


version = args.version
year = args.year

path = '/isilon/data/users/mstamenk/eos-triple-h/%s/mva-inputs-%s-categorisation-spanet-boosted-classification/'%(version,year)

category = args.prob + '_' + args.cat + '_inclusive_CR'

data = ROOT.RDataFrame('Events',path +'/' + category + '/' + 'data_obs.root')
bkg_model = ROOT.RDataFrame('Events',path +'/' + category + '/' + 'QCD_datadriven.root')
hhh = ROOT.RDataFrame('Events',path +'/' + category + '/' + 'GluGluToHHHTo6B_SM.root')
hh = ROOT.RDataFrame('Events',path +'/' + category + '/' + 'GluGluToHHTo4B_cHHH1.root')



#cut = 'ProbMultiH > 0.9825 && ProbMultiH < 0.9965'
cut = 'ProbMultiH > 0.99'
#cut = 'ProbMultiH > 0.95 && ProbMultiH < 0.997'
var = 'jet1Pt'

jet_list = ['jet1','jet2','jet3','jet4','jet5','jet6','fatJet1','fatJet2','fatJet3']

var_list = ['Pt','Eta','Phi','Mass']


for jet in jet_list:
    for v in var_list:
        var = jet+v
        nbins = histograms_dict[var]['nbins']
        xmin = histograms_dict[var]['xmin']
        xmax = histograms_dict[var]['xmax']
        label = histograms_dict[var]['label']

        h_data = data.Filter(cut).Histo1D((var,var,nbins,xmin,xmax),var)

        h_bkg = bkg_model.Filter(cut).Histo1D((var,var,nbins,xmin,xmax),var)

        h_sig = hhh.Filter(cut).Histo1D((var,var,nbins,xmin,xmax),var)

        h_hh = hh.Filter(cut).Histo1D((var,var,nbins,xmin,xmax),var)

        h_data = h_data.GetValue()
        h_bkg = h_bkg.GetValue()

        h_sig = h_sig.GetValue()
        h_hh = h_hh.GetValue()


        h_data.Scale(1./h_data.Integral())
        h_bkg.Scale(1./h_bkg.Integral())
        h_sig.Scale(1./h_sig.Integral())
        try:
            h_hh.Scale(1./h_hh.Integral())
        except: h_hh.Scale(0)

        h_data.SetStats(0)
        h_data.SetMarkerColor(ROOT.kBlack)
        h_data.SetLineColor(ROOT.kBlack)

        h_data.GetXaxis().SetTitle(label)
        h_data.GetYaxis().SetTitle('Normalized')

        h_bkg.SetFillColor(ROOT.kOrange + 2)
        h_bkg.SetLineColor(ROOT.kOrange + 2)

        h_sig.SetLineColor(ROOT.kRed + 2)
        h_hh.SetLineColor(ROOT.kViolet + 2)

        h_div = h_data.Clone(var + '_div')
        h_div.Divide(h_bkg)

        h_div.GetYaxis().SetTitle('Data / QCD')

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

        h_div.GetYaxis().SetRangeUser(-1.0,3.)

        c = ROOT.TCanvas()

        p1 = ROOT.TPad("c_1","",0,0,1,0.3)
        p2 = ROOT.TPad("c_2","", 0,0.3,1,0.95)

        p1.Draw()
        p2.Draw()

        p1.SetBottomMargin(0.3)
        p1.SetTopMargin(0.05)
        p1.SetRightMargin(0.05)
        p2.SetTopMargin(0.05)
        p2.SetBottomMargin(0.02)
        p2.SetRightMargin(0.05)

        legend = ROOT.TLegend(0.6,0.6,0.89,0.89)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)

        legend.AddEntry(h_data, 'Data')
        legend.AddEntry(h_bkg,'QCD model')
        legend.AddEntry(h_sig,'HHH SM')
        legend.AddEntry(h_hh,'HH SM')

        p2.cd()

        h_data.Draw('e')
        h_bkg.Draw('hist e same')
        h_sig.Draw('hist e same')
        h_hh.Draw('hist e same')
        h_data.Draw('e same')

        legend.Draw()

        p1.cd()
        p1.SetGridy()
        h_div.Draw('e')

        c.Print('plots-other-vars/' + category + '_' + var+ '_' + year +'.png')