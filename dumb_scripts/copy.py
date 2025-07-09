import os
import shutil

def copy_histograms_to_new_location(base_path, new_base_path):
    # Walk through all the directories in the base_path
    for dirpath, dirnames, filenames in os.walk(base_path):
        # Check if the directory is one of the target directories
        if "ProbHHH6" in os.path.basename(dirpath):
            # Check if there is a 'histograms' directory inside
            histograms_dir = os.path.join(dirpath, "histograms")
            if os.path.isdir(histograms_dir):
                # Construct the new directory path
                relative_path = os.path.relpath(dirpath, base_path)
                new_dir_path = os.path.join(new_base_path, relative_path)
                
                # Create the directory if it doesn't exist
                if not os.path.exists(new_dir_path):
                    os.makedirs(new_dir_path)
                
                # Copy the entire 'histograms' directory to the new location
                new_histograms_dir = os.path.join(new_dir_path, "histograms")
                if not os.path.exists(new_histograms_dir):
                    os.makedirs(new_histograms_dir)
                
                # Copy files inside 'histograms' to the new location
                for item in os.listdir(histograms_dir):
                    s = os.path.join(histograms_dir, item)
                    d = os.path.join(new_histograms_dir, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
                
                print(f"Copied histograms from {histograms_dir} to {new_histograms_dir}")

# Define the base path (current directory) and the new base path where the folders will be copied
base_path = "/eos/cms/store/group/phys_higgs/cmshhh/v34-test/add_TTHH_v34/2017" # Current directory
new_base_path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34_test/2017"  # Replace this with the target directory path

# Call the function to copy the histograms
copy_histograms_to_new_location(base_path, new_base_path)
