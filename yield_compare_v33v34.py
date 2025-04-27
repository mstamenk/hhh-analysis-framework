import ROOT
import glob

# 设定luminosity值（你需要提供正确的luminosity值）
lumi = 41480.0
# 目录路径
root_dir = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-2017-categorisation-spanet-boosted-classification/inclusive-weights/"
file_list = glob.glob(root_dir + "*.root")

# 创建字典存储每个文件的 yield
yield_results = {}

for file_path in file_list:
    if "BTagCSV" in file_path or "UP" in file_path or "DOWN" in file_path or "datadriven" in file_path  or "SingleMuon" in file_path: 
        continue
    print(f"Processing file: {file_path}")
    
    # 读取 ROOT 文件
    df = ROOT.RDataFrame("Events", file_path)  # "Events" 是默认的 TTree 名称

    # 定义 totalWeight 列
    df = df.Define("totalWeight", f"({lumi} * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF)")

    # 计算 totalWeight 的总和
    yield_value = df.Sum("totalWeight").GetValue()
    
    # 存储结果
    yield_results[file_path] = yield_value

    print(f"Yield for {file_path}: {yield_value}")

# 打印所有文件的 yield 结果
print("\n==== Yield Summary ====")
for file, yield_val in yield_results.items():
    print(f"{file}: {yield_val}")
