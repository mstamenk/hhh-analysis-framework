import json
import ROOT
from array import array

def apply_rebin(bin_name, process_name, nominal_shape, systematic_shapes):
    # 加载 JSON 配置文件
    with open("rebin_config.json", "r") as f:
        rebin_config = json.load(f)
    
    # 查找对应的 new_x_edges
    try:
        new_x_edges = rebin_config[bin_name][process_name]
    except KeyError:
        print(f"No rebin configuration found for bin: {bin_name}, process: {process_name}")
        return

    # 创建新的 nominal histogram
    new_nominal = ROOT.TH1F(
        f"{nominal_shape.GetName()}_rebinned",
        nominal_shape.GetTitle(),
        len(new_x_edges) - 1,
        array('d', new_x_edges),
    )

    # 填充 nominal histogram
    for i in range(1, nominal_shape.GetNbinsX() + 1):
        bin_center = nominal_shape.GetXaxis().GetBinCenter(i)
        bin_content = nominal_shape.GetBinContent(i)
        bin_error = nominal_shape.GetBinError(i)

        # 找到新 histogram 中对应的 bin
        new_bin = new_nominal.FindBin(bin_center)
        new_nominal.SetBinContent(new_bin, new_nominal.GetBinContent(new_bin) + bin_content)
        new_nominal.SetBinError(new_bin, (new_nominal.GetBinError(new_bin)**2 + bin_error**2)**0.5)

    # 同样对系统误差的直方图进行 rebin
    for syst_name, (down, up) in systematic_shapes.items():
        for direction, hist in zip(["down", "up"], [down, up]):
            new_hist = ROOT.TH1F(
                f"{hist.GetName()}_rebinned_{direction}",
                hist.GetTitle(),
                len(new_x_edges) - 1,
                array('d', new_x_edges),
            )
            for i in range(1, hist.GetNbinsX() + 1):
                bin_center = hist.GetXaxis().GetBinCenter(i)
                bin_content = hist.GetBinContent(i)
                bin_error = hist.GetBinError(i)

                new_bin = new_hist.FindBin(bin_center)
                new_hist.SetBinContent(new_bin, new_hist.GetBinContent(new_bin) + bin_content)
                new_hist.SetBinError(new_bin, (new_hist.GetBinError(new_bin)**2 + bin_error**2)**0.5)

            # 替换旧的系统误差直方图
            if direction == "down":
                systematic_shapes[syst_name] = (new_hist, systematic_shapes[syst_name][1])
            elif direction == "up":
                systematic_shapes[syst_name] = (systematic_shapes[syst_name][0], new_hist)

    # 更新 nominal 直方图
    nominal_shape.Reset()
    nominal_shape.Add(new_nominal)
