import ROOT
import matplotlib.pyplot as plt
import numpy as np

# 禁用交互式显示
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()  # 启用并行处理
cat = '''
int cat_reco_function(int nFatJetsPassed, int nJetsPassed, float hhh_mass2) {
    if (hhh_mass2 > 700) {
        if (nFatJetsPassed == 3) return 1;
        else if (nFatJetsPassed == 2 && nJetsPassed >= 2) return 2;
        else if (nFatJetsPassed == 2 && nJetsPassed < 2) return 5;
        else if (nFatJetsPassed == 1 && nJetsPassed >= 4) return 3;
        else if (nFatJetsPassed == 1 && nJetsPassed < 4 && nJetsPassed >= 2 ) return 6;
        else if (nFatJetsPassed == 1 && nJetsPassed < 2) return 8;
        else if (nFatJetsPassed == 0 && nJetsPassed == 6) return 4;
        else if (nFatJetsPassed == 0 && nJetsPassed < 6 && nJetsPassed >= 4) return 7;
        else if (nFatJetsPassed == 0 && nJetsPassed < 4 && nJetsPassed >= 2) return 9;
        else if (nFatJetsPassed == 0 && nJetsPassed < 2) return 0;
    }
    else if (hhh_mass2 <= 700) {
        if (nJetsPassed == 6) return 4;
        else if (nJetsPassed < 6 && nJetsPassed >= 4 && nFatJetsPassed >= 1) return 3;
        else if (nJetsPassed < 6 && nJetsPassed >= 4 && nFatJetsPassed < 1) return 7;
        else if (nJetsPassed < 4 && nJetsPassed >= 2 && nFatJetsPassed >= 2) return 2;
        else if (nJetsPassed < 4 && nJetsPassed >= 2 && nFatJetsPassed == 1) return 6;
        else if (nJetsPassed < 4 && nJetsPassed >= 2 && nFatJetsPassed == 0) return 9;
        else if (nJetsPassed < 2 && nFatJetsPassed == 3) return 1;
        else if (nJetsPassed < 2 && nFatJetsPassed == 2) return 5;
        else if (nJetsPassed < 2 && nFatJetsPassed == 1) return 8;
        else if (nJetsPassed < 2 && nFatJetsPassed == 0) return 0;
    }
    return -1;
}
'''
ROOT.gInterpreter.Declare(cat)

category_colors = {
    "0bh0h": "blue",
    "3bh0h": "orange",
    "2bh1h": "green",
    "1bh2h": "red",
    "0bh3h": "purple",
    "2bh0h": "brown",
    "1bh1h": "pink",
    "0bh2h": "gray",
    "1bh0h": "cyan",
    "0bh1h": "magenta"
}
# 定义工作点
wp_jet_range = np.arange(0.40, 0.97, 0.02)
# wp_jet_range = np.arange(0.40, 0.97, 0.3)
# wp_jet_range = np.array([0.40])
# wp_fatjet_range = np.arange(0.641, 0.9735, 0.05)
wp_fatjet_range = np.array([0.9])

# 类别标签
categories = ["0bh0h", "3bh0h", "2bh1h", "1bh2h", "0bh3h", "2bh0h", "1bh1h", "0bh2h", "1bh0h", "0bh1h"]
# categories = ["3bh0h", "2bh1h", "1bh2h", "0bh3h"]
category_numbers = list(range(10))  # 分类标签从 0 到 9

# 用于存储结果的字典
wp_results = []

# 遍历所有工作点组合
for wp_jet in wp_jet_range:
    for wp_fatjet in wp_fatjet_range:
        # 加载ROOT文件
        path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/categorization/2018"
        file = ROOT.TFile(f"{path}/GluGluToHHHTo6B_SM.root")
        df = ROOT.RDataFrame("Events", file)

        # 设置 PassBtag 条件
        for i in range(1, 11):
            pnet_b_plus_c = f"jet{i}PNetBPlusC"
            pnet_b_vs_c = f"jet{i}PNetBVsC"
            df = df.Define(f"jet{i}PassBtag", f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > {wp_jet}) ? 1 : 0")

        for i in range(1, 5):
            pnet_xbb = f"fatJet{i}PNetXbb"
            df = df.Define(f"fatJet{i}PassBtag", f"({pnet_xbb} > {wp_fatjet}) ? 1 : 0")


        
        # 计算通过条件的 jet 和 fatJet 数量
        df = df.Define('nJetsPassed', 'jet1PassBtag + jet2PassBtag + jet3PassBtag + jet4PassBtag + jet5PassBtag + jet6PassBtag + jet7PassBtag + jet8PassBtag + jet9PassBtag + jet10PassBtag')
        df = df.Define('nFatJetsPassed', 'fatJet1PassBtag + fatJet2PassBtag + fatJet3PassBtag + fatJet4PassBtag')

        # 定义分类函数
        
        df = df.Define('category_reco', 'cat_reco_function(nFatJetsPassed, nJetsPassed, hhh_mass2)')
        df = df.Filter('category_reco != -1')  # 排除无效数据

        # 计算比例
        ratios = {}
        for cat_num, cat_name in zip(category_numbers, categories):
            total_count_true = df.Filter(f"categorisation == {cat_num}").Count().GetValue()  # True category count
            total_count_reco = df.Filter(f"category_reco == {cat_num} && categorisation == {cat_num}").Count().GetValue()  # Reco category count
            ratio = (total_count_reco / total_count_true) * 100 if total_count_true > 0 else 0
            ratios[cat_name] = ratio

        # 保存每个组合的比例
        wp_results.append((wp_jet, wp_fatjet, ratios))

# 输出最佳的工作点组合和比例
# for wp_jet, wp_fatjet, ratios in wp_results:
#     print(f"Jet WP: {wp_jet}, FatJet WP: {wp_fatjet}")
#     for category, ratio in ratios.items():
#         print(f"{category}: {ratio:.2f}%")
#     print()

# 画出每个类别的比例曲线
fig, ax = plt.subplots(figsize=(10, 6))
for wp_jet, wp_fatjet, ratios in wp_results:
    for category in categories:
        ax.plot([wp_jet] * len(ratios), [ratios[category] for _ in ratios], label=f"{category}",color=category_colors[category])

plt.xlabel("Jet WP")
plt.ylabel("Ratio (%)")
plt.title("Ratio of Categories for Different WP Combinations")
# plt.legend(loc="best")
plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize='small', markerscale=0.8)

plt.savefig("optimize_jet.pdf")
