import os, ROOT, glob

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.EnableImplicitMT()
from array import array

from utils import histograms_dict, drawText, addLabel_CMS_preliminary, luminosities


typename = 'spanet-boosted-classification'
year = '2018'
path = '/isilon/data/users/mstamenk/eos-triple-h/v28-fix/mva-inputs-%s-%s/inclusive_boosted-weights/'%(year,typename)

samples = glob.glob(path+ '*.root')
samples = [os.path.basename(s).replace('.root','') for s in samples]
#samples = [s for s in samples if 'GluGlu' not in s]
samples = [s for s in samples if 'JetHT' not in s]

sample = 'GluGluToHHHTo6B_SM'
#sample = 'GluGluToHHTo4B_cHHH1'
df = ROOT.RDataFrame('Events', path + '/' + sample + '.root')

df = df.Define('Prob1', 'ProbHHH + ProbHH4b')
df = df.Define('Prob2', 'ProbHHH + ProbHH4b + ProbHHH4b2tau')
df = df.Define('Prob3', 'ProbHHH + ProbHH4b + ProbHHH4b2tau + ProbHH2b2tau')

df = df.Filter('nprobejets > 1')


higgs = 'h1'

varx = 'ProbHHH4b2tau'

binsx = 100
xmin = 0
xmax = 1

h = df.Histo1D((varx,varx,binsx,xmin,xmax),varx,'eventWeight')

varx = 'Prob1'
h_kin = df.Histo1D((varx,varx,binsx,xmin,xmax),varx,'eventWeight')

varx = 'Prob2'
h_spanet = df.Histo1D((varx,varx,binsx,xmin,xmax),varx,'eventWeight')

varx = 'Prob3'
h_spanet_2 = df.Histo1D((varx,varx,binsx,xmin,xmax),varx,'eventWeight')


h = h.GetValue()
h_kin = h_kin.GetValue()
h_spanet = h_spanet.GetValue()
h_spanet_2 = h_spanet_2.GetValue()

h.SetLineWidth(2)
h_kin.SetLineWidth(2)
h_spanet.SetLineWidth(2)
h_spanet_2.SetLineWidth(2)

h.SetLineColor(ROOT.kRed)
h_kin.SetLineColor(ROOT.kBlue)
h_spanet.SetLineColor(ROOT.kGreen)
h_spanet_2.SetLineColor(ROOT.kBlack)

h.Scale(1./h.Integral())
h_kin.Scale(1./h_kin.Integral())
h_spanet.Scale(1./h_spanet.Integral())
h_spanet_2.Scale(1./h_spanet_2.Integral())


h.SetTitle(sample)

h.SetMaximum(h_spanet_2.GetMaximum()*2)
c = ROOT.TCanvas()



legend = ROOT.TLegend(0.23,0.44,0.94,0.92)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

legend.AddEntry(h,'ProbHHH6b')
legend.AddEntry(h_kin,'ProbHHH6b + ProbHH4b')
legend.AddEntry(h_spanet,'ProbHHH6b + ProbHH4b + ProbHHH4b2tau')
legend.AddEntry(h_spanet_2,'ProbHHH6b + ProbHH4b + ProbHHH4b2tau + ProbHH2b2tau')

h.SetStats(0)

h.Draw('hist e')
h_kin.Draw('hist e same')
h_spanet.Draw('hist e same')
h_spanet_2.Draw('hist e same')
legend.Draw()

c.Print('%s_%s_%s.png'%(sample,higgs,year))