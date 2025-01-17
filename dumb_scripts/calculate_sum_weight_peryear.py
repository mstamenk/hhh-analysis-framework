import sympy as sp
import ROOT
import numpy as np
import matplotlib.pyplot as plt


entries = {
    '2016': {
        'c3_0_d4_99': 184000.0,
        'c3_0_d4_0': 4292992.0,
        'c3_0_d4_m1': 184000.0,
        'c3_19_d4_19': 181285.0,
        'c3_1_d4_0': 584000.0,
        'c3_1_d4_2': 184000.0,
        'c3_2_d4_m1': 184000.0,
        'c3_4_d4_9': 184000.0,
        'c3_m1_d4_0': 183080.0,
        'c3_m1_d4_m1': 184000.0,
        'c3_m1p5_d4_m0p5': 184000.0,
        'ggHH_kl_0_kt_1':449692.0,
        'ggHH_kl_1_kt_1':460000.0,
        'ggHH_kl_5_kt_1':460000.0
    },
    '2016APV': {
        'c3_0_d4_99': 216000.0,
        'c3_0_d4_0': 4936877.0,
        'c3_0_d4_m1': 216000.0,
        'c3_19_d4_19': 216000.0,
        'c3_1_d4_0': 216000.0,
        'c3_1_d4_2': 211445.0,
        'c3_2_d4_m1': 215079.0,
        'c3_4_d4_9': 216000.0,
        'c3_m1_d4_0': 216000.0,
        'c3_m1_d4_m1': 216000.0,
        'c3_m1p5_d4_m0p5': 216000.0,
        'ggHH_kl_0_kt_1':540000.0,
        'ggHH_kl_1_kt_1':540000.0,
        'ggHH_kl_5_kt_1':539182.0
    },
    '2017': {
        'c3_0_d4_99': 398000.0,
        'c3_0_d4_0': 3824239.0,
        'c3_0_d4_m1': 390000.0,
        'c3_19_d4_19': 382000.0,
        'c3_1_d4_0': 400000.0,
        'c3_1_d4_2': 381000.0,
        'c3_2_d4_m1': 383000.0,
        'c3_4_d4_9': 372000.0,
        'c3_m1_d4_0': 400000.0,
        'c3_m1_d4_m1': 399000.0,
        'c3_m1p5_d4_m0p5': 372000.0,
        'ggHH_kl_0_kt_1':997000.0,
        'ggHH_kl_1_kt_1':997197.0,
        'ggHH_kl_5_kt_1':992000.0
    },
    '2018': {
        'c3_0_d4_99': 396000.0,
        'c3_0_d4_0': 7460957.0,
        'c3_0_d4_m1': 387000.0,
        'c3_19_d4_19': 399000.0,
        'c3_1_d4_0': 398000.0,
        'c3_1_d4_2': 393000.0,
        'c3_2_d4_m1': 400000.0,
        'c3_4_d4_9': 398000.0,
        'c3_m1_d4_0': 399000.0,
        'c3_m1_d4_m1': 399000.0,
        'c3_m1p5_d4_m0p5': 397000.0,
        'ggHH_kl_0_kt_1':978000.0,
        'ggHH_kl_1_kt_1':999277.0,
        'ggHH_kl_5_kt_1':994000.0

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
    "c3_m1p5_d4_m0p5"       :0.1723*1e-3,
    "ggHH_kl_0_kt_1"        :69.7*1e-3,
    "ggHH_kl_1_kt_1"        :31.05*1e-3,
    "ggHH_kl_5_kt_1"        :91.7*1e-3,
}

# ggHHto4B_13TeV           31.05e-3*5.824e-01*5.824e-01
# ggHHto4B_13TeV_cHHH0     69.7e-3*5.824e-01*5.824e-01
# ggHHto4B_13TeV_cHHH2p45  13.15e-3*5.824e-01*5.824e-01
# ggHHto4B_13TeV_cHHH5     91.7e-3*5.824e-01*5.824e-01



branch_ratio = 0.5824
year_list = ['2016','2016APV','2017','2018']
sm_sample_list = ["GluGluToHHHTo6B_SM"]
bsm_sample_list = ["HHHTo6B_c3_0_d4_99","HHHTo6B_c3_0_d4_minus1","HHHTo6B_c3_19_d4_19","HHHTo6B_c3_1_d4_0","HHHTo6B_c3_1_d4_2","HHHTo6B_c3_2_d4_minus1","HHHTo6B_c3_4_d4_9","HHHTo6B_c3_minus1_d4_0","HHHTo6B_c3_minus1_d4_minus1","HHHTo6B_c3_minus1p5_d4_minus0p5"]
hh4B_sample_list = ["GluGluToHHTo4B_cHHH0","GluGluToHHTo4B_cHHH1","GluGluToHHTo4B_cHHH5"]
hh4B_powheg_list = ["powheg%s_bbbb_kl_0p00","powheg%s_bbbb_kl_1p0","powheg%s_bbbb_kl_5p00"]

for proctodo in sm_sample_list:
    total_xs = 0.0
    if proctodo == "GluGluToHHHTo6B_SM":
        kappa = "c3_0_d4_0"
    for year in year_list:
        path_for_SM = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)
        path_for_BSM = "/eos/cms/store/group/phys_higgs/cmshhh/v33-additional-samples/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)
        path_for_4B = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)

        file_in = ROOT.TFile("%s/%s.root"%(path_for_SM,proctodo),"READ")
        tree = file_in.Get("Events")
        first_entry = tree.GetEntry(0)
        xsec_weight = tree.xsecWeight
        
        
        entries_per_year = entries[year][kappa]
        print("xsec_weight for %s (%s) is : %s"%(kappa,year,xsec_weight))
        print("entries (nanoAOD) for %s (%s) is : %s"%(kappa,year,entries_per_year))

        xs_per_year = entries_per_year * xsec_weight
        # total_xs = total_xs + xs_per_year
        xs_theory = yield_table[kappa]
        # xs_withbr = xs_theory * 2.74 * branch_ratio * branch_ratio * branch_ratio
        xs_withbr = 0.0894e-3*5.824e-01*5.824e-01*5.824e-01
        # xs_withbr = xs_theory * branch_ratio * branch_ratio * branch_ratio
        # ratio = total_xs/xs_theory
        ratio = xs_per_year/xs_withbr
    # print(ratio)

        # print("xs(%s) for %s is : %s"%(year,kappa,xs_per_year))
        # # print("xs for %s is : %s"%(kappa,xs_theory))
        # print("xs for %s is : %s"%(kappa,xs_withbr))
        print("ratio(%s)for %s is : %s"%(year,kappa,ratio))



