import ROOT, os
#ROOT.EnableImplicitMT()


import  onnxruntime 

import numpy as np

# argument parser
import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--f_in', default = 'GluGluToHHHTo6B_SM') # input samples
parser.add_argument('-v','--version', default='v28') # version of NanoNN production
parser.add_argument('--year', default='2018') # year
parser.add_argument('--batch_size', default='1000000') # year
parser.add_argument('--batch_number',default = '0')
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

    higgses = boosted_higgs + pair_higgs(max_h1.tolist(),index_h1.tolist(), max_h2.tolist(),index_h2.tolist(), max_h3.tolist(),index_h3.tolist(),h1Det,h2Det,h3Det)
    return higgses[0], higgses[1], higgses[2]

# return df.Define(name, [&](ULong64_t e) { return v[e]; }, {"rdfentry_"});
# return df.Define(name, [&](ULong64_t e) { return v[e]; }, {"rdfentry_"});
ROOT.gInterpreter.Declare('''
ROOT::RDF::RNode AddArray(ROOT::RDF::RNode df, ROOT::RVec<double> &v, const std::string &name) {
    return df.Define(name, [&](unsigned int e) { return v[e]; }, {"counter"});
}

ROOT::RDF::RNode AddBoolArray(ROOT::RDF::RNode df, ROOT::RVec<Long64_t> &v, const std::string &name) {
    unsigned rdf_entry = 0;
    return df.Define(name, [&](unsigned int e) { return v[e]; }, {"counter"});
}

unsigned counter = 0;
''')

# Open RDF and onnx session

#session = onnxruntime.InferenceSession("/HEP/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework/spanet-inference/spanet_classification_test.onnx")

sess_options = onnxruntime.SessionOptions()
sess_options.intra_op_num_threads = 23
sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_PARALLEL


session = onnxruntime.InferenceSession("/users/mstamenk/hhh-analysis-framework/spanet-inference/spanet_pnet_v15.onnx",sess_options)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

path = '/users/mstamenk/scratch/mstamenk/samples-%s-%s-nanoaod/'%(args.version,args.year)
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
df = df.Define('counter','counter++')

jet_vars = ["%sPtCorr", "%sEta","%sSinPhi","%sCosPhi", "%sPNetB","%sMass"]
arrays = []


