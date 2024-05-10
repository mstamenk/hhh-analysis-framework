# Script to store informations to add BDTs from TMVA (and other)

import os, ROOT

root_path = os.environ['MYROOT']
#root_path = '/isilon/data/users/mstamenk/hhh-6b-producer/master/CMSSW_12_5_2/src/hhh-master/hhh-analysis-framework/'

path_bdt_xml = '%s/data/bdt/'%(root_path)

bdts_xml = {
            '2016APV' : [path_bdt_xml+'TMVAClassification_2016APV_v24_regular.xml',path_bdt_xml+'TMVAClassification_2016APV_v24_inverted.xml'],
            '2016' : [path_bdt_xml+'TMVAClassification_2016_v24_regular.xml',path_bdt_xml+'TMVAClassification_2016_v24_inverted.xml'],
            '2017' : [path_bdt_xml+'TMVAClassification_2017_v24_regular.xml',path_bdt_xml+'TMVAClassification_2017_v24_inverted.xml'],
            '2018' : [path_bdt_xml+'TMVAClassification_2018_v24_regular.xml',path_bdt_xml+'TMVAClassification_2018_v24_inverted.xml'],
            #'2017' : ['/isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_12_5_2/src/data/bdt/TMVAClassification_2017_BDT.weights.xml'],
            #'2018' : '/isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_12_5_2/src/data/bdt/TMVAClassification_2018_optimal_BDT.weights.xml'
            }

bdts_xml_boosted = {
            '2016APV' : [path_bdt_xml+'TMVAClassification_2018_v25_regular_boosted.xml',path_bdt_xml+'TMVAClassification_2018_v25_inverted_boosted.xml'],
            '2016' : [path_bdt_xml+'TMVAClassification_2018_v25_regular_boosted.xml',path_bdt_xml+'TMVAClassification_2018_v25_inverted_boosted.xml'],
            '2017' : [path_bdt_xml+'TMVAClassification_2018_v25_regular_boosted.xml',path_bdt_xml+'TMVAClassification_2018_v25_inverted_boosted.xml'],
            '2018' : [path_bdt_xml+'TMVAClassification_2018_v26_regular_boosted_cut.xml',path_bdt_xml+'TMVAClassification_2018_v26_inverted_boosted_cut.xml'],
            }

def init_bdt(df, year):
    if year not in bdts_xml: return
    xmlpath_odd, xmlpath_even = bdts_xml[year]

    ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model_even("{}");'''.format(xmlpath_even))
    nvars = ROOT.model_even.GetVariableNames().size()

    ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model_odd("{}");'''.format(xmlpath_odd))
    nvars = ROOT.model_odd.GetVariableNames().size()

    l_expr = ROOT.model_even.GetVariableNames()
    l_varn = ROOT.std.vector['std::string']()
    l_varn.push_back('event')

    ls_var = ['int event']
    ls_call = ['event']
    ls_bdt = []

    for i_expr, expr in enumerate(l_expr):
        varname = 'v_{}'.format(i_expr)
        l_varn.push_back(varname)
        ls_var.append('float ' + varname)
        ls_call.append(varname)
        ls_bdt.append(varname)

    method_all = ','.join(ls_var)
    method_bdt = ','.join(ls_bdt)
    method_call = ','.join(ls_call)

    # Split even and odd numbers and apply it different mva training
    ROOT.gInterpreter.Declare(" auto computeModel(%s){ auto prediction = model_odd.Compute({%s}); if (event"%(method_all,method_bdt) + "%"+ " 2 == 0) { prediction =  model_even.Compute({%s});} return prediction;}"%(method_bdt))


