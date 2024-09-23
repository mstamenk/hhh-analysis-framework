import uproot
import pandas as pd
import numpy as np


year_list  = ['2018','2017','2016','2016APV']
sample_list = ["HHHTo6B_c3_0_d4_99", 
               "HHHTo6B_c3_0_d4_minus1", 
               "HHHTo6B_c3_19_d4_19", 
               "HHHTo6B_c3_1_d4_0", 
               "HHHTo6B_c3_1_d4_2", 
               "HHHTo6B_c3_2_d4_minus1", 
               "HHHTo6B_c3_4_d4_9", 
               "HHHTo6B_c3_minus1_d4_0", 
               "HHHTo6B_c3_minus1_d4_minus1", 
               "HHHTo6B_c3_minus1p5_d4_minus0p5"]

for year in year_list:
    print(year)
    for sample in sample_list: 
        sample_for_kappa = '/eos/cms/store/group/phys_higgs/cmshhh/v33-additional-samples/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights/%s.root'%(year,sample)
        kappa_xs = uproot.open("%s:Events"%(sample_for_kappa)).arrays(["xsecWeight"], library='pd')
        print(sample)
        a = np.unique(kappa_xs)
        print(a)


    sample_for_SM = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-%s-categorisation-spanet-boosted-classification/inclusive-weights/GluGluToHHHTo6B_SM.root"%year
    kappa_SM = uproot.open("%s:Events"%(sample_for_SM)).arrays(["xsecWeight"], library='pd')
    print("GluGluToHHHTo6B_SM")
    b = np.unique(kappa_SM)
    print(b)
