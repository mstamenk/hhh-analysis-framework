import os, ROOT, glob
import ctypes
import argparse

ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v33_new')
parser.add_argument('--year', default='2018')
parser.add_argument('--prob', default='ProbHHH6b')
parser.add_argument('--path_year', default='2017')
parser.add_argument('--var', default = 'ProbMultiH')
parser.add_argument('--doSyst', action = 'store_true')
args = parser.parse_args()

# Custom bin configuration: category -> (bin_width, x_cut)
custom_bin_config = {
    'ProbHHH6b_1bh2h_inclusive': (0.0015, 0.9970),
    'ProbHHH6b_0bh3h_inclusive': (0.0015, 0.9980),
    'ProbHHH6b_3bh0h_inclusive': (0.0020, 0.9965),
    'ProbHHH6b_2bh1h_inclusive': (0.0018, 0.9972),
    'ProbHHH6b_2bh0h_inclusive': (0.0016, 0.9968),
    'ProbHHH6b_1bh1h_inclusive': (0.0017, 0.9971),
    'ProbHHH6b_0bh2h_inclusive': (0.0015, 0.9975),
    'ProbHHH6b_1Higgs_inclusive': (0.0016, 0.9960),
    'ProbHHH6b_0bh0h_inclusive': (0.0017, 0.9967),
}

# Build binning dictionaries for ROOT histograms
binnings = {}
def convert_list_to_dict(ls):
    ret = {}
    for i in range(len(ls) - 1):
        ret[i + 1] = [ls[i], ls[i + 1]]
    return ret

for cat, (bin_width, x_cut) in custom_bin_config.items():
    bin_edges = [1.0 - i * bin_width for i in range(10)]
    bin_edges = [x for x in bin_edges if x >= x_cut]
    bin_edges.append(1.0)
    bin_edges = sorted(set(bin_edges))
    binnings[cat] = convert_list_to_dict(bin_edges)

# Set ROOT variable used for histogramming
variables = {k: 'ProbMultiH' for k in custom_bin_config.keys()}

# Apply default category cut
categories = {k: '(nprobejets > -1)' for k in custom_bin_config.keys()}

# ROOT utils

def get_integral_and_error(hist):
    integral = hist.Integral()
    error = ctypes.c_double(0.0)
    hist.IntegralAndError(0, hist.GetNbinsX() + 1, error)
    return integral, error.value

# Path setup
path = f'/eos/cms/store/group/phys_higgs/cmshhh/v34-test/add_TTHH_{args.version}/{args.path_year}'

# Loop categories
for cat in custom_bin_config:
    print(f"Processing: {cat}")
    target = f'{cat}_CR/histograms'
    os.makedirs(f'{path}/{target}', exist_ok=True)
    file_path = f'{cat}_CR'

    samples = glob.glob(f'{path}/{file_path}/*.root')
    samples = [os.path.basename(s).replace('.root','') for s in samples]
    var = args.var
    binning = binnings[cat]
    cut = categories[cat]
    outfile = ROOT.TFile(f'{path}/{target}/histograms_{var}.root', 'recreate')

    # Process all samples except signal/QCD
    for s in samples:
        if 'GluGlu' in s or 'QCD' in s: continue
        tree = ROOT.TChain('Events')
        tree.AddFile(f'{path}/{file_path}/{s}.root')
        h_mva = ROOT.TH1F(s, s, len(binning), 0, len(binning))

        for i in range(1, len(binning) + 1):
            low, up = binning[i]
            h_name = f'{s}_histo_{i}'
            draw_expr = f'({cut} && {var} > {low} && {var} < {up}) * eventWeight'
            tree.Draw(f'{var}>>{h_name}(100,0,1)', draw_expr)
            h = ROOT.gPad.GetPrimitive(h_name)
            if h:
                integral, error = get_integral_and_error(h)
                h_mva.SetBinContent(i, integral)
                h_mva.SetBinError(i, error)
        outfile.cd()
        h_mva.Write()

    # Process QCD
    tree = ROOT.TChain('Events')
    tree.AddFile(f'{path}/{file_path}/QCD_datadriven.root')
    h_mva = ROOT.TH1F('QCD', 'QCD', len(binning), 0, len(binning))

    for i in range(1, len(binning) + 1):
        low, up = binning[i]
        h_name = f'QCD_histo_{i}'
        draw_expr = f'({cut} && {var} > {low} && {var} < {up}) * eventWeight'
        tree.Draw(f'{var}>>{h_name}(100,0,1)', draw_expr)
        h = ROOT.gPad.GetPrimitive(h_name)
        if h:
            integral, error = get_integral_and_error(h)
            h_mva.SetBinContent(i, integral)
            h_mva.SetBinError(i, error)

    h_mva.Write()
    outfile.Close()
    print(f"Saved histograms to: {path}/{target}/histograms_{var}.root")
