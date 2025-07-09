# Script to add JME systematics

import ROOT

# ROOT in batch mode (in case used interactively)
ROOT.gROOT.SetBatch(True)

# Define samples for which JME uncertainties should be applied
samples_with_jme = {
    'GluGluToHHTo4B_cHHH2p45',
    'GluGluToHHTo4B_cHHH5',
    'HHHTo6B_c3_0_d4_minus1',
    'HHHTo6B_c3_19_d4_19',
    'HHHTo4B2Tau_c3_0_d4_0',
    'GluGluToHHTo2B2Tau',
    'HHHTo6B_c3_1_d4_2',
    'HHHTo6B_c3_minus1_d4_minus1',
    'HHHTo6B_c3_0_d4_99',
    'HHHTo6B_c3_2_d4_minus1',
    'HHHTo6B_c3_minus1p5_d4_minus0p5',
    'GluGluToHHHTo6B_SM',
    'GluGluToHHTo4B_cHHH1',
    'HHHTo6B_c3_1_d4_0',
    'HHHTo6B_c3_minus1_d4_0',
    'HHHTo6B_c3_4_d4_9_',
    'GluGluToHHTo4B_cHHH0',
}

def apply_jme_variations(h_nominal, sample, cat,year,variation, binning_dict, verbose=False):
    """
    Apply JME systematic variations using ratio histograms.

    Parameters:
        h_nominal     : ROOT.TH1 histogram with yields rebinned in MVA bins
        sample        : Sample name used to load histogram/{sample}.root
        variation     : 'JESUP', 'JERUP', etc.
        binning_dict  : Dictionary mapping bin index -> [low, high] MVA score range
        verbose       : If True, prints debug output

    Returns:
        (h_up, h_down): ROOT.TH1 histograms with variation applied
    """
    if sample not in samples_with_jme:
        if verbose:
            print(f"[JME] Skipping {variation} for sample {sample}")
        return None, None

    ratio_path = f"jme-systematics/{sample}_{cat.replace('_inclusive','')}_{year}.root"
    ratio_file = ROOT.TFile.Open(ratio_path)
    if not ratio_file or ratio_file.IsZombie():
        raise RuntimeError(f"[JME] Cannot open file: {ratio_path}")

    ratio_hist = ratio_file.Get(f"ratio_{variation}")
    if not ratio_hist:
        raise KeyError(f"[JME] Histogram 'ratio_{variation}' not found in {ratio_path}")

    var = variation.replace("UP","")
    h_up = h_nominal.Clone(f"{h_nominal.GetName()}_{var}_Up")
    h_up.SetDirectory(0)
    h_down = h_nominal.Clone(f"{h_nominal.GetName()}_{var}_Down")
    h_down.SetDirectory(0)

    for i in range(1, h_nominal.GetNbinsX() + 1):
        val = h_nominal.GetBinContent(i)
        err = h_nominal.GetBinError(i)

        if i not in binning_dict:
            print(f"[Warning] Bin {i} not found in binning_dict, skipping")
            continue

        low, high = binning_dict[i]
        score_center = 0.5 * (low + high)
        ratio = ratio_hist.GetBinContent(ratio_hist.FindBin(score_center))

        h_up.SetBinContent(i, val * ratio)
        h_up.SetBinError(i, err * ratio)

        h_down.SetBinContent(i, val * (2.0 - ratio))
        h_down.SetBinError(i, err * abs(2.0 - ratio))

    ratio_file.Close()
    return h_up, h_down