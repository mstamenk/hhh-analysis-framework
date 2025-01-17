import ROOT
from array import array

def rebin_histogram(hist1,hist2):
    """Rebins a ROOT histogram such that all bin contents become non-negative."""
    # 获取 bin 总数
    nbins1 = hist1.GetNbinsX()
    nbins2 = hist2.GetNbinsX()

    # 找到最后一个负数 bin 的索引
    last_negative_bin_1 = 0
    for i in range(1, nbins1 + 1):
        if hist1.GetBinContent(i) < 0:
            last_negative_bin_1 = i

    last_negative_bin_2 = 0
    for i in range(1, nbins2 + 1):
        if hist2.GetBinContent(i) < 0:
            last_negative_bin_2 = i

    last_negative_bin = max(last_negative_bin_1,last_negative_bin_2)
    

    # 如果没有负数，直接返回原直方图
    if last_negative_bin == 0:
        print("No negative bins found. Returning the original histograms.")
        return hist1.Clone(), hist2.Clone()

    print(f"Last negative bin: {last_negative_bin}")

    # 开始动态 rebin
    rebin_size = 2  # 初始分组大小
    success = False  # 是否分组成功
    new_x_edges_1 = []  # 存储新 X 轴边界
    new_x_edges_2 = []  # 存储新 X 轴边界
    new_bins_1 = []  # 存储分组后的结果
    new_bins_2 = []  # 存储分组后的结果

    while not success:
        new_bins_1 = []  # 存储分组后的结果
        new_bins_2 = []  # 存储分组后的结果
        sum_contents_1 = 0  # 当前分组的内容和
        sum_errors_1 = 0  # 当前分组的误差平方和
        sum_contents_2 = 0  # 当前分组的内容和
        sum_errors_2 = 0  # 当前分组的误差平方和
        new_x_edges_1 = [hist1.GetXaxis().GetBinLowEdge(1)]  # 初始化 X 轴边界
        new_x_edges_2 = [hist2.GetXaxis().GetBinLowEdge(1)]  # 初始化 X 轴边界
        success = True

        # 倒序分组
        for i in range(last_negative_bin, 0, -1):
            sum_contents_1 += hist1.GetBinContent(i)
            sum_errors_1 += hist1.GetBinError(i) ** 2 
            sum_contents_2 += hist2.GetBinContent(i)
            sum_errors_2 += hist2.GetBinError(i) ** 2  # 累加误差平方
            # print(f"Adding bin {i}: content={hist.GetBinContent(i)}, sum_contents={sum_contents}")
            if (last_negative_bin - i + 1) % rebin_size == 0 or i == 1:
                # 满足分组大小，或者到达第一个 bin
                # print(f"Evaluating group ending at bin {i}: sum_contents={sum_contents}, rebin_size={rebin_size}")
                if sum_contents_1 < 0 or sum_contents_2 < 0:
                    # 如果分组后仍有负数，重新尝试
                    success = False
                    # print("Negative group found. Increasing rebin size.")
                    rebin_size += 1
                    break
                if i != 1: 
                    new_x_edges_1.insert(1, hist1.GetXaxis().GetBinLowEdge(i))
                    new_x_edges_2.insert(1, hist2.GetXaxis().GetBinLowEdge(i))
                new_bins_1.insert(0, (sum_contents_1, sum_errors_1 ** 0.5))
                new_bins_2.insert(0, (sum_contents_2, sum_errors_2 ** 0.5))
                # print(f"Group added: content={sum_contents}, error={sum_errors ** 0.5}")
                sum_contents_1 = 0
                sum_errors_1 = 0
                sum_contents_2 = 0
                sum_errors_2 = 0
        else:
            # 如果循环正常结束（没有 break），说明分组成功
            success = True

    print(f"Final rebin size: {rebin_size}")
    # print(f"New bins: {new_bins}")

    new_x_edges_1.append(hist1.GetXaxis().GetBinUpEdge(last_negative_bin))
    new_x_edges_2.append(hist2.GetXaxis().GetBinUpEdge(last_negative_bin))
    # 添加未修改部分的 X 坐标
    for i in range(last_negative_bin + 1, nbins1 + 1):
        new_x_edges_1.append(hist1.GetXaxis().GetBinUpEdge(i))
    for i in range(last_negative_bin + 1, nbins2 + 1):
        new_x_edges_2.append(hist2.GetXaxis().GetBinUpEdge(i))

    print(f"New X edges1: {new_x_edges_1}")
    print(f"New X edges2: {new_x_edges_2}")

    return new_x_edges_1

