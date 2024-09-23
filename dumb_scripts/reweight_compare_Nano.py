import ROOT

path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD/histograms"
path_r = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD/histograms_0bh3h"
path_plot = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD/plots"

hist_list = ['c3_1_d4_2','c3_2_d4_m1','c3_0_d4_m1','c3_0_d4_99','c3_19_d4_19','c3_1_d4_0','c3_4_d4_9','c3_m1_d4_0','c3_m1_d4_m1','c3_m1p5_d4_m0p5','c3_0_d4_0']
branch_list = ['mhhh','mh1h2','mh1h3']
for hist_name in hist_list:
    file_o = ROOT.TFile("%s/%s_original_widebin.root"%(path,hist_name), "READ")
    # file_r = ROOT.TFile("%s/%s.root"%(path_r,hist_name), "READ")
    file_r = ROOT.TFile("%s/%s_widebin.root"%(path,hist_name), "READ")
    print(file_o)
    print(file_r)
    for br in branch_list:
        hist_o = file_o.Get(br)  
        # hist_r = file_r.Get(f"{br})  
        hist_r = file_r.Get(br)  

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

        hist_o.SetTitle(hist_name)

        hist_o.Draw("HIST") 
        hist_r.Draw("HIST SAME") 

        legend = ROOT.TLegend(0.1, 0.75, 0.3, 0.9)
        legend.AddEntry(hist_o, "madgraph", "l")
        legend.AddEntry(hist_r, "reweight", "l")
        legend.Draw()

        c1.Update()
        c1.Draw()

        # c1.SaveAs("hist_comparison_%s.pdf"%(hist_name))
        c1.SaveAs("%s/comparison_%s_%s.pdf"%(path_plot,hist_name,br))

    file_o.Close()
    file_r.Close()
