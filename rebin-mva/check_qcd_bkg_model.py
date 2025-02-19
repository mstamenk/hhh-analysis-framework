# Script to check the QCD modelling via MC with the background model

import os, ROOT


year = '2018'

prob = 'ProbHHH6b'

for year in ['2016APV201620172018']:
    for prob in ['ProbHHH6b','ProbHH4b']:
        for cat in ['%s_3bh0h_inclusive','%s_2bh1h_inclusive','%s_1bh2h_inclusive','%s_0bh3h_inclusive','%s_2bh0h_inclusive','%s_1bh1h_inclusive','%s_0bh2h_inclusive','%s_1bh0h_inclusive','%s_0bh1h_inclusive','%s_0bh0h_inclusive','%s_2Higgs_inclusive','%s_1Higgs_inclusive','%s_3Higgs_inclusive']:
            category = cat%prob + '_CR'

            path = '/isilon/data/users/mstamenk/eos-triple-h/v33/mva-inputs-%s-categorisation-spanet-boosted-classification/%s'%(year,category)

            f_in = 'histograms_ProbMultiH_test'

            f = ROOT.TFile(path + '/histograms/' + f_in + '.root')

            h_qcd = f.Get("QCD")

            h_model = f.Get("QCD_mc")


            h_qcd.SetLineColor(ROOT.kRed)
            h_qcd.SetLineWidth(2)

            h_qcd.GetXaxis().SetTitle('ProbMultiH 10 bins')
            h_qcd.GetYaxis().SetTitle('Normalised')
            h_qcd.SetTitle(category)

            h_qcd.SetStats(0)

            h_model.SetLineColor(ROOT.kBlue+2)
            h_model.SetLineWidth(2)
            try:
                h_qcd.Scale(1./h_qcd.Integral())
                h_model.Scale(1./h_model.Integral())
            except: continue
            h_qcd.SetMaximum(h_qcd.GetMaximum()*2)

            c = ROOT.TCanvas()
            legend = ROOT.TLegend(0.6,0.6,0.89,0.89)
            legend.SetBorderSize(0)
            legend.SetFillColor(0)

            legend.AddEntry(h_qcd,'QCD MC')
            legend.AddEntry(h_model,'BKG model on QCD')

            h_qcd.Draw("hist e")
            h_model.Draw("hist e same")
            legend.Draw()

            c.Print("plots-qcd/%s_%s_comparison.png"%(category,year))