import uproot as urt
import numpy as np
import os
import argparse
import glob
import ROOT

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--searchString", help="Search String for .root files")
args = parser.parse_args()

# Collect files
fNames = glob.glob(args.searchString.replace("@", "*"))

# Initialize total weight
total_entries = 0.0
treeName = 'Events'

# Process each file
# Process each file
for i, fileName in enumerate(fNames):
    # Print file index and name
    # print(f"[{i+1} / {len(fNames)}] Processing file: {fileName}")

    try:
        # Use ROOT to open file
        fileIn = ROOT.TFile.Open(fileName)
        if not fileIn or fileIn.IsZombie():
            print(f"  > ERROR: Cannot open file {fileName} or file is corrupted.")
            continue

        # Check if the tree exists
        if not fileIn.Get(treeName):
            print(f"  > WARNING: '{treeName}' not found in {fileName}, skipping this file.")
            fileIn.Close()
            continue

        # Get the tree and count entries
        data = fileIn.Get(treeName)
        entries = data.GetEntries()
        # print(f"  > {fileName}: Obtained file with {entries} events")

        # Sum entries
        total_entries += entries

        # Close the file
        fileIn.Close()

    except Exception as e:
        print(f"  > ERROR: Failed to process {fileName}. Error: {str(e)}")
        continue

# Output total entries
print(f"Total entries from all files: {total_entries}")