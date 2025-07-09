#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uproot
import numpy as np
import pandas as pd

# ——— Configuration ———
# 1) Define the base directory
base_dir = "/eos/cms/store/group/phys_higgs/cmshhh/v34-test/BTV"

# 2) Define integrated luminosities (in pb^-1) for each year or sub-period
luminosities = {
    '2016APV'      : 19207.0,
    '2016PostAPV'  : 17122.0,
    '2016'         : 17122.0,
    '2017'         : 41480.0,
    '2018'         : 59830.0,
    '2022'         : 8174.68,
    '2022EE'       : 27007.2,
    '2023'         : 17628.0,
    '2023BPix'     : 9525.0, 
}

# 3) List of processes to include in the yield summation
process_list = ['DYJetsToL', 'QCD','GluGluToHHHTo6B_SM','GluGluToHHTo2B2Tau','GluGluToHHTo4B_cHHH1','TTTo','WJets']

# 4) Two sets of weight definitions (branch names in the ROOT tree)
weight_branches = {
    'all':  [
        'xsecWeight',
        'l1PreFiringWeight',
        'puWeight',
        'genWeight',
        'triggerSF',
        'fatJetFlavTagWeight',
        'flavTagWeight'
    ],
    'none': [
        'xsecWeight',
        'l1PreFiringWeight',
        'puWeight',
        'genWeight',
        'triggerSF'
    ]
}
# ————————————————

results = []

# Loop over each year (or sub-period) in the base directory
for year in sorted(os.listdir(base_dir)):
    year_dir = os.path.join(base_dir, year)
    if not os.path.isdir(year_dir):
        continue

    # Lookup the luminosity for this year
    lumi = luminosities.get(year)
    if lumi is None:
        print(f"[WARN] No luminosity defined for {year}, skipping.")
        continue

    # Find all classification folders starting with "ProbHHH6b"
    for category in sorted(os.listdir(year_dir)):
        if not category.startswith("ProbHHH6b"):
            continue
        category_dir = os.path.join(year_dir, category)
        if not os.path.isdir(category_dir):
            continue

        # Loop over all ROOT files in this category folder
        for filename in os.listdir(category_dir):
            if not filename.endswith(".root"):
                continue
            filepath = os.path.join(category_dir, filename)

            # Only process the ROOT files matching our process list
            if not any(proc in filename for proc in process_list):
                continue

            # Open the ROOT file and get the "Events" tree
            with uproot.open(filepath) as f:
                tree = f.get("Events")
                if tree is None:
                    print(f"[WARN] 'Events' tree not found in {filepath}, skipping.")
                    continue

                # Compute the weighted yield for each weight type
                for wtype, branches in weight_branches.items():
                    # Read all branches as NumPy arrays
                    data = tree.arrays(branches, library="np")
                    # Multiply them together to form the total per-event weight
                    weights = data[branches[0]]
                    for br in branches[1:]:
                        weights *= data[br]
                    # Sum over all events and scale by luminosity
                    total_yield = np.sum(weights) * lumi

                    # Record the result
                    results.append({
                        'year'          : year,
                        'category'      : category,
                        'filename'      : filename,
                        'weight_type'   : wtype,
                        'process'       : filename.split('_')[0],
                        'yield'         : total_yield
                    })

# Convert results to a DataFrame
df = pd.DataFrame(results)

# Aggregate (sum) yields by year, category, process, and weight type
agg_df = (
    df
    .groupby(['year', 'category', 'process', 'weight_type'])
    .agg({'yield': 'sum'})
    .reset_index()
)

# Pivot so that each weight type becomes a separate column
summary = (
    agg_df
    .pivot_table(
        index=['year', 'category', 'process'],
        columns='weight_type',
        values='yield'
    )
    .reset_index()
)

# Clean up column names
summary.columns.name = None
summary = summary.rename(columns={'all': 'yield_all', 'none': 'yield_none'})

# Sort the table for readability
summary = summary.sort_values(['year', 'category', 'process'])

# Write to CSV
out_csv = "yields_summary_combined.csv"
summary.to_csv(out_csv, index=False)

# Print a preview
print(f"Results saved to {out_csv}. Preview:")
print(summary.to_string(index=False))
