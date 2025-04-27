###############################################
# Author: Yuhao Wang
# Snakemake Workflow for your process
###############################################

# Set up input and output paths
input_dir = "output/v33_new"  # Assuming output path is in this directory
script_dir = "."  # Assuming the scripts are in the current directory

## ---------------------
##       Settings
## ---------------------
# Env_Conda = "env"  # Conda environment

Year = ["2016APV", "2016", "2017", "2018"]
Prob = ["ProbHHH6b"]
Var = ["ProbMultiH"]  # as you are using this variable in each command
Version = "v34"
Category = ["ProbHHH6b_0bh3h_inclusive"]  # For last step

## ---------------------
##       First Step: Apply Binning
## ---------------------
rule apply_binning:
    input:
        script_2018 = "apply_binning_cat_2018.py",
        script_2017 = "apply_binning_cat_2017.py",
        script_2016 = "apply_binning_cat_2016.py",
        script_2016APV = "apply_binning_cat_2016APV.py"
    output:
        temp_dir = temp("output/v33_new/{year}_{prob}_binning_done")
    params:
        version = Version
    threads: 4
    shell:
        """
        for year in {wildcards.year}
        do
            for prob in {wildcards.prob}
            do
                python {input.script_2018} --year $year --path_year 2018 --prob $prob --var {wildcards.var} --doSyst --version {params.version} &
                python {input.script_2017} --year $year --path_year 2017 --prob $prob --var {wildcards.var} --doSyst --version {params.version} &
                python {input.script_2016} --year $year --path_year 2016 --prob $prob --var {wildcards.var} --doSyst --version {params.version} &
                python {input.script_2016APV} --year $year --path_year 2016APV --prob $prob --var {wildcards.var} --doSyst --version {params.version} &
            done
        done
        wait
        """

## ---------------------
##       Second Step: Run hadd_v33_new.sh
## ---------------------
rule hadd_v33_new:
    input:
        script = "hadd_v33_new.sh"
    output:
        "output/v33_new/hadd_v33_new_done"
    shell:
        "source {input.script} && touch {output}"

## ---------------------
##       Third Step: Run Correction_Asymeric.py
## ---------------------
rule correction_asymmetric:
    input:
        script = "Correction_Asymeric.py"
    output:
        "output/v33_new/Correction_Asymeric_done"
    shell:
        "python {input.script} && touch {output}"

## ---------------------
##       Fourth Step: Run hadd_v33_new_2Higgs.sh and hadd_v33_new_3Higgs.sh
## ---------------------
rule hadd_v33_new_2Higgs:
    input:
        script = "hadd_v33_new_2Higgs.sh"
    output:
        "output/v33_new/hadd_v33_new_2Higgs_done"
    shell:
        "source {input.script} && touch {output}"

rule hadd_v33_new_3Higgs:
    input:
        script = "hadd_v33_new_3Higgs.sh"
    output:
        "output/v33_new/hadd_v33_new_3Higgs_done"
    shell:
        "source {input.script} && touch {output}"

## ---------------------
##       Fifth Step: Run merge_separate.py
## ---------------------
rule merge_separate:
    input:
        script = "merge_separate.py"
    output:
        "output/v33_new/merge_separate_done"
    shell:
        "python {input.script} && touch {output}"

## ---------------------
##       Sixth Step: Skim Tree
## ---------------------
rule skimm_tree:
    input:
        script = "skimm_tree.py"
    output:
        temp_dir = temp("output/v33_new/{var}_skimmed_done")
    params:
        category = Category
    threads: 4
    shell:
        """
        for var in {wildcards.var}
        do
            python {input.script} --skip_do_trees --skip_do_plots --skip_do_histograms --category $var --do_limit_input {wildcards.var} --do_CR &
        done
        wait
        """

## ---------------------
##       Final Output
## ---------------------
rule all:
    input:
        expand("output/v33_new/{var}_skimmed_done", var=Category),
        "output/v33_new/merge_separate_done",
        "output/v33_new/hadd_v33_new_done",
        "output/v33_new/hadd_v33_new_2Higgs_done",
        "output/v33_new/hadd_v33_new_3Higgs_done",
        "output/v33_new/Correction_Asymeric_done"
