import ROOT
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 读取 ROOT 文件
file_name = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights/HHHTo6B_c3_0_d4_0_TuneCP5_13TeV-amcatnlo-pythia8_tree.root"
tree_name = "Events"  # 你的 TTree 名称，通常需要确认

# 2. 选择需要的 branch
selected_branches = ["hhh_mass", "hhh_pt", "h1_t3_mass","h1_t3_pt","h2_t3_mass","h2_t3_pt","h3_t3_mass","h3_t3_pt"]+[f"jet{i}Pt" for i in range(1, 11)]

# 3. 用 RDataFrame 读取数据
df = ROOT.RDataFrame(tree_name, file_name)

# 4. 转换成 pandas DataFrame
df_pandas = pd.DataFrame(df.AsNumpy(columns=selected_branches))

# 5. 计算相关性矩阵
corr_matrix = df_pandas.corr()

# 6. 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Matrix of Selected Branches")
plt.savefig("corr_6b.pdf")
