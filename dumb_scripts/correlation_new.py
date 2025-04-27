import ROOT
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 读取 ROOT 文件
path = "/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights"
root_files = [f"{path}/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root", f"{path}/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",f"{path}/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",f"{path}/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",f"{path}/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",f"{path}/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",f"{path}/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",f"{path}/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root",f"{path}/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8_tree.root"]
tree_name = "Events"
N_JETS = 10 
N_FJETS = 3 # 选择 jet 数量

# 2. 选择需要的 branch
selected_branches = ["hhh_mass", "hhh_pt","met","ht","h1_t3_mass","h1_t3_pt","h2_t3_mass","h2_t3_pt","h3_t3_mass","h3_t3_pt"] + \
                    [f"jet{i}Pt" for i in range(1, N_JETS+1)] + \
                    [f"jet{i}bRegCorr" for i in range(1, N_JETS+1)] +\
                    [f"jet{i}Eta" for i in range(1, N_JETS + 1)] +\
                    [f"jet{i}Phi" for i in range(1, N_JETS + 1)] +\
                    [f"jet{i}Mass" for i in range(1, N_JETS + 1)] +\
                    [f"jet{i}PNetTagCat" for i in range(1, N_JETS + 1)] +\
                    [f"fatJet{i}Pt" for i in range(1, N_FJETS + 1)] +\
                    [f"fatJet{i}Eta" for i in range(1, N_FJETS + 1)] +\
                    [f"fatJet{i}Pt" for i in range(1, N_FJETS + 1)] +\
                    [f"fatJet{i}Mass" for i in range(1, N_FJETS + 1)] +\
                    [f"fatJet{i}PNetXbbTagCat" for i in range(1, N_FJETS + 1)] +\
                    [f"ptjet1jet{i}" for i in range(2, N_JETS + 1)] +\
                    [f"ptjet2jet{i}" for i in range(3, N_JETS + 1)] +\
                    [f"ptjet3jet{i}" for i in range(4, N_JETS + 1)] +\
                    [f"ptjet4jet{i}" for i in range(5, N_JETS + 1)] +\
                    [f"ptjet5jet{i}" for i in range(6, N_JETS + 1)] +\
                    [f"ptjet6jet{i}" for i in range(7, N_JETS + 1)] +\
                    [f"ptjet7jet{i}" for i in range(8, N_JETS + 1)] +\
                    [f"ptjet8jet{i}" for i in range(9, N_JETS + 1)] +\
                    [f"ptjet9jet{i}" for i in range(10, N_JETS + 1)] +\
                    [f"massjet1jet{i}" for i in range(2, N_JETS + 1)] +\
                    [f"massjet2jet{i}" for i in range(3, N_JETS + 1)] +\
                    [f"massjet3jet{i}" for i in range(4, N_JETS + 1)] +\
                    [f"massjet4jet{i}" for i in range(5, N_JETS + 1)] +\
                    [f"massjet5jet{i}" for i in range(6, N_JETS + 1)] +\
                    [f"massjet6jet{i}" for i in range(7, N_JETS + 1)] +\
                    [f"massjet7jet{i}" for i in range(8, N_JETS + 1)] +\
                    [f"massjet8jet{i}" for i in range(9, N_JETS + 1)] +\
                    [f"massjet9jet{i}" for i in range(10, N_JETS + 1)] +\
                    [f"drjet1jet{i}" for i in range(2, N_JETS + 1)] +\
                    [f"drjet2jet{i}" for i in range(3, N_JETS + 1)] +\
                    [f"drjet3jet{i}" for i in range(4, N_JETS + 1)] +\
                    [f"drjet4jet{i}" for i in range(5, N_JETS + 1)] +\
                    [f"drjet5jet{i}" for i in range(6, N_JETS + 1)] +\
                    [f"drjet6jet{i}" for i in range(7, N_JETS + 1)] +\
                    [f"drjet7jet{i}" for i in range(8, N_JETS + 1)] +\
                    [f"drjet8jet{i}" for i in range(9, N_JETS + 1)] +\
                    [f"drjet9jet{i}" for i in range(10, N_JETS + 1)] 
                    

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

