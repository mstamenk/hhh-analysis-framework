import ROOT
import math

def polarP4(obj=None, pt='pt', eta='eta', phi='phi', mass='mass'):
    if obj is None:
        return ROOT.Math.PtEtaPhiMVector()
    pt_val = getattr(obj, pt) if pt else 0
    eta_val = getattr(obj, eta) if eta else 0
    phi_val = getattr(obj, phi) if phi else 0
    mass_val = getattr(obj, mass) if mass else 0
    return ROOT.Math.PtEtaPhiMVector(pt_val, eta_val, phi_val, mass_val)

def deltaR2(eta1, phi1, eta2=None, phi2=None):
    if eta2 is None:
        a, b = eta1, phi1
        return deltaR2(a.eta, a.phi, b.eta, b.phi)
    else:
        deta = eta1 - eta2
        dphi = deltaPhi(phi1, phi2)
        return deta * deta + dphi * dphi


def deltaR(eta1, phi1, eta2=None, phi2=None):
    return math.sqrt(deltaR2(eta1, phi1, eta2, phi2))


def manualPermutation(input1, input2, input3=[0]):
  output = []
  for i1,v1 in enumerate(input1):
    for i2,v2 in enumerate(input2):
      if v1==v2 or (input1==input2 and i2<=i1): continue
      if v1.startswith("JP") and v2.startswith("JP") and len(list(set(v1.split("_")[1:]+v2.split("_")[1:])))<4: continue
      if v1.startswith("TauP") and v2.startswith("TauP") and len(list(set(v1.split("_")[1:]+v2.split("_")[1:])))<4: continue
      for i3,v3 in enumerate(input3):
        if v3!=0:
          if v1==v3 or (input1==input3 and i3<=i1): continue
          if v2==v3 or (input2==input3 and i3<=i2): continue
          if v1.startswith("JP") and v3.startswith("JP") and len(list(set(v1.split("_")[1:]+v3.split("_")[1:])))<4: continue
          if v1.startswith("TauP") and v3.startswith("TauP") and len(list(set(v1.split("_")[1:]+v3.split("_")[1:])))<4: continue
          if v2.startswith("JP") and v3.startswith("JP") and len(list(set(v2.split("_")[1:]+v3.split("_")[1:])))<4: continue
          if v2.startswith("TauP") and v3.startswith("TauP") and len(list(set(v2.split("_")[1:]+v3.split("_")[1:])))<4: continue
          output.append([v1,v2,v3])
        else:
          output.append([v1,v2])
  return output

jet_list = []
fatjet_list = []

probejets = sorted([fj for fj in fatjets if fj.Xbb > XbbWP and fj!=probetau], key=lambda x: x.Xbb, reverse = True)


jetpairs = []
    for i1,j1 in enumerate(jets_4vec):
      for i2,j2 in enumerate(jets_4vec):
        if i2<=i1: continue
        jetpairs.append((i1,i2,(j1+j2),j1.btagPNetB*j2.btagPNetB,"Jet",(j1+j2).M()))
    jetpairs = sorted([p for p in jetpairs], key=lambda x: x[3], reverse = True)

allobjects = {}
    for i,fj in enumerate(probejets):
        allobjects["FJ"+str(i+1)] = fj
   
    for i,j in enumerate(jetpairs):
      allobjects["JP_"+str(j[0]+1)+"_"+str(j[1]+1)] = j
    
    objlist_jet = [k for k in allobjects if "J" in k]


permutations = manualPermutation(objlist_jet, objlist_jet, objlist_jet)
if permutations==[]:
# Try 2b
permutations = manualPermutation(objlist_jet, objlist_jet)
if permutations==[]:
# Either 1b or 0b
# "Worst case" can still have 3 jets, so 3 jet pairs. Since list is b-score-sorted, will just choose the one with highest score
assert len(objlist_jet)<=3
if len(objlist_jet)>=1:
    permutations = [[obj] for obj in objlist_jet]
nHiggs = len(permutations[0])

h = []
for i in range(3):
    h.append(dummyHiggs)
j = []
for i in range(6):
    j.append(dummyJet)

min_chi2 = 1000000000000000
for permutation in permutations:
    masses = []
    for name in permutation:
    thismass = allobjects[name].mass if name.startswith("F") else allobjects[name][5]
    masses.append(thismass)
    fitted_mass = sum(masses)/nHiggs
    chi2 = 0.0
    for m in masses:
    chi2 += (m - fitted_mass)**2
    if chi2 < min_chi2:
    m_fit = fitted_mass
    min_chi2 = chi2
    finalPermutation = permutation
    if nHiggs==1: break # Use the jet pair with highest score, which will be always the first
nBoostedH = len([name for name in finalPermutation if name.startswith("F")])
jetCandCount = 0
    for i in range(nHiggs):
      if finalPermutation[i].startswith("F"):
        h[i] = allobjects[finalPermutation[i]]
        if Run==2:
          h[i].Mass = h[i].particleNet_mass
        else:
          h[i].Mass = h[i].mass*h[i].particleNet_massCorr
        h[i].dRjets = -1
      else:
        h[i] = allobjects[finalPermutation[i]][2]
        h[i].Mass = allobjects[finalPermutation[i]][5] # h[i].M()
        h[i].pt = h[i].Pt()
        h[i].eta = h[i].Eta()
        h[i].phi = h[i].Phi()
        setattr(h[i], "matchH"+str(i+1), False)
    
    # return reco_idx, fitted_mass, Higgs 1/2/3, Jets 1/2/3/4/5/6, TauBoosted H Idx, TauResolved H Idx
    # should add Higgs pt eta phi
    return m_fit,h[0],h[1],h[2],j[0],j[1],j[2],j[3],j[4],j[5]