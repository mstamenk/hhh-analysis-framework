import ROOT
import os

def check_root_file(file_path):
    try:
        # 打开ROOT文件
        root_file = ROOT.TFile(file_path, "READ")
        
        # 检查文件是否打开成功
        if root_file.IsZombie():
            print(f"[ERROR] Failed to open file {file_path}.")
            return
        
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"[ERROR] File {file_path} is empty.")
            return
        
        print(f"Checking file {file_path}:")
        
        # 获取树对象
        tree = root_file.Get("Events")  # 修改为你的实际树名
        if not tree:
            print(f"[ERROR] Tree 'Events' not found in {file_path}.")
            return
        
        n_entries = tree.GetEntries()
        print(f"Total entries in tree: {n_entries}")
        
        # 示例：检查第一个 entry 是否能正常读取
        for entry in range(n_entries):
            tree.GetEntry(entry)
            try:
                ht_value = tree.ht
                if ht_value is None:
                    print(f"[ERROR] Missing or invalid data for 'ht' at entry {entry} in {file_path}.")
  # 修改为你的分支名
            except Exception as e:
                print(f"[ERROR] Error accessing entry {entry} in {file_path}: {str(e)}")
        
        print(f"File size: {file_size} bytes")
        root_file.Close()

    except Exception as e:
        print(f"[ERROR] Failed to process file {file_path}: {str(e)}")

def check_selected_files(file_list):
    for file_path in file_list:
        check_root_file(file_path)


path_check="/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights"
if __name__ == "__main__":
    # ✏️ 在这里列出你要检查的10个文件（可以是绝对路径或相对路径）
    files_to_check = [
        "%s/GluGluToHHTo2B2Tau.root"%(path_check),
        "%s/GluGluToHHTo4B_cHHH1.root"%(path_check),
        "%s/HHHTo6B_c3_0_d4_0.root"%(path_check),
        "%s/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root"%(path_check),
        "%s/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root"%(path_check),
        "%s/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root"%(path_check),
        "%s/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root"%(path_check),
        "%s/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root"%(path_check),
        "%s/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root"%(path_check),
        "%s/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root"%(path_check),
        "%s/TTHHTo4b_TuneCP5_13TeV-madgraph-pythia8_tree.root"%(path_check),
        "%s/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tree.root"%(path_check),
        
    ]

    check_selected_files(files_to_check)
