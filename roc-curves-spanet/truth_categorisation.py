import os, ROOT, glob

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.EnableImplicitMT()
from array import array

from utils import histograms_dict, drawText, addLabel_CMS_preliminary, luminosities, init_get_max_cat,init_get_max_prob


year = '2018'

typename = 'categorisation-spanet-boosted-classification'
path = '/isilon/data/users/mstamenk/eos-triple-h/v28-categorisation/mva-inputs-%s-%s/inclusive-weights'%(year,typename)
#path = '/isilon/data/users/mstamenk/eos-triple-h/v31-merged/mva-inputs-%s-%s/inclusive-weights'%(year,typename)

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

#ROOT.gInterpreter.Declare(getmax)
init_get_max_cat()
init_get_max_prob()



samples_mapping = {
            '3bh0h' : 1,
            '2bh1h' : 2,
            '1bh2h'  : 3,
            '0bh3h' : 4, 
            '2bh0h' : 5,
            '1bh1h': 6,
            '0bh2h': 7,
            '1bh0h' : 8,
            '0bh1h': 9,
            '0bh0h' : 0,
}

mapping = {'Prob3bh0h' : 1, 
           'Prob2bh1h' : 2,
           'Prob1bh2h' : 3,
           'Prob0bh3h': 4,
           'Prob2bh0h' : 5,
           'Prob1bh1h' : 6,
           'Prob0bh2h' : 7,
           'Prob1bh0h' : 8,
           'Prob0bh1h' : 9,
           'Prob0bh0h' : 0,
            }




#sample = 'GluGluToHHTo4B_cHHH1'
sample = 'GluGluToHHHTo6B_SM'
df = ROOT.RDataFrame('Events', path + '/' + sample + '.root')
df = df.Define('IndexMaxCat2', 'get_max_cat(Prob3bh0h, Prob2bh1h, Prob1bh2h, Prob0bh3h, Prob2bh0h, Prob1bh1h, Prob0bh2h, Prob1bh0h, Prob0bh1h, Prob0bh0h)')
df = df.Define('IndexMaxProb', 'get_max_prob(ProbHHH, ProbQCD, ProbTT, ProbVJets, ProbVV, ProbHHH4b2tau, ProbHH4b, ProbHH2b2tau)')

# Filter category 1 = HHH6b 7 = HH4b
maxprob = '0'
#df = df.Filter('IndexMaxProb == %s'%maxprob)

#df = df.Filter('HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0')



lumi = 59830.0
cutWeight = '(%f * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF)'%(lumi)
df = df.Define('eventWeight2', cutWeight)

'''
matrix = ROOT.TH2F('cm','cm',len(samples_mapping),0,len(samples_mapping),len(mapping),0,len(mapping))

print(path + '/' + sample + '.root')
df = df.Define('IndexMaxCat', 'get_max_cat(Prob3bh0h, Prob2bh1h, Prob1bh2h, Prob0bh3h, Prob2bh0h, Prob1bh1h, Prob0bh2h, Prob1bh0h, Prob0bh1h, Prob0bh0h)')

for sample in samples_mapping:
    print(sample)
    index = samples_mapping[sample]
    print('categorisation == %d'%index)
    df_tmp = df.Filter('categorisation == %d'%index)
    tot = df_tmp.Count().GetValue()
    for prob in mapping:
        index_prob = mapping[prob]
        #passed = df.Filter('%s > 0.5'%prob).Count().GetValue()
        passed = df_tmp.Filter('IndexMaxCat == %d'%index_prob).Count().GetValue()
        ratio = float(passed) / tot
        print(prob,ratio)
        matrix.SetBinContent(index,index_prob,ratio)
'''

binx = 10
xmin = 0
xmax = 10
biny = 10
ymin = 0
ymax = 10

matrix = df.Histo2D(('cm','cm',binx,xmin,xmax,biny,ymin,ymax), 'categorisation','nAK4matched','eventWeight')

if 'HHHTo6B' in sample or 'HHHTo4B2Tau' in sample:
    matrix.Scale(250)

matrix.SetStats(0)
matrix.SetTitle('Confusion matrix')

#for key,value in mapping.items():
#    matrix.GetYaxis().SetBinLabel(value + 1,key)

for key,value in mapping.items():
    matrix.GetXaxis().SetBinLabel(value + 1,key.replace('Prob',''))

c = ROOT.TCanvas()
matrix.Draw('colz text')

c.Print('truth_study_matrix_%s_%s_%s_%s_categorisation.png'%(typename,year,sample,maxprob))

for i in range(matrix.GetNbinsX()):
    tot = 0
    for j in range(matrix.GetNbinsY()):
        tot += matrix.GetBinContent(i + 1,j + 1)

    for j in range(matrix.GetNbinsY()):
        if tot > 0:
            matrix.SetBinContent(i + 1,j + 1, matrix.GetBinContent(i + 1,j + 1)/ float(tot))
        else:
            matrix.SetBinContent(i + 1,j + 1, matrix.GetBinContent(i + 1,j + 1))
c2 = ROOT.TCanvas()
matrix.Draw('colz text')

c2.Print('truth_study_normalised_%s_%s_%s_%s_categorisation.png'%(typename,year,sample,maxprob))
