# Script to inspect the jet-veto-map file and how to use it
import correctionlib

from array import array
import ROOT


ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)


year = '2018'

era = {'2016APV': 'Summer19UL16_V0', '2016': 'Summer19UL16_V0', '2017': 'Summer19UL17_V2', '2018': 'Summer19UL18_V1','2022': 'Summer22_23Sep2023','2022EE':'Summer22EE_23Sep2023','2023':'Summer23Prompt23','2023BPIX':'Summer23BPixPrompt23'}[year]

correction_file = "JECDatabase/jet_veto_maps/%s/jetvetomaps.json.gz"%era

ceval = correctionlib.CorrectionSet.from_file(correction_file)

for corr in ceval.values():
    print(f"Correction {corr.name}")
    #for ix in corr.inputs:
    #    print(f"   Input {ix.name} ({ix.type}): {ix.description}")
