# Script to add new PNetB, PNetXbb, PNetXjj, PNetQCD score to QCD sample based on histograms

import ROOT

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
parser.add_argument('--year', default='2018') 
args = parser.parse_args()

year = args.year
path = 'v33/mva-inputs-%s/inclusive-weights'%year

df = ROOT.RDataFrame('Events','data_%s_modelling.root'%year)
df = df.Define('counter','counter++')
#df = df.Filter('nprobejets > 0 || nsmalljets >= 4')


f = ROOT.TFile('histograms_data_%s_pnet_distribution.root'%year)

h_jet1 = f.Get('jet1PNetB')
h_jet2 = f.Get('jet2PNetB')
h_jet3 = f.Get('jet3PNetB')
h_jet4 = f.Get('jet4PNetB')
h_jet5 = f.Get('jet5PNetB')
h_jet6 = f.Get('jet6PNetB')
h_jet7 = f.Get('jet7PNetB')
h_jet8 = f.Get('jet8PNetB')
h_jet9 = f.Get('jet9PNetB')
h_jet10 = f.Get('jet10PNetB')

h_fj1_xbb = f.Get('fatJet1PNetXbb')
h_fj1_xjj = f.Get('fatJet1PNetXjj')
h_fj1_qcd = f.Get('fatJet1PNetQCD')

h_fj2_xbb = f.Get('fatJet2PNetXbb')
h_fj2_xjj = f.Get('fatJet2PNetXjj')
h_fj2_qcd = f.Get('fatJet2PNetQCD')
 
h_fj3_xbb = f.Get('fatJet3PNetXbb')
h_fj3_xjj = f.Get('fatJet3PNetXjj')
h_fj3_qcd = f.Get('fatJet3PNetQCD')

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
    jet1PNetB.append(h_jet1.GetRandom())
    jet2PNetB.append(h_jet2.GetRandom())
    jet3PNetB.append(h_jet3.GetRandom())
    jet4PNetB.append(h_jet4.GetRandom())
    jet5PNetB.append(h_jet5.GetRandom())
    jet6PNetB.append(h_jet6.GetRandom())
    jet7PNetB.append(h_jet7.GetRandom())
    jet8PNetB.append(h_jet8.GetRandom())
    jet9PNetB.append(h_jet9.GetRandom())
    jet10PNetB.append(h_jet10.GetRandom())

    fatJet1PNetXbb.append(h_fj1_xbb.GetRandom())
    fatJet2PNetXbb.append(h_fj2_xbb.GetRandom())
    fatJet3PNetXbb.append(h_fj3_xbb.GetRandom())

    fatJet1PNetXjj.append(h_fj1_xjj.GetRandom())
    fatJet2PNetXjj.append(h_fj2_xjj.GetRandom())
    fatJet3PNetXjj.append(h_fj3_xjj.GetRandom())

    fatJet1PNetQCD.append(h_fj1_qcd.GetRandom())
    fatJet2PNetQCD.append(h_fj2_qcd.GetRandom())
    fatJet3PNetQCD.append(h_fj3_qcd.GetRandom())



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
df.Snapshot('Events', path + '/' + 'QCD_datadriven.root',variables)


