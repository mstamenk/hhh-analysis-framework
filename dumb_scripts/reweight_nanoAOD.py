import sympy as sp
import ROOT
import uproot
import numpy as np
import matplotlib.pyplot as plt
from array import array

k4, k3 = sp.symbols('k4 k3')



reweight = {'c3_0_d4_m1'     : '0.01*k4**2 + 0.318534528202425*k4*k3**2 - 1.31853452820243*k4*k3 - 0.01*k4 - 0.00404182041820418*k3**4 - 0.188269021261641*k3**3 + 0.274565278509927*k3**2 + 0.917745563169917*k3',
            'c3_0_d4_99'   : '0.000101010101010101*k4**2 - 5.45252205768805e-5*k4*k3**2 + 5.45252205768828e-5*k4*k3 - 0.000101010101010101*k4 + 2.65881446693261e-6*k3**4 - 9.21000551997246e-6*k3**3 + 6.35435358682633e-5*k3**2 - 5.69923448152232e-5*k3',
            'c3_19_d4_19'   : '-2.03879412444105e-22*k4**2 - 1.52595510917515e-5*k4*k3**2 + 1.52595510917515e-5*k4*k3 + 2.03879412444105e-22*k4 + 7.76849873761895e-6*k3**4 - 1.63693366256971e-5*k3**3 + 9.98806980551009e-6*k3**2 - 1.38723191743197e-6*k3',
            'c3_1_d4_0'     : '8.35090073371053e-19*k4**2 - 0.118871903004744*k4*k3**2 + 0.118871903004744*k4*k3 - 8.35090073371053e-19*k4 - 0.00615006150061501*k3**4 + 0.239149534352486*k3**3 - 0.0555262695484097*k3**2 - 0.177473203303462*k3',
            'c3_4_d4_9'    : '2.60965647928454e-20*k4**2 + 0.00648392198207696*k4*k3**2 - 0.00648392198207697*k4*k3 - 2.60965647928454e-20*k4 - 0.00027060270602706*k3**4 - 0.000620277631347738*k3**3 - 0.00272887014584432*k3**2 + 0.00361975048321911*k3',
            'c3_m1_d4_0'     : '6.68072058696843e-18*k4**2 + 0.0208223510806536*k4*k3**2 - 1.02082235108065*k4*k3 + 1.0*k4 - 0.0287822878228783*k3**4 + 0.667791249341065*k3**3 - 1.3227200843437*k3**2 + 0.683711122825514*k3',
            'c3_m1_d4_m1'     : '-6.68072058696843e-18*k4**2 - 0.341776489193463*k4*k3**2 + 1.34177648919346*k4*k3 - 1.0*k4 - 0.00782287822878225*k3**4 + 0.487912493410648*k3**3 - 1.067200843437*k3**2 - 0.41288877174486*k3 + 1.0',
            'c3_m1p5_d4_m0p5': '8.35090073371053e-19*k4**2 + 0.151818661043753*k4*k3**2 - 0.151818661043753*k4*k3 - 8.35090073371053e-19*k4 + 0.019680196801968*k3**4 - 0.612897557547004*k3**3 + 1.54911263398348*k3**2 - 0.955895273238447*k3',
            'c3_0_d4_0'     : '-0.0101010101010101*k4**2 - 0.0369412853390325*k4*k3**2 + 1.03694128533903*k4*k3 + 0.0101010101010101*k4 + 0.0273770265613342*k3**4 - 0.593040841322061*k3**3 + 0.624424623375876*k3**2 - 0.058760808615149*k3'
}

yield_table = {
    "c3_0_d4_0"             : "0.03274*1e-3",
    "c3_0_d4_99"            : "5.243*1e-3",
    "c3_0_d4_m1"            : "0.03624*1e-3",
    "c3_19_d4_19"           : "131.8*1e-3",
    "c3_1_d4_0"             : "0.02567*1e-3",
    "c3_1_d4_2"             : "0.01415*1e-3",
    "c3_2_d4_m1"            : "0.0511*1e-3",
    "c3_4_d4_9"             : "0.2182*1e-3",
    "c3_m1_d4_0"            : "0.1004*1e-3",
    "c3_m1_d4_m1"           : "0.09674*1e-3",
    "c3_m1p5_d4_m0p5"       : "0.1723*1e-3"
}

kappa_list = {'c3_m14_d4_m101' : {'k3': -13, 'k4': -100},
              'c3_m11_d4_m51'   : {'k3': -10, 'k4': -50},
              'c3_m5_d4_m21'   : {'k3': -4, 'k4': -20},
              'c3_m6_d4_m31'    : {'k3': -5, 'k4': -30},
              'c3_2_d4_59'     : {'k3': 3, 'k4': 60},
              'c3_7_d4_49'     : {'k3': 8, 'k4': 50},
              'c3_8_d4_99'    : {'k3': 9, 'k4': 100},
              'c3_16_d4_33'   : {'k3': 17, 'k4': 34},
              'c3_1_d4_2'      : {'k3': 2, 'k4': 3},
              'c3_2_d4_3'     : {'k3': 3, 'k4': 4},
              'c3_2_d4_m1'     : {'k3': 3, 'k4': 0},
              'c3_0_d4_m1'    : {'k3': 1, 'k4': 0},
              'c3_0_d4_99'    : {'k3': 1, 'k4': 100},
              'c3_19_d4_19'    : {'k3': 20, 'k4': 20},
              'c3_1_d4_0'    : {'k3': 2, 'k4': 1},
              'c3_4_d4_9'    : {'k3': 5, 'k4': 10},
              'c3_m1_d4_0'    : {'k3': 0, 'k4': 1},
              'c3_m1_d4_m1'    : {'k3': 0, 'k4': 0},
              'c3_m1p5_d4_m0p5': {'k3': -0.5, 'k4': 0.5},
              'c3_0_d4_0': {'k3': 1, 'k4': 1}
            
}

path_for_sample = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD"
output_path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD/histograms"

xmin = 0
xmax = 1200
nbins = 12

branch_names = ["mhhh","mh1h2","mh1h3"]
for new_kappa_name, values in kappa_list.items():
    k3 = values['k3']
    k4 = values['k4']
    output_file = ROOT.TFile(f"{output_path}/{new_kappa_name}_widebin.root", "RECREATE")
    for branch_name in branch_names:
        
        h_total = ROOT.TH1D(f"h_{branch_name}", f"Weighted Histogram for {branch_name}", nbins, xmin, xmax)
        
        for basis_kappa_name in reweight:
            
            df = ROOT.RDataFrame('features', f"{path_for_sample}/{basis_kappa_name}.root")
            total_entries = df.Count().GetValue()
            kappa_weight =  eval(reweight[basis_kappa_name])
            xs = eval(yield_table[basis_kappa_name])
            lumi = 1.0
            total_weight_value = kappa_weight * xs * lumi /total_entries
            print(total_weight_value)
            df = df.Define("totalWeight", f"{total_weight_value}")

            h_tmp = df.Histo1D((branch_name, branch_name, nbins, xmin, xmax), branch_name, "totalWeight")
            h_total.Add(h_tmp.GetPtr())  

        output_file.cd()
        h_total.Write()

    output_file.Close()
    print(f"aleady saved {new_kappa_name}")

        # c = ROOT.TCanvas(f"c_{branch_name}", f"Canvas for {branch_name}", 800, 600)
        # h_total.Draw("hist")
        # c.SaveAs(f"{branch_name}_weighted_histogram.png")  # 保存图像为文件










