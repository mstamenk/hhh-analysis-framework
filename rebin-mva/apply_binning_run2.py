import os, ROOT,glob

import ctypes

# Test : nAK4 >= 6 and nprobejets >= 2 [1.0, 0.9971, 0.9944, 0.9904, 0.9831, 0.9695, 0.9458] 
# nAK4 < 6 nprobejets >= 2: [1.0, 0.9969, 0.9938, 0.9876, 0.9741, 0.9394, 0.8229]
# nAK4 >= 6 nprobejets == 1: [1.0, 0.9988, 0.9983, 0.9979, 0.9976, 0.9973, 0.997, 0.9967, 0.9964, 0.9961, 0.9957, 0.9954, 0.9952, 0.995, 0.9948, 0.9945, 0.9942, 0.9939, 0.9936, 0.9933, 0.9931, 0.9927, 0.9923, 0.992, 0.9916, 0.9913, 0.9909, 0.9905, 0.9902, 0.9899, 0.9895, 0.989, 0.9886, 0.9882, 0.9878, 0.9874, 0.9869, 0.9863999999999999, 0.986, 0.9855, 0.9851, 0.9846, 0.9841, 0.9835, 0.983, 0.9826, 0.9822, 0.9817, 0.9812, 0.9806, 0.9801, 0.9795, 0.9791, 0.9786, 0.9781, 0.9776, 0.977, 0.9763, 0.9758, 0.975, 0.9745, 0.9738, 0.9732, 0.9726, 0.9718, 0.9712, 0.9705, 0.9701, 0.9694, 0.9687, 0.9682, 0.9676, 0.9668, 0.966, 0.9654, 0.9646, 0.9638, 0.9631, 0.9621999999999999, 0.9614, 0.9606, 0.9599, 0.9591, 0.9581999999999999, 0.9572, 0.9564, 0.9556, 0.9544, 0.9536, 0.9528, 0.9521, 0.951, 0.9501, 0.9491, 0.9478, 0.9468, 0.9458, 0.9451, 0.9440999999999999, 0.943, 0.9423, 0.9414, 0.9405, 0.9396, 0.9383, 0.9371, 0.9359, 0.935, 0.9338, 0.9323, 0.9312, 0.9301, 0.9284, 0.927, 0.9258, 0.9251, 0.9238999999999999, 0.9224, 0.9215, 0.9207, 0.9191, 0.9174, 0.9165, 0.9149, 0.9136, 0.9124, 0.9113, 0.9096, 0.9077999999999999, 0.906, 0.9045, 0.9033, 0.9015, 0.8997999999999999, 0.8984, 0.8966, 0.8946, 0.8931, 0.8916, 0.8901, 0.8887, 0.8874, 0.8855999999999999, 0.8838, 0.8819, 0.8805, 0.8783, 0.8764, 0.8748, 0.8731, 0.8713, 0.8693, 0.8675999999999999, 0.8658, 0.8633, 0.8613, 0.8599, 0.8569, 0.8547, 0.8527, 0.8506, 0.849, 0.847, 0.8447, 0.8429, 0.8406, 0.8386, 0.8368, 0.8344, 0.8329, 0.8308, 0.8285, 0.8261000000000001, 0.8243, 0.8224, 0.8199, 0.8171999999999999, 0.8153, 0.8122, 0.8089999999999999, 0.8069, 0.8042, 0.802]
# nAK4 < 6  nprobejets == 1: [1.0, 0.9957, 0.9928, 0.9894, 0.9848, 0.9786, 0.9714, 0.9624, 0.9513, 0.9392, 0.9248, 0.9087, 0.8908, 0.8709, 0.8466, 0.8167]

ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(ROOT.kTRUE)


import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v31')
parser.add_argument('--year', default='2016APV201620172018')
parser.add_argument('--prob', default='ProbHHH6b')

args = parser.parse_args()

def convert_list_to_dict(ls):
    length = len(ls)
    ret = {}
    for i in range(length):
        index = length - (i + 1)
        if i > 0:
            upper = ls[index]
            lower = ls[index+1]
            print(lower,upper)
            ret[i] = [lower,upper]
    return ret


