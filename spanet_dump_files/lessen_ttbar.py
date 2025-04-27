import ROOT
import random 

# 打开原始 ROOT 文件
input_path = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tree.root"

output_path_12percent = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tree_12percent.root"
output_path_88percent = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tree_88percent.root"

# 读取输入文件和 TTree
input_file = ROOT.TFile.Open(input_path, "READ")
tree = input_file.Get("Events")
ROOT.SetOwnership(tree, False)  # 防止 ROOT 清理错误

# 创建输出文件和空的 TTree
output_file_12percent = ROOT.TFile.Open(output_path_12percent, "RECREATE")
output_file_88percent = ROOT.TFile.Open(output_path_88percent, "RECREATE")

output_tree_12percent = tree.CloneTree(0)
output_tree_88percent = tree.CloneTree(0)

ROOT.SetOwnership(output_tree_12percent, False)
ROOT.SetOwnership(output_tree_88percent, False)

n_entries = tree.GetEntries()
print(f"原始 TTree 总 entry 数: {n_entries}")
print("正在随机采样 12% 的 entries 和剩余 88%...")

# 主循环：随机抽样，12% 的 entries 被保存到一个文件，剩余的 88% 被保存到另一个文件
for i in range(n_entries):
    tree.GetEntry(i)
    if random.random() < 0.12:
        output_tree_12percent.Fill()  # 12% 存入这个文件
    else:
        output_tree_88percent.Fill()  # 剩余 88% 存入另一个文件

    if i % 1000000 == 0:
        print(f"已处理: {i} / {n_entries}", end="\r")

print("\nWriting output...")
output_file_12percent.Write()
output_file_88percent.Write()

output_file_12percent.Close()
output_file_88percent.Close()
input_file.Close()

# 显式删除引用（保险）
del output_tree_12percent
del output_tree_88percent
del tree
del input_file
del output_file_12percent
del output_file_88percent

print("✅ Done! Outputs written to:")
print(f"12%: {output_path_12percent}")
print(f"88%: {output_path_88percent}")
