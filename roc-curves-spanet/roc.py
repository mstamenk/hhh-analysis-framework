import os, ROOT, glob

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.EnableImplicitMT()
from array import array

from utils import histograms_dict, drawText, addLabel_CMS_preliminary, luminosities


typename = 'spanet-boosted-classification-variables-pnet-v15'
path = '/isilon/data/users/mstamenk/eos-triple-h/samples-v28-2018-%s-nanoaod/'%(typename)

outname = '%s.root'%(typename)
outfile = ROOT.TFile(outname,'recreate')


samples = glob.glob(path+ '*.root')
samples = [os.path.basename(s).replace('.root','') for s in samples]
samples = [s for s in samples if 'GluGlu' not in s]
samples = [s for s in samples if 'JetHT' not in s]



outfile = ROOT.TFile(typename+'.root','recreate')

signal = 'GluGluToHHHTo6B_SM'
bkg = 'QCD'
print(samples)
for signal in ['GluGluToHHHTo6B_SM','GluGluToHHTo4B_cHHH1']:
    for bkg in ['QCD']:#samples:

        df_sig = ROOT.RDataFrame('Events', path + '/' + signal + '.root')
        df_bkg = ROOT.RDataFrame('Events', path + '/' + bkg + '.root')

        df_sig = df_sig.Filter('nprobejets > 0')
        df_bkg = df_bkg.Filter('nprobejets > 0')

        df_sig = df_sig.Define('ProbMultiH','ProbHHH + ProbHHH4b2tau + ProbHH2b2tau + ProbHH4b')
        df_bkg = df_bkg.Define('ProbMultiH','ProbHHH + ProbHHH4b2tau + ProbHH2b2tau + ProbHH4b')

        sig_tot = df_sig.Count().GetValue()
        bkg_tot = df_bkg.Count().GetValue()

        print(sig_tot,bkg_tot)

        x = array( 'd' )
        y = array( 'd' )

        n = 200
        for i in range(n):
            cut = 'ProbMultiH > %f'%(i * 0.005)
            x_tmp = df_sig.Filter(cut).Count().GetValue()
            y_tmp = df_bkg.Filter(cut).Count().GetValue()

            print(cut, x_tmp / float(sig_tot), y_tmp / float(bkg_tot))
            x.append(x_tmp / float(sig_tot))
            y.append(1-y_tmp / float(bkg_tot))

        gr = ROOT.TGraph( n, x, y )

        c1 = ROOT.TCanvas()

        gr.SetLineColor( 2 )
        gr.SetLineWidth( 2 )
        #gr.SetMarkerColor( 4 )
        #gr.SetMarkerStyle( 21 )
        gr.GetXaxis().SetTitle( 'HHH6b efficiency' )
        gr.GetYaxis().SetTitle( '%s 1 - efficiency'%bkg )
        gr.Draw( 'ACP' )
        c1.Update()
        #c1.GetFrame().SetFillColor( 21 )
        c1.GetFrame().SetBorderSize( 12 )
        c1.Modified()
        c1.Update()
        c1.Print('roc.png')

        name = '%s_%s'%(signal,bkg)
        gr.SetTitle(name)
        gr.SetName(name)
        outfile.cd()
        gr.Write()
outfile.Close()