years = {'2018' : [1.0, 0.7095, 0.693, 0.6815, 0.6719999999999999, 0.6639999999999999, 0.6565, 0.6499999999999999, 0.6435, 0.6375, 0.632],
         '2017' : [1.0, 0.6915, 0.6705, 0.6549999999999999, 0.6419999999999999, 0.6305, 0.6194999999999999, 0.609, 0.599, 0.589, 0.579], 
         '2016' : [1.0, 0.695, 0.6755, 0.6615, 0.6505, 0.6405, 0.6315, 0.6234999999999999, 0.616, 0.6084999999999999, 0.6014999999999999],
         '2016APV': [1.0, 0.6859999999999999, 0.6645, 0.649, 0.6365, 0.6255, 0.615, 0.6054999999999999, 0.5964999999999999, 0.5874999999999999, 0.579], 
}



bins_ProbHH4b_2Higgs = [1.0, 0.9973, 0.9961, 0.9948, 0.9934, 0.9917, 0.9897, 0.9874, 0.9847, 0.9814, 0.9775, 0.9731]

#bins_ProbHH4b_2Higgs = [1.0 - 0.01 * i for i in range(10)] 

#bins_ProbHHH6b_3Higgs = [1.0, 0.697, 0.6775, 0.6635, 0.6519999999999999, 0.6415, 0.6319999999999999, 0.6234999999999999, 0.615, 0.607, 0.599]
#bins_ProbHHH6b_3Higgs = [1.0, 0.7015, 0.6835, 0.6705, 0.6599999999999999, 0.6505, 0.6419999999999999, 0.6339999999999999, 0.6265, 0.6194999999999999, 0.6124999999999999]

bins_ProbHHH6b_3Higgs = [1.0, 0.705, 0.688, 0.6755, 0.6655, 0.657, 0.649, 0.642, 0.635, 0.6285, 0.6224999999999999, 0.6164999999999999, 0.6104999999999999, 0.605, 0.5994999999999999, 0.594, 0.5885, 0.583]
#bins_ProbHHH6b_3Higgs = [1.0 - 0.01 * i for i in range(10)] #[1.0, 0.59] + [0.54 - 0.05 * i for i in range(10)]
bins_ProbHHH6b_3Higgs = [1.0, 0.996, 0.9935, 0.991, 0.9884, 0.9857, 0.9829, 0.98, 0.977, 0.9739, 0.9708]
bins_ProbHHH6b_2Higgs = [1.0] + [0.644 - 0.06 * i for i in range(10)]
bins_ProbVV_2Higgs = [1.0] + [0.57 - 0.05 * i for i in range(10)]

categories = {            
            'ProbHH4b_3bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_2bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_1bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh3h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_2bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_1bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_1bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh0h_inclusive' : '(nprobejets > -1)',

            'ProbHH4b_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_3Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_1Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHH4b_0bh0h_inclusive' : '(nprobejets > -1)',

            'ProbHHH6b_1Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_3Higgs_inclusive' : '(nprobejets > -1)',

            'ProbVV_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbVV_2bh0h_inclusive' : '(nprobejets > -1)',
            'ProbVV_1bh1h_inclusive' : '(nprobejets > -1)',
            'ProbVV_0bh2h_inclusive' : '(nprobejets > -1)',

            'ProbHHH6b_1Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_2Higgs_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_3Higgs_inclusive' : '(nprobejets > -1)',

            'ProbHHH6b_3bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_2bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_1bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_0bh3h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_2bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_1bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_0bh2h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_1bh0h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_0bh1h_inclusive' : '(nprobejets > -1)',
            'ProbHHH6b_0bh0h_inclusive' : '(nprobejets > -1)',
}

binnings = {


    'ProbHH4b_3bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1bh2h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh3h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh2h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh1h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    
    'ProbHH4b_3Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_2Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_1Higgs_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),
    'ProbHH4b_0bh0h_inclusive' : convert_list_to_dict(bins_ProbHH4b_2Higgs),

    'ProbHHH6b_3Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_1Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_2Higgs_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),

    'ProbVV_2Higgs_inclusive' : convert_list_to_dict(bins_ProbVV_2Higgs),
    'ProbVV_2bh0h_inclusive' : convert_list_to_dict(bins_ProbVV_2Higgs),
    'ProbVV_1bh1h_inclusive' : convert_list_to_dict(bins_ProbVV_2Higgs),
    'ProbVV_0bh2h_inclusive' : convert_list_to_dict(bins_ProbVV_2Higgs),

    'ProbHHH6b_3bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_2bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_1bh2h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_0bh3h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),

    'ProbHHH6b_2bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_1bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_0bh2h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),

    'ProbHHH6b_1bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_0bh1h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),
    'ProbHHH6b_0bh0h_inclusive' : convert_list_to_dict(bins_ProbHHH6b_3Higgs),




}

