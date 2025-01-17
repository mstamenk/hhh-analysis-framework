import subprocess
import os,sys
import ROOT

# process_strings = ["DYJetsToLL","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau","GluGluToHHTo4B_cHHH1","TTToSemiLeptonic","WJetsToLNu_0J","WJetsToLNu_1J","WJetsToLNu_2J", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu", "QCD", "data_obs" , "GluGluToHHHTo6B_SM"]

year = '2016'
path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/'
# path2 = '/eos/user/m/mstamenk/CxAOD31run/hhh-6b/v26'

var = 'ProbMultiH'
cat = 'ProbHHH6b'
option = '_CR'
# btag_cut_strings = ['%s_2bh0h_inclusive%s','%s_1bh1h_inclusive%s','%s_0bh2h_inclusive%s','%s_3bh0h_inclusive%s','%s_2bh1h_inclusive%s','%s_1bh2h_inclusive%s','%s_0bh3h_inclusive%s','%s_3Higgs_inclusive%s','%s_2Higgs_inclusive%s','%s_1Higgs_inclusive%s','%s_0bh0h_inclusive%s']
btag_cut_strings = ['%s_2bh0h_inclusive%s','%s_1bh1h_inclusive%s','%s_0bh2h_inclusive%s']
# btag_cut_strings = ['%s_2Higgs_inclusive%s','%s_1Higgs_inclusive%s','%s_0bh0h_inclusive%s']
# process_list = ["GluGluToHHTo4B_cHHH1","GluGluToHHTo4B_cHHH0","GluGluToHHTo4B_cHHH5","data_obs","GluGluToHHHTo6B_SM","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau_SM","QCD_datadriven"]
process_list = ["HHHTo6B_c3_0_d4_99","HHHTo6B_c3_0_d4_minus1","HHHTo6B_c3_19_d4_19","HHHTo6B_c3_1_d4_0","HHHTo6B_c3_1_d4_2","HHHTo6B_c3_2_d4_minus1","HHHTo6B_c3_4_d4_9","HHHTo6B_c3_minus1_d4_0","HHHTo6B_c3_minus1_d4_minus1","HHHTo6B_c3_minus1p5_d4_minus0p5"]
# btag_cut_strings = ['%s_3Higgs_inclusive_']

for btag_cut in btag_cut_strings:
    btag_cut = btag_cut%(cat,option)
    output_folder = "{}/2016_all/{}/histograms".format(path,btag_cut)
    
    output_folder3 = "{}/2016_all/{}/histograms".format(path,btag_cut)
    output_folder2 = "{}/2016_all/{}".format(path,btag_cut)

    if not os.path.exists(output_folder2) :
        procs=subprocess.Popen(['mkdir %s' % output_folder2],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % output_folder2)

    if not os.path.exists(output_folder3) :
        procs=subprocess.Popen(['mkdir %s' % output_folder3],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % output_folder3)



    os.system("hadd -f  {}/2016_all/{}/histograms/histograms_{}.root \
                        {}/2016/{}/histograms/histograms_{}.root \
                        {}/2016APV/{}/histograms/histograms_{}.root \
                        ".format(path,btag_cut,var,path,btag_cut,var,path,btag_cut,var))
        