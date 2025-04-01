# Script to add new PNetB, PNetXbb, PNetXjj, PNetQCD score to QCD sample based on histograms

import ROOT
import random
from array import array 
import glob
import sys


import csv
csv.field_size_limit(sys.maxsize)

import os

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
parser.add_argument('--doMC', action='store_true') 
parser.add_argument('--version', default='v33-3Higgs-test') 
#parser.add_argument('--lab', default = 'ak4_4_ak8_0')
args = parser.parse_args()

year = args.year
#lab = args.lab
version = args.version

path = '%s-2/mva-inputs-%s/inclusive-weights'%(version,year)

if not os.path.isdir(path):
    os.makedirs(path)

print("Running over:")
if args.doMC:
    print('samples-modelling-%s//mc_%s_modelling_%s.root'%(version,year,args.type))
    df = ROOT.RDataFrame('Events','samples-modelling-%s/mc_%s_modelling_%s.root'%(version,year,args.type))
else:
    print('samples-modelling-%s/data_%s_modelling_%s.root'%(version, year,args.type))
    df = ROOT.RDataFrame('Events','samples-modelling-%s/data_%s_modelling_%s.root'%(version,year,args.type))
df = df.Define('counter','counter++')

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


#csv_files = glob.glob('csv-files-v33/csv_%s_%s.dat'%(year,args.type))
#if 'boosted' in args.type:
#    csv_files = glob.glob('csv-files-v33/csv_%s_%s.dat'%(year,'ak4_*_ak8_1'))

if args.doMC:
    print('csv-files-%s/csv_mc_%s_%s_rdf.dat'%(version,year,args.type))
    with open('csv-files-%s/csv_mc_%s_%s_rdf.dat'%(version,year,args.type)) as csv_file:
        data  = csv_file.read().splitlines()
else:
    print('csv-files-%s/csv_%s_%s_rdf.dat'%(version,year,args.type))
    with open('csv-files-%s/csv_%s_%s_rdf.dat'%(version,year,args.type)) as csv_file:
        data  = csv_file.read().splitlines()

#print(csv_files)

tot = len(data)
counter = 0

for i in range(entries):
    rand = random.randint(1,tot -1)
    
    #print(data[rand])

    elements = data[rand].split(',')
    #print(elements)
    



    jet1PNetB.append(float(elements[0]))
    jet2PNetB.append(float(elements[1]))
    jet3PNetB.append(float(elements[2]))
    jet4PNetB.append(float(elements[3]))
    jet5PNetB.append(float(elements[4]))
    jet6PNetB.append(float(elements[5]))
    jet7PNetB.append(float(elements[6]))
    jet8PNetB.append(float(elements[7]))
    jet9PNetB.append(float(elements[8]))
    jet10PNetB.append(float(elements[9]))

    fatJet1PNetXbb.append(float(elements[10]))
    fatJet2PNetXbb.append(float(elements[11]))
    fatJet3PNetXbb.append(float(elements[12]))

    fatJet1PNetXjj.append(float(elements[13]))
    fatJet2PNetXjj.append(float(elements[14]))
    fatJet3PNetXjj.append(float(elements[15]))

    fatJet1PNetQCD.append(float(elements[16]))
    fatJet2PNetQCD.append(float(elements[17]))
    fatJet3PNetQCD.append(float(elements[18]))

    if counter % 1000 == 0: print(counter, entries, float(counter)/entries)

    counter += 1

print("Running over:")
print('samples-modelling-%s/data_%s_modelling_%s.root'%(version,year,args.type))

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

print("Writing in")
if args.doMC:
    print(path + '/' + 'QCD_mc_%s.root'%args.type)
else:
    print(path + '/' + 'QCD_datadriven_%s.root'%args.type)
variables = [str(el) for el in df.GetColumnNames() if 'counter' not in str(el) and 'CosPhi' not in str(el) and 'SinPhi' not in str(el) and 'LogPt' not in str(el) and 'PtCorr' not in str(el) and 'cosphi' not in str(el) and 'sinphi' not in str(el) and 'spanet' not in str(el)]

if args.doMC:
    df.Snapshot('Events', path + '/' + 'QCD_mc_%s.root'%args.type,variables)
else:
    df.Snapshot('Events', path + '/' + 'QCD_datadriven_%s.root'%args.type,variables)

