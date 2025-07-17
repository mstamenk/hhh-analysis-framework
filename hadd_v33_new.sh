
#!/bin/bash

# Usage: ./hadd_v33_new.sh /your/output/dir
# Exit on any error
set -e

# Get the output dir from argument
OUTPUT_DIR=$1
# OUTPUT_DIR="/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34_final_marko"
# cat_strings=("0bh3h" "1bh2h" "2bh1h" "3bh0h" "0bh2h" "1bh1h" "2bh0h" "1Higgs" "1bh0h" "0bh1h" "0bh0h")
cat_strings=("0bh3h" "1bh2h" "2bh1h" "3bh0h" "0bh2h" "1bh1h" "2bh0h" "1Higgs" "0bh1h" "1bh0h" "0bh0h")
# var_strings=("h1_spanet_boosted_mass" "h2_spanet_boosted_mass" "h3_spanet_boosted_mass" "ProbMultiH_regubin")
var_strings=("ProbMultiH")
type_strings=("ProbHHH6b")
# type_strings=("ProbHH4b")


for str in "${cat_strings[@]}"; do
    for var in "${var_strings[@]}"; do
        for type in "${type_strings[@]}"; do

            output_folder1="$OUTPUT_DIR/2016_all/${type}_${str}_inclusive_CR"
            if [ ! -d "$output_folder1" ]; then
                mkdir -p "$output_folder1"
                echo "folder already produced: $output_folder1"
            else
                echo "folder already exist: $output_folder1"
            fi

            output_folder2="$OUTPUT_DIR/2016_all/${type}_${str}_inclusive_CR/histograms"
            if [ ! -d "$output_folder2" ]; then
                mkdir -p "$output_folder2"
                echo "folder created: $output_folder2"
            else
                echo "folder already exist: $output_folder2"
            fi

            input_file_2016="$OUTPUT_DIR/2016/${type}_${str}_inclusive_CR/histograms/histograms_${var}.root"
            input_file_2016APV="$OUTPUT_DIR/2016APV/${type}_${str}_inclusive_CR/histograms/histograms_${var}.root"
            output_file="$OUTPUT_DIR/2016_all/${type}_${str}_inclusive_CR/histograms/histograms_${var}.root"

            if [ -f "$input_file_2016" ] && [ -f "$input_file_2016APV" ]; then
                echo "Merging files for ${type} ${str} ${var}..."
                hadd -f "$output_file" "$input_file_2016" "$input_file_2016APV"
            else
                echo "Skipping ${type} ${str} ${var}: one or both input files do not exist."
                if [ ! -f "$input_file_2016" ]; then
                    echo "  Missing: $input_file_2016"
                fi
                if [ ! -f "$input_file_2016APV" ]; then
                    echo "  Missing: $input_file_2016APV"
                fi
            fi
        done
    done
done


