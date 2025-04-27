# Script to filter output from NanoAOD-tools into inclusive_resolved and inclusive_boosted

import os, ROOT

import glob

from machinelearning import init_bdt_boosted, add_bdt_boosted, init_bdt, add_bdt
from utils import init_mhhh, addMHHH, initialise_df,triggersCorrections, save_variables, matching_variables, hlt_paths
from calibrations import btag_init, addBTagSF, addBTagEffSF

from hhh_variables import add_hhh_variables, add_hhh_variables_resolved

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.ROOT.EnableImplicitMT()

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v31')
parser.add_argument('--year', default='2017')
parser.add_argument('--f_in', default = 'GluGluToHHHTo6B_SM')
args = parser.parse_args()

version = args.version
year = args.year
#path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-nanoaod'%(version,year)
#path = '/isilon/data/users/mstamenk/eos-triple-h/%s/mva-inputs-%s/inclusive_resolved/'%(version,year)

#path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-spanet-boosted-variables-nanoaod'%(version,year)
#path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-nanoaod'%(version,year)
# path = '/isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/condor/%s_ak8_option4_%s/*/parts/'%(version,year)
path = '/eos/cms/store/group/phys_higgs/cmshhh/%s_try_ak8_option4_%s/data/parts'%(version,year)


print(path)

# output = '/isilon/data/users/mstamenk/eos-triple-h/%s-parts/mva-inputs-%s/'%(version,year)
output = '/eos/cms/store/group/phys_higgs/cmshhh/%s_ak8_option4_%s/mva-inputs-%s'%(version,year,year)


inclusive_resolved = 'inclusive_resolved-weights'
inclusive_boosted = 'inclusive-weights'
#inclusive_boosted = 'inclusive_boosted'

cut_resolved = 'nsmalljets >= 4 && nprobejets == 0 && nloosebtags >= 4'
#cut_boosted = 'nprobejets > 0 '
cut_boosted = '(nprobejets > 0) || (nsmalljets >= 4 && nprobejets == 0 && nloosebtags >= 4)'

if not os.path.isdir(output + '/' + inclusive_resolved):
    print("Creating %s"%(output + '/' + inclusive_resolved))
    os.makedirs(output + '/' + inclusive_resolved)

if not os.path.isdir(output + '/' + inclusive_boosted):
    print("Creating %s"%(output + '/' + inclusive_boosted))
    os.makedirs(output + '/' + inclusive_boosted)

files = glob.glob(path + '/' + '*.root')

first = True

init_mhhh()


if '2016' in year:
    ROOT.gInterpreter.Declare(triggersCorrections['2016'][0])
else:
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

#for f_in in files:

f_in = args.f_in
f_name = os.path.basename(f_in)
print(f_name)

df = ROOT.RDataFrame('Events',f_in)

print(path+'/'+f_name)
#df = ROOT.RDataFrame('Events',f_in)
#if 'BTagCSV' in f_name:

cmd = '''
    Bool_t get_false(){return 0;}
'''

ROOT.gInterpreter.Declare(cmd)

list_inputs = [str(el) for el in df.GetColumnNames() ]
if 'HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2' not in list_inputs:
    df = df.Define('HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2','get_false()')
if 'HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1' not in list_inputs:
    df = df.Define('HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1','get_false()')
if 'HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1' not in list_inputs:
    df = df.Define('HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1','get_false()')
if 'HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2' not in list_inputs:   
    df = df.Define('HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2','get_false()')
if 'HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1' not in list_inputs:
    df = df.Define('HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1','get_false()')
if 'HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2' not in list_inputs:
    df = df.Define('HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2','get_false()')
if 'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94' not in list_inputs:
    df = df.Define('HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94','get_false()')
if 'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59' not in list_inputs:
    df = df.Define('HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59','get_false()')

if 'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4' not in list_inputs:
    df = df.Define('HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4','get_false()')

if 'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17' not in list_inputs:
    df = df.Define('HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17','get_false()')

if 'HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1' not in list_inputs:
    df = df.Define('HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1','get_false()')

if 'HLT_AK8PFJet330_PFAK8BTagCSV_p17' not in list_inputs:
    df = df.Define('HLT_AK8PFJet330_PFAK8BTagCSV_p17','get_false()')

if 'HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0' not in list_inputs:
    df = df.Define('HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0','get_false()')


if 'HLT_AK8PFHT750_TrimMass50' not in list_inputs:
    df = df.Define('HLT_AK8PFHT750_TrimMass50','get_false()')
if 'HLT_AK8PFJet400_TrimMass30' not in list_inputs:
    df = df.Define('HLT_AK8PFJet400_TrimMass30','get_false()')
if 'HLT_AK8PFJet360_TrimMass30' not in list_inputs:
    df = df.Define('HLT_AK8PFJet360_TrimMass30','get_false()')
if 'HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1' not in list_inputs:
    df = df.Define('HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1','get_false()')

if 'HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2' not in list_inputs:
    df = df.Define('HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2','get_false()')
if 'HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2' not in list_inputs:
    df = df.Define('HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2','get_false()')
if 'HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5' not in list_inputs:
    df = df.Define('HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5','get_false()')

hlt = hlt_paths[year]
df = df.Filter(hlt)

if first:
    init_bdt(df,year)
    init_bdt_boosted(df,year)
    first = False

df = initialise_df(df,year,f_in)

df,masses,pts,etas,phis,drs = add_hhh_variables_resolved(df)

df = add_bdt(df,year)
df = add_bdt_boosted(df,year)
if 'JetHT' not in f_in and 'BTagCSV' not in f_in and 'SingleMuon' not in f_in:
    df = matching_variables(df)

#df = df.Define('ProbMultiH','ProbHHH + ProbHH4b + ProbHHH4b2tau + ProbHH2b2tau')

df_resolved = df.Filter(cut_resolved)
df_boosted = df.Filter(cut_boosted)

print("Running on %s"%f_in)
print("Doing resolved")

to_save = [str(el) for el in df_boosted.GetColumnNames() if 'L1_' not in str(el) and 'v_' not in str(el) and 'MassRegressed' not in str(el) and 'bcand' not in str(el) and 'boostedTau_' not in str(el)]
print(to_save)
print(len(to_save))
#if not os.path.isfile( output + '/' + inclusive_resolved + '/' + f_name):
#df_resolved.Snapshot('Events', output + '/' + inclusive_resolved + '/' + f_name, to_save)
print("Doing boosted")

#if not os.path.isfile( output + '/' + inclusive_boosted + '/' + f_name):
#print(save_variables + ['eventWeight']+masses+pts+etas+phis+drs)

df_boosted.Snapshot('Events', output + '/' + inclusive_boosted + '/' + f_name, to_save)


print("All done!")