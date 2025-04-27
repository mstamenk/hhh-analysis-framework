import ROOT
import os

def check_root_file(file_path):
    try:
        root_file = ROOT.TFile(file_path, "READ")
        if root_file.IsZombie():
            print(f"[ERROR] Failed to open file {file_path}.")
            return

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"[ERROR] File {file_path} is empty.")
            return

        print(f"Checking file {file_path}:")
        tree = root_file.Get("Events")  # 修改为实际树名
        if not tree:
            print(f"[ERROR] Tree 'Events' not found in {file_path}.")
            return

        n_entries = tree.GetEntries()
        print(f"Total entries in tree: {n_entries}")
        for entry in range(n_entries):
            tree.GetEntry(entry)
            try:
                ht_value = tree.ht  # 修改为实际分支名
                if ht_value is None:
                    print(f"[ERROR] Missing or invalid data for 'ht' at entry {entry} in {file_path}.")
            except Exception as e:
                print(f"[ERROR] Error accessing entry {entry} in {file_path}: {str(e)}")

        print(f"File size: {file_size} bytes")
        root_file.Close()
    except Exception as e:
        print(f"[ERROR] Failed to process file {file_path}: {str(e)}")

def check_all_root_files(directory):
    # 跳过列表（只保留文件名，不带路径）
    skip_files = {
        "GluGluToHHTo2B2Tau.root",
        "GluGluToHHTo4B_cHHH1.root",
        "HHHTo6B_c3_0_d4_0.root",
        "QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",
        "QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",
        "QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",
        "QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",
        "QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",
        "QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",
        "QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",
        "TTHHTo4b_TuneCP5_13TeV-madgraph-pythia8_tree.root",
        "TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tree.root"
    }

    for filename in os.listdir(directory):
        if filename.endswith(".root"):
            if filename == "BTagCSV.root" or filename in skip_files:
                print(f"Skipping file {filename}")
                continue
            file_path = os.path.join(directory, filename)
            check_root_file(file_path)

if __name__ == "__main__":
    directory_path = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights"
    check_all_root_files(directory_path)
