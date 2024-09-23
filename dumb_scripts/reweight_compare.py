import ROOT

path_o = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v33/run2/ProbHHH6b_3Higgs_inclusive_CR/histograms"
path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_11_3_4/src/datacards_maker_hhh/teste_datacards/v33/kappa_reweight/HHH_only"
file_o = ROOT.TFile("%s/histograms_kappa_scale.root"%(path_o), "READ")
file_r = ROOT.TFile("%s/histograms_3Higgs_reweight_shape_only.root"%(path_r), "READ")
# file_r = ROOT.TFile("%s/histograms_3Higgs_reweight.root"%(path_r), "READ")

hist_list = ['c3_1_d4_2','c3_2_d4_m1','c3_0_d4_m1','c3_0_d4_99','c3_19_d4_19','c3_1_d4_0','c3_4_d4_9','c3_m1_d4_0','c3_m1_d4_m1','c3_m1p5_d4_m0p5','c3_0_d4_0']
for hist_name in hist_list:
    hist_o = file_o.Get(hist_name)  
    hist_r = file_r.Get(hist_name)  

    if not hist_o:
        print("Error: Could not find histogram in file_o.")
    if not hist_r:
        print("Error: Could not find histogram in file_r.")


    c1 = ROOT.TCanvas("c1", "Comparison of Histograms", 800, 600)

    hist_o.SetLineColor(ROOT.kRed)  
    hist_r.SetLineColor(ROOT.kBlue)  

    all_max = max(hist_o.GetMaximum(),hist_r.GetMaximum())
    all_min = min(hist_o.GetMinimum(),hist_r.GetMinimum())

    hist_o.SetMaximum(all_max * 1.1) 
    hist_o.SetMinimum(all_min * 0.9)
    hist_o.SetStats(False)

    hist_o.Draw("HIST") 
    hist_r.Draw("HIST SAME") 

    legend = ROOT.TLegend(0.1, 0.75, 0.3, 0.9)
    legend.AddEntry(hist_o, "madgraph", "l")
    legend.AddEntry(hist_r, "reweight", "l")
    legend.Draw()

    c1.Update()
    c1.Draw()

    # c1.SaveAs("hist_comparison_%s.pdf"%(hist_name))
    c1.SaveAs("hist_comparison_%s_shape_only.pdf"%(hist_name))

file_o.Close()
file_r.Close()
