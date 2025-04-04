import ROOT
from array import array

def rebin_histogram(hist):
    """Rebins a ROOT histogram such that all bin contents become non-negative."""
    # Get total number of bins
    nbins = hist.GetNbinsX()

    # Find the index of the last negative bin
    last_negative_bin = 0
    for i in range(1, nbins + 1):
        if hist.GetBinContent(i) < 0:
            last_negative_bin = i

    # If there are no negative bins, return the original histogram
    if last_negative_bin == 0:
        print("No negative bins found. Returning the original histogram.")
        return hist.Clone()

    print(f"Last negative bin: {last_negative_bin}")

    # Start dynamic rebinning
    rebin_size = 2  # Initial binning size
    success = False  # Whether the binning was successful
    new_x_edges = []  # To store the new X axis edges
    new_bins = []  # To store the rebinned results

    while not success:
        new_bins = []  # To store the rebinned results
        sum_contents = 0  # Sum of contents for the current bin group
        sum_errors = 0  # Sum of squared errors for the current bin group
        new_x_edges = [hist.GetXaxis().GetBinLowEdge(1)]  # Initialize the X axis edges
        success = True

        # Rebin in reverse order
        for i in range(last_negative_bin, 0, -1):
            sum_contents += hist.GetBinContent(i)
            sum_errors += hist.GetBinError(i) ** 2  # Accumulate squared errors
            # print(f"Adding bin {i}: content={hist.GetBinContent(i)}, sum_contents={sum_contents}")
            if (last_negative_bin - i + 1) % rebin_size == 0 or i == 1:
                # If the group size is reached or it's the first bin
                # print(f"Evaluating group ending at bin {i}: sum_contents={sum_contents}, rebin_size={rebin_size}")
                if sum_contents < 0:
                    # If the grouped bin still has negative content, retry
                    success = False
                    # print("Negative group found. Increasing rebin size.")
                    rebin_size += 1
                    break
                if i != 1: 
                    new_x_edges.insert(1, hist.GetXaxis().GetBinLowEdge(i))
                new_bins.insert(0, (sum_contents, sum_errors ** 0.5))
                # print(f"Group added: content={sum_contents}, error={sum_errors ** 0.5}")
                sum_contents = 0
                sum_errors = 0
        else:
            # If the loop ends without a break, binning is successful
            success = True

    print(f"Final rebin size: {rebin_size}")
    # print(f"New bins: {new_bins}")

    new_x_edges.append(hist.GetXaxis().GetBinUpEdge(last_negative_bin))
    # Add the unmodified part of the X axis
    for i in range(last_negative_bin + 1, nbins + 1):
        new_x_edges.append(hist.GetXaxis().GetBinUpEdge(i))

    print(f"New X edges: {new_x_edges}")

    # Create a new histogram
    new_hist = ROOT.TH1F(
        hist.GetName(),
        hist.GetTitle(),
        len(new_x_edges) - 1,
        array('d', new_x_edges),
    )

    # Fill the new histogram with the rebinned contents
    for i, (content, error) in enumerate(new_bins, start=1):
        new_hist.SetBinContent(i, content)
        new_hist.SetBinError(i, error)

    # Fill the unmodified bins
    for i in range(last_negative_bin + 1, nbins + 1):
        bin_index = len(new_bins) + (i - last_negative_bin)
        new_hist.SetBinContent(bin_index, hist.GetBinContent(i))
        new_hist.SetBinError(bin_index, hist.GetBinError(i))

    return new_hist , new_x_edges

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

# Test code
# Main program
type_list = ["alt","alt2"]
for type in type_list:
    input_path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbbb/new_hist_%s" % type
    output_path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbbb/new_hist_%s_rebin" % type
    cat_list = ['GGFcateg1_1','GGFcateg1','GGFcateg2_1','GGFcateg2','VBFcateg1_1','VBFcateg1']
    for cat in cat_list:
        input_file = ROOT.TFile.Open("%s/outPlotter_%s.root" % (input_path, cat), "READ")
        if not input_file or input_file.IsZombie():
            print(f"Failed to open file: {input_path}/outPlotter_{cat}.root")
            continue
        output_file = ROOT.TFile.Open("%s/outPlotter_%s.root" % (output_path, cat), "RECREATE")

        # Special histograms that need rebinning
        special_histograms = ["ggHH_kl_m20p00_kt_1p00_c2_2p24_2018_hbbhbb", "ggHH_kl_m20p00_kt_1p00_c2_2p24_2017_hbbhbb", "ggHH_kl_m20p00_kt_1p00_c2_2p24_2016_hbbhbb"]  
        skip_histograms = []  # Histograms to skip

        new_x_edges_2016 = []
        new_x_edges_2017 = []
        new_x_edges_2018 = []
        for key in input_file.GetListOfKeys():

            obj = key.ReadObj()
            if isinstance(obj, ROOT.TH1F):  # Ensure it's a TH1F type
                hist_name = obj.GetName()
                

                if hist_name in special_histograms:
                    print(f"Rebinning histogram: {hist_name}")
                    # new_hist = rebin_histogram(obj)
                    print("%s/outPlotter_%s.root" % (input_path, cat))
                    new_hist, new_x_edges = rebin_histogram(obj)
                    if hist_name == "ggHH_kl_m20p00_kt_1p00_c2_2p24_2016_hbbhbb":
                        new_x_edges_2016 = new_x_edges
                    elif hist_name == "ggHH_kl_m20p00_kt_1p00_c2_2p24_2017_hbbhbb":
                        new_x_edges_2017 = new_x_edges
                    elif hist_name == "ggHH_kl_m20p00_kt_1p00_c2_2p24_2018_hbbhbb":
                        new_x_edges_2018 = new_x_edges

                    new_hist.Write()

                elif hist_name.startswith("ggHH_kl_m20p00_kt_1p00_c2_2p24_2016_hbbhbb"):
                    new_hist = rebin_histogram_with_fixed_edges(obj, new_x_edges_2016)
                    new_hist.Write()
                elif hist_name.startswith("ggHH_kl_m20p00_kt_1p00_c2_2p24_2017_hbbhbb"):
                    new_hist = rebin_histogram_with_fixed_edges(obj, new_x_edges_2017)
                    new_hist.Write()

                elif hist_name.startswith("ggHH_kl_m20p00_kt_1p00_c2_2p24_2018_hbbhbb"):
                    new_hist = rebin_histogram_with_fixed_edges(obj, new_x_edges_2018)
                    new_hist.Write()

                else:
                    # Copy the histogram without changes
                    obj_clone = obj.Clone()
                    obj_clone.Write()

        input_file.Close()
        output_file.Close()
