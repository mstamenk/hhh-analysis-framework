
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
        
        # 获取树对象（假设树的名称为 "tree_name"）
        tree = root_file.Get("Events")  # 修改为实际树名称
        if not tree:
            print(f"[ERROR] Tree 'tree_name' not found in {file_path}.")
            return
        
        # 检查文件是否填充正确，遍历所有entries
        n_entries = tree.GetEntries()
        print(f"Total entries in tree: {n_entries}")
        
        # 遍历所有条目，检查每个条目是否能成功读取
        for entry in range(n_entries):
            tree.GetEntry(entry)
            # 检查各个分支数据是否有效
            try:
                # 假设我们要检查的分支名为"ht"，可以在此处扩展检查其他分支
                ht_value = tree.ht  # 修改为你实际分支名
                if ht_value is None:
                    print(f"[ERROR] Missing or invalid data for 'ht' at entry {entry} in {file_path}.")
            except Exception as e:
                print(f"[ERROR] Error accessing entry {entry} in {file_path}: {str(e)}")
        
        # 打印文件的大小信息
        print(f"File size: {file_size} bytes")
        
        # 关闭文件
        root_file.Close()
    except Exception as e:
        print(f"[ERROR] Failed to process file {file_path}: {str(e)}")

# def check_all_root_files(directory):
#     # 获取指定目录下所有的 .root 文件
#     for filename in os.listdir(directory):
#         if filename.endswith(".root"):  # 只处理 .root 文件
#             file_path = os.path.join(directory, filename)
#             check_root_file(file_path)

def check_all_root_files(directory):
    # 获取指定目录下所有的 .root 文件
    for filename in os.listdir(directory):
        if filename.endswith(".root"):
            # 如果文件名是BTagCSV.root，则跳过
            if filename == "BTagCSV.root":
                print(f"Skipping file {filename}")
                continue  # 跳过这个文件

            file_path = os.path.join(directory, filename)
            check_root_file(file_path)

if __name__ == "__main__":
    # 设置要检查的根文件夹路径
    directory_path = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights"  # 请修改为实际路径
    
    # 检查该目录下所有的ROOT文件
    check_all_root_files(directory_path)