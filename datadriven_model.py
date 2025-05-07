# Script to prepare histograms from which to sample randomly

import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--year', default='2017') 
parser.add_argument('--version', default = 'v34')
parser.add_argument('--doMC', action = 'store_true')
parser.add_argument('--type', default = 'resolved')
parser.add_argument('--path', default = '')
args = parser.parse_args()

from utils import init_get_max_prob, init_get_max_cat
import numpy as np
import random
from array import array 
import ROOT
import glob
import sys
import csv
csv.field_size_limit(sys.maxsize)
import os
import gc

init_get_max_prob()
init_get_max_cat()
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


if args.doMC:
    datas = {'2018' : 'QCD', 
         '2017' : 'QCD',
         '2016' : 'QCD',
         '2016APV' : 'QCD', 
         '2022' : 'QCD',
         '2022EE' : 'QCD',
    }
    
else:
    datas = {'2018' : 'JetHT', 
         '2017' : 'BTagCSV',
         '2016' : 'JetHT',
         '2016APV' : 'JetHT', 
         '2022' : 'JetMET',
         '2022EE' : 'JetMET',
    }

cat_cut = {
    'resolved' : "nfatjets == 0" ,
    'boosted'  : "nfatjets > 0"  ,
}

year = args.year
version = args.version
# path = '/eos/home-x/xiangran/samples/%s_%s/inclusive-weights/'%(year,version)
path = args.path
sample = datas[year]


