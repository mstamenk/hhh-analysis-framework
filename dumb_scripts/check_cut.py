import ROOT
import os

# 输入文件和参数
year_list = ["2018","2017","2016","2016APV"]
# year_list = ["2016_all"]
for year in year_list:
    path = "/eos/cms/store/group/phys_higgs/cmshhh/v34-fix-ak4-ak8/mva-inputs-%s-categorisation-spanet-boosted-classification/ProbHHH6b_3bh0h_inclusive_CR"%(year)
    filename = os.path.join(path, "GluGluToHHHTo6B_SM.root")
    treename = "Events"
    cut = "ProbMultiH > 0.829"
    weight_expr = "totalWeight"

    # 读取 TTree -> RDataFrame
    df = ROOT.RDataFrame(treename, filename)
    filtered_df = df.Filter(cut)
    yield_result = filtered_df.Define("w", weight_expr).Sum("w").GetValue()
    print(f"✅{year} Yield from RDataFrame (after cut): {yield_result:.6f}")

# ---- 读取直方图 yield ----
# 你想读取的 histogram 名称列表
    path_hist = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34-fix-ak4-ak8/%s/ProbHHH6b_3bh0h_inclusive_CR/histograms"%(year)
    hist_names = [
        "GluGluToHHHTo6B_SM",  # 替换为你实际文件中存在的名字
    ]

    # 打开 ROOT 文件
    f = ROOT.TFile.Open('{}/histograms_ProbMultiH.root'.format(path_hist))
    if not f or f.IsZombie():
        print("❌ Error opening file.")
        exit(1)

    print("✅ Histogram yields:")
    for hname in hist_names:
        h = f.Get(hname)
        if not h:
            print(f"  ⚠️  Histogram '{hname}' not found.")
            continue
        # 累加 bin contents
        integral = h.Integral()
        print(f" {year} - {hname}: {integral:.6f}")

    f.Close()
