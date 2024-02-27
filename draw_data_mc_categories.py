# Script to plot data / mc from processed files

import os
from utils import histograms_dict, hist_properties, addLabel_CMS_preliminary, luminosities

import ROOT

#ROOT.PyConfig.IgnoreCommandLineOptions = True
#ROOT.gROOT.CloseFiles()
#ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2000;")
#ROOT.gROOT.SetMustClean(True)
ROOT.gStyle.SetOptStat("0")
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.ROOT.EnableImplicitMT()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--input_folder", type="string", dest="input_folder", help="Folder in where to look for the categories", default='/eos/user/m/mstamenk/CxAOD31run/hhh-6b/v25/2017/baseline_recomputedSF/')
parser.add_option("--output_folder", type="string", dest="output_folder", help="Folder in where to look for the categories", default='none')
parser.add_option("--log", action="store_true", dest="log", help="Write...", default=False)
parser.add_option("--save_pdf", action="store_true", dest="save_pdf", help="Write...", default=False)
parser.add_option("--plot_label", type="string", dest="plot_label", help="Text to add on top left of the plot", default='none')


(options, args) = parser.parse_args()

input_folder = options.input_folder
do_log       = options.log
save_pdf     = options.save_pdf
plot_label   = options.plot_label


# change into one liner....
output_folder=options.output_folder
if output_folder == "none" :
    output_folder = input_folder

for era in ['2016APV', '2016', '2017', '2018', '2022', '2022EE'] :
    if era in input_folder : year = era

labels = addLabel_CMS_preliminary(luminosities[year])

iPeriod = 0
datahist   = 'data_obs'
signalhist = 'GluGluToHHHTo6B_SM'
signalhist2 = 'GluGluToHHTo4B_cHHH1'
inputTree = 'Events'

if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

file_data   = "{}/{}.root".format(input_folder, datahist)
file_signal = "{}/{}.root".format(input_folder, signalhist)
file_signal2 = "{}/{}.root".format(input_folder, signalhist2)



chunk_data   = ROOT.RDataFrame(inputTree, file_data)
chunk_signal = ROOT.RDataFrame(inputTree, file_signal)
chunk_signal2 = ROOT.RDataFrame(inputTree, file_signal2)
variables = chunk_data.GetColumnNames()
variables = ROOT.std.vector['string'](['fatJet1Mass','mvaBoosted','h1_spanet_boosted_mass','h2_spanet_boosted_mass','h3_spanet_boosted_mass','ProbHHH','ProbMultiH','ProbHH4b','ProbHHH4b2tau','ProbVV'])

#file_data = ROOT.TFile(input_folder + '/' + 'histograms_%s.root'%(datahist))
#variables = [v.GetName() for v in file_data.GetListOfKeys()]
#file_data.Close()

if do_log :
    scale_sig = 1000.0
    scale_sig2 = 15
    ypos     = 0.095
else :
    scale_sig = 1000.0
    scale_sig2 = 15
    ypos     = 0.9

