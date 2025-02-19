import os, ROOT,glob

ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v33')
parser.add_argument('--year', default='2016APV201620172018')
parser.add_argument('--prob', default='ProbHHH6b')
parser.add_argument('--cat', default='3Higgs')
parser.add_argument('--var', default = 'ProbMultiH')
parser.add_argument('--opt', default = 'CR')
parser.add_argument('--doLog', action = 'store_true')
args = parser.parse_args()

path = '/isilon/data/users/mstamenk/eos-triple-h/' + args.version + '/' + 'mva-inputs-%s-categorisation-spanet-boosted-classification'%args.year 
category = '%s_%s_inclusive_%s'%(args.prob,args.cat,args.opt)
filename = path + '/' + category + '/' + 'histograms/histograms_%s_symmetrised.root'%args.var


output = 'syst_symmetrised_%s_%s_%s'%(args.prob,args.cat,args.opt)

if not os.path.isdir(output):
    os.makedirs(output)


f_in = ROOT.TFile(filename)

histograms = [str(el.GetName()) for el in f_in.GetListOfKeys() if 'data_obs' not in str(el.GetName()) and 'QCD' not in str(el.GetName())]

print(histograms)

samples = []
systematics = []
for hist in histograms:
    s_name = hist.split('_')[0] + '_' + hist.split('_')[1] # samples fetching
    if s_name not in samples:
        samples.append(s_name)
    
    syst_name = hist.replace(s_name,'').replace('_Up','').replace('_Down','') # systematics fetching
    if syst_name not in systematics and syst_name:
        systematics.append(syst_name)

print(samples)
print(systematics)


sample = samples[0]
syst = systematics[0]


for sample in samples:
    first = True
    for syst in systematics:
        nom = f_in.Get(sample)
        print(sample + syst)
        up = f_in.Get(sample+syst+'_Up')
        down = f_in.Get(sample+syst+'_Down')



        nom.SetStats(0)
        if first:
            nom.SetMaximum(2.0*nom.GetMaximum())
            first = False
        nom.GetXaxis().SetTitle('ProbMultiH')
        nom.SetLineColor(ROOT.kBlack)
        nom.SetLineWidth(2)

        try:
            up.SetLineColor(ROOT.kBlue + 2)
        except: continue
        up.SetLineWidth(2)
        down.SetLineColor(ROOT.kRed+2)
        down.SetLineWidth(2)

        c = ROOT.TCanvas()
        legend = ROOT.TLegend(0.6,0.6,0.89,0.89)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)

        legend.AddEntry(nom,'Nominal')
        legend.AddEntry(up,'+1 #sigma')
        legend.AddEntry(down,'-1 #sigma')

        nom.SetTitle(sample + syst)

        nom.Draw('hist e')
        up.Draw('hist e same')
        down.Draw('hist e same')
        legend.Draw()

        c.Print(output + '/' + '%s.png'%(sample+syst))




