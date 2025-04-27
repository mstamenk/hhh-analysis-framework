
import ROOT

# 打开 ROOT 文件
ROOT.gROOT.SetBatch(True)
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
working_points = ['loose', 'medium', 'tight']
# working_points = ['tight']
wp_jet = {
    'loose': 0.40,
    'medium': 0.70,
    'tight': 0.96
}
wp_fatjet = {
    'loose': 0.641,
    'medium': 0.90,
    'tight': 0.9734
}
for wp in working_points:


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
        cut_jet = wp_jet[wp]

        # 添加新的 branch，判断是否满足 Btag 条件
        df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > {cut_jet}) ? 1 : 0")
        # df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.70) ? 1 : 0")
        # df = df.Define(pass_btag_branch, f"({pnet_b_plus_c} > 0.5 && {pnet_b_vs_c} > 0.40) ? 1 : 0")

    # 对 fatJet1 创建 PassBtag branch
    for i in range(1, 5):  # 遍历 fatJet1 到 fatJet4
        # 定义变量名
        pnet_xbb = f"fatJet{i}PNetXbb"
        pass_btag_branch = f"fatJet{i}PassBtag"
        cut_fatjet = wp_fatjet[wp]

        # 添加新的 branch，判断是否满足 Btag 条件
        df = df.Define(pass_btag_branch, f"({pnet_xbb} > {cut_fatjet}) ? 1 : 0")
        # df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.90) ? 1 : 0")
        # df = df.Define(pass_btag_branch, f"({pnet_xbb} > 0.641) ? 1 : 0")


    # 计算通过条件的 jet 和 fatJet 数量
    df = df.Define('nJetsPassed', 'jet1PassBtag + jet2PassBtag + jet3PassBtag + jet4PassBtag + jet5PassBtag + jet6PassBtag + jet7PassBtag + jet8PassBtag + jet9PassBtag + jet10PassBtag')
    df = df.Define('nFatJetsPassed', 'fatJet1PassBtag + fatJet2PassBtag + fatJet3PassBtag + fatJet4PassBtag')


    # 3bh0h 1
    # 2bh1h 2
    # 1bh2h 3
    # 0bh3h 4

    # 2Higgs 
    # 2bh0h 5
    # 1bh1h 6 
    # 0bh2h 7

    # 1Higgs 
    # 1bh0h 8
    # 0bh1h 9

    # 0Higgs
    # 0bh0h 0
    # cat = '''
    # int cat_reco_function(int nFatJetsPassed, int nJetsPassed, float hhh_mass2) {
        
    #     if (hhh_mass2 > 700) {
    #         if (nFatJetsPassed == 3) return 1;
    #         else if (nFatJetsPassed == 2 && nJetsPassed == 2) return 2;
    #         else if (nFatJetsPassed == 2 && nJetsPassed == 0) return 5;
    #         else if (nFatJetsPassed == 1 && nJetsPassed == 4) return 3;
    #         else if (nFatJetsPassed == 1 && nJetsPassed == 2) return 6;
    #         else if (nFatJetsPassed == 1 && nJetsPassed == 0) return 8;
    #         else if (nFatJetsPassed == 0 && nJetsPassed == 6) return 4;
    #         else if (nFatJetsPassed == 0 && nJetsPassed == 4) return 7;
    #         else if (nFatJetsPassed == 0 && nJetsPassed == 2) return 9;
    #         else if (nFatJetsPassed == 0 && nJetsPassed == 0) return 0;
    #         }
    #     else if (hhh_mass2 <= 700) {
    #         if (nJetsPassed == 6) return 4;
    #         else if (nJetsPassed == 4 && nFatJetsPassed == 1) return 3;
    #         else if (nJetsPassed == 4 && nFatJetsPassed == 0) return 5;
    #         else if (nJetsPassed == 2 && nFatJetsPassed == 2) return 2;
    #         else if (nJetsPassed == 2 && nFatJetsPassed == 1) return 6;
    #         else if (nJetsPassed == 2 && nFatJetsPassed == 0) return 8;
    #         else if (nJetsPassed == 0 && nFatJetsPassed == 3) return 1;
    #         else if (nJetsPassed == 0 && nFatJetsPassed == 2) return 5;
    #         else if (nJetsPassed == 0 && nFatJetsPassed == 1) return 8;
    #         else if (nJetsPassed == 0 && nFatJetsPassed == 0) return 0;

    #         }
    #     return 0;
    # }
    # '''

    

    # cat = '''
    # int cat_reco_function(int nFatJetsPassed, int nJetsPassed, float hhh_mass2) {
        
    #     if (hhh_mass2 > 700) {
    #         if (nFatJetsPassed == 3) return 1;
    #         else if (nFatJetsPassed == 2 && nJetsPassed == 2) return 2;
    #         else if (nFatJetsPassed == 1 && nJetsPassed == 4) return 3;
    #         else if (nFatJetsPassed == 0 && nJetsPassed == 6) return 4;
    #         }
    #     else if (hhh_mass2 <= 700) {
    #         if (nJetsPassed == 6) return 4;
    #         else if (nJetsPassed == 4 && nFatJetsPassed == 1) return 3;
    #         else if (nJetsPassed == 2 && nFatJetsPassed == 2) return 2;
    #         else if (nJetsPassed == 0 && nFatJetsPassed == 3) return 1;
    #         }
    #     return 0;
    # }
    # '''
    
    df = df.Define('category_reco', 'cat_reco_function(nFatJetsPassed, nJetsPassed, hhh_mass2)')

    # df = df.Define('category_new', """
    #     (categorisation == 2 || categorisation == 3) ? 2 : 
    #     (categorisation == 4 ? 3 : categorisation)
    # """)
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
    count_reco_4 = df.Filter("category_reco == 4").Count().GetValue()

    # 计算总和
    total_count_reco = count_reco_1 + count_reco_2 + count_reco_3 + count_reco_4

    # 打印结果
    print(f"Number of events for reco == 1: {count_reco_1}")
    print(f"Number of events for reco == 2: {count_reco_2}")
    print(f"Number of events for reco == 3: {count_reco_3}")
    print(f"Number of events for reco == 4: {count_reco_4}")
    print(f"Total number of events for reco 1, 2, 3, 4: {total_count_reco}")



    # 创建新的二维分布
    df = df.Filter('category_reco != -1')
    df_2d = df.Histo2D(('category_reco', 'Reco Category vs true category', 10, -0.5, 9.5, 10, -0.5, 9.5), 'category_reco','categorisation')

    # 设置自定义的X轴和Y轴标签
    x_labels = ["Prob0bh0h", "Prob3bh0h", "Prob2bh1h", "Prob1bh2h", "Prob0bh3h", "Prob2bh0h", "Prob1bh1h", "Prob0bh2h", "Prob1bh0h", "Prob0bh1h"]
    y_labels = ["0bh0h", "3bh0h", "2bh1h", "1bh2h", "0bh3h", "2bh0h", "1bh1h", "0bh2h", "1bh0h", "0bh1h"]

    # 设置每个bin的标签
    for i in range(1, 11):  # X轴标签
        df_2d.GetXaxis().SetBinLabel(i, x_labels[i-1])

    for i in range(1, 11):  # Y轴标签
        df_2d.GetYaxis().SetBinLabel(i, y_labels[i-1])




    # 显示图形
    canvas = ROOT.TCanvas("canvas", "2D Distribution", 800, 600)
    ROOT.gStyle.SetOptStat(0)
    df_2d.Draw("COLZ")
    df_2d.GetXaxis().SetTitle("reco Category")  # X轴标题
    df_2d.GetYaxis().SetTitle("true Category") 
    total_entries = df_2d.GetEntries()
    print("total_entries:", total_entries)

    texts = []
    for i in range(0, 10):  # 遍历 X 轴的所有值
        # 计算当前 X 轴值为 i 时的 total_count_reco
        total_count_reco_x = df.Filter(f"category_reco == {i}").Count().GetValue()
        if total_count_reco_x == 0:
            continue

        # 遍历 Y 轴的所有值
        for j in range(1, df_2d.GetNbinsY() + 1):
            bin_content = df_2d.GetBinContent(i + 1, j)  # 获取当前 (i, j) bin 的内容
            if bin_content > 0:
                # 计算比例
                percentage = (bin_content / total_count_reco_x) * 100
                # 获取bin的坐标
                x = df_2d.GetXaxis().GetBinCenter(i + 1)  # X轴坐标
                y = df_2d.GetYaxis().GetBinCenter(j)  # Y轴坐标
                # 在图上添加文本显示比例
                text = ROOT.TText(x, y, f"{percentage:.2f}%")
                text.SetTextAlign(22)
                text.SetTextSize(0.03)
                texts.append(text)
            else:
                # 如果计数为零，则显示0%
                x = df_2d.GetXaxis().GetBinCenter(i + 1)
                y = df_2d.GetYaxis().GetBinCenter(j)
                text = ROOT.TText(x, y, "0%")
                text.SetTextAlign(22)
                text.SetTextSize(0.03)
                texts.append(text)

    # 在图形上绘制所有文本
    for text in texts:
        text.Draw()

    canvas.Update()
    canvas.SaveAs("output_2d_%s_reverse.pdf"%wp)


