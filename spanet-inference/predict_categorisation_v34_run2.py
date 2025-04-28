import ROOT, os
#ROOT.EnableImplicitMT()


import  onnxruntime 

import numpy as np

# argument parser
import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--f_in', default = 'GluGluToHHHTo6B_SM') # input samples
parser.add_argument('-v','--version', default='v35') # version of NanoNN production
parser.add_argument('--year', default='2018') # year
parser.add_argument('--batch_size', default='100') # year
parser.add_argument('--batch_number',default = '0')
parser.add_argument('--afterCat', action='store_true')
parser.add_argument('--secondCategorisation', action='store_true')
args = parser.parse_args()


# Method declarations

def get_best(ls, index):
    ret = str(ls[index])
    if len(ret) == 1:
        ret = str(ls[index]*10)
    return ret

def get_maximas(arr_in):
    arr = np.triu(arr_in[0:10,0:10])
    #max_values = np.partition(arr.flatten(), -5)[-5:]
    #max_indices = np.argpartition(arr.flatten(), -5)[-5:]
    max_indices = np.argsort(arr.flatten())[::-1][:45]
    max_values = arr.flatten()[max_indices]
    return max_values,max_indices

def convertIndex(index):
    if len(str(index)) == 1:
        ret = str(index*10)
    else:
        ret = str(index)
    return ret

def remove_elements(index, m, ind):
    tmp_index = convertIndex(index)
    ind_ret = [i for i in ind if tmp_index[0] not in convertIndex(i) and tmp_index[1] not in convertIndex(i)]
    m_ret = [m[i] for i in range(len(m)) if ind.count(i) == 1]
    return m_ret, ind_ret

def pair_higgs(max_h1, index_h1, max_h2, index_h2, max_h3, index_h3, h1Det, h2Det, h3Det):
    higgs = []

    m_h1 = h1Det
    m_h2 = h2Det
    m_h3 = h3Det

    if m_h1 > m_h2:
        if m_h1 > m_h3:
            higgs.append(index_h1[0])
            m_prime_2, index_prime_2 = remove_elements(index_h1[0], max_h2, index_h2)
            m_prime_3, index_prime_3 = remove_elements(index_h1[0], max_h3, index_h3)
        else:
            higgs.append(index_h3[0])
            m_prime_2, index_prime_2 = remove_elements(index_h3[0], max_h1, index_h1)
            m_prime_3, index_prime_3 = remove_elements(index_h3[0], max_h2, index_h2)

    else:
        if m_h2 > m_h3:
            higgs.append(index_h2[0]) 
            m_prime_2, index_prime_2 = remove_elements(index_h2[0], max_h1, index_h1)
            m_prime_3, index_prime_3 = remove_elements(index_h2[0], max_h3, index_h3)

        else:
            higgs.append(index_h3[0])
            m_prime_2, index_prime_2 = remove_elements(index_h3[0], max_h1, index_h1)
            m_prime_3, index_prime_3 = remove_elements(index_h3[0], max_h2, index_h2)

    m_h2 = m_prime_2[0]
    m_h3 = m_prime_3[0]

    if m_h2 > m_h3:
        higgs.append(index_prime_2[0])
        m_last_3, index_last_3 = remove_elements(index_prime_2[0], m_prime_3, index_prime_3)
    else:
        higgs.append(index_prime_3[0])
        m_last_3, index_last_3 = remove_elements(index_prime_3[0], m_prime_2, index_prime_2)
    higgs.append(index_last_3[0])
    return higgs


def find_boosted_higgs(bh1,bh2,bh3):
    boosted_h = []
    for higgs in [bh1,bh2,bh3]:
        for i in range(10,13):
            if higgs[i] > 0.5:
                boosted_h.append(i+100)
    boosted_h = list(set(boosted_h))
    return boosted_h

