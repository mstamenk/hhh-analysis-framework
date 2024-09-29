import yaml
import sympy as sp
import ROOT
import numpy as np
import matplotlib.pyplot as plt

# 定义一个函数来创建每个样本的字典结构
def create_sample_data(sample_name, years):
    sample_data = {}
    for year in years:
        # 可以根据需要设置数据的默认值
        sample_data[year] = {
            "Nevents_generated": None,  # 你可以通过循环或条件在这里插入实际数据
            "Nevents_assumed": None,
            "Ratio_correct": None,
            "Kfactor": None
        }
    return {sample_name: sample_data}

# 定义样本名称列表和年份

# 初始化一个空的字典来存储所有样本数据
data = {}

# 通过循环自动为每个样本和年份添加数据
# for sample in samples:
#     # 生成每个样本的结构
#     sample_data = create_sample_data(sample, years)
#     # 将生成的样本数据合并到总的数据字典中
#     data.update(sample_data)

# # 将数据写入YAML文件
# with open('output.yaml', 'w') as file:
#     yaml.dump(data, file, default_flow_style=False)

# print("YAML 文件已生成！")


# for sample in samples:
#     sample_data = create_sample_data(sample, years)
#     for year in years:
#         sample_data[sample][year]["Nevents_generated"] = sample_values[sample][year]
#         sample_data[sample][year]["Nevents_assumed"] = sample_values[sample][year] * 1.1  # 假设值
#         sample_data[sample][year]["Kfactor"] = 1.2  # 假设值
#     data.update(sample_data)



entries = {
    '2016': {
        'c3_0_d4_99': 24192.0,
        'c3_0_d4_0': 326592.0,
        'c3_0_d4_m1': 27216.0,
        'c3_19_d4_19': 33264.0,
        'c3_1_d4_0': 73926.0,
        'c3_1_d4_2': 24192.0,
        'c3_2_d4_m1': 30240.0,
        'c3_4_d4_9': 28728.0,
        'c3_m1_d4_0': 30240.0,
        'c3_m1_d4_m1': 27216.0,
        'c3_m1p5_d4_m0p5': 27216.0
    },
    '2016APV': {
        'c3_0_d4_99': 18144.0,
        'c3_0_d4_0': 347760.0,
        'c3_0_d4_m1': 19656.0,
        'c3_19_d4_19': 15120.0,
        'c3_1_d4_0': 22680.0,
        'c3_1_d4_2': 28728.0,
        'c3_2_d4_m1': 19656.0,
        'c3_4_d4_9': 9072.0,
        'c3_m1_d4_0': 21168.0,
        'c3_m1_d4_m1': 21168.0,
        'c3_m1p5_d4_m0p5': 6048.0
    },
    '2017': {
        'c3_0_d4_99': 33480.0,
        'c3_0_d4_0': 296298.0,
        'c3_0_d4_m1': 35154.0,
        'c3_19_d4_19': 41850.0,
        'c3_1_d4_0': 45198.0,
        'c3_1_d4_2': 41850.0,
        'c3_2_d4_m1': 53568.0,
        'c3_4_d4_9': 36828.0,
        'c3_m1_d4_0': 33480.0,
        'c3_m1_d4_m1': 40176.0,
        'c3_m1p5_d4_m0p5': 38502.0
    },
    '2018': {
        'c3_0_d4_99': 37628.0,
        'c3_0_d4_0': 492436.0,
        'c3_0_d4_m1': 32720.0,
        'c3_19_d4_19': 31084.0,
        'c3_1_d4_0': 31084.0,
        'c3_1_d4_2': 35992.0,
        'c3_2_d4_m1': 29448.0,
        'c3_4_d4_9': 31084.0,
        'c3_m1_d4_0': 35992.0,
        'c3_m1_d4_m1': 29448.0,
        'c3_m1p5_d4_m0p5': 32720.0
    }
}

yield_table = {
    "c3_0_d4_0"             :0.03274*1e-3,
    "c3_0_d4_99"            :5.243*1e-3,
    "c3_0_d4_m1"            :0.03624*1e-3,
    "c3_19_d4_19"           :131.8*1e-3,
    "c3_1_d4_0"             :0.02567*1e-3,
    "c3_1_d4_2"             :0.01415*1e-3,
    "c3_2_d4_m1"            :0.0511*1e-3,
    "c3_4_d4_9"             :0.2182*1e-3,
    "c3_m1_d4_0"            :0.1004*1e-3,
    "c3_m1_d4_m1"           :0.09674*1e-3,
    "c3_m1p5_d4_m0p5"       :0.1723*1e-3
}



