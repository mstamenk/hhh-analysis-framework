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

from utils import histograms_dict, wps_years, wps, tags, luminosities, hlt_paths, triggersCorrections, hist_properties, init_mhhh, addMHHH, clean_variables, initialise_df, save_variables
from machinelearning import init_bdt, add_bdt, init_bdt_boosted, add_bdt_boosted
from calibrations import btag_init, addBTagSF, addBTagEffSF
from hhh_variables import add_hhh_variables

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--base_folder ", type="string", dest="base", help="Folder in where to look for the categories", default='/eos/user/m/mstamenk/CxAOD31run/hhh-6b/v28-spanet-boosted-classification-variables/mva-inputs-2018')
parser.add_option("--category ", type="string", dest="category", help="Category to compute it. if no argument is given will do all", default='none')
parser.add_option("--skip_do_trees", action="store_true", dest="skip_do_trees", help="Write...", default=False)
parser.add_option("--skip_do_histograms", action="store_true", dest="skip_do_histograms", help="Write...", default=False)
parser.add_option("--skip_do_plots", action="store_true", dest="skip_do_plots", help="Write...", default=False)
parser.add_option("--do_SR", action="store_true", dest="do_SR", help="Write...", default=False)
parser.add_option("--do_CR", action="store_true", dest="do_CR", help="Write...", default=False)
parser.add_option("--process ", type="string", dest="process_to_compute", help="Process to compute it. if no argument is given will do all", default='none')
parser.add_option("--do_limit_input ", type="string", dest="do_limit_input", help="If given it will do the histograms only in that variable with all the uncertainties", default='none')
parser.add_option("--bdt_category ", type="string", dest="bdt_category", help="Folder in where to look for the categories", default='divide_bdt_cut_0.25_0.5')
parser.add_option("--bdt_cut ", type="float", dest="bdt_cut", help="Folder in where to look for the categories", default=0)
# parser.add_option("--bdt_cut_low ", type="float", dest="bdt_cut", help="Folder in where to look for the categories", default=0)
# parser.add_option("--bdt_cut_high ", type="float", dest="bdt_cut", help="Folder in where to look for the categories", default=0)

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
bdt_cat            = options.bdt_category
bdt_cut            = options.bdt_cut
input_tree = input_tree 
bdt_cut_low = bdt_cut -0.25

if do_SR and do_CR :
    print("You should chose to signal region OR control region")
    exit()

#define a function to find the highqest prob for each event
compareProb='''
int compareProb(double ProbHHH,double ProbQCD,double ProbTT,double ProbVJets,double ProbVV){
    if (ProbHHH>ProbQCD && ProbHHH>ProbTT && ProbHHH>ProbVJets && ProbHHH>ProbVV)
        return 0;
    else if (ProbQCD>ProbHHH && ProbQCD>ProbTT && ProbQCD>ProbVJets && ProbQCD>ProbVV)
        return 1;
    else if (ProbTT>ProbHHH && ProbTT>ProbQCD && ProbTT>ProbVJets && ProbTT>ProbVV)
        return 2;
    else
        return 3;
    }
'''
ROOT.gInterpreter.Declare(compareProb)
#bdt_cat = "divide_bdt_cut_0"

getmax = '''
int get_max_prob(float ProbHHH, float ProbQCD, float ProbTT, float ProbVJets, float ProbVV, float ProbHHH4b2tau, float ProbHH4b, float ProbHH2b2tau){
    std::vector<float> probs;
    probs.push_back(ProbHHH);
    probs.push_back(ProbQCD);
    probs.push_back(ProbTT);
    probs.push_back(ProbVJets);
    probs.push_back(ProbVV);
    probs.push_back(ProbHHH4b2tau);
    probs.push_back(ProbHH4b);
    probs.push_back(ProbHH2b2tau);
    //probs.push_back(ProbDY);

    auto it = std::max_element(probs.begin(), probs.end());
    int index = std::distance(probs.begin(), it);

    //std::cout << index << " " << probs[index] << std::endl;

    return index + 1;

}

'''

def init_get_max_prob():
    ROOT.gInterpreter.Declare(getmax)


