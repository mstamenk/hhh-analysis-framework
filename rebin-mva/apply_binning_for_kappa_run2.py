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
parser.add_argument('-v','--version', default='v33')
parser.add_argument('--year', default='2018')
parser.add_argument('--path_year', default='2018')
parser.add_argument('--prob', default='ProbHHH6b')
parser.add_argument('--var', default = 'ProbMultiH')
parser.add_argument('--doSyst', action = 'store_true')
args = parser.parse_args()

if args.doSyst:
    systematics = [
        # FTAG
        'nominal',
        '1./flavTagWeight_Stat_DOWN',
        'flavTagWeight_LHEScaleWeight_muF_ttbar_UP',
        'flavTagWeight_LHEScaleWeight_muF_wjets_UP',
        'flavTagWeight_LHEScaleWeight_muF_zjets_UP',
        'flavTagWeight_LHEScaleWeight_muR_ttbar_UP',
        'flavTagWeight_LHEScaleWeight_muR_wjets_UP',
        'flavTagWeight_LHEScaleWeight_muR_zjets_UP',
        'flavTagWeight_PSWeightISR_UP',
        'flavTagWeight_PSWeightFSR_UP',
        'flavTagWeight_XSec_WJets_c_UP',
        'flavTagWeight_XSec_WJets_b_UP',
        'flavTagWeight_XSec_ZJets_c_UP',
        'flavTagWeight_XSec_ZJets_b_UP',
        'flavTagWeight_PUWeight_UP',
        'flavTagWeight_PUJetID_UP',

        'flavTagWeight_Stat_DOWN',
        'flavTagWeight_LHEScaleWeight_muF_ttbar_DOWN',
        'flavTagWeight_LHEScaleWeight_muF_wjets_DOWN',
        'flavTagWeight_LHEScaleWeight_muF_zjets_DOWN',
        'flavTagWeight_LHEScaleWeight_muR_ttbar_DOWN',
        'flavTagWeight_LHEScaleWeight_muR_wjets_DOWN',
        'flavTagWeight_LHEScaleWeight_muR_zjets_DOWN',
        'flavTagWeight_PSWeightISR_DOWN',
        'flavTagWeight_PSWeightFSR_DOWN',
        'flavTagWeight_XSec_WJets_c_DOWN',
        'flavTagWeight_XSec_WJets_b_DOWN',
        'flavTagWeight_XSec_ZJets_c_DOWN',
        'flavTagWeight_XSec_ZJets_b_DOWN',
        'flavTagWeight_PUWeight_DOWN',
        'flavTagWeight_PUJetID_DOWN',

        # Fatjet FLAV TAG
        'fatJetFlavTagWeight_UP',
        'fatJetFlavTagWeight_DOWN',

        # L1 prefiring
        'l1PreFiringWeightUp', 
        'l1PreFiringWeightDown',

        # Pile-up
        'puWeightUp',
        'puWeightDown',

        # ISR
        'PSWeight[0]',
        'PSWeight[2]',

        # FSR
        'PSWeight[1]',
        'PSWeight[3]', 

        # MUR
        'LHEScaleWeight[6]',
        'LHEScaleWeight[1]',

        # MUF
        'LHEScaleWeight[4]',
        'LHEScaleWeight[3]',

        # PDF
        'LHEPdfWeight[0]', 
        '1./LHEPdfWeight[0]'

    ]
else:
    systematics = ['nominal']


