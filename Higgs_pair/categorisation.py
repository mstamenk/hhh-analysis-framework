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
    df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.96) ? 1 : 0")
    # df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.70) ? 1 : 0")
    # df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.40) ? 1 : 0")

# 对 fatJet1 创建 PassBtag branch
for i in range(1, 5):  # 遍历 fatJet1 到 fatJet4
    # 定义变量名
    pnet_xbb = f"fatJet{i}PNetXbb"
    pass_btag_branch = f"fatJet{i}PassBtag"

    # 添加新的 branch，判断是否满足 Btag 条件
    df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.9734) ? 1 : 0")
    # df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.90) ? 1 : 0")
    # df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.641) ? 1 : 0")


# 计算通过条件的 jet 和 fatJet 数量
df = df.Define('nJetsPassed', 'jet1PassBtag + jet2PassBtag + jet3PassBtag + jet4PassBtag + jet5PassBtag + jet6PassBtag + jet7PassBtag + jet8PassBtag + jet9PassBtag + jet10PassBtag')
df = df.Define('nFatJetsPassed', 'fatJet1PassBtag + fatJet2PassBtag + fatJet3PassBtag + fatJet4PassBtag')


# # 判断最终的分类
# df = df.Define('category_reco', """
#     int result = 0;
#     if (nFatJetsPassed == 3) {
#         if (nJetsPassed <2){
#             result = 1;
#         }else if (nJetsPassed >= 2 && nJetsPassed < 6){
#             if(hhh_mass2 <= 900){
#                 result = 2;
#             }else if (hhh_mass2 > 900){
#                 result = 1;
#             }
#         }else if (nJetsPassed == 6){
#             if(hhh_mass2 <= 900){
#                 result = 3;
#             }else if (hhh_mass2 > 900){
#                 result = 1;
#             }
#         }    
#     }else if(nFatJetsPassed == 2){
#         if (nJetsPassed >=2 && nJetsPassed < 6){
#             result = 2
#         }else if (nJetsPassed == 6){
#             if(hhh_mass2 <= 700){
#                 result = 3;
#             }else if (hhh_mass2 > 700){
#                 result = 2;
#             }
#         }
#     }else if(nFatJetsPassed == 1){
#         if (nJetsPassed >=4 && nJetsPassed < 6){
#             result = 2
#         }else if (nJetsPassed == 6){
#             if(hhh_mass2 <= 700){
#                 result = 3;
#             }else if (hhh_mass2 > 700){
#                 result = 2;
#             }
#         }
#     }else if(nFatJetsPassed == 0){
#         if (nJetsPassed == 6){
#             result = 3;
#         }
#     }


#     result
# """)

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
count_categorisation_4 = df.Filter("categorisation == 4").Count().GetValue()

# 计算总和
total_count = count_categorisation_1 + count_categorisation_2 + count_categorisation_3 + count_categorisation_4

# 打印结果
print(f"Number of events for categorisation == 1: {count_categorisation_1}")
print(f"Number of events for categorisation == 2: {count_categorisation_2}")
print(f"Number of events for categorisation == 3: {count_categorisation_3}")
print(f"Number of events for categorisation == 4: {count_categorisation_4}")
print(f"Total number of events for categorisation 1, 2, 3, 4: {total_count}")


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


count_true_new_1 = df.Filter("category_new == 1").Count().GetValue()
count_true_new_2 = df.Filter("category_new == 2").Count().GetValue()
count_true_new_3 = df.Filter("category_new == 3").Count().GetValue()

# 计算总和
total_count_true_new = count_true_new_1 + count_true_new_2 + count_true_new_3

# 打印结果
print(f"Number of events for reco == 1: {count_true_new_1}")
print(f"Number of events for reco == 2: {count_true_new_2}")
print(f"Number of events for reco == 3: {count_true_new_3}")
print(f"Total number of events for reco 1, 2, 3: {total_count_true_new}")

# 创建新的二维分布
df_2d = df.Histo2D(('category_reco', 'Reco Category vs true category', 3, 0.5, 3.5, 3, 0.5, 3.5), 'category_reco', 'category_new')

# 显示图形
canvas = ROOT.TCanvas("canvas", "2D Distribution", 800, 600)
ROOT.gStyle.SetOptStat(0)
df_2d.Draw("COLZ")
df_2d.GetXaxis().SetTitle("Reco Category")  # X轴标题
df_2d.GetYaxis().SetTitle("True Category") 
total_entries = df_2d.GetEntries()
print("total_entries:", total_entries)

texts = []
# 获取每个bin的计数并显示比例
# 获取每个bin的计数并显示比例
for i in range(1, df_2d.GetNbinsX() + 1):
    for j in range(1, df_2d.GetNbinsY() + 1):
        bin_content = df_2d.GetBinContent(i, j)
        if bin_content > 0:
            # 计算比例
            percentage = (bin_content / total_count_reco) * 100
            # 获取bin的坐标
            x = df_2d.GetXaxis().GetBinCenter(i)
            y = df_2d.GetYaxis().GetBinCenter(j)
            # 在图上添加文本显示比例
            text = ROOT.TText(x, y, f"{percentage:.2f}%")
            text.SetTextAlign(22)
            text.SetTextSize(0.03)
            texts.append(text)
            # text.Draw()  # 确保文本绘制在正确的层级
        else:
            # 如果计数为零，则显示0%
            x = df_2d.GetXaxis().GetBinCenter(i)
            y = df_2d.GetYaxis().GetBinCenter(j)
            text = ROOT.TText(x, y, "0%")
            text.SetTextAlign(22)
            text.SetTextSize(0.03)
            texts.append(text)
            # text.Draw()

# 保存图形
for text in texts:
    text.Draw()
canvas.Update()
canvas.SaveAs("output_2d_distribution.pdf")
