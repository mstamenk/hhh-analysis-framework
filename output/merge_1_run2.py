import subprocess
import os,sys
import ROOT
import argparse


# process_strings = ["DYJetsToLL","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau","GluGluToHHTo4B_cHHH1","TTToSemiLeptonic","WJetsToLNu_0J","WJetsToLNu_1J","WJetsToLNu_2J", "ZZTo4Q", "WWTo4Q", "ZJetsToQQ", "WJetsToQQ", "TTToHadronic","TTTo2L2Nu", "QCD", "data_obs" , "GluGluToHHHTo6B_SM"]

parser = argparse.ArgumentParser()
parser.add_argument('--path_hist', type=str, required=True)
args = parser.parse_args()

path = args.path_hist
year = '2018'
# path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34_AN_HHH6b_new'
# path2 = '/eos/user/m/mstamenk/CxAOD31run/hhh-6b/v26'

var = 'ProbMultiH'
cat = 'ProbHHH6b'
# cat = 'ProbHH4b'
option = '_CR'
btag_cut_strings = ['%s_2bh0h_inclusive%s','%s_1bh1h_inclusive%s','%s_0bh2h_inclusive%s','%s_3bh0h_inclusive%s','%s_2bh1h_inclusive%s','%s_1bh2h_inclusive%s','%s_0bh3h_inclusive%s','%s_0bh0h_inclusive%s','%s_1Higgs_inclusive%s']
# btag_cut_strings = ['%s_1bh0h_inclusive%s','%s_0bh1h_inclusive%s']

for btag_cut in btag_cut_strings:
    btag_cut = btag_cut%(cat,option)
    output_folder = "{}/run2/{}/histograms".format(path,btag_cut)

    output_folder4 = "{}/run2".format(path)
    if not os.path.exists(output_folder4) :
        procs=subprocess.Popen(['mkdir %s' % output_folder4],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % output_folder4)
    
    output_folder3 = "{}/run2/{}".format(path,btag_cut)
    if not os.path.exists(output_folder3) :
        procs=subprocess.Popen(['mkdir %s' % output_folder3],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % output_folder3)
    
    if not os.path.exists(output_folder) :
        procs=subprocess.Popen(['mkdir %s' % output_folder],shell=True,stdout=subprocess.PIPE)
        out = procs.stdout.read()
        print("made directory %s" % output_folder)
    

    # ====== NEW: 自动检查文件是否存在
    # input_files = [
    #     "{}/2016/{}/histograms/histograms_{}.root".format(path, btag_cut, var),
    #     "{}/2016APV/{}/histograms/histograms_{}.root".format(path, btag_cut, var),
    #     "{}/2017/{}/histograms/histograms_{}.root".format(path, btag_cut, var),
    #     "{}/2018/{}/histograms/histograms_{}.root".format(path, btag_cut, var)
    # ]
    input_files = [
        "{}/2016_all/{}/histograms/histograms_{}.root".format(path, btag_cut, var),
        "{}/2017/{}/histograms/histograms_{}.root".format(path, btag_cut, var),
        "{}/2018/{}/histograms/histograms_{}.root".format(path, btag_cut, var)
    ]

    existing_input_files = []
    for f in input_files:
        if os.path.exists(f):
            existing_input_files.append(f)
        else:
            print(f"[SKIP] Missing input file: {f}")

    if len(existing_input_files) > 0:
        hadd_cmd = "hadd -f  {}/run2/{}/histograms/histograms_{}.root {}".format(
            path, btag_cut, var, " ".join(existing_input_files)
        )
        print(f"[INFO] Running: {hadd_cmd}")
        os.system(hadd_cmd)
    else:
        print(f"[WARN] No input files found for {btag_cut}, skipping hadd.")

    # os.system("hadd -f  {}/run2/{}/histograms/histograms_{}.root \
    #                     {}/2016/{}/histograms/histograms_{}.root \
    #                     {}/2016APV/{}/histograms/histograms_{}.root \
    #                     {}/2017/{}/histograms/histograms_{}.root \
    #                     {}/2018/{}/histograms/histograms_{}.root \
    #                     ".format(path,btag_cut,var,path,btag_cut,var,path,btag_cut,var,path,btag_cut,var,path,btag_cut,var))
    
    # os.system("hadd -f  {}/run2/{}/histograms/histograms_{}_fixAsy.root \
    #                     {}/2016_all/{}/histograms/histograms_{}_fixAsy.root \
    #                     {}/2017/{}/histograms/histograms_{}_fixAsy.root \
    #                     {}/2018/{}/histograms/histograms_{}_fixAsy.root \
    #                     ".format(path,btag_cut,var,path,btag_cut,var,path,btag_cut,var,path,btag_cut,var))
    