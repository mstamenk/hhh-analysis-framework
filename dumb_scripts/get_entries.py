
import ROOT
import shutil
import sys, os, re, shlex
import shutil,subprocess
import time
import os.path
from os import path
import gc

from optparse import OptionParser
parser = OptionParser()


parser.add_option("--base_folder ", type="string", dest="base", help="Folder in where to look for the categories", default='/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v28/2018/boost_resolved')
parser.add_option("--category ", type="string", dest="category", help="Category to compute it. if no argument is given will do all", default='none')
(options, args) = parser.parse_args()

base_folder=options.base
cat=options.category

if not cat == 'none' :
    categories = [cat]
else :
    categories = [

    # "v26_2016APV_nAK8_0_4L2M_SR_inclusive",
    # "v26_2016_nAK8_0_4L2M_SR_inclusive",
    # "v26_2017_nAK8_0_4L2M_SR_inclusive",
    # "v26_2018_nAK8_0_4L2M_SR_inclusive",

    # "gt5bloose_0PFfat_",
    # "gt5bloose_gt0medium_0PFfat_",
    # "gt5bloose_gt1medium_0PFfat_",
    # "gt5bloose_gt2medium_0PFfat_",

    # "gt5bloose_gt3medium_0PFfat_",
    # "gt5bloose_gt4medium_0PFfat_",
    # "gt5bmedium_0PFfat_",

    # "6l_1l_",
    # "6l_2l_",
    # "6l_mt1l_",
    # "6l_mt2l_",
    # "gt5bloose_0PFfat_no_bdt_cut_",
    # "no_cat_",

    # "gt5bloose_0PFfat_",
    # "gt5bloose_0PFfat_orthogonal_",
    # "gt5bmedium_0PFfat_",

   'ProbHHH6b_inclusive_' ,
   'ProbQCD_inclusive_'   ,
   'ProbTT_inclusive_'    ,
   'ProbVJets_inclusive_' ,
   'ProbVV_inclusive_'    ,
   'Probrest_inclusive'  ,
    #  'ProbQCD_3bh0h_inclusive_'  ,
    #  'ProbQCD_2bh1h_inclusive_'  ,
    #  'ProbQCD_1bh2h_inclusive_',
    #  'ProbQCD_0bh3h_inclusive_'  ,
    #  'ProbQCD_3Higgs_inclusive_'  ,
    #  'ProbTT_3bh0h_inclusive_'   ,
    #  'ProbTT_2bh1h_inclusive_'   ,
    #  'ProbTT_1bh2h_inclusive_'   ,
    #  'ProbTT_0bh3h_inclusive_'   ,
    #  'ProbTT_3Higgs_inclusive_'  ,
    #  'ProbVV_3Higgs_inclusive_'  ,
    #  'ProbVJets_3Higgs_inclusive_'  ,
#               'ProbVJets_3bh0h_inclusive','ProbVJets_2bh1h_inclusive','ProbVJets_1bh2h_inclusive','ProbVJets_0bh3h_inclusive','ProbVJets_3Higgs_inclusive','ProbVJets_rest_inclusive',
#               'ProbVV_3bh0h_inclusive'   ,'ProbVV_2bh1h_inclusive'   ,'ProbVV_1bh2h_inclusive'   ,'ProbVV_0bh3h_inclusive'   ,'ProbVV_3Higgs_inclusive'   ,'ProbVV_rest_inclusive',
#               'ProbHHH6b_3bh0h_inclusive','ProbHHH6b_2bh1h_inclusive','ProbHHH6b_1bh2h_inclusive','ProbHHH6b_0bh3h_inclusive','ProbHHH6b_3Higgs_inclusive' ]


    

    # "gt5bloose_0PFfat_SR",
    # "gt5bloose_gt0medium_0PFfat_SR",
    # "gt5bloose_gt1medium_0PFfat_SR",
    # "gt5bloose_gt2medium_0PFfat_SR",
    # "gt5bloose_gt3medium_0PFfat_SR",
    # "gt5bloose_gt4medium_0PFfat_SR",
    # "gt5bmedium_0PFfat_SR",
    
    # "gt5bloose_0PFfat_CR",
    # "gt5bloose_gt0medium_0PFfat_CR",
    # "gt5bloose_gt1medium_0PFfat_CR",
    # "gt5bloose_gt2medium_0PFfat_CR",
    # "gt5bloose_gt3medium_0PFfat_CR",
    # "gt5bloose_gt4medium_0PFfat_CR",
    # "gt5bmedium_0PFfat_CR",
    ]
    # "1PFfat",
    # "gt1PFfat"

#procstodo = ["ZZZ", "WZZ", "WWZ", "WWW", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TT", "QCD", "QCD6B", "GluGluToHHHTo6B_SM", "data_obs" ]
#procstodo = ["ZZZ", "WZZ", "WWZ", "WWW", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu" ,"TTToSemiLeptonic","QCD", "data_obs" , "GluGluToHHHTo6B_SM" ]
# procstodo = ["ZZZ", "WZZ", "WWZ", "WWW", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu","TTToSemiLeptonic", "QCD", "data_obs" , "GluGluToHHHTo6B_SM","QCD_bEnriched"]
#procstodo = ["WJetsToQQ"]
#
procstodo = ["DYJetsToLL","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau","GluGluToHHTo4B_cHHH1","TTToSemiLeptonic","WJetsToLNu_0J","WJetsToLNu_1J","WJetsToLNu_2J", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu", "QCD", "data_obs" , "GluGluToHHHTo6B_SM"]


inputTree = 'Events'

# Chalange:
# 1 - have an option to compute the yield with processes grouped as on the plotting
# 2 - make the script already output the yields in table format for all categories
#     tip: instead of print the values as you compute them do a dataframe to be fimming collumns and print at the end, or even save in a csv file

for category in categories :
    print("Computing for category: %s" % category )
    for proc in procstodo :
        input_file="{}/{}/{}.root".format(base_folder,category,proc)

        #tfile = ROOT.TFile(input_file)

        #try :
        #    tree = tfile.Get(inputTree)
        #except :
        #    #print("The file %s is not correctly done" % input_file)
        #    continue

        try :
            #chunk_arr = tree2array(tree)
            chunk_df = ROOT.RDataFrame(inputTree, input_file)
        except :
            print("{}: Yield  = {} | #events = {}".format(proc, 0, 0))
            print("fail")
            continue
        try :
            proc_yield = chunk_df.Sum('eventWeight')
        except :
            print("{}: Yield  = {} | #events = {}".format(proc, 0, 0))
            continue
        entries = chunk_df.Count()
        print("{}: Yield  = {} | #events = {}".format(proc, proc_yield.GetValue(), entries.GetValue()))
        #chunk_df.Close()
