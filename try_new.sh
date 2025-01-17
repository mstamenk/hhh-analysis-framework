# #for var in gt5bloose_0PFfat gt5bloose_gt0medium_0PFfat gt5bloose_gt1medium_0PFfat gt5bloose_gt2medium_0PFfat gt5bloose_gt3medium_0PFfat gt5bloose_gt4medium_0PFfat  gt5bmedium_0PFfat
# for var in  gt5bloose_0PFfat_orthogonal
# do
#     # python skimm_tree2.py --skip_do_trees  --skip_do_plots  --category $var --do_limit_input h1_t3_mass --bdt_category divide_bdt_cut_0.45_0.7  --bdt_cut 0.7&
#     #python skimm_tree2.py --skip_do_trees  --skip_do_plots  --category $var --do_limit_input h1_t3_mass --bdt_category divide_bdt_cut_0.35_0.6  --bdt_cut 0.6&
#     #python3 skimm_tree.py --skip_do_trees --skip_do_histograms   --category $var --bdt_category divide_bdt_cut_0.6  --bdt_cut 0.6 &
#     #python skimm_tree2.py --skip_do_trees --skip_do_histograms --category $var --bdt_category divide_bdt_cut_0.35_0.6  --bdt_cut 0.6 &
#     #python3 skimm_tree2.py --skip_do_trees --skip_do_histograms   --category $var --bdt_category divide_no_cut   

#     python skimm_tree_for2016.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category divide_bdt_cut_0.1    &
#     python skimm_tree_for2016APV.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category divide_bdt_cut_0.1    &
#     python skimm_tree_for2018.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category divide_bdt_cut_0.1    &
#     python skimm_tree.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category divide_bdt_cut_0.1    &


#    #python skimm_tree.py --skip_do_trees --skip_do_histograms   --category $var --bdt_category divide_bdt_cut_0.7  --bdt_cut 0.7 &

    

# done
    #python skimm_tree_nobdt.py --skip_do_trees  --skip_do_plots   --category  medium_0to5_  --do_limit_input h1_t3_mass   &
#gt5bloose_gt0medium_0PFfat gt5bloose_gt1medium_0PFfat gt5bloose_gt2medium_0PFfat gt5bloose_gt3medium_0PFfat gt5bloose_gt4medium_0PFfat  gt5bmedium_0PFfat
#gt5bloose_gt0medium_0PFfat gt5bloose_gt1medium_0PFfat gt5bloose_gt2medium_0PFfat gt5bloose_gt3medium_0PFfat gt5bloose_gt4medium_0PFfat  gt5bmedium_0PFfat

# for bdt in  divide_bdt_cut_0.7 
# do
#     for var in  0M 1M 2M 3M 4M 5M 6M
#     do
#         python skimm_tree_sub.py --skip_do_trees  --skip_do_plots  --category $var --do_limit_input h1_t3_mass --bdt_category $bdt --category_old gt5bloose_0PFfat_ &
#     #python skimm_tree2.py --skip_do_trees  --skip_do_plots  --category $var --do_limit_input h1_t3_mass --bdt_category divide_bdt_cut_0.35_0.6  --bdt_cut 0.6&
#     #python3 skimm_tree.py --skip_do_trees --skip_do_histograms   --category $var --bdt_category divide_bdt_cut_0.6  --bdt_cut 0.6 &
#     #python skimm_tree2.py --skip_do_trees --skip_do_histograms --category $var --bdt_category divide_bdt_cut_0.35_0.6  --bdt_cut 0.6 &
#     done
# done
#


# gt5bloose_0PFfat QCD_bEnriched QCD6B_bEnriched gt5bloose_0PFfat gt5bloose_0PFfat gt5bloose_0PFfat gt5bloose_gt0medium_0PFfat gt5bloose_gt1medium_0PFfat gt5bloose_gt2medium_0PFfat gt5bloose_gt3medium_0PFfat 
#gt5bloose_0PFfat gt5bloose_gt0medium_0PFfat gt5bloose_gt1medium_0PFfat gt5bloose_gt2medium_0PFfat gt5bloose_gt3medium_0PFfat gt5bloose_gt4medium_0PFfat  gt5bmedium_0PFfat
# 0M 1M 2M 3M 4M 5M 6M  
#divide_bdt_cut_0 divide_bdt_cut_0.1 divide_bdt_cut_0.2 divide_bdt_cut_0.3 divide_bdt_cut_0.4 divide_bdt_cut_0.5 divide_bdt_cut_0.6 

