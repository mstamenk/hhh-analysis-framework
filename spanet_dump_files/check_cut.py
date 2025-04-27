import glob
import ROOT

treename = "Events"

# 找到当前目录下所有 .root 文件
root_files = glob.glob("/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights/*.root")

for f in sorted(root_files):
    df = ROOT.RDataFrame(treename, f)

    n_total = df.Count()
    n_pass = df.Filter("hhh_mass > 0").Count()

    print(f"File: {f}")
    print(f"  Total events: {n_total.GetValue()}")
    print(f"  Passing (hhh_mass>0): {n_pass.GetValue()}")
    print("-" * 50)
