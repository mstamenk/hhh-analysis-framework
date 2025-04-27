###############################################
# Author: Yuhao Wang (yuhaow@cern.ch)
# Usage:
# snakemake -s this_script.py
# snakemake -j 4 --cores 4 --rerun-incomplete -s this_script.py --use-conda
# snakemake -j 4 --cores 4 --rerun-incomplete --unlock -s this_script.py --use-conda
###############################################
## ---------------------
##       Inputs
## ---------------------
import os
from os.path import isfile, join
import yaml
from pathlib import Path

include   : "helpers.py"
configfile: "snakemake/Selection_Bc2Jpsipi.yaml"

## ---------------------
##       Settings
## ---------------------
workpath  = os.path.dirname(workflow.snakefile)
Env_Conda = "env"

wildcard_constraints: 
    Year=r"\d{2}"
    
Tuple_Bcst = ['tuple_Bcst', 'mct_Bcst']
Tuple_Bc   = ['tuple_Bc', 'mct_Bc']
Decay=['Bc2Jpsipi', 'BcstBc2Jpsipi']
# Mag=['md', 'mu']
# Year=['16', '17', '18']
Mag=['md']
Year=['16']

## ---------------------
##        Main
## ---------------------
rule all:
    input:
        ## Bc**
        expand(output_path("logs/Calib_Bcst_{Decay}_{Mag}{Year}.log"),
            Tuple_Bcst=Tuple_Bcst,
            Decay=Decay,
            Mag=Mag,
            Year=Year,
        ),
        # ## Bc from Bc**
        # expand(output_path("logs/BcMC_{Tuple_Bc}_{Decay}_{Mag}{Year}.log"),
        #     Tuple_Bc=Tuple_Bc,
        #     Decay=Decay,
        #     Mag=Mag,
        #     Year=Year,
        # ),
        # ## Inclusive Bc
        # expand(output_path("logs/IncBcMC_{Tuple_Bc}_Bc2Jpsipi_{Mag}{Year}.log"),
        #     Tuple_Bc=Tuple_Bc,
        #     Mag=Mag,
        #     Year=Year,
        # ),


## -----------------
##       Bc**
## -----------------
rule precut_Bcst:
    input:
        script   = "Samples_Bcst.py",
        cuts     = os.path.join(SMK_DIR, "Selection_{Decay}.yaml"),
        gangadir = "/eos/lhcb/user/y/yuhaow/MC/Bcst_{Decay}/MC_{Decay}_{Mag}{Year}",
    output:
        logs = output_path("logs/BcstMC_{Tuple_Bcst}_{Decay}_{Mag}{Year}.log"),
    params:
        outputdir = tuples_path("Production/Precut"),
    threads: 4
    conda: Env_Conda
    resources: retries=3
    shell:
        '''
        echo "#### Precut to Bc** [{wildcards.Decay}]"
        python {input.script}   --GangaDIR    {input.gangadir}  \
                                --OutputDIR   {params.outputdir}     \
                                --Cuts        {input.cuts}      \
                                --Decay       {wildcards.Decay} \
                                --Tuple       {wildcards.Tuple_Bcst} \
                                --Mag         {wildcards.Mag}   \
                                --Year        {wildcards.Year} | tee {output.logs}
        '''

rule calib_Bcst:
    input:
        script   = "Samples_Calib.py",
        logs     = expand(output_path("logs/BcstMC_{Tuple_Bcst}_{Decay}_{Mag}{Year}.log"), Tuple_Bcst=Tuple_Bcst, Decay=Decay, Mag=Mag, Year=Year),
    output:
        logs     = output_path("logs/Calib_Bcst_{Decay}_{Mag}{Year}.log"),
    params:
        inputroot  = tuples_path("Production/Precut/MC_Bcst_{Decay}_{Mag}{Year}.root"),
        outputroot = tuples_path("Production/Calib/MC_Bcst_{Decay}_{Mag}{Year}.root"),
    threads: 4
    conda: Env_Conda
    resources: retries=3
    shell:
        '''
        echo "#### Gamma eff calib to Bc** [{wildcards.Decay}]"
        python {input.script}   --InputROOT   {params.inputroot}    \
                                --OutputROOT  {params.outputroot}   | tee {output.logs}
        '''

# ## -----------------
# ##   Bc from Bc**
# ## -----------------
# rule precut_Bc:
#     input:
#         script   = "Samples_Bcst.py",
#         cuts     = os.path.join(SMK_DIR, "Selection_{Decay}.yaml"),
#         gangadir = "/eos/lhcb/user/y/yuhaow/MC/Bcst_{Decay}/MC_{Decay}_{Mag}{Year}",
#         logs     = expand(output_path("logs/Calib_Bcst_{Decay}_{Mag}{Year}.log"), Decay=Decay, Mag=Mag, Year=Year),
#     output:
#         logs     = output_path("logs/BcMC_{Tuple_Bc}_{Decay}_{Mag}{Year}.log"),
#     params:
#         outputdir = tuples_path("Production/Precut"),
#     threads: 4
#     conda: Env_Conda
#     resources: retries=3
#     shell:
#         '''
#         echo "#### Precut to Bc from Bc** [{wildcards.Decay}]"
#         python {input.script}   --GangaDIR    {input.gangadir}  \
#                                 --OutputDIR   {params.outputdir}     \
#                                 --Cuts        {input.cuts}      \
#                                 --Decay       {wildcards.Decay} \
#                                 --Tuple       {wildcards.Tuple_Bc} \
#                                 --Mag         {wildcards.Mag}   \
#                                 --Year        {wildcards.Year} | tee {output.logs}
#         '''

# ## -----------------
# ##   Inclusive Bc
# ## -----------------
# rule precut_IncBc:
#     input:
#         script   = "Samples_Bc.py",
#         cuts     = os.path.join(SMK_DIR, "Selection_Bc2Jpsipi.yaml"),
#         logs     = expand(output_path("logs/BcMC_{Tuple_Bc}_{Decay}_{Mag}{Year}.log"), Tuple_Bc=Tuple_Bc, Decay=Decay, Mag=Mag, Year=Year),
#     output:
#         logs = output_path("logs/IncBcMC_{Tuple_Bc}_Bc2Jpsipi_{Mag}{Year}.log"),
#     params:
#         outputdir = tuples_path("Production/Precut"),
#     threads: 4
#     conda: Env_Conda
#     resources: retries=3
#     shell:
#         '''
#         echo "#### Precut to Inclusive Bc"
#         python {input.script}   --OutputDIR   {params.outputdir}     \
#                                 --Cuts        {input.cuts}      \
#                                 --Decay       Bc2Jpsipi \
#                                 --Tuple       {wildcards.Tuple_Bc} \
#                                 --Mag         {wildcards.Mag}   \
#                                 --Year        {wildcards.Year} | tee {output.logs}
#         '''




