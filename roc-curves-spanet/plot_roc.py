import ROOT


f = ROOT.TFile('spanet-boosted-classification-variables-pnet-v4.root')
f_2 = ROOT.TFile('spanet-boosted-classification-variables-pnet-v15.root')

gr = f.Get('GluGluToHHHTo6B_SM_QCD')
gr_2 = f_2.Get('GluGluToHHHTo6B_SM_QCD')


gr.SetLineColor(ROOT.kRed)
gr_2.SetLineColor(ROOT.kGreen)

c = ROOT.TCanvas()
legend = ROOT.TLegend(0.43,0.64,0.94,0.92)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

legend.AddEntry(gr,'v4')
legend.AddEntry(gr_2,'v15')

gr.Draw('acp')
gr_2.Draw('cp same')
legend.Draw()
c.Print('roc_comp.png')