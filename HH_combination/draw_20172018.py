import ROOT

# 打开 ROOT 文件
path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbbb"
cat_list = ["new_hist"]
for cat in cat_list:

input_file = ROOT.TFile.Open("your_input_file.root", "READ")

# 获取两个直方图
hist1 = input_file.Get("hist1_name")  # 替换为实际的直方图名
hist2 = input_file.Get("hist2_name")  # 替换为实际的直方图名

if not hist1 or not hist2:
    print("Failed to load histograms.")
    exit(1)

# 创建一个画布
canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)

# 绘制第一个直方图
hist1.SetLineColor(ROOT.kRed)  # 设置颜色
hist1.Draw("HIST")  # 绘制第一个直方图

# 在第一个直方图上绘制第二个直方图
hist2.SetLineColor(ROOT.kBlue)  # 设置第二个直方图的颜色
hist2.Draw("HIST SAME")  # 使用 SAME 参数将第二个直方图绘制到同一个画布上

# 添加图例
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)  # 图例位置
legend.AddEntry(hist1, "Histogram 1", "l")  # "l"表示线条
legend.AddEntry(hist2, "Histogram 2", "l")
legend.Draw()

# 显示画布
canvas.Update()
canvas.Draw()

# 保存为图像文件
canvas.SaveAs("combined_histograms.png")

input_file.Close()
