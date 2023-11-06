# Scritp to rebin mva inputs
import ROOT,os

ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)

year = '2018'
#path = '/isilon/data/users/mstamenk/eos-triple-h/v27-spanet-boosted-classification-variables/mva-inputs-%s/inclusive_boosted-weights'%year
path = '/isilon/data/users/mstamenk/eos-triple-h/v28-spanet-boosted-classification-variables-pnet-v4-nanoaod/mva-inputs-%s/inclusive_boosted-weights'%year

signal = ROOT.TChain('Events')
#signal.AddFile(path + '/' + 'GluGluToHHHTo6B_SM.root')
#signal.AddFile(path + '/' + 'GluGluToHHHTo4B2Tau_SM.root')
signal.AddFile(path + '/' + 'GluGluToHHTo4B_cHHH1.root')
#signal.AddFile(path + '/' + 'GluGluToHHTo2B2Tau.root')

background = ROOT.TChain('Events')
#background.AddFile(path + '/' + 'QCD_bEnriched.root')
#background.AddFile(path + '/' + 'QCD.root')
#background.AddFile(path + '/' + 'TTTo2L2Nu.root')
#background.AddFile(path + '/' + 'TTToHadronic.root')
#background.AddFile(path + '/' + 'TTToSemiLeptonic.root')
#background.AddFile(path + '/' + 'WJetsToQQ.root')
#background.AddFile(path + '/' + 'WWTo4Q.root')
#background.AddFile(path + '/' + 'WWW.root')
#background.AddFile(path + '/' + 'WWZ.root')
#background.AddFile(path + '/' + 'WZZ.root')
#background.AddFile(path + '/' + 'ZJetsToQQ.root')
#background.AddFile(path + '/' + 'ZZTo4Q.root')
#background.AddFile(path + '/' + 'ZZZ.root')
#background.AddFile(path + '/' + 'DYJetsToLL.root')
background.AddFile(path + '/' + 'JetHT.root')

cut_baseline = '(nprobejets == 1 && ((ProbHHH + ProbHHH4b2tau) < (ProbHH4b + ProbHH2b2tau))) * eventWeight'
bins = '(10,0,1)'

var = '(ProbHHH + ProbHHH4b2tau + ProbHH4b + ProbHH2b2tau)'


h_sig = 'h_signal'
signal.Draw("%s>>%s%s"%(var,h_sig,bins),cut_baseline)
h_s = ROOT.gPad.GetPrimitive(h_sig)

h_bkg = 'h_background'
background.Draw("%s>>%s%s"%(var,h_bkg,bins),cut_baseline)
h_b = ROOT.gPad.GetPrimitive(h_bkg)

h_s.SetLineColor(ROOT.kRed)
h_b.SetLineColor(ROOT.kBlue)

c = ROOT.TCanvas()
c.SetLogy()
h_b.Draw('hist e')
h_s.Draw('hist e same')


bkg_threshold = 15.0
firstBin = True

sig_yield = 0

cuts = [1.0]

upper_cut = 1.0



for i in range(1,2000):
    cut_value = 1.0 - 0.0003 * i 
    print(cut_value,upper_cut)
    h_sig = 'h_signal_%.2f'%cut_value

    cut = '(%s > %f && %s < %f && %s) * eventWeight'%(var,cut_value,var,upper_cut, cut_baseline)
    signal.Draw("%s>>%s%s"%(var,h_sig,bins),cut)
    h_s = ROOT.gPad.GetPrimitive(h_sig)

    h_bkg = 'h_background_%.2f'%cut_value
    background.Draw("%s>>%s%s"%(var,h_bkg,bins),cut)
    h_b = ROOT.gPad.GetPrimitive(h_bkg)

    yield_s = h_s.Integral() 
    yield_b = h_b.Integral()
    print(yield_s,yield_b)

    #if yield_b > bkg_threshold and firstBin: 
    if yield_s > 1 and firstBin: 
        print(cut_value, yield_s, yield_b)
        cuts.append(cut_value)
        sig_yield = yield_s
        upper_cut = cut_value
        firstBin = False

    if not firstBin:
        if yield_s > sig_yield:
            cuts.append(cut_value)
            upper_cut = cut_value
            print(cut_value, yield_s, yield_b)
    if len(cuts) > 11: break



print(cuts)







