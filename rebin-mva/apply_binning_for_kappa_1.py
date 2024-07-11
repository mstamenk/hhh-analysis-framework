import os, ROOT,glob

import ctypes
from utils import histograms_dict, wps_years, wps, tags, luminosities, hlt_paths, triggersCorrections, hist_properties, init_mhhh, addMHHH, clean_variables, initialise_df, save_variables, init_get_max_prob, init_get_max_cat

# Test : nAK4 >= 6 and nprobejets >= 2 [1.0, 0.9971, 0.9944, 0.9904, 0.9831, 0.9695, 0.9458] 
# nAK4 < 6 nprobejets >= 2: [1.0, 0.9969, 0.9938, 0.9876, 0.9741, 0.9394, 0.8229]
# nAK4 >= 6 nprobejets == 1: [1.0, 0.9988, 0.9983, 0.9979, 0.9976, 0.9973, 0.997, 0.9967, 0.9964, 0.9961, 0.9957, 0.9954, 0.9952, 0.995, 0.9948, 0.9945, 0.9942, 0.9939, 0.9936, 0.9933, 0.9931, 0.9927, 0.9923, 0.992, 0.9916, 0.9913, 0.9909, 0.9905, 0.9902, 0.9899, 0.9895, 0.989, 0.9886, 0.9882, 0.9878, 0.9874, 0.9869, 0.9863999999999999, 0.986, 0.9855, 0.9851, 0.9846, 0.9841, 0.9835, 0.983, 0.9826, 0.9822, 0.9817, 0.9812, 0.9806, 0.9801, 0.9795, 0.9791, 0.9786, 0.9781, 0.9776, 0.977, 0.9763, 0.9758, 0.975, 0.9745, 0.9738, 0.9732, 0.9726, 0.9718, 0.9712, 0.9705, 0.9701, 0.9694, 0.9687, 0.9682, 0.9676, 0.9668, 0.966, 0.9654, 0.9646, 0.9638, 0.9631, 0.9621999999999999, 0.9614, 0.9606, 0.9599, 0.9591, 0.9581999999999999, 0.9572, 0.9564, 0.9556, 0.9544, 0.9536, 0.9528, 0.9521, 0.951, 0.9501, 0.9491, 0.9478, 0.9468, 0.9458, 0.9451, 0.9440999999999999, 0.943, 0.9423, 0.9414, 0.9405, 0.9396, 0.9383, 0.9371, 0.9359, 0.935, 0.9338, 0.9323, 0.9312, 0.9301, 0.9284, 0.927, 0.9258, 0.9251, 0.9238999999999999, 0.9224, 0.9215, 0.9207, 0.9191, 0.9174, 0.9165, 0.9149, 0.9136, 0.9124, 0.9113, 0.9096, 0.9077999999999999, 0.906, 0.9045, 0.9033, 0.9015, 0.8997999999999999, 0.8984, 0.8966, 0.8946, 0.8931, 0.8916, 0.8901, 0.8887, 0.8874, 0.8855999999999999, 0.8838, 0.8819, 0.8805, 0.8783, 0.8764, 0.8748, 0.8731, 0.8713, 0.8693, 0.8675999999999999, 0.8658, 0.8633, 0.8613, 0.8599, 0.8569, 0.8547, 0.8527, 0.8506, 0.849, 0.847, 0.8447, 0.8429, 0.8406, 0.8386, 0.8368, 0.8344, 0.8329, 0.8308, 0.8285, 0.8261000000000001, 0.8243, 0.8224, 0.8199, 0.8171999999999999, 0.8153, 0.8122, 0.8089999999999999, 0.8069, 0.8042, 0.802]
# nAK4 < 6  nprobejets == 1: [1.0, 0.9957, 0.9928, 0.9894, 0.9848, 0.9786, 0.9714, 0.9624, 0.9513, 0.9392, 0.9248, 0.9087, 0.8908, 0.8709, 0.8466, 0.8167]

ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v31')
parser.add_argument('--year', default='2017')
parser.add_argument('--prob', default='ProbHH4b')
args = parser.parse_args()

