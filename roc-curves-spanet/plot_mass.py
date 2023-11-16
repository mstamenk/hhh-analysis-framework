import os, ROOT, glob

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.EnableImplicitMT()
from array import array

from utils import histograms_dict, drawText, addLabel_CMS_preliminary, luminosities


typename = 'spanet-boosted-classification-variables-pnet-v15'
path = '/isilon/data/users/mstamenk/eos-triple-h/samples-v28-2018-%s-nanoaod/'%(typename)

samples = glob.glob(path+ '*.root')
samples = [os.path.basename(s).replace('.root','') for s in samples]
#samples = [s for s in samples if 'GluGlu' not in s]
samples = [s for s in samples if 'JetHT' not in s]

#sample = 'GluGluToHHHTo6B_SM'
sample = 'QCD'
df = ROOT.RDataFrame('Events', path + '/' + sample + '.root')

df = df.Filter('nfatjets == 0')


higgs = 'h1'

for higgs in ['h1','h2','h3']:
    varx = '%s_mass'%higgs

    binsx = 15
    xmin = 50
    xmax = 200

    h = df.Histo1D((varx,varx,binsx,xmin,xmax),varx)

    varx = '%s_t3_mass'%higgs
    h_kin = df.Histo1D((varx,varx,binsx,xmin,xmax),varx)

    varx = '%s_spanet_boosted_mass'%higgs
    h_spanet = df.Histo1D((varx,varx,binsx,xmin,xmax),varx)

    h = h.GetValue()
    h_kin = h_kin.GetValue()
    h_spanet = h_spanet.GetValue()

    h.SetLineColor(ROOT.kRed)
    h_kin.SetLineColor(ROOT.kBlue)
    h_spanet.SetLineColor(ROOT.kGreen)

    h.Scale(1./h.Integral())
    h_kin.Scale(1./h_kin.Integral())
    h_spanet.Scale(1./h_spanet.Integral())
    h.SetMaximum(1.8* h.GetMaximum())
    c = ROOT.TCanvas()

    legend = ROOT.TLegend(0.43,0.64,0.94,0.92)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    legend.AddEntry(h,'Chi2')
    legend.AddEntry(h_kin,'Kinfit')
    legend.AddEntry(h_spanet,'Spanet')
    h.SetStats(0)

    h.Draw('hist e')
    h_kin.Draw('hist e same')
    h_spanet.Draw('hist e same')
    legend.Draw()

    c.Print('%s_%s.png'%(sample,higgs))