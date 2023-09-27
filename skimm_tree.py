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

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--base_folder ", type="string", dest="base", help="Folder in where to look for the categories", default='/eos/user/m/mstamenk/CxAOD31run/hhh-6b/v26/2018/')
parser.add_option("--category ", type="string", dest="category", help="Category to compute it. if no argument is given will do all", default='none')
parser.add_option("--skip_do_trees", action="store_true", dest="skip_do_trees", help="Write...", default=False)
parser.add_option("--skip_do_histograms", action="store_true", dest="skip_do_histograms", help="Write...", default=False)
parser.add_option("--skip_do_plots", action="store_true", dest="skip_do_plots", help="Write...", default=False)
parser.add_option("--do_SR", action="store_true", dest="do_SR", help="Write...", default=False)
parser.add_option("--do_CR", action="store_true", dest="do_CR", help="Write...", default=False)
parser.add_option("--process ", type="string", dest="process_to_compute", help="Process to compute it. if no argument is given will do all", default='none')
parser.add_option("--do_limit_input ", type="string", dest="do_limit_input", help="If given it will do the histograms only in that variable with all the uncertainties", default='none')
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

    
   
   
    



    #########################boosted categories####################
    
   
    
    
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

procstodo = ["ZZZ", "WZZ", "WWZ", "WWW", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTo2L2Nu","TTToSemiLeptonic", "QCD", "data_obs" , "GluGluToHHHTo6B_SM"]
if not process_to_compute == 'none' :
    procstodo     = [process_to_compute]
    skip_do_plots = True

#for era in [2016, 2017, 2018] :
for era in [2018] :
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
  output_folder = "{}/{}_{}".format(input_tree,selection,additional_label)
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

    outtree = "{}/{}_{}/{}.root".format(input_tree,selection,additional_label,proctodo)

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
        string_multiply = 'eventWeight'
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
  output_histos = "{}/{}_{}/histograms".format(input_tree,selection,additional_label)
  if not path.exists(output_histos) :
    procs=subprocess.Popen(['mkdir %s' % output_histos],shell=True,stdout=subprocess.PIPE)
    out = procs.stdout.read()

  if not skip_do_histograms : # args.doHistograms:
    ## already doing plots, will do histogram file only to the chosen variable
    seconds0 = time.time()
    #histograms = []
    proctodo = "GluGluToHHHTo6B_SM" ## for taking the list of variables and doing the first histogram in the file
    outtree = "{}/{}_{}/{}.root".format(input_tree,selection,additional_label,proctodo)
    chunk_df = ROOT.RDataFrame(inputTree, outtree)
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
                outtree = "{}/{}_{}/{}.root".format(input_tree,selection,additional_label,proctodo) ## make better, to not have to call it twice

                try :
                    chunk_df = ROOT.RDataFrame(inputTree, outtree)
                except :
                    print("process %s has 0 entries, skipping doing the histogram" % proctodo)
                    continue

                datahist = proctodo
                if proctodo == "data_obs" :
                    if year == '2018' :
                        datahist = 'JetHT'
                    else:
                        datahist = 'BTagCSV'

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
      command = "python3 draw_data_mc_categories.py --input_folder %s --plot_label '%s (%s)'" % (output_histos.replace('histograms',''), selections[selection]["label"], additional_label)
      #if "0PFfat" in selection :
      #command = command + " --log"
      print(command)

      proc=subprocess.Popen([command],shell=True,stdout=subprocess.PIPE)
      out = proc.stdout.read()
