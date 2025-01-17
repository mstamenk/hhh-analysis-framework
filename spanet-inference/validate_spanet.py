# Script to validate merging and make sure events are ok

import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import glob, os

# argument parser
import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v27') # version of NanoNN production
parser.add_argument('--year', default='2018') # year
args = parser.parse_args()

year = args.year
version = args.version

typename = 'spanet-boosted'

path_ref = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-nanoaod/'%(version,year)
path_new = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-%s-variables-nanoaod/'%(version,year,typename)


output_plots = 'validation'
if not os.path.isdir(output_plots):
    os.makedirs(output_plots)

samples = glob.glob(path_ref + '/*.root')

samples = [os.path.basename(s) for s in samples]

sample = 'GluGluToHHHTo6B_SM.root'

for sample in samples:
    df_ref = ROOT.RDataFrame('Events',path_ref + '/' + sample)
    df_new = ROOT.RDataFrame('Events',path_new + '/' + sample)

    varx = 'h1_t3_mass'

    binsx = 20
    xmin = 0
    xmax = 200

    h_ref = df_ref.Histo1D((varx,varx,binsx,xmin,xmax),varx)
    h_new = df_new.Histo1D((varx,varx,binsx,xmin,xmax),varx)


    h_ref = h_ref.GetValue()
    h_new = h_new.GetValue()

    h_new.SetLineColor(ROOT.kGreen + 2)

    h_ref.SetLineWidth(2)
    h_new.SetLineWidth(2)

    c = ROOT.TCanvas()
    legend = ROOT.TLegend(0.6,0.6,0.9,0.9)
    legend.AddEntry(h_ref,'Ref')
    legend.AddEntry(h_new,'Adding SPANET variables')

    h_ref.Draw("hist e")
    h_new.Draw("hist e same")
    legend.Draw()

    c.Print(output_plots + '/' + sample.replace('.root','') + '_%s'%args.year + '.pdf')

    c2 = ROOT.TCanvas()

    h_div = h_ref.Clone(sample+'_div')
    h_div.Divide(h_new)

    h_div.Draw('hist e')

    c2.Print(output_plots + '/' + sample.replace('.root','') + '_%s'%args.year + '_div.pdf')

    print("Difference between number of events", df_ref.Count().GetValue() - df_new.Count().GetValue())