def convert_list_to_dict(ls):
    length = len(ls)
    ret = {}
    for i in range(length):
        index = length - (i + 1)
        if i > 0:
            upper = ls[index]
            lower = ls[index+1]
            print(lower,upper)
            ret[i] = [lower,upper]
    return ret

opt_bins = {'2018': 0.699, 
            '2017': 0.699,
            '2016': 0.673,
            '2016APV': 0.673,
}

opt_bins_split = {'2018': {'3bh0h' : 0.613,
                           '2bh1h' : 0.676,
                           '1bh2h' : 0.682,
                           '0bh3h' : 0.698,
                            },
                  '2017': {'3bh0h' : 0.613,
                           '2bh1h' : 0.651,
                           '1bh2h' : 0.658,
                           '0bh3h' : 0.679,
                            },
                  '2016': {'3bh0h' : 0.613,
                           '2bh1h' : 0.593,
                           '1bh2h' : 0.611,
                           '0bh3h' : 0.647,
                            },
                  '2016APV': {'3bh0h' : 0.613,
                           '2bh1h' : 0.598,
                           '1bh2h' : 0.613,
                           '0bh3h' : 0.646,
                            },
}


year = args.year
version = args.version

#bins_ProbHH4b_2Higgs = [1.0, 0.942, 0.91, 0.901, 0.879, 0.862, 0.844, 0.8240000000000001,0.808, 0.8049999999999999, 0.7949999999999999]

bins_ProbHH4b_2Higgs = [1.0 ] + [ 0.35- 0.013 * i for i in range(10)] 
#bins_ProbHHH6b_3Higgs = [1.0, 0.699, 0.6799999999999999, 0.6659999999999999, 0.6539999999999999, 0.6439999999999999, 0.635, 0.626, 0.618, 0.61, 0.602, 0.594, 0.586, 0.578, 0.57, 0.5619999999999999, 0.5539999999999999, 0.5449999999999999, 0.5359999999999999, 0.5269999999999999, 0.518]
bins_ProbHHH6b_3Higgs = [1.0 ] + [ opt_bins[year]- 0.013 * i for i in range(10)] #[1.0, 0.59] + [0.54 - 0.05 * i for i in range(10)]

if '2016' in args.year:
    bins_ProbHHH6b_3Higgs = [1.0 ] + [ opt_bins[year] - 0.013 * i for i in range(10)] #[1.0, 0.59] + [0.54 - 0.05 * i for i in range(10)]


bins_ProbHHH6b_2Higgs = [1.0] + [opt_bins[year] - 0.06 * i for i in range(10)]
bins_ProbVV_2Higgs = [1.0] + [0.57 - 0.05 * i for i in range(10)]


bins_ProbHHH6b_3bh0h = [1.0 ] + [opt_bins_split[year]['3bh0h'] - 0.013 * i for i in range(10)]
bins_ProbHHH6b_2bh1h = [1.0 ] + [opt_bins_split[year]['2bh1h'] - 0.013 * i for i in range(10)]
bins_ProbHHH6b_1bh2h = [1.0 ] + [opt_bins_split[year]['1bh2h'] - 0.013 * i for i in range(10)]
bins_ProbHHH6b_0bh3h = [1.0 ] + [opt_bins_split[year]['0bh3h'] - 0.013 * i for i in range(10)]

bins_ProbHHH6b_2bh0h = [1.0 ] + [opt_bins[year] - 0.013 * i for i in range(10)]
bins_ProbHHH6b_1bh1h = [1.0 ] + [opt_bins[year] - 0.013 * i for i in range(10)]
bins_ProbHHH6b_0bh2h = [1.0 ] + [opt_bins[year] - 0.013 * i for i in range(10)]

bins_ProbHHH6b_1bh0h = [1.0 ] + [opt_bins[year] - 0.013 * i for i in range(10)]
bins_ProbHHH6b_0bh1h = [1.0 ] + [opt_bins[year] - 0.013 * i for i in range(10)]
bins_ProbHHH6b_0bh0h = [1.0 ] + [opt_bins[year] - 0.013 * i for i in range(10)]

