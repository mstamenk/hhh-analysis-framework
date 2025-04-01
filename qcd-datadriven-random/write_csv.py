# Script to add new PNetB, PNetXbb, PNetXjj, PNetQCD score to QCD sample based on histograms

import ROOT
import random
from array import array 

ROOT.ROOT.EnableImplicitMT()

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
parser.add_argument('--year', default='2017') 
parser.add_argument('--type', default='resolved') 
args = parser.parse_args()

year = args.year
path = 'v32/mva-inputs-%s/inclusive-weights'%year

#df = ROOT.RDataFrame('Events','data_%s_modelling_%s.root'%(year,args.type))
#df = df.Define('counter','counter++')
#df = df.Filter('nprobejets > 0 || nsmalljets >= 4')



#f = ROOT.TFile('data_%s_reference.root'%(year))
#tree = f.Events


#tot = tree.GetEntries()

out = 'jet1PNetB,jet2PNetB,jet3PNetB,jet4PNetB,jet5PNetB,jet6PNetB,jet7PNetB,jet8PNetB,jet9PNetB,jet10PNetB,fatJet1PNetXbb,fatJet2PNetXbb,fatJet3PNetXbb,fatJet1PNetXjj,fatJet2PNetXjj,fatJet3PNetXjj,fatJet1PNetQCD,fatJet2PNetQCD,fatJet3PNetQCD\n'


outputs = {}

#for ak4 in ['5','6','7','8','9','10']:
#for ak4 in ['10']:
#for ak8 in ['0','1','2','3']:
#        lab = 'ak4_%s_ak8_%s'%(ak4,ak8)

lab = args.type
outputs[lab] = 'jet1PNetB,jet2PNetB,jet3PNetB,jet4PNetB,jet5PNetB,jet6PNetB,jet7PNetB,jet8PNetB,jet9PNetB,jet10PNetB,fatJet1PNetXbb,fatJet2PNetXbb,fatJet3PNetXbb,fatJet1PNetXjj,fatJet2PNetXjj,fatJet3PNetXjj,fatJet1PNetQCD,fatJet2PNetQCD,fatJet3PNetQCD\n'

f = ROOT.TFile('samples-reference-v33-resolved-boosted/data_%s_reference_%s.root'%(year,lab))
tree = f.Events


tot = tree.GetEntries()
counter = 0
for event in tree:
    # jet PNet B
    jet1PNetB = event.jet1PNetB
    jet2PNetB = event.jet2PNetB
    jet3PNetB = event.jet3PNetB
    jet4PNetB = event.jet4PNetB
    jet5PNetB = event.jet5PNetB
    jet6PNetB = event.jet6PNetB
    jet7PNetB = event.jet7PNetB
    jet8PNetB = event.jet8PNetB
    jet9PNetB = event.jet9PNetB
    jet10PNetB = event.jet10PNetB

    fatJet1PNetXbb = event.fatJet1PNetXbb
    fatJet2PNetXbb = event.fatJet2PNetXbb
    fatJet3PNetXbb = event.fatJet3PNetXbb

    fatJet1PNetXjj = event.fatJet1PNetXjj
    fatJet2PNetXjj = event.fatJet2PNetXjj
    fatJet3PNetXjj = event.fatJet3PNetXjj

    fatJet1PNetQCD = event.fatJet1PNetQCD
    fatJet2PNetQCD = event.fatJet2PNetQCD
    fatJet3PNetQCD = event.fatJet3PNetQCD

    
    #lab = 'ak4_%d_ak8_%d'%(event.nsmalljets,event.nfatjets)
    #if event.nsmalljets >= 10:
    #    lab = 'ak4_10_ak8_%d'%(event.nfatjets)
    #out+= '%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n'%(jet1PNetB,jet2PNetB,jet3PNetB,jet4PNetB,jet5PNetB,jet6PNetB,jet7PNetB,jet8PNetB,jet9PNetB,jet10PNetB,fatJet1PNetXbb,fatJet2PNetXbb,fatJet3PNetXbb,fatJet1PNetXjj,fatJet2PNetXjj,fatJet3PNetXjj,fatJet1PNetQCD,fatJet2PNetQCD,fatJet3PNetQCD)

    outputs[lab] += '%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n'%(jet1PNetB,jet2PNetB,jet3PNetB,jet4PNetB,jet5PNetB,jet6PNetB,jet7PNetB,jet8PNetB,jet9PNetB,jet10PNetB,fatJet1PNetXbb,fatJet2PNetXbb,fatJet3PNetXbb,fatJet1PNetXjj,fatJet2PNetXjj,fatJet3PNetXjj,fatJet1PNetQCD,fatJet2PNetQCD,fatJet3PNetQCD)
    counter+=1
    
    if counter % 1000 == 0: print(counter,tot, float(counter)/tot)

    #if counter > 10 : break


print("Writing", 'csv-files-v33/csv_%s_%s.dat'%(year,lab))
with open('csv-files-v33/csv_%s_%s.dat'%(year,lab), 'w') as f:
    f.write(outputs[lab])

