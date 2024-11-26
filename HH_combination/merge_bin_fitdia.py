import ROOT
from array import array

def rebin_new_histogram_with_existing_scheme(hist, last_negative_bin, rebin_size):
    """
    Rebin a histogram using the scheme from another histogram.
    Parameters:
        hist (TH1F): The new histogram to rebin.
        last_negative_bin (int): The last negative bin position from the original histogram.
        rebin_size (int): The size of the groups to merge bins.
    Returns:
        TH1F: The rebinned histogram.
    """
    num_bins = hist.GetNbinsX()
    x_edges = []  # Stores the new bin edges
    new_bins = []  # Stores the new bin contents and errors

    # Initialize new bin edges
    x_edges.append(hist.GetXaxis().GetBinLowEdge(1))

    sum_content = 0
    sum_error_sq = 0
    for i in range(1, last_negative_bin + 1):
        # Accumulate content and error
        sum_content += hist.GetBinContent(i)
        sum_error_sq += hist.GetBinError(i) ** 2

        # If we've reached the rebin_size or the last bin before last_negative_bin
        if (i - 1) % rebin_size == (rebin_size - 1) or i == last_negative_bin:
            new_bins.append((sum_content, sum_error_sq ** 0.5))
            x_edges.append(hist.GetXaxis().GetBinUpEdge(i))
            sum_content = 0
            sum_error_sq = 0

    # Append remaining bins without merging
    for i in range(last_negative_bin + 1, num_bins + 1):
        new_bins.append((hist.GetBinContent(i), hist.GetBinError(i)))
        x_edges.append(hist.GetXaxis().GetBinUpEdge(i))

    # Create the new histogram
    new_hist = ROOT.TH1F(
        hist.GetName() + "_rebin",
        hist.GetTitle(),
        len(x_edges) - 1,
        array('d', x_edges)
    )

    # Fill the new histogram with the rebinned contents and errors
    for i, (content, error) in enumerate(new_bins, start=1):
        new_hist.SetBinContent(i, content)
        new_hist.SetBinError(i, error)

    return new_hist


# 示例代码
path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/fitdiagnose/bbbb"
input_file = ROOT.TFile.Open("%s/fitdiagnostics__unblinded__poi_r__params_r1.0_r_gghh1.0_r_qqhh0.0_kl-20.0_kt1.0_CV1.0_C2V1.0_C22.24__fromsnapshot.root"%path, "READ")
output_file = ROOT.TFile.Open("%s/rebin_fitdiagnostics__unblinded__poi_r__params_r1.0_r_gghh1.0_r_qqhh0.0_kl-20.0_kt1.0_CV1.0_C2V1.0_C22.24__fromsnapshot.root"%path, "RECREATE")
folder_shapes = output_file.mkdir("shapes_prefit")
# 假设原来的最后负数 bin 和合并方案
last_negative_bin = 43
rebin_size = 8

cat_list = {
    #alt
    "GGFcateg1_2016": {"final": 43, "size":8},
    "GGFcateg2_2016": {"final": 42, "size":7},
    "VBFcateg1_2016": {"final": 30, "size":5},
    #alt2
    # "GGFcateg1_2016": {"final": 43, "size":8},
    # "GGFcateg2_2016": {"final": 42, "size":8},
    # "VBFcateg1_2016": {"final": 30, "size":8},
    
}

for cat in cat_list:
    dir_path = "shapes_prefit/bbbb_%s"%(cat)
    dic_fit = input_file.Get(dir_path)
    if not dic_fit:
        print(f"Directory {dir_path} not found in the file!")
    else:
        hist_fit = dic_fit.Get("total_signal")

        if not hist_fit:
            print("Error: Could not find histogram in file_fit.")
            print("shapes_prefit/bbbb_%s in %s"%(cat,path) )
    folder_shapes.cd()
    folder_out = output_file.mkdir("bbbb_%s"%(cat))
    folder_out.cd()
    last_negative_bin = cat_list[cat]["final"]
    rebin_size = cat_list[cat]["size"]
    rebinned_hist = rebin_new_histogram_with_existing_scheme(hist_fit, last_negative_bin, rebin_size)
    rebinned_hist.Write()
    folder_shapes.cd()

input_file.Close()
output_file.Close()