variables = {
            'ProbHH4b_2Higgs_inclusive' : 'ProbMultiH',

            'ProbHH4b_3bh0h_inclusive' : 'ProbMultiH',
            'ProbHH4b_2bh1h_inclusive' : 'ProbMultiH',
            'ProbHH4b_1bh2h_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh3h_inclusive' : 'ProbMultiH',
            'ProbHH4b_2bh0h_inclusive' : 'ProbMultiH',
            'ProbHH4b_1bh1h_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh2h_inclusive' : 'ProbMultiH',
            'ProbHH4b_1bh0h_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh1h_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh0h_inclusive' : 'ProbMultiH',

            'ProbHHH6b_3bh0h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_2bh1h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_1bh2h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_0bh3h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_2bh0h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_1bh1h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_0bh2h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_1bh0h_inclusive' : 'ProbMultiH',
            'ProbHHH6b_0bh1h_inclusive' : 'ProbMultiH',
            


            'ProbHH4b_2Higgs_inclusive' : 'ProbMultiH',
            'ProbHH4b_3Higgs_inclusive' : 'ProbMultiH',
            'ProbHH4b_1Higgs_inclusive' : 'ProbMultiH',
            'ProbHH4b_0bh0h_inclusive' : 'ProbMultiH',

            'ProbHHH6b_1Higgs_inclusive' : 'ProbMultiH',
            'ProbHHH6b_2Higgs_inclusive' : 'ProbMultiH',
            'ProbHHH6b_3Higgs_inclusive' : 'ProbMultiH',
            'ProbHHH6b_0bh0h_inclusive' : 'ProbMultiH',
            #'ProbVV_2Higgs_inclusive' : 'ProbVV',
            #'ProbVV_0bh2h_inclusive' : 'ProbVV',
            #'ProbVV_2bh0h_inclusive' : 'ProbVV',
            #'ProbVV_1bh1h_inclusive' : 'ProbVV',
}





def get_integral_and_error(hist):
    integral = hist.Integral()
    error = ctypes.c_double(0.0)
    hist.IntegralAndError(0, hist.GetNbinsX() + 1, error)
    return integral, error.value


year = args.year
version = args.version

#path = '/isilon/data/users/mstamenk/eos-triple-h/v28-categorisation/mva-inputs-2018-categorisation-spanet-boosted-classification/'
path = '/isilon/data/users/mstamenk/eos-triple-h/%s/mva-inputs-%s-categorisation-spanet-boosted-classification/'%(version,year)

cat = 'ProbHHH6b_1Higgs_inclusive'
option = '_SR'

prob = args.prob