labels = {
        'nominal' : '',
        '1./flavTagWeight_Stat_DOWN' : 'PNetAK4_Stat_Up',
        'flavTagWeight_LHEScaleWeight_muF_ttbar_UP' : 'PNetAK4_ttbar_muF_Up',
        'flavTagWeight_LHEScaleWeight_muF_wjets_UP' :'PNetAK4_wjets_muF_Up',
        'flavTagWeight_LHEScaleWeight_muF_zjets_UP' :'PNetAK4_zjets_muF_Up',
        'flavTagWeight_LHEScaleWeight_muR_ttbar_UP' :'PNetAK4_ttbar_muR_Up',
        'flavTagWeight_LHEScaleWeight_muR_wjets_UP' :'PNetAK4_wjets_muR_Up',
        'flavTagWeight_LHEScaleWeight_muR_zjets_UP' :'PNetAK4_zjets_muR_Up',
        'flavTagWeight_PSWeightISR_UP' : 'PNetAK4_ISR_Up',
        'flavTagWeight_PSWeightFSR_UP' : 'PNetAK4_FSR_Up',
        'flavTagWeight_XSec_WJets_c_UP' : 'PNetAK4_wjets_c_xsec_Up',
        'flavTagWeight_XSec_WJets_b_UP':  'PNetAK4_wjets_b_xsec_Up',
        'flavTagWeight_XSec_ZJets_c_UP' : 'PNetAK4_zjets_c_xsec_Up',
        'flavTagWeight_XSec_ZJets_b_UP': 'PNetAK4_zjets_b_xsec_Up',
        'flavTagWeight_PUWeight_UP' : 'PNetAK4_pileup_Up',
        'flavTagWeight_PUJetID_UP' : 'PNetAK4_jetID_Up',

        'flavTagWeight_Stat_DOWN' : 'PNetAK4_Stat_Down',
        'flavTagWeight_LHEScaleWeight_muF_ttbar_DOWN' : 'PNetAK4_ttbar_muF_Down',
        'flavTagWeight_LHEScaleWeight_muF_wjets_DOWN' :'PNetAK4_wjets_muF_Down',
        'flavTagWeight_LHEScaleWeight_muF_zjets_DOWN' :'PNetAK4_zjets_muF_Down',
        'flavTagWeight_LHEScaleWeight_muR_ttbar_DOWN' :'PNetAK4_ttbar_muR_Down',
        'flavTagWeight_LHEScaleWeight_muR_wjets_DOWN' :'PNetAK4_wjets_muR_Down',
        'flavTagWeight_LHEScaleWeight_muR_zjets_DOWN' :'PNetAK4_zjets_muR_Down',
        'flavTagWeight_PSWeightISR_DOWN' : 'PNetAK4_ISR_Down',
        'flavTagWeight_PSWeightFSR_DOWN' : 'PNetAK4_FSR_Down',
        'flavTagWeight_XSec_WJets_c_DOWN' : 'PNetAK4_wjets_c_xsec_Down',
        'flavTagWeight_XSec_WJets_b_DOWN':  'PNetAK4_wjets_b_xsec_Down',
        'flavTagWeight_XSec_ZJets_c_DOWN' : 'PNetAK4_zjets_c_xsec_Down',
        'flavTagWeight_XSec_ZJets_b_DOWN': 'PNetAK4_zjets_b_xsec_Down',
        'flavTagWeight_PUWeight_DOWN' : 'PNetAK4_pileup_Down',
        'flavTagWeight_PUJetID_DOWN' : 'PNetAK4_jetID_Down',

        'fatJetFlavTagWeight_UP' : 'PNetAK8_Up',
        'fatJetFlavTagWeight_DOWN': 'PNetAK8_Down',

        'l1PreFiringWeightUp' : 'l1Prefiring_Up', 
        'l1PreFiringWeightDown' : 'l1Prefiring_Down',
    
        'puWeightUp' : 'PileUp_Up',
        'puWeightDown': 'PileUp_Down',
    
        'PSWeight[0]': 'ISR_Up', 
        'PSWeight[2]': 'ISR_Down',
        'PSWeight[1]': 'FSR_Up',
        'PSWeight[3]': 'FSR_Down',  

             # MUR
        'LHEScaleWeight[6]': 'MUR_Up',
        'LHEScaleWeight[1]': 'MUR_Down',

        # MUF
        'LHEScaleWeight[4]': 'MUF_Up',
        'LHEScaleWeight[3]': 'MUF_Down',

        # PDF
        'LHEPdfWeight[0]' : 'PDF_Up',
        '1./LHEPdfWeight[0]' : 'PDF_Down', 


 }

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

#ProbHHH
opt_bins_probHHH = {'2018': 0.7225, 
            '2017': 0.7075,
            '2016': 0.7185,
            '2016APV': 0.71,
            '2016APV201620172018': 0.7275 , 
}

