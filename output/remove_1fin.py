
import ROOT, os, glob
from array import array

def process_file(path):
    # 打开原文件
    fin = ROOT.TFile.Open(path, "READ")
    if not fin or fin.IsZombie():
        print(f"无法打开：{path}")
        return

    # 构造输出文件名
    dirname  = os.path.dirname(path)
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    out_path = os.path.join(dirname, f"{name}_2to10{ext}")

    fout = ROOT.TFile.Open(out_path, "RECREATE")
    if not fout or fout.IsZombie():
        print(f"无法创建输出：{out_path}")
        fin.Close()
        return

    # 遍历所有对象
    for key in fin.GetListOfKeys():
        obj = key.ReadObj()
        fout.cd()

        if obj.InheritsFrom("TH1"):
            orig = obj
            xax  = orig.GetXaxis()

            # 只取原第2–10个 bin
            edges = [ xax.GetBinLowEdge(i) for i in range(2, 11) ]
            edges.append( xax.GetBinUpEdge(10) )
            eb = array('d', edges)

            # 新 TH1 用原名字、原标题
            newH = ROOT.TH1D(orig.GetName(),
                             orig.GetTitle(),
                             len(eb)-1, eb)

            # 复制内容与误差
            for i in range(1, len(eb)):
                newH.SetBinContent(i, orig.GetBinContent(i+1))
                newH.SetBinError(  i, orig.GetBinError(  i+1))
            newH.Write()
        else:
            # 其余对象原样写入
            obj.Write()

    fout.Close()
    fin.Close()
    print(f"[已生成] {out_path}")

if __name__ == "__main__":
    cat_list = [
        "3bh0h","2bh1h","1bh2h","0bh3h",
        "2bh0h","1bh1h","0bh2h","1bh0h",
        "0bh1h","0bh0h"
    ]
    base_dir = (
        "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/"
        "src/hhh-analysis-framework/output/"
        "v34_fix_ak4_ak8/run2"
    )

    for cat in cat_list:
        hist_dir = os.path.join(
            base_dir,
            f"ProbHHH6b_{cat}_inclusive_CR",
            "histograms"
        )
        file_path = os.path.join(hist_dir, "histograms_ProbMultiH.root")
        if os.path.exists(file_path):
            process_file(file_path)
        else:
            print(f"未找到：{file_path}")
