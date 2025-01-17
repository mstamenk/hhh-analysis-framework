import ROOT

def read_histograms(file_path, folder_path, histograms_to_read):
    # 打开 ROOT 文件
    root_file = ROOT.TFile(file_path, "READ")
    
    if root_file.IsZombie():
        print("Failed to open file.")
        return

    # 进入指定文件夹
    folder = root_file.Get(folder_path)
    if not folder:
        print(f"Folder {folder_path} not found.")
        return

    results = {}

    for hist_name in histograms_to_read:
        # 获取直方图或 TGraphAsymmErrors
        obj = folder.Get(hist_name)
        if not obj:
            print(f"Histogram {hist_name} not found in {folder_path}.")
            continue

        if isinstance(obj, ROOT.TH1):  # 如果是 TH1 类型
            total_yield = obj.Integral()
            n_bins = obj.GetNbinsX()
            last_three_sum = sum(obj.GetBinContent(i) for i in range(n_bins - 2, n_bins + 1))
        elif isinstance(obj, ROOT.TGraphAsymmErrors):  # 如果是 TGraphAsymmErrors 类型
            n_points = obj.GetN()
            total_yield = sum(obj.GetY()[i] for i in range(n_points))  # 计算所有点的总和
            last_three_sum = sum(obj.GetY()[i] for i in range(n_points - 3, n_points))  # 最后三个点的和
        else:
            print(f"Object {hist_name} is of unsupported type: {type(obj)}")
            continue

        # 保存结果
        results[hist_name] = {
            "total_yield": total_yield,
            "last_three_bins_sum": last_three_sum
        }

    # 关闭文件
    root_file.Close()

    return results

if __name__ == "__main__":
    # 输入 ROOT 文件路径
    root_file_path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_10_2_13/src/new/datacards_maker_hhh/combine_results/boost_resolved/v33/Marko_sample_1Higgs/9tag/ProbMultiH/fitDiagnosticsTest.root"  # 修改为你的文件路径
    folder_list = ["shapes_prefit/HHH_0bh0h_run2","shapes_prefit/HHH_1Higgs_run2","shapes_prefit/HHH_0bh2h_run2","shapes_prefit/HHH_1bh1h_run2","shapes_prefit/HHH_2bh0h_run2","shapes_prefit/HHH_0bh3h_run2","shapes_prefit/HHH_1bh2h_run2","shapes_prefit/HHH_2bh1h_run2","shapes_prefit/HHH_3bh0h_run2"]
    histograms = ["data", "QCD", "GluGluToHHHTo6B_SM", "GluGluToHHTo4B_cHHH1"]

    for folder_name in folder_list:

        # 读取直方图数据
        results = read_histograms(root_file_path, folder_name, histograms)
        print(folder_name)


        # 打印结果
        for hist_name, data in results.items():
            print(f"Histogram: {hist_name}")
            print(f"  Total Yield: {data['total_yield']}")
            print(f"  Sum of Last Three Bins: {data['last_three_bins_sum']}")