for cat in ['%s_2Higgs_inclusive','%s_1Higgs_inclusive','%s_3Higgs_inclusive','%s_0bh0h_inclusive']:# variables:
    cat = cat%prob
    print(binnings[cat])
    target = '%s%s/histograms'%(cat,option)

    if not os.path.isdir(path + '/' + target):
        os.makedirs(path+'/'+target)

    file_path = '%s'%cat + option +'/'

    samples = glob.glob(path.replace('2016APV201620172018','2018')+'/'+file_path+'/*.root')
    samples = [os.path.basename(s).replace('.root','') for s in samples if 'QCD' not in s and ('GluGlu' in s or 'data_obs' in s)]

    outfile = ROOT.TFile(path +'/' + target + '/' + 'histograms_ProbMultiH.root','recreate')

    #samples = ['GluGluToHHHTo6B_SM']

    var = variables[cat]

    binning = binnings[cat]
    cut = categories[cat]

    data_yield = 0
    bkg_yield = 0

    for s in samples:
        print(s)
        f_name = []
        f_name.append(path.replace('2016APV201620172018','2016APV') + '/' + file_path + '/' + s + '.root')
        f_name.append(path.replace('2016APV201620172018','2016') + '/' + file_path + '/' + s + '.root')
        f_name.append(path.replace('2016APV201620172018','2017') + '/' + file_path + '/' + s + '.root')
        f_name.append(path.replace('2016APV201620172018','2018') + '/' + file_path + '/' + s + '.root')

        print(f_name)

        #tree = ROOT.TChain('Events')
        #tree.AddFile(f_name)
        df = ROOT.RDataFrame('Events', f_name, [var])

        if 'JetHT' in s:
            h_mva = ROOT.TH1F('data_obs','data_obs',len(binning),0,len(binning))
        else:
            h_mva = ROOT.TH1F(s,s,len(binning),0,len(binning))
        for i in range(1,h_mva.GetNbinsX() + 1):

            low,up = binning[i]
        
            h_name = s + '_histo_%d'%i
            #tree.Draw("%s>>%s(100,0,1)"%(var,h_name),'(%s && %s > %f && %s < %f ) * totalWeight'%(cut, var,low, var,up))
            h = df.Filter('(%s && %s > %f && %s < %f )'%(cut, var,low, var,up)).Histo1D((h_name,h_name,100,0,1),var,'totalWeight')
            try:
                #h = ROOT.gPad.GetPrimitive(h_name)
                h = h.GetValue()
                integral, error = get_integral_and_error(h)
            except: continue
            
            print(i,integral,error)
            h_mva.SetBinContent(i,integral)
            h_mva.SetBinError(i,error)
        if 'data_obs' in s:
            data_yield = h_mva.Integral() 
        if 'data_obs' not in s:
            bkg_yield += h_mva.Integral()   

        
        #h_mva.Rebin(2)
        #if 'data_obs' not in s:
        #if 'QCD' in s:
        #    h_mva.Scale(0.47)
        outfile.cd()
        h_mva.Write()


    #tree = ROOT.TChain('Events')
    #tree.AddFile(path + '/' + file_path + '/' + 'QCD' + '.root')
    #tree.AddFile(path + '/' + file_path + '/' + 'QCD_modelling' + '.root')
    #tree.AddFile(path + '/' + file_path + '/' + 'QCD_datadriven_data' + '.root')

    s = 'QCD_datadriven_data' 
    f_name = []
    f_name.append(path.replace('2016APV201620172018','2016APV') + '/' + file_path + '/' + s + '.root')
    f_name.append(path.replace('2016APV201620172018','2016') + '/' + file_path + '/' + s + '.root')
    f_name.append(path.replace('2016APV201620172018','2017') + '/' + file_path + '/' + s + '.root')
    f_name.append(path.replace('2016APV201620172018','2018') + '/' + file_path + '/' + s + '.root')
    df = ROOT.RDataFrame('Events', f_name, [var])
    h_mva = ROOT.TH1F('QCD','QCD',len(binning),0,len(binning))
    print('QCD')
    for i in range(1,h_mva.GetNbinsX() + 1):

        low,up = binning[i]

        h_name = 'QCD' + '_histo_%d'%i
        #tree.Draw("%s>>%s(100,0,1)"%(var,h_name),'(%s && %s > %f && %s < %f ) * totalWeight'%(cut, var,low, var,up))
        h = df.Filter('(%s && %s > %f && %s < %f )'%(cut, var,low, var,up)).Histo1D((h_name,h_name,100,0,1),var,'totalWeight')
        try:
            #h = ROOT.gPad.GetPrimitive(h_name)
            h = h.GetValue()
            integral, error = get_integral_and_error(h)
        except: continue
        
        print(i,integral,error)
        h_mva.SetBinContent(i,integral)
        h_mva.SetBinError(i,error)


    print(data_yield,bkg_yield, h_mva.Integral())
    #h_mva.Scale(float((data_yield-bkg_yield)) / h_mva.Integral())
    h_mva.Scale(float((data_yield)) / h_mva.Integral())

    h_mva.Write()

    outfile.Close()

    print("Done with:")
    print(path +'/' + target + '/' + 'histograms_ProbMultiH.root')


