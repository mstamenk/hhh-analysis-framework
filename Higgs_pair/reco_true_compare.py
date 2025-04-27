import ROOT

# 打开 ROOT 文件
path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/categorization/2018"
file = ROOT.TFile("%s/GluGluToHHHTo6B_SM.root" % path)

# 创建 RDataFrame
df = ROOT.RDataFrame("Events", file)
# 遍历 jet1 到 jet10，创建 jetXPassBtag branch
for i in range(1, 11):  # 遍历 jet1 到 jet10
    # 定义变量名
    pnet_b_plus_c = f"jet{i}PNetBPlusC"
    pnet_b_vs_c = f"jet{i}PNetBVsC"
    pass_btag_branch = f"jet{i}PassBtag"

    # 添加新的 branch，判断是否满足 Btag 条件
    # df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.96) ? 1 : 0")
    # df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.70) ? 1 : 0")
    df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.40) ? 1 : 0")

# 对 fatJet1 创建 PassBtag branch
for i in range(1, 5):  # 遍历 fatJet1 到 fatJet4
    # 定义变量名
    pnet_xbb = f"fatJet{i}PNetXbb"
    pass_btag_branch = f"fatJet{i}PassBtag"

    # 添加新的 branch，判断是否满足 Btag 条件
    # df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.9734) ? 1 : 0")
    # df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.90) ? 1 : 0")
    df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.641) ? 1 : 0")


# 计算通过条件的 jet 和 fatJet 数量
df = df.Define('nJetsPassed', 'jet1PassBtag + jet2PassBtag + jet3PassBtag + jet4PassBtag + jet5PassBtag + jet6PassBtag + jet7PassBtag + jet8PassBtag + jet9PassBtag + jet10PassBtag')
df = df.Define('nFatJetsPassed', 'fatJet1PassBtag + fatJet2PassBtag + fatJet3PassBtag + fatJet4PassBtag')


cat = '''
int cat_reco_function(int nFatJetsPassed, int nJetsPassed, float hhh_mass2) {
    
    if (nFatJetsPassed == 3) {
        if (nJetsPassed < 2) return 1;
        else if (nJetsPassed >= 2 && nJetsPassed < 6) {
            return (hhh_mass2 <= 900) ? 2 : 1;
        } else if (nJetsPassed == 6) {
            return (hhh_mass2 <= 900) ? 3 : 1;
        }
    } else if (nFatJetsPassed == 2) {
        if (nJetsPassed >= 2 && nJetsPassed < 6) return 2;
        else if (nJetsPassed == 6) {
            return (hhh_mass2 <= 700) ? 3 : 2;
        }
    } else if (nFatJetsPassed == 1) {
        if (nJetsPassed >= 4 && nJetsPassed < 6) return 2;
        else if (nJetsPassed == 6) {
            return (hhh_mass2 <= 700) ? 3 : 2;
        }
    } else if (nFatJetsPassed == 0 && nJetsPassed == 6) {
        return 3;
    }
    return 0; // 默认分类
}
'''
ROOT.gInterpreter.Declare(cat)
df = df.Define('category_reco', 'cat_reco_function(nFatJetsPassed, nJetsPassed, hhh_mass2)')

df = df.Define('category_new', """
    (categorisation == 2 || categorisation == 3) ? 2 : 
    (categorisation == 4 ? 3 : categorisation)
""")
count_categorisation_1 = df.Filter("categorisation == 1").Count().GetValue()
count_categorisation_2 = df.Filter("categorisation == 2").Count().GetValue()
count_categorisation_3 = df.Filter("categorisation == 3").Count().GetValue()
count_categorisation_3 = df.Filter("categorisation == 4").Count().GetValue()

# 计算总和
total_count = count_categorisation_1 + count_categorisation_2 + count_categorisation_3

# 打印结果
print(f"Number of events for categorisation == 1: {count_categorisation_1}")
print(f"Number of events for categorisation == 2: {count_categorisation_2}")
print(f"Number of events for categorisation == 3: {count_categorisation_3}")
print(f"Total number of events for categorisation 1, 2, 3: {total_count}")


count_reco_1 = df.Filter("category_reco == 1").Count().GetValue()
count_reco_2 = df.Filter("category_reco == 2").Count().GetValue()
count_reco_3 = df.Filter("category_reco == 3").Count().GetValue()

# 计算总和
total_count_reco = count_reco_1 + count_reco_2 + count_reco_3

# 打印结果
print(f"Number of events for reco == 1: {count_reco_1}")
print(f"Number of events for reco == 2: {count_reco_2}")
print(f"Number of events for reco == 3: {count_reco_3}")
print(f"Total number of events for reco 1, 2, 3: {total_count_reco}")



# 定义新的分类变量，将其他值归为 "other"（值为 5）
df = df.Define("categorisation_class", """
    (categorisation == 1 || categorisation == 2 || categorisation == 3 || categorisation == 4) ? categorisation : 5
""")


# 定义 category_reco 的值和对应的标签
category_reco_values = [1, 2, 3]
category_reco_labels = ["3bh0h_reco", "semi-boosted_reco", "0bh3h_reco"]

# 定义 categorisation 的标签
categorisation_labels = {
    1: "3bh0h",
    2: "2bh1h",
    3: "1bh2h",
    4: "0bh3h",
    5: "other"
}

# 循环绘制直方图
for reco_value, reco_label in zip(category_reco_values, category_reco_labels):
    # 筛选当前 category_reco 的事件
    df_filtered = df.Filter(f"category_reco == {reco_value}")

    # 创建一维直方图
    hist = df_filtered.Histo1D(
        (f'categorisation_distribution_{reco_label}', f'Categorisation Distribution ({reco_label});Categorisation;Entries', 5, 0.5, 5.5),
        "categorisation_class"
    )

    # 设置 X 轴标签
    x_axis = hist.GetXaxis()
    for bin_index, label in categorisation_labels.items():
        x_axis.SetBinLabel(bin_index, label)

    # 创建画布
    canvas = ROOT.TCanvas(f"canvas_{reco_label}", f"Categorisation Distribution ({reco_label})", 800, 600)

    # 绘制直方图
    hist.SetStats(0)  # 去掉统计框
    hist.SetLineWidth(2)
    hist.SetLineColor(ROOT.kBlue + reco_value)  # 颜色区分
    hist.Draw("HIST")
    total_entries = hist.Integral()

    text_list = []  # 存储 TText 对象
    for bin_index in range(1, hist.GetNbinsX() + 1):
        bin_content = hist.GetBinContent(bin_index)
        if bin_content > 0:  # 避免空 bin
            percentage = (bin_content / total_entries) * 100
            bin_center = hist.GetXaxis().GetBinCenter(bin_index)
            text = ROOT.TText(bin_center, bin_content + 0.05 * hist.GetMaximum(), f"{percentage:.2f}%")
            text.SetTextAlign(22)  # 居中显示
            text.SetTextSize(0.03)
            text_list.append(text)

    # 绘制所有文本
    for text in text_list:
        text.Draw()
    # 保存图形
    canvas.SaveAs(f"categorisation_distribution_{reco_label}.pdf")

print("All distributions have been saved!")
