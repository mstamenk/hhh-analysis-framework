import ROOT
import os
import gc

# 不进入交互式界面
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# ─── 1. 定义四类文件路径（请根据你自己的存放位置修改） ───
# 举例：假设所有文件都放在同一个 base_dir 目录下
year_list = ["2016", "2016APV", "2017", "2018"]  # 可根据需要修改年份列表
base_dir = "/eos/cms/store/group/phys_higgs/cmshhh/v34-fix-ak4-ak8/mva-inputs-{year}-categorisation-spanet-boosted-classification/inclusive-weights"
df_dict_6b = {}
df_dict_4b = {}
df_dict_qcd = {}
var_settings = {
    "h1_t3_mass": {"xmin": 0, "xmax": 500, "bin_width": 20, "x_title": "m_{H1} (GeV)"},
    "h2_t3_mass": {"xmin": 0, "xmax": 500, "bin_width": 20, "x_title": "m_{H2} (GeV)"},
    "h3_t3_mass": {"xmin": 0, "xmax": 500, "bin_width": 20, "x_title": "m_{H3} (GeV)"},
    
    "hhh_mass": {"xmin": 0, "xmax": 2000, "bin_width": 20, "x_title": "m_{HHH} (GeV)"},

    "hhh_pt":   {"xmin": 0, "xmax": 1000, "bin_width": 10, "x_title": "p_{T, HHH} (GeV)"}
}


for year in year_list:
    year_base_dir = base_dir.format(year=year)

    file_6b_path = os.path.join(year_base_dir, "GluGluToHHHTo6B_SM.root")
    file_4b_path = os.path.join(year_base_dir, "GluGluToHHTo4B_cHHH1.root")
    file_qcd_path = os.path.join(year_base_dir, "QCD_datadriven.root")

    if os.path.isfile(file_6b_path):
        df_dict_6b[year] = ROOT.RDataFrame("Events", file_6b_path)
    else:
        print(f"Warning: Missing 6b file for year {year}")

    if os.path.isfile(file_4b_path):
        df_dict_4b[year] = ROOT.RDataFrame("Events", file_4b_path)
    else:
        print(f"Warning: Missing 4b file for year {year}")

    if os.path.isfile(file_qcd_path):
        df_dict_qcd[year] = ROOT.RDataFrame("Events", file_qcd_path)
    else:
        print(f"Warning: Missing QCD file for year {year}")


for var, vinfo in var_settings.items():
    xmin = vinfo["xmin"]
    xmax = vinfo["xmax"]
    bin_width = vinfo["bin_width"]
    x_title = vinfo["x_title"]
    nbins = int((xmax - xmin) / bin_width)

    print(f"\n>>> Drawing RUN2 overlay: variable = {var}")

    canvas = ROOT.TCanvas(f"canvas_run2_{var}", f"RUN2 {var} overlay", 800, 600)
    max_y = 0.0
    hist_list = []

    # 定义 process 列表
    process_list = [
        ("6b", df_dict_6b, ROOT.kRed),
        ("4b", df_dict_4b, ROOT.kBlue),
        ("QCD", df_dict_qcd, ROOT.kGreen+2)
    ]

    # 针对每个 process 叠加 4 年 → 做总和
    for label, df_dict, color in process_list:
        print(f"  - Processing {label} ...")

        # 初始化为空 histogram
        sum_hist = None

        for year in year_list:
            if year not in df_dict:
                continue

            rdf = df_dict[year]

            hist_rptr = rdf.Histo1D(
                (f"{var}_{label}_{year}", "", nbins, xmin, xmax),
                var,
                "eventWeight"
            )
            hist = hist_rptr.GetValue()

            if hist.Integral() <= 0:
                print(f"    Warning: {label} {year} has no events → skip this year")
                continue

            # 叠加
            if sum_hist is None:
                sum_hist = hist.Clone(f"sum_{label}")
                sum_hist.SetDirectory(0)
            else:
                sum_hist.Add(hist)

        # 如果这个 process 完全没有效 hist → skip
        if sum_hist is None or sum_hist.Integral() <= 0:
            print(f"    Warning: {label} RUN2 total has no events → skip this process")
            continue

        # 归一化
        sum_hist.Scale(1.0 / sum_hist.Integral())

        # 设置风格
        sum_hist.SetLineColor(color)
        sum_hist.SetLineWidth(2)
        sum_hist.GetXaxis().SetTitle(x_title)
        sum_hist.GetYaxis().SetTitle("Normalized yield")

        max_y = max(max_y, sum_hist.GetMaximum())
        hist_list.append((label, sum_hist))

    # 没图就跳
    if not hist_list:
        print(f"  No valid histograms for RUN2 {var}, skipping.")
        del canvas
        gc.collect()
        continue

    # Draw first
    _, first_hist = hist_list[0]
    first_hist.SetMaximum(1.2 * max_y)
    first_hist.Draw("HIST")

    for _, hist in hist_list[1:]:
        hist.Draw("HIST SAME")

    # Legend
    legend = ROOT.TLegend(0.65, 0.7, 0.9, 0.9)
    for label, hist in hist_list:
        legend.AddEntry(hist, f"{label} RUN2", "l")
    legend.SetBorderSize(0)
    legend.Draw()
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.DrawLatex(0.15, 0.91, f"{var} Run2")

    # Save
    output_name = f"output_RUN2_{var}_norm_comparison.pdf"
    canvas.SaveAs(output_name)
    print(f"  Saved: {output_name}")

    # 清理
    del canvas
    del hist_list
    gc.collect()
