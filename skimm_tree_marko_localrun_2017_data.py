import ROOT
import shutil
import sys, os, re, shlex
import shutil,subprocess
import time
import os.path
from os import path
import glob
import gc
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.ROOT.EnableImplicitMT()

from utils_v34 import histograms_dict, wps_years, wps, tags, luminosities, hlt_paths, triggersCorrections, hist_properties, init_mhhh, addMHHH, clean_variables, initialise_df, save_variables, init_get_max_cat, applySelection
from calibrations import btag_init, addBTagSF, addBTagEffSF
from hhh_variables import add_hhh_variables


from optparse import OptionParser
parser = OptionParser()
parser.add_option("--base_folder ", type="string", dest="base", help="Folder in where to look for the categories", default='/eos/user/x/xiangran/samples/test4_2016_v34/')
parser.add_option("--category ", type="string", dest="category", help="Category to compute it. if no argument is given will do all", default='none')
parser.add_option("--skip_do_trees", action="store_true", dest="skip_do_trees", help="Write...", default=False)
parser.add_option("--do_SR", action="store_true", dest="do_SR", help="Write...", default=False)
parser.add_option("--do_CR", action="store_true", dest="do_CR", help="Write...", default=False)
parser.add_option("--process ", type="string", dest="process_to_compute", help="Process to compute it. if no argument is given will do all", default='none')
parser.add_option("--run_all_categories ",  dest="run_all_categories", help="Run on all ProbHHH6b and ProbHH4b categories in a for loop", action='store_true', default = False)

(options, args) = parser.parse_args()

process_to_compute = options.process_to_compute
do_SR              = options.do_SR
do_CR              = options.do_CR
skip_do_trees      = options.skip_do_trees
input_tree         = options.base
cat                = options.category
run_all_categories = options.run_all_categories

if do_SR and do_CR :
    print("You should chose to signal region OR control region")
    exit()

selections = {
        "ProbHHH6b_3bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 1 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        "doCR" : "&& (ProbMultiH_v34 > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH6b_2bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 2 )",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        "doCR" : "&& (ProbMultiH_v34 > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        # "ProbHHH6b_1bh2h_inclusive"              : {
        # "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 3 )",
        # "label" : "ProbHHH ",
        # "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        # "doCR" : "&& (ProbMultiH_v34 > 0. && ht > 450)",
        # "dataset" : "-weights",
        # },

        # "ProbHHH6b_0bh3h_inclusive"              : {
        # "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 4 )",
        # "label" : "ProbHHH ",
        # "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        # "doCR" : "&& (ProbMultiH_v34 > 0. && ht > 450)",
        # "dataset" : "-weights",
        # },

        "ProbHHH6b_2bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 5)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        "doCR" : "&& (ProbMultiH_v34 > 0. && ht > 450)",
        "dataset" : "-weights",
        },

        "ProbHHH6b_1bh1h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 6)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        "doCR" : "&& (ProbMultiH_v34 > 0.0 && ht > 450)",
        "dataset" : "-weights",
        },
        # "ProbHHH6b_0bh2h_inclusive"              : {
        # "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 7)",
        # "label" : "ProbHHH ",
        # "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        # "doCR" : "&& (ProbMultiH_v34 > 0.0 && ht > 450)",
        # "dataset" : "-weights",
        # },

        "ProbHHH6b_0bh0h_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && IndexMaxCat == 0)",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        "doCR" : "&& (ProbMultiH_v34 > 0. && ht > 450)",
        "dataset" : "-weights",
        },



        "ProbHHH6b_3Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && (IndexMaxCat == 1 || IndexMaxCat == 2 || IndexMaxCat == 3 || IndexMaxCat == 4))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        "doCR" : "&& (ProbMultiH_v34 > 0. && ht > 450 )",
        "dataset" : "-weights",
        },
        # "ProbHHH6b_2Higgs_inclusive"              : {
        # "sel" : "(IndexMaxProb == 1 && (IndexMaxCat == 5 || IndexMaxCat == 6 || IndexMaxCat == 7 ))",
        # "label" : "ProbHHH ",
        # "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        # "doCR" : "&& (ProbMultiH_v34 > 0 && ht > 450)",
        # "dataset" : "-weights",
        # },
        "ProbHHH6b_1Higgs_inclusive"              : {
        "sel" : "(IndexMaxProb == 1 && (IndexMaxCat == 8 || IndexMaxCat == 9 ))",
        "label" : "ProbHHH ",
        "doSR" : "&& ProbMultiH_v34 > 0.0 ",
        "doCR" : "&& (ProbMultiH_v34 > 0. && ht > 450)",
        "dataset" : "-weights",
        },
}

additional_selection = ""
additional_label     = ""
if do_SR : 
    additional_label     = "SR"
if do_CR :
    additional_label     = "CR"

inputTree = 'Events'

# procstodo = ["QCD_datadriven","GluGluToHHTo4B_cHHH1","data_obs","GluGluToHHHTo6B_SM"]

