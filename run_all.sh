path="/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework"
out_dir="/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34_fix_ak4_ak8_JME"


###to merge 1bh0h + 0bh1h to 1Higgs
source output/v33_new/hadd_1Higgs.sh $out_dir

##to merge 2016 2016APV to 2016_all, the name is for v33_new version, but can used in v34 now
source output/v33_new/hadd_v33_new.sh $out_dir

##to correct some asymetric uncertainties, named 2018, but it used to correct 2017 2018 2016 separately
python3 Correction_Asymeric_2018.py --path_hist_folder $out_dir

#### used to merge 3Higgs categories
# # source output/v33_new/hadd_v33_new_3Higgs.sh $out_dir

### used to merge 2Higgs categories 
# # source output/v33_new/hadd_v33_new_2Higgs.sh $out_dir



###merge 2016 2017 2018 to merged run2
python3 output/merge_1_run2.py --path_hist $out_dir

###### merge QCD data 2016 2017 2018 to merged run2, but 6b and 4b are separate and add new name here
####our baseline

python3 output/v33_new/merge_separate.py --path_hist $out_dir
# # python3 skimm_tree.py --skip_do_trees --skip_do_plots --skip_do_histograms \
# #        --category ProbHHH6b_1bh2h_inclusive --do_limit_input ProbMultiH --do_CR --path_to_histograms $out_dir  --do_kappa_bkg


#### used to produce datadriven background for run2 and run2_separate
python3 skimm_tree.py --skip_do_trees --skip_do_plots --skip_do_histograms \
       --category ProbHHH6b_1bh2h_inclusive --do_limit_input ProbMultiH --do_CR --path_to_histograms $out_dir --do_run2_bkg
# # python3 skimm_tree_4b_unc.py --skip_do_trees --skip_do_plots --skip_do_histograms \
# #        --category ProbHHH6b_1bh2h_inclusive --do_limit_input ProbMultiH --do_CR --path_to_histograms $out_dir --do_run2_bkg
# #for kappa
# # source output/v33_new/hadd_v33_new_3Higgs_kappa.sh $out_dir



