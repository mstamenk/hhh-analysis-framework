# Script to add variables for spanet

import os, ROOT
import itertools


ROOT.ROOT.EnableImplicitMT()


computem = '''
    float computemH(int type, float j1_pt, float j1_eta, float j1_phi, float j1_mass, float j1_breg ,float j2_pt, float j2_eta, float j2_phi, float j2_mass, float j2_breg){
        TLorentzVector j1;
        TLorentzVector j2;

        j1.SetPtEtaPhiM(j1_pt*j1_breg, j1_eta, j1_phi, j1_mass);
        j2.SetPtEtaPhiM(j2_pt*j2_breg, j2_eta, j2_phi, j2_mass);

        if (type == 0) return (j1+j2).M(); 
        else if (type == 1) return (j1+j2).Pt();
        else if (type == 2) return (j1+j2).Eta();
        else if (type == 3) return (j1+j2).Phi();
        else if (type == 4) return j1.DeltaR(j2);
        else return 0;
    }

'''

ROOT.gInterpreter.Declare(computem)


# 12 34 56 78 910
# 13 

unique = []
for j in ['jet1','jet2','jet3','jet4','jet5','jet6','jet7','jet8','jet9','jet10']:
    for k in ['jet1','jet2','jet3','jet4','jet5','jet6','jet7','jet8','jet9','jet10']:
        if j in k and k in j: continue
        perm = [j,k]
        perm_inv = [k,j]


        if perm_inv in unique: continue
        else: unique.append(perm)


#print(unique)
#print(len(unique))

def add_h1_mass_corrected(df):
    j1 = 'bcand1'
    j2 = 'bcand2'
    variables = ['%sPt'%j1,'%sEta'%j1,'%sPhi'%j1,'%sMass'%j1,'%sbRegCorr'%j1,'%sPt'%j2,'%sEta'%j2,'%sPhi'%j2,'%    sMass'%j2,'%sbRegCorr'%j2]
    df = df.Define('h1_breg_mass','computemH(0,%s)'%','.join(variables))
    return df


def add_hhh_variables(df):
    masses = []
    pts = []
    etas = []
    phis = []
    drs = []
    for i in range(len(unique)):
        perm = unique[i]
        j1,j2 = perm
        variables = ['%sPt'%j1,'%sEta'%j1,'%sPhi'%j1,'%sMass'%j1,'%sbRegCorr'%j1,'%sPt'%j2,'%sEta'%j2,'%sPhi'%j2,'%sMass'%j2,'%sbRegCorr'%j2]
        mass = 'mass%s%s'%(j1,j2)
        pt = 'pt%s%s'%(j1,j2)
        eta = 'eta%s%s'%(j1,j2)
        phi = 'phi%s%s'%(j1,j2)
        dr = 'dr%s%s'%(j1,j2)
        df = df.Define(mass, 'computemH(0,%s)'%','.join(variables))
        df = df.Define(pt, 'computemH(1,%s)'%','.join(variables))
        df = df.Define(eta, 'computemH(2,%s)'%','.join(variables))
        df = df.Define(phi, 'computemH(3,%s)'%','.join(variables))
        df = df.Define(dr, 'computemH(4,%s)'%','.join(variables))

        masses.append(mass)
        pts.append(pt)
        etas.append(eta)
        phis.append(phi)
        drs.append(dr)
    return df,masses,pts,etas,phis,drs

def add_hhh_variables_resolved(df):
    masses = []
    pts = []
    etas = []
    phis = []
    drs = []
    for i in range(len(unique)):
        perm = unique[i]
        j1,j2 = perm
        variables = ['%sPt'%j1,'%sEta'%j1,'%sPhi'%j1,'%sMass'%j1,'%sbRegCorr'%j1,'%sPt'%j2,'%sEta'%j2,'%sPhi'%j2,'%sMass'%j2,'%sbRegCorr'%j2]
        mass = 'mass%s%s'%(j1,j2)
        pt = 'pt%s%s'%(j1,j2)
        eta = 'eta%s%s'%(j1,j2)
        phi = 'phi%s%s'%(j1,j2)
        dr = 'dr%s%s'%(j1,j2)
        #df = df.Define(mass, 'computemH(0,%s)/h1_t3_mass'%','.join(variables))
        df = df.Define(mass, 'computemH(0,%s)'%','.join(variables))
        #df = df.Define(pt, 'computemH(1,%s)/h1_t3_pt'%','.join(variables))
        df = df.Define(pt, 'computemH(1,%s)'%','.join(variables))
        df = df.Define(eta, 'computemH(2,%s)'%','.join(variables))
        df = df.Define(phi, 'computemH(3,%s)'%','.join(variables))
        df = df.Define(dr, 'computemH(4,%s)'%','.join(variables))

        masses.append(mass)
        pts.append(pt)
        etas.append(eta)
        phis.append(phi)
        drs.append(dr)
    return df,masses,pts,etas,phis,drs

def add_missing_variables():
    # Missing variables for Run3
    added = []
    for i in range(len(unique)):
        perm = unique[i]
        j1,j2 = perm
        if j1 not in added:
            added.append(j1)
            ROOT.gInterpreter.Declare('float %sbRegCorr = 1.0;'%j1)
        if j2 not in added:
            added.append(j2)
            ROOT.gInterpreter.Declare('float %sbRegCorr = 1.0;'%j2)




#df.Snapshot('Events', 'GluGluToHHHTo6B_SM_spanet.root')


if __name__ == '__main__':
    f_in = 'GluGluToHHHTo6B_SM'

    path = '/isilon/data/users/mstamenk/eos-triple-h/v25/mva-inputs-HLT-boosted-bdt-v25-inclusive-loose-wp-0ptag-2018/inclusive/'

    df = ROOT.RDataFrame('Events',path + '/' + f_in + '.root')
    #j1 = 'jet1'
    #j2 = 'jet2'
    #variables = ['%sPt'%j1,'%sEta'%j1,'%sPhi'%j1,'%sMass'%j1,'%sPt'%j2,'%sEta'%j2,'%sPhi'%j2,'%sMass'%j2]

    #df = df.Define('mH12', 'computemH(0,%s)'%','.join(variables))
    df,masses,pts,etas,phis = add_hhh_variables(df)

    h = df.Histo1D('massjet1jet2')
    h.Draw()


