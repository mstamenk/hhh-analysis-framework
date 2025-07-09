import os

# ✅ 自定义你想要遍历的目标根目录
target_dir = "/eos/cms/store/group/phys_higgs/cmshhh/v34-fix-ak4-ak8"  # ← 改成你要操作的路径

# ✅ 你自定义的重命名字典
rename_dict = {
    "GluGluToHHTo4B_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8.root": "GluGluToHHTo4B_cHHH0.root",
    "GluGluToHHTo4B_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8.root": "GluGluToHHTo4B_cHHH1.root",
    "GluGluToHHTo4B_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8.root": "GluGluToHHTo4B_cHHH2p45.root",
    "GluGluToHHTo4B_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8.root": "GluGluToHHTo4B_cHHH5.root",
    "HHHTo6B_c3_0_d4_99_TuneCP5_13TeV_amcatnlo-pythia.root": "HHHTo6B_c3_0_d4_99.root",
    "HHHTo6B_c3_0_d4_minus1_TuneCP5_13TeV_amcatnlo-pythia8.root":"HHHTo6B_c3_0_d4_minus1.root",
    "HHHTo6B_c3_19_d4_19_TuneCP5_13TeV_amcatnlo-pythia8.root":"HHHTo6B_c3_19_d4_19.root",
    "HHHTo6B_c3_1_d4_0_TuneCP5_13TeV_amcatnlo-pythia8.root": "HHHTo6B_c3_1_d4_0.root",
    "HHHTo6B_c3_1_d4_2_TuneCP5_13TeV_amcatnlo-pythia8.root": "HHHTo6B_c3_1_d4_2.root",
    "HHHTo6B_c3_2_d4_minus1_TuneCP5_13TeV_amcatnlo-pythia8.root": "HHHTo6B_c3_2_d4_minus1.root",
    "HHHTo6B_c3_4_d4_9_TuneCP5_13TeV_amcatnlo-pythia8.root":"HHHTo6B_c3_4_d4_9.root",
    "HHHTo6B_c3_minus1_d4_0_TuneCP5_13TeV_amcatnlo-pythia8.root":"HHHTo6B_c3_minus1_d4_0.root",
    "HHHTo6B_c3_minus1_d4_minus1_TuneCP5_13TeV_amcatnlo-pythia8.root": "HHHTo6B_c3_minus1_d4_minus1.root",
    "HHHTo6B_c3_minus1p5_d4_minus0p5_TuneCP5_13TeV_amcatnlo-pythia8.root": "HHHTo6B_c3_minus1p5_d4_minus0p5.root",
    "HHHTo6B_c3_0_d4_99_TuneCP5_13TeV_amcatnlo-pythia8.root": "HHHTo6B_c3_0_d4_99.root",
    "GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_SM_13TeV-madgraph-pythia8.root": "GluGluToHHTo2B2Tau.root",
    "HHHTo4B2Tau_c3_0_d4_0_TuneCP5_13TeV-amcatnlo-pythia8.root": "HHHTo4B2Tau_c3_0_d4_0.root",


    # 可以继续添加更多条目
}

# ✅ 遍历指定文件夹下的所有子目录和文件
for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file in rename_dict:
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, rename_dict[file])
            if os.path.exists(new_path):
                print(f"[跳过] 已存在: {new_path}")
            else:
                os.rename(old_path, new_path)
                print(f"[重命名] {file} → {rename_dict[file]} in {root}")