for i in ['1','2','3','4','5','6','7','8','9','10']:
    df = df.Define('jet%sCosPhi'%i, 'TMath::Cos(jet%sPhi)'%i)
    df = df.Define('jet%sSinPhi'%i, 'TMath::Sin(jet%sPhi)'%i)
    df = df.Define('jet%sLogPt'%i, 'TMath::Log(jet%sPt+1)'%i)
    df = df.Define('jet%sPtCorr'%i, 'jet%sPt * jet%sbRegCorr'%(i,i))
    if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
        df = df.Define('jet%sHiggsMatchedIndex'%i,'-1')
    
    column = [el%'jet%s'%i for el in jet_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack(np_dict[col] for col in column).T.astype(np.float32)
    arrays.append(np_arr)

# Boosted arrays
boosted_arrays = []
fatjet_vars = ['fatJet%sPt', 'fatJet%sEta','fatJet%sSinPhi','fatJet%sCosPhi','fatJet%sPNetXbb','fatJet%sPNetXjj','fatJet%sPNetQCD','fatJet%sMass']
for i in ['1','2','3']:
    df = df.Define('fatJet%sCosPhi'%i, 'TMath::Cos(fatJet%sPhi)'%i)
    df = df.Define('fatJet%sSinPhi'%i, 'TMath::Sin(fatJet%sPhi)'%i)
    df = df.Define('fatJet%sLogPt'%i, 'TMath::Log(fatJet%sPt + 1)'%i)
    #if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
    #    df = df.Define('fatJet%sHiggsMatchedIndex'%i,'-1')
    

    column = [el%i for el in fatjet_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack(np_dict[col] for col in column).T.astype(np.float32)
    boosted_arrays.append(np_arr)

lep_arrays = []
lep_vars = ['lep%sPt', 'lep%sEta','lep%sSinPhi','lep%sCosPhi']
for i in ['1','2']:
    df = df.Define('lep%sCosPhi'%i, 'TMath::Cos(lep%sPhi)'%i)
    df = df.Define('lep%sSinPhi'%i, 'TMath::Sin(lep%sPhi)'%i)
    df = df.Define('lep%sLogPt'%i, 'TMath::Log(lep%sPt + 1)'%i)
    #if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
    #    df = df.Define('fatJet%sHiggsMatchedIndex'%i,'-1')
    

    column = [el%i for el in lep_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack(np_dict[col] for col in column).T.astype(np.float32)
    lep_arrays.append(np_arr)

tau_arrays = []
tau_vars = ['tau%sPt', 'tau%sEta','tau%sSinPhi','tau%sCosPhi']
for i in ['1','2']:
    df = df.Define('tau%sCosPhi'%i, 'TMath::Cos(tau%sPhi)'%i)
    df = df.Define('tau%sSinPhi'%i, 'TMath::Sin(tau%sPhi)'%i)
    df = df.Define('tau%sLogPt'%i, 'TMath::Log(tau%sPt + 1)'%i)
    #if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
    #    df = df.Define('fatJet%sHiggsMatchedIndex'%i,'-1')
    
    column = [el%i for el in tau_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack(np_dict[col] for col in column).T.astype(np.float32)
    tau_arrays.append(np_arr)

met_arrays = []
met_vars = ['met']
column = [el for el in met_vars]
np_dict = df.AsNumpy(column)
np_arr = np.vstack(np_dict[col] for col in column).T.astype(np.float32)
met_arrays.append(np_arr)

ht_arrays = []
ht_vars = ['ht']
column = [el for el in ht_vars]
np_dict = df.AsNumpy(column)
np_arr = np.vstack(np_dict[col] for col in column).T.astype(np.float32)
ht_arrays.append(np_arr)


# 4 vectors
jet_4vec = ["%sPt", "%sEta","%sPhi","%sMass","%sHiggsMatchedIndex"]
array_4vec = []
for i in ['1','2','3','4','5','6','7','8','9','10']:
    column_4vec = [el%'jet%s'%i for el in jet_4vec]
    np_4vec = df.AsNumpy(column_4vec)
    np_arr_4vec = np.vstack(np_4vec[col] for col in column_4vec).T
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
    np_arr_4vec = np.vstack(np_4vec[col] for col in column_4vec).T
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
BoostedJets_Mass = BoostedJets_data[:,:,5]
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
HT_mask = MET_data[:,:,0] > 0

input_dict = {"Jets_data": Jets_data, "Jets_mask": Jets_mask, "BoostedJets_data":BoostedJets_data, "BoostedJets_mask": BoostedJets_mask, "Leptons_data" : Leptons_data, "Leptons_mask" : Leptons_mask, 'Taus_data' : Taus_data, 'Taus_mask': Taus_mask, "MET_data" : MET_data, "MET_mask": MET_mask, 'HT_data': HT_data, "HT_mask" : HT_mask}

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


for i in range(len(output_values[0])):
    best = process(i)
    #print(best)

    jets_tmp = jets[i]
    fjets_tmp = fatjets[i]

    h1_index = get_best(best,0)
    h2_index = get_best(best,1)
    h3_index = get_best(best,2)

    if len(h1_index) == 2:
        h1 = jets_tmp[int(h1_index[0])] + jets_tmp[int(h1_index[1])]
        h1.HiggsMatchedIndex = jets_tmp[int(h1_index[0])].HiggsMatchedIndex ==  jets_tmp[int(h1_index[1])].HiggsMatchedIndex and jets_tmp[int(h1_index[1])].HiggsMatchedIndex > 0
    elif len(h1_index) == 3:
        h1 = fjets_tmp[int(h1_index)-110]
        h1.HiggsMatchedIndex = fjets_tmp[int(h1_index)-110].HiggsMatchedIndex > 0


    if len(h2_index) == 2:
        h2 = jets_tmp[int(h2_index[0])] + jets_tmp[int(h2_index[1])]
        h2.HiggsMatchedIndex = jets_tmp[int(h2_index[0])].HiggsMatchedIndex ==  jets_tmp[int(h2_index[1])].HiggsMatchedIndex and jets_tmp[int(h2_index[1])].HiggsMatchedIndex > 0
    elif len(h2_index) == 3:
        h2 = fjets_tmp[int(h2_index)-110]
        h2.HiggsMatchedIndex = fjets_tmp[int(h2_index)-110].HiggsMatchedIndex > 0

    if len(h3_index) == 2:
        h3 = jets_tmp[int(h3_index[0])] + jets_tmp[int(h3_index[1])]
        h3.HiggsMatchedIndex = jets_tmp[int(h3_index[0])].HiggsMatchedIndex ==  jets_tmp[int(h3_index[1])].HiggsMatchedIndex and jets_tmp[int(h3_index[1])].HiggsMatchedIndex > 0
    elif len(h3_index) == 3:
        h3 = fjets_tmp[int(h2_index)-110]
        h3.HiggsMatchedIndex = fjets_tmp[int(h3_index)-110].HiggsMatchedIndex > 0

    higgses = [h1,h2,h3]
    higgses.sort(key= lambda x: x.Pt(), reverse=True)

    h1 = higgses[0]
    h2 = higgses[1]
    h3 = higgses[2]
            
    h1_mass.append(h1.M())
    h1_pt.append(h1.Pt())
    h1_eta.append(h1.Eta())
    h1_phi.append(h1.Phi())

    h2_mass.append(h2.M())
    h2_pt.append(h2.Pt())
    h2_eta.append(h2.Eta())
    h2_phi.append(h2.Phi())

    h3_mass.append(h3.M())
    h3_pt.append(h3.Pt())
    h3_eta.append(h3.Eta())
    h3_phi.append(h3.Phi())

    h1_match.append(int(h1.HiggsMatchedIndex))
    h2_match.append(int(h2.HiggsMatchedIndex))
    h3_match.append(int(h3.HiggsMatchedIndex))

    prob_hhh.append(float(output_values[12][i][1])) # based on mapping in SPANET training
    prob_qcd.append(float(output_values[12][i][2]))
    prob_tt.append(float(output_values[12][i][3]))
    prob_vjets.append(float(output_values[12][i][4]))
    prob_vv.append(float(output_values[12][i][5]))
    prob_hhh4b2tau.append(float(output_values[12][i][6]))
    prob_hh4b.append(float(output_values[12][i][7]))
    prob_hh2b2tau.append(float(output_values[12][i][8]))
    prob_dy.append(float(output_values[12][i][9]))


#test = [i *0.2 for i in range(10)]

arr_h1_mass = ROOT.VecOps.AsRVec(np.array(h1_mass))
arr_h1_pt = ROOT.VecOps.AsRVec(np.array(h1_pt))
arr_h1_eta = ROOT.VecOps.AsRVec(np.array(h1_eta))
arr_h1_phi = ROOT.VecOps.AsRVec(np.array(h1_phi))
arr_h1_match = ROOT.VecOps.AsRVec(np.array(h1_match))


arr_h2_mass = ROOT.VecOps.AsRVec(np.array(h2_mass))
arr_h2_pt = ROOT.VecOps.AsRVec(np.array(h2_pt))
arr_h2_eta = ROOT.VecOps.AsRVec(np.array(h2_eta))
arr_h2_phi = ROOT.VecOps.AsRVec(np.array(h2_phi))
arr_h2_match = ROOT.VecOps.AsRVec(np.array(h2_match))

arr_h3_mass = ROOT.VecOps.AsRVec(np.array(h3_mass))
arr_h3_pt = ROOT.VecOps.AsRVec(np.array(h3_pt))
arr_h3_eta = ROOT.VecOps.AsRVec(np.array(h3_eta))
arr_h3_phi = ROOT.VecOps.AsRVec(np.array(h3_phi))
arr_h3_match = ROOT.VecOps.AsRVec(np.array(h3_match))

arr_prob_hhh = ROOT.VecOps.AsRVec(np.array(prob_hhh))
arr_prob_qcd = ROOT.VecOps.AsRVec(np.array(prob_qcd))
arr_prob_tt = ROOT.VecOps.AsRVec(np.array(prob_tt))
arr_prob_vjets = ROOT.VecOps.AsRVec(np.array(prob_vjets))
arr_prob_vv = ROOT.VecOps.AsRVec(np.array(prob_vv))
arr_prob_hhh4b2tau = ROOT.VecOps.AsRVec(np.array(prob_hhh4b2tau))
arr_prob_hh4b = ROOT.VecOps.AsRVec(np.array(prob_hh4b))
arr_prob_hh2b2tau = ROOT.VecOps.AsRVec(np.array(prob_hh2b2tau))
arr_prob_dy = ROOT.VecOps.AsRVec(np.array(prob_dy))


df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h1_mass, "h1_spanet_boosted_mass")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h1_pt, "h1_spanet_boosted_pt")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h1_eta, "h1_spanet_boosted_eta")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h1_phi, "h1_spanet_boosted_phi")
df = ROOT.AddBoolArray(ROOT.RDF.AsRNode(df), arr_h1_match, "h1_spanet_boosted_match")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h2_mass, "h2_spanet_boosted_mass")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h2_pt, "h2_spanet_boosted_pt")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h2_eta, "h2_spanet_boosted_eta")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h2_phi, "h2_spanet_boosted_phi")
df = ROOT.AddBoolArray(ROOT.RDF.AsRNode(df), arr_h2_match, "h2_spanet_boosted_match")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h3_mass, "h3_spanet_boosted_mass")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h3_pt, "h3_spanet_boosted_pt")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h3_eta, "h3_spanet_boosted_eta")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h3_phi, "h3_spanet_boosted_phi")
df = ROOT.AddBoolArray(ROOT.RDF.AsRNode(df), arr_h3_match, "h3_spanet_boosted_match")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_hhh, "ProbHHH")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_qcd, "ProbQCD")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_tt, "ProbTT")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_vjets, "ProbVJets")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_vv, "ProbVV")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_hhh4b2tau, "ProbHHH4b2tau")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_hh4b, "ProbHH4b")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_hh2b2tau, "ProbHH2b2tau")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_prob_dy, "ProbDY")


print("Saving output")
output_path = path.replace('%s'%args.year,'%s-spanet-boosted-classification'%args.year)
if not os.path.isdir(output_path):
    os.makedirs(output_path)

output_name = args.f_in + '_%s'%args.batch_number + '.root'
print(output_path,output_name)

df.Snapshot('Events',output_path + '/' + output_name)
