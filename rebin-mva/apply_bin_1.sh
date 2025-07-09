for prob  in  ProbHHH6b
# for prob  in  ProbHH4b 
do
    for year in  2016APV201620172018
    # for year in 2018
     

    do


        # python apply_binning_cat_run2.py --year $year --path_year run2 --prob $prob --var ProbMultiH  --version v33_new  &
        # python apply_binning_cat_cut_2018.py --year $year --path_year 2018 --prob $prob --var ProbMultiH  --version cat_new &
        # python apply_binning_cat_2016.py --year $year --path_year v34_2016_test2 --prob $prob --var ProbMultiH  --version tmp_samples --doSyst&
        python3 apply_binning_final_marko.py --year $year --path_year 2018 --prob $prob --var ProbMultiH  --version v34 --doSyst&
        python3 apply_binning_final_marko.py --year $year --path_year 2017 --prob $prob --var ProbMultiH  --version v34 --doSyst&
        python3 apply_binning_final_marko.py --year $year --path_year 2016 --prob $prob --var ProbMultiH  --version v34 --doSyst&
        python3 apply_binning_final_marko.py --year $year --path_year 2016APV --prob $prob --var ProbMultiH  --version v34 --doSyst&
        # python apply_binning_cat_2018.py --year $year --path_year 2016 --prob $prob --var ProbMultiH  --version v33_new --doSyst&
        # python apply_binning_cat_2018.py --year $year --path_year 2016APV --prob $prob --var ProbMultiH  --version v33_new --doSyst&
        # python apply_binning_cat_2017.py --year $year --path_year 2017 --prob $prob --var ProbMultiH  --doSyst --version v33_new  &
        # python apply_binning_cat_2016.py --year $year --path_year 2016 --prob $prob --var ProbMultiH  --doSyst --version v33_new  &
        # python apply_binning_cat_2016APV.py --year $year --path_year 2016APV --prob $prob --var ProbMultiH --doSyst  --version v33_new  &
        # python apply_binning_cat_1.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_cat_2.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_cat_3.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_for_kappa.py --year $year --prob  $prob &

        

    done
done

