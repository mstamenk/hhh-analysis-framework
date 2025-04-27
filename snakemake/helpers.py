"""Helper functions for defining inputs and outputs for rules."""
import os
from os.path import isfile, join
import yaml

# TUPLES_DIR = "/eos/lhcb/user/y/yuhaow/BcGamma"
TUPLES_DIR = "/eos/lhcb/wg/BandQ/BcGamma"
OUTPUT_DIR = os.path.join(os.path.dirname(workflow.snakefile), 'outputs')
INPUT_DIR  = os.path.join(os.path.dirname(workflow.snakefile), 'inputs')
SMK_DIR    = os.path.join(os.path.dirname(workflow.snakefile), 'snakemake')
CALIBPARS_DIR = os.path.join(os.path.dirname(workflow.snakefile), 'Calibration')
INPUTRSIM_DIR = os.path.join(os.path.dirname(workflow.snakefile), 'inputs_RapidSim')

def output_path(path):
    assert not path.startswith('/')
    return os.path.join(OUTPUT_DIR, path)


def tuples_path(path):
    assert not path.startswith('/')
    return os.path.join(TUPLES_DIR, path)
