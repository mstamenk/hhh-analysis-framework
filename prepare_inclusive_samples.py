# Script to filter output from NanoAOD-tools into inclusive_resolved and inclusive_boosted

import os, ROOT

import glob

from machinelearning import init_bdt_boosted, add_bdt_boosted
from utils import init_mhhh, addMHHH, initialise_df,triggersCorrections
from calibrations import btag_init, addBTagSF, addBTagEffSF

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.ROOT.EnableImplicitMT()

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v28')
parser.add_argument('--year', default='2018') 
parser.add_argument('--f_in', default = 'GluGluToHHHTo6B_SM')
args = parser.parse_args()


version = args.version
year = args.year
path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-spanet-boosted-classification-variables-nanoaod'%(version,year)

output = '/isilon/data/users/mstamenk/eos-triple-h/%s-spanet-boosted-classification-variables/mva-inputs-%s/'%(version,year)


inclusive_resolved_4jets = 'inclusive_resolved_4jets'
inclusive_resolved = 'inclusive_resolved'
#inclusive_boosted = 'inclusive_boosted_mvacut0'
inclusive_boosted = 'inclusive_boosted'

cut_resolved_4jets = 'nsmalljets >= 4 && nsmalljets < 6 && nprobejets == 0'
cut_resolved = 'nsmalljets >= 6 && nprobejets == 0'
cut_boosted = 'nprobejets > 0 '
#cut_boosted = 'nprobejets > 0 && mvaBoosted[0] > 0.0'

if not os.path.isdir(output + '/' + inclusive_resolved_4jets):
    print("Creating %s"%(output + '/' + inclusive_resolved_4jets))
    os.makedirs(output + '/' + inclusive_resolved_4jets)

if not os.path.isdir(output + '/' + inclusive_resolved):
    print("Creating %s"%(output + '/' + inclusive_resolved))
    os.makedirs(output + '/' + inclusive_resolved)

if not os.path.isdir(output + '/' + inclusive_boosted):
    print("Creating %s"%(output + '/' + inclusive_boosted))
    os.makedirs(output + '/' + inclusive_boosted)


files = glob.glob(path + '/' + '*.root')
#for f_in in files:
f_in = args.f_in
f_name = os.path.basename(f_in)
print(f_name)

df = ROOT.RDataFrame('Events',f_in)

df_resolved = df.Filter(cut_resolved)
df_resolved_4jets = df.Filter(cut_resolved_4jets)
df_boosted = df.Filter(cut_boosted)

print("Running on %s"%f_in)
print("Doing resolved")
df_resolved.Snapshot('Events', output + '/' + inclusive_resolved + '/' + f_name)
print("Doing boosted")
df_boosted.Snapshot('Events', output + '/' + inclusive_boosted + '/' + f_name)
print("Doing resolved 4 jets")
df_resolved_4jets.Snapshot('Events', output + '/' + inclusive_resolved_4jets + '/' + f_name)

print("All done!")