procstodo = ["DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8",\
            "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",\
            "GluGluToHHHTo6B_SM",\
            "GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_SM_13TeV-madgraph-pythia8",\
            "GluGluToHHTo4B_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8",\
            "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",\
            "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",\
            "QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",\
            "QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",\
            "QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",\
            "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",\
            "QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",\
            "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",\
            "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",\
            "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",\
            "WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",\
            "WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",\
            "WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",\
            "WJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",\
            "WJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",\
            "WJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",\
            "WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8","QCD_datadriven"]

if not process_to_compute == 'none' :
    procstodo     = [process_to_compute]

for era in ['2016', '2016APV', '2017', '2018','2016APV201620172018'] :
    if str(era) in input_tree : year = str(era)

if '2016APV201620172018' in year:
    year = '2018'

wp_loose = wps_years['loose'][year]
wp_medium = wps_years['medium'][year]
wp_tight = wps_years['tight'][year]

init_mhhh()
getmax = '''
int get_max_prob(float ProbHHH, float ProbQCD, float ProbTT, float ProbHH4b){
    std::vector<float> probs;
    probs.push_back(ProbHHH); // 1
    probs.push_back(ProbQCD); // 2
    probs.push_back(ProbTT); // 3
    probs.push_back(ProbHH4b); // 4
    auto it = std::max_element(probs.begin(), probs.end());
    int index = std::distance(probs.begin(), it);
    return index + 1;
}
'''
def init_get_max_prob():
    ROOT.gInterpreter.Declare(getmax)
init_get_max_prob()
init_get_max_cat()


# define b-tagging
if '2016APV' in year:
    btag_init('2016preVFP')
elif '2016' in year:
    btag_init('2016postVFP')
elif '2022' in year:
    btag_init('2018')
else:
    btag_init(year)


if run_all_categories:
    category_list = selections.keys()
else:
    category_list = []
    category_list.append(cat)
for selection in category_list:
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
  output_tree = "/eos/cms/store/group/phys_higgs/cmshhh/v34-test/final/%s"%(year)
  output_folder = "{}/{}_{}".format(output_tree,selection,additional_label)
  if not path.exists(output_folder) :
      procs=subprocess.Popen(['mkdir %s' % output_folder],shell=True,stdout=subprocess.PIPE)
      out = procs.stdout.read()
      print("made directory %s" % output_folder)

  if not skip_do_trees :

   for proctodo in procstodo :
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
    list_proc=glob.glob("{}/inclusive{}/{}.root".format(input_tree,dataset,datahist))

    for proc in list_proc :
        tlocal = time.localtime()
        current_time = time.strftime("%H:%M:%S", tlocal)
        print(current_time)
        seconds0 = time.time()
        print("Reading from:",proc)
        print("Cutting tree and saving it to ", outtree)
        print("With selection: ", final_selection)

        chunk_df = ROOT.RDataFrame(inputTree, proc)
        chunk_df = chunk_df.Define('ProbMultiH_v34','ProbHHH_v34 + ProbHH4b_v34')
        
        chunk_df = chunk_df.Define('IndexMaxProb', 'get_max_prob(ProbHHH_v34, ProbQCD_v34, ProbTT_v34, ProbHH4b_v34)')
        chunk_df = chunk_df.Define('IndexMaxCat', 'get_max_cat(Prob3bh0h_v34, Prob2bh1h_v34, Prob1bh2h_v34, Prob0bh3h_v34, Prob2bh0h_v34, Prob1bh1h_v34, Prob0bh2h_v34, Prob1bh0h_v34, Prob0bh1h_v34, Prob0bh0h_v34)')
        chunk_df = chunk_df.Define('Prob3Higgs_v34','Prob3bh0h_v34+Prob2bh1h_v34+Prob1bh2h_v34+Prob0bh3h_v34')
        chunk_df = chunk_df.Define('Prob2Higgs_v34','Prob2bh0h_v34+Prob1bh1h_v34+Prob0bh2h_v34')
        chunk_df = chunk_df.Define('Prob1Higgs_v34','Prob1bh0h_v34+Prob0bh1h_v34')
        chunk_df = chunk_df.Define('Prob0Higgs_v34','Prob0bh0h_v34')
        print(dataset)
        
        try:
            entries_no_filter = int(chunk_df.Count().GetValue())
        except:
            print('Error with %s'%proc)
            continue

        chunk_df = chunk_df.Filter(final_selection)
        entries = int(chunk_df.Count().GetValue())


        print("cut made, tree size: ", entries_no_filter, entries)
        variables = list(chunk_df.GetColumnNames())

        for type_obj in ['fatJet', 'jet'] :
            for jet_number in range(1,11) :
                for angle in ['Eta', 'Phi'] :
                    obj = '{}{}{}'.format(type_obj,jet_number,angle)
                    if obj in variables :
                        chunk_df = chunk_df.Define('Abs%s'%obj, "abs(%s)" % obj)
        
        proc_yield = chunk_df.Sum('eventWeight')
        print("Yield:", proc_yield.GetValue())

        to_save = [str(el) for el in chunk_df.GetColumnNames() if 'mva' not in str(el) and 'HLT' not in str(el)]
        chunk_df.Snapshot(inputTree, outtree,to_save)

        gc.collect() # clean menory
        sys.stdout.flush() # extra clean

        seconds = time.time()
        print("Seconds to load : ", seconds-seconds0)
        print("Minutes to load : ", (seconds-seconds0)/60.0)
