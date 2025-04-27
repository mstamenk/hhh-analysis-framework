#from utils import wps_years
import ROOT
import shutil
import sys, os, re, shlex
from Correction_new import Unc_Shape
from array import array
#from subprocess import Popen, PIPE
#ROOT.ROOT.EnableImplicitMT()
#os.environ["MKL_NUM_THREADS"] = "1"
#os.environ["OMP_NUM_THREADS"] = "1"
import shutil,subprocess
import time
import os.path
from os import path
#from root_numpy import tree2array, array2tree
#import numpy as np
#import pandas
import glob
import gc

#import tdrstyle,CMS_lumi

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.ROOT.EnableImplicitMT()

from utils import histograms_dict, wps_years,ProbMultiH_cut, wps, tags, luminosities, hlt_paths, triggersCorrections, hist_properties, init_mhhh, addMHHH, clean_variables, initialise_df, save_variables, init_get_max_prob, init_get_max_cat
from machinelearning import init_bdt, add_bdt, init_bdt_boosted, add_bdt_boosted
from calibrations import btag_init, addBTagSF, addBTagEffSF
from hhh_variables import add_hhh_variables

from optparse import OptionParser
parser = OptionParser()
# parser.add_option("--base_folder ", type="string", dest="base", help="Folder in where to look for the categories", default='/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-2017-categorisation-spanet-boosted-classification/')
parser.add_option("--base_folder ", type="string", dest="base", help="Folder in where to look for the categories", default='/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-2017-categorisation-spanet-boosted-classification/')
# parser.add_option("--base_folder ", type="string", dest="base", help="Folder in where to look for the categories", default='/eos/cms/store/group/phys_higgs/cmshhh/v33-additional-samples/mva-inputs-2017-categorisation-spanet-boosted-classification/')
parser.add_option("--category ", type="string", dest="category", help="Category to compute it. if no argument is given will do all", default='none')
parser.add_option("--skip_do_trees", action="store_true", dest="skip_do_trees", help="Write...", default=False)
parser.add_option("--skip_do_histograms", action="store_true", dest="skip_do_histograms", help="Write...", default=False)
parser.add_option("--skip_do_plots", action="store_true", dest="skip_do_plots", help="Write...", default=False)
parser.add_option("--do_SR", action="store_true", dest="do_SR", help="Write...", default=False)
parser.add_option("--do_CR", action="store_true", dest="do_CR", help="Write...", default=False)
parser.add_option("--process ", type="string", dest="process_to_compute", help="Process to compute it. if no argument is given will do all", default='none')
parser.add_option("--do_limit_input ", type="string", dest="do_limit_input", help="If given it will do the histograms only in that variable with all the uncertainties", default='none')
parser.add_option("--skip_do_correct", action="store_true", dest="skip_do_correct", help="Write...", default=False)

## separate SR_CR as an option, this option would add _SR and _CR to the subfolder name
## add option to enter a process and if that is given to make the trees and histos only to it
## add option to add BDT computation here -- or not, we leave this only to MVA input variables -- the prefit plots already do data/MC
(options, args) = parser.parse_args()

do_limit_input      = options.do_limit_input ## X: to implement
process_to_compute = options.process_to_compute
do_SR              = options.do_SR
do_CR              = options.do_CR
skip_do_trees      = options.skip_do_trees
skip_do_histograms = options.skip_do_histograms
skip_do_plots      = options.skip_do_plots
skip_do_correct      = options.skip_do_correct
input_tree         = options.base
cat                = options.category

if do_SR and do_CR :
    print("You should chose to signal region OR control region")
    exit()