for cat in [args.type]:
    # cat = args.type
    df = ROOT.RDataFrame('Events',path +'/inclusive-weights/' + sample + '.root')
    df = df.Define('IndexMaxProb', 'get_max_prob(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV, ProbHHH4b2tau, ProbHH4b, ProbHH2b2tau)')
    df = df.Define('IndexMaxCat', 'get_max_cat(Prob3bh0h, Prob2bh1h, Prob1bh2h, Prob0bh3h, Prob2bh0h, Prob1bh1h, Prob0bh2h, Prob1bh0h, Prob0bh1h, Prob0bh0h)')

    df_higgs = df.Filter('(IndexMaxProb == 1 || IndexMaxProb == 7) && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4 )')
    df_qcd = df.Filter('(IndexMaxProb != 1 && IndexMaxProb!= 7)')

    modelling_path = ''

    variables = [str(el) for el in df_qcd.GetColumnNames() if 'Prob' not in str(el) and 'IndexMaxProb' not in str(el) and 'mva' not in str(el) and 'counter' not in str(el) and 'CosPhi' not in str(el) and 'SinPhi' not in str(el) and 'LogPt' not in str(el) and 'PtCorr' not in str(el) and 'IndexMax' not in str(el)]

    print("Got reference")
    if args.doMC:
        df_higgs.Filter(cat_cut[cat])
    else:
        df_higgs.Filter(cat_cut[cat])

    variables = [str(el) for el in df_qcd.GetColumnNames() if 'Prob' not in str(el) and 'PNet' not in str(el) and 'IndexMaxProb' not in str(el) and 'mva' not in str(el) and 'counter' not in str(el) and 'CosPhi' not in str(el) and 'SinPhi' not in str(el) and 'LogPt' not in str(el) and 'PtCorr' not in str(el) and 'IndexMax' not in str(el)]
    print("Saving modelling")
    if args.doMC:
        df_qcd.Filter(cat_cut[cat]).Snapshot('Events', path+'/temp/mc_%s_modelling_%s.root'%(year,cat),variables)
    else:
        df_qcd.Filter(cat_cut[cat]).Snapshot('Events', path+'/temp/data_%s_modelling_%s.root'%(year,cat),variables)


    # # got PNetB, PNetXbb, PNetXjj, PNetQCD score from reference data

    out = 'jet1PNetB,jet2PNetB,jet3PNetB,jet4PNetB,jet5PNetB,jet6PNetB,jet7PNetB,jet8PNetB,jet9PNetB,jet10PNetB,fatJet1PNetXbb,fatJet2PNetXbb,fatJet3PNetXbb,fatJet1PNetXjj,fatJet2PNetXjj,fatJet3PNetXjj,fatJet1PNetQCD,fatJet2PNetQCD,fatJet3PNetQCD'
    columns = out.split(',')
    outputs = {}
    outputs[cat] = 'jet1PNetB,jet2PNetB,jet3PNetB,jet4PNetB,jet5PNetB,jet6PNetB,jet7PNetB,jet8PNetB,jet9PNetB,jet10PNetB,fatJet1PNetXbb,fatJet2PNetXbb,fatJet3PNetXbb,fatJet1PNetXjj,fatJet2PNetXjj,fatJet3PNetXjj,fatJet1PNetQCD,fatJet2PNetQCD,fatJet3PNetQCD\n'
    print(columns)
    np_dump = df_higgs.AsNumpy(columns)

    #add new PNetB, PNetXbb, PNetXjj, PNetQCD score to QCD modelling

    print("Running over:")
    if args.doMC:
        model_df = ROOT.RDataFrame('Events',path+'/temp/mc_%s_modelling_%s.root'%(year,cat))
    else:
        model_df = ROOT.RDataFrame('Events',path+'/temp/data_%s_modelling_%s.root'%(year,cat))
    model_df = model_df.Define('counter','counter++')

    entries = model_df.Count().GetValue()

    if args.doMC:
        data = list(zip(*np_dump.values()))
    else:
        data = list(zip(*np_dump.values()))
    # print(data)

    tot = len(data)
    if tot != df_higgs.Count().GetValue():
        print("len(data)",tot)
        print("df_higgs",df_higgs.Count().GetValue())
        continue
    print(tot,df_higgs.Count().GetValue())
    counter = 0
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
        rand = random.randint(0,tot-1)
        # print(rand)
        # print(data[rand])

        elements = data[rand]
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

        if counter % 3000 == 0: #print(counter, entries, float(counter)/entries)
            print("finished: ",float(counter)/entries)

        counter += 1

    print("Running over:")

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

    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet1, "jet1PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet2, "jet2PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet3, "jet3PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet4, "jet4PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet5, "jet5PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet6, "jet6PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet7, "jet7PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet8, "jet8PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet9, "jet9PNetB")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_jet10, "jet10PNetB")

    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj1_xbb, "fatJet1PNetXbb")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj1_xjj, "fatJet1PNetXjj")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj1_qcd, "fatJet1PNetQCD")

    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj2_xbb, "fatJet2PNetXbb")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj2_xjj, "fatJet2PNetXjj")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj2_qcd, "fatJet2PNetQCD")

    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj3_xbb, "fatJet3PNetXbb")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj3_xjj, "fatJet3PNetXjj")
    model_df = ROOT.AddArray(ROOT.RDF.AsRNode(model_df), arr_fj3_qcd, "fatJet3PNetQCD")

    print("Writing in")
    if args.doMC:
        print(path + '/' + 'QCD_mc_%s.root'%cat)
    else:
        print(path + '/' + 'QCD_datadriven_%s.root'%cat)
    variables = [str(el) for el in model_df.GetColumnNames() if 'counter' not in str(el) and 'CosPhi' not in str(el) and 'SinPhi' not in str(el) and 'LogPt' not in str(el) and 'PtCorr' not in str(el) and 'cosphi' not in str(el) and 'sinphi' not in str(el) and 'spanet' not in str(el)]

    if args.doMC:
        model_df.Snapshot('Events', path + '/' + 'QCD_mc_%s.root'%cat,variables)
    else:
        model_df.Snapshot('Events', path + '/' + 'QCD_datadriven_%s.root'%cat,variables)
        print("create QCD_datadriven successfully ! ")
    gc.collect() # clean menory
    sys.stdout.flush() # extra clean


