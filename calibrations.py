# Utility to add calibrations
# git clone ssh://git@gitlab.cern.ch:7999/cms-nanoAOD/jsonpog-integration.git

import os
import ROOT
import correctionlib
correctionlib.register_pyroot_binding()



def addBTagSF(df, f_in): # shape scale factors for MVA
    if 'JetHT' in f_in or 'BTagCSV' in f_in:
        df = df.Define('bcand1BTagSF', '1')
        df = df.Define('bcand2BTagSF', '1')
        df = df.Define('bcand3BTagSF', '1')
        df = df.Define('bcand4BTagSF', '1')
        df = df.Define('bcand5BTagSF', '1')
        df = df.Define('bcand6BTagSF', '1')
        df = df.Define('jet7BTagSF', '1')
        df = df.Define('jet8BTagSF', '1')
        df = df.Define('jet9BTagSF', '1')
        df = df.Define('jet10BTagSF', '1')
    else:
        df = df.Define('bcand1BTagSF', 'btvjson_shape->evaluate({"central",int(round(bcand1HadronFlavour)),std::abs(bcand1Eta),bcand1Pt,bcand1DeepFlavB})')
        df = df.Define('bcand2BTagSF', 'btvjson_shape->evaluate({"central",int(round(bcand2HadronFlavour)),std::abs(bcand2Eta),bcand2Pt,bcand2DeepFlavB})')
        df = df.Define('bcand3BTagSF', 'btvjson_shape->evaluate({"central",int(round(bcand3HadronFlavour)),std::abs(bcand3Eta),bcand3Pt,bcand3DeepFlavB})')
        df = df.Define('bcand4BTagSF', 'btvjson_shape->evaluate({"central",int(round(bcand4HadronFlavour)),std::abs(bcand4Eta),bcand4Pt,bcand4DeepFlavB})')
        df = df.Define('bcand5BTagSF', 'btvjson_shape->evaluate({"central",int(round(bcand5HadronFlavour)),std::abs(bcand5Eta),bcand5Pt,bcand5DeepFlavB})')
        df = df.Define('bcand6BTagSF', 'btvjson_shape->evaluate({"central",int(round(bcand6HadronFlavour)),std::abs(bcand6Eta),bcand6Pt,bcand6DeepFlavB})')
        df = df.Define('jet7BTagSF', 'btvjson_shape->evaluate({"central",int(round(jet7HadronFlavour)),std::abs(jet7Eta),jet7Pt,jet7DeepFlavB})')
        df = df.Define('jet8BTagSF', 'btvjson_shape->evaluate({"central",int(round(jet8HadronFlavour)),std::abs(jet8Eta),jet8Pt,jet8DeepFlavB})')
        df = df.Define('jet9BTagSF', 'btvjson_shape->evaluate({"central",int(round(jet9HadronFlavour)),std::abs(jet9Eta),jet9Pt,jet9DeepFlavB})')
        df = df.Define('jet10BTagSF', 'btvjson_shape->evaluate({"central",int(round(jet10HadronFlavour)),std::abs(jet10Eta),jet10Pt,jet10DeepFlavB})')

    return df


computeLooseBTAGSF = '''
    float computeLooseBTagsEffSFPerFlavour(int hadronFlavour, float eta, float pt){
        float sf;
        if (hadronFlavour == 0) { sf = btvjson_incl->evaluate({"central","L",hadronFlavour,eta,pt});  }
        else { sf = btvjson_comb->evaluate({"central","L",hadronFlavour,eta,pt});} 
        return sf;
    }
'''

computeMediumBTAGSF = '''
    float computeMediumBTagsEffSFPerFlavour(int hadronFlavour, float eta, float pt){
        float sf;
        if (hadronFlavour == 0) { sf = btvjson_incl->evaluate({"central","M",hadronFlavour,eta,pt});  }
        else {sf = btvjson_comb->evaluate({"central","M",hadronFlavour,eta,pt});} 
        return sf;
    }
'''

computeTightBTAGSF = '''
    float computeTightBTagsEffSFPerFlavour(int hadronFlavour, float eta, float pt){
        float sf;
        if (hadronFlavour == 0) { sf = btvjson_incl->evaluate({"central","T",hadronFlavour,eta,pt});  }
        else {sf = btvjson_comb->evaluate({"central","T",hadronFlavour,eta,pt});} 
        return sf;
    }
'''

