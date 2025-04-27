# jet1PNetBPlusC
# jet1PNetBVsC
# jet1PNetTagCat 0-10
# fatJet1PNetXbb
# fatJet1PNetXbbTagCat 123

import ROOT
import matplotlib.pyplot as plt

# 打开ROOT文件
file = ROOT.TFile('/eos/cms/store/group/phys_higgs/cmshhh/v34_ak8_option4_2017/mva-inputs-2017/inclusive-weights/HHHTo6B_c3_0_d4_0_TuneCP5_13TeV-amcatnlo-pythia8_tree.root')

# 获取树
tree = file.Get('Events')

# 定义你需要的变量
variables = ['jet1PNetBPlusC', 'jet1PNetBVsC', 'jet1PNetTagCat', 'fatJet1PNetXbb', 'fatJet1PNetXbbTagCat']

# 创建一个字典存储变量的直方图
histograms = {}

# 遍历所有需要的变量，生成直方图
for var in variables:
    if var in ['jet1PNetTagCat', 'fatJet1PNetXbbTagCat']:
        # 对于离散的变量，使用整数直方图，并设置适当的区间
        if var == 'jet1PNetTagCat':
            histograms[var] = ROOT.TH1I(var, var, 10, 0, 10)  # 1-10的整数分布
        elif var == 'fatJet1PNetXbbTagCat':
            histograms[var] = ROOT.TH1I(var, var, 3, 0, 3)  # 1-3的整数分布
    else:
        # 对于连续变量，使用浮动的直方图
        histograms[var] = ROOT.TH1F(var, var, 20, 0, 1)  # 假设变量范围在0到1之间，你可以根据实际情况调整
    
    # 填充直方图
    tree.Draw(f'{var}>>{var}')

# 绘制每个变量的分布
plt.figure(figsize=(10, 8))
for var in variables:
    # 获取直方图数据并绘制
    n_bins = histograms[var].GetNbinsX()
    values = [histograms[var].GetBinContent(i) for i in range(1, n_bins+1)]
    plt.bar(range(1, n_bins+1), values, alpha=0.7, label=var)

# 添加标签和标题
plt.legend(loc='best')
plt.xlabel('Variable Value')
plt.ylabel('Frequency')
plt.title('Distributions of Jet Variables')

# 保存图形为PDF
plt.savefig('distribution_plot.pdf', format='pdf')

# 显示图形
# plt.show()