opt_bins_probMultiH = {'2018': 0.997, 
            '2017': 0.9965,
            '2016': 0.9965,
            '2016APV': 0.9965,
            '2016APV201620172018': 0.971 , 
            '2022' : 0.62,
            '2022EE': 0.695,
}

opt_bins_probHHH_2Higgs = {'2018': 0.7225, 
            '2017': 0.7075,
            '2016': 0.7185,
            '2016APV': 0.71,
            '2016APV201620172018': 0.7045, 
}

opt_bins_probMultiH_2Higgs = {'2018': 0.9975, 
            '2017': 0.997,
            '2016': 0.9965,
            '2016APV': 0.9965,
            '2016APV201620172018': 0.977, 
            '2022': 0.685,
            '2022EE': 0.75,

}



opt_bins_probMultiH_HH4b = {'2018': 0.9965, 
            '2017': 0.997,
            '2016': 0.9945,
            '2016APV': 0.996,
            '2016APV201620172018': 0.9985,
            '2022': 0.9985, 
            '2022EE': 0.9985, 
}


opt_bins_split_probHHH = {'2018': {'3bh0h' : 0.652, #0.667,
                           '2bh1h' : 0.692,#0.698,
                           '1bh2h' : 0.7015, #0.7015,
                           '0bh3h' : 0.709, #0.71
                           '2bh0h' : 0.6875, # 0.700
                           '1bh1h' : 0.7, # 0.7055
                           '0bh2h' : 0.7145, # 0.7215
                            },
                  '2017': {'3bh0h' : 0.6535,
                           '2bh1h' : 0.6785,
                           '1bh2h' : 0.6915,
                           '0bh3h' : 0.699,
                           '2bh0h' : 0.691,
                           '1bh1h' : 0.6935,
                           '0bh2h' : 0.712,
                            },
                  '2016': {'3bh0h' : 0.650,
                           '2bh1h' : 0.6795,
                           '1bh2h' : 0.6935,
                           '0bh3h' : 0.713,
                           '2bh0h' : 0.6895,
                           '1bh1h' : 0.6795,
                           '0bh2h' : 0.7005,
                            },
                  '2016APV': {'3bh0h' : 0.649,
                           '2bh1h' : 0.6755,
                           '1bh2h' : 0.6845,
                           '0bh3h' : 0.705,
                           '2bh0h' : 0.68,
                           '1bh1h' : 0.6935,
                           '0bh2h' : 0.708,
                            },
                   '2016APV201620172018': {'3bh0h' : 0.650,
                           '2bh1h' : 0.697,
                           '1bh2h' : 0.702,
                           '0bh3h' : 0.7125,
                           '2bh0h' : 0.679,
                           '1bh1h' : 0.682,
                           '0bh2h' : 0.651,
                            },
                    '2022': {'3bh0h' : 0.650,
                           '2bh1h' : 0.697,
                           '1bh2h' : 0.702,
                           '0bh3h' : 0.7125,
                           '2bh0h' : 0.679,
                           '1bh1h' : 0.682,
                           '0bh2h' : 0.651,
                            },

                    '2022EE': {'3bh0h' : 0.650,
                           '2bh1h' : 0.697,
                           '1bh2h' : 0.702,
                           '0bh3h' : 0.7125,
                           '2bh0h' : 0.679,
                           '1bh1h' : 0.682,
                           '0bh2h' : 0.651,
                            },
}

