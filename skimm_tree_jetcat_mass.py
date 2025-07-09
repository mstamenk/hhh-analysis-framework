#from utils import wps_years
import ROOT
import shutil
import sys, os, re, shlex
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

from utils_jet_newest import histograms_dict, wps_years, wps, tags, luminosities, hlt_paths, triggersCorrections, hist_properties, init_mhhh, addMHHH, clean_variables, initialise_df, save_variables, init_get_max_prob, init_get_max_cat,init_get_hand_cat, applySelection, init_get_max_prob_v34, add_correction_factor,addFJMinPtCut,addMinPtCut
from machinelearning import init_bdt, add_bdt, init_bdt_boosted, add_bdt_boosted
from calibrations import btag_init, addBTagSF, addBTagEffSF
from hhh_variables import add_hhh_variables


from optparse import OptionParser
parser = OptionParser()
parser.add_option("--base_folder ", type="string", dest="base", help="Folder in where to look for the categories", default='/isilon/data/users/mstamenk/eos-triple-h/v27-spanet-boosted-classification-variables/mva-inputs-2018/')
parser.add_option("--category ", type="string", dest="category", help="Category to compute it. if no argument is given will do all", default='none')
parser.add_option("--skip_do_trees", action="store_true", dest="skip_do_trees", help="Write...", default=False)
parser.add_option("--skip_do_histograms", action="store_true", dest="skip_do_histograms", help="Write...", default=False)
parser.add_option("--skip_do_plots", action="store_true", dest="skip_do_plots", help="Write...", default=False)
parser.add_option("--do_SR", action="store_true", dest="do_SR", help="Write...", default=False)
parser.add_option("--do_CR", action="store_true", dest="do_CR", help="Write...", default=False)
parser.add_option("--process ", type="string", dest="process_to_compute", help="Process to compute it. if no argument is given will do all", default='none')
parser.add_option("--do_limit_input ", type="string", dest="do_limit_input", help="If given it will do the histograms only in that variable with all the uncertainties", default='none')
parser.add_option("--run_all_categories ",  dest="run_all_categories", help="Run on all ProbHHH6b and ProbHH4b categories in a for loop", action='store_true', default = False)

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
input_tree         = options.base
cat                = options.category
run_all_categories = options.run_all_categories

if do_SR and do_CR :
    print("You should chose to signal region OR control region")
    exit()

