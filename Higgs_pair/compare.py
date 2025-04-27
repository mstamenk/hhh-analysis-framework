import ROOT
path_x = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/cat_new/2018"
path_M = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33_new/2018"
ROOT.gROOT.SetBatch(True)
cat_list = ['3bh0h','2bh1h','1bh2h','0bh3h','2bh0h','1bh1h','0bh2h','1Higgs','0bh0h']
for cat in cat_list:

    # 定义输入文件路径和对象名称
    file1_path = "%s/ProbHHH6b_%s_inclusive_CR/histograms/histograms_ProbMultiH.root"%(path_x,cat)
    file2_path = "%s/ProbHHH6b_%s_inclusive_CR/histograms/histograms_ProbMultiH.root"%(path_M,cat)

    # 打开 ROOT 文件
    file1 = ROOT.TFile.Open(file1_path, "READ")
    file2 = ROOT.TFile.Open(file2_path, "READ")

    # 从文件中获取 TH1F 对象
    hist1 = file1.Get("GluGluToHHHTo6B_SM")
    hist2 = file2.Get("GluGluToHHHTo6B_SM")

    # 检查是否成功读取直方图
    if not hist1 or not hist2:
        print("cannot find hist")
        exit(1)

    # 计算两个分布的 yield（所有 bin 的内容之和）
    yield1 = hist1.Integral()
    yield2 = hist2.Integral()

    # 输出 yield 值
    print(f"xinyue: {cat}  yield: {yield1}")
    print(f"Marko {cat}  yield: {yield2}")

    max_value = max(hist1.GetMaximum(),hist2.GetMaximum())
    y_max = 1.2* max_value

    # 设置绘图样式
    ROOT.gStyle.SetOptStat(0)

    # 创建画布并绘制两个直方图
    canvas = ROOT.TCanvas("canvas", "Histogram Comparison", 800, 600)

    # 设置直方图样式
    hist1.SetLineColor(ROOT.kRed)
    hist1.SetLineWidth(2)
    hist1.SetTitle(f"Comparison of cut-base and mva")
    hist1.SetMaximum(y_max)

    hist2.SetLineColor(ROOT.kBlue)
    hist2.SetLineWidth(2)

    # 绘制直方图
    hist1.Draw("HIST")
    hist2.Draw("HIST SAME")

    # 添加图例
    legend = ROOT.TLegend(0.85, 0.85, 1.0, 1.0)
    legend.AddEntry(hist1, "cut_based", "l")
    legend.AddEntry(hist2, " mva", "l")
    legend.Draw()

    # 保存为 PDF 文件
    output_pdf = "com_%s.pdf"%(cat)
    canvas.SaveAs(output_pdf)

    print(f"already saved {output_pdf}")

    # 关闭 ROOT 文件
    file1.Close()
    file2.Close()