categories = {            
            'ProbHH4b_3bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_2bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_1bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh3h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_2bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_1bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_1bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh0h_inclusive' : '(nprobejets > -1)',

            'ProbHH4b_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_3Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_1Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh0h_inclusive' : '(nprobejets > -1)',

            'ProbHHH6b_1Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_3Higgs_inclusive' : '(nprobejets > -1)',

            'ProbVV_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbVV_2bh0h_inclusive' : '(nprobejets > -1)',
            'ProbVV_1bh1h_inclusive' : '(nprobejets > -1)',
            'ProbVV_0bh2h_inclusive' : '(nprobejets > -1)',

            'ProbHHH6b_1Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_3Higgs_inclusive' : '(nprobejets > -1)',

            'ProbHHH6b_3bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_2bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_1bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_0bh3h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_2bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_1bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_0bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_1bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_0bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_0bh0h_inclusive' : '(nprobejets > -1)',
}

binnings = {


    'ProbHH4b_3bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1bh2h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh3h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh2h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    
    'ProbHH4b_3Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),

    'ProbHHH6b_3Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_1Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_2Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),

    'ProbVV_2Higgs_inclusive' : convert_list_to_dict(bins_ProbVV_2Higgs),
    'ProbVV_2bh0h_inclusive' : convert_list_to_dict(bins_ProbVV_2Higgs),
    'ProbVV_1bh1h_inclusive' : convert_list_to_dict(bins_ProbVV_2Higgs),
    'ProbVV_0bh2h_inclusive' : convert_list_to_dict(bins_ProbVV_2Higgs),

    'ProbHHH6b_3bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3bh0h),
    'ProbHHH6b_2bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_2bh1h),
    'ProbHHH6b_1bh2h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_1bh2h),
    'ProbHHH6b_0bh3h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0bh3h),

    'ProbHHH6b_2bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_2bh0h),
    'ProbHHH6b_1bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_1bh1h),
    'ProbHHH6b_0bh2h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0bh2h),

    'ProbHHH6b_1bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_1bh0h),
    'ProbHHH6b_0bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0bh1h),
    'ProbHHH6b_0bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0bh0h),




}

variables = {
            'ProbHH4b_2Higgs_inclusive' : 'ProbHHH',

            'ProbHH4b_3bh0h_inclusive' : 'ProbHHH',
            'ProbHH4b_2bh1h_inclusive' : 'ProbHHH',
            'ProbHH4b_1bh2h_inclusive' : 'ProbHHH',
            'ProbHH4b_0bh3h_inclusive' : 'ProbHHH',
            'ProbHH4b_2bh0h_inclusive' : 'ProbHHH',
            'ProbHH4b_1bh1h_inclusive' : 'ProbHHH',
            'ProbHH4b_0bh2h_inclusive' : 'ProbHHH',
            'ProbHH4b_1bh0h_inclusive' : 'ProbHHH',
            'ProbHH4b_0bh1h_inclusive' : 'ProbHHH',
            'ProbHH4b_0bh0h_inclusive' : 'ProbHHH',

            'ProbHHH6b_3bh0h_inclusive' : 'ProbHHH',
            'ProbHHH6b_2bh1h_inclusive' : 'ProbHHH',
            'ProbHHH6b_1bh2h_inclusive' : 'ProbHHH',
            'ProbHHH6b_0bh3h_inclusive' : 'ProbHHH',
            'ProbHHH6b_2bh0h_inclusive' : 'ProbHHH',
            'ProbHHH6b_1bh1h_inclusive' : 'ProbHHH',
            'ProbHHH6b_0bh2h_inclusive' : 'ProbHHH',
            'ProbHHH6b_1bh0h_inclusive' : 'ProbHHH',
            'ProbHHH6b_0bh1h_inclusive' : 'ProbHHH',
            'ProbHHH6b_0bh0h_inclusive' : 'ProbHHH',


            'ProbHH4b_2Higgs_inclusive' : 'ProbHHH',
            'ProbHH4b_3Higgs_inclusive' : 'ProbHHH',
            'ProbHH4b_1Higgs_inclusive' : 'ProbHHH',
            'ProbHH4b_0bh0h_inclusive' : 'ProbHHH',
            'ProbHHH6b_1Higgs_inclusive' : 'ProbHHH',
            'ProbHHH6b_2Higgs_inclusive' : 'ProbHHH',
            'ProbHHH6b_3Higgs_inclusive' : 'ProbHHH',
            #'ProbVV_2Higgs_inclusive' : 'ProbVV',
            #'ProbVV_0bh2h_inclusive' : 'ProbVV',
            #'ProbVV_2bh0h_inclusive' : 'ProbVV',
            #'ProbVV_1bh1h_inclusive' : 'ProbVV',
}