opt_bins_split_probMultiH = {'2018': {'3bh0h' : 0.9875,
                           '2bh1h' : 0.9935,
                           '1bh2h' : 0.9945,
                           '0bh3h' : 0.997,
                           '2bh0h' : 0.994,
                           '1bh1h' : 0.9965,
                           '0bh2h' : 0.9975,
                            },
                  '2017': {'3bh0h' : 0.9885,
                           '2bh1h' : 0.9915,
                           '1bh2h' : 0.9935,
                           '0bh3h' : 0.9965,
                           '2bh0h' : 0.9935,
                           '1bh1h' : 0.9945,
                           '0bh2h' : 0.997,
                            },
                  '2016': {'3bh0h' : 0.985,
                           '2bh1h' : 0.992,
                           '1bh2h' : 0.994,
                           '0bh3h' : 0.9965,
                           '2bh0h' : 0.993,
                           '1bh1h' : 0.994,
                           '0bh2h' : 0.996,
                            },
                  '2016APV': {'3bh0h' : 0.985,
                           '2bh1h' : 0.992,
                           '1bh2h' : 0.994,
                           '0bh3h' : 0.9965,
                           '2bh0h' : 0.993,
                           '1bh1h' : 0.994,
                           '0bh2h' : 0.996,
                            },

                  '2016APV201620172018': {'3bh0h' : 0.964,
                           '2bh1h' : 0.96,
                           '1bh2h' : 0.961,
                           '0bh3h' : 0.963,
                           '2bh0h' : 0.974,
                           '1bh1h' : 0.97,
                           '0bh2h' : 0.969,
                           '1bh0h' : 0.979, 
                           '0bh1h' : 0.974, 
                           '0bh0h' : 0.983,
                            },
                  '2022': {'3bh0h' : 0.565,
                           '2bh1h' : 0.64,
                           '1bh2h' : 0.649,
                           '0bh3h' : 0.649,
                           '2bh0h' : 0.72,
                           '1bh1h' : 0.659,
                           '0bh2h' : 0.53,
                            },
                  '2022EE': {'3bh0h' : 0.565,
                           '2bh1h' : 0.64,
                           '1bh2h' : 0.649,
                           '0bh3h' : 0.649,
                           '2bh0h' : 0.72,
                           '1bh1h' : 0.659,
                           '0bh2h' : 0.53,
                            },
}

opt_bins_split_probMultiH_HH4b = {'2018': {
                           '3bh0h' : 0.997,
                           '2bh1h' : 0.997,
                           '1bh2h' : 0.997,
                           '0bh3h' : 0.997,
                           '2bh0h' : 0.997,
                           '1bh1h' : 0.997,
                           '0bh2h' : 0.997,
                            },
                  '2017': {
                           '3bh0h' : 0.997,
                           '2bh1h' : 0.997,
                           '1bh2h' : 0.997,
                           '0bh3h' : 0.997,
                           '2bh0h' : 0.997,
                           '1bh1h' : 0.997,
                           '0bh2h' : 0.997,
                            },
                  '2016': {
                           '3bh0h' : 0.9865,
                           '2bh1h' : 0.9965,
                           '1bh2h' : 0.996,
                           '0bh3h' : 0.997,
                           '2bh0h' : 0.995,
                           '1bh1h' : 0.986,
                           '0bh2h' : 0.956,
                            },
                  '2016APV': {
                           '3bh0h' : 0.956,
                           '2bh1h' : 0.9965,
                           '1bh2h' : 0.996,
                           '0bh3h' : 0.997,
                           '2bh0h' : 0.988,
                           '1bh1h' : 0.984,
                           '0bh2h' : 0.958,
                            },
                  '2016APV201620172018': {'3bh0h' : 0.9865,
                           '2bh1h' : 0.996,
                           '1bh2h' : 0.9945,
                           '0bh3h' : 0.9925,
                           '2bh0h' : 0.996,
                           '1bh1h' : 0.996,
                           '0bh2h' : 0.9975,
                            },



}


year = args.year
version = args.version
var = args.var
path_year = args.path_year

if 'ProbHHH' in var:
    opt_bins = opt_bins_probHHH
    opt_bins_2Higgs = opt_bins_probHHH_2Higgs
    opt_bins_split = opt_bins_split_probHHH

elif 'ProbMultiH' in var:
    opt_bins = opt_bins_probMultiH
    opt_bins_2Higgs = opt_bins_probMultiH_2Higgs
    opt_bins_split = opt_bins_split_probMultiH
    if 'ProbHH4b' in args.prob:
        opt_bins = opt_bins_probMultiH_HH4b
        opt_bins_split = opt_bins_split_probMultiH_HH4b

#bins_ProbHH4b_2Higgs = [1.0, 0.942, 0.91, 0.901, 0.879, 0.862, 0.844, 0.8240000000000001,0.808, 0.8049999999999999, 0.7949999999999999]
if 'ProbMultiH' in var:
    delta = 0.015
