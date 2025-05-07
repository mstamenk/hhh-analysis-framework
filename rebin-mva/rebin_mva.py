# Scritp to rebin mva inputs
import ROOT,os

from array import array 
import ctypes


def get_integral_and_error(hist):
    integral = hist.Integral()
    error = ctypes.c_double(0.0)
    hist.IntegralAndError(0, hist.GetNbinsX() + 1, error)
    return integral, error.value

ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)

year = '2018'
category = 'ProbHHH6b_3Higgs_inclusive_SR'
#path = '/isilon/data/users/mstamenk/eos-triple-h/v27-spanet-boosted-classification-variables/mva-inputs-%s/inclusive_boosted-weights'%year
#path = '/isilon/data/users/mstamenk/eos-triple-h/v28-categorisation/mva-inputs-%s-categorisation-spanet-boosted-classification/%s'%(year,category)
path = '/isilon/data/users/mstamenk/eos-triple-h/v31/mva-inputs-%s-categorisation-spanet-boosted-classification/%s'%(year,category)


signal = ROOT.TChain('Events')
signal.AddFile(path + '/' + 'GluGluToHHHTo6B_SM.root')
#signal.AddFile(path + '/' + 'GluGluToHHHTo4B2Tau_SM.root')
#signal.AddFile(path + '/' + 'GluGluToHHTo4B_cHHH1.root')
#signal.AddFile(path + '/' + 'GluGluToHHTo2B2Tau.root')

#signal.AddFile(path + '/' + 'ZZTo4Q.root')
#signal.AddFile(path + '/' + 'WWTo4Q.root')

background = ROOT.TChain('Events')
#background.AddFile(path + '/' + 'QCD_bEnriched.root')
background.AddFile(path + '/' + 'QCD.root')
#background.AddFile(path + '/' + 'QCD_modelling.root')
background.AddFile(path + '/' + 'TTTo2L2Nu.root')
background.AddFile(path + '/' + 'TTToHadronic.root')
background.AddFile(path + '/' + 'TTToSemiLeptonic.root')
background.AddFile(path + '/' + 'WJetsToQQ.root')
background.AddFile(path + '/' + 'WWTo4Q.root')
background.AddFile(path + '/' + 'WWW.root')
background.AddFile(path + '/' + 'WWZ.root')
background.AddFile(path + '/' + 'WZZ.root')
background.AddFile(path + '/' + 'ZJetsToQQ.root')
background.AddFile(path + '/' + 'ZZTo4Q.root')
background.AddFile(path + '/' + 'ZZZ.root')
background.AddFile(path + '/' + 'DYJetsToLL.root')
#background.AddFile(path + '/' + 'JetHT.root')
#background.AddFile(path + '/' + 'data_obs.root')


cut_baseline = '(nprobejets > -1) * totalWeight'
bins = '(10,0,1)'

var = '(ProbMultiH)'
#var = 'ProbHH4b'

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


bkg_threshold = 3.0
firstBin = True

sig_yield = 0

cuts = [1.0]
yields = []

upper_cut = 1.0



for i in range(1,300):
    cut_value = 1.0 - 0.001 * i 
    print(cut_value,upper_cut)
    h_sig = 'h_signal_%.2f'%cut_value

    cut = '(%s > %f && %s < %f && %s) * totalWeight'%(var,cut_value,var,upper_cut, cut_baseline)
    signal.Draw("%s>>%s%s"%(var,h_sig,bins),cut)
    h_s = ROOT.gPad.GetPrimitive(h_sig)

    h_bkg = 'h_background_%.2f'%cut_value
    background.Draw("%s>>%s%s"%(var,h_bkg,bins),cut)
    h_b = ROOT.gPad.GetPrimitive(h_bkg)

    
    yield_s, error_s = get_integral_and_error(h_s)
    yield_b, error_b = get_integral_and_error(h_b)
    print(yield_s,yield_b, error_b)


    #if yield_b > bkg_threshold and firstBin: 
    #if yield_s > 1. and firstBin:
    #if yield_b < 0.0001 : continue 
    if yield_b < 0.0001 : continue
    if yield_b > 1 and error_b / yield_b < 0.01:
        print(cut_value, yield_s, yield_b)
        cuts.append(cut_value)
        sig_yield = yield_s 
        upper_cut = cut_value
        firstBin = False
        yields.append([yield_s,yield_b])

    if not firstBin:
        #if yield_s > sig_yield:
        if error_b / yield_b < 0.2:
            cuts.append(cut_value)
            upper_cut = cut_value
            print(cut_value, yield_s, yield_b)
            yields.append([yield_s,yield_b])
    if len(cuts) > 20: break


print(category)
print(cuts)
print(yields)







