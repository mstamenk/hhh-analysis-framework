import ROOT
import math
import itertools
from PhysicsTools.NanoNN.helpers.utils import polarP4, deltaR

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

def higgsPairingAlgorithm_v2(event, jets, fatjets, XbbWP, isMC, Run, dotaus=False, taus=[], XtautauWP=0.0, METvars=[]):

    # save jets properties
    dummyJet = polarP4()
    dummyJet.HiggsMatch = False
    dummyJet.HiggsMatchIndex = -1
    dummyJet.FatJetMatch = False
    dummyJet.btagDeepFlavB = -1
    dummyJet.btagPNetB = -1
    dummyJet.DM = -1
    dummyJet.kind = -1
    dummyJet.DeepTauVsJet = -1
    dummyJet.hadronFlavour = -1
    dummyJet.jetId = -1
    dummyJet.puId = -1
    dummyJet.rawFactor = -1
    dummyJet.bRegCorr = -1
    dummyJet.bRegRes = -1
    dummyJet.cRegCorr = -1
    dummyJet.cRegRes = -1
    dummyJet.MatchedGenPt = 0
    dummyJet.mass = 0.

    dummyHiggs = polarP4()
    dummyHiggs.matchH1 = False
    dummyHiggs.matchH2 = False
    dummyHiggs.matchH3 = False
    dummyHiggs.mass = 0.
    dummyHiggs.Mass = 0.
    dummyHiggs.pt = -1
    dummyHiggs.eta = -1
    dummyHiggs.phi = -1
    dummyHiggs.dRjets = 0.

    probetau = sorted([fj for fj in fatjets if fj.Xtautau > XtautauWP], key=lambda x: x.Xtautau, reverse = True)
    if len(probetau)>0:
        probetau = probetau[0]
    probejets = sorted([fj for fj in fatjets if fj.Xbb > XbbWP and fj!=probetau], key=lambda x: x.Xbb, reverse = True)
    if len(probejets) > 4:
        probejets = probejets[:4]
    if probetau!=[]:
        if dotaus:
            if len(probejets) <= 3:
                probejets.append(probetau)
            else:
                probejets = probejets[:3]+[probetau]
        elif probetau.Xbb > XbbWP:
            if len(probejets) <= 3:
                probejets.append(probetau)
            elif probetau.Xbb > probejets[3].Xbb:
                probejets[3] = probetau
        if not dotaus: probetau = []

    if dotaus:
        # Prepare MET variables for FastMTT
        MET_x = METvars[0]*math.cos(METvars[1])
        MET_y = METvars[0]*math.sin(METvars[1])
        covMET = ROOT.TMatrixD(2,2)
        covMET[0][0] = METvars[2]
        covMET[1][0] = METvars[3]
        covMET[0][1] = METvars[3]
        covMET[1][1] = METvars[4]


    jets_4vec = []
    for j in jets:
        overlap = False
        for fj in probejets:
            if deltaR(j,fj) < 0.8: overlap = True
        if overlap == False:
            j_tmp = polarP4(j)
            j_tmp.HiggsMatch = j.HiggsMatch
            j_tmp.HiggsMatchIndex = j.HiggsMatchIndex
            j_tmp.FatJetMatch = j.FatJetMatch
            j_tmp.btagDeepFlavB = j.btagDeepFlavB
            j_tmp.btagPNetB = j.btagPNetB
            j_tmp.DM = -1
            j_tmp.kind = -1
            j_tmp.DeepTauVsJet = -1
            if isMC:
                j_tmp.hadronFlavour = j.hadronFlavour
            j_tmp.jetId = j.jetId
            j_tmp.rawFactor = j.rawFactor
            j_tmp.mass = j.mass
            j_tmp.MatchedGenPt = j.MatchedGenPt
            if Run==2:
                j_tmp.puId = j.puId
                j_tmp.bRegCorr = j.bRegCorr
                j_tmp.bRegRes = j.bRegRes
                j_tmp.cRegCorr = j.cRegCorr
                j_tmp.cRegRes = j.cRegRes

            jets_4vec.append(j_tmp)

    if len(jets_4vec) > 10:
        jets_4vec = jets_4vec[:10]

    jetpairs = []
    for i1,j1 in enumerate(jets_4vec):
      for i2,j2 in enumerate(jets_4vec):
        if i2<=i1: continue
        jetpairs.append((i1,i2,(j1+j2),j1.btagPNetB*j2.btagPNetB,"Jet",(j1+j2).M()))
    jetpairs = sorted([p for p in jetpairs], key=lambda x: x[3], reverse = True)

    taus_4vec = []
    for t in taus:
        overlap = False
        for fj in probejets:
            if deltaR(t,fj) < 0.8: overlap = True
        if overlap == False:
            t_tmp = polarP4(t)
            t_tmp.HiggsMatch = t.HiggsMatch
            t_tmp.HiggsMatchIndex = t.HiggsMatchIndex
            t_tmp.FatJetMatch = t.FatJetMatch
            t_tmp.charge = t.charge
            t_tmp.btagDeepFlavB = -1
            t_tmp.btagPNetB = -1
            t_tmp.kind = t.kind
            t_tmp.DM = t.decayMode
            if Run==2:
                t_tmp.DeepTauVsJet = t.rawDeepTau2017v2p1VSjet
            else:
                t_tmp.DeepTauVsJet = t.rawDeepTau2018v2p5VSjet
            if isMC:
                t_tmp.hadronFlavour = -1
            t_tmp.jetId = -1
            t_tmp.rawFactor = -1
            t_tmp.mass = t.mass
            t_tmp.MatchedGenPt = t.MatchedGenPt
            if Run==2:
                t_tmp.puId = -1
                t_tmp.bRegCorr = -1
                t_tmp.bRegRes = -1
                t_tmp.cRegCorr = -1
                t_tmp.cRegRes = -1

            taus_4vec.append(t_tmp)

    if len(taus_4vec) > 4:
        taus_4vec = taus_4vec[:4]

    taupairs = []
    for i1,t1 in enumerate(taus_4vec):
      for i2,t2 in enumerate(taus_4vec):
        if i2<=i1: continue
        if t1.charge * t2.charge >= 0: continue
        tau1 = ROOT.MeasuredTauLepton(t1.kind, t1.Pt(), t1.Eta(), t1.Phi(), t1.mass, t1.DM)
        tau2 = ROOT.MeasuredTauLepton(t2.kind, t2.Pt(), t2.Eta(), t2.Phi(), t2.mass, t2.DM)
        VectorOfTaus = ROOT.std.vector('MeasuredTauLepton')
        bothtaus = VectorOfTaus()
        bothtaus.push_back(tau1)
        bothtaus.push_back(tau2)
        FMTT = ROOT.FastMTT()
        FMTT.run(bothtaus, MET_x, MET_y, covMET)
        FMTToutput = FMTT.getBestP4()
        FastMTTmass = FMTToutput.M()
        taupairs.append((i1,i2,(t1+t2),t1.DeepTauVsJet*t2.DeepTauVsJet,"Tau",FastMTTmass))
    taupairs = sorted([p for p in taupairs], key=lambda x: x[3], reverse = True)

    allobjects = {}
    for i,fj in enumerate(probejets):
      if fj!=probetau: allobjects["FJ"+str(i+1)] = fj
    if probetau!=[]: allobjects["FatTau"] = probetau
    for i,j in enumerate(jetpairs):
      allobjects["JP_"+str(j[0]+1)+"_"+str(j[1]+1)] = j
    for i,t in enumerate(taupairs):
      allobjects["TauP_"+str(t[0]+1)+"_"+str(t[1]+1)] = t
    objlist_jet = [k for k in allobjects if "J" in k]
    objlist_tau = [k for k in allobjects if "Tau" in k]

    if dotaus:
      # Try to make 3H: 2b+1t
      permutations = manualPermutation(objlist_jet, objlist_jet, objlist_tau)
      if permutations==[]:
        # Either 2b only or 1b+1t
        permnotau = manualPermutation(objlist_jet, objlist_jet)
        permoneb = manualPermutation(objlist_jet, objlist_tau)
        assert permnotau==[] or permoneb==[]
        permutations = permnotau+permoneb
      if permutations==[]:
        # Either 1b only or 1t only
        #assert (objlist_jet==[] or objlist_tau==[]) and len(objlist_jet+objlist_tau)<=3, "Shouldn't this be just one pair? ["+", ".join(objlist_jet)+"] and ["+", ".join(objlist_tau)+"]" # We CAN have multiple Tau pairs! Previous steps fail because there's not a single jet pair
        assert (objlist_jet==[] or objlist_tau==[]) and len(objlist_jet)<=3
        if len(objlist_jet+objlist_tau)>=1:
          permutations = [[obj] for obj in objlist_jet+objlist_tau]
    else:
      # Try 3b
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

    h = []
    for i in range(3):
      h.append(dummyHiggs)
    j = []
    for i in range(6):
      j.append(dummyJet)
    TauIsBoosted = 0
    TauIsResolved = 0
    if permutations==[]: return 0,0,h[0],h[1],h[2],j[0],j[1],j[2],j[3],j[4],j[5],TauIsBoosted,TauIsResolved
    nHiggs = len(permutations[0])
    assert all([nHiggs==len(perm) for perm in permutations])
    assert all([len([name for name in perm if "Tau" in name])<=1 for perm in permutations])

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
        setattr(h[i], "matchH"+str(i+1), h[i].HiggsMatch)
        if Run==2:
          h[i].Mass = h[i].particleNet_mass
        else:
          h[i].Mass = h[i].mass*h[i].particleNet_massCorr
        h[i].dRjets = -1
        if "Tau" in finalPermutation[i]: TauIsBoosted = i+1
      else:
        h[i] = allobjects[finalPermutation[i]][2]
        h[i].Mass = allobjects[finalPermutation[i]][5] # h[i].M()
        h[i].pt = h[i].Pt()
        h[i].eta = h[i].Eta()
        h[i].phi = h[i].Phi()
        setattr(h[i], "matchH"+str(i+1), False)
        if allobjects[finalPermutation[i]][4]=="Jet":
          j[jetCandCount] = jets_4vec[allobjects[finalPermutation[i]][0]]
          j[jetCandCount+1] = jets_4vec[allobjects[finalPermutation[i]][1]]
          h[i].dRjets = deltaR(j[jetCandCount].eta(),j[jetCandCount].phi(),j[jetCandCount+1].eta(),j[jetCandCount+1].phi())
          if j[jetCandCount].HiggsMatch == True and j[jetCandCount+1].HiggsMatch == True and j[jetCandCount].HiggsMatchIndex == j[jetCandCount+1].HiggsMatchIndex:
            setattr(h[i], "matchH"+str(i+1), True)
        elif allobjects[finalPermutation[i]][4]=="Tau":
          j[jetCandCount] = taus_4vec[allobjects[finalPermutation[i]][0]]
          j[jetCandCount+1] = taus_4vec[allobjects[finalPermutation[i]][1]]
          h[i].dRjets = deltaR(j[jetCandCount].eta(),j[jetCandCount].phi(),j[jetCandCount+1].eta(),j[jetCandCount+1].phi())
          if j[jetCandCount].HiggsMatch == True and j[jetCandCount+1].HiggsMatch == True and j[jetCandCount].HiggsMatchIndex == j[jetCandCount+1].HiggsMatchIndex:
            setattr(h[i], "matchH"+str(i+1), True)
        jetCandCount += 2
        if "Tau" in finalPermutation[i]: TauIsResolved = i+1
    if nHiggs==3:
      #if nBoostedH==3: recoidx = 1
      #elif nBoostedH==2: recoidx = 2
      #elif nBoostedH==1: recoidx = 3
      #elif nBoostedH==0: recoidx = 4
      recoidx = 4-nBoostedH
    elif nHiggs==2:
      #if nBoostedH==2: recoidx = 5
      #elif nBoostedH==1: recoidx = 6
      #elif nBoostedH==0: recoidx = 7
      recoidx = 7-nBoostedH
    elif nHiggs==1:
      #if nBoostedH==1: recoidx = 8
      #elif nBoostedH==0: recoidx = 9
      recoidx = 9-nBoostedH
    # return reco_idx, fitted_mass, Higgs 1/2/3, Jets 1/2/3/4/5/6, TauBoosted H Idx, TauResolved H Idx
    return recoidx,m_fit,h[0],h[1],h[2],j[0],j[1],j[2],j[3],j[4],j[5],TauIsBoosted,TauIsResolved