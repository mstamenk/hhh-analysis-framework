import os, ROOT,glob

import ctypes

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
parser.add_argument('--nbins', default='10')
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




year = args.year
version = args.version
var = args.var
nbins = args.nbins
nbins = int(nbins)





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

def get_integral_and_error(hist):
    integral = hist.Integral()
    error = ctypes.c_double(0.0)
    hist.IntegralAndError(0, hist.GetNbinsX() + 1, error)
    return integral, error.value

def convert_list_to_dict(ls):
    length = len(ls)
    ret = {}
    for i in range(length -1):
        if i < length:
            upper = ls[i+1]
            lower = ls[i]
            print(lower,upper)
            ret[i] = [lower,upper]
    return ret

path = '/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/%s/%s'%(version,year)



cat = 'ProbHH4b_1bh1h_inclusive'
option = '_CR'

prob = args.prob#'ProbHHH6b'



for cat in ['%s_3bh0h_inclusive','%s_2bh1h_inclusive','%s_1bh2h_inclusive','%s_0bh3h_inclusive','%s_0bh0h_inclusive','%s_2Higgs_inclusive','%s_1Higgs_inclusive','%s_3Higgs_inclusive']:# variables:
   
    target = '%s%s/histograms'%(cat,option)

    if not os.path.isdir(path + '/' + target):
        os.makedirs(path+'/'+target)

    file_path = '%s'%cat + option +'/'

    samples = glob.glob(path+'/'+file_path+'/*.root')
    samples = [os.path.basename(s).replace('.root','') for s in samples]

    #var = "ProbMultiH" #variables[cat]
    outfile = ROOT.TFile(path +'/' + target + '/' + 'histograms_compare_%s.root'%var,'recreate')

    #samples = ['GluGluToHHHTo6B_SM']
    binning = convert_list_to_dict([1.0/nbins * i  for i in range(nbins)]+[1.0])
    cut = categories[cat]

    data_yield = 0
    bkg_yield = 0

    for s in samples:
        if 'GluGlu' in s: continue # separate signal from other processes
        if 'QCD' in s: continue
        print(s)
        f_name = path + '/' + file_path + '/' + s + '.root'
        tree = ROOT.TChain('Events')
        tree.AddFile(f_name)

        if 'JetHT' in s:
            h_mva = ROOT.TH1F('data_obs','data_obs',len(binning),0,len(binning))
        else:
            h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))

        weight = 'totalWeight'

        #    weight = 'totalWeight / (flavTagWeight * fatJetFlavTagWeight)'
        try :
            chunk_df = ROOT.RDataFrame('Events','%s/%s/%s.root'%(path,file_path,s))

        except :
            print("process %s has 0 entries, skipping doing the histogram" % proctodo)

        h_mva = chunk_df.Filter("%s && %s > 0.0"%(cut,var)).Histo1D((var,var,nbins,0.0,1.0),var, weight)

        if 'data_obs' in s:
            data_yield = h_mva.Integral() 
        if 'data_obs' not in s:
            bkg_yield += h_mva.Integral()   

        
      
        outfile.cd()
        h_mva.Write()


    for sam in samples:
        if 'GluGlu' not in sam: continue # separate signal from other processes

        for syst in systematics:
            if 'nominal' in syst:
                s = sam 
                if 'JMRUP' in sam:
                    s = sam.replace('JMRUP','') + '_JMR_Up'
                elif 'JMRDOWN' in sam:
                    s = sam.replace('JMRDOWN','') + '_JMR_Down'

                if 'JESUP' in sam:
                    s = sam.replace('JESUP','') + '_JES_Up'
                elif 'JESDOWN' in sam:
                    s = sam.replace('JESDOWN','') + '_JES_Down'

                if 'JERUP' in sam:
                    s = sam.replace('JERUP','') + '_JER_Up'
                elif 'JERDOWN' in sam:
                    s = sam.replace('JERDOWN','') + '_JER_Down'

            else:
                s = sam + '_' + labels[syst]
                if 'JMR' in sam or 'JES' in sam or 'JER' in sam: continue
            print(s)


            f_name = path + '/' + file_path + '/' + sam + '.root'
            tree = ROOT.TChain('Events')
            tree.AddFile(f_name)

            if 'JetHT' in s:
                h_mva = ROOT.TH1F('data_obs','data_obs',len(binning),0,len(binning))
            else:
                h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))

            if 'nominal' in syst:
                weight = 'totalWeight'
            elif 'LHE' in syst or 'PSWeight' in syst:
                weight = 'totalWeight * %s'%syst

            elif 'flavTag' in syst or 'FlavTag' in syst:
                w = syst.split('_')[0]
                weight = '(totalWeight / %s) * %s'%(w,syst)

            
            #    weight = 'totalWeight / (flavTagWeight * fatJetFlavTagWeight)'

            for i in range(0,h_mva.GetNbinsX()):
                print(h_mva.GetNbinsX())
                print(binning)
                low,up = binning[i]
            
                h_name = sam + '_histo_%d_%s'%(i,labels[syst])

                

                tree.Draw("%s>>%s(100,0,1)"%(var,h_name),'(%s && %s > %f && %s < %f) * %s'%(cut, var,low, var,up,weight))
                try:
                    h = ROOT.gPad.GetPrimitive(h_name)
                    integral, error = get_integral_and_error(h)
                except: continue
                
                print(i,integral,error)
                h_mva.SetBinContent(i,integral)
                h_mva.SetBinError(i,error)
            if 'data_obs' in s:
                data_yield = h_mva.Integral() 
            if 'data_obs' not in s:
                bkg_yield += h_mva.Integral()   

            
            #h_mva.Rebin(2)
            #if 'data_obs' not in s:
            #if 'QCD' in s:
            #    h_mva.Scale(0.47)
            outfile.cd()
            h_mva.Write()
            

    tree = ROOT.TChain('Events')
    #tree.AddFile(path + '/' + file_path + '/' + 'QCD' + '.root')
    #tree.AddFile(path + '/' + file_path + '/' + 'QCD_modelling' + '.root')
    tree.AddFile(path + '/' + file_path + '/' + 'QCD_datadriven' + '.root')

    h_mva = ROOT.TH1F('QCD','QCD',len(binning),0,len(binning))
    print('QCD')
    for i in range(0,h_mva.GetNbinsX()):

        low,up = binning[i]

        h_name = 'QCD' + '_histo_%d'%i
        tree.Draw("%s>>%s(100,0,1)"%(var,h_name),'(%s && %s > %f && %s < %f) * totalWeight'%(cut, var,low, var,up))
        try:
            h = ROOT.gPad.GetPrimitive(h_name)
            integral, error = get_integral_and_error(h)
        except: continue
        
        print(i,integral,error)
        h_mva.SetBinContent(i,integral)
        h_mva.SetBinError(i,error)


    print(data_yield,bkg_yield, h_mva.Integral())
    #h_mva.Scale(float((data_yield-bkg_yield)) / h_mva.Integral())
    if h_mva.Integral() > 0:
        h_mva.Scale(float((data_yield)) / h_mva.Integral())

    h_mva.Write()

    outfile.Close()
   

    print("Done with:")
    print(path +'/' + target + '/' + 'histograms_compare_%s.root'%var)
