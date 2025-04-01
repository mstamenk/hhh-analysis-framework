# Script to add new PNetB, PNetXbb, PNetXjj, PNetQCD score to QCD sample based on histograms

import ROOT
import random
from array import array 

import csv

#ROOT.ROOT.EnableImplicitMT()



import numpy as np

ROOT.gInterpreter.Declare('''
ROOT::RDF::RNode AddArray(ROOT::RDF::RNode df, ROOT::RVec<double> &v, const std::string &name) {
    return df.Define(name, [&](unsigned int e) { return v[e]; }, {"counter"});
    }

ROOT::RDF::RNode AddBoolArray(ROOT::RDF::RNode df, ROOT::RVec<Long64_t> &v, const std::string &name) {
    unsigned rdf_entry = 0;
    return df.Define(name, [&](unsigned int e) { return v[e]; }, {"counter"});
}

unsigned counter = 0;
''')


import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--year', default='2018') 
parser.add_argument('--type', default='resolved') 
parser.add_argument('--doMC', action='store_true')
parser.add_argument('--version', default='v33-3Higgs-test') 
args = parser.parse_args()

year = args.year
path = 'v33/mva-inputs-%s/inclusive-weights'%year
version = args.version


#df = ROOT.RDataFrame('Events','data_%s_modelling_%s.root'%(year,args.type))
#df = df.Define('counter','counter++')
#df = df.Filter('nprobejets > 0 || nsmalljets >= 4')



#f = ROOT.TFile('data_%s_reference.root'%(year))
#tree = f.Events


#tot = tree.GetEntries()

out = 'jet1PNetB,jet2PNetB,jet3PNetB,jet4PNetB,jet5PNetB,jet6PNetB,jet7PNetB,jet8PNetB,jet9PNetB,jet10PNetB,fatJet1PNetXbb,fatJet2PNetXbb,fatJet3PNetXbb,fatJet1PNetXjj,fatJet2PNetXjj,fatJet3PNetXjj,fatJet1PNetQCD,fatJet2PNetQCD,fatJet3PNetQCD'

columns = out.split(',')


outputs = {}

#for ak4 in ['5','6','7','8','9','10']:
#for ak4 in ['10']:
#for ak8 in ['0','1','2','3']:
#        lab = 'ak4_%s_ak8_%s'%(ak4,ak8)

lab = args.type
outputs[lab] = 'jet1PNetB,jet2PNetB,jet3PNetB,jet4PNetB,jet5PNetB,jet6PNetB,jet7PNetB,jet8PNetB,jet9PNetB,jet10PNetB,fatJet1PNetXbb,fatJet2PNetXbb,fatJet3PNetXbb,fatJet1PNetXjj,fatJet2PNetXjj,fatJet3PNetXjj,fatJet1PNetQCD,fatJet2PNetQCD,fatJet3PNetQCD\n'

#f = ROOT.TFile('samples-reference-v33-resolved-boosted/data_%s_reference_%s.root'%(year,lab))
#tree = f.Events

print(columns)

if args.doMC:
    df = ROOT.RDataFrame('Events','samples-reference-%s/mc_%s_reference_%s.root'%(version,year,lab))
else:
    df = ROOT.RDataFrame('Events','samples-reference-%s/data_%s_reference_%s.root'%(version,year,lab))
#df = df.Range(0,10)

np_dump = df.AsNumpy(columns)
print(np_dump)

if args.doMC:
    with open('csv-files-%s/csv_mc_%s_%s_rdf.dat'%(version,year,lab), 'w') as csv_file:  
        writer = csv.writer(csv_file)
        #for key, value in np_dump.items():
        #writer.writerow([key, list(value)])
        writer.writerow(np_dump.keys())
        writer.writerows(zip(*np_dump.values()))
else:
    with open('csv-files-%s/csv_%s_%s_rdf.dat'%(version,year,lab), 'w') as csv_file:  
        writer = csv.writer(csv_file)
        #for key, value in np_dump.items():
        #writer.writerow([key, list(value)])
        writer.writerow(np_dump.keys())
        writer.writerows(zip(*np_dump.values()))

#np.savetxt("foo.csv", np_dump, delimiter=",")