elif 'ProbHHH' in var:
    delta = 0.013

if 'ProbHH4b' in args.prob:
    delta = 0.001


bins_ProbHH4b_2Higgs = [1.0 ] + [ 0.997 - delta * i for i in range(10)] 
#bins_ProbHHH6b_3Higgs = [1.0, 0.699, 0.6799999999999999, 0.6659999999999999, 0.6539999999999999, 0.6439999999999999, 0.635, 0.626, 0.618, 0.61, 0.602, 0.594, 0.586, 0.578, 0.57, 0.5619999999999999, 0.5539999999999999, 0.5449999999999999, 0.5359999999999999, 0.5269999999999999, 0.518]
bins_ProbHHH6b_3Higgs = [1.0 ] + [ opt_bins[year]- delta * i for i in range(10)] #[1.0, 0.59] + [0.54 - 0.05 * i for i in range(10)]

if '2016' in args.year:
    bins_ProbHHH6b_3Higgs = [1.0 ] + [ opt_bins[year] - delta * i for i in range(10)] #[1.0, 0.59] + [0.54 - 0.05 * i for i in range(10)]



bins_ProbHHH6b_2Higgs = [1.0] + [opt_bins_2Higgs[year] - delta * i for i in range(10)]
#bins_ProbHHH6b_2Higgs = [1.0, 0.9988, 0.9982, 0.9976, 0.9969, 0.9962, 0.9954, 0.9946, 0.9937, 0.9928, 0.9918, 0.9907]
bins_ProbHHH6b_2Higgs = bins_ProbHHH6b_2Higgs[:11]
bins_ProbHHH6b_0Higgs = [1.0] + [0.98 - delta / 4 - delta  * i for i in range(10)]
bins_ProbHHH6b_1Higgs = [1.0] + [0.974 - delta / 2  * i for i in range(10)]



bins_ProbVV_2Higgs = [1.0] + [0.57 - delta * i for i in range(10)]

bins_ProbHHH6b_3bh0h = [1.0 ] + [opt_bins_split[year]['3bh0h'] - delta * i for i in range(10)]
bins_ProbHHH6b_2bh1h = [1.0 ] + [opt_bins_split[year]['2bh1h'] - delta * i for i in range(10)]
bins_ProbHHH6b_1bh2h = [1.0 ] + [opt_bins_split[year]['1bh2h'] - delta / 2 * i for i in range(10)]
bins_ProbHHH6b_0bh3h = [1.0 ] + [opt_bins_split[year]['0bh3h'] - delta * i for i in range(10)]
bins_ProbHHH6b_2bh0h = [1.0 ] + [opt_bins_split[year]['2bh0h'] - delta / 2 * i for i in range(10)]
bins_ProbHHH6b_1bh1h = [1.0 ] + [opt_bins_split[year]['1bh1h'] - delta / 2 * i for i in range(10)]
bins_ProbHHH6b_0bh2h = [1.0 ] + [opt_bins_split[year]['0bh2h'] - delta / 2 * i for i in range(10)]

bins_ProbHHH6b_1bh0h = [1.0 ] + [opt_bins_split[year]['1bh0h'] - delta * i for i in range(10)]
bins_ProbHHH6b_0bh1h = [1.0 ] + [opt_bins_split[year]['0bh1h'] - delta * i for i in range(10)]
bins_ProbHHH6b_0bh0h = [1.0 ] + [opt_bins_split[year]['0bh0h'] - delta * i for i in range(10)]


bins_ProbHH4b_2bh0h = [1.0 ] + [opt_bins_split[year]['2bh0h'] - delta * i for i in range(10)]
bins_ProbHH4b_1bh1h = [1.0 ] + [opt_bins_split[year]['1bh1h'] - delta * i for i in range(10)]
bins_ProbHH4b_0bh2h = [1.0 ] + [opt_bins_split[year]['0bh2h'] - delta * i for i in range(10)]

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

            'ProbHHH4b2tau_1Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_3Higgs_inclusive' : '(nprobejets > -1)',

            'ProbHHH4b2tau_3bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_2bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_1bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_0bh3h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_2bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_1bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_0bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_1bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_0bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH4b2tau_0bh0h_inclusive' : '(nprobejets > -1)',
}

