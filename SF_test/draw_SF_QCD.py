import ROOT
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import triggersCorrections

# Define luminosity (in pb^-1)
lumi = 41480.0  
path = "/eos/cms/store/group/phys_higgs/cmshhh/v34-test/SF/2017/ProbQCD_inclusive_CR"

char_var = "ProbMultiH"
nbins = 50
xmin = 0
xmax = 1

type_list = ['all','AK4','AK8']
for type in type_list:
    if type == 'all':
        cutWeight = '(%f * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF * fatJetFlavTagWeight * flavTagWeight)' % lumi

    elif type == 'AK4':
        cutWeight = '(%f * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF  * flavTagWeight)' % lumi

    elif type == 'AK8':
        cutWeight = '(%f * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF * fatJetFlavTagWeight )' % lumi

    # Create RDataFrame to read the ROOT data file
    data_df = ROOT.RDataFrame("Events", "%s/data_obs.root"%(path))

    # For data, set the weight to 1
    data_hist = data_df.Define("SFweight", "1.0").Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'SFweight')

    # Define the weight expression for MC (QCD) files

    # For MC (QCD), we read multiple files and merge them into one RDataFrame
    qcd_files = [
        "{}/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8.root".format(path),
        "{}/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8.root".format(path),
        "{}/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8.root".format(path),
        "{}/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8.root".format(path),
        "{}/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8.root".format(path),
        "{}/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8.root".format(path),
        "{}/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8.root".format(path),
            # Add other file paths...
    ]

    # Read QCD files and apply weights
    qcd_df = ROOT.RDataFrame("Events", qcd_files)  # Merge multiple files
    qcd_hist = qcd_df.Define("SFweight", cutWeight).Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'SFweight')

    data_hist = data_hist.GetValue()
    qcd_hist  = qcd_hist.GetValue()
    data_hist.SetStats(0)
    qcd_hist.SetStats(0)
    # Create canvas for plotting
    canvas = ROOT.TCanvas("c1", "Data vs MC", 800, 600)

    # Set marker color for data and line color for QCD histograms
    data_hist.SetMarkerColor(ROOT.kBlack)  # Use SetMarkerColor for data points
    data_hist.SetMarkerStyle(20)  # Set marker style (e.g., 20 = filled circle)

    qcd_hist.SetFillColor(ROOT.kYellow)

    qcd_hist.SetFillStyle(1001)   # Set line color for QCD histogram

    # Draw data and MC histograms
    qcd_hist.Draw("HIST ")  # "SAME" ensures QCD is drawn on top of data

    data_hist.Draw("E1 SAME")  # "E1" draws data with error bars

    # Add legend
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(data_hist, "Data", "lep")  # 'lep' for marker in legend (data is points)

    legend.AddEntry(qcd_hist, "QCD MC", "l")   # 'l' for line in legend (QCD is histogram)
    legend.Draw()

    # Update and draw the canvas
    canvas.Update()
    canvas.Draw()

    # Save the plot as a PDF file
    canvas.SaveAs("SF_QCD_%s.pdf"%(type))
