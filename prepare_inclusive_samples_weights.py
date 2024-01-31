# Script to filter output from NanoAOD-tools into inclusive_resolved and inclusive_boosted

import os, ROOT

import glob

from machinelearning import init_bdt_boosted, add_bdt_boosted, init_bdt, add_bdt
from utils import init_mhhh, addMHHH, initialise_df,triggersCorrections, save_variables, matching_variables, hlt_paths, GetAllTriggers
from calibrations import btag_init, addBTagSF, addBTagEffSF

from hhh_variables import add_hhh_variables, add_hhh_variables_resolved, add_missing_variables

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.ROOT.EnableImplicitMT()

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v28')
parser.add_argument('--year', default='2018')
parser.add_argument('--f_in', default='') # GluGluToHHHTo6B_SM
parser.add_argument('--path', default='/isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/condor/')
parser.add_argument('--output', default='/isilon/data/users/mstamenk/eos-triple-h/')
args = parser.parse_args()

version = args.version
year = args.year
#path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-nanoaod'%(version,year)
#path = '/isilon/data/users/mstamenk/eos-triple-h/%s/mva-inputs-%s/inclusive_resolved/'%(version,year)

#path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-spanet-boosted-variables-nanoaod'%(version,year)
#path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-nanoaod'%(version,year)
path = os.path.join(args.path, '%s_ak8_option4_%s'%(version,year), '*', 'parts')

print(path)

output = os.path.join(args.output, '%s-parts-no-lhe'%version, 'mva-inputs-%s'%year)

cutlist = {
    "inclusive": ['inclusive-weights', '1.0'],
    "combined": ['inclusive_combined-weights', '(nprobejets > 0) || (nprobetaus > 0) || (nsmalljets >= 2) || (ntaus >= 2)'],
    #"resolved": ['inclusive_resolved-weights', 'nsmalljets >= 4 && nprobejets == 0'],
    #"boosted": ['inclusive_boosted-weights', '(nprobejets > 0) || (nprobetaus > 0) || (nsmalljets >= 4 && nprobejets == 0 && nloosebtags >= 4) || (nsmalljets >= 2 && nprobejets == 0 && nloosebtags >= 2 && ntaus>=2)']
}


#cut_boosted = '(nprobejets > -1)'

for cut in cutlist:
    if not os.path.isdir(output + '/' + cutlist[cut][0]):
        print("Creating %s"%(output + '/' + cutlist[cut][0]))
        os.makedirs(output + '/' + cutlist[cut][0])

files = glob.glob(path + '/' + '*.root')
if args.f_in!='': files = [args.f_in]

first = True

init_mhhh()


if '2016' in year:
    ROOT.gInterpreter.Declare(triggersCorrections['2016'][0])
elif '2022' not in year: # TODO: No SFs yet for 2022/2022EE
    ROOT.gInterpreter.Declare(triggersCorrections[year][0])

if '2016APV' in year:
    btag_init('2016preVFP')
elif '2016' in year:
    btag_init('2016postVFP')
else:
    btag_init(year)

if '2017' in year:
    data_files = ['BTagCSV.root']
else:
    data_files = ['JetHT.root']

inited = False
for f_in in files:

    f_name = os.path.basename(f_in)
    print(f_name)

    df = ROOT.RDataFrame('Events',f_in)

    print(path+'/'+f_name)
    #df = ROOT.RDataFrame('Events',f_in)
    #if 'BTagCSV' in f_name:

    cmd = '''
        Bool_t get_false(){return 0;}
    '''

    if not inited:
        ROOT.gInterpreter.Declare(cmd)

    list_inputs = [str(el) for el in df.GetColumnNames() ]
    #MustHaveTriggers = ['HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2', 'HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1', 'HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1', 'HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2', 'HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1', 'HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2', 'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94', 'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59', 'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4', 'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17', 'HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1', 'HLT_AK8PFJet330_PFAK8BTagCSV_p17', 'HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0', 'HLT_AK8PFHT750_TrimMass50', 'HLT_AK8PFJet400_TrimMass30', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1', 'HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2', 'HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2', 'HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5', 'HLT_AK8PFJet450']
    # Do we need all a branch for all triggers of all years?
    MustHaveTriggers = GetAllTriggers()
    MustHaveTriggers = [trig for y in MustHaveTriggers for trig in MustHaveTriggers[y]]
    MustHaveTriggers = list(dict.fromkeys(MustHaveTriggers))
    # Or just ensure we have all for the corresponding era?
    #MustHaveTriggers = [trig for trig in GetAllTriggers[year]]
    for trig in MustHaveTriggers:
        if trig not in list_inputs:
            df = df.Define(trig,'get_false()')
    hlt = hlt_paths[year]
    df = df.Filter(hlt)

    if first:
        init_bdt(df,year)
        init_bdt_boosted(df,year)
        first = False

    df = initialise_df(df,year,f_in)

    if "2022" in year and not inited:
        add_missing_variables()
    inited = True
    df,masses,pts,etas,phis,drs = add_hhh_variables_resolved(df)

    df = add_bdt(df,year)
    df = add_bdt_boosted(df,year)
    if 'JetHT' not in f_in and 'BTagCSV' not in f_in and 'SingleMuon' not in f_in:
        df = matching_variables(df)

    #df = df.Define('ProbMultiH','ProbHHH + ProbHH4b + ProbHHH4b2tau + ProbHH2b2tau')

    dfs = {}
    for cut in cutlist:
        dfs[cut] = df.Filter(cutlist[cut][1])

    print("Running on %s"%f_in)
    #to_save = [str(el) for el in df_boosted.GetColumnNames() if 'L1_' not in str(el) and 'v_' not in str(el) and 'MassRegressed' not in str(el) and 'bcand' not in str(el) and 'boostedTau_' not in str(el) and 'PNet' not in str(el)]

    for cut in cutlist:
        print("Doing", cut, "for", f_name)
        if os.path.isfile( output + '/' + cutlist[cut][0] + '/' + f_name): continue

        to_save = [str(el) for el in dfs[cut].GetColumnNames() if 'L1_' not in str(el) and 'v_' not in str(el) and 'MassRegressed' not in str(el) and 'bcand' not in str(el) and 'boostedTau_' not in str(el) and 'LHE' not in str(el)]
        print(to_save)
        print(len(to_save))

        dfs[cut].Snapshot('Events', output + '/' + cutlist[cut][0] + '/' + f_name, to_save)


    #print(save_variables + ['eventWeight']+masses+pts+etas+phis+drs)


print("All done!")



