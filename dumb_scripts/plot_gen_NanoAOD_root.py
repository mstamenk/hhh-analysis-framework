import uproot as urt
import vector
import numpy as np
import awkward as ak
import os
import argparse
import glob
import ROOT

vector.register_awkward()

arraysToGet = ['LHEPart_pt', 'LHEPart_eta', 'LHEPart_phi', 'LHEPart_mass', 'LHEPart_incomingpz', 'LHEPart_pdgId', 'LHEPart_status', 'LHEPart_spin']
treeName = 'Events'

parser = argparse.ArgumentParser()
parser.add_argument('-t', "--tag", help="Tag")
parser.add_argument("-s", "--searchString", help="Search String")
parser.add_argument("-d", "--destination", help="Destination folder")
args = parser.parse_args()

tag = args.tag

fNames = glob.glob(args.searchString.replace("@", "*"))

dataStore = {}

for i, fileName in enumerate(fNames):
    print(f"[{i+1} / {len(fNames)}] Processing file : {fileName}")

    try:
        fileIn = urt.open(fileName)
        if treeName not in fileIn:
            print(f"  > WARNING: '{treeName}' not found in {fileName}, skipping this file.")
            continue

        data = fileIn[treeName].arrays(arraysToGet)
        print(f"  > Obtained file with {len(data)} events ")

        br_list = []
        for ky in data.fields:
            kyN = ky
            if '_' in ky:
                kyN = ky.split("_")[1]
            data[kyN] = data[ky]
            br_list.append(kyN)
        data = data[br_list]
        data = ak.zip({kyz: ak.flatten(data[kyz], axis=0) for kyz in data.fields}, with_name='Momentum4D')

        data = data[data.pdgId == 25]
        pt = data.pt
        srtidx = ak.argsort(pt * -1, axis=1)
        sortedHigsses = data[srtidx]
        data = sortedHigsses
        if tag not in dataStore:
            dataStore[tag] = data
        else:
            dataStore[tag] = ak.concatenate([dataStore[tag], data])

    except Exception as e:
        print(f"  > ERROR: Failed to process {fileName}, skipping this file. Error: {str(e)}")
        continue

feature_store = {}
z = vector.MomentumObject3D.from_xyz(0.0, 0.0, 1.0)
y = vector.MomentumObject3D.from_xyz(0.0, 1.0, 0.0)
for ky in dataStore:
    print("Processing ", ky, f" with {len(dataStore[ky])} entries ")
    higgs = dataStore[ky]
    feature_store[ky] = {}
    h1 = higgs[:, 0]
    h2 = higgs[:, 1]
    h3 = higgs[:, 2]
    hhh = h1 + h2 + h3
    feature_store[ky]['mhhh'] = hhh.mass
    feature_store[ky]['mh1h2'] = (h1 + h2).mass
    feature_store[ky]['mh1h3'] = (h1 + h3).mass

if not os.path.exists(args.destination):
    os.makedirs(args.destination)

for ky in feature_store:
    foutName = f'{args.destination}/{args.tag}.root'
    
    root_file = ROOT.TFile(foutName, 'RECREATE')
    tree = ROOT.TTree('features', 'Extracted Features Tree')

    mhhh = np.zeros(1, dtype=float)
    mh1h2 = np.zeros(1, dtype=float)
    mh1h3 = np.zeros(1, dtype=float)
    
    tree.Branch('mhhh', mhhh, 'mhhh/D')
    tree.Branch('mh1h2', mh1h2, 'mh1h2/D')
    tree.Branch('mh1h3', mh1h3, 'mh1h3/D')
    
    for i in range(len(feature_store[ky]['mhhh'])):
        mhhh[0] = feature_store[ky]['mhhh'][i]
        mh1h2[0] = feature_store[ky]['mh1h2'][i]
        mh1h3[0] = feature_store[ky]['mh1h3'][i]
        tree.Fill()
    
    tree.Write()
    root_file.Close()