getmaxcat = '''
int get_max_cat(float Prob3bh0h, float Prob2bh1h, float Prob1bh2h, float Prob0bh3h, float Prob2bh0h, float Prob1bh1h, float Prob0bh2h, float Prob1bh0h, float Prob0bh1h, float Prob0bh0h){
    std::vector<float> probs;
    probs.push_back(Prob0bh0h);
    probs.push_back(Prob3bh0h);
    probs.push_back(Prob2bh1h);
    probs.push_back(Prob1bh2h);
    probs.push_back(Prob0bh3h);
    probs.push_back(Prob2bh0h);
    probs.push_back(Prob1bh1h);
    probs.push_back(Prob0bh2h);
    probs.push_back(Prob1bh0h);
    probs.push_back(Prob0bh1h);

    auto it = std::max_element(probs.begin(), probs.end());
    int index = std::distance(probs.begin(), it);

    //std::cout << index << " " << probs[index] << std::endl;

    return index;

}

'''

def init_get_max_cat():
    ROOT.gInterpreter.Declare(getmaxcat)
    

selections = {
    #"final_selection_jetMultiplicity" : "(nbtags > 4 && nfatjets == 0) || (nbtags > 2 && nfatjets > 0)",

    ######multiclass categories
    "6l_multiclass_HHH"              : {
        "sel" : "(nloosebtags > 5 && nprobejets == 0  && nleps == 0 && ntaus == 0 && compareProb(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV) == 0)",
        "label" : "Resolved 6L HHH enriched",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    
    "6l_multiclass_QCD"              : {
        "sel" : "(nloosebtags > 5 && nprobejets == 0  && nleps == 0 && ntaus == 0 && compareProb(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV) == 1)",
        "label" : "Resolved 6L QCD enriched",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    
    "6l_multiclass_TT"              : {
        "sel" : "(nloosebtags > 5 && nprobejets == 0  && nleps == 0 && ntaus == 0 && compareProb(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV) == 2)",
        "label" : "Resolved 6L TT enriched",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },

    "6l_multiclass_rest"              : {
        "sel" : "(nloosebtags > 5 && nprobejets == 0  && nleps == 0 && ntaus == 0 && compareProb(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV) == 3)",
        "label" : "Resolved 6L rest",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    
    "6m_multiclass_HHH"              : {
        "sel" : "(nmediumbtags > 5 && nprobejets == 0  && nleps == 0 && ntaus == 0 && compareProb(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV) == 0)",
        "label" : "Resolved 6M HHH enriched",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    
    "6m_multiclass_QCD"              : {
        "sel" : "(nmediumbtags > 5 && nprobejets == 0  && nleps == 0 && ntaus == 0 && compareProb(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV) == 1)",
        "label" : "Resolved 6M QCD enriched",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    
    "6m_multiclass_TT"              : {
        "sel" : "(nmediumbtags > 5 && nprobejets == 0  && nleps == 0 && ntaus == 0 && compareProb(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV) == 2)",
        "label" : "Resolved 6M TT enriched",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },

    "6m_multiclass_rest"              : {
        "sel" : "(nmediumbtags > 5 && nprobejets == 0  && nleps == 0 && ntaus == 0 && compareProb(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV) == 3)",
        "label" : "Resolved 6M rest ",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    
    "gt5bloose_test"                : {
        "sel" : "(nloosebtags > 5 )",
        "label" : "6L",
        "dataset" : "resolved",
        },

    "gt5bloose_0PFfat"              : {
        "sel" : "(nloosebtags > 5 && nprobejets == 0    && nleps == 0 && ntaus == 0 && mva[0] > %s)"%(bdt_cut),
        "label" : "Resolved 6L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
    
    "QCD_test"              : {
        "sel" : "(nloosebtags == 5 && nprobejets == 0    && nleps == 0 && ntaus == 0 && mva[0] > %s)"%(bdt_cut),
        "label" : "5L_1F",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },

    "gt5bloose_0PFfat_no_bdt_cut"              : {
        "sel" : "(nloosebtags > 5 && nprobejets == 0    && nleps == 0 && ntaus == 0 )",
        "label" : "Resolved 6L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
    
    

    "6l_mt2l"              : {
        "sel" : "(nloosebtags >= 6 && nprobejets == 0 && nleps >= 2 && ntaus == 0)",
        "label" : "6l_mt2l",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
        
    "6l_mt1l"              : {
        "sel" : "(nloosebtags >= 6 && nprobejets == 0 && nleps >= 1 && ntaus == 0 )",
        "label" : "6l_mt1l",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
    
    "6l_mt1l_5btag"              : {
        "sel" : "(nloosebtags == 5 && nprobejets == 0 && nleps >= 1 && ntaus == 0 )",
        "label" : "6l_mt1l_5btag",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },

    "6l_1l"              : {
        "sel" : "(nloosebtags >= 6 && nprobejets == 0 && nleps == 1 && ntaus == 0 )",
        "label" : "6l_1l",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },

    "6l_1l_5btag"              : {
        "sel" : "(nloosebtags == 5 && nprobejets == 0 && nleps == 1 && ntaus == 0 )",
        "label" : "6l_1l_5btag",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },

    "6l_2l"              : {
        "sel" : "(nloosebtags >= 6 && nprobejets == 0 && nleps == 2 && ntaus == 0 )",
        "label" : "6l_2l",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
    
    "6l_2l_5btag"              : {
        "sel" : "(nloosebtags == 5 && nprobejets == 0 && nleps == 2 && ntaus == 0 )",
        "label" : "6l_2l_5btag",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
    

    "fourb_twotau"              : {
        "sel" : "(nloosebtags >= 4 && nprobejets == 0 && ntaus >= 2 )",
        "label" : "fourb_twotau",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },

    "no_cat"              : {
        "sel" : "(nprobejets == 0 && nleps == 0 && ntaus == 0   )",
        "label" : "Resolved 6L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },


     "gt5bloose_0PFfat_orthogonal"              : {
        "sel" : "(nloosebtags > 5  && nmediumbtags <6 && nleps == 0 && ntaus == 0 && nprobejets == 0  && mva[0] > %s )"%(bdt_cut),
        "label" : "Resolved 6L(orthogonal)",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",

        },
    
    

    "gt5bloose_gt0medium_0PFfat"    : {
        "sel" : "(nloosebtags > 5 && nmediumbtags >0&& nleps == 0 && ntaus ==0 && nprobejets == 0 && mva[0] > %s )"%(bdt_cut),
        "label" : "Resolved 1M 5L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    "gt5bloose_gt1medium_0PFfat"    : {
        "sel" : "(nloosebtags > 5 && nmediumbtags >1&& nleps == 0 && ntaus ==0 && nprobejets == 0 && mva[0] > %s)"%(bdt_cut),
        "label" : "Resolved 2M 4L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    "gt5bloose_gt2medium_0PFfat"    : {
        "sel" : "(nloosebtags > 5 && nmediumbtags >2 && nleps == 0 && ntaus ==0 && nprobejets == 0  && mva[0] > %s )"%(bdt_cut),
        "label" : "Resolved 3M 3L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    "gt5bloose_gt3medium_0PFfat"    : {
        "sel" : "(nloosebtags > 5 && nmediumbtags >3 && nleps == 0 && ntaus ==0 && nprobejets == 0 && mva[0] > %s )"%(bdt_cut),
        "label" : "Resolved 4M 2L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    "gt5bloose_gt4medium_0PFfat"    : {
        "sel" : "(nloosebtags > 5 && nmediumbtags >4 && nleps == 0 && ntaus ==0 && nprobejets == 0 && mva[0] > %s )"%(bdt_cut),
        "label" : "Resolved 5M 1L",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    "gt5bmedium_0PFfat"             : {
        "sel" : "(nmediumbtags > 5 && nleps == 0 && ntaus == 0  && nprobejets == 0 && mva[0] > %s )"%(bdt_cut),
        "label" : "Resolved 6M",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
    
    "gt5bmedium_0PFfat_no_cat"             : {
        "sel" : "(nmediumbtags > 5 && nleps == 0 && ntaus == 0  && nprobejets == 0)",
        "label" : "Resolved 6M",
        "doSR" : "&& (h_fit_mass > 80 && h_fit_mass < 150)",
        "doCR" : "&& !(h_fit_mass > 80 && h_fit_mass < 150)",
        "dataset" : "resolved",
        },
   


   
    "1PFfat"                        : {
        "sel" : "(nprobejets == 1)",
        "label" : "Boosted (1 PN fat jet)",
        "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt1PFfat"                      : {
        "sel" : "(nprobejets > 1)",
        "label" : "Boosted (> 1 PN fat jet)",
        "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    #"gt0PFfat"                      : {
    #    "sel" : "(nprobejets > 0)",
    #    "label" : "Boosted (> 0 PN fat jet)",
    #    "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
    #    "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
    #    },
    "1PNfatLoose"                        : {
        "sel" : "(nprobejets == 1 && fatJet1PNetXbb > 0.95)",
        "label" : "Boosted (1 PN fat jet) with PNet Xbb > 0.95",
        "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt1PNfatLoose"                      : {
        "sel" : "(nprobejets > 1 && fatJet1PNetXbb > 0.95)",
        "label" : "Boosted (> 1 PN fat jet) with PNet Xbb > 0.95",
        "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "1PNfatMedium"                        : {
        "sel" : "(nprobejets == 1 && fatJet1PNetXbb > 0.975)",
        "label" : "Boosted (1 PN fat jet) with PNet Xbb > 0.975",
        "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt1PNfatMedium"                      : {
        "sel" : "(nprobejets > 1 && fatJet1PNetXbb > 0.975)",
        "label" : "Boosted (> 1 PN fat jet) with PNet Xbb > 0.975",
        "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "1PNfatTight"                        : {
        "sel" : "(nprobejets == 1 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted (1 PN fat jet) with PNet Xbb > 0.985",
        "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt1PNfatTight"                      : {
        "sel" : "(nprobejets > 1 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted (> 1 PN fat jet) with PNet Xbb > 0.985",
        "doSR" : "&& (fatJet1Mass > 80 && fatJet1Mass < 150)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    # nprobejets >= 1
    "gt0PFfat_cat1"                      : {
        "sel" : "(nprobejets > 0 && mvaBoosted[0] > 0.4 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted category 1",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt0PFfat_cat2"                      : {
        "sel" : "(nprobejets > 0 && mvaBoosted[0] > 0.15 && mvaBoosted[0] < 0.4 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted category 2",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt0PFfat_cat3"                      : {
        "sel" : "(nprobejets > 0 && mvaBoosted[0] > -0.04 && mvaBoosted[0] < 0.4 && fatJet1PNetXbb > 0.95)",
        "label" : "Boosted category 3",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    # nprobejets >= 2
    "gt1PFfat_cat1"                      : {
        "sel" : "(nprobejets > 1 && mvaBoosted[0] > 0.15 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted category 1",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt1PFfat_cat2"                      : {
        "sel" : "(nprobejets > 1 && mvaBoosted[0] > 0.0 && mvaBoosted[0] < 0.15 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted category 2",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt1PFfat_cat3"                      : {
        "sel" : "(nprobejets > 1 && mvaBoosted[0] > 0.0 && mvaBoosted[0] < 0.15 && fatJet1PNetXbb > 0.95)",
        "label" : "Boosted category 3",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    # nprobejets == 1
    "1PFfat_cat1"                      : {
        "sel" : "(nprobejets == 1 && mvaBoosted[0] > 0.15 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted category 1",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "1PFfat_cat2"                      : {
        "sel" : "(nprobejets == 1 && mvaBoosted[0] > 0.0 && mvaBoosted[0] < 0.15 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted category 2",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "1PFfat_cat3"                      : {
        "sel" : "(nprobejets == 1 && mvaBoosted[0] > 0.0 && mvaBoosted[0] < 0.15 && fatJet1PNetXbb > 0.95)",
        "label" : "Boosted category 3",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },

    # inclusive boosted category
    "gt0PFfat"                      : {
        "sel" : "(nprobejets > 0 && mvaBoosted[0] > 0.0 && fatJet1PNetXbb > 0.95)",
        "label" : "Boosted category 3",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
        },
    "gt0PFfat_PNetTight"                      : {
        "sel" : "(nprobejets > 0 && mvaBoosted[0] > 0.0 && fatJet1PNetXbb > 0.985)",
        "label" : "Boosted category 3",
        "doSR" : "&& (fatJet1Mass > 0)",
        "doCR" : "&& !(fatJet1Mass > 80 && fatJet1Mass < 150)",
        "dataset" : "boosted",
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

# procstodo = ["DYJetsToLL","GluGluToHHHTo4B2Tau_SM","SingleMuon","WJetsToLNu_0J","WJetsToLNu_1J","WJetsToLNu_2J", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu", "QCD", "data_obs" , "GluGluToHHHTo6B_SM"]
procstodo = ["DYJetsToLL","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau","GluGluToHHTo4B_cHHH0","TTToSemiLeptonic","WJetsToLNu_0J","WJetsToLNu_1J","WJetsToLNu_2J", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu", "QCD", "data_obs" , "GluGluToHHHTo6B_SM"]

# procstodo = ["ZZZ", "WZZ", "WWZ", "WWW" ,"TTToSemiLeptonic"]


if not process_to_compute == 'none' :
    procstodo     = [process_to_compute]
    skip_do_plots = True

#for era in [2016, 2017, 2018] :
for era in ['2018'] :
    if str(era) in input_tree : year = str(era)

wp_loose = wps_years['loose'][year]
wp_medium = wps_years['medium'][year]
wp_tight = wps_years['tight'][year]

# define function to run on mHHH
init_mhhh()
ROOT.gInterpreter.Declare(triggersCorrections[year][0])

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
  output_tree = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v28/2018/DeepFlav"

  output_folder1 = "{}/{}/".format(output_tree,bdt_cat)
  if not path.exists(output_folder1) :
      procs=subprocess.Popen(['mkdir %s' % output_folder1],shell=True,stdout=subprocess.PIPE)
      out = procs.stdout.read()
      print("made directory %s" % output_folder1)
  output_folder = "{}/{}/{}_{}".format(output_tree,bdt_cat,selection,additional_label)
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
        if year == '2018' :
            datahist = 'JetHT'
        else:
            datahist = 'BTagCSV'

    outtree = "{}/{}/{}_{}/{}.root".format(output_tree,bdt_cat,selection,additional_label,proctodo)

    dataset = selections[selection]["dataset"] # inclusive_resolved or inclusive_boosted
    list_proc=glob.glob("{}/inclusive_{}/{}.root".format(input_tree,dataset,datahist))
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

        # initialise df - so we don't need make_selection_rdataframes.py anymore

        chunk_df = initialise_df(chunk_df,year,proc) # mHHH done inside now
        
        if firstProc:
            #init_bdt(chunk_df,year)
            init_bdt(chunk_df,year)
            init_bdt_boosted(chunk_df,year)
            firstProc = False
        entries_no_filter = int(chunk_df.Count().GetValue())

        # Add mva and mvaBoosted variables (needs to happen before cutting on variables mva and mvaBoosted)
        chunk_df,masses,pts,etas,phis = add_hhh_variables(chunk_df)
        chunk_df = add_bdt(chunk_df,year)
        chunk_df = add_bdt_boosted(chunk_df,year)

        chunk_df = chunk_df.Filter(final_selection)
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
        for type_obj in ['bcand', 'fatJet', 'jet'] :
            for jet_number in range(1,11) :
                for angle in ['Eta', 'Phi'] :
                    obj = '{}{}{}'.format(type_obj,jet_number,angle)
                    if obj in variables :
                        #print("Take absolute of %s" % obj)
                        chunk_df = chunk_df.Define('Abs%s'%obj, "abs(%s)" % obj)
        chunk_df = chunk_df.Define('Abshhh_eta', "abs(hhh_eta)")
                #chunk_df = chunk_df.Redefine('hh_phi', "abs(hh_phi)")

        print("2 - construct the eventWeight")
        to_multiply = []
        do_SF = True

        if (selection == "gt5bloose_test" or 
            selection == "gt5bloose_0PFfat" or
            selection ==  "gt5bloose_0PFfat_orthogonal" or 
            selection == "gt5bloose_0PFfat_no_bdt_cut" or 
            selection == "6l_multiclass_HHH" or 
            selection == "6l_multiclass_TT" or 
            selection == "6l_multiclass_QCD" or 
            selection == "6l_multiclass_rest"):
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
        elif (selection == "gt5bmedium_0PFfat" or 
              selection == "6m_multiclass_HHH" or 
              selection == "6m_multiclass_TT" or 
              selection == "6m_multiclass_QCD" or 
              selection == "6m_multiclass_rest"):
            nmedium_cut = 6
        else :
            print("no SF ready to selection %s , we are ignoring it by the moment" % selection)
            do_SF = False

        if do_SF :
            for jet_number in range(1,nmedium_cut+1) :
                to_multiply = to_multiply + ['jet{}MediumBTagEffSF'.format(jet_number)]
            for jet_number in range(nmedium_cut+1,7) :
                to_multiply = to_multiply + ['jet{}LooseBTagEffSF'.format(jet_number)]
        string_multiply = 'eventWeight'
        print("to_multiply")
        print(to_multiply)
        for ss in to_multiply :
            string_multiply = string_multiply + ' * {}'.format(ss)

        print( "Redefine eventWeight = {}".format(string_multiply))
        chunk_df = chunk_df.Define('totalWeight', string_multiply)

        proc_yield = chunk_df.Sum('totalWeight')
        print("Yield:", proc_yield.GetValue())

        print(variables)

        chunk_df.Snapshot(inputTree, outtree, variables + ['totalWeight'])

        gc.collect() # clean menory
        sys.stdout.flush() # extra clean

        seconds = time.time()
        print("Seconds to load : ", seconds-seconds0)
        print("Minutes to load : ", (seconds-seconds0)/60.0)

  ## do Histograms -- reorganize to do directly limits
  output_histos = "{}/{}/{}_{}/histograms".format(output_tree,bdt_cat,selection,additional_label)
  if not path.exists(output_histos) :
    procs=subprocess.Popen(['mkdir %s' % output_histos],shell=True,stdout=subprocess.PIPE)
    out = procs.stdout.read()

  if not skip_do_histograms : # args.doHistograms:
    ## already doing plots, will do histogram file only to the chosen variable
    seconds0 = time.time()
    #histograms = []
    proctodo = "GluGluToHHHTo6B_SM" ## for taking the list of variables and doing the first histogram in the file
    outtree = "{}/{}/{}_{}/{}.root".format(output_tree,bdt_cat,selection,additional_label,proctodo)
    chunk_df = ROOT.RDataFrame(inputTree, outtree)
    # chunk_df = chunk_df.Filter('met > 90')
    chunk_df = chunk_df.Filter('h1_t3_mass > 50')
    print("add new cut")
    variables = chunk_df.GetColumnNames()


    print("Will produce histograms for following variables:")
    print(do_limit_input)
    for var in variables: # booking all variables to be produced

        #template = ROOT.TH1F("", "", histograms_dict[do_limit_input]["nbins"], histograms_dict[do_limit_input]["xmin"], histograms_dict[do_limit_input]["xmax"])
        # Define histograms to be produced === make that can be a list
        if do_limit_input == var :
            nbins = histograms_dict[do_limit_input]["nbins"]
            xmin = histograms_dict[do_limit_input]["xmin"]
            xmax = histograms_dict[do_limit_input]["xmax"]

            try :
                histograms_dict[do_limit_input]
            except :
                print("The binning options for the variable %s should be added in utils" % do_limit_input)
                exit()

            nameout = output_histos + '/' + 'histograms_%s.root'%(do_limit_input)
            f_out = ROOT.TFile(nameout, 'recreate')
            print("Writing in %s" % nameout)

            f_out.cd()
            for proctodo in procstodo :
                outtree = "{}/{}/{}_{}/{}.root".format(output_tree,bdt_cat,selection,additional_label,proctodo) ## make better, to not have to call it twice

                try :
                    chunk_df = ROOT.RDataFrame(inputTree, outtree)
                    # chunk_df = chunk_df.Filter('met > 90')
                    chunk_df = chunk_df.Filter('h1_t3_mass > 50')
                except :
                    print("process %s has 0 entries, skipping doing the histogram" % proctodo)
                    continue

                # datahist = proctodo
                # if proctodo == "data_obs" :
                #     if year == '2018' :
                #         datahist = 'JetHT'
                #     else:
                #         datahist = 'BTagCSV'

                char_var = var.c_str()
                try:
                    #h_tmp = chunk_df.Fill(template, [char_var, 'totalWeight'])
                    f_out.cd()
                    h_tmp = chunk_df.Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'totalWeight')
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
      # Draw the data/MC to this selection
      
     #path_to_plots = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/plots/%s' %(era)
      path_to_plots = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/plots_addmva/%s/%s/DeepFlav' %(bdt_cat,era)
      
      output_folder_draw = "{}/{}_{}".format(path_to_plots,selection,additional_label)
      if not path.exists(output_folder_draw) :
        procs=subprocess.Popen(['mkdir %s' % output_folder],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
      print("made directory %s" % output_folder_draw)

      
      input_folder_plots = "{}/{}/{}_{}".format(output_tree,bdt_cat,selection,additional_label)


      #command = "python3 draw_data_mc_categories.py --input_folder %s --plot_label '%s (%s)' --output_folder %s" % (output_histos.replace('histograms',''), selections[selection]["label"], additional_label, output_folder_draw)
    #   command = "python3 draw_data_log.py --input_folder %s --log --plot_label '%s (%s)'  --save_pdf --output_folder %s" % (input_folder_plots , selections[selection]["label"], additional_label, output_folder_draw)
      command = "python3 draw_data_log.py --input_folder %s --log --plot_label '%s (%s)'  --save_pdf --output_folder %s" % (input_folder_plots , selections[selection]["label"], additional_label, output_folder_draw)

      #if "0PFfat" in selection :
      #command = command + " --log"
      print(command)

      proc=subprocess.Popen([command],shell=True,stdout=subprocess.PIPE)
      out = proc.stdout.read()
      
print("SUCCESSFUL!!!!!!!!!!!!!!!!!!!!!!!")
