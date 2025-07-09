#from utils import wps_years
import ROOT
import shutil
import sys, os, re, shlex
import shutil,subprocess
import time
import os.path
from os import path
import glob
import gc

inputTree = 'Events'
path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33'
path_new  = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new'
pro_list=["data_obs",'GluGluToHHTo4B_cHHH0','GluGluToHHTo4B_cHHH1','GluGluToHHTo4B_cHHH5','GluGluToHHHTo4B2Tau_SM','GluGluToHHHTo6B_SM','QCD_datadriven']
# pro_list=['QCD_datadriven']
year_list  =['2018','2017','2016','2016APV']
categories_list = ["ProbHHH6b_3bh0h_inclusive_CR","ProbHHH6b_2bh1h_inclusive_CR","ProbHHH6b_1bh2h_inclusive_CR","ProbHHH6b_0bh3h_inclusive_CR","ProbHHH6b_3Higgs_inclusive_CR","ProbHHH6b_2Higgs_inclusive_CR","ProbHHH6b_1Higgs_inclusive_CR","ProbHHH6b_0bh0h_inclusive_CR"]
# categories_list = ["ProbHHH6b_2Higgs_inclusive_CR","ProbHHH6b_0bh0h_inclusive_CR"]
for cat in categories_list:
    for pro in pro_list:
        for year in year_list:
            outtree = "%s/%s/%s/%s.root"%(path_new,year,cat,pro)

            output_folder_1 = path_new
            if not os.path.exists(output_folder_1) :
                procs=subprocess.Popen(['mkdir %s' % output_folder_1],shell=True,stdout=subprocess.PIPE)
                out = procs.stdout.read()
                print("made directory %s" % output_folder_1)

            output_folder_2 = "%s/%s"%(path_new,year)
            if not os.path.exists(output_folder_2) :
                procs=subprocess.Popen(['mkdir %s' % output_folder_2],shell=True,stdout=subprocess.PIPE)
                out = procs.stdout.read()
                print("made directory %s" % output_folder_2)

            output_folder_3 = "%s/%s/%s"%(path_new,year,cat)
            if not os.path.exists(output_folder_3) :
                procs=subprocess.Popen(['mkdir %s' % output_folder_3],shell=True,stdout=subprocess.PIPE)
                out = procs.stdout.read()
                print("made directory %s" % output_folder_3)

        # process_path = "%s/%s/%s/%s.root"%(path,year,cat,pro)
        process_path_2018    = "%s/2018/%s/%s.root"%(path,cat,pro)
        process_path_2017    = "%s/2017/%s/%s.root"%(path,cat,pro)
        process_path_2016    = "%s/2016/%s/%s.root"%(path,cat,pro)
        process_path_2016APV = "%s/2016APV/%s/%s.root"%(path,cat,pro)

        chunk_df_2018 = ROOT.RDataFrame(inputTree, process_path_2018)
        br_name_2018=[str(el) for el in chunk_df_2018.GetColumnNames()]
        # br_name_2018=chunk_df_2018.GetColumnNames()

        chunk_df_2017 = ROOT.RDataFrame(inputTree, process_path_2017)
        br_name_2017=[str(el) for el in chunk_df_2017.GetColumnNames()]
        # br_name_2017=chunk_df_2017.GetColumnNames()


        chunk_df_2016 = ROOT.RDataFrame(inputTree, process_path_2016)
        br_name_2016=[str(el) for el in chunk_df_2016.GetColumnNames()]
        # br_name_2016=chunk_df_2016.GetColumnNames()


        chunk_df_2016APV = ROOT.RDataFrame(inputTree, process_path_2016APV)
        br_name_2016APV=[str(el) for el in chunk_df_2016APV.GetColumnNames()]
        # br_name_2016APV=chunk_df_2016APV.GetColumnNames()

        common_branches = []
        for item in br_name_2018:
            if item in br_name_2016 and item in br_name_2016APV and item in br_name_2017:
                common_branches.append(item)




        # common_branches = set(br_name_2018)&set(br_name_2017)&set(br_name_2016)&set(br_name_2016APV)
        # vector_common_branches= ROOT.std.vector[str](common_branches)
        # common_branches =br_name_2018 &br_name_2017 &br_name_2016&br_name_2016APV
        # to_save = [str(el) for el in vector_common_branches if 'LHEReweightingWeight' not in str(el) and  'PSWeight' not in str(el) and 'LHEScaleWeightNormNew'not in str(el)]
        # to_save = to_save + ['LHEReweightingWeight'] + ['PSWeight'] +['LHEScaleWeightNormNew']
        # to_save_new = [str(el) for el in to_save]
        to_save = common_branches


        

        outtree_2018 = "%s/2018/%s/%s.root"%(path_new,cat,pro)
        outtree_2017 = "%s/2017/%s/%s.root"%(path_new,cat,pro)
        outtree_2016 = "%s/2016/%s/%s.root"%(path_new,cat,pro)
        outtree_2016APV = "%s/2016APV/%s/%s.root"%(path_new,cat,pro)

        chunk_df_2018.Snapshot(inputTree, outtree_2018,to_save)
        chunk_df_2017.Snapshot(inputTree, outtree_2017,to_save)
        chunk_df_2016.Snapshot(inputTree, outtree_2016,to_save)
        chunk_df_2016APV.Snapshot(inputTree, outtree_2016APV,to_save)
        print("already done %s"%(outtree))



           