#python skimm_tree2.py --skip_do_trees  --skip_do_plots  --category gt5bloose_0PFfat --do_limit_input h1_t3_mass --bdt_category divide_bdt_cut_-0.25_0  --bdt_cut 0&
#python3 skimm_tree.py --skip_do_trees --skip_do_plots   --category gt5bloose_0PFfat --do_limit_input h1_t3_mass --bdt_category divide_bdt_cut_0.1  --bdt_cut 0.1 &
# python skimm_tree_sub.py --skip_do_trees  --skip_do_plots  --category_old gt5bloose_0PFfat_  --category 0M --do_limit_input h1_t3_mass --bdt_category divide_bdt_cut_0  --bdt_cut 0&
# python3 skimm_tree.py --skip_do_trees --skip_do_histograms   --category gt5bmedium_0PFfat --bdt_category divide_no_cut   &
#for bdt_cat in divide_bdt_cut_0 divide_bdt_cut_0.1 divide_bdt_cut_0.2 divide_bdt_cut_0.3 divide_bdt_cut_0.4 divide_bdt_cut_0.5 divide_bdt_cut_0.6 divide_bdt_cut_0.7 
for bdt_cat in divide_no_cut
#for bdt_cat in divide_bdt_cut_-0.25_0 divide_bdt_cut_-0.15_0.1 divide_bdt_cut_-0.05_0.2 divide_bdt_cut_0.05_0.3 divide_bdt_cut_0.15_0.4  divide_bdt_cut_0.25_0.5 divide_bdt_cut_0.35_0.6 divide_bdt_cut_0.45_0.7
do
    #for var in   gt5bloose_0PFfat gt5bloose_gt0medium_0PFfat gt5bloose_gt1medium_0PFfat gt5bloose_gt2medium_0PFfat gt5bloose_gt3medium_0PFfat gt5bloose_gt4medium_0PFfat  gt5bmedium_0PFfat
    # for var  in   6l_mt2l  6l_1l 6l_2l 6l_mst1l
    # for var  in   6l_mt2l_5btag  6l_1l_5btag 6l_2l_5btag 6l_mt1l_5btag
    # for var  in   QCD_est
    # for var  in   gt5bloose_0PFfat  gt5bloose_0PFfat_orthogonal  gt5bmedium_0PFfat
    # for var in ProbHHH6b_inclusive ProbQCD_inclusive ProbTT_inclusive ProbVJets_inclusive ProbVV_inclusive Probrest_inclusive \
    #             ProbQCD_3bh0h_inclusive ProbQCD_2bh1h_inclusive ProbQCD_1bh2h_inclusive ProbQCD_0bh3h_inclusive ProbQCD_3Higgs_inclusive ProbQCD_rest_inclusive \
    #             ProbTT_3bh0h_inclusive ProbTT_2bh1h_inclusive ProbTT_1bh2h_inclusive ProbTT_0bh3h_inclusive ProbTT_3Higgs_inclusive ProbTT_rest_inclusive \
    #             ProbVJets_3bh0h_inclusive ProbVJets_2bh1h_inclusive ProbVJets_1bh2h_inclusive ProbVJets_0bh3h_inclusive ProbVJets_3Higgs_inclusive ProbVJets_rest_inclusive \
    #             ProbVV_3bh0h_inclusive ProbVV_2bh1h_inclusive ProbVV_1bh2h_inclusive ProbVV_0bh3h_inclusive ProbVV_3Higgs_inclusive ProbVV_rest_inclusive \
    #             ProbHHH6b_3bh0h_inclusive ProbHHH6b_2bh1h_inclusive ProbHHH6b_1bh2h_inclusive ProbHHH6b_0bh3h_inclusive ProbHHH6b_3Higgs_inclusive 
    # for var in ProbQCD_0bh3h_inclusive ProbTT_3bh0h_inclusive ProbVJets_3bh0h_inclusive ProbVV_3bh0h_inclusive
    # for var  in  ProbHHH6b_3bh0h_inclusive ProbHHH6b_2bh1h_inclusive ProbHHH6b_1bh2h_inclusive ProbHHH6b_0bh3h_inclusive ProbHHH6b_3Higgs_inclusive  
    # for var  in  ProbQCD_3bh0h_inclusive   ProbQCD_semi_boosted_inclusive ProbQCD_3Higgs_inclusive
    # for var  in  Probrest_3bh0h_inclusive   Probrest_semi_boosted_inclusive Probrest_3Higgs_inclusive
    # for var  in  ProbTT_3bh0h_inclusive ProbTT_2bh1h_inclusive ProbTT_1bh2h_inclusive ProbTT_0bh3h_inclusive ProbTT_3Higgs_inclusive  
    # for var  in  ProbTT_3Higgs_inclusive  
    # for var  in  ProbQCD_3Higgs_inclusive  
    # for var  in 
    
    

    # for var  in      ProbHHH6b_0bh3h_inclusive  ProbHHH6b_1bh2h_inclusive 
    # for var  in  ProbHH4b_3Higgs_inclusive   ProbHH4b_2Higgs_inclusive    ProbHH4b_1Higgs_inclusive ProbHH4b_0bh0h_inclusive
    # for var  in   ProbHHH6b_3Higgs_inclusive     ProbHHH6b_2Higgs_inclusive ProbHHH6b_1Higgs_inclusive  ProbHHH6b_0bh0h_inclusive 
    # for var  in  ProbHHH6b_2bh0h_inclusive ProbHHH6b_1bh1h_inclusive ProbHHH6b_0bh2h_inclusive ProbHHH6b_3Higgs_inclusive     ProbHHH6b_2Higgs_inclusive ProbHHH6b_1Higgs_inclusive  ProbHHH6b_0bh0h_inclusive ProbHHH6b_3bh0h_inclusive ProbHHH6b_2bh1h_inclusive ProbHHH6b_1bh2h_inclusive ProbHHH6b_0bh3h_inclusive
    # for var  in   ProbHHH6b_3Higgs_inclusive    ProbHHH6b_2Higgs_inclusive    ProbHH4b_2Higgs_inclusive  
    # for var  in    ProbHH4b_3Higgs_inclusive   ProbHHH6b_1Higgs_inclusive  ProbHHH6b_0bh0h_inclusive  ProbHH4b_1Higgs_inclusive ProbHH4b_0bh0h_inclusive
    for var  in   ProbHHH6b_0bh3h_inclusive ProbHHH6b_1bh2h_inclusive ProbHHH6b_2bh1h_inclusive ProbHHH6b_3bh0h_inclusive
    # for var  in    ProbHHH6b_1bh2h_inclusive ProbHHH6bs_2bh1h_inclusive ProbHHH6b_3bh0h_inclusive
    # for var  in   ProbHHH6b_0bh3h_inclusive ProbHHH6b_1bh2h_inclusive
    # for var  in   ProbHHH6b_0bh3h_inclusive  ProbHHH6b_3bh0h_inclusive
    # for var  in   ProbHHH6b_1bh2h_inclusive 
    # for var  in   6m_multiclass_HHH 6m_multiclass_QCD 6m_multiclass_TT 6m_multiclass_rest 
    # for var  in    6l_1l 6l_2l 6l_lt2bm 6l_mt1l gt5bloose_0PFfat_no_bdt_cut
    # for var  in    6l_mt2l 6l_mt1l 6l_1l 6l_2l gt5bloose_0PFfat_no_bdt_cut no_cat
    # for var  in    6l_mt2l 6l_mt1l 6l_1l 6l_2l gt5bmedium_0PFfat gt5bloose_0PFfat 


    do
        # python skimm_tree2.py --skip_do_trees  --skip_do_plots  --category $var --do_limit_input h1_t3_mass --bdt_category divide_bdt_cut_0.45_0.7  --bdt_cut 0.7&
        #python skimm_tree2.py --skip_do_trees  --skip_do_plots  --category $var --do_limit_input h1_t3_mass --bdt_category divide_bdt_cut_0.35_0.6  --bdt_cut 0.6&
        #python3 skimm_tree.py --skip_do_trees --skip_do_histograms   --category $var --bdt_category divide_bdt_cut_0.6  --bdt_cut 0.6 &
        #python skimm_tree2.py --skip_do_trees --skip_do_histograms --category $var --bdt_category divide_bdt_cut_0.35_0.6  --bdt_cut 0.6 &
        #python3 skimm_tree2.py --skip_do_trees --skip_do_histograms   --category $var --bdt_category divide_no_cut   

        # python skimm_tree_for2016.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category $bdt_cat    &
        # python skimm_tree_for2016APV.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category $bdt_cat    &
        # python skimm_tree.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category $bdt_cat    &
        # python skimm_tree_PNet.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category $bdt_cat    &

        # python skimm_tree.py --skip_do_trees --skip_do_plots  --skip_do_histograms --category $var  --do_limit_input ProbMultiH  --do_CR  &
    
        # python skimm_tree.py --skip_do_trees --skip_do_plots --do_CR --skip_do_correct --category $var  --do_limit_input ProbMultiH   &
        # python skimm_tree_2017.py --skip_do_trees --skip_do_plots --do_CR --skip_do_correct --category $var  --do_limit_input ProbMultiH    &
        # python skimm_tree_2016.py --skip_do_trees --skip_do_plots --do_CR --skip_do_correct --category $var  --do_limit_input ProbMultiH   &
        # python skimm_tree_2016APV.py --skip_do_trees --skip_do_plots --do_CR --skip_do_correct --category $var  --do_limit_input ProbMultiH    &
        # python skimm_tree_2017.py --skip_do_trees --skip_do_plots --do_CR --skip_do_correct  --category $var  --do_limit_input ProbHHH    &
        # python skimm_tree_2016.py --skip_do_trees --skip_do_plots  --do_CR --skip_do_correct  --category $var  --do_limit_input ProbHHH    &
        # python skimm_tree_2016APV.py --skip_do_trees --skip_do_plots --do_CR  --skip_do_correct  --category $var  --do_limit_input ProbHHH    &

        python skimm_tree.py --skip_do_trees --skip_do_histograms --do_CR --skip_do_correct --category $var   &
        # python skimm_tree_2016.py --skip_do_trees --skip_do_histograms --do_CR --skip_do_correct --category $var   &
        # python skimm_tree_2016APV.py --skip_do_trees --skip_do_histograms --do_CR --skip_do_correct --category $var   &
        # python skimm_tree_2017.py --skip_do_trees --skip_do_histograms --do_CR --skip_do_correct --category $var   &



        # python skimm_tree.py --skip_do_trees   --skip_do_histograms --do_CR --skip_do_correct  --category $var  --do_limit_input ProbMultiH    &
        # python skimm_tree_2017.py --skip_do_trees --skip_do_plots  --skip_do_histograms  --category $var  --do_limit_input ProbHHH    &
        # python skimm_tree_2016.py --skip_do_trees --skip_do_plots  --skip_do_histograms  --category $var  --do_limit_input ProbMultiH   &
        # python skimm_tree_2016APV.py --skip_do_trees --skip_do_plots  --skip_do_histograms  --category $var  --do_limit_input ProbHHH    &

        

        # python skimm_tree_PNet.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input ProbHHH  --bdt_category $bdt_cat    &
        # python skimm_tree.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input ProbHHH  --bdt_category $bdt_cat    &
        # python skimm_tree_5L_2.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category $bdt_cat    &
        # python skimm_tree_5L_PNet_2.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category $bdt_cat    &
        # python skimm_tree_for_run2.py --skip_do_trees --skip_do_plots   --category $var  --do_limit_input h1_t3_mass  --bdt_category $bdt_cat    &



        # python skimm_tree.py --skip_do_trees  --skip_do_correct --skip_do_histograms   --category $var    &
        # # python skimm_tree_5L_PNet.py --skip_do_trees --skip_do_histograms   --category $var --bdt_category $bdt_cat   &
        # python skimm_tree_PNet.py --skip_do_trees --skip_do_histograms   --category $var --bdt_category $bdt_cat   &

        

    done
done