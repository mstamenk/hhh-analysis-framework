for prob  in  ProbHHH6b
# for prob  in  ProbHH4b 
do
    # for year in  2018 2017 2016 2016APV
    for year in 2016APV201620172018
     

    do


        python apply_binning_for_kappa_run2.py --year $year --prob $prob --var ProbMultiH --version v33_new  &
        # python apply_binning_cat_2017.py --year $year --path_year 2017 --prob $prob --var ProbMultiH --doSyst --version v33  &
        # python apply_binning_cat_2016.py --year $year --path_year 2016 --prob $prob --var ProbMultiH  --doSyst --version v33_new  &
        # python apply_binning_cat_2016APV.py --year $year --path_year 2016APV --prob $prob --var ProbMultiH --doSyst  --version v33_new  &
        # python apply_binning_cat_1.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_cat_2.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_cat_3.py --year $year --prob $prob --var ProbHHH  --version v32 --doSyst &
        # python apply_binning_for_kappa.py --year $year --prob  $prob &

        

    done
done

