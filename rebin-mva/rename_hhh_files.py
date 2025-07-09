#!/usr/bin/env python3
"""
batch_rename_hhh.py

Usage:
    python3 rename_hhh_files.py [--dry-run] [--verbose] /path/to/directory

Renames ROOT files by:
1) Removing the "_TuneCP5..." segment, preserving any _d<value> part and the final _ProbHHH6b_<suffix>_<year>(APV?).
2) Fixing filenames that accidentally contain duplicate "ProbHHH6b_" segments (i.e., "ProbHHH6b_ProbHHH6b_").
Supports HHHTo* and GluGluToHHTo* samples.

Options:
  --dry-run    Show planned renames without executing
  --verbose    Log skipped files and matches
"""
import os
import re
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Batch rename HHH and HH ROOT files.")
    parser.add_argument('directory', help='Directory containing ROOT files')
    parser.add_argument('--dry-run', action='store_true', help="Don't actually rename, just show actions")
    parser.add_argument('--verbose', action='store_true', help="Show files not matching pattern")
    return parser.parse_args()


def main():
    args = parse_args()
    dir_path = args.directory
    if not os.path.isdir(dir_path):
        print(f"ERROR: {dir_path} is not a directory.")
        sys.exit(1)

    # Regex to match files with TuneCP5 segment
    tune_pattern = re.compile(
        r'^(.*?)(?:_d([^_]+))?'                # prefix and optional d-value
        r'_TuneCP5[^_]*amcatnlo[^_]*'           # drop TuneCP5...amcatnlo-pythia8
        r'_ProbHHH6b_([^_]+_[0-9]{4}(?:APV)?)'  # capture ProbHHH6b suffix
        r'\.root$'
    )

    for fname in sorted(os.listdir(dir_path)):
        if not fname.endswith('.root'):
            if args.verbose:
                print(f"Skipping non-root file: {fname}")
            continue
        old_path = os.path.join(dir_path, fname)
        if not os.path.isfile(old_path):
            continue

        # 1) Fix duplicate ProbHHH6b_ProbHHH6b_
        if 'ProbHHH6b_ProbHHH6b_' in fname:
            new_name = fname.replace('ProbHHH6b_ProbHHH6b_', 'ProbHHH6b_')
            new_path = os.path.join(dir_path, new_name)
            msg = f"{fname} -> {new_name}"
            if args.dry_run:
                print(f"Would rename: {msg}")
            else:
                print(f"Renaming duplicate fix: {msg}")
                os.rename(old_path, new_path)
            continue

        # 2) Handle TuneCP5 renaming
        m = tune_pattern.match(fname)
        if m:
            prefix, dval, tail = m.group(1), m.group(2), m.group(3)
            parts = [prefix]
            if dval:
                parts.append('d' + dval)
            parts.append('ProbHHH6b_' + tail)
            new_name = '_'.join(parts) + '.root'
            new_path = os.path.join(dir_path, new_name)
            msg = f"{fname} -> {new_name}"
            if args.dry_run:
                print(f"Would rename: {msg}")
            else:
                print(f"Renaming: {msg}")
                os.rename(old_path, new_path)
        else:
            if args.verbose:
                print(f"No match for: {fname}")

if __name__ == '__main__':
    main()