def get_integral_and_error(hist):
    integral = hist.Integral()
    error = ctypes.c_double(0.0)
    hist.IntegralAndError(0, hist.GetNbinsX() + 1, error)
    return integral, error.value



#path = '/isilon/data/users/mstamenk/eos-triple-h/v28-categorisation/mva-inputs-2018-categorisation-spanet-boosted-classification/'
# path = '/isilon/data/users/mstamenk/eos-triple-h/%s/mva-inputs-%s-categorisation-spanet-boosted-classification/'%(version,year)
path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/%s/%s'%(version,year)
# cat = 'ProbHHH6b_1Higgs_inclusive'
option = '_'

prob = args.prob#'ProbHHH6b'

varibles_list=['h1_t3_mass', 'h2_t3_mass', 'h3_t3_mass', 'h_fit_mass', 'h1_t3_pt', 'h2_t3_pt', 'h3_t3_pt', 'h1_t3_eta', 'h2_t3_eta', 'h3_t3_eta', 'h1_t3_phi', 'h2_t3_phi', 'h3_t3_phi', 'h1_t3_dRjets', 'h2_t3_dRjets', 'h3_t3_dRjets', 'h1_t3_match', 'h2_t3_match', 'h3_t3_match',  'fatJet1Mass', 'fatJet2Mass', 'fatJet3Mass', 'fatJet1Pt', 'fatJet2Pt', 'fatJet3Pt', 'fatJet1Eta', 'fatJet2Eta', 'fatJet3Eta', 'fatJet1Phi', 'fatJet2Phi', 'fatJet3Phi', 'fatJet1PNetXbb', 'fatJet2PNetXbb', 'fatJet3PNetXbb', 'fatJet1PNetXjj', 'fatJet2PNetXjj', 'fatJet3PNetXjj', 'fatJet1PNetQCD', 'fatJet2PNetQCD', 'fatJet3PNetQCD', 'HHH_mass', 'HHH_pt', 'HHH_eta', 'nprobejets', 'nbtags', 'nloosebtags', 'nmediumbtags', 'ntightbtags', 'nsmalljets', 'nfatjets', 'ht', 'met', 'bdt', 'ProbHHH', 'ProbHH4b', 'ProbHHH4b2tau', 'ProbMultiH', 'ProbVV', 'ProbQCD', 'ProbTT', 'ProbVJets', 'ProbHH2b2tau', 'Prob3bh0h', 'Prob2bh1h', 'Prob1bh2h', 'Prob0bh3h', 'Prob2bh0h', 'Prob1bh1h', 'Prob0bh2h', 'Prob1bh0h', 'Prob0bh1h', 'Prob0bh0h', 'jet1DeepFlavB', 'jet2DeepFlavB', 'jet3DeepFlavB', 'jet4DeepFlavB', 'jet5DeepFlavB', 'jet6DeepFlavB', 'jet7DeepFlavB', 'jet8DeepFlavB', 'jet9DeepFlavB', 'jet10DeepFlavB',  'jet1Pt', 'jet2Pt', 'jet3Pt', 'jet4Pt', 'jet5Pt', 'jet6Pt', 'jet7Pt', 'jet8Pt', 'jet9Pt', 'jet10Pt', 'jet1Eta', 'jet2Eta', 'jet3Eta', 'jet4Eta', 'jet5Eta', 'jet6Eta', 'jet7Eta', 'jet8Eta', 'jet9Eta', 'jet10Eta', 'nsmalljets', 'nfatjets']


