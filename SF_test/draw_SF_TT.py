import ROOT
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import triggersCorrections

# Define luminosity (in pb^-1)
lumi = 41480.0  
path = "/eos/cms/store/group/phys_higgs/cmshhh/v34-test/SF/2017/ProbTT_inclusive_CR"

char_var = "h1_t3_mass"
nbins = 50
xmin = 0
xmax = 300

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

    # Define the weight expression for MC (ttbar) files

    # For MC (ttbar), we read multiple files and merge them into one RDataFrame
    ttbar_files = [
        # "{}/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root".format(path),
        "{}/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root".format(path),
        # "{}/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.root".format(path),
            # Add other file paths...
    ]

    # Read ttbar files and apply weights
    ttbar_df = ROOT.RDataFrame("Events", ttbar_files)  # Merge multiple files
    ttbar_hist = ttbar_df.Define("SFweight", cutWeight).Histo1D((char_var,char_var,nbins,xmin,xmax),char_var, 'SFweight')

    data_hist = data_hist.GetValue()
    ttbar_hist  = ttbar_hist.GetValue()
    data_hist.SetStats(0)
    ttbar_hist.SetStats(0)
    # Create canvas for plotting
    canvas = ROOT.TCanvas("c1", "Data vs MC", 800, 600)

    # Set marker color for data and line color for ttbar histograms
    data_hist.SetMarkerColor(ROOT.kBlack)  # Use SetMarkerColor for data points
    data_hist.SetMarkerStyle(20)  # Set marker style (e.g., 20 = filled circle)

    ttbar_hist.SetFillColor(ROOT.kYellow)

    ttbar_hist.SetFillStyle(1001)   # Set line color for ttbar histogram

    # Draw data and MC histograms
    data_hist.Draw("E1")  # "E1" draws data with error bars

    ttbar_hist.Draw("HIST SAME ")  # "SAME" ensures ttbar is drawn on top of data


    # Add legend
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(data_hist, "Data", "lep")  # 'lep' for marker in legend (data is points)

    legend.AddEntry(ttbar_hist, "ttbar MC", "l")   # 'l' for line in legend (ttbar is histogram)
    legend.Draw()

 

    # Save the plot as a PDF file
    canvas.SaveAs("SF_ttbar_h1_t3_mass_%s_hadro.pdf"%(type))
