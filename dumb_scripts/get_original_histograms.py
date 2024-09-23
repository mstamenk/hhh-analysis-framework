import sympy as sp
import ROOT
import uproot
import numpy as np
import matplotlib.pyplot as plt
from array import array

k4, k3 = sp.symbols('k4 k3')



reweight = {'c3_19_d4_19'   : '9.06091847289793e-6*k3**4 - 4.9300725444354e-5*k3**3 - 1.28986682294749e-5*k3**2*k4 + 7.41895333895021e-5*k3**2 + 4.88255754744921e-5*k3*k4 - 2.35068699375642e-5*k3 + 1.04428564804817e-7*k4**2 - 4.64741922903036e-5*k4',
            'c3_1_d4_2'     : '0.00181859908941073*k3**4 + 0.0612344145588463*k3**3 - 0.117052946187404*k3**2*k4 - 0.0852248165990747*k3**2 + 0.495450856752831*k3*k4 - 0.34453745664648*k3 - 0.00366709259597299*k4**2 - 0.00802155837215495*k4',
            'c3_0_d4_0'     : '-0.0156567767640078*k3**4 + 0.296450661053703*k3**3 + 0.116113507117289*k3**2*k4 - 1.17541762393027*k3**2 - 0.943320520412559*k3*k4 + 1.28092989493571*k3 - 0.00623794854805879*k4**2 + 1.4471388065482*k4',
            'c3_2_d4_m1'     : '-0.00432741529694681*k3**4 + 0.134315219432959*k3**3 - 0.0348180673391588*k3**2*k4 - 0.254218287446726*k3**2 - 0.0121776760133018*k3*k4 + 0.00399143379444837*k3 - 0.00120239049516266*k4**2 + 0.16843718336389*k4',
            'c3_m1_d4_m1'     : '0.00269506107191331*k3**4 + 0.0869752273166167*k3**3 - 0.173807100320902*k3**2*k4 - 0.32776033936777*k3**2 + 1.06104582179224*k3*k4 - 0.205596010021244*k3 + 0.00556313938999517*k4**2 - 1.44911579986085*k4 + 1.0',
            'c3_m1p5_d4_m0p5': '0.00178625756289069*k3**4 - 0.128966102905578*k3**3 + 0.0878144535538641*k3**2*k4 + 0.614548792715285*k3**2 - 0.499940475718061*k3*k4 - 0.7311804061937*k3 - 0.00243811458821102*k4**2 + 0.65837559557351*k4',
            'c3_0_d4_99'   : '3.54406639377261e-6*k3**4 - 8.23419233486239e-5*k3**3 + 3.68602946798598e-6*k3**2*k4 + 0.000190060163750484*k3**2 - 0.000133213138375878*k3*k4 + 7.52070262542428e-5*k3 + 0.0001028747943406*k4**2 - 0.000159817018482608*k4',
            'c3_4_d4_9'    : '-0.000544382627375349*k3**4 + 0.00482523670822783*k3**3 + 0.00769645658563427*k3**2*k4 - 0.0138311282893779*k3**2 - 0.0199714878689513*k3*k4 + 0.0127645854332177*k3 + 3.21431122469228e-5*k4**2 + 0.00902857694637784*k4',
            'c3_1_d4_0'     : '0.0142160519792486*k3**4 - 0.454703013515982*k3**3 + 0.114062909229438*k3**2*k4 + 1.2416391532208*k3**2 - 0.0810021309692927*k3*k4 - 0.0164237414582671*k3 + 0.00784728450225797*k4**2 - 0.825636512988201*k4'
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



path_for_sample = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD"
output_path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD/histograms"

xmin = 0
xmax = 1200
nbins = 12

branch_names = ["mhhh","mh1h2","mh1h3"]
    
    
    
for basis_kappa_name in yield_table:
    output_file = ROOT.TFile(f"{output_path}/{basis_kappa_name}_original_widebin.root", "RECREATE")
    for branch_name in branch_names:
        
        # h_total = ROOT.TH1D(f"h_{branch_name}", f"Weighted Histogram for {branch_name}", nbins, xmin, xmax)
        
    
        df = ROOT.RDataFrame('features', f"{path_for_sample}/{basis_kappa_name}.root")
        total_entries = df.Count().GetValue()
        xs = eval(yield_table[basis_kappa_name])
        lumi = 1.0
        total_weight_value =  xs * lumi /total_entries
        print(total_weight_value)
        df = df.Define("totalWeight", f"{total_weight_value}")

        h_original = df.Histo1D((branch_name, branch_name, nbins, xmin, xmax), branch_name, "totalWeight")

        output_file.cd()
        h_original.Write()

    output_file.Close()
    print(f"aleady saved {basis_kappa_name}")

        # c = ROOT.TCanvas(f"c_{branch_name}", f"Canvas for {branch_name}", 800, 600)
        # h_total.Draw("hist")
        # c.SaveAs(f"{branch_name}_weighted_histogram.png")  # 保存图像为文件










