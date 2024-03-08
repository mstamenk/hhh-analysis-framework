import ROOT

import os

from utils import hist_properties, drawText

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v33')
parser.add_argument('--year', default='2018')
parser.add_argument('--prob', default='ProbHHH6b')
parser.add_argument('--doCR', action='store_true')
parser.add_argument('--var', default = 'ProbMultiH')

args = parser.parse_args()

prob = args.prob
version = args.version
year = args.year
var = args.var


option = '_SR'
if args.doCR:
    option = '_CR'

first = True
for cat in ['%s_3bh0h_inclusive', '%s_2bh1h_inclusive', '%s_1bh2h_inclusive', '%s_0bh3h_inclusive', '%s_2bh0h_inclusive', '%s_1bh1h_inclusive', '%s_0bh2h_inclusive', '%s_1bh0h_inclusive', '%s_0bh1h_inclusive', '%s_0bh0h_inclusive','%s_3Higgs_inclusive', '%s_2Higgs_inclusive', '%s_1Higgs_inclusive']:
#or cat in ['%s_3Higgs_inclusive']:

    category = cat%prob
    #path = '/isilon/data/users/mstamenk/eos-triple-h/v28-categorisation/mva-inputs-2018-categorisation-spanet-boosted-classification/%s/histograms'%category

    path = '/isilon/data/users/mstamenk/eos-triple-h/%s/mva-inputs-%s-categorisation-spanet-boosted-classification/%s%s/histograms'%(version,year,category,option)

    filename = 'histograms_%s.root'%var

    f = ROOT.TFile(path+'/'+filename)

    n_hhh = 'GluGluToHHHTo6B_SM'

    #if 'ProbHHH4b2tau' in prob:
    #    n_hhh = 'GluGluToHHHTo4B2Tau_SM'
    hhh = f.Get(n_hhh)

    n_hh = 'GluGluToHHTo4B_cHHH1'
    hh = f.Get(n_hh)
    hh.SetDirectory(0)

    n_hhh4b2tau = 'GluGluToHHHTo4B2Tau_SM'
    hhh4b2tau = f.Get(n_hhh4b2tau)

    hh.Scale(15)
    hhh.Scale(1000)
    hhh4b2tau.Scale(1000)


    rebin = 1
    #if '0bh0h' in cat:
    #    rebin = 2

    n_data = 'data_obs'
    data = f.Get(n_data)

    maps = {}
    maps[n_data] = data
    maps[n_hhh] = hhh
    maps[n_hh] = hh

    backgrounds = [str(el.GetName()) for el in f.GetListOfKeys()]
    backgrounds = [el for el in backgrounds if n_hhh not in el and n_data not in el]

    print(backgrounds)


    c = ROOT.TCanvas()
    p1 = ROOT.TPad("c_1","",0,0,1,0.3)
    p2 = ROOT.TPad("c_2","", 0,0.3,1,0.95)
    p1.Draw()
    p2.Draw()
    print("setting pads")
    p1.SetBottomMargin(0.3)
    p1.SetTopMargin(0.05)
    p1.SetRightMargin(0.05)
    p2.SetTopMargin(0.05)
    p2.SetBottomMargin(0.02)
    p2.SetRightMargin(0.05)



    legend = ROOT.TLegend(0.6,0.6,0.9,0.9)
    data.SetStats(0)
    if first:
        hist_properties[n_hhh][3] += ' x 1000 SM'
        hist_properties[n_hh][3] += ' x 15 SM'
        hist_properties[n_hhh4b2tau][3] += 'x 1000 SM'
        first = False


    for el in [n_data, n_hhh, n_hh]:
        h_tmp = maps[el]
        try:
            h_tmp.Rebin(rebin)
        except:
            continue
        properties = hist_properties[el]

        h_tmp.SetLineColor(properties[0])
        h_tmp.SetMarkerColor(properties[0])
        

        h_tmp.SetMarkerSize(properties[1])
        h_tmp.SetLineWidth(properties[2])

        if properties[4]:
            legend.AddEntry(h_tmp,properties[3])


    data.SetMaximum(data.GetMaximum()*2)
    data.SetMinimum(1.0)

    data.SetTitle('')
    data.GetYaxis().SetTitle('Events')
    if 'VV' in category:
        data.GetXaxis().SetTitle('Prob VV')
    else:
        data.GetXaxis().SetTitle('Prob MultiHiggs')
    data.SetMarkerColor(ROOT.kBlack)
    data.SetLineColor(ROOT.kBlack)
    data.SetMarkerSize(100)
    data.SetLineWidth(2)

    bins_x = data.GetXaxis().GetNbins()


    tmp = {}
    h_bkg = ROOT.THStack()

    first = True

    #for el in ['GluGluToHHTo2B2Tau', 'GluGluToHHTo4B_cHHH1','GluGluToHHHTo4B2Tau_SM','DYJetsToLL', 'ZZTo4Q', 'WWTo4Q', 'ZJetsToQQ',  'WJetsToQQ', 'TTToHadronic', 'TTToSemiLeptonic', 'QCD']: #backgrounds:
    for el in ['GluGluToHHTo2B2Tau', 'GluGluToHHTo4B_cHHH1','GluGluToHHHTo4B2Tau_SM','QCD']:
        h_tmp = f.Get(el)
        try:
            h_tmp.Rebin(rebin)
        except: continue
        if first:
            h_unc = h_tmp.Clone('ratio_unc')
            first = False
        else:
            h_unc.Add(h_tmp)

        properties = hist_properties[el]

        h_tmp.SetLineColor(properties[0])
        h_tmp.SetMarkerColor(properties[0])
        h_tmp.SetFillColor(properties[0])

        h_tmp.SetMarkerSize(properties[1])
        h_tmp.SetLineWidth(properties[2])

        if properties[4]:
            if 'QCD' in el:
                legend.AddEntry(h_tmp,'Background model')
            else:
                if '15' in properties[3]:
                    legend.AddEntry(h_tmp,properties[3].replace('x 15 SM',''))
                else:
                    legend.AddEntry(h_tmp,properties[3])
        
            
                
        h_bkg.Add(h_tmp)
        tmp[el] = h_tmp

    print(data.Integral())
    print(h_unc.Integral())
    try:
        print(h_unc.Integral()/data.Integral())
    except: continue
    h_div = data.Clone('div')
    h_div.Divide(h_unc)

    h_div.GetYaxis().SetTitle('Data / MC')

    h_div.GetXaxis().SetTitleSize(0.11)
    h_div.GetXaxis().SetTitleOffset(1.35)
    h_div.GetXaxis().SetLabelSize(0.11)
    h_div.GetXaxis().SetLabelOffset(0.03)
    h_div.GetYaxis().SetTitleSize(0.11)
    h_div.GetYaxis().SetTitleOffset(0.35)
    h_div.GetYaxis().SetLabelSize(0.11)
    h_div.GetYaxis().SetLabelOffset(0.001)
    h_div.GetYaxis().SetMaxDigits(0)
    h_div.GetYaxis().SetNdivisions(4,8,0,ROOT.kTRUE)

    h_div.GetYaxis().SetRangeUser(0.,2.0)


    h_div_unc = h_unc.Clone('unc_error')
    h_div_unc.Divide(h_unc)
    h_div_unc.SetFillColor(ROOT.kBlue)
    h_div_unc.SetFillStyle(3244)




    print("Chi2Test",data.Chi2Test(h_unc, 'UW'))
    print("KS test",data.KolmogorovTest(h_unc))
    
    chi2 = data.Chi2Test(h_unc, 'UW')
    ks = data.KolmogorovTest(h_unc)

    # blinding signal region last 2 bins

    if 'ProbHH4b_2Higgs' in category or 'ProbHHH6b_2Higgs' in category or 'ProbHHH6b_3bh0h' in category or 'ProbHHH6b_2bh1h' in category or 'ProbHHH6b_1bh2h' in category or 'ProbHHH6b_0bh3h' in category or 'ProbHHH6b_2bh0h' in category or 'ProbHHH6b_1bh1h' in category or 'ProbHHH6b_0bh2h' in category or 'ProbHH4b_2bh0h' in category or 'ProbHH4b_1bh1h' in category or 'ProbHH4b_0bh2h' in category or 'ProbHHH6b_3Higgs' in category or 'ProbHHH6b_2Higgs' in category:
    #if 'ProbHHH6b_2Higgs' in category or 'ProbHHH6b_3Higgs' in category:
        data.SetBinContent(bins_x, 0)
        data.SetBinError(bins_x, 0)
        data.SetBinContent(bins_x-1, 0)
        data.SetBinError(bins_x-1, 0.0)

        h_div.SetBinContent(bins_x, -3)
        h_div.SetBinError(bins_x, 0)
        h_div.SetBinContent(bins_x-1, -3)
        h_div.SetBinError(bins_x-1, 0.0)

        #h_unc.SetBinContent(bins_x, 0)
        #h_unc.SetBinError(bins_x, 0)
        #h_unc.SetBinContent(bins_x-1, 0)
        #h_unc.SetBinError(bins_x-1, 0.0)



    s = hh.GetBinContent(bins_x) / 15.
    b = h_unc.GetBinContent(bins_x)
    b_error = h_unc.GetBinError(bins_x)
    n = b
    b = n-s 

    print(n, s,b,b_error)

    #Z = ROOT.TMath.Sqrt( 2 * ( n *  ROOT.TMath.Log( (n * (b + b_error **2 )) / (b**2 + n*b_error**2)) - (b**2)/(b_error**2) * ROOT.TMath.Log( 1 + (b_error**2 * (n-b))/ (b * (b+b_error**2))  )))

    #Z2 = ROOT.TMath.Sqrt( 2 *  ( n *  ROOT.TMath.Log( n / b ) - (n - b)))

    #print(Z, Z2)

    p2.cd()
    #p2.SetLogy()
    data.Draw("e")
    h_bkg.Draw("hist e same")
    hhh.Draw("hist e same")
    hh.Draw("hist e same")
    hhh4b2tau.Draw('hist e same')
    data.Draw("e same")
    legend.Draw()
    drawText(0.2,0.8,category)
    drawText(0.2,0.72,year)
    drawText(0.2,0.64,'KS: %.2f   Chi2: %.2f'%(ks,chi2))
    p1.cd()
    h_div.Draw('e')
    h_div_unc.Draw('e2 same')
    


    c.Print('%s_%s_%s%s_%s.png'%(category,version,year,option,var))


