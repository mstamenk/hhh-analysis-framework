for path in /eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mc/parts
#for bdt_cat in divide_bdt_cut_-0.25_0 divide_bdt_cut_-0.15_0.1 divide_bdt_cut_-0.05_0.2 divide_bdt_cut_0.05_0.3 divide_bdt_cut_0.15_0.4  divide_bdt_cut_0.25_0.5 divide_bdt_cut_0.35_0.6 divide_bdt_cut_0.45_0.7
do
    

    for sample  in  TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_tree.root  
                    # WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8_tree.root \
                    # WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8_tree.root \
                    # WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8_tree.root 
                    


    do

        python prepare_inclusive_samples_weights_mc.py -v v34 --year 2017 --f_in $path/$sample &
        
    done
done

