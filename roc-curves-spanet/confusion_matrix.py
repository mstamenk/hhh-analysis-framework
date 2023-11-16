import os, ROOT, glob

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.EnableImplicitMT()
from array import array

from utils import histograms_dict, drawText, addLabel_CMS_preliminary, luminosities


year = '2018'

typename = 'categorisation-spanet-boosted-classification'
path = '/isilon/data/users/mstamenk/eos-triple-h/v28-categorisation/mva-inputs-%s-%s/inclusive-weights'%(year,typename)

outname = '%s.root'%(typename)
outfile = ROOT.TFile(outname,'recreate')


samples = glob.glob(path+ '*.root')
samples = [os.path.basename(s).replace('.root','') for s in samples]
samples = [s for s in samples if 'GluGlu' not in s]
samples = [s for s in samples if 'JetHT' not in s]


getmax = '''
int get_max_prob(float ProbHHH, float ProbQCD, float ProbTT, float ProbVJets, float ProbVV, float ProbHHH4b2tau, float ProbHH4b, float ProbHH2b2tau){
    std::vector<float> probs;
    probs.push_back(ProbHHH);
    probs.push_back(ProbQCD);
    probs.push_back(ProbTT);
    probs.push_back(ProbVJets);
    probs.push_back(ProbVV);
    probs.push_back(ProbHHH4b2tau);
    probs.push_back(ProbHH4b);
    probs.push_back(ProbHH2b2tau);
    //probs.push_back(ProbDY);

    auto it = std::max_element(probs.begin(), probs.end());
    int index = std::distance(probs.begin(), it);

    //std::cout << index << " " << probs[index] << std::endl;

    return index + 1;

}

'''

ROOT.gInterpreter.Declare(getmax)


mapping = {'ProbHHH' : 1, 
           'ProbQCD' : 2,
           'ProbTT' : 3,
           'ProbVJets': 4,
           'ProbVV' : 5,
           'ProbHHH4b2tau' : 6,
           'ProbHH4b' : 7,
           'ProbHH2b2tau' : 8,
           'ProbDY' : 9
            }

samples_mapping = {'GluGluToHHHTo6B_SM' : 1,
            'QCD' : 2,
            'QCD_modelling' : 3,
            'TTToHadronic'  : 4,
            'TTToSemiLeptonic' : 5, 
            'TTTo2L2Nu' : 6,
            'WJetsToQQ': 7,
            'ZJetsToQQ': 8,
            'GluGluToHHHTo4B2Tau_SM' : 9,
            'GluGluToHHTo4B_cHHH1': 10,
            'GluGluToHHTo2B2Tau' : 11,
            'DYJetsToLL' : 12,
            'ZZTo4Q' : 13,
            'WWTo4Q' : 14,
            #'WZ' : 15,

}

matrix = ROOT.TH2F('cm','cm',len(samples_mapping),0,len(samples_mapping),len(mapping),0,len(mapping))

for sample in samples_mapping:
    try:
        df = ROOT.RDataFrame('Events', path + '/' + sample + '.root')
        #df = df.Filter('nprobejets > 0')
    except: continue
    #df = df.Range(0,10)
    
    print(sample)
    df = df.Define('IndexMaxProb', 'get_max_prob(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV, ProbHHH4b2tau, ProbHH4b, ProbHH2b2tau)')
    index = samples_mapping[sample]
    h = df.Histo1D('IndexMaxProb')
    h.Draw()
    tot = df.Count().GetValue()
    for prob in mapping:
        index_prob = mapping[prob]
        #passed = df.Filter('%s > 0.5'%prob).Count().GetValue()
        passed = df.Filter('IndexMaxProb == %d'%index_prob).Count().GetValue()
        ratio = float(passed) / tot
        print(prob,ratio)
        matrix.SetBinContent(index,index_prob,ratio)

matrix.SetStats(0)
matrix.SetTitle('Confusion matrix')

for key,value in mapping.items():
    matrix.GetYaxis().SetBinLabel(value,key)

for key,value in samples_mapping.items():
    matrix.GetXaxis().SetBinLabel(value,key)

c = ROOT.TCanvas()
matrix.Draw('colz text')

c.Print('confusion_matrix_%s_%s.png'%(typename,year))