def rebin_histogram_with_fixed_edges(hist, new_x_edges):
    """Rebins a histogram using predefined bin edges."""
    new_hist = ROOT.TH1F(
        hist.GetName(),
        hist.GetTitle(),
        len(new_x_edges) - 1,
        array('d', new_x_edges),
    )

    # Fill the new histogram with the contents of the old histogram
    for i in range(1, hist.GetNbinsX() + 1):
        bin_center = hist.GetXaxis().GetBinCenter(i)
        bin_content = hist.GetBinContent(i)
        bin_error = hist.GetBinError(i)

        # Find the bin in the new histogram corresponding to the old bin
        new_bin = new_hist.FindBin(bin_center)
        new_hist.SetBinContent(new_bin, new_hist.GetBinContent(new_bin) + bin_content)
        new_hist.SetBinError(new_bin, (new_hist.GetBinError(new_bin)**2 + bin_error**2)**0.5)

    return new_hist

def merge_bins(new_x_edges_1, new_x_edges_2):
    """Merge two sets of bin edges into a unified set of bin edges."""
    # Find the union of the two sets of bin edges, and keep unique edges
    unified_edges = sorted(set(new_x_edges_1 + new_x_edges_2))
    return unified_edges

# 测试代码
# 主程序
type_list = ["alt"]
for type in type_list:
    input_path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbbb/new_hist_%s_rebin_20178"%type
    output_path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbbb/new_hist_%s_rebin_20178_try"%type
    # cat_list = ['GGFcateg1_1','GGFcateg1','GGFcateg2_1','GGFcateg2','VBFcateg1_1','VBFcateg1']
    cat_list = ['GGFcateg1_1','GGFcateg2_1','VBFcateg1_1']
    for cat in cat_list:
        print("%s/outPlotter_%s.root"%(input_path,cat))
        input_file = ROOT.TFile.Open("%s/outPlotter_%s.root"%(input_path,cat), "READ")
        if not input_file or input_file.IsZombie():
            print(f"Failed to open file: {input_path}/outPlotter_{cat}.root")
            continue
        output_file = ROOT.TFile.Open("%s/outPlotter_%s.root"%(output_path,cat), "RECREATE")

        # 需要特殊处理的直方图名字
        special_histograms = ["ggHH_kl_m20p00_kt_1p00_c2_2p24_2018_hbbhbb", "ggHH_kl_m20p00_kt_1p00_c2_2p24_2017_hbbhbb","ggHH_kl_m20p00_kt_1p00_c2_2p24_2016_hbbhbb"]  # 需要做 rebin 操作的直方图名字
        skip_histograms = []  # 需要直接跳过的直方图名字

        new_x_edges_2016 = []
        new_x_edges_2017 = []
        new_x_edges_2018 = []


        
        # 关闭文件
        hist1 = input_file.Get("ggHH_kl_m20p00_kt_1p00_c2_2p24_2017_hbbhbb")
        if hist1:
            print("Successfully loaded histogram:ggHH_kl_m20p00_kt_1p00_c2_2p24_2017_hbbhbb")
        else:
            print(f"Failed to find the histogram in the file.{input_path}/{cat}/2017")
        
        hist2 = input_file.Get("ggHH_kl_m20p00_kt_1p00_c2_2p24_2018_hbbhbb")
        if hist2:
            print("Successfully loaded histogram:ggHH_kl_m20p00_kt_1p00_c2_2p24_2018_hbbhbb")
        else:
            print(f"Failed to find the histogram in the file.{input_path}/{cat}/2018")
        


        
        new_x_edges = rebin_histogram(hist1,hist2)
        print("final new_x_edges")
        print(new_x_edges)

        new_hist1 = rebin_histogram_with_fixed_edges(hist1,new_x_edges)
        new_hist1.Write()
        new_hist2 = rebin_histogram_with_fixed_edges(hist2,new_x_edges)
        new_hist2.Write()
       

        input_file.Close()
        output_file.Close()
