import uproot
import numpy as np
import awkward as ak
import matplotlib.pyplot as plt

# 读取 ROOT 文件并获取变量和权重
def load_data(file_list):
    prob_all = []
    weight_all = []
    for file_name in file_list:
        with uproot.open(file_name) as f:
            tree = f["Events"]
            prob = tree["ProbMultiH_v34"].array(library="np")
            if 'data' in file_name:   
                weight = np.ones_like(prob)
            else:   
                weight = tree["eventWeight"].array(library="np")
            prob_all.append(prob)
            weight_all.append(weight)
    return np.concatenate(prob_all), np.concatenate(weight_all)

# 计算误差（假设为 sqrt(sum of weights^2)）
def hist_and_error(values, weights, bins):
    hist, _ = np.histogram(values, bins=bins, weights=weights)
    err2, _ = np.histogram(values, bins=bins, weights=weights**2)
    err = np.sqrt(err2)
    return hist, err

# def get_data_yield_in_range(data_files, x_cut):
#     data_values, data_weights = load_data(data_files)
#     mask = (data_values >= x_cut) & (data_values <= 1.0)
#     return np.sum(data_weights[mask])
    
# 主程序逻辑
def find_best_binning(qcd_files, signal_files, data_files,category):
    # prob_data, w_data = load_data(data_file)
    prob_qcd, w_qcd = load_data(qcd_files)
    prob_6b, w_6b = load_data(signal_files)
    prob_data, w_data = load_data(data_files)

    
    # 遍历最后一个 bin 的起始点 x
    for x in np.linspace(1.0, 0.7, 300):  # 从大到小遍历
        bins = [x, 1.0]
        _, err_qcd = hist_and_error(prob_qcd, w_qcd, bins)
        hist_qcd, _ = hist_and_error(prob_qcd, w_qcd, bins)
        hist_data, _ = hist_and_error(prob_data, w_data, bins)

        if hist_qcd[0] > 0:
            ratio = hist_data[0] / hist_qcd[0]
            _, err_qcd_scale = hist_and_error(prob_qcd, w_qcd*ratio, bins)
            hist_qcd_scaled, _ = hist_and_error(prob_qcd, w_qcd*ratio, bins)


            if err_qcd_scale[0] / hist_qcd_scaled[0] <= 0.2:
                x_cut = x
                break
    else:
        raise RuntimeError("No x found where error/yield >= 0.2")


    print(f"[{category}] Found x = {x_cut:.4f} for last bin (x,1.0) with rel error = 0.2")
    

    # 遍历等宽 bin 的宽度
    best_metric = -np.inf
    best_bins = None
    best_bin_width = None
    final_bin_width = 1.0-x_cut
    
    bin_width_range = np.linspace(0.01, final_bin_width, 200)
    for width in  bin_width_range:
        left_edge = x_cut - 9 * width
        if left_edge < 0:
            continue  # bin 超出范围

    # 构造等宽 bin，从 left_edge 开始，每个宽度为 width，直到 x_cut
        bin_edges = list(np.arange(left_edge, x_cut + 1e-8, width))  # 只到 x_cut
        bin_edges.append(1.0)  # 加上最后一个 bin 的终点

        hist_qcd, _ = hist_and_error(prob_qcd, w_qcd, bin_edges)
        hist_6b, _ = hist_and_error(prob_6b, w_6b, bin_edges)
        hist_data, _ = hist_and_error(prob_data, w_data, bin_edges)
        total_qcd_yield = np.sum(hist_qcd)
        total_6b_yield = np.sum(hist_6b)
        total_data_yield = np.sum(hist_data)
        ratio = total_data_yield / total_qcd_yield

        z_total_sq = 0.0
        hist_qcd_scaled,_ = hist_and_error(prob_qcd, w_qcd*ratio, bin_edges)
        for s, b in zip(hist_6b, hist_qcd_scaled):
            if b > 0:
                z_total_sq += (s / np.sqrt(b))**2
        z_total = np.sqrt(z_total_sq)
        # print(f"Trying width={width:.5f},  z_total = {z_total:.10f}")

        if z_total > best_metric:
            best_metric = z_total
            best_bins = bin_edges
            best_hist_qcd_scaled = hist_qcd_scaled
            best_hist_6b = hist_6b
            best_bin_width = width
            best_data = hist_data


    print("Best bin width found:", best_bin_width)
    print("Best bin edges found:", best_bins)
    print("Best S/sqrt(B) =", best_metric)

    return best_bins, best_hist_qcd_scaled, best_hist_6b,best_data, best_bin_width, x_cut

