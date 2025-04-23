#!/usr/bin/env python3
import os
import re
import glob
import ROOT
import argparse


import time

def get_process_name(filename):
    """
    Given a file path, extract the process name by removing the trailing 
    underscore and digits before the '.root' extension.
    Example:
      "GluGluToHHHTo6B_SMJESDOWN_79.root" -> "GluGluToHHHTo6B_SMJESDOWN"
    """
    basename = os.path.basename(filename)
    # This regex uses a lookahead to match an underscore followed by digits
    # immediately before the ".root" extension.
    process_name = re.sub(r"_[0-9]+(?=\.root$)", "", basename)
    # Remove the .root extension (if still present)
    process_name = process_name.replace(".root", "")
    return process_name

def group_files_by_process(root_dir):
    """
    Recursively search the directory for all .root files and group them
    by process (determined by their name with trailing digits removed).
    Returns a dictionary where keys are process names and values are lists of file paths.
    """
    # Search recursively for *.root files within the specified directory.
    file_pattern = os.path.join(root_dir, "**", "*.root")
    file_list = glob.glob(file_pattern, recursive=True)
    
    groups = {}
    for filepath in file_list:
        process = get_process_name(filepath)
        if process not in groups:
            groups[process] = []
        groups[process].append(filepath)
    return groups

def merge_group(process, file_list, tree_name="Events", output_dir="./merged_outputs"):
    """
    Create an RDataFrame from the given list of ROOT files and
    merge the output (by writing a Snapshot) to a new ROOT file.
    
    Arguments:
      process   -- the process name used for naming the output file.
      file_list -- list of ROOT file paths to merge.
      tree_name -- name of the TTree in the ROOT files.
      output_dir -- directory where the merged file will be saved.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()
    
    print(f"Merging process '{process}' with {len(file_list)} files...")
    # Create an RDataFrame from the list of files
    # RDataFrame accepts a list of filenames (the chain of files)
    df = ROOT.RDataFrame(tree_name, file_list)
    
    # Retrieve all column names from the dataframe (to write all branches)
    columns = df.GetColumnNames()
    
    # Define the output filename as <process>_merged.root in the output directory.
    out_filename = os.path.join(output_dir, f"{process}.root")
    print(f"Saving merged output to: {out_filename}")
    
    # Write out the merged file using Snapshot.
    # Snapshot copies the TTree (with all columns) into the new file.
    df.Snapshot(tree_name, out_filename, columns)

    elapsed_minutes = (time.time() - start_time) / 60.0
    print(f"Process '{process}' merged successfully in {elapsed_minutes:.2f} minutes.\n")


def main():


    parser = argparse.ArgumentParser(description="Merge ROOT samples with RDataFrame")
    parser.add_argument("--version", type=str, default="v37",
                        help="Version string (e.g. 'v1.2.3')")
    parser.add_argument("--year", type=str, default="2018",
                        help="Year string (e.g. '2018')")
    parser.add_argument("--doCat", action="store_true",
                        help="Boolean flag to enable cataloging (doCat)")
    parser.add_argument("--afterCat", action="store_true",
                        help="Boolean flag to enable cataloging (afterCat)")
    parser.add_argument("--secondInference", action="store_true",
                        help="Boolean flag to enable cataloging (secondInference)")

    args = parser.parse_args()

    if args.doCat:
        typename = 'categorisation-spanet-boosted-classification'
    else:
        typename = 'spanet-boosted-classification'

    if args.afterCat:
        typename = 'spanet-boosted-classification-categorisation-spanet-boosted-classification'

    if args.secondInference:
        typename = 'spanet-boosted-classification-spanet-boosted-classification-categorisation-spanet-boosted-classification'


    # Define the directory containing the ROOT files.
    # You can adjust this path as needed.
    start = time.time()
    input_directory = (f"/users/mstamenk/scratch/mstamenk/{args.version}/mva-inputs-{args.year}-{typename}/inclusive-weights/")
    
    # Enable ROOT’s implicit multi-threading (this will use the default number of threads)
    ROOT.ROOT.EnableImplicitMT()
    
    # Group the ROOT files by process.
    groups = group_files_by_process(input_directory)
    
    # Print summary of groups
    print("Found the following process groups:")
    for process, files in groups.items():
        print(f"  {process}: {len(files)} file(s)")
    
    # Loop over the groups and merge each group using RDataFrame.
    # The tree name "Events" is assumed; change if your TTree has a different name.

    out_dir = f'/users/mstamenk/scratch/mstamenk/eos-triple-h/{args.version}-merged-selection/mva-inputs-{args.year}-{typename}/inclusive-weights/'
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    for process, file_list in groups.items():
        try:
            merge_group(process, file_list, tree_name="Events", output_dir=out_dir)
        except Exception as e:
            print(f"Error while processing group '{process}': {e}")

    end_time = (time.time() - start)/60.

    print(f"Total time {end_time:.2f} minutes")


if __name__ == "__main__":
    main()

