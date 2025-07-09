# Script to add jet veto from JERC maps

import ROOT
import correctionlib
correctionlib.register_pyroot_binding()


ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)


computeJetVeto = '''
    int computeJetVeto(float eta, float phi){
        int ret(0);
        
        if (phi > 3.1415) {phi = 3.1415;}
        if (phi < -3.1415) {phi = -3.1415;}

        //std::cout<< eta << " " << phi << " " << jetveto_sf->evaluate({"jetvetomap",eta,phi}) << std::endl;
        if (jetveto_sf->evaluate({"jetvetomap",eta,phi}) > 0) ret=1;
        return ret;
    }
'''


def jetveto_init(year):
    era = {'2016APV': 'Summer19UL16_V0', '2016': 'Summer19UL16_V0', '2017': 'Summer19UL17_V2', '2018': 'Summer19UL18_V1','2022': 'Summer22_23Sep2023','2022EE':'Summer22EE_23Sep2023','2023':'Summer23Prompt23','2023BPIX':'Summer23BPixPrompt23'}[year]
    maps = {'2016APV': 'Summer19UL16_V1', '2016': 'Summer19UL16_V1', '2017': 'Summer19UL17_V1', '2018': 'Summer19UL18_V1','2022': 'Summer22_23Sep2023','2022EE':'Summer22EE_23Sep2023','2023':'Summer23Prompt23','2023BPIX':'Summer23BPixPrompt23'}[year]
    sfDir = '/isilon/data/users/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework/jet-veto-maps/JECDatabase/jet_veto_maps/%s/jetvetomaps.json.gz'%era

    # Jet Veto json
    ROOT.gInterpreter.Declare('auto jetvetojson = correction::CorrectionSet::from_file("%s");'%sfDir)
    print(era)
    ROOT.gInterpreter.Declare('auto jetveto_sf = jetvetojson->at("%s");'%maps)
    ROOT.gInterpreter.Declare(computeJetVeto)
    #ROOT.gInterpreter.ProcessLine('computeJetVeto(-0.433716,-1.1377);')


def addJetVetoFlag(df):
    counter = []
    #for jet in ['jet1','jet2','jet3','jet4','jet5','jet6','jet7','jet8','jet9','jet10','fatJet1','fatJet2','fatJet3']:
    for jet in ['jet1','jet2','jet3','jet4','jet5','jet6']:
        df = df.Define('%sVeto'%(jet),'computeJetVeto(%sEta,%sPhi)'%(jet,jet))
        counter.append('int(%sVeto)'%jet)
    
    selection = '+'.join(counter)

    df = df.Define('PassJetVeto', '(%s) < 1'%selection)

    return df


if __name__ == '__main__':

    path = '/isilon/data/users/mstamenk/eos-triple-h/v33/mva-inputs-2016APV201620172018-categorisation-spanet-boosted-classification/ProbHHH6b_3Higgs_inclusive_CR/'
    #f_in = 'GluGluToHHHTo6B_SM'
    f_in = 'data_obs'

    jetveto_init('2017')

    df = ROOT.RDataFrame('Events', path + '/' + f_in + '.root')

    df = addJetVetoFlag(df)

    df.Snapshot('Events',f_in + '_test.root')