# for cat in ['%s_0bh0h_inclusive','%s_2Higgs_inclusive','%s_1Higgs_inclusive','%s_3Higgs_inclusive']:# variables:
for cat in ['%s_1Higgs_inclusive','%s_3Higgs_inclusive']:# variables:
# for cat in ['%s_0bh0h_inclusive']:# variables:
    cat = cat%prob
    print(cat)
    #print(binnings[cat])
    target = '%s%s/histograms'%(cat,option)

    if not os.path.isdir(path + '/' + target):
        os.makedirs(path+'/'+target)

    file_path = '%s'%cat + option +'/'

    # samples = glob.glob(path+'/'+file_path+'/*.root')
    # samples = [os.path.basename(s).replace('.root','') for s in samples if 'QCD' not in s]
    samples=["GluGluToHHTo4B_cHHH1","GluGluToHHTo4B_cHHH0","GluGluToHHTo4B_cHHH5","data_obs","GluGluToHHHTo6B_SM","GluGluToHHHTo4B2Tau_SM","GluGluToHHTo2B2Tau_SM","QCD_datadriven_data"]
    # samples=["data_obs","QCD_datadriven_data"]

    #samples = ['GluGluToHHHTo6B_SM']

    var_HHH = "ProbHHH" #variables[cat]

    binning = binnings[cat]
    cut = categories[cat]

    data_yield = {}
    bkg_yield = {}

    for s in samples:
        outfile = ROOT.TFile(path +'/' + target + '/' + 'histograms_%s.root'%(s),'recreate')
        print(s)
        f_name = path + '/' + file_path + '/' + s + '.root'
        tree = ROOT.TChain('Events')
        tree.AddFile(f_name)
        chunk_df = ROOT.RDataFrame('Events', f_name)
        variables = chunk_df.GetColumnNames()
        # print(variables)
        
        

        for var in varibles_list:
            
            # var = var.c_str()
            
            if var == 'ProbHHH':
                h_mva = ROOT.TH1F(var,var,len(binning),0,len(binning))
                
                for i in range(1,h_mva.GetNbinsX() + 1):

                    low,up = binning[i]
                
                    h_name = s + '_histo_%d'%i
                    tree.Draw("%s>>%s(100,0,1)"%(var,h_name),'(%s && %s > %f && %s < %f) * totalWeight'%(cut, var,low, var,up))
                    try:
                        h = ROOT.gPad.GetPrimitive(h_name)
                        integral, error = get_integral_and_error(h)
                    except: continue
                    # print("value equals:")
                    # print(i,integral,error)
                    h_mva.SetBinContent(i,integral)
                    h_mva.SetBinError(i,error)
                if 'data_obs' in s:
                    data_yield[var] = h_mva.Integral() 
                
                if 'QCD_datadriven_data' in s:
                    h_mva.Scale(float((data_yield[var])) / h_mva.Integral())
                    # print("new!")
                    # print(data_yield[var], h_mva.Integral())

                
                outfile.cd()
                h_mva.Write()
            
            else:
               
                # print(var)
                
                nbins = histograms_dict[var]["nbins"]
                xmin = histograms_dict[var]["xmin"]
                xmax = histograms_dict[var]["xmax"]   
                # chunk_df = ROOT.RDataFrame('Events', f_name)
                h_tmp = chunk_df.Filter("%s > %s"%(var,xmin)).Histo1D((var,var,nbins,xmin,xmax),var, 'totalWeight')

                
                
                if s == "data_obs":
                    data_yield[var] = h_tmp.Integral()
                    # print("already get the data value !!!!!!!!!!!!!")
                    # print(h_tmp.Integral())

                if s == "QCD_datadriven_data":
                    if h_tmp.Integral() > 0.0 :
                        # print(h_tmp.Integral())
                        h_tmp.Scale(data_yield[var]/h_tmp.Integral())
                        # print("already scale the QCD !!!!!!!!!!!!!")
                        print(data_yield[var], h_tmp.Integral())

                h_tmp.SetTitle('%s'%(var))
                h_tmp.SetName('%s'%(var))
                h_tmp.Write()


        outfile.Close()

        print("Done with:")
        print(path +'/' + target + '/' + 'histograms_%s.root'%(s))

