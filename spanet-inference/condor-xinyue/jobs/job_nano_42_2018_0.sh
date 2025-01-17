#! /bin/bash
#SBATCH -p batch
#SBATCH -n 1
#SBATCH -t 03:00:00
#SBATCH --mem=24g
python3 /eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/spanet-inference//predict_spanet_classification_categorisation.py --f_in nano_42 --year 2018 --batch_size 50000 --batch_number 0 --version v31-parts-no-lhe
exit