'''
entries = df.Count().GetValue()

jet1PNetB = []
jet2PNetB = []
jet3PNetB = []
jet4PNetB = []
jet5PNetB = []
jet6PNetB = []
jet7PNetB = []
jet8PNetB = []
jet9PNetB = []
jet10PNetB = []

fatJet1PNetXbb = []
fatJet1PNetXjj = []
fatJet1PNetQCD = []

fatJet2PNetXbb = []
fatJet2PNetXjj = []
fatJet2PNetQCD = []

fatJet3PNetXbb = []
fatJet3PNetXjj = []
fatJet3PNetQCD = []

for i in range(entries):
    rand = random.randint(0,tot)
    tree.GetEntry(rand)

    jet1PNetB.append(tree.GetLeaf("jet1PNetB").GetValue(0))
    jet2PNetB.append(tree.GetLeaf("jet2PNetB").GetValue(0))
    jet3PNetB.append(tree.GetLeaf("jet3PNetB").GetValue(0))
    jet4PNetB.append(tree.GetLeaf("jet4PNetB").GetValue(0))
    jet5PNetB.append(tree.GetLeaf("jet5PNetB").GetValue(0))
    jet6PNetB.append(tree.GetLeaf("jet6PNetB").GetValue(0))
    jet7PNetB.append(tree.GetLeaf("jet7PNetB").GetValue(0))
    jet8PNetB.append(tree.GetLeaf("jet8PNetB").GetValue(0))
    jet9PNetB.append(tree.GetLeaf("jet9PNetB").GetValue(0))
    jet10PNetB.append(tree.GetLeaf("jet10PNetB").GetValue(0))

    fatJet1PNetXbb.append(tree.GetLeaf("fatJet1PNetXbb").GetValue(0))
    fatJet2PNetXbb.append(tree.GetLeaf("fatJet2PNetXbb").GetValue(0))
    fatJet3PNetXbb.append(tree.GetLeaf("fatJet3PNetXbb").GetValue(0))

    fatJet1PNetXjj.append(tree.GetLeaf("fatJet1PNetXjj").GetValue(0))
    fatJet2PNetXjj.append(tree.GetLeaf("fatJet2PNetXjj").GetValue(0))
    fatJet3PNetXjj.append(tree.GetLeaf("fatJet3PNetXjj").GetValue(0))

    fatJet1PNetQCD.append(tree.GetLeaf("fatJet1PNetQCD").GetValue(0))
    fatJet2PNetQCD.append(tree.GetLeaf("fatJet2PNetQCD").GetValue(0))
    fatJet3PNetQCD.append(tree.GetLeaf("fatJet3PNetQCD").GetValue(0))


arr_jet1 = ROOT.VecOps.AsRVec(np.array(jet1PNetB))
arr_jet2 = ROOT.VecOps.AsRVec(np.array(jet2PNetB))
arr_jet3 = ROOT.VecOps.AsRVec(np.array(jet3PNetB))
arr_jet4 = ROOT.VecOps.AsRVec(np.array(jet4PNetB))
arr_jet5 = ROOT.VecOps.AsRVec(np.array(jet5PNetB))
arr_jet6 = ROOT.VecOps.AsRVec(np.array(jet6PNetB))
arr_jet7 = ROOT.VecOps.AsRVec(np.array(jet7PNetB))
arr_jet8 = ROOT.VecOps.AsRVec(np.array(jet8PNetB))
arr_jet9 = ROOT.VecOps.AsRVec(np.array(jet9PNetB))
arr_jet10 = ROOT.VecOps.AsRVec(np.array(jet10PNetB))

arr_fj1_xbb = ROOT.VecOps.AsRVec(np.array(fatJet1PNetXbb))
arr_fj1_xjj = ROOT.VecOps.AsRVec(np.array(fatJet1PNetXjj))
arr_fj1_qcd = ROOT.VecOps.AsRVec(np.array(fatJet1PNetQCD))

arr_fj2_xbb = ROOT.VecOps.AsRVec(np.array(fatJet2PNetXbb))
arr_fj2_xjj = ROOT.VecOps.AsRVec(np.array(fatJet2PNetXjj))
arr_fj2_qcd = ROOT.VecOps.AsRVec(np.array(fatJet2PNetQCD))

arr_fj3_xbb = ROOT.VecOps.AsRVec(np.array(fatJet3PNetXbb))
arr_fj3_xjj = ROOT.VecOps.AsRVec(np.array(fatJet3PNetXjj))
arr_fj3_qcd = ROOT.VecOps.AsRVec(np.array(fatJet3PNetQCD))

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet1, "jet1PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet2, "jet2PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet3, "jet3PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet4, "jet4PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet5, "jet5PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet6, "jet6PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet7, "jet7PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet8, "jet8PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet9, "jet9PNetB")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_jet10, "jet10PNetB")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj1_xbb, "fatJet1PNetXbb")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj1_xjj, "fatJet1PNetXjj")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj1_qcd, "fatJet1PNetQCD")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj2_xbb, "fatJet2PNetXbb")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj2_xjj, "fatJet2PNetXjj")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj2_qcd, "fatJet2PNetQCD")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj3_xbb, "fatJet3PNetXbb")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj3_xjj, "fatJet3PNetXjj")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_fj3_qcd, "fatJet3PNetQCD")


variables = [str(el) for el in df.GetColumnNames() if 'counter' not in str(el) and 'CosPhi' not in str(el) and 'SinPhi' not in str(el) and 'LogPt' not in str(el) and 'PtCorr' not in str(el) and 'cosphi' not in str(el) and 'sinphi' not in str(el) and 'spanet' not in str(el)]
df.Snapshot('Events', path + '/' + 'QCD_datadriven_%s.root'%args.type,variables)

'''