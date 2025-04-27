for path in /eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2018/mc/v34_mc_ak8_option4_2018/mc/parts
#for bdt_cat in divide_bdt_cut_-0.25_0 divide_bdt_cut_-0.15_0.1 divide_bdt_cut_-0.05_0.2 divide_bdt_cut_0.05_0.3 divide_bdt_cut_0.15_0.4  divide_bdt_cut_0.25_0.5 divide_bdt_cut_0.35_0.6 divide_bdt_cut_0.45_0.7
do
    
# /eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mc/parts/ttbar_merge_1
# TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tree \ \_3 \
    for sample  in  TTHHTo4b_TuneCP5_13TeV-madgraph-pythia8_tree \
                    # QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8_tree \
                    # QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8_tree \
                    
    do

        # python prepare_inclusive_xiangran.py -v v34 --year 2017 --f_in $path/ttbar_merge_3/$sample 
        python prepare_inclusive_xiangran.py -v v34 --year 2018 --f_in $sample 
        
    done
done

# QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8_tree \
                    # QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8_tree \
                    # QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8_tree \