for var in variables:
    canvas = ROOT.TCanvas()
    canvas.SetCanvasSize(600, 700)
    #c.SetBorderMode(0)
    #c.SetTopMargin(0.5)
    p1 = ROOT.TPad("c_1","",0,0,1,0.3)
    p2 = ROOT.TPad("c_2","", 0,0.3,1,0.95)

    #if "Resolved" in plot_label and "fatJet" in var :
    #    continue

    try :
        histograms_dict[var]
    except :
        print("Will skip draw %s, if you want to draw the should be added in utils" % var)
        continue

    xpos = 0.05*(histograms_dict[var]["xmax"]-histograms_dict[var]["xmin"])

    try :
        binining = histograms_dict[var]
    except :
        print("Skip drawing %s, if you want to draw add the binning option in utils" % var)
        continue

    template = ROOT.TH1F("", "", histograms_dict[var]["nbins"], histograms_dict[var]["xmin"], histograms_dict[var]["xmax"])
    nbins = histograms_dict[var]["nbins"]
    xmin = histograms_dict[var]["xmin"]
    xmax = histograms_dict[var]["xmax"]
    char_var = var.c_str()
    #file_data = ROOT.TFile(input_folder + '/' + 'histograms_%s.root'%(datahist))
    #file_signal = ROOT.TFile(input_folder + '/' + 'histograms_%s.root'%('GluGluToHHHTo6B_SM'))

    files_bkg = {}
    for bkg in ['DYJetsToLL','GluGluToHHTo2B2Tau','ZZZ','WWW','WZZ','ZZTo4Q', 'WWTo4Q', 'WWTo4Q','ZJetsToQQ', 'WJetsToQQ', 'TTToHadronic','TTToSemiLeptonic','QCD','QCD_bEnriched']:
        #f_tmp = ROOT.TFile(input_folder + '/' + 'histograms_%s.root'%bkg)
        f_tmp = "{}/{}.root".format(input_folder, bkg)
        if os.path.exists(f_tmp) :
            files_bkg[bkg] = f_tmp

    legend = ROOT.TLegend(0.62,0.65,.95,0.9)
    legend.SetBorderSize(0)

    #h_data = template.Clone()
    #h_data = chunk_data.Fill(template, [char_var])
    h_data = chunk_data.Histo1D((char_var,char_var,nbins,xmin,xmax),char_var)
    h_data.Draw()
    h_data = h_data.GetValue()
    h_data.SetTitle(hist_properties[datahist][3])
    h_data.SetName(hist_properties[datahist][3])
    #h_data = file_data.Get(var)
    h_data.SetMarkerColor(ROOT.kBlack)
    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerSize(100)
    h_data.SetLineWidth(2)
    h_data.SetStats(0)
    h_data.GetXaxis().SetTitle(histograms_dict[var]["label"])
    h_data.SetTitle('')
    legend.AddEntry( h_data, h_data.GetName())

    if do_log :
        ymax      = 1000000.0*h_data.GetMaximum()
    else :
        ymax      = 2.0*h_data.GetMaximum()

    # blinding
    if 'mass' in str(var) or 'Mass' in str(var):
        for mass_value in [110,120,130]:
            bin_m = h_data.FindBin(mass_value)
            h_data.SetBinContent(bin_m,-100000.0000001)
            h_data.SetBinError(bin_m,-100000.0)

    if 'bdt' in str(var) or 'mva' in str(var):
        blind_bdt = [x*0.01 + 0.5 for x in range(20)]
        for value in blind_bdt:
            bin_blind = h_data.FindBin(value)
            h_data.SetBinContent(bin_blind,-3.0000001)
            h_data.SetBinError(bin_blind,0)

    if 'ProbHHH' in str(var) or 'ProbMultiH' in str(var):
        blind_bdt = [x*0.001 + 0.95 for x in range(1000)]
        for value in blind_bdt:
            bin_blind = h_data.FindBin(value)
            h_data.SetBinContent(bin_blind,-10000.0000001)
            h_data.SetBinError(bin_blind,0)



    #h_signal = template.Clone()
    #h_signal = chunk_signal.Fill(template, [char_var, 'totalWeight'])
    h_signal = chunk_signal.Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'totalWeight')
    h_signal.Draw()
    h_signal = h_signal.GetValue()

    h_signal2 = chunk_signal2.Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'totalWeight')
    h_signal2.Draw()
    h_signal2 = h_signal2.GetValue()
    #h_signal = file_signal.Get(var)
    h_signal.SetDirectory(0)
    h_signal.SetMarkerColor(hist_properties[signalhist][0])
    h_signal.SetLineColor(hist_properties[signalhist][0])
    h_signal.SetMarkerSize(hist_properties[signalhist][1])
    h_signal.SetLineWidth(hist_properties[signalhist][2])

    h_signal2.SetMarkerColor(hist_properties[signalhist2][0])
    h_signal2.SetLineColor(hist_properties[signalhist2][0])
    h_signal2.SetMarkerSize(hist_properties[signalhist2][1])
    h_signal2.SetLineWidth(hist_properties[signalhist2][2])


    h_signal.Scale(scale_sig)
    h_signal2.Scale(scale_sig2)

    label_sig = hist_properties[signalhist][3]
    if not scale_sig == 1.0 :
        label_sig =  "%s (X %s)" % (label_sig, str(scale_sig))

    label_sig2 = hist_properties[signalhist2][3]
    if not scale_sig2 == 1.0 :
        label_sig2 =  "%s (X %s)" % (label_sig2, str(scale_sig2))
    #legend.AddEntry(h_signal, label_sig, 'l')
    legend.AddEntry(h_signal, label_sig, 'l')
    legend.AddEntry(h_signal2, label_sig2, 'l')

    h_stack = ROOT.THStack()

    #h_bkg = ROOT.TH1F(var+"bkg", var+"bkg", h_data.GetXaxis().GetNbins(), h_data.GetXaxis().GetXmin(), h_data.GetXaxis().GetXmax())
    h_bkg = template.Clone()
    h_bkg.SetTitle('%s_bkg'%(var))
    h_bkg.SetName('%s_bkg'%(var))

    histograms_bkg = {} # need to save histograms outside of for loop other wise seg fault

    for bkg in files_bkg:

        f_tmp = ROOT.TFile(files_bkg[bkg])
        if 'Events' not in f_tmp.GetListOfKeys():
            f_tmp.Close()
            continue
        f_tmp.Close()
        chunk_bkg   = ROOT.RDataFrame(inputTree, files_bkg[bkg])
        print(inputTree, files_bkg[bkg])
        #h_tmp       = chunk_bkg.Fill(template, [char_var, 'totalWeight'])
        h_tmp = chunk_bkg.Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'totalWeight')
        h_tmp = h_tmp.GetValue()
        histograms_bkg[bkg ] = h_tmp

        try:
            h_tmp.SetDirectory(0)
        except:
            continue

        h_tmp.Draw()

        h_bkg.Add(h_tmp)

        h_tmp.SetFillColor(hist_properties[bkg][0])
        h_tmp.SetMarkerSize(hist_properties[bkg][1])
        if hist_properties[bkg][4]:
            legend.AddEntry(h_tmp, hist_properties[bkg][3], 'f')
        print("adding to stack", bkg)
        h_stack.Add(h_tmp)

    maxi = max(h_data.GetMaximum(), h_bkg.GetMaximum())

    h_data.SetMaximum(1.5*maxi)

    print("doing histo to divide")
    h_div = h_data.Clone(var+'_ratio')
    h_div.Divide(h_bkg)

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

    h_div.GetYaxis().SetRangeUser(-1.0,3.)

    h_mc_stat = h_bkg.Clone(h_bkg.GetName()+'_mcstat')
    h_mc_stat.Divide(h_bkg)
    h_mc_stat.SetFillColor(ROOT.kBlue)
    h_mc_stat.SetFillStyle(3244)

    h_data.GetXaxis().SetLabelOffset(999)
    h_data.GetXaxis().SetLabelSize(0)
    print("opening canvas")
    canvas.cd()
    print("drawing pads")
    p1.Draw()
    p2.Draw()
    print("setting pads")
    p1.SetBottomMargin(0.3)
    p1.SetTopMargin(0.05)
    p1.SetRightMargin(0.05)
    p2.SetTopMargin(0.05)
    p2.SetBottomMargin(0.02)
    p2.SetRightMargin(0.05)

    h_data.SetMinimum(0.0001)
    h_data.SetMaximum(ymax)

    print("opening pads")
    p2.cd()
    if do_log :
        p2.SetLogy()

    print("drawing histograms in upper  pads")
    h_data.Draw('e')
    h_stack.Draw('hist e same')
    h_signal.Draw('hist e same')
    h_signal2.Draw('hist e same')
    h_data.Draw('e same')
    legend.Draw()

    print("adding text")
    plot_label_tpave = ROOT.TText(xpos , ypos*ymax, plot_label)
    plot_label_tpave.SetTextAlign(11)
    plot_label_tpave.SetTextSize(0.04)
    plot_label_tpave.Draw()

    for ll, label in enumerate(labels):
        label.Draw("same")

    # plot_label
    print("drawing histograms in down  pads")

    p1.cd()
    p1.SetGridy()
    h_div.Draw('e')
    h_mc_stat.Draw('e2 same')
    #canvas.cd()
    print("drawing histograms in down  pads done")

    plot_file = "%s/%s" % (output_folder,str(var))
    if save_pdf :
        canvas.Print("%s%s" % (plot_file, '.pdf') ) # save PDF only when we need to add to docs
    canvas.Print("%s%s" % (plot_file, '.png'))

    print("did %s" % plot_file)

