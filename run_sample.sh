for path in /eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/signal/parts
#for bdt_cat in divide_bdt_cut_-0.25_0 divide_bdt_cut_-0.15_0.1 divide_bdt_cut_-0.05_0.2 divide_bdt_cut_0.05_0.3 divide_bdt_cut_0.15_0.4  divide_bdt_cut_0.25_0.5 divide_bdt_cut_0.35_0.6 divide_bdt_cut_0.45_0.7
do
    

    for sample  in  GluGluToHHTo4B_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8_tree.root \
                    GluGluToHHTo4B_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8_tree.root \
                    GluGluToHHTo4B_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8_tree.root \
                    GluGluToHHTo4B_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8_tree.root \
                    HHHTo4B2Tau_c3_0_d4_0_TuneCP5_13TeV-amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_0_d4_0_TuneCP5_13TeV-amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_0_d4_99_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_0_d4_minus1_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_19_d4_19_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_1_d4_0_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_1_d4_2_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_2_d4_minus1_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_4_d4_9_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_minus1_d4_0_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_minus1_d4_minus1_TuneCP5_13TeV_amcatnlo-pythia8_tree.root \
                    HHHTo6B_c3_minus1p5_d4_minus0p5_TuneCP5_13TeV_amcatnlo-pythia8_tree.root


    do

        python prepare_inclusive_samples_weights.py -v v34 --year 2017 --f_in $path/$sample &
        
    done
done

