path="/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework"
out_dir="/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34-fix-ak4-ak8"

# source output/v33_new/hadd_v33_new.sh $out_dir
# python Correction_Asymeric_2018.py --path_hist_folder $out_dir
# source output/v33_new/hadd_v33_new_3Higgs.sh $out_dir
# source output/v33_new/hadd_v33_new_2Higgs.sh $out_dir
# python output/merge_1_run2.py --path_hist $out_dir
python output/v33_new/merge_separate.py --path_hist $out_dir
python skimm_tree.py --skip_do_trees --skip_do_plots --skip_do_histograms \
       --category ProbHHH6b_1bh2h_inclusive --do_limit_input ProbMultiH --do_CR --path_to_histograms $out_dir

#for kappa
# source output/v33_new/hadd_v33_new_3Higgs_kappa.sh $out_dir