def draw_and_save_hist(bin_edges, hist_qcd, hist_6b,hist_data,category, bin_width, x_cut,  out_path="./"):
    bin_centers = 0.5 * (np.array(bin_edges[:-1]) + np.array(bin_edges[1:]))
    bin_widths = np.diff(bin_edges)

    hist_6b_scaled = hist_6b * 1000
    visible_bins = len(hist_data) - 2
    data_visible = hist_data[:visible_bins]
    data_centers_visible = bin_centers[:visible_bins]
    data_errors_visible = np.sqrt(hist_data[:visible_bins])

    plt.figure(figsize=(10, 6))
    plt.bar(bin_centers, hist_qcd, width=bin_widths, alpha=0.6, label="QCD", align="center", color="C0")
    plt.bar(bin_centers, hist_6b_scaled, width=bin_widths, alpha=1.0, label="6b Signal (X 1000)", align="center", edgecolor="C1", facecolor="none", linewidth=1.8)   
    plt.errorbar(data_centers_visible, data_visible, yerr=data_errors_visible, fmt='ko', label="Data")    
    y_max = max(np.max(hist_qcd), np.max(hist_6b_scaled),np.max(hist_data)) * 1.2
    # text = f"bin width = {bin_width:.5f}\nlast bin starts at {x_cut:.4f}"
    # plt.text(0.05, y_max * 0.99, text, fontsize=10, bbox=dict(facecolor='black', alpha=0.7))
    info_text = f"bin width = {bin_width:.5f}\nlast bin starts at {x_cut:.4f}"
    plt.text(0.95,1.08, info_text,
            transform=plt.gca().transAxes,   # 👈 这是关键，使用当前坐标轴的轴坐标系
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7),
            color='black',
            verticalalignment='top',
            horizontalalignment='right')

    plt.xlabel("ProbMultiH")
    plt.ylabel("Weighted yield")
    plt.title(f"Optimized binning: {category}")
    plt.ylim(0, y_max)
    plt.legend()
    plt.grid(True)
    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
    plt.savefig(f"{out_path}/optimized_binning_{category}_inclusive.pdf")
    plt.close()


years = ["2016", "2016APV", "2017", "2018"]
base_path = "/eos/cms/store/group/phys_higgs/cmshhh/v34-test/final"
category_list = ["3bh0h","1bh2h","2bh1h","0bh3h","0bh2h","1bh1h","2bh0h","1Higgs","0bh0h"]  # 可拓展为多类别


custom_bin_config = {}

for cat in category_list:
    qcd_files = []
    signal_files = []
    data_files = []
    for year in years:
        # year_path = f"{base_path}/mva-inputs-{year}-categorisation-spanet-boosted-classification"
        year_path = f"{base_path}/{year}"
        qcd_files.append(f"{year_path}/ProbHHH6b_{cat}_inclusive_CR/QCD_datadriven.root")
        signal_files.append(f"{year_path}/ProbHHH6b_{cat}_inclusive_CR/GluGluToHHHTo6B_SM.root")
        data_files.append(f"{year_path}/ProbHHH6b_{cat}_inclusive_CR/data_obs.root")

    print(f"\n🔍 Processing category: {cat}")
    bins, hist_qcd, hist_6b,hist_data, width, x_cut = find_best_binning(qcd_files, signal_files, data_files,cat)
    draw_and_save_hist(bins, hist_qcd, hist_6b, hist_data,cat, width, x_cut)
    config_key = f"ProbHHH6b_{cat}_inclusive"
    custom_bin_config[config_key] = (round(x_cut, 4), round(width, 5))

print("\ncustom_bin_config = {")
for k, v in custom_bin_config.items():
    print(f"    '{k}': {v},")
print("}")