selections = {
    #"final_selection_jetMultiplicity" : "(nbtags > 4 && nfatjets 
    # Start of SR definition

        "ProbTT_inclusive"              : {
        "sel" : "(IndexMaxProb == 3)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbTT_v34 > 0.0 ",
        "doCR" : "&& (ProbTT_v34 > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH6b_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1 && IndexHandCat == 1 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHHH6b_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 2 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHHH6b_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 3 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHHH6b_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 4 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHHH6b_2bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 5)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHHH6b_1bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 6)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHHH6b_0bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 7)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHHH6b_1bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 8)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHHH6b_0bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 9)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHHH6b_0bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && IndexHandCat == 0)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },



        "ProbHHH6b_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && (IndexHandCat == 1 || IndexHandCat == 2 || IndexHandCat == 3 || IndexHandCat == 4))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt) )",
        "dataset" : "-weights",
        },
        "ProbHHH6b_2Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && (IndexHandCat == 5 || IndexHandCat == 6 || IndexHandCat == 7 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0 && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHHH6b_1Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxProbOld == 1  && (IndexHandCat == 8 || IndexHandCat == 9 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450   && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
# HH
        "ProbHH4b_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 1 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHH4b_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 2 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHH4b_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 3 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHH4b_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 4 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHH4b_2bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 5)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0  ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbHH4b_1bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 6)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450   && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHH4b_0bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 7)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHH4b_1bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 8)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHH4b_0bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 9)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHH4b_0bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && IndexHandCat == 0)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHH4b_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && (IndexHandCat == 1 || IndexHandCat == 2 || IndexHandCat == 3 || IndexHandCat == 4))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0  ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt) )",
        "dataset" : "-weights",
        },
        "ProbHH4b_2Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && (IndexHandCat == 5 || IndexHandCat == 6 || IndexHandCat == 7 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },
        "ProbHH4b_1Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 4 && IndexMaxProbOld == 4 && (IndexHandCat == 8 || IndexHandCat == 9 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450  && (passMinPt||passFJMinPt))",
        "dataset" : "-weights",
        },

        "ProbVV_2Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexHandCat == 5 || IndexHandCat == 6 || IndexHandCat == 7 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0  ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        "ProbVV_2bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexHandCat == 5 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0. && ht > 450 && (nmediumbtags >= 4 || nprobejets >= 2) )",
        "dataset" : "-weights",
        },
        "ProbVV_1bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 5 && (IndexHandCat == 6))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbHHH > 0.0 ",
        "doCR" : "&& (ProbHHH > 0. && ht > 450 && (nmediumbtags >= 4 || nprobejets >= 2) )",
        "dataset" : "-weights",
        },

        # HHH4b2tau
        "ProbHHH4b2tau_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && (IndexHandCat == 1 || IndexHandCat == 8 || IndexHandCat == 3 || IndexHandCat == 4))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450)",
        "dataset" : "-weights",
        },
        "ProbHHH4b2tau_2Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && (IndexHandCat == 5 || IndexHandCat == 6 || IndexHandCat == 7 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0 && ht > 450)",
        "dataset" : "-weights",
        },
        "ProbHHH4b2tau_1Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && (IndexHandCat == 8 || IndexHandCat == 9 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH4b2tau_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 1 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH4b2tau_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 2 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH4b2tau_1bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 3 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH4b2tau_0bh3h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 4 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH4b2tau_2bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 5)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH4b2tau_1bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 6)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450)",
        "dataset" : "-weights",
        },
        "ProbHHH4b2tau_0bh2h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 7)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450)",
        "dataset" : "-weights",
        },
        "ProbHHH4b2tau_1bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 8)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450)",
        "dataset" : "-weights",
        },
        "ProbHHH4b2tau_0bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 9)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0.0 && ht > 450)",
        "dataset" : "-weights",
        },
        "ProbHHH4b2tau_0bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 6 && IndexHandCat == 0)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH > 0.0 ",
        "doCR" : "&& (ProbMultiH > 0. && ht > 450)",
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

