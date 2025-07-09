import ROOT
import os

# 打开 ROOT 文件
ROOT.gROOT.SetBatch(True)

cat = '''
int cat_reco_function(int nFatJetsPassed, int nJetsPassed, float hhh_mass) {
    
    if (hhh_mass > 750) {
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
    else if (hhh_mass <= 750) {
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
# working_points = ['loose', 'medium', 'tight']
working_points = ['loose','medium', 'tight']
# wp_jet = {
#     'loose': 0.40,
#     'medium': 0.70,
#     'tight': 0.96,
#     'try' : 0.80

# }
#WP for PNetB
wp_jet = {
    'loose': 6, #>6 =7
    'medium':7,
    'tight': 8,
    'try' : 0.80

}
wp_fatjet = {
    'loose': 0,
    'medium': 0,
    'tight': 1,
    'try' : 0.90

}
for wp in working_points:

    years = ["2016", "2016APV", "2017", "2018"]
    base_path = "/eos/cms/store/group/phys_higgs/cmshhh/v34-fix-ak4-ak8/mva-inputs-{}-categorisation-spanet-boosted-classification/inclusive-weights"
    file_name = "GluGluToHHHTo6B_SM.root"
    

    # 读取所有年份的文件
    files = []
    for year in years:
        path = base_path.format(year)
        file_path = os.path.join(path, file_name)
        files.append(file_path)


    # 创建 RDataFrame

    # 创建 RDataFrame，支持多个文件
    df = ROOT.RDataFrame("Events", files)


    for i in range(1, 11):  # 遍历 jet1 到 jet10
        # 定义变量名
        pnet_b_cat = f"jet{i}PNetTagCat"
        pass_btag_branch = f"jet{i}PassBtag"
        cut_jet = wp_jet[wp]

        # # 添加新的 branch，判断是否满足 Btag 条件
        df = df.Define(pass_btag_branch, f"({pnet_b_cat} > {cut_jet}) ? 1 : 0")


    for i in range(1, 4):  # 遍历 fatJet1 到 fatJet3
        pnet_xbb_cat = f"fatJet{i}PNetXbbTagCat"
        pass_btag_branch = f"fatJet{i}PassBtag"
        cut_fatjet = wp_fatjet[wp]
        df = df.Define(pass_btag_branch, f"({pnet_xbb_cat} > {cut_fatjet}) ? 1 : 0")

    # 计算通过条件的 jet 和 fatJet 数量
    df = df.Define('nJetsPassed', 'jet1PassBtag + jet2PassBtag + jet3PassBtag + jet4PassBtag + jet5PassBtag + jet6PassBtag + jet7PassBtag + jet8PassBtag + jet9PassBtag + jet10PassBtag')
    # df = df.Define('nFatJetsPassed', 'fatJet1PassBtag + fatJet2PassBtag + fatJet3PassBtag + fatJet4PassBtag')
    df = df.Define('nFatJetsPassed', 'fatJet1PassBtag + fatJet2PassBtag + fatJet3PassBtag ')

    # 根据给定的函数为数据定义类别
    df = df.Define('category_reco', 'cat_reco_function(nFatJetsPassed, nJetsPassed, hhh_mass)')

    # 过滤掉无效的分类
    df = df.Filter('category_reco != -1')
    
    # 计算每个 X 类别（如 0bh0h, 3bh0h）对应的总事例数
    total_count_reco_x = {}
    for i in range(0, 10):  # X轴
        total_count_reco_x[i] = df.Filter(f"categorisation == {i}").Count().GetValue()

    # 创建 2D 直方图
    df_2d = df.Histo2D(('category_reco', 'Reco Category vs true category', 10, -0.5, 9.5, 10, -0.5, 9.5), 'categorisation','category_reco')

    # 修改 Z 值：Z = 事例数 / 对应 X 类别的总事例数
    for i in range(0, 10):  # X 轴的每个 bin
        for j in range(1, df_2d.GetNbinsY() + 1):  # Y 轴的每个 bin
            bin_content = df_2d.GetBinContent(i + 1, j)
            if total_count_reco_x[i] > 0:
                ratio = bin_content / total_count_reco_x[i]  # 计算比值
                df_2d.SetBinContent(i + 1, j, ratio)  # 更新该 bin 的 Z 值为比值
            else:
                df_2d.SetBinContent(i + 1, j, 0)  # 如果该类别的总事例数为 0，Z 值设为 0

    # 设置 X 轴和 Y 轴标签
    x_labels = ["0bh0h", "3bh0h", "2bh1h", "1bh2h", "0bh3h", "2bh0h", "1bh1h", "0bh2h", "1bh0h", "0bh1h"]
    y_labels = ["Prob0bh0h", "Prob3bh0h", "Prob2bh1h", "Prob1bh2h", "Prob0bh3h", "Prob2bh0h", "Prob1bh1h", "Prob0bh2h", "Prob1bh0h", "Prob0bh1h"]
    
    for i in range(1, 11):  # 设置 X 轴和 Y 轴标签
        df_2d.GetXaxis().SetBinLabel(i, x_labels[i-1])
        df_2d.GetYaxis().SetBinLabel(i, y_labels[i-1])

    # 绘制直方图
    canvas = ROOT.TCanvas("canvas", "2D Distribution", 800, 600)
    ROOT.gStyle.SetOptStat(0)
    df_2d.Draw("COLZ")
    df_2d.GetXaxis().SetTitle("true Category")  # X 轴标题
    df_2d.GetYaxis().SetTitle("reco Category")

    # 添加文本标注，显示每个 bin 的比值（百分比）
    texts = []
    for i in range(0, 10):  # 遍历所有 X 轴的值
        for j in range(1, df_2d.GetNbinsY() + 1):  # 遍历所有 Y 轴的值
            bin_content = df_2d.GetBinContent(i + 1, j)
            if bin_content > 0:
                percentage = bin_content * 100  # Z 值是比值，乘以 100 显示为百分比
                x = df_2d.GetXaxis().GetBinCenter(i + 1)  # 获取 X 轴坐标
                y = df_2d.GetYaxis().GetBinCenter(j)  # 获取 Y 轴坐标
                text = ROOT.TText(x, y, f"{percentage:.2f}%")
                text.SetTextAlign(22)
                text.SetTextSize(0.03)
                texts.append(text)
            else:
                x = df_2d.GetXaxis().GetBinCenter(i + 1)
                y = df_2d.GetYaxis().GetBinCenter(j)
                text = ROOT.TText(x, y, "0%")
                text.SetTextAlign(22)
                text.SetTextSize(0.03)
                texts.append(text)

    # 绘制所有文本标注
    for text in texts:
        text.Draw()

    canvas.Update()
    canvas.SaveAs(f"output_2d_{wp}_color_right_cat_run2.pdf")