def process(i):
    max_h1, index_h1 = get_maximas(output_values[0][i])
    max_h2, index_h2 = get_maximas(output_values[1][i])
    max_h3, index_h3 = get_maximas(output_values[2][i])

    h1Det = output_values[6][i]
    h2Det = output_values[7][i]
    h3Det = output_values[8][i]

    bh1 = output_values[3][i]
    bh2 = output_values[4][i]
    bh3 = output_values[5][i]

    boosted_higgs = find_boosted_higgs(bh1,bh2,bh3)

    try:
        higgses = boosted_higgs + pair_higgs(max_h1.tolist(),index_h1.tolist(), max_h2.tolist(),index_h2.tolist(), max_h3.tolist(),index_h3.tolist(),h1Det,h2Det,h3Det)
        return higgses[0], higgses[1], higgses[2]
    except:
        h_1 = ROOT.TLorentzVector()
        h_2 = ROOT.TLorentzVector()
        h_3 = ROOT.TLorentzVector()
        h_1.SetPtEtaPhiM(0,0,0,0)
        h_2.SetPtEtaPhiM(0,0,0,0)
        h_3.SetPtEtaPhiM(0,0,0,0)
        return h_1,h_2,h_3



# return df.Define(name, [&](ULong64_t e) { return v[e]; }, {"rdfentry_"});
# return df.Define(name, [&](ULong64_t e) { return v[e]; }, {"rdfentry_"});
ROOT.gInterpreter.Declare('''
ROOT::RDF::RNode AddArray(ROOT::RDF::RNode df, ROOT::RVec<double> &v, const std::string &name) {
    return df.Define(name, [&](unsigned int e) { return v[e]; }, {"counter_cat"});
}

ROOT::RDF::RNode AddBoolArray(ROOT::RDF::RNode df, ROOT::RVec<Long64_t> &v, const std::string &name) {
    unsigned rdf_entry = 0;
    return df.Define(name, [&](unsigned int e) { return v[e]; }, {"counter_cat"});
}

unsigned counter_cat = 0;
''')

# Open RDF and onnx session

#session = onnxruntime.InferenceSession("/HEP/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework/spanet-inference/spanet_classification_test.onnx")

sess_options = onnxruntime.SessionOptions()
sess_options.intra_op_num_threads = 23
sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_PARALLEL

#sess_options.log_severity_level = 0  # Debug level logging
#sess_options.log_verbosity_level = 4  # More detailed logs

if '2022' in args.year:
    session = onnxruntime.InferenceSession("/users/mstamenk/hhh-analysis-framework/spanet-inference/spanet_classification_2022_optimised.onnx",sess_options, providers=['CUDAExecutionProvider'])
else:
    session = onnxruntime.InferenceSession("/users/mstamenk/hhh-analysis-framework/spanet-inference/spanet_v34_categorisation_v1.onnx",sess_options, providers=['CPUExecutionProvider'])



input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

regime = 'inclusive-weights'
path = '/users/mstamenk/scratch/mstamenk/%s/mva-inputs-%s/%s/'%(args.version,args.year,regime)
if args.afterCat:
    path = '/users/mstamenk/scratch/mstamenk/%s/mva-inputs-%s-categorisation-spanet-boosted-classification/%s/'%(args.version,args.year,regime)
if args.secondCategorisation:
    path = '/users/mstamenk/scratch/mstamenk/%s/mva-inputs-%s-spanet-boosted-classification-categorisation-spanet-boosted-classification/%s/'%(args.version,args.year,regime)
path_f_in = path + '/' + '%s.root'%args.f_in

df = ROOT.RDataFrame("Events", path_f_in)
entries = df.Count().GetValue()

event_min = int(args.batch_size) * int(args.batch_number)
event_max = event_min + int(args.batch_size)

print(entries, event_min, event_max)
if event_max > entries:
    event_max = entries 

if event_min > entries:
    print("Error %d out of range, max events %d"%(event_min,entries))
    exit()

df = df.Range(event_min,event_max)
df = df.Define('counter_cat','counter_cat++')

if '2022' in args.year:
    jet_vars = ["%sPt", "%sEta","%sSinPhi","%sCosPhi", "%sPNetB","%sMass"]
else:
    #jet_vars = ["%sPtCorr", "%sEta","%sSinPhi","%sCosPhi", "%sPNetB","%sMass"]
    jet_vars = ["%sPtCorr", "%sEta","%sSinPhi","%sCosPhi","%sPNetTagCat","%sMass"]