procstodo = ["ZZZ", "WZZ", "WWZ", "WWW", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTo2L2Nu","TTToSemiLeptonic", "QCD", "data_obs","DYJetsToLL","GluGluToHHHTo6B_SM","GluGluToHHTo4B_cHHH1","GluGluToHHTo2B2Tau","GluGluToHHHTo4B2Tau_SM","QCD_datadriven"]


if not process_to_compute == 'none' :
    procstodo     = [process_to_compute]
    skip_do_plots = True

for era in ['2016','2016APV', '2017', '2018','2016APV201620172018','2022','2022EE'] :
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
init_get_max_prob_v34()
init_get_max_cat()
init_get_hand_cat()



# define b-tagging
if '2016APV' in year:
    btag_init('2016preVFP')
elif '2016' in year:
    btag_init('2016postVFP')
elif '2022' in year:
    btag_init('2018')
else:
    btag_init(year)


csv_saved = False
category_list = selections.keys()
if run_all_categories:
    category_list = ['ProbHHH6b_3bh0h_inclusive', 'ProbHHH6b_2bh1h_inclusive', 'ProbHHH6b_1bh2h_inclusive', 'ProbHHH6b_0bh3h_inclusive', 'ProbHHH6b_2bh0h_inclusive', 'ProbHHH6b_1bh1h_inclusive', 'ProbHHH6b_0bh2h_inclusive','ProbHHH6b_0bh0h_inclusive',"ProbHHH6b_1Higgs_inclusive","ProbHHH6b_2Higgs_inclusive","ProbHHH6b_3Higgs_inclusive"]
    #category_list = ['ProbHH4b_3Higgs_inclusive','ProbHH4b_2Higgs_inclusive', 'ProbHH4b_1Higgs_inclusive','ProbHH4b_0bh0h_inclusive','ProbHHH6b_3Higgs_inclusive','ProbHHH6b_2Higgs_inclusive','ProbHHH6b_1Higgs_inclusive','ProbHHH6b_0bh0h_inclusive']
for selection in category_list:
  if not cat == 'none' :
      if not selection == cat :
          continue

  final_selection = selections[selection]["sel"]
  if do_SR:
      additional_selection = selections[selection]["doSR"]
  elif do_CR:
      additional_selection = selections[selection]["doCR"]
      if '2016' in year:
          hlt = hlt_paths['2016']
      else:
          hlt = hlt_paths[year]
      additional_selection += ' && %s'%(hlt)
  if not additional_selection == "" :
      final_selection = "(%s %s)" % (selections[selection]["sel"], additional_selection)

  print("Doing tree skimmed for %s_%s" % (selection, additional_label))
  print(final_selection)
  output_tree = "/eos/cms/store/group/phys_higgs/cmshhh/v34-test/jet_couting_cat/%s"%(year)
  output_folder = "{}/{}_{}".format(output_tree,selection,additional_label)
  if not path.exists(output_folder) :
      procs=subprocess.Popen(['mkdir %s' % output_folder],shell=True,stdout=subprocess.PIPE)
      out = procs.stdout.read()
      print("made directory %s" % output_folder)

  if not skip_do_trees :

   firstProc = True
   for proctodo in procstodo :

    ## do that in a utils function
    datahist = proctodo
    if proctodo == "data_obs" :
        if year == '2018' or '2016' in year:
            datahist = 'JetHT'
        elif year == '2017':
            datahist = 'BTagCSV'
        elif '2022' in year:
            datahist = 'JetMET'

    outtree = "{}/{}_{}/{}.root".format(output_tree,selection,additional_label,proctodo)

    dataset = selections[selection]["dataset"] # inclusive_resolved or inclusive_boosted
    print("Dataset: ", dataset)
    list_proc=glob.glob("{}/inclusive{}/{}.root".format(input_tree,dataset,datahist))
    # print("{}/inclusive{}/{}.root".format(input_tree,dataset,datahist))
    # print("List of processes to compute: ", list_proc)
    print("Will create %s" % outtree)


    for proc in list_proc :
        #if not csv_saved :
        tlocal = time.localtime()
        current_time = time.strftime("%H:%M:%S", tlocal)
        print(current_time)
        seconds0 = time.time()
        print("Reading from:",proc)
        print("Cutting tree and saving it to ", outtree)
        print("With selection: ", final_selection)

      
       


        chunk_df = ROOT.RDataFrame(inputTree, proc)
        for i in range(1, 11):  # 遍历 jet1 到 jet10
        # 定义变量名
            pnet_b_cat = f"jet{i}PNetTagCat"
            pass_btag_branch = f"jet{i}PassBtag"
            cut_jet = 6

            # # 添加新的 branch，判断是否满足 Btag 条件
            chunk_df  = chunk_df.Define(pass_btag_branch, f"({pnet_b_cat} > {cut_jet}) ? 1 : 0")

            # 添加新的 branch，判断是否满足 Btag 条件
            
        for i in range(1, 4):  # 遍历 fatJet1 到 fatJet4
            # 定义变量名
            pnet_xbb_cat = f"fatJet{i}PNetXbbTagCat"
            pass_btag_branch = f"fatJet{i}PassBtag"
            cut_fatjet = 0
            # 添加新的 branch，判断是否满足 Btag 条件
         
            chunk_df = chunk_df.Define(pass_btag_branch, f"({pnet_xbb_cat} > {cut_fatjet}) ? 1 : 0")



        chunk_df = chunk_df.Define('nJetsPassed', 'jet1PassBtag + jet2PassBtag + jet3PassBtag + jet4PassBtag + jet5PassBtag + jet6PassBtag + jet7PassBtag + jet8PassBtag + jet9PassBtag + jet10PassBtag')
        chunk_df = chunk_df.Define('nFatJetsPassed', 'fatJet1PassBtag + fatJet2PassBtag + fatJet3PassBtag')

        #####apply 2 training
        #marko inclusive training
        chunk_df = chunk_df.Define('ProbMultiHOld','ProbHHH_v34 + ProbHH4b_v34')
        chunk_df = chunk_df.Define('IndexMaxProbOld', 'get_max_prob_v34(ProbHHH_v34, ProbQCD_v34, ProbTT_v34, ProbHH4b_v34)')
        #marko HHH6b training, 
        chunk_df = chunk_df.Define('ProbMultiH','ProbHHH_v34bis + ProbHH4b_v34bis')
        chunk_df = chunk_df.Define('IndexMaxProb', 'get_max_prob_v34(ProbHHH_v34bis, ProbQCD_v34bis, ProbTT_v34bis, ProbHH4b_v34bis)')
            #marko new v34 categorisation training
        chunk_df = chunk_df.Define('IndexMaxCat', 'get_max_cat(Prob3bh0h_v34, Prob2bh1h_v34, Prob1bh2h_v34, Prob0bh3h_v34, Prob2bh0h_v34, Prob1bh1h_v34, Prob0bh2h_v34, Prob1bh0h_v34, Prob0bh1h_v34, Prob0bh0h_v34)') 
        chunk_df = chunk_df.Define('IndexHandCat', 'get_hand_cat(nFatJetsPassed, nJetsPassed, hhh_mass)')

        chunk_df = chunk_df.Define('Prob3Higgs','Prob3bh0h+Prob2bh1h+Prob1bh2h+Prob0bh3h')
        chunk_df = chunk_df.Define('Prob2Higgs','Prob2bh0h+Prob1bh1h+Prob0bh2h')
        chunk_df = chunk_df.Define('Prob1Higgs','Prob1bh0h+Prob0bh1h')
        chunk_df = chunk_df.Define('Prob0Higgs','Prob0bh0h')
        chunk_df = chunk_df.Define('Prob3Higgs_v34','Prob3bh0h_v34+Prob2bh1h_v34+Prob1bh2h_v34+Prob0bh3h_v34')
        chunk_df = chunk_df.Define('Prob2Higgs_v34','Prob2bh0h_v34+Prob1bh1h_v34+Prob0bh2h_v34')
        chunk_df = chunk_df.Define('Prob1Higgs_v34','Prob1bh0h_v34+Prob0bh1h_v34')
        chunk_df = chunk_df.Define('Prob0Higgs_v34','Prob0bh0h_v34')
        # initialise df - so we don't need make_selection_rdataframes.py anymore
        print(dataset)
        if 'mvacut0' not in dataset and 'weights' not in dataset:
            chunk_df = initialise_df(chunk_df,year,proc) # mHHH done inside now
        
        if firstProc:
            #init_bdt(chunk_df,year)
            if '2022' in year:
                init_bdt(chunk_df,'2018')
                init_bdt_boosted(chunk_df,'2018')
            else:
                init_bdt(chunk_df,year)
                init_bdt_boosted(chunk_df,year)

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


        chunk_df = applySelection(chunk_df,year)
        chunk_df = addMinPtCut(chunk_df)
        chunk_df = addFJMinPtCut(chunk_df)
        
        chunk_df = chunk_df.Filter(final_selection)
        entries = int(chunk_df.Count().GetValue())


        #print("cut made, tree size: ", int(tree.GetEntries()), (tree_cut.GetEntries()))
        print("cut made, tree size: ", entries_no_filter, entries)
        print("starting to construct calibrations")
        variables = list(chunk_df.GetColumnNames())

        print("Cleaning variables", len(variables))
        #variables = clean_variables(variables)
        variables = save_variables

        ## if to do limit the cleaning will be different
        print("Cleaned variables", len(variables))
        
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

        string_multiply = 'eventWeight'
        
        print( "Redefine eventWeight = {}".format(string_multiply))
        lumi = luminosities[year]
        

        chunk_df = chunk_df.Define('totalWeight', string_multiply)

        proc_yield = chunk_df.Sum('totalWeight')
        print("Yield:", proc_yield.GetValue())

        print(variables)
         
        to_save = [str(el) for el in chunk_df.GetColumnNames() if 'mva' not in str(el) and 'HLT' not in str(el)]



        chunk_df.Snapshot(inputTree, outtree,to_save)

        gc.collect() # clean menory
        sys.stdout.flush() # extra clean

        seconds = time.time()
        print("Seconds to load : ", seconds-seconds0)
        print("Minutes to load : ", (seconds-seconds0)/60.0)

  