pt = get_n_features("jet{i}Pt", df_final, range(1, N_JETS+1))
bregcorr = get_n_features("jet{i}bRegCorr", df_final, range(1, N_JETS+1))
ptcorr = pt * bregcorr  # 计算 ptcorr（NumPy 数组）

ptcorr_columns = []  # 用于存储所有 `jet{i}PtCorr` 的列名
for i in range(N_JETS):
    col_name = f"jet{i+1}PtCorr"
    df_final[col_name] = ptcorr[:, i]  # 每个 jet 的 ptcorr 加入 df_final
    ptcorr_columns.append(col_name)  # 记录列名

# 7. 计算 `ptcorr_total`
df_final["ptcorr_total"] = np.sum(ptcorr, axis=1)  # 所有 jet 的 `ptcorr` 之和

# 8. ✅ 动态选择哪些变量计算相关性
# selected_for_corr = ["hhh_mass", "hhh_pt", "ptcorr_total"] 
# selected_main = ["hhh_mass","hhh_pt","h1_t3_mass","h1_t3_pt","h2_t3_mass","h2_t3_pt","h3_t3_mass","h3_t3_pt"]+[f"jet{i}PNetTagCat" for i in range(1, N_JETS + 1)] +[f"fatJet{i}PNetXbbTagCat" for i in range(1, N_FJETS + 1)]
# selected_others = [col for col in df_final.columns if col not in selected_main]  
# corr_matrix = df_final[selected_others].corrwith(df_final[selected_main]) 
#  # 计算相关性
# corr_df = corr_matrix.unstack().reset_index()
# corr_df.columns = ["Feature", "Main Feature", "Correlation"]
# pivot_corr = corr_df.pivot(index="Feature", columns="Main Feature", values="Correlation")

# n_rows = len(pivot_corr)  # 纵轴变量个数
# n_cols = len(selected_main)  # 横轴变量个数
# fig_width = max(10, n_cols * 0.5)  # 每个变量 0.5 单位宽度，至少 10
# fig_height = max(15, n_rows * 0.2)  # 每个变量 0.2 单位高度，至少 15

# plt.figure(figsize=(fig_width, fig_height))
# sns.heatmap(pivot_corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)

# plt.xticks(rotation=45, ha="right")  # 横轴标签倾斜 45°，防止重叠
# plt.yticks(fontsize=8)  # 纵轴标签字体变小，避免重叠
# plt.title("Correlation between Selected Features and Other Variables")
# plt.savefig("corr_non_square.pdf", format="pdf", dpi=300, bbox_inches="tight")



selected_for_corr = [col for col in df_final.columns if not col.startswith("jet") or not col.endswith("Pt")]
corr_matrix = df_final[selected_for_corr].corr()
n_vars = len(selected_for_corr)  # 变量数量
fig_width = max(15, n_vars * 0.3)  # 每个变量 0.3 单位宽度，至少 15
fig_height = max(15, n_vars * 0.3)  # 每个变量 0.3 单位高度，至少 15
plt.figure(figsize=(fig_width, fig_height))
sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap="coolwarm", linewidths=0.5, square=True)
plt.xticks(rotation=90, fontsize=6)  # X 轴标签旋转 90° 并减小字体
plt.yticks(fontsize=6)  # Y 轴字体变小，避免重叠
plt.title("Full Correlation Matrix", fontsize=14)
plt.savefig("corr_QCD_large.pdf", format="pdf", dpi=300, bbox_inches="tight")

# 9. 绘制热力图
# plt.figure(figsize=(10, 8))
# sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
# plt.title("Correlation Matrix of Selected Branches")
# plt.savefig("corr_QCD.pdf", format="pdf", dpi=300, bbox_inches="tight")  # 保存图像
# plt.show()
