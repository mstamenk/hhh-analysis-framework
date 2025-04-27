import ROOT
import glob
import os

# 设置路径与通配符
path_pattern = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2018/mc/v34_mc_ak8_option4_2018/mc/parts/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tree_*.root"

# 使用 glob 匹配所有文件
file_list = glob.glob(path_pattern)
print(f"Found {len(file_list)} ROOT files.")

# 树的名称
tree_name = "Events"  # 如果树不是 Events，请改成你实际使用的树名

# 初始化总 entries 计数器
total_entries = 0

# 遍历每个文件
for file_path in file_list:
    try:
        root_file = ROOT.TFile.Open(file_path)
        if not root_file or root_file.IsZombie():
            print(f"[WARNING] Could not open file: {file_path}")
            continue
        
        tree = root_file.Get(tree_name)
        if not tree:
            print(f"[WARNING] Tree '{tree_name}' not found in: {file_path}")
            continue

        entries = tree.GetEntries()
        total_entries += entries
        print(f"{os.path.basename(file_path)}: {entries} entries")

        root_file.Close()

    except Exception as e:
        print(f"[ERROR] Exception while processing {file_path}: {e}")

print(f"\n✅ Total number of entries across all files: {total_entries}")
