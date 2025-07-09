import subprocess
import os,sys
import ROOT

# process_strings = ["DYJetsToLL","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau","GluGluToHHTo4B_cHHH1","TTToSemiLeptonic","WJetsToLNu_0J","WJetsToLNu_1J","WJetsToLNu_2J", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu", "QCD", "data_obs" , "GluGluToHHHTo6B_SM"]

year = 'run2'
path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34_AN_HHH6b'
# path2 = '/eos/user/m/mstamenk/CxAOD31run/hhh-6b/v26'

btag_cut_strings = ["ProbHHH6b_3Higgs_inclusive_CR","ProbHHH6b_2Higgs_inclusive_CR","ProbHHH6b_1Higgs_inclusive_CR","ProbHHH6b_0bh0h_inclusive_CR","ProbHHH6b_3bh0h_inclusive_CR","ProbHHH6b_2bh1h_inclusive_CR","ProbHHH6b_1bh2h_inclusive_CR","ProbHHH6b_0bh3h_inclusive_CR"]
process_list = ["ProbMultiH"]

for btag_cut in btag_cut_strings:
    output_folder = "{}/run2/{}/histograms".format(path,btag_cut)
    
    output_folder3 = "{}/run2/{}".format(path,btag_cut)
    if not os.path.exists(output_folder3) :
        procs=subprocess.Popen(['mkdir %s' % output_folder3],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % output_folder3)
    
    if not os.path.exists(output_folder) :
        procs=subprocess.Popen(['mkdir %s' % output_folder],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % output_folder)

    for process in process_list :

        os.system("hadd -f  {}/run2/{}/histograms/histograms_{}.root \
                            {}/2016/{}/histograms/histograms_{}.root \
                            {}/2016APV/{}/histograms/histograms_{}.root \
                            {}/2017/{}/histograms/histograms_{}.root \
                            {}/2018/{}/histograms/histograms_{}.root \
                            ".format(path,btag_cut,process,path,btag_cut,process,path,btag_cut,process,path,btag_cut,process,path,btag_cut,process))


