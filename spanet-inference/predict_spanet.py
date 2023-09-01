import ROOT, os
#ROOT.EnableImplicitMT()


import  onnxruntime 

import numpy as np

# argument parser
import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--f_in', default = 'GluGluToHHHTo6B_SM') # input samples
parser.add_argument('-v','--version', default='v27') # version of NanoNN production
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
    arr = np.triu(arr_in)
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

def process(i):
    max_h1, index_h1 = get_maximas(output_values[0][i])
    max_h2, index_h2 = get_maximas(output_values[1][i])
    max_h3, index_h3 = get_maximas(output_values[2][i])

    h1Det = output_values[3][i]
    h2Det = output_values[4][i]
    h3Det = output_values[5][i]

    higgses = pair_higgs(max_h1.tolist(),index_h1.tolist(), max_h2.tolist(),index_h2.tolist(), max_h3.tolist(),index_h3.tolist(),h1Det,h2Det,h3Det)
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

session = onnxruntime.InferenceSession("/isilon/data/users/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework/spanet-inference/spanet_250epochs_resolved_nolog.onnx")

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

path = '/isilon/data/users/mstamenk/eos-triple-h/samples-%s-%s-nanoaod/'%(args.version,args.year)
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

jet_vars = ["%sPt", "%sEta","%sSinPhi","%sCosPhi", "%sDeepFlavB","%sMass"]
arrays = []


for i in ['1','2','3','4','5','6','7','8','9','10']:
    df = df.Define('jet%sCosPhi'%i, 'TMath::Cos(jet%sPhi)'%i)
    df = df.Define('jet%sSinPhi'%i, 'TMath::Sin(jet%sPhi)'%i)
    df = df.Define('jet%sLogPt'%i, 'TMath::Log(jet%sPt+1)'%i)
    if 'JetHT' in args.f_in or 'BTagCSV' in args.f_in or 'SingleMuon' in args.f_in:
        df = df.Define('jet%sHiggsMatchedIndex'%i,'-1')
    
    column = [el%'jet%s'%i for el in jet_vars]
    np_dict = df.AsNumpy(column)
    np_arr = np.vstack(np_dict[col] for col in column).T.astype(np.float32)
    arrays.append(np_arr)


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


Jets_data = np.transpose(arrays,(1,0,2))
MIN_PT = 20
Jets_Pt = Jets_data[:,:,0]

Jets_mask = Jets_Pt > MIN_PT

input_dict = {"Jets_data": Jets_data, "Jets_mask": Jets_mask}

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

for i in range(len(output_values[0])):
    best = process(i)
    #print(best)

    jets_tmp = jets[i]

    h1_index = get_best(best,0)
    h2_index = get_best(best,1)
    h3_index = get_best(best,2)

    h1 = jets_tmp[int(h1_index[0])] + jets_tmp[int(h1_index[1])]
    h1.HiggsMatchedIndex = jets_tmp[int(h1_index[0])].HiggsMatchedIndex ==  jets_tmp[int(h1_index[1])].HiggsMatchedIndex and jets_tmp[int(h1_index[1])].HiggsMatchedIndex > 0

    h2 = jets_tmp[int(h2_index[0])] + jets_tmp[int(h2_index[1])]
    h2.HiggsMatchedIndex = jets_tmp[int(h2_index[0])].HiggsMatchedIndex ==  jets_tmp[int(h2_index[1])].HiggsMatchedIndex and jets_tmp[int(h2_index[1])].HiggsMatchedIndex > 0

    h3 = jets_tmp[int(h3_index[0])] + jets_tmp[int(h3_index[1])]
    h3.HiggsMatchedIndex = jets_tmp[int(h3_index[0])].HiggsMatchedIndex ==  jets_tmp[int(h3_index[1])].HiggsMatchedIndex and jets_tmp[int(h3_index[1])].HiggsMatchedIndex > 0

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

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h1_mass, "h1_spanet_mass")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h1_pt, "h1_spanet_pt")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h1_eta, "h1_spanet_eta")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h1_phi, "h1_spanet_phi")
df = ROOT.AddBoolArray(ROOT.RDF.AsRNode(df), arr_h1_match, "h1_spanet_match")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h2_mass, "h2_spanet_mass")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h2_pt, "h2_spanet_pt")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h2_eta, "h2_spanet_eta")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h2_phi, "h2_spanet_phi")
df = ROOT.AddBoolArray(ROOT.RDF.AsRNode(df), arr_h2_match, "h2_spanet_match")

df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h3_mass, "h3_spanet_mass")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h3_pt, "h3_spanet_pt")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h3_eta, "h3_spanet_eta")
df = ROOT.AddArray(ROOT.RDF.AsRNode(df), arr_h3_phi, "h3_spanet_phi")
df = ROOT.AddBoolArray(ROOT.RDF.AsRNode(df), arr_h3_match, "h3_spanet_match")

print("Saving output")
output_path = path.replace('%s'%args.year,'%s-spanet-resolved'%args.year)
if not os.path.isdir(output_path):
    os.makedirs(output_path)

output_name = args.f_in + '_%s'%args.batch_number + '.root'
print(output_path,output_name)

df.Snapshot('Events',output_path + '/' + output_name)