def btag_init(year):
    if year in ['2016APV', '2016', '2017', '2018']:
        sfDir = os.path.join(os.environ["CMSSW_BASE"], 'src/jsonpog-integration/POG/BTV/%s_UL/btagging.json.gz'%year)
    elif year == '2022':
        sfDir = os.path.join(os.environ["CMSSW_BASE"], 'src/jsonpog-integration/POG/BTV/2022_Summer22/btagging.json.gz')
    elif year == '2022EE':
        sfDir = os.path.join(os.environ["CMSSW_BASE"], 'src/jsonpog-integration/POG/BTV/2022_Summer22EE/btagging.json.gz')
    ROOT.gInterpreter.Declare('auto btvjson = correction::CorrectionSet::from_file("%s");'%sfDir)
    if year in ['2016APV', '2016', '2017', '2018']:
        ROOT.gInterpreter.Declare('auto btvjson_shape = btvjson->at("deepJet_shape");')
        ROOT.gInterpreter.Declare('auto btvjson_comb = btvjson->at("deepJet_comb");') # bc
        ROOT.gInterpreter.Declare('auto btvjson_incl = btvjson->at("deepJet_incl");') # light
        ROOT.gInterpreter.Declare(computeLooseBTAGSF)
        ROOT.gInterpreter.Declare(computeMediumBTAGSF)
        ROOT.gInterpreter.Declare(computeTightBTAGSF)
    elif year in ['2022', '2022EE']:
        # No SFs available yet; just WPs
        ROOT.gInterpreter.Declare('float computeLooseBTagsEffSFPerFlavour(int hadronFlavour, float eta, float pt){return 1.0;}')
        ROOT.gInterpreter.Declare('float computeMediumBTagsEffSFPerFlavour(int hadronFlavour, float eta, float pt){return 1.0;}')
        ROOT.gInterpreter.Declare('float computeTightBTagsEffSFPerFlavour(int hadronFlavour, float eta, float pt){return 1.0;}')



def addBTagEffSF(df,f_in,wp):

    if 'JetHT' in f_in or 'BTagCSV' in f_in:
        if wp == 'loose':
            df = df.Define('jet1LooseBTagEffSF', '1')
            df = df.Define('jet2LooseBTagEffSF', '1')
            df = df.Define('jet3LooseBTagEffSF', '1')
            df = df.Define('jet4LooseBTagEffSF', '1')
            df = df.Define('jet5LooseBTagEffSF', '1')
            df = df.Define('jet6LooseBTagEffSF', '1')
        elif wp == 'medium':
            df = df.Define('jet1MediumBTagEffSF', '1')
            df = df.Define('jet2MediumBTagEffSF', '1')
            df = df.Define('jet3MediumBTagEffSF', '1')
            df = df.Define('jet4MediumBTagEffSF', '1')
            df = df.Define('jet5MediumBTagEffSF', '1')
            df = df.Define('jet6MediumBTagEffSF', '1')
        elif wp == 'tight':
            df = df.Define('jet1TightBTagEffSF', '1')
            df = df.Define('jet2TightBTagEffSF', '1')
            df = df.Define('jet3TightBTagEffSF', '1')
            df = df.Define('jet4TightBTagEffSF', '1')
            df = df.Define('jet5TightBTagEffSF', '1')
            df = df.Define('jet6TightBTagEffSF', '1')
    else: 
        if wp == 'loose':
            name = 'LooseBTagEffSF'
            script = 'computeLooseBTagsEffSFPerFlavour'
        elif wp == 'medium':
            name = 'MediumBTagEffSF'
            script = 'computeMediumBTagsEffSFPerFlavour'
        elif wp == 'tight':
            name = 'TightBTagEffSF'
            script = 'computeTightBTagsEffSFPerFlavour'
        df = df.Define('jet1%s'%name, "%s(int(round(jet1HadronFlavour)),std::abs(jet1Eta),jet1Pt)"%script)
        df = df.Define('jet2%s'%name, "%s(int(round(jet2HadronFlavour)),std::abs(jet2Eta),jet2Pt)"%script)
        df = df.Define('jet3%s'%name, "%s(int(round(jet3HadronFlavour)),std::abs(jet3Eta),jet3Pt)"%script)
        df = df.Define('jet4%s'%name, "%s(int(round(jet4HadronFlavour)),std::abs(jet4Eta),jet4Pt)"%script)
        df = df.Define('jet5%s'%name, "%s(int(round(jet5HadronFlavour)),std::abs(jet5Eta),jet5Pt)"%script)
        df = df.Define('jet6%s'%name, "%s(int(round(jet6HadronFlavour)),std::abs(jet6Eta),jet6Pt)"%script)
    return df



