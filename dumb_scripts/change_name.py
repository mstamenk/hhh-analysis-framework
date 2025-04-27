import os

def rename_files_in_directory(base_directory):
    # 遍历当前目录及其子目录
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            # 检查文件名是否为 HHHTo6B_c3_0_d4_0.root
            if file == "HHHTo6B_c3_0_d4_0.root":
                # 构造新的文件名
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, "GluGluToHHHTo6B_SM.root")
                
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")

# 调用函数进行文件重命名
rename_files_in_directory("/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/tmp_samples")
