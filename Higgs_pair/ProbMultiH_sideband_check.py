import ROOT


binning_dict = {
    "3bh0h": [0.952, 0.9565, 0.961, 0.9655, 0.97, 0.9745, 0.979, 0.9835, 0.988, 0.9925, 1.0],
    "2bh1h": [0.9825, 0.984, 0.9855, 0.987, 0.9885, 0.99, 0.9915, 0.993, 0.9945, 0.996, 1.0],
    "1bh2h": [0.981, 0.9825, 0.984, 0.9855, 0.987, 0.9885, 0.99, 0.9915, 0.993, 0.9945, 1.0],
    "0bh3h": [0.9825, 0.984, 0.9855, 0.987, 0.9885, 0.99, 0.9915, 0.993, 0.9945, 0.996, 1.0],
    # 添加其他分类和分 bin 配置
}

# 打开 ROOT 文件
path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/2018"
cat_list = ["3bh0h","2bh1h","1bh2h","0bh3h"]
sample_list = ["data_obs","QCD_datadriven","GluGluToHHHTo6B_SM","GluGluToHHTo4B_cHHH1"]
for cat in cat_list:
    bins = binning_dict[cat]
    for sample in sample_list:
        file = ROOT.TFile.Open("%s/ProbHHH6b_%s_inclusive_CR/%s_new.root"(path,cat,sample))
        tree = file.Get("Events")  # 替换为你的 TTree 名称
        # 变量和 cuts
        variable_A = "A"
        variable_B = "B"
        cut_condition = "your_cut_expression"  # 替换为实际的切割条件

        # 绘制每个分类的图表
        canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)
        
            
        # 创建直方图
        hist_name = f"hist_{category}"
        hist = ROOT.TH1F(hist_name, f"Histogram for {category}", len(bins) - 1, array('d', bins))
        
        # 应用切割并填充直方图
        draw_command = f"{variable_B}>>{hist_name}"
        full_cut = f"{cut_condition} && category == \"{category}\""  # 替换为实际分类逻辑
        tree.Draw(draw_command, full_cut, "goff")
        
        # 绘制直方图
        hist.Draw("HIST")
        canvas.SaveAs(f"{category}.png")  # 保存图片

        file.Close()
