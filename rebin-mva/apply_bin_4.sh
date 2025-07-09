for prob  in  ProbHHH6b
# for prob  in  ProbHH4b 
do
    # for year in  2018 2017 2016 2016APV
    for year in 2016APV201620172018
     

    do


        # python3 apply_binning_final_marko.py --year $year  --path_year 2018 --prob $prob --var ProbMultiH --doSyst --version v34  &
        # python3 apply_binning_final_marko.py --year $year  --path_year 2017 --prob $prob --var ProbMultiH --doSyst --version v34  &
        # python3 apply_binning_final_marko.py --year $year  --path_year 2016 --prob $prob --var ProbMultiH --doSyst --version v34  &
        # python3 apply_binning_final_marko.py --year $year  --path_year 2016APV --prob $prob --var ProbMultiH --doSyst --version v34  &
        python3 apply_binning_xinyue_mass_kappa_6.py --doSyst --year $year --prob $prob --var ProbMultiH --version v34  &
        python3 apply_binning_xinyue_mass_kappa_7.py --doSyst --year $year --prob $prob --var ProbMultiH --version v34  &
        python3 apply_binning_xinyue_mass_kappa_8.py --doSyst --year $year --prob $prob --var ProbMultiH --version v34  &
        python3 apply_binning_xinyue_mass_kappa_9.py --doSyst --year $year --prob $prob --var ProbMultiH --version v34  &

        # python apply_binning_cat_2017.py --year $year --path_year 2017 --prob $prob --var ProbMultiH --doSyst --version v33  &
        # python apply_binning_cat_2016.py --year $year --path_year 2016 --prob $prob --var ProbMultiH  --doSyst --version v33_new  &
        # python apply_binning_cat_2016APV.py --year $year --path_year 2016APV --prob $prob --var ProbMultiH --doSyst  --version v33_new  &
        # python apply_binning_cat_1.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_cat_2.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_cat_3.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_for_kappa.py --year $year --prob  $prob &

        

    done
done