# for proctodo in bsm_sample_list:
#     total_xs = 0.0
#     if proctodo == "HHHTo6B_c3_0_d4_minus1":
#         kappa = "c3_0_d4_m1"
#     elif proctodo == "HHHTo6B_c3_19_d4_19":
#         kappa = "c3_19_d4_19" 
#     elif proctodo == "HHHTo6B_c3_1_d4_0":
#         kappa = "c3_1_d4_0"
#     elif proctodo == "HHHTo6B_c3_1_d4_2":
#         kappa = "c3_1_d4_2" 
#     elif proctodo == "HHHTo6B_c3_2_d4_minus1":
#         kappa = "c3_2_d4_m1"  
#     elif proctodo == "HHHTo6B_c3_4_d4_9":
#         kappa = "c3_4_d4_9" 
#     elif proctodo == "HHHTo6B_c3_minus1_d4_0":
#         kappa = "c3_m1_d4_0"
#     elif proctodo == "HHHTo6B_c3_minus1_d4_minus1":
#         kappa = "c3_m1_d4_m1"
#     elif proctodo == "HHHTo6B_c3_minus1p5_d4_minus0p5":
#         kappa = "c3_m1p5_d4_m0p5"
#     elif proctodo == "HHHTo6B_c3_0_d4_99":
#         kappa = "c3_0_d4_99"
        
