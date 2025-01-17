import matplotlib.pyplot as plt
import numpy as np
import uproot
import numpy as np
import ROOT
from matplotlib.colors import LogNorm

path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v28/2018/boost_resolved'
root_file_path = "%s/ProbHHH6b_3Higgs_inclusive_/GluGluToHHHTo6B_SM.root"%(path)

root_file = ROOT.TFile.Open(root_file_path)
tree = ROOT.RDataFrame("Events", root_file)
h1_t3_mass = np.array(tree.AsNumpy(columns=["h1_t3_mass"])["h1_t3_mass"])
h2_t3_mass = np.array(tree.AsNumpy(columns=["h2_t3_mass"])["h2_t3_mass"])
h3_t3_mass = np.array(tree.AsNumpy(columns=["h3_t3_mass"])["h3_t3_mass"])
print(h1_t3_mass)



# plt.scatter(h1_mass, h2_mass, c=all_labels, alpha=0.5)
plt.hist2d(h2_t3_mass, h3_t3_mass, bins=100, cmap='viridis')
plt.colorbar()
plt.xlabel(r'$M_{H1}$', usetex=True)
plt.ylabel(r'$M_{H1}$', usetex=True)
plt.xlim([0, 350])  # 用你的实际范围替换 min_value_x 和 max_value_x
plt.ylim([0, 350])
# plt.title('H1 和 H2 ')
# plt.legend(['H1', 'H2', 'H3'])
path_to_plot = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/reweighting/'
plt.savefig("%s/region_plot_H2_H3.png"%(path_to_plot))
# plt.show()