def add_bdt(df, year):
    if year not in bdts_xml: return df
    xmlpath_odd, xmlpath_even = bdts_xml[year]


    #ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model_even("{}");'''.format(xmlpath_even))
    nvars = ROOT.model_even.GetVariableNames().size()

    #ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model_odd("{}");'''.format(xmlpath_odd))
    nvars = ROOT.model_odd.GetVariableNames().size()

    l_expr = ROOT.model_even.GetVariableNames()
    l_varn = ROOT.std.vector['std::string']()
    l_varn.push_back('event')

    ls_var = ['int event']
    ls_call = ['event']
    ls_bdt = []

    for i_expr, expr in enumerate(l_expr):
        varname = 'v_{}'.format(i_expr)
        l_varn.push_back(varname)
        df=df.Define(varname, '(float)({})'.format(expr) )
        ls_var.append('float ' + varname)
        ls_call.append(varname)
        ls_bdt.append(varname)

    method_all = ','.join(ls_var)
    method_bdt = ','.join(ls_bdt)
    method_call = ','.join(ls_call)

    # Split even and odd numbers and apply it different mva training
    #ROOT.gInterpreter.Declare(" auto computeModel(%s){ auto prediction = model_odd.Compute({%s}); if (event"%(method_all,method_bdt) + "%"+ " 2 == 0) { prediction =  model_even.Compute({%s});} return prediction;}"%(method_bdt))
    df = df.Define('mva', 'computeModel(%s)'%method_call)

    return df


def init_bdt_boosted(df, year): # need to initialise once so that it doesnt create memory issues for multiple processes in for loop
    if year not in bdts_xml_boosted: return
    xmlpath_odd, xmlpath_even = bdts_xml_boosted[year]

    ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model_even_boosted("{}");'''.format(xmlpath_even))
    nvars = ROOT.model_even_boosted.GetVariableNames().size()

    ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model_odd_boosted("{}");'''.format(xmlpath_odd))
    nvars = ROOT.model_odd_boosted.GetVariableNames().size()

    l_expr = ROOT.model_even_boosted.GetVariableNames()
    l_varn = ROOT.std.vector['std::string']()
    l_varn.push_back('event')

    ls_var = ['int event']
    ls_call = ['event']
    ls_bdt = []

    for i_expr, expr in enumerate(l_expr):
        varname = 'v_boosted_{}'.format(i_expr)
        l_varn.push_back(varname)
        #df=df.Define(varname, '(float)({})'.format(expr) )
        ls_var.append('float ' + varname)
        ls_call.append(varname)
        ls_bdt.append(varname)

    method_all = ','.join(ls_var)
    method_bdt = ','.join(ls_bdt)
    method_call = ','.join(ls_call)

    # Split even and odd numbers and apply it different mva training
    ROOT.gInterpreter.Declare(" auto computeModelBoosted(%s){ auto prediction = model_odd_boosted.Compute({%s}); if (event"%(method_all,method_bdt) + "%"+ " 2 == 0) { prediction =  model_even_boosted.Compute({%s});} return prediction;}"%(method_bdt))
    #df = df.Define('mvaBoosted', 'computeModelBoosted(%s)'%method_call)

def add_bdt_boosted(df, year):
    if year not in bdts_xml_boosted: return df
    xmlpath_odd, xmlpath_even = bdts_xml_boosted[year]

    #ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model_even_boosted("{}");'''.format(xmlpath_even))
    nvars = ROOT.model_even_boosted.GetVariableNames().size()

    #ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model_odd_boosted("{}");'''.format(xmlpath_odd))
    nvars = ROOT.model_odd_boosted.GetVariableNames().size()

    l_expr = ROOT.model_even_boosted.GetVariableNames()
    l_varn = ROOT.std.vector['std::string']()
    l_varn.push_back('event')

    ls_var = ['int event']
    #ls_call = ['event']
    ls_call = ['1']
    ls_bdt = []

    for i_expr, expr in enumerate(l_expr):
        varname = 'v_boosted_{}'.format(i_expr)
        l_varn.push_back(varname)
        df=df.Define(varname, '(float)({})'.format(expr) )
        ls_var.append('float ' + varname)
        ls_call.append(varname)
        ls_bdt.append(varname)

    method_all = ','.join(ls_var)
    method_bdt = ','.join(ls_bdt)
    method_call = ','.join(ls_call)

    # Split even and odd numbers and apply it different mva training
    #ROOT.gInterpreter.Declare(" auto computeModelBoosted(%s){ auto prediction = model_odd_boosted.Compute({%s}); if (event"%(method_all,method_bdt) + "%"+ " 2 == 0) { prediction =  model_even_boosted.Compute({%s});} return prediction;}"%(method_bdt))
    df = df.Define('mvaBoosted', 'computeModelBoosted(%s)'%method_call)

    return df