#     for year in year_list:
#         path_for_BSM = "/eos/cms/store/group/phys_higgs/cmshhh/v33-additional-samples/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)

#         file_in = ROOT.TFile("%s/%s.root"%(path_for_BSM,proctodo),"READ")
#         tree = file_in.Get("Events")
#         first_entry = tree.GetEntry(0)
#         xsec_weight = tree.xsecWeight
#         # print(year)
#         # print(xsec_weight)
        
#         entries_per_year = entries[year][kappa]
#         # print(year)
#         # print(kappa)
#         # print(xsec_weight)
#         # print(entries_per_year)
#         print("xsec_weight for %s (%s) is : %s"%(kappa,year,xsec_weight))
#         print("entries (nanoAOD) for %s (%s) is : %s"%(kappa,year,entries_per_year))

#         xs_per_year = entries_per_year * xsec_weight
#         # total_xs = total_xs + xs_per_year
#         # print(xs_per_year)

#         xs_theory = yield_table[kappa]
#         xs_withbr = xs_theory * branch_ratio * branch_ratio * branch_ratio
#         # ratio = total_xs/xs_theory
#         ratio = xs_per_year/xs_withbr
#         # print(ratio)

#         # print("xs(%s) for %s is : %s"%(year,kappa,xs_per_year))
#         # # print("xs for %s is : %s"%(kappa,xs_theory))
#         # print("xs for %s is : %s"%(kappa,xs_withbr))
#         print("ratio(%s) for %s is : %s"%(year,kappa,ratio))
for proctodo in hh4B_powheg_list:
# for proctodo in hh4B_sample_list:

    total_xs = 0.0
    # if proctodo == "GluGluToHHTo4B_cHHH0":
    #     kappa = "ggHH_kl_0_kt_1"
    # elif proctodo == "GluGluToHHTo4B_cHHH1":
    #     kappa = "ggHH_kl_1_kt_1" 
    # elif proctodo == "GluGluToHHTo4B_cHHH5":
    #     kappa = "ggHH_kl_5_kt_1"

    if proctodo == "powheg%s_bbbb_kl_0p00":
        kappa = "ggHH_kl_0_kt_1"
    elif proctodo == "powheg%s_bbbb_kl_1p0":
        kappa = "ggHH_kl_1_kt_1" 
    elif proctodo == "powheg%s_bbbb_kl_5p00":
        kappa = "ggHH_kl_5_kt_1"

    for year in year_list:
        # path_for_4B = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)
        path_fot_4B = "/eos/cms/store/group/phys_higgs/cmshhh/v33-additional-samples/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights"%(year)
        file_in = ROOT.TFile("%s/%s.root"%(path_for_4B, proctodo%year),"READ")
        # file_in = ROOT.TFile("%s/%s.root"%(path_for_4B,proctodo),"READ")
        tree = file_in.Get("Events")
        first_entry = tree.GetEntry(0)
        xsec_weight = tree.xsecWeight
        # print(year)
        # print(xsec_weight)
        
        entries_per_year = entries[year][kappa]
        # print(year)
        # print(kappa)
        # print(xsec_weight)
        # print(entries_per_year)
        print("xsec_weight for %s (%s) is : %s"%(kappa,year,xsec_weight))
        print("entries (nanoAOD) for %s (%s) is : %s"%(kappa,year,entries_per_year))

        xs_per_year = entries_per_year * xsec_weight
        # total_xs = total_xs + xs_per_year
        # print(xs_per_year)

        xs_theory = yield_table[kappa]
        xs_withbr = xs_theory * branch_ratio * branch_ratio 
        # ratio = total_xs/xs_theory
        ratio = xs_per_year/xs_withbr
        # print(ratio)

        # print("xs(%s) for %s is : %s"%(year,kappa,xs_per_year))
        # # print("xs for %s is : %s"%(kappa,xs_theory))
        # print("xs for %s is : %s"%(kappa,xs_withbr))
        print("ratio(%s) for %s is : %s"%(year,kappa,ratio))
    



    