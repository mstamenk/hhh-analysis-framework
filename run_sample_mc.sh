for path in /eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mc/parts
#for bdt_cat in divide_bdt_cut_-0.25_0 divide_bdt_cut_-0.15_0.1 divide_bdt_cut_-0.05_0.2 divide_bdt_cut_0.05_0.3 divide_bdt_cut_0.15_0.4  divide_bdt_cut_0.25_0.5 divide_bdt_cut_0.35_0.6 divide_bdt_cut_0.45_0.7
do
    
# /eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mc/parts/ttbar_merge_1
# TTToHadronic_TuneCP5_13TeV-powheg-pythia8 \_tree \ \_3 \
    for sample  in  WHHTo4B_CV_0_5_C2V_1_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8_tree \
                    # WHHTo4B_CV_0_5_C2V_1_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # WHHTo4B_CV_1_0_C2V_0_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # WHHTo4B_CV_1_0_C2V_1_0_C3_0_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # WHHTo4B_CV_1_0_C2V_1_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # WHHTo4B_CV_1_0_C2V_1_0_C3_20_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # WHHTo4B_CV_1_0_C2V_1_0_C3_2_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # WHHTo4B_CV_1_0_C2V_2_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # WHHTo4B_CV_1_5_C2V_1_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \
                    # ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0_TuneCP5_13TeV-madgraph-pythia8 \


    do

        # python prepare_inclusive_xiangran.py -v v34 --year 2017 --f_in $path/ttbar_merge_3/$sample 
        python prepare_inclusive_xiangran.py -v v34 --year 2017 --f_in $sample 
        
    done
done


