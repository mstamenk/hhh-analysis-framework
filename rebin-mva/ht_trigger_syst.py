import ROOT, os

def load_ht_histogram(year, base_dir="./trigger-correction/"):
    filename = os.path.join(base_dir, f"{year}_ht_correction.root")
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        raise RuntimeError(f"Could not open {filename}")
    h = f.Get("correction")
    if not h:
        raise RuntimeError("No 'correction' histo in %s" % filename)
    h.SetDirectory(0)
    f.Close()
    return h

def declare_ht_syst_weights(hist, ht_col="ht", weight_col="totalWeight"):
    n_bins = hist.GetNbinsX()
    edges = [hist.GetBinLowEdge(i+1) for i in range(n_bins)] + \
            [hist.GetBinLowEdge(n_bins) + hist.GetBinWidth(n_bins)]
    vals  = [hist.GetBinContent(i+1)    for i in range(n_bins)]

    # turn them into C‐style arrays
    cpp_edges    = "{" + ",".join(f"{e:.5f}" for e in edges) + "}"
    cpp_contents = "{" + ",".join(f"{v:.5f}" for v in vals)  + "}"

    # declare a GLOBAL function getHTCorr(double)
    ROOT.gInterpreter.Declare(f"""
    static double getHTCorr(double ht) {{
        static const double edges[{len(edges)}] = {cpp_edges};
        static const double vals[{len(vals)}]  = {cpp_contents};
        const int   n = {len(vals)};
        for(int i=0; i<n; ++i) {{
            if (ht >= edges[i] && ht < edges[i+1]) return vals[i];
        }}
        return 1.0;
    }}
    """)

    return {
        "HTUp":   f"{weight_col} * getHTCorr({ht_col})",
        "HTDown": f"{weight_col} / getHTCorr({ht_col})"
    }