branch_ratio = 0.5824
year_list = ['2016','2016APV','2017','2018']
sm_sample_list = ["GluGluToHHHTo6B_SM"]
bsm_sample_list = ["HHHTo6B_c3_0_d4_99","HHHTo6B_c3_0_d4_minus1","HHHTo6B_c3_19_d4_19","HHHTo6B_c3_1_d4_0","HHHTo6B_c3_1_d4_2","HHHTo6B_c3_2_d4_minus1","HHHTo6B_c3_4_d4_9","HHHTo6B_c3_minus1_d4_0","HHHTo6B_c3_minus1_d4_minus1","HHHTo6B_c3_minus1p5_d4_minus0p5"]

for proctodo in sm_sample_list:
    total_xs = 0.0
    sample_data = create_sample_data(proctodo, year_list)
    if proctodo == "GluGluToHHHTo6B_SM":
        kappa = "c3_0_d4_0"
    for year in year_list:
        path_for_SM = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)
        path_for_BSM = "/eos/cms/store/group/phys_higgs/cmshhh/v33-additional-samples/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)

        file_in = ROOT.TFile("%s/%s.root"%(path_for_SM,proctodo),"READ")
        tree = file_in.Get("Events")
        first_entry = tree.GetEntry(0)
        xsec_weight = tree.xsecWeight
        
        
        entries_per_year = entries[year][kappa]

        xs_per_year = entries_per_year * xsec_weight
        total_xs = total_xs + xs_per_year

        sample_data[proctodo][year]["Nevents_generated"] = entries_per_year
    xs_theory = yield_table[kappa]
    xs_withbr = 0.0894e-3*5.824e-01*5.824e-01*5.824e-01
    ratio = xs_withbr/total_xs
    for year in year_list:
        sample_data[proctodo][year]["Kfactor"] = 8.94/3.274
        sample_data[proctodo][year]["Nevents_assumed"] =  sample_data[proctodo][year]["Nevents_generated"] * ratio
        sample_data[proctodo][year]["Ratio_correct"] = ratio

        
    data.update(sample_data)

    # print("xs_sum for %s is : %s"%(kappa,total_xs))
    # print("xs for %s is : %s"%(kappa,xs_withbr))
    # print("ratio for %s is : %s"%(kappa,ratio))



for proctodo in bsm_sample_list:
    total_xs = 0.0
    sample_data = create_sample_data(proctodo, year_list)

    if proctodo == "HHHTo6B_c3_0_d4_minus1":
        kappa = "c3_0_d4_m1"
    elif proctodo == "HHHTo6B_c3_19_d4_19":
        kappa = "c3_19_d4_19" 
    elif proctodo == "HHHTo6B_c3_1_d4_0":
        kappa = "c3_1_d4_0"
    elif proctodo == "HHHTo6B_c3_1_d4_2":
        kappa = "c3_1_d4_2" 
    elif proctodo == "HHHTo6B_c3_2_d4_minus1":
        kappa = "c3_2_d4_m1"  
    elif proctodo == "HHHTo6B_c3_4_d4_9":
        kappa = "c3_4_d4_9" 
    elif proctodo == "HHHTo6B_c3_minus1_d4_0":
        kappa = "c3_m1_d4_0"
    elif proctodo == "HHHTo6B_c3_minus1_d4_minus1":
        kappa = "c3_m1_d4_m1"
    elif proctodo == "HHHTo6B_c3_minus1p5_d4_minus0p5":
        kappa = "c3_m1p5_d4_m0p5"
    elif proctodo == "HHHTo6B_c3_0_d4_99":
        kappa = "c3_0_d4_99"
        
    for year in year_list:
        path_for_BSM = "/eos/cms/store/group/phys_higgs/cmshhh/v33-additional-samples/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)

        file_in = ROOT.TFile("%s/%s.root"%(path_for_BSM,proctodo),"READ")
        tree = file_in.Get("Events")
        first_entry = tree.GetEntry(0)
        xsec_weight = tree.xsecWeight
        
        entries_per_year = entries[year][kappa]

        xs_per_year = entries_per_year * xsec_weight
        total_xs = total_xs + xs_per_year
        sample_data[proctodo][year]["Nevents_generated"] = entries_per_year


    xs_theory = yield_table[kappa]
    xs_withbr = xs_theory * branch_ratio * branch_ratio * branch_ratio
    ratio = xs_withbr/total_xs

    for year in year_list:
        sample_data[proctodo][year]["Kfactor"] = 1.0
        sample_data[proctodo][year]["Nevents_assumed"] =  sample_data[proctodo][year]["Nevents_generated"] * ratio
        sample_data[proctodo][year]["Ratio_correct"] = ratio

        
    data.update(sample_data)

    # print("xs_sum for %s is : %s"%(kappa,total_xs))
    # # print("xs for %s is : %s"%(kappa,xs_theory))
    # print("xs for %s is : %s"%(kappa,xs_withbr))
    # print("ratio for %s is : %s"%(kappa,ratio))
with open('output.yaml', 'w') as file:
    yaml.dump(data, file, default_flow_style=False)

print("YAML 文件已生成！")




    