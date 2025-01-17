for cat in 0bh3h 1bh2h 2bh1h 3bh0h
do

    # python make_morphig_scans_run2only.py -i kappa_scale.json -d results -c $cat -t fix_BSM_only
    python make_morphig_scans_reweight_new.py -i kappa_fix_reweight_new.json -d results -c $cat -t fix_reweight_new

done