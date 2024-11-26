import sympy as sp
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import re
from optparse import OptionParser
parser = OptionParser()

kl, kt, C2 = sp.symbols('kl kt C2')
parser.add_option("--scale", action="store_true", dest="use_scale", help="BSM sample scale by 2.73...", default=False)

(options, args) = parser.parse_args()

use_scale      = options.use_scale ## X: to implement



reweight_alt = {'ggHH_kl_5p00_kt_1p00_c2_0p00' : '-8.88178419700125e-16*C2**2 + 0.24019607843138*C2*kl*kt - 0.240196078431378*C2*kt**2 + 0.0980392156862759*kl**2*kt**2 - 0.338235294117652*kl*kt**3 + 0.240196078431374*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_0p00' : '0.952380952380887*C2**2 - 0.126026272577926*C2*kl*kt - 3.06444991789806*C2*kt**2 + 0.172413793103444*kl**2*kt**2 - 1.28448275862065*kl*kt**3 + 2.11206896551718*kt**4', 
                'ggHH_kl_2p45_kt_1p00_c2_0p00' : '8.43769498715119e-15*C2**2 - 1.35226504394863*C2*kl*kt + 1.3522650439486*C2*kt**2 - 0.270453008789724*kl**2*kt**2 + 1.62271805273834*kl*kt**3 - 1.35226504394862*kt**4', 
                'ggHH_kl_0p00_kt_1p00_c2_1p00' : '7.99360577730113e-15*C2**2 - 1.0*C2*kl*kt + 0.999999999999973*C2*kt**2 + 1.88737914186277e-15*kl**2*kt**2 - 1.24344978758018e-14*kl*kt**3 + 1.77635683940025e-14*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_0p35' : '-1.07816711590292*C2**2 + 2.15633423180587*C2*kl*kt + 1.07816711590287*C2*kt**2 + 2.55351295663786e-15*kl**2*kt**2 - 2.04281036531029e-14*kl*kt**3 + 3.90798504668055e-14*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_3p00' : '0.125786163522007*C2**2 + 0.0817610062893164*C2*kl*kt - 0.125786163521997*C2*kt**2 - 9.99200722162641e-16*kl**2*kt**2 + 7.105427357601e-15*kl*kt**3 - 8.88178419700125e-15*kt**4'
}

reweight_alt2 = {'ggHH_kl_5p00_kt_1p00_c2_0p00' : '-0.0657606033416659*C2**2 + 0.187229832085625*C2*kl*kt + 0.0330681891089486*C2*kt**2 + 0.0734080117390722*kl**2*kt**2 - 0.175149059480534*kl*kt**3 + 0.0326924142327139*kt**4', 
                'ggHH_kl_0p00_kt_1p00_c2_0p00' : '0.273778838402017*C2**2 + 0.22051253580681*C2*kl*kt - 1.13767164445357*C2*kt**2 + 0.102546236841415*kl**2*kt**2 - 0.678971262570841*kl*kt**3 + 0.863892806051557*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_0p00' : '0.374141164376642*C2**2 - 0.591763955962986*C2*kl*kt - 0.661608944698771*C2*kt**2 - 0.044170931259883*kl**2*kt**2 + 0.14955137353324*kl*kt**3 + 0.28746778032213*kt**4', 
                'ggHH_kl_2p45_kt_1p00_c2_0p00' : '0.370221552943913*C2**2 - 1.05407365002462*C2*kl*kt - 0.186168552337499*C2*kt**2 - 0.131783317320603*kl**2*kt**2 + 0.704568948518136*kl*kt**3 - 0.184053000606413*kt**4', 
                'ggHH_kl_0p00_kt_1p00_c2_1p00' : '4.44089209850063e-15*C2**2 - 1.0*C2*kl*kt + 0.999999999999992*C2*kt**2 + 3.81639164714898e-16*kl**2*kt**2 - 2.44249065417534e-15*kl*kt**3 + 3.5527136788005e-15*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_0p35' : '-1.07816711590293*C2**2 + 2.15633423180586*C2*kl*kt + 1.07816711590291*C2*kt**2 - 9.15933995315754e-16*kl**2*kt**2 + 2.22044604925031e-15*kl*kt**3 + 9.10382880192628e-15*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_3p00' : '0.12578616352201*C2**2 + 0.0817610062893148*C2*kl*kt - 0.125786163522007*C2*kt**2 + 5.55111512312578e-17*kl**2*kt**2 - 6.66133814775094e-16*kl*kt**3 - 1.11022302462516e-15*kt**4'
}

pattern = re.compile(r'(ggHH_kl_.*_hbbhbb)_(.*)(Up|Down)')