selections = {
    #"final_selection_jetMultiplicity" : "(nbtags > 4 && nfatjets == 0) || (nbtags > 2 && nfatjets > 0)",


     ########################### categories for resolved ###############################
    # SR for resolved 6L (bdt > 0.6 can change)
    "gt5bloose_0PFfat"              : {
        "sel" : "(nloosebtags > 5 && nprobejets == 0  && nleps == 0 && ntaus ==0 && mva[0] > 0.6)",
        "label" : "Resolved 6L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
    #SR for resolved 6L(exclude 6M from it) in order to combine 6L(veto 6M) and 6M
    "gt5bloose_0PFfat_orthogonal"              : {
        "sel" : "(nloosebtags > 5  && nmediumbtags <6  && nleps == 0 && ntaus ==0 && nprobejets == 0  && mva[0] > 0.6 )",
        "label" : "Resolved 6L(orthogonal)",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
    
    #SR for resolved 6M in order to combine 6L(veto 6M) and 6M
    "gt5bmedium_0PFfat"             : {
        "sel" : "(nmediumbtags > 5  && nleps == 0 && ntaus ==0 && nprobejets == 0 && mva[0] > 0.6 )",
        "label" : "Resolved 6M",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    #CR for purer ttbar need at least 2 leptons (still need some cut to make it purer)
    "6l_mt2l"              : {
        "sel" : "(nloosebtags >= 6 && nprobejets == 0 && nleps >= 2 && ntaus ==0)",
        "label" : "6l_mt2l",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },

    #CR for ttbar need at least one lepton (the cut is loose than 6l_mt2l)
    "6l_mt1l"              : {
        "sel" : "(nloosebtags >= 6 && nprobejets == 0 && nleps >= 1 && ntaus ==0 )",
        "label" : "6l_mt1l",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },

    #CR for W +jets need 1 lepton (still need cut for met to make it purer)
    "6l_1l"              : {
        "sel" : "(nloosebtags >= 6 && nprobejets == 0 && nleps == 1 && ntaus ==0 )",
        "label" : "6l_1l",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },

    #CR for Z + jets need 2 lepton (need cut for met to distinguish it from ttbar)
    "6l_2l"              : {
        "sel" : "(nloosebtags >= 6 && nprobejets == 0 && nleps == 2 && ntaus ==0 )",
        "label" : "6l_2l",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },




###################category for all####################

        "ProbHHH6b_inclusive"              : {
        "sel" : "(IndexMaxProb == 1  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
#################3Higgs################
        "Prob3Higgs_inclusive"              : {
        "sel" : "(IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4  )",
        "label" : "Prob3Higgs ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
#################3bh0h###############
        "Prob3bh0h_inclusive"              : {
        "sel" : "(IndexMaxCat == 1  )",
        "label" : "Prob3bh0h ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
####################2bh1h############
        "Prob2bh1h_inclusive"              : {
        "sel" : "(IndexMaxCat == 2  )",
        "label" : "Prob2bh1h ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
################1bh2h###############
        "Prob1bh2h_inclusive"              : {
        "sel" : "(IndexMaxCat == 3  )",
        "label" : "Prob1bh2h ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
###############0bh3h###############
        "Prob0bh3h_inclusive"              : {
        "sel" : "(IndexMaxCat == 4  )",
        "label" : "Prob0bh3h ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
################QCD################
        "ProbQCD_inclusive"              : {
        "sel" : "(IndexMaxProb == 2  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbQCD_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 2 && IndexMaxCat == 1  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbQCD_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 2 && IndexMaxCat == 2  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbQCD_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 2 && IndexMaxCat == 3  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbQCD_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 2 && IndexMaxCat == 4  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbQCD_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 2 && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbQCD_rest_inclusive"              : {
        "sel" : "(IndexMaxProb == 2 && (IndexMaxCat == 0 || IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 || IndexMaxCat == 8 || IndexMaxCat == 9))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
#########################TT######################
        "ProbTT_inclusive"              : {
        "sel" : "(IndexMaxProb == 3)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbTT_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 3 && IndexMaxCat == 1  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbTT_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 3 && IndexMaxCat == 2  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
        
        "ProbTT_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 3 && IndexMaxCat == 3  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbTT_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 3 && IndexMaxCat == 4  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbTT_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 3 && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4) )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbTT_rest_inclusive"              : {
        "sel" : "(IndexMaxProb == 3 && (IndexMaxCat == 0 || IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 || IndexMaxCat == 8 || IndexMaxCat == 9))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
###############VJets########################
        "ProbVJets_inclusive"              : {
        "sel" : "(IndexMaxProb == 4)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVJets_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxCat == 1  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVJets_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxCat == 2  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
        
        "ProbVJets_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxCat == 3  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVJets_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxCat == 4  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVJets_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4) )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVJets_rest_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && (IndexMaxCat == 0 || IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 || IndexMaxCat == 8 || IndexMaxCat == 9))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        ###################VV#################
        "ProbVV_inclusive"              : {
        "sel" : "(IndexMaxProb == 5)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVV_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && IndexMaxCat == 1  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVV_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && IndexMaxCat == 2  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
        
        "ProbVV_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && IndexMaxCat == 3  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVV_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && IndexMaxCat == 4  )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVV_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4) )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbVV_rest_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexMaxCat == 0 || IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 || IndexMaxCat == 8 || IndexMaxCat == 9))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },
        #####################DY###############

        


        ##################rest###############
        "Probrest_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 || IndexMaxProb == 7 || IndexMaxProb == 8)",
        "label" : "Probrest ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbHH4b_rest_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && (IndexMaxCat == 0 || IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 || IndexMaxCat == 8 || IndexMaxCat == 9))",
        "label" : "ProbHH4b_rest_inclusive ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "ProbHH4b_inclusive"              : {
        "sel" : "(IndexMaxProb == 7)",
        "label" : "ProbHH4b_inclusive ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

#################merge category####################
        "ProbQCD_semi_boosted_inclusive"              : {
        "sel" : "(IndexMaxProb == 2 &&(IndexMaxCat ==2 || IndexMaxCat ==3 || IndexMaxCat ==4))",
        "label" : "ProbQCD_semi_boosted ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "Probrest_3bh0h_inclusive"              : {
        "sel" : "((IndexMaxProb == 4 || IndexMaxProb == 5)&& IndexMaxCat ==1)",
        "label" : "Prob(VV+VJets)_3bh0h ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "Probrest_semi_boosted_inclusive"              : {
        "sel" : "((IndexMaxProb == 4 || IndexMaxProb == 5)&&(IndexMaxCat ==2 || IndexMaxCat ==3 || IndexMaxCat ==4))",
        "label" : "Prob(VV+VJets)_semi_boosted ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },

        "Probrest_3Higgs_inclusive"              : {
        "sel" : "((IndexMaxProb == 4 || IndexMaxProb == 5)&&(IndexMaxCat == 1 || IndexMaxCat ==2 || IndexMaxCat ==3 || IndexMaxCat ==4))",
        "label" : "Prob(VV+VJets)_semi_boosted ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0.2)",
        "dataset" : "-weights",
        },


         ##################HHH###############




    

        "ProbHHH6b_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 1 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHHH6b_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 2 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHHH6b_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 3 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHHH6b_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 4 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHHH6b_2bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 5)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHHH6b_1bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 6)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHHH6b_0bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 7)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHHH6b_1bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 8)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHHH6b_0bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 9)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHHH6b_0bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 0)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHHH6b_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHHH6b_2Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && (IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHHH6b_1Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && (IndexMaxCat == 8 || IndexMaxCat == 9 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
# HH
        "ProbHH4b_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 1 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHH4b_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 2 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHH4b_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 3 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHH4b_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 4 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHH4b_2bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 5)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0  ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbHH4b_1bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 6)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHH4b_0bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 7)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHH4b_1bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 8)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHH4b_0bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 9)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHH4b_0bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && IndexMaxCat == 0)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHH4b_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0  ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHH4b_2Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && (IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0  ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbHH4b_1Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 7 && (IndexMaxCat == 8 || IndexMaxCat == 9 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },

        "ProbVV_2Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0  ",
        "doCR" : "&& (ProbHHH > 0. && ht > 450 && (nmediumbtags >= 4 || nprobejets >= 2) )",
        "dataset" : "-weights",
        },
        "ProbVV_2bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexMaxCat == 5 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0. && ht > 450 && (nmediumbtags >= 4 || nprobejets >= 2) )",
        "dataset" : "-weights",
        },
        "ProbVV_1bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexMaxCat == 6))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0. && ht > 450 && (nmediumbtags >= 4 || nprobejets >= 2) )",
        "dataset" : "-weights",
        },
        "ProbVV_0bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexMaxCat == 7))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0. && ht > 450 && (nmediumbtags >= 4 || nprobejets >= 2) )",
        "dataset" : "-weights",
        },

        "test"              : {
        "sel" : "(nsmalljets >= 4)",
        "label" : "ProbHHH ",
        "doSR" : "&& nprobejets > 0",
        "doCR" : "&&  nprobejets == 0",
        "dataset" : "-weights",
        },



    ## you can add here categories with PN score
}

additional_selection = ""
additional_label     = ""
if do_SR : # done as attribute from the selections[selection]["doSR"] or selections[selection]["doCR"]
    #additional_selection = " && (h_fit_mass > 80 && h_fit_mass < 150)"
    additional_label     = "SR"
if do_CR :
    #additional_selection = " && !(h_fit_mass > 80 && h_fit_mass < 150)"
    additional_label     = "CR"

inputTree = 'Events'

# procstodo = ["DYJetsToLL","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau_SM","GluGluToHHTo4B_cHHH1","TTToSemiLeptonic","WJetsToLNu_0J","WJetsToLNu_1J","WJetsToLNu_2J", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu", "QCD", "data_obs" , "GluGluToHHHTo6B_SM","WWW","WWZ","WZZ","ZZZ"]
# procstodo = ["GluGluToHHTo4B_cHHH1","data_obs","GluGluToHHHTo6B_SM","QCD_datadriven","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau_SM","HHHTo6B_c3_0_d4_99","HHHTo6B_c3_0_d4_minus1","HHHTo6B_c3_19_d4_19","HHHTo6B_c3_1_d4_0","HHHTo6B_c3_1_d4_2","HHHTo6B_c3_2_d4_minus1","HHHTo6B_c3_4_d4_9","HHHTo6B_c3_minus1_d4_0","HHHTo6B_c3_minus1_d4_minus1","HHHTo6B_c3_minus1p5_d4_minus0p5"]
# procstodo = ["GluGluToHHTo4B_cHHH1","data_obs","GluGluToHHHTo6B_SM","QCD_datadriven","GluGluToHHHTo4B2Tau_SM","HHHTo6B_c3_0_d4_99","HHHTo6B_c3_0_d4_minus1","HHHTo6B_c3_19_d4_19","HHHTo6B_c3_1_d4_0","HHHTo6B_c3_1_d4_2","HHHTo6B_c3_2_d4_minus1","HHHTo6B_c3_4_d4_9","HHHTo6B_c3_minus1_d4_0","HHHTo6B_c3_minus1_d4_minus1","HHHTo6B_c3_minus1p5_d4_minus0p5"]
procstodo = ["GluGluToHHTo4B_cHHH1","data_obs","GluGluToHHHTo6B_SM","QCD_datadriven","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau_SM","GluGluToHHHTo6B_SMJERDOWN","GluGluToHHHTo6B_SMJERUP","GluGluToHHHTo6B_SMJESDOWN","GluGluToHHHTo6B_SMJESUP","GluGluToHHHTo6B_SMJMRDOWN","GluGluToHHHTo6B_SMJMRUP","GluGluToHHTo4B_cHHH1JERDOWN","GluGluToHHTo4B_cHHH1JERUP","GluGluToHHTo4B_cHHH1JESDOWN","GluGluToHHTo4B_cHHH1JESUP","GluGluToHHTo4B_cHHH1JMRDOWN","GluGluToHHTo4B_cHHH1JMRUP","GluGluToHHHTo4B2Tau_SMJERDOWN","GluGluToHHHTo4B2Tau_SMJERUP","GluGluToHHHTo4B2Tau_SMJESDOWN","GluGluToHHHTo4B2Tau_SMJESUP","GluGluToHHHTo4B2Tau_SMJMRDOWN","GluGluToHHHTo4B2Tau_SMJMRUP"]
if not process_to_compute == 'none' :
    procstodo     = [process_to_compute]
    skip_do_plots = True

for era in ['2016','2016APV',  '2017', '2018','2016APV201620172018'] :
#for era in [2018] :
    if str(era) in input_tree : year = str(era)

if '2016APV201620172018' in year:
    year = '2018'

wp_loose = wps_years['loose'][year]
wp_medium = wps_years['medium'][year]
wp_tight = wps_years['tight'][year]

# define function to run on mHHH
init_mhhh()
#if '2016' in year:
#    ROOT.gInterpreter.Declare(triggersCorrections['2016'][0])
#else:
#    ROOT.gInterpreter.Declare(triggersCorrections[year][0])
init_get_max_prob()
init_get_max_cat()


# define b-tagging
if '2016APV' in year:
    btag_init('2016preVFP')
elif '2016' in year:
    btag_init('2016postVFP')
else:
    btag_init(year)


csv_saved = False
for selection in selections.keys() :
  if not cat == 'none' :
      if not selection == cat :
          continue

  final_selection = selections[selection]["sel"]
  if do_SR:
      additional_selection = selections[selection]["doSR"]
  elif do_CR:
      additional_selection = selections[selection]["doCR"]
  if not additional_selection == "" :
      final_selection = "(%s %s)" % (selections[selection]["sel"], additional_selection)

  print("Doing tree skimmed for %s_%s" % (selection, additional_label))
  print(final_selection)

  output_tree = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new/%s"%(year)
  output_folder = "{}/{}_{}".format(output_tree,selection,additional_label)
  if not path.exists(output_folder) :
      procs=subprocess.Popen(['mkdir %s' % output_folder],shell=True,stdout=subprocess.PIPE)
      out = procs.stdout.read()
      print("made directory %s" % output_folder)

  if not skip_do_trees :
   print("1111111")

   firstProc = True
   for proctodo in procstodo :
    print("2222222")

    ## do that in a utils function
    datahist = proctodo
    if proctodo == "data_obs" :
        print(year)
        if year in ['2018', '2016', '2016APV']:
            datahist = 'JetHT'
            print("4444")
            print(year)

        else:
            datahist = 'BTagCSV'
            print("33331")

    outtree = "{}/{}_{}/{}.root".format(output_tree,selection,additional_label,proctodo)

    dataset = selections[selection]["dataset"] # inclusive_resolved or inclusive_boosted
    list_proc=glob.glob("{}/inclusive{}/{}.root".format(input_tree,dataset,datahist))
    
    print("Will create %s" % outtree)
    


    for proc in list_proc :
        #if not csv_saved :
        tlocal = time.localtime()
        current_time = time.strftime("%H:%M:%S", tlocal)
        print(current_time)
        seconds0 = time.time()
        print(proc)
        print("Cutting tree and saving it to ", outtree)
        print("With selection: ", final_selection)

        chunk_df = ROOT.RDataFrame(inputTree, proc)
        chunk_df = chunk_df.Define('ProbMultiH','ProbHHH + ProbHHH4b2tau + ProbHH4b + ProbHH2b2tau')
        chunk_df = chunk_df.Define('IndexMaxProb', 'get_max_prob(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV, ProbHHH4b2tau, ProbHH4b, ProbHH2b2tau)')
        chunk_df = chunk_df.Define('IndexMaxCat', 'get_max_cat(Prob3bh0h, Prob2bh1h, Prob1bh2h, Prob0bh3h, Prob2bh0h, Prob1bh1h, Prob0bh2h, Prob1bh0h, Prob0bh1h, Prob0bh0h)')
        # initialise df - so we don't need make_selection_rdataframes.py anymore
        print(dataset)
        if 'mvacut0' not in dataset and 'weights' not in dataset:
            chunk_df = initialise_df(chunk_df,year,proc) # mHHH done inside now
        
        if firstProc:
            #init_bdt(chunk_df,year)
            # init_bdt(chunk_df,year)
            # init_bdt_boosted(chunk_df,year)

            firstProc = False
        try:
            entries_no_filter = int(chunk_df.Count().GetValue())
        except:
            print('Error with %s'%proc)
            continue

        # Add mva and mvaBoosted variables (needs to happen before cutting on variables mva and mvaBoosted)
        if 'mvacut0' not in dataset and 'weights' not in dataset:
            chunk_df = add_bdt_boosted(chunk_df,year)
            chunk_df = add_bdt(chunk_df,year)

        chunk_df = chunk_df.Filter(final_selection)
        # chunk_df = chunk_df.Filter()
        chunk_df.Report().Print()
        entries = int(chunk_df.Count().GetValue())


        #print("cut made, tree size: ", int(tree.GetEntries()), int(tree_cut.GetEntries()))
        print("cut made, tree size: ", entries_no_filter, entries)
        print("starting to construct calibrations")
        variables = list(chunk_df.GetColumnNames())

        print("Cleaning variables", len(variables))
        #variables = clean_variables(variables)
        variables = save_variables

        ## if to do limit the cleaning will be different
        print("Cleaned variables", len(variables))
        #print(variables)
        ## cleaning is not working for all variables, even if explicitelly asking to remove all that name, and for some not cleaned variables will given
        ## Error in <TBranch::TBranch>: Illegal leaf: LHEReweightingWeight/LHEReweightingWeight[nLHEReweightingWeight]/F. If this is a variable size C array it's possible that the branch holding the size is not available
        ## Maybe because I do not source CMSSW

        ## symetrize angle variables
        for type_obj in ['fatJet', 'jet'] :
            for jet_number in range(1,11) :
                for angle in ['Eta', 'Phi'] :
                    obj = '{}{}{}'.format(type_obj,jet_number,angle)
                    if obj in variables :
                        #print("Take absolute of %s" % obj)
                        chunk_df = chunk_df.Define('Abs%s'%obj, "abs(%s)" % obj)
        #chunk_df = chunk_df.Define('Abshhh_eta', "abs(hhh_eta)")
                #chunk_df = chunk_df.Redefine('hh_phi', "abs(hh_phi)")
        
        print("2 - construct the eventWeight")
        to_multiply = []
        do_SF = True

        if selection == "gt5bloose_test" or selection == "gt5bloose_0PFfat" :
            nmedium_cut = 0
        elif selection == "gt5bloose_gt0medium_0PFfat" :
            nmedium_cut = 1
        elif selection == "gt5bloose_gt1medium_0PFfat" :
            nmedium_cut = 2
        elif selection == "gt5bloose_gt2medium_0PFfat" :
            nmedium_cut = 3
        elif selection == "gt5bloose_gt3medium_0PFfat" :
            nmedium_cut = 4
        elif selection == "gt5bloose_gt4medium_0PFfat" :
            nmedium_cut = 5
        elif selection == "gt5bmedium_0PFfat" :
            nmedium_cut = 6
        else :
            print("no SF ready to selection %s , we are ignoring it by the moment" % selection)
            do_SF = False

        if do_SF :
            for jet_number in range(1,nmedium_cut+1) :
                to_multiply = to_multiply + ['jet{}MediumBTagEffSF'.format(jet_number)]
            for jet_number in range(nmedium_cut+1,7) :
                to_multiply = to_multiply + ['jet{}LooseBTagEffSF'.format(jet_number)]
        string_multiply = 'eventWeight2'
        for ss in to_multiply :
            string_multiply = string_multiply + ' * {}'.format(ss)

        print( "Redefine eventWeight = {}".format(string_multiply))
        lumi = luminosities[year]
        # Re-definition of event weight to be used on v28 - will be fixed
        if 'BTagCSV' in datahist: cutWeight = '1' 
        elif'QCD_datadriven' in datahist: cutWeight = '1' 
        else: cutWeight = '(%f * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF)'%(lumi)
        chunk_df = chunk_df.Define('eventWeight2', cutWeight)
        chunk_df = chunk_df.Define('totalWeight', string_multiply)

        proc_yield = chunk_df.Sum('totalWeight')
        print("Yield:", proc_yield.GetValue())

        print(variables)
        #if 'JetHT' in proctodo or 'data_obs' in proctodo:
        #    chunk_df = chunk_df.Define('jet1HadronFlavour', '-1')
        #    chunk_df = chunk_df.Define('jet2HadronFlavour', '-1')
        #    chunk_df = chunk_df.Define('jet3HadronFlavour', '-1')
        #    chunk_df = chunk_df.Define('jet4HadronFlavour', '-1')
        #    chunk_df = chunk_df.Define('jet5HadronFlavrou', '-1')
        #    chunk_df = chunk_df.Define('jet6HadronFlavrou', '-1')

        #chunk_df.Snapshot(inputTree, outtree, variables + ['totalWeight'])
        to_save = [str(el) for el in chunk_df.GetColumnNames() if 'mva' not in str(el)]

        chunk_df.Snapshot(inputTree, outtree,to_save)

        gc.collect() # clean menory
        sys.stdout.flush() # extra clean

        seconds = time.time()
        print("Seconds to load : ", seconds-seconds0)
        print("Minutes to load : ", (seconds-seconds0)/60.0)

  ## do Histograms -- reorganize to do directly limits
  output_histos = "{}/{}_{}/histograms".format(output_tree,selection,additional_label)
  if not path.exists(output_histos) :
    procs=subprocess.Popen(['mkdir %s' % output_histos],shell=True,stdout=subprocess.PIPE)
    out = procs.stdout.read()

  data_value = -1

  if not skip_do_histograms : # args.doHistograms:
    ## already doing plots, will do histogram file only to the chosen variable
    seconds0 = time.time()
    #histograms = []
    proctodo = "GluGluToHHHTo6B_SM" ## for taking the list of variables and doing the first histogram in the file
    outtree = "{}/{}_{}/{}.root".format(output_tree,selection,additional_label,proctodo)

    chunk_df = ROOT.RDataFrame(inputTree, outtree)
    variables = chunk_df.GetColumnNames()


    print("Will produce histograms for following variables:")
    print(do_limit_input)
    for var in variables: # booking all variables to be produced

        #template = ROOT.TH1F("", "", histograms_dict[do_limit_input]["nbins"], histograms_dict[do_limit_input]["xmin"], histograms_dict[do_limit_input]["xmax"])
        # Define histograms to be produced === make that can be a list
        if do_limit_input == var :

            if do_limit_input == 'ProbMultiH':
                xmin = ProbMultiH_cut[cat]
            else: 
                xmin = histograms_dict[do_limit_input]["xmin"]
            nbins = histograms_dict[do_limit_input]["nbins"]
            xmax = histograms_dict[do_limit_input]["xmax"]
            # define_bins = histograms_dict[do_limit_input]["define_bins"]
            print("11111111")

            try :
                histograms_dict[do_limit_input]
            except :
                print("The binning options for the variable %s should be added in utils" % do_limit_input)
                exit()

            if do_limit_input == 'ProbMultiH':
                nameout = output_histos + '/' + 'histograms_%s_regubin_scale.root'%(do_limit_input)
                # nameout = output_histos + '/' + 'histograms_%s_regubin.root'%(do_limit_input)
            else:
                nameout = output_histos + '/' + 'histograms_%s_scale.root'%(do_limit_input)
                # nameout = output_histos + '/' + 'histograms_%s.root'%(do_limit_input)



            f_out = ROOT.TFile(nameout, 'recreate')
            print("Writing in %s" % nameout)

            f_out.cd()
            for proctodo in procstodo :
                outtree = "{}/{}_{}/{}.root".format(output_tree,selection,additional_label,proctodo) ## make better, to not have to call it twice


                try :
                    chunk_df = ROOT.RDataFrame(inputTree, outtree)
                    # chunk_df.Filter("%s > %s"%(char_var,xmin))
                except :
                    print("process %s has 0 entries, skipping doing the histogram" % proctodo)
                    continue

                datahist = proctodo
                if proctodo == "data_obs" :
                    if year == '2018' or year == '2016' or year == '2016APV' or year == '2016APV201620172018' :
                        datahist = 'JetHT'
                    else:
                        datahist = 'BTagCSV'
                    
                
                char_var = var.c_str()
                try:
                    #h_tmp = chunk_df.Fill(template, [char_var, 'totalWeight'])
                    f_out.cd()
                    # h_tmp = chunk_df.Filter("%s > %s"%(char_var,xmin)).Histo1D((char_var,char_var,nbins,array('d',define_bins)),char_var,'totalWeight')
                    h_tmp = chunk_df.Filter("%s > %s"%(char_var,xmin)).Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'totalWeight')
                    if proctodo == "data_obs":
                        data_value = h_tmp.Integral()
                        print("already get the data value !!!!!!!!!!!!!")
                        print(h_tmp.Integral())

                    if proctodo == "QCD_datadriven":
                        print(h_tmp.Integral())
                        h_tmp.Scale(data_value/h_tmp.Integral())
                        print("already scale the QCD !!!!!!!!!!!!!")
                        print(h_tmp.Integral())

                    


                    # h_tmp.SetTitle('%s_tmp'%(proctodo))
                    # h_tmp.SetName('%s_tmp'%(proctodo))
                    # h_uni = ROOT.TH1F(char_var,char_var,nbins,0,nbins)
                    # h_uni.SetTitle('%s'%(proctodo))
                    # h_uni.SetName('%s'%(proctodo))

                    # for i in range(1, h_uni.GetNbinsX()+1):
                    #     data_tmp = h_tmp.GetBinContent(i)
                    #     e_data_tmp = h_tmp.GetBinError(i)
                    #     h_uni.SetBinContent(i, data_tmp)
                    #     h_uni.SetBinError(i, e_data_tmp)
                    # h_uni.Write()
                    if proctodo == "HHHTo6B_c3_0_d4_minus1":
                        proctodo = "c3_0_d4_m1"
                        h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_19_d4_19":
                         proctodo = "c3_19_d4_19"
                         h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_1_d4_0":
                         proctodo = "c3_1_d4_0"
                         h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_1_d4_2":
                         proctodo = "c3_1_d4_2"
                         h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_2_d4_minus1":
                         proctodo = "c3_2_d4_m1"
                         h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_4_d4_9":
                         proctodo = "c3_4_d4_9"
                         h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_minus1_d4_0":
                         proctodo = "c3_m1_d4_0"
                         h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_minus1_d4_minus1":
                         proctodo = "c3_m1_d4_m1"
                         h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_minus1p5_d4_minus0p5":
                         proctodo = "c3_m1p5_d4_m0p5"
                         h_tmp.Scale(5.46)
                    elif proctodo == "HHHTo6B_c3_0_d4_99":
                         proctodo = "c3_0_d4_99"
                         h_tmp.Scale(5.46)
                    elif proctodo == "GluGluToHHHTo6B_SM":
                         proctodo = "c3_0_d4_0"

                    h_tmp.SetTitle('%s'%(proctodo))
                    h_tmp.SetName('%s'%(proctodo))
                    h_tmp.Write()

                except:
                    print("%s likely has 0 events"%proctodo)

            f_out.Close()
            seconds = time.time()
            print("Seconds to load : ", seconds-seconds0)
            #print("Minutes to load : ", (seconds-seconds0)/60.0)

  if not skip_do_plots :
      # Draw the data/MC to this selection
      path_to_plots = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/plots/v33_new/%s/'%(year)
      
      output_folder_draw = "{}/{}_{}/".format(path_to_plots,selection,additional_label)
      if not path.exists(output_folder_draw) :
        procs=subprocess.Popen(['mkdir %s' % output_folder],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
      print("made directory %s" % output_folder_draw)

    #   command = "python3 draw_data_mc_categories.py --input_folder %s --plot_label '%s (%s)' --output_folder %s" % (output_histos.replace('histograms',''), selections[selection]["label"], additional_label,output_folder_draw)
      command = "python3 draw_data_mc_categories.py --input_folder %s --plot_label '%s (%s)' --output_folder %s" % (output_histos.replace('histograms',''), selections[selection]["label"], additional_label,output_folder_draw)
      #if "0PFfat" in selection :
      #command = command + " --log"
      print(command)

      proc=subprocess.Popen([command],shell=True,stdout=subprocess.PIPE)
      out = proc.stdout.read()

  if not skip_do_correct :
    # path_to_histograms = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new/%s'%(year)
    path_to_histograms = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new/run2_separate'

    Higgs_number_strings = ["3Higgs","2Higgs","3bh0h","2bh1h","1bh2h","0bh3h","2bh0h","1bh1h","0bh2h"]
    # Higgs_number_strings = ["3Higgs"]
    for Higgs_number in Higgs_number_strings: 
        file_1Higgs = "{}/ProbHHH6b_1Higgs_inclusive_/histograms/histograms_{}.root".format(path_to_histograms,do_limit_input)
        file_2Higgs = "{}/ProbHHH6b_{}_inclusive_/histograms/histograms_{}.root".format(path_to_histograms,Higgs_number,do_limit_input)
        Unc_Shape(file_1Higgs,file_2Higgs,do_limit_input,path_to_histograms,Higgs_number,year)
    
    