# Script to symmetrise the uncertainties


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
args = parser.parse_args()


path = '/isilon/data/users/mstamenk/eos-triple-h/' + args.version + '/' + 'mva-inputs-%s-categorisation-spanet-boosted-classification'%args.year 
category = '%s_%s_inclusive_%s'%(args.prob,args.cat,args.opt)
filename = path + '/' + category + '/' + 'histograms/histograms_%s.root'%args.var

fileout = path + '/' + category + '/' + 'histograms/histograms_%s_symmetrised.root'%args.var

outfile = ROOT.TFile(fileout,'recreate')
print("Creating:%s"%fileout)



f_in = ROOT.TFile(filename)

histograms = [str(el.GetName()) for el in f_in.GetListOfKeys()]

print(histograms)

samples = []
systematics = []
for hist in histograms:
    if len(hist.split('_')) > 1:
        s_name = hist.split('_')[0] + '_' + hist.split('_')[1] # samples fetching
    else:
        s_name = hist
    if s_name not in samples:
        samples.append(s_name)
    
    syst_name = hist.replace(s_name,'').replace('_Up','').replace('_Down','') # systematics fetching
    if syst_name not in systematics and syst_name:
        systematics.append(syst_name)

print(samples)
print(systematics)


sample = samples[0]
syst = systematics[0]

first = True

for sample in samples:
    first = True
    nom = f_in.Get(sample)
    outfile.cd()
    nom.Write()
    print(sample)

    if 'QCD' not in sample and 'data_obs' not in sample:
        for syst in systematics:
            
            print(sample + syst)
            down = f_in.Get(sample+syst+'_Down')
            if 'JES' in syst: 
                up = f_in.Get(sample+syst+'_Up')
            else:
                up = nom.Clone(sample+syst+'_Up')
                up.SetTitle(sample+syst+'_Up')
                up.SetName(sample+syst+'_Up')

                delta = nom.Clone(sample+syst+'_delta')
                try:
                    delta.Add(down,-1)
                except: continue 

                up.Add(delta)
            outfile.cd()
            try:
                up.Write()
            except: continue
            down.Write()


outfile.Close()