arrays = []


for i in ['1','2','3','4','5','6','7','8','9','10']:
    #df = df.Define('jet%sCosPhi'%i, 'TMath::Cos(jet%sPhi)'%i)
    #df = df.Define('jet%sSinPhi'%i, 'TMath::Sin(jet%sPhi)'%i)
    #df = df.Define('jet%sLogPt'%i, 'TMath::Log(jet%sPt+1)'%i)
 #   if '2022' in args.year:
 #       df = df.Define('jet%sbRegCorr'%i, '1')
    #df = df.Define('jet%sPtCorr'%i, 'jet%sPt * jet%sbRegCorr'%(i,i))
    #if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in or 'JetMET' in args.f_in:
    #    df = df.Define('jet%sHiggsMatchedIndex'%i,'-1')    
    column = [el%'jet%s'%i for el in jet_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack([np_dict[col] for col in column]).T.astype(np.float32)
    arrays.append(np_arr)


np_arr = np.vstack([np_dict[col] for col in column])
print("Shape after vstack:", np_arr.shape)
print("Shape after transpose:",np_arr.T.astype(np.float32).shape)

# Boosted arrays
boosted_arrays = []
#fatjet_vars = ['fatJet%sPt', 'fatJet%sEta','fatJet%sSinPhi','fatJet%sCosPhi','fatJet%sPNetXbb','fatJet%sPNetXjj','fatJet%sPNetQCD','fatJet%sMass']
fatjet_vars = ['fatJet%sPt', 'fatJet%sEta','fatJet%sSinPhi','fatJet%sCosPhi','fatJet%sPNetXbbTagCat','fatJet%sMass']
for i in ['1','2','3']:
    #df = df.Define('fatJet%sCosPhi'%i, 'TMath::Cos(fatJet%sPhi)'%i)
    #df = df.Define('fatJet%sSinPhi'%i, 'TMath::Sin(fatJet%sPhi)'%i)
    #df = df.Define('fatJet%sLogPt'%i, 'TMath::Log(fatJet%sPt + 1)'%i)
    #if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
    #    df = df.Define('fatJet%sHiggsMatchedIndex'%i,'-1')
    

    column = [el%i for el in fatjet_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack([np_dict[col] for col in column]).T.astype(np.float32)
    boosted_arrays.append(np_arr)

lep_arrays = []
lep_vars = ['lep%sPt', 'lep%sEta','lep%sSinPhi','lep%sCosPhi']
for i in ['1','2']:
    #df = df.Define('lep%sCosPhi'%i, 'TMath::Cos(lep%sPhi)'%i)
    #df = df.Define('lep%sSinPhi'%i, 'TMath::Sin(lep%sPhi)'%i)
    #df = df.Define('lep%sLogPt'%i, 'TMath::Log(lep%sPt + 1)'%i)
    #if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
    #    df = df.Define('fatJet%sHiggsMatchedIndex'%i,'-1')
    

    column = [el%i for el in lep_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack([np_dict[col] for col in column]).T.astype(np.float32)
    lep_arrays.append(np_arr)

tau_arrays = []
tau_vars = ['tau%sPt', 'tau%sEta','tau%sSinPhi','tau%sCosPhi']
for i in ['1','2']:
    #df = df.Define('tau%sCosPhi'%i, 'TMath::Cos(tau%sPhi)'%i)
    #df = df.Define('tau%sSinPhi'%i, 'TMath::Sin(tau%sPhi)'%i)
    #df = df.Define('tau%sLogPt'%i, 'TMath::Log(tau%sPt + 1)'%i)
    #if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
    #    df = df.Define('fatJet%sHiggsMatchedIndex'%i,'-1')
    
    column = [el%i for el in tau_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack([np_dict[col] for col in column]).T.astype(np.float32)
    tau_arrays.append(np_arr)


Jets_arrays = {}
#Higgs_vars = ['massjet%sjet%s', 'ptjet%sjet%s','etajet%sjet%s','sinphijet%sjet%s','cosphijet%sjet%s','drjet%sjet%s']
Higgs_vars = ['massjet%sjet%s', 'ptjet%sjet%s','drjet%sjet%s']
for i in ['1','2','3','4','5','6','7','8','9','10']:
    name = 'Jet%s'%i
    Higgs_list = []
    for j in ['2','3','4','5','6','7','8','9','10']:
        if i == j: continue
        if int(j) < int(i): continue
        #df = df.Define('cosphijet%sjet%s'%(i,j), 'TMath::Cos(phijet%sjet%s)'%(i,j))
        #df = df.Define('sinphijet%sjet%s'%(i,j), 'TMath::Sin(phijet%sjet%s)'%(i,j))
        #if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
        #    df = df.Define('fatJet%sHiggsMatchedIndex'%i,'-1')
        
        column = [el%(i,j) for el in Higgs_vars]
        np_dict = df.AsNumpy(column)
        np_arr = np.vstack([np_dict[col] for col in column]).T.astype(np.float32)
        Higgs_list.append(np_arr)
    Jets_arrays[name] = Higgs_list






met_arrays = []
met_vars = ['met']
column = [el for el in met_vars]
np_dict = df.AsNumpy(column)
np_arr = np.vstack([np_dict[col] for col in column]).T.astype(np.float32)
met_arrays.append(np_arr)

ht_arrays = []
ht_vars = ['ht']
column = [el for el in ht_vars]
np_dict = df.AsNumpy(column)
np_arr = np.vstack([np_dict[col] for col in column]).T.astype(np.float32)
ht_arrays.append(np_arr)

if '2016APV' in args.year:
    era_value = 1
elif '2016' in args.year:
    era_value = 2
elif '2017' in args.year:
    era_value = 3
elif '2018' in args.year:
    era_value = 4

era = np.full_like(np_arr, era_value)
era_arrays = [era]





# 4 vectors
jet_4vec = ["%sPt", "%sEta","%sPhi","%sMass","%sHiggsMatchedIndex"]
array_4vec = []
for i in ['1','2','3','4','5','6','7','8','9','10']:
    column_4vec = [el%'jet%s'%i for el in jet_4vec]
    np_4vec = df.AsNumpy(column_4vec)
    np_arr_4vec = np.vstack([np_4vec[col] for col in column_4vec]).T
    array_4vec.append(np_arr_4vec)

jets = []
for i in range(len(array_4vec[0])):
    jets_tmp = []
    for j in range(10):
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(array_4vec[j][i][0], array_4vec[j][i][1], array_4vec[j][i][2], array_4vec[j][i][3])
        jet.HiggsMatchedIndex = array_4vec[j][i][4]
        jets_tmp.append(jet)
    jets.append(jets_tmp)


fatjet_4vec = ["%sPt", "%sEta","%sPhi","%sMass","%sHiggsMatchedIndex"]
array_fj_4vec = []
for i in ['1','2','3']:
    column_4vec = [el%'fatJet%s'%i for el in jet_4vec]
    np_4vec = df.AsNumpy(column_4vec)
    np_arr_4vec = np.vstack([np_4vec[col] for col in column_4vec]).T
    array_fj_4vec.append(np_arr_4vec)

fatjets = []
for i in range(len(array_fj_4vec[0])):
    jets_tmp = []
    for j in range(3):
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(array_4vec[j][i][0], array_4vec[j][i][1], array_4vec[j][i][2], array_4vec[j][i][3])
        jet.HiggsMatchedIndex = array_4vec[j][i][4]
        jets_tmp.append(jet)
    fatjets.append(jets_tmp)


# Inputs dictionaries
Jets_data = np.transpose(arrays,(1,0,2))
MIN_PT = 20
Jets_Pt = Jets_data[:,:,0]

Jets_mask = Jets_Pt > MIN_PT

BoostedJets_data = np.transpose(boosted_arrays, (1,0,2))
MIN_FJPT = 200
MIN_FJMASS = 70
BoostedJets_Pt = BoostedJets_data[:,:,0]
BoostedJets_Mass = BoostedJets_data[:,:,3]
BoostedJets_mask = BoostedJets_Pt > MIN_FJPT
#BoostedJets_mask = BoostedJets_Mass > MIN_FJMASS

Leptons_data = np.transpose(lep_arrays, (1,0,2))
Leptons_Pt = Leptons_data[:,:,0]
Leptons_mask = Leptons_Pt > 20

Taus_data = np.transpose(tau_arrays, (1,0,2))
Taus_Pt = Taus_data[:,:,0]
Taus_mask = Taus_Pt > 20

MET_data = np.transpose(met_arrays, (1,0,2))
MET_mask = MET_data[:,:,0] > 0

HT_data = np.transpose(ht_arrays, (1,0,2))
HT_mask = HT_data[:,:,0] > 0

ERA_data = np.transpose(era_arrays, (1,0,2))
ERA_mask = ERA_data[:,:,0] > 0 

#INDEX_data = np.transpose(index_arrays, (1,0,2))
#INDEX_mask = INDEX_data[:,:,0] > -1

Jet1_data = np.transpose(Jets_arrays['Jet1'],(1,0,2))
Jet1_Mass = Jet1_data[:,:,0]
Jet1_mask = Jet1_Mass > 20

Jet2_data = np.transpose(Jets_arrays['Jet2'],(1,0,2))
Jet2_Mass = Jet2_data[:,:,0]
Jet2_mask = Jet2_Mass > 20

Jet3_data = np.transpose(Jets_arrays['Jet3'],(1,0,2))
Jet3_Mass = Jet3_data[:,:,0]
Jet3_mask = Jet3_Mass > 20

Jet4_data = np.transpose(Jets_arrays['Jet4'],(1,0,2))
Jet4_Mass = Jet4_data[:,:,0]
Jet4_mask = Jet4_Mass > 20

Jet5_data = np.transpose(Jets_arrays['Jet5'],(1,0,2))
Jet5_Mass = Jet5_data[:,:,0]
Jet5_mask = Jet5_Mass > 20

Jet6_data = np.transpose(Jets_arrays['Jet6'],(1,0,2))
Jet6_Mass = Jet6_data[:,:,0]
Jet6_mask = Jet6_Mass > 20

Jet7_data = np.transpose(Jets_arrays['Jet7'],(1,0,2))
Jet7_Mass = Jet7_data[:,:,0]
Jet7_mask = Jet7_Mass > 20

Jet8_data = np.transpose(Jets_arrays['Jet8'],(1,0,2))
Jet8_Mass = Jet8_data[:,:,0]
Jet8_mask = Jet8_Mass > 20

Jet9_data = np.transpose(Jets_arrays['Jet9'],(1,0,2))
Jet9_Mass = Jet9_data[:,:,0]
Jet9_mask = Jet9_Mass > 20


input_dict = {"Jets_data": Jets_data, "Jets_mask": Jets_mask, "BoostedJets_data":BoostedJets_data, "BoostedJets_mask": BoostedJets_mask, "Leptons_data" : Leptons_data, "Leptons_mask" : Leptons_mask, 'Taus_data' : Taus_data, 'Taus_mask': Taus_mask, "MET_data" : MET_data, "MET_mask": MET_mask, 'HT_data': HT_data, "HT_mask" : HT_mask, 'Jet1_data' : Jet1_data, 'Jet1_mask': Jet1_mask, 'Jet2_data' : Jet2_data, 'Jet2_mask': Jet2_mask, 'Jet3_data' : Jet3_data, 'Jet3_mask': Jet3_mask, 'Jet4_data' : Jet4_data, 'Jet4_mask': Jet4_mask, 'Jet5_data' : Jet5_data, 'Jet5_mask': Jet5_mask, 'Jet6_data' : Jet6_data, 'Jet6_mask': Jet6_mask, 'Jet7_data' : Jet7_data, 'Jet7_mask': Jet7_mask, 'Jet8_data' : Jet8_data, 'Jet8_mask': Jet8_mask,'Jet9_data' : Jet9_data, 'Jet9_mask': Jet9_mask, 'ERA_data': ERA_data, 'ERA_mask': ERA_mask }# 'INDEX_data': INDEX_data, 'INDEX_mask': INDEX_mask}


for key, value in input_dict.items():
    print(key, value.shape)

output_nodes = session.get_outputs()
output_names = [node.name for node in output_nodes]
output_values = session.run(output_names, input_dict)


h1_mass = []
h2_mass = []
h3_mass = []

h1_pt = []
h2_pt = []
h3_pt = []

h1_eta = []
h2_eta = []
h3_eta = []

h1_phi = []
h2_phi = []
h3_phi = []

h1_match = []
h2_match = []
h3_match = []

prob_hhh = [] # 1
prob_qcd = [] # 2
prob_tt = [] # 3
prob_vjets = [] # 4
prob_vv = [] # 5
prob_hhh4b2tau = [] # 6
prob_hh4b = [] # 7
prob_hh2b2tau = [] # 8
prob_dy = [] # 9

prob_3bh0h = [] # 1
prob_2bh1h = [] # 2
prob_1bh2h = [] # 3
prob_0bh3h = [] # 4
prob_2bh0h = [] # 5
prob_1bh1h = [] # 6
prob_0bh2h = [] # 7
prob_1bh0h = [] # 8
prob_0bh1h = [] # 9
prob_0bh0h = [] # 10


for i in range(len(output_values[0])):
    best = process(i)
    prob_3bh0h.append(float(output_values[12][i][1])) # based on mapping in SPANET training
    prob_2bh1h.append(float(output_values[12][i][2]))
    prob_1bh2h.append(float(output_values[12][i][3]))
    prob_0bh3h.append(float(output_values[12][i][4]))
    prob_2bh0h.append(float(output_values[12][i][5]))
    prob_1bh1h.append(float(output_values[12][i][6]))
    prob_0bh2h.append(float(output_values[12][i][7]))
    prob_1bh0h.append(float(output_values[12][i][8]))
    prob_0bh1h.append(float(output_values[12][i][9]))
    prob_0bh0h.append(float(output_values[12][i][0]))


#test = [i *0.2 for i in range(10)]

arr_prob_3bh0h = ROOT.VecOps.AsRVec(np.array(prob_3bh0h))
arr_prob_2bh1h = ROOT.VecOps.AsRVec(np.array(prob_2bh1h))
arr_prob_1bh2h = ROOT.VecOps.AsRVec(np.array(prob_1bh2h))
arr_prob_0bh3h = ROOT.VecOps.AsRVec(np.array(prob_0bh3h))

arr_prob_2bh0h = ROOT.VecOps.AsRVec(np.array(prob_2bh0h))
arr_prob_1bh1h = ROOT.VecOps.AsRVec(np.array(prob_1bh1h))
arr_prob_0bh2h = ROOT.VecOps.AsRVec(np.array(prob_0bh2h))

arr_prob_1bh0h = ROOT.VecOps.AsRVec(np.array(prob_1bh0h))
arr_prob_0bh1h = ROOT.VecOps.AsRVec(np.array(prob_0bh1h))

arr_prob_0bh0h = ROOT.VecOps.AsRVec(np.array(prob_0bh0h))

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_3bh0h, "Prob3bh0h_v34")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_2bh1h, "Prob2bh1h_v34")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_1bh2h, "Prob1bh2h_v34")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_0bh3h, "Prob0bh3h_v34")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_2bh0h, "Prob2bh0h_v34")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_1bh1h, "Prob1bh1h_v34")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_0bh2h, "Prob0bh2h_v34")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_1bh0h, "Prob1bh0h_v34")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_0bh1h, "Prob0bh1h_v34")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_0bh0h, "Prob0bh0h_v34")


print("Saving output")
output_path = path.replace('%s'%args.year,'%s-categorisation'%args.year)
if not os.path.isdir(output_path):
    os.makedirs(output_path)

output_name = args.f_in + '_%s'%args.batch_number + '.root'
print(output_path,output_name)

df.Snapshot('Events',output_path + '/' + output_name)
