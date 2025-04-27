import os
import ROOT

# 映射字典
mappings = {
    'GluGluToHHHTo6B_SM': 1,
    'QCD_HT': 2,
    'TTToHadronic_TuneCP5_13TeV-powheg-pythia8': 3,
    'GluGluToHHTo4B_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8': 4,
    'TTHHTo4b_TuneCP5_13TeV-madgraph-pythia8_tree': 5,
    
}

def get_file_size_and_entries(file_path):
    """获取ROOT文件大小和entries数量"""
    # 获取文件大小，并转换为GB
    file_size = os.path.getsize(file_path) / (1024 ** 3)  # 转换为GB
    
    # 使用ROOT读取文件并获取entries数目
    try:
        file = ROOT.TFile(file_path)
        tree = file.Get("Events")  # 假设树的名字是'Events'
        entries = tree.GetEntries() if tree else 0
        return file_size, entries
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0, 0

def scan_directory(directory_path):
    """扫描目录，输出符合映射的ROOT文件大小和entries"""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".root"):
                # 获取文件名
                base_name = os.path.splitext(file)[0]
                
                # 检查文件名是否在mappings字典中
                if base_name in mappings:
                    file_path = os.path.join(root, file)
                    file_size, entries = get_file_size_and_entries(file_path)
                    print(f"File: {file}, Mapping: {base_name}, Size: {file_size:.2f} GB, Entries: {entries}")

# 使用你的路径替换下面的示例路径
directory_path = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2018/mva-inputs-2018/inclusive-weights"
scan_directory(directory_path)
