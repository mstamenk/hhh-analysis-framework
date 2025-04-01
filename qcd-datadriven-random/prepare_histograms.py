# Script to prepare histograms from which to sample randomly

import ROOT
ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)


import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--year', default='2018') 
parser.add_argument('--version', default = 'v33')
parser.add_argument('--doMC', action = 'store_true')
args = parser.parse_args()



from utils import init_get_max_prob, init_get_max_cat

init_get_max_prob()
init_get_max_cat()

binnings = {'1' : 100, 
            '2' : 100,
            '3' : 100,
            '4' : 100,
            '5' : 100,
            '6' : 100,
            '7' : 50,
            '8' : 50,
            '9' : 50,
            '10' : 50,
}

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


year = args.year
path = '/isilon/data/users/mstamenk/eos-triple-h/%s/mva-inputs-%s-categorisation-spanet-boosted-classification/'%(args.version,year)

#sample = 'QCD'

sample = datas[year]

df = ROOT.RDataFrame('Events',path +'/' + 'inclusive-weights/' + sample + '.root')

df = df.Define('IndexMaxProb', 'get_max_prob(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV, ProbHHH4b2tau, ProbHH4b, ProbHH2b2tau)')
df = df.Define('IndexMaxCat', 'get_max_cat(Prob3bh0h, Prob2bh1h, Prob1bh2h, Prob0bh3h, Prob2bh0h, Prob1bh1h, Prob0bh2h, Prob1bh0h, Prob0bh1h, Prob0bh0h)')



#df_higgs = ROOT.RDataFrame('Events',path +'/' + 'sr-weights/' + sample + '.root')

df_higgs = df.Filter('(IndexMaxProb == 1 || IndexMaxProb == 7) && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4 )')
#df_qcd = ROOT.RDataFrame('Events',path +'/' + 'bkg-weights/' + sample + '.root')
df_qcd = df.Filter('(IndexMaxProb != 1 && IndexMaxProb!= 7)')


#outfile = ROOT.TFile('histograms_data_%s_pnet_distribution.root'%year,'recreate')

'''
for jet in ['1','2','3','4','5','6','7','8','9','10']:
    varx = 'jet%sPNetB'%jet
    filter = 'jet%sPt > 20'%jet
    df_tmp = df_higgs.Filter(filter)
    
    binsx = 100 #binnings[jet]
    xmin = 0
    xmax = 1.0 

    h = df_tmp.Histo1D((varx,varx,binsx,xmin,xmax),varx,'eventWeight')
    h = h.GetValue()

    h.Scale(1./h.Integral())
    outfile.cd()
    h.SetTitle(varx)
    h.SetName(varx)
    h.Write()


for jet in ['1','2','3']:
    for var in ['Xbb','Xjj','QCD']:
        varx = 'fatJet%sPNet%s'%(jet,var)
        filter = 'fatJet%sPt > 200'%jet
        df_tmp = df_higgs.Filter(filter)
        
        binsx = 50 #binnings[jet]
        xmin = 0
        xmax = 1.0 

        h = df_tmp.Histo1D((varx,varx,binsx,xmin,xmax),varx,'eventWeight')
        h = h.GetValue()

        h.Scale(1./h.Integral())
        outfile.cd()
        h.SetTitle(varx)
        h.SetName(varx)
        h.Write()
'''

#outfile.Close()

variables = [str(el) for el in df_qcd.GetColumnNames() if 'Prob' not in str(el) and 'IndexMaxProb' not in str(el) and 'mva' not in str(el) and 'counter' not in str(el) and 'CosPhi' not in str(el) and 'SinPhi' not in str(el) and 'LogPt' not in str(el) and 'PtCorr' not in str(el) and 'IndexMax' not in str(el)]

print("Saving reference")

if args.doMC:
    df_higgs.Filter("nfatjets == 0").Snapshot('Events', 'samples-reference-v33-3Higgs/mc_%s_reference_resolved.root'%year,variables)
    df_higgs.Filter("nfatjets > 0").Snapshot('Events', 'samples-reference-v33-3Higgs/mc_%s_reference_boosted.root'%year,variables)
else:
    df_higgs.Filter("nfatjets == 0").Snapshot('Events', 'samples-reference-v33-3Higgs-test/data_%s_reference_resolved.root'%year,variables)
    df_higgs.Filter("nfatjets > 0").Snapshot('Events', 'samples-reference-v33-3Higgs-test/data_%s_reference_boosted.root'%year,variables)

#for ak4 in ['4','5','6','7','8','9','10']:
#    for ak8 in ['0','1','2','3']:
#        lab = 'ak4_%s_ak8_%s'%(ak4,ak8)
#        print(lab)
#        cut = "nsmalljets == %s && nfatjets == %s"%(ak4,ak8)
#        if '10' in ak4:
#            cut = "nsmalljets >= %s && nfatjets == %s"%(ak4,ak8)
#        df_higgs.Filter(cut).Snapshot('Events', 'samples-reference-v33/data_%s_%s_reference.root'%(year,#lab),variables)


# Save QCD file remaining without the Prob variables
variables = [str(el) for el in df_qcd.GetColumnNames() if 'Prob' not in str(el) and 'PNet' not in str(el) and 'IndexMaxProb' not in str(el) and 'mva' not in str(el) and 'counter' not in str(el) and 'CosPhi' not in str(el) and 'SinPhi' not in str(el) and 'LogPt' not in str(el) and 'PtCorr' not in str(el) and 'IndexMax' not in str(el)]
print("Saving modelling")

if args.doMC:
    df_qcd.Filter("nfatjets == 0").Snapshot('Events', 'samples-modelling-v33-3Higgs/mc_%s_modelling_resolved.root'%year,variables)
    df_qcd.Filter("nfatjets > 0").Snapshot('Events', 'samples-modelling-v33-3Higgs/mc_%s_modelling_boosted.root'%year,variables)
else:
    df_qcd.Filter("nfatjets == 0").Snapshot('Events', 'samples-modelling-v33-3Higgs-test/data_%s_modelling_resolved.root'%year,variables)
    df_qcd.Filter("nfatjets > 0").Snapshot('Events', 'samples-modelling-v33-3Higgs-test/data_%s_modelling_boosted.root'%year,variables)
#for ak4 in ['4','5','6','7','8','9','10']:
#    for ak8 in ['0','1','2','3']:
#        lab = 'ak4_%s_ak8_%s'%(ak4,ak8)
#        print(lab)
#        cut = "nsmalljets == %s && nfatjets == %s"%(ak4,ak8)
#        if '10' in ak4:
#            cut = "nsmalljets >= %s && nfatjets == %s"%(ak4,ak8)
#        df_qcd.Filter(cut).Snapshot('Events', 'samples-modelling-v33/data_%s_%s_modelling.root'%(year,lab),variables)

