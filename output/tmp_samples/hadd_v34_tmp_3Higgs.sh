OUTPUT_DIR="/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/tmp_samples"
# cat_strings=("2Higgs" "1bh2h" "2bh1h" "3bh0h" "0bh2h" "1bh1h" "2bh0h" "1Higgs" "0bh0h")
cat_strings=("2Higgs")
# var_strings=("h1_spanet_boosted_mass" "h2_spanet_boosted_mass" "h3_spanet_boosted_mass" "ProbMultiH_regubin")
var_strings=("ProbMultiH")
# year_strings=("2016_all" "2017" "2018")
year_strings=("v34_2016_test2")
type_strings=("ProbHHH6b")
# year_strings=("2016_all")


for str in "${cat_strings[@]}"; do
    for var in "${var_strings[@]}"; do
        for year in "${year_strings[@]}"; do
            for type in "${type_strings[@]}"; do

        # hadd -f $OUTPUT_DIR/run2/ProbHHH6b_${str}_inclusive_CR/histograms/histograms_${var}_fixAsy.root $OUTPUT_DIR/2018/ProbHHH6b_${str}_inclusive_CR/histograms/histograms_${var}_fixAsy.root $OUTPUT_DIR/2017/ProbHHH6b_${str}_inclusive_CR/histograms/histograms_${var}_fixAsy.root $OUTPUT_DIR/2016/ProbHHH6b_${str}_inclusive_CR/histograms/histograms_${var}_fixAsy.root $OUTPUT_DIR/2016APV/ProbHHH6b_${str}_inclusive_CR/histograms/histograms_${var}_fixAsy.root
        # hadd -f $OUTPUT_DIR/2016_all/ProbHHH6b_${str}_inclusive_CR/histograms/histograms_${var}_fixAsy.root  $OUTPUT_DIR/2016/ProbHHH6b_${str}_inclusive_CR/histograms/histograms_${var}_fixAsy.root $OUTPUT_DIR/2016APV/ProbHHH6b_${str}_inclusive_CR/histograms/histograms_${var}_fixAsy.root

                output_folder1="$OUTPUT_DIR/$year/${type}_${str}_inclusive_CR"
                if [ ! -d "$output_folder1" ]; then
                    mkdir -p "$output_folder1"
                    echo "folder already produced: $output_folder1"
                else
                    echo "folder already exist: $output_folder1"
                fi

                output_folder2="$OUTPUT_DIR/$year/${type}_${str}_inclusive_CR/histograms"
                if [ ! -d "$output_folder2" ]; then
                    mkdir -p "$output_folder2"
                    echo "folder already produced: $output_folder2"
                else
                    echo "folder already exist: $output_folder2"
                fi

                hadd -f $OUTPUT_DIR/$year/${type}_3Higgs_inclusive_CR/histograms/histograms_${var}_fixAsy.root  $OUTPUT_DIR/$year/${type}_3bh0h_inclusive_CR/histograms/histograms_${var}_fixAsy.root $OUTPUT_DIR/$year/${type}_2bh1h_inclusive_CR/histograms/histograms_${var}_fixAsy.root $OUTPUT_DIR/$year/${type}_1bh2h_inclusive_CR/histograms/histograms_${var}_fixAsy.root $OUTPUT_DIR/$year/${type}_0bh3h_inclusive_CR/histograms/histograms_${var}_fixAsy.root
            done
        done
    done 

done


