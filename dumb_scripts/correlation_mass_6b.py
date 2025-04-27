import ROOT
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 读取 ROOT 文件
path = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights"
root_files = [f"{path}/HHHTo6B_c3_0_d4_0_TuneCP5_13TeV-amcatnlo-pythia8_tree.root"]
tree_name = "Events"
N_JETS = 10 
N_FJETS = 3 # 选择 jet 数量

# 2. 选择需要的 branch
selected_branches = ["hhh_mass", "h1_t3_mass","h2_t3_mass","h3_t3_mass"] + \
                    [f"massjet1jet{i}" for i in range(2, N_JETS + 1)] +\
                    [f"massjet2jet{i}" for i in range(3, N_JETS + 1)] +\
                    [f"massjet3jet{i}" for i in range(4, N_JETS + 1)] +\
                    [f"massjet4jet{i}" for i in range(5, N_JETS + 1)] +\
                    [f"massjet5jet{i}" for i in range(6, N_JETS + 1)] +\
                    [f"massjet6jet{i}" for i in range(7, N_JETS + 1)] +\
                    [f"massjet7jet{i}" for i in range(8, N_JETS + 1)] +\
                    [f"massjet8jet{i}" for i in range(9, N_JETS + 1)] +\
                    [f"massjet9jet{i}" for i in range(10, N_JETS + 1)] 
                    

# 3. 读取所有 ROOT 文件
df_list = []
for file in root_files:
    rdf = ROOT.RDataFrame(tree_name, file)  # 读取 ROOT 文件
    df_pandas = pd.DataFrame(rdf.AsNumpy(columns=selected_branches))  # 转换 pandas
    df_list.append(df_pandas)

# 4. 合并所有 ROOT 文件的数据
df_final = pd.concat(df_list, ignore_index=True)

# 5. 计算 ptcorr
def get_n_features(pattern, df, indices):
    """从 DataFrame 里提取多个 feature"""
    return df[[pattern.format(i=i) for i in indices]].values




selected_for_corr = [col for col in df_final.columns if not col.startswith("jet") or not col.endswith("Pt")]
corr_matrix = df_final[selected_for_corr].corr()
n_vars = len(selected_for_corr)  # 变量数量
fig_width = max(15, n_vars * 0.5)  # 每个变量 0.3 单位宽度，至少 15
fig_height = max(15, n_vars * 0.5)  # 每个变量 0.3 单位高度，至少 15
plt.figure(figsize=(fig_width, fig_height))
sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap="coolwarm", linewidths=0.5, square=True)
plt.xticks(rotation=90, fontsize=6)  # X 轴标签旋转 90° 并减小字体
plt.yticks(fontsize=6)  # Y 轴字体变小，避免重叠
plt.title("Full Correlation Matrix", fontsize=14)
plt.savefig("corr_6b_mass.pdf", format="pdf", dpi=300, bbox_inches="tight")

# 9. 绘制热力图
# plt.figure(figsize=(10, 8))
# sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
# plt.title("Correlation Matrix of Selected Branches")
# plt.savefig("corr_QCD.pdf", format="pdf", dpi=300, bbox_inches="tight")  # 保存图像
# plt.show()