kappa_list = {'ggHH_kl_m20p00_kt_1p00_c2_2p24' : {'kl': -20, 'kt': 1, 'C2': 2.24}}
cat_list = ['GGFcateg1_1','GGFcateg1','GGFcateg2_1','GGFcateg2','VBFcateg1_1','VBFcateg1']
path_for_histograms = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/cards_histograms_original_4b"
out_folder = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination/bbbb"

for cat in cat_list:
    file = ROOT.TFile("%s/outPlotter_%s.root"%(path_for_histograms,cat),"READ")
    output_file = ROOT.TFile("%s/new_hist_alt2/outPlotter_%s.root"%(out_folder,cat), "RECREATE")
    processed_unc = set()

    for key in file.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, ROOT.TH1F):
            output_file.cd()
            obj_clone = obj.Clone()  
            obj_clone.Write()   

        hist_unc = key.GetName()
        match = pattern.match(hist_unc)
        if match:
            base_name = match.group(1)  
            # print(base_name)
            unc_name = match.group(2) 
            # print(unc_name)
            updown = match.group(3)
            if unc_name in  processed_unc:
                continue
            else: 
                processed_unc.add(unc_name)
    print(processed_unc)

    for kappa_name, values in kappa_list.items():
        kl = values['kl']
        kt = values['kt']
        C2 = values['C2']
        
        if "_1" in cat:
            year_list = ["2017","2018"]
        else :
            year_list = ["2016"]
        
        for year in year_list:
            combined_histogram = None


            for basis in reweight_alt2:
            
                hist_basis = file.Get(f"{basis}_{year}_hbbhbb")
                if not hist_basis:
                    print("no %s"%(hist_basis))
                    continue

                weight =  eval(reweight_alt2[basis])

                if combined_histogram is None:
                    # print("now is none")
                    # print(basis)
                    combined_histogram = hist_basis.Clone(f"{kappa_name}_{year}_hbbhbb")
                    combined_histogram.SetTitle(f"{kappa_name}_{year}_hbbhbb")
                    # print(weight)
                    combined_histogram.SetName(f"{kappa_name}_{year}_hbbhbb")
                    combined_histogram.Scale(weight)
                else:
                    # print(basis)
                    # print(weight)
                    hist_temp = hist_basis.Clone()
                    hist_temp.Scale(weight)
                    combined_histogram.Add(hist_temp)  

            combined_histogram.Write()
            print("%s %s already done"%(kappa_name,year))

            
                    
                    
            for unc_name in processed_unc:
                if year not in unc_name and any(y in unc_name for y in year_list):
                    continue

                combined_up = None
                combined_down = None

                # if base_name in reweight_alt2:
                for base_name in reweight_alt2:

                    weight =  eval(reweight_alt2[base_name])
                    hist_up = file.Get('%s_%s_hbbhbb_%sUp'%(base_name,year,unc_name))
                    # print("check !!!!!!!!!!!!!!s")
                    # print('%s_%s_hbbhbb_%sUp'%(base_name,year,unc_name))
                    hist_down = file.Get('%s_%s_hbbhbb_%sDown'%(base_name,year,unc_name))

                    if not hist_up:
                        print("no %s"%(hist_up))
                        print("nooooooooooooooooo!")
                        print("nooooooooooooooooo! %s_%s_hbbhbb_%sUp in %s/outPlotter_%s.root"%(base_name,year,unc_name,path_for_histograms,cat))
                        continue

                    if not hist_down:
                        print("no %s"%(hist_down))
                        print("nooooooooooooooooo!")
                        print("nooooooooooooooooo! %s_%s_hbbhbb_%sDown in %s/outPlotter_%s.root"%(base_name,year,unc_name,path_for_histograms,cat))
                        continue


                    if combined_up is None:
                        combined_up = hist_up.Clone()
                        combined_up.SetTitle('%s_%s_hbbhbb_%sUp'%(kappa_name,year,unc_name))
                        combined_up.SetName('%s_%s_hbbhbb_%sUp'%(kappa_name,year,unc_name))
                        combined_up.Scale(weight)
                    else:
                        hist_temp_up = hist_up.Clone()
                        hist_temp_up.Scale(weight)
                        combined_up.Add(hist_temp_up)  

                    if combined_down is None:
                        combined_down = hist_down.Clone()
                        combined_down.SetTitle('%s_%s_hbbhbb_%sDown'%(kappa_name,year,unc_name))
                        combined_down.SetName('%s_%s_hbbhbb_%sDown'%(kappa_name,year,unc_name))
                        combined_down.Scale(weight)
                    else:
                        hist_temp_down = hist_down.Clone()
                        hist_temp_down.Scale(weight)
                        combined_down.Add(hist_temp_down)  

                
                combined_up.Write()
                combined_down.Write()
                print("%s_%s_%s already done"%(kappa_name,year,unc_name))
        



    file.Close()
    output_file.Close()
