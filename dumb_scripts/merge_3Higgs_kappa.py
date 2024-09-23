import subprocess
import os,sys
import ROOT

# process_strings = ["DYJetsToLL","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau","GluGluToHHTo4B_cHHH1","TTToSemiLeptonic","WJetsToLNu_0J","WJetsToLNu_1J","WJetsToLNu_2J", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu", "QCD", "data_obs" , "GluGluToHHHTo6B_SM"]

year = 'run2'
path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33'
# path2 = '/eos/user/m/mstamenk/CxAOD31run/hhh-6b/v26'

btag_cut_strings = ["ProbHHH6b_3Higgs_inclusive_CR"]
process_list = ["GluGluToHHTo4B_cHHH1","GluGluToHHTo4B_cHHH0","GluGluToHHTo4B_cHHH5","data_obs","GluGluToHHHTo6B_SM","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau_SM","QCD_datadriven"]

output_folder = "{}/run2/ProbHHH6b_3Higgs_inclusive_CR/histograms".format(path)

output_folder3 = "{}/run2/ProbHHH6b_3Higgs_inclusive_CR".format(path)
if not os.path.exists(output_folder3) :
    procs=subprocess.Popen(['mkdir %s' % output_folder3],shell=True,stdout=subprocess.PIPE)
    out = procs.stdout.read()
    print("made directory %s" % output_folder3)

if not os.path.exists(output_folder) :
    procs=subprocess.Popen(['mkdir %s' % output_folder],shell=True,stdout=subprocess.PIPE)
    out = procs.stdout.read()
    print("made directory %s" % output_folder)



# os.system("hadd -f  {}/run2/ProbHHH6b_3Higgs_inclusive_CR/histograms/histograms_kappa_scale.root \
#                     {}/run2/ProbHHH6b_3bh0h_inclusive_CR/histograms/histograms_kappa_scale.root \
#                     {}/run2/ProbHHH6b_2bh1h_inclusive_CR/histograms/histograms_kappa_scale.root \
#                     {}/run2/ProbHHH6b_1bh2h_inclusive_CR/histograms/histograms_kappa_scale.root \
#                     {}/run2/ProbHHH6b_0bh3h_inclusive_CR/histograms/histograms_kappa_scale.root \
#                     ".format(path,path,path,path,path))

os.system("hadd -f  {}/run2/ProbHHH6b_3Higgs_inclusive_CR/histograms/histograms_kappa.root \
                    {}/run2/ProbHHH6b_3bh0h_inclusive_CR/histograms/histograms_kappa.root \
                    {}/run2/ProbHHH6b_2bh1h_inclusive_CR/histograms/histograms_kappa.root \
                    {}/run2/ProbHHH6b_1bh2h_inclusive_CR/histograms/histograms_kappa.root \
                    {}/run2/ProbHHH6b_0bh3h_inclusive_CR/histograms/histograms_kappa.root \
                    ".format(path,path,path,path,path))