binnings = {


    'ProbHH4b_3bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1bh2h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh3h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2bh0h),
    'ProbHH4b_1bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_1bh1h),
    'ProbHH4b_0bh2h_inclusive' : convert_list_to_dict(bins_ProbHH4b_0bh2h),
    'ProbHH4b_1bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    
    'ProbHH4b_3Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),

    'ProbHHH6b_3Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_1Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_1Higgs),
    'ProbHHH6b_2Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_2Higgs),

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
    'ProbHHH6b_0bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0Higgs),

    'ProbHHH4b2tau_3bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3bh0h),
    'ProbHHH4b2tau_2bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_2bh1h),
    'ProbHHH4b2tau_1bh2h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_1bh2h),
    'ProbHHH4b2tau_0bh3h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0bh3h),

    'ProbHHH4b2tau_2bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_2bh0h),
    'ProbHHH4b2tau_1bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_1bh1h),
    'ProbHHH4b2tau_0bh2h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0bh2h),

    'ProbHHH4b2tau_1bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_1bh0h),
    'ProbHHH4b2tau_0bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0bh1h),
    'ProbHHH4b2tau_0bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_0bh0h),



    'ProbHHH4b2tau_3Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH4b2tau_1Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH4b2tau_2Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),


}

variables = {
            'ProbHH4b_2Higgs_inclusive' : 'ProbMultiH',

            'ProbHH4b_3bh0h_inclusive' : 'ProbMultiH',
            'ProbHH4b_2bh1h_inclusive' : 'ProbMultiH',
            'ProbHH4b_1bh2h_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh3h_inclusive' : 'ProbMultiH',
            'ProbHH4b_2bh0h_inclusive' : 'ProbMultiH',
            'ProbHH4b_1bh1h_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh2h_inclusive' : 'ProbMultiH',
            'ProbHH4b_1bh0h_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh1h_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh0h_inclusive' : 'ProbMultiH',

            'ProbHHH6b_3bh0h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_2bh1h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_1bh2h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_0bh3h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_2bh0h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_1bh1h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_0bh2h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_1bh0h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_0bh1h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_0bh0h_inclusive' : 'ProbMultiH',


            'ProbHH4b_2Higgs_inclusive' : 'ProbMultiH',
            'ProbHH4b_3Higgs_inclusive' : 'ProbMultiH',
            'ProbHH4b_1Higgs_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh0h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_1Higgs_inclusive' : 'ProbMultiH',
            'ProbHHH6b_2Higgs_inclusive' : 'ProbMultiH',
            'ProbHHH6b_3Higgs_inclusive' : 'ProbMultiH',
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
# path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/%s/%s'%(version,path_year)

path = '/eos/cms/store/group/phys_higgs/cmshhh/%s-fix-ak4-ak8'%(version)
# path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/%s'%(version)
# cat = 'ProbHHH6b_1Higgs_inclusive'
option = '_CR'

prob = args.prob#'ProbHHH6b'

# varibles_list=['h1_t3_mass', 'h2_t3_mass', 'h3_t3_mass', 'h_fit_mass', 'h1_t3_pt', 'h2_t3_pt', 'h3_t3_pt', 'h1_t3_eta', 'h2_t3_eta', 'h3_t3_eta', 'h1_t3_phi', 'h2_t3_phi', 'h3_t3_phi', 'h1_t3_dRjets', 'h2_t3_dRjets', 'h3_t3_dRjets', 'h1_t3_match', 'h2_t3_match', 'h3_t3_match',  'fatJet1Mass', 'fatJet2Mass', 'fatJet3Mass', 'fatJet1Pt', 'fatJet2Pt', 'fatJet3Pt', 'fatJet1Eta', 'fatJet2Eta', 'fatJet3Eta', 'fatJet1Phi', 'fatJet2Phi', 'fatJet3Phi', 'fatJet1PNetXbb', 'fatJet2PNetXbb', 'fatJet3PNetXbb', 'fatJet1PNetXjj', 'fatJet2PNetXjj', 'fatJet3PNetXjj', 'fatJet1PNetQCD', 'fatJet2PNetQCD', 'fatJet3PNetQCD', 'HHH_mass', 'HHH_pt', 'HHH_eta', 'nprobejets', 'nbtags', 'nloosebtags', 'nmediumbtags', 'ntightbtags', 'nsmalljets', 'nfatjets', 'ht', 'met', 'bdt', 'ProbHHH', 'ProbHH4b', 'ProbHHH4b2tau', 'ProbMultiH', 'ProbVV', 'ProbQCD', 'ProbTT', 'ProbVJets', 'ProbHH2b2tau', 'Prob3bh0h', 'Prob2bh1h', 'Prob1bh2h', 'Prob0bh3h', 'Prob2bh0h', 'Prob1bh1h', 'Prob0bh2h', 'Prob1bh0h', 'Prob0bh1h', 'Prob0bh0h', 'jet1DeepFlavB', 'jet2DeepFlavB', 'jet3DeepFlavB', 'jet4DeepFlavB', 'jet5DeepFlavB', 'jet6DeepFlavB', 'jet7DeepFlavB', 'jet8DeepFlavB', 'jet9DeepFlavB', 'jet10DeepFlavB',  'jet1Pt', 'jet2Pt', 'jet3Pt', 'jet4Pt', 'jet5Pt', 'jet6Pt', 'jet7Pt', 'jet8Pt', 'jet9Pt', 'jet10Pt', 'jet1Eta', 'jet2Eta', 'jet3Eta', 'jet4Eta', 'jet5Eta', 'jet6Eta', 'jet7Eta', 'jet8Eta', 'jet9Eta', 'jet10Eta', 'nsmalljets', 'nfatjets']
varibles_list=['ProbMultiH']


# for cat in ['%s_2bh0h_inclusive','%s_1bh1h_inclusive','%s_0bh2h_inclusive','%s_0bh0h_inclusive','%s_1Higgs_inclusive','%s_2Higgs_inclusive','%s_3Higgs_inclusive','%s_3bh0h_inclusive','%s_2bh1h_inclusive','%s_1bh2h_inclusive','%s_0bh3h_inclusive']:# variables:
# for cat in ['%s_2bh0h_inclusive','%s_1bh1h_inclusive','%s_0bh2h_inclusive','%s_0bh0h_inclusive','%s_1Higgs_inclusive','%s_2Higgs_inclusive','%s_3Higgs_inclusive','%s_3bh0h_inclusive','%s_2bh1h_inclusive','%s_1bh2h_inclusive','%s_0bh3h_inclusive']:# variables:
# for cat in ['%s_2Higgs_inclusive']:# variables:
# for cat in ['%s_1bh2h_inclusive','%s_0bh3h_inclusive']:# variables:
# for cat in ['%s_3bh0h_inclusive','%s_2bh1h_inclusive','%s_1bh2h_inclusive','%s_0bh3h_inclusive']:# variables:
for cat in ['%s_2bh0h_inclusive','%s_1bh1h_inclusive','%s_0bh2h_inclusive','%s_3bh0h_inclusive','%s_2bh1h_inclusive','%s_1bh2h_inclusive','%s_0bh3h_inclusive']:# variables:
    cat = cat%prob
    print(cat)
    #print(binnings[cat])
    cat_path = cat + option
    output_path = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/v34-fix-ak4-ak8"


    if not os.path.isdir(output_path + '/run2/' + cat_path):
        os.makedirs(output_path+'/run2/'+cat_path)
    hist_path = output_path + '/run2/' + cat_path + '/histograms'
    if not os.path.isdir(hist_path):
        os.makedirs(hist_path)

    samples = ["GluGluToHHTo4B_cHHH1","GluGluToHHTo4B_cHHH0","GluGluToHHTo4B_cHHH5","data_obs","GluGluToHHHTo6B_SM","QCD_datadriven",'HHHTo6B_c3_0_d4_99','HHHTo6B_c3_0_d4_minus1','HHHTo6B_c3_19_d4_19','HHHTo6B_c3_1_d4_0','HHHTo6B_c3_1_d4_2','HHHTo6B_c3_2_d4_minus1','HHHTo6B_c3_4_d4_9','HHHTo6B_c3_minus1_d4_0','HHHTo6B_c3_minus1_d4_minus1','HHHTo6B_c3_minus1p5_d4_minus0p5']

    var_HHH = "ProbMultiH" 

    binning = binnings[cat]
    cut = categories[cat]

    data_yield = {}
    bkg_yield = {}
    outfile = ROOT.TFile(output_path +'/run2/' + cat_path + '/histograms/' + 'histograms_kappa.root','recreate')

    for s in samples:
        print(s)
        proc_list = ['%s/mva-inputs-2016-categorisation-spanet-boosted-classification/%s/%s.root'%(path,cat_path,s),'%s/mva-inputs-2016APV-categorisation-spanet-boosted-classification/%s/%s.root'%(path,cat_path,s),'%s/mva-inputs-2017-categorisation-spanet-boosted-classification/%s/%s.root'%(path,cat_path,s),'%s/mva-inputs-2018-categorisation-spanet-boosted-classification/%s/%s.root'%(path,cat_path,s)]
        tree = ROOT.TChain('Events')
        for f_name in proc_list:
            tree.AddFile(f_name)        

        chunk_df = ROOT.RDataFrame('Events', proc_list)
        try:
            entries_no_filter = int(chunk_df.Count().GetValue())
        except:
            continue
        variables = chunk_df.GetColumnNames()
        # print(variables)
        
        

        for var in varibles_list:
            # var = var.c_str()
            if var == 'ProbMultiH':
                if 'data_obs' in s:
                    h_mva = ROOT.TH1F('data_obs','data_obs',len(binning),0,len(binning))
                    copy = False
                elif 'QCD' in s:
                    h_mva = ROOT.TH1F('QCD','QCD',len(binning),0,len(binning))
                    copy = False
                elif s == 'GluGluToHHTo4B_cHHH1':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('ggHH_kl_1_kt_1','ggHH_kl_1_kt_1',len(binning),0,len(binning))
                    copy = True
                elif s == 'GluGluToHHTo4B_cHHH0':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('ggHH_kl_0_kt_1','ggHH_kl_0_kt_1',len(binning),0,len(binning))
                    copy = True
                elif s == 'GluGluToHHTo4B_cHHH5':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('ggHH_kl_5_kt_1','ggHH_kl_5_kt_1',len(binning),0,len(binning))
                    copy = True
                elif s == 'GluGluToHHHTo6B_SM':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_0_d4_0','c3_0_d4_0',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_0_d4_99':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_0_d4_99','c3_0_d4_99',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_0_d4_minus1':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_0_d4_m1','c3_0_d4_m1',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_19_d4_19':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_19_d4_19','c3_19_d4_19',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_1_d4_0':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_1_d4_0','c3_1_d4_0',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_1_d4_2':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_1_d4_2','c3_1_d4_2',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_2_d4_minus1':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_2_d4_m1','c3_2_d4_m1',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_4_d4_9':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_4_d4_9','c3_4_d4_9',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_minus1_d4_0':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_m1_d4_0','c3_m1_d4_0',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_minus1_d4_minus1':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_m1_d4_m1','c3_m1_d4_m1',len(binning),0,len(binning))
                    copy = True
                elif s == 'HHHTo6B_c3_minus1p5_d4_minus0p5':
                    h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
                    h_copy = ROOT.TH1F('c3_m1p5_d4_m0p5','c3_m1p5_d4_m0p5',len(binning),0,len(binning))
                    copy = True
                

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
                    if copy :
                        h_copy.SetBinContent(i,integral)
                        h_copy.SetBinError(i,error)
                if 'data_obs' in s:
                    data_yield[var] = h_mva.Integral() 
                
                if 'QCD_datadriven' in s:
                    h_mva.Scale(float((data_yield[var])) / h_mva.Integral())
                    # print("new!")
                    # print(data_yield[var], h_mva.Integral())

                
                outfile.cd()
                h_mva.Write()
                if copy : 
                    h_copy.Write()
            
    outfile.Close()

    print("Done with:")
    print(path +'/run2/' + cat_path + '/histogrmas/' + 'histograms_kappa.root')


