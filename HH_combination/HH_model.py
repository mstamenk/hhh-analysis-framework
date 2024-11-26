import sympy as sp
import ROOT
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
parser = OptionParser()

kl, kt, C2 = sp.symbols('kl kt C2')
parser.add_option("--scale", action="store_true", dest="use_scale", help="BSM sample scale by 2.73...", default=False)

(options, args) = parser.parse_args()

use_scale      = options.use_scale ## X: to implement

##function for alt2 is here     alt is also the same function: 


reweight_alt = {'ggHH_kl_5p00_kt_1p00_c2_0p00_hbbhtt' : '-8.88178419700125e-16*C2**2 + 0.24019607843138*C2*kl*kt - 0.240196078431378*C2*kt**2 + 0.0980392156862759*kl**2*kt**2 - 0.338235294117652*kl*kt**3 + 0.240196078431374*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_0p00_hbbhtt' : '0.952380952380887*C2**2 - 0.126026272577926*C2*kl*kt - 3.06444991789806*C2*kt**2 + 0.172413793103444*kl**2*kt**2 - 1.28448275862065*kl*kt**3 + 2.11206896551718*kt**4', 
                'ggHH_kl_2p45_kt_1p00_c2_0p00_hbbhtt' : '8.43769498715119e-15*C2**2 - 1.35226504394863*C2*kl*kt + 1.3522650439486*C2*kt**2 - 0.270453008789724*kl**2*kt**2 + 1.62271805273834*kl*kt**3 - 1.35226504394862*kt**4', 
                'ggHH_kl_0p00_kt_1p00_c2_1p00_hbbhtt' : '7.99360577730113e-15*C2**2 - 1.0*C2*kl*kt + 0.999999999999973*C2*kt**2 + 1.88737914186277e-15*kl**2*kt**2 - 1.24344978758018e-14*kl*kt**3 + 1.77635683940025e-14*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_0p35_hbbhtt' : '-1.07816711590292*C2**2 + 2.15633423180587*C2*kl*kt + 1.07816711590287*C2*kt**2 + 2.55351295663786e-15*kl**2*kt**2 - 2.04281036531029e-14*kl*kt**3 + 3.90798504668055e-14*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_3p00_hbbhtt' : '0.125786163522007*C2**2 + 0.0817610062893164*C2*kl*kt - 0.125786163521997*C2*kt**2 - 9.99200722162641e-16*kl**2*kt**2 + 7.105427357601e-15*kl*kt**3 - 8.88178419700125e-15*kt**4'
}

reweight_alt2 = {'ggHH_kl_5p00_kt_1p00_c2_0p00_hbbhtt' : '-0.0657606033416659*C2**2 + 0.187229832085625*C2*kl*kt + 0.0330681891089486*C2*kt**2 + 0.0734080117390722*kl**2*kt**2 - 0.175149059480534*kl*kt**3 + 0.0326924142327139*kt**4', 
                'ggHH_kl_0p00_kt_1p00_c2_0p00_hbbhtt' : '0.273778838402017*C2**2 + 0.22051253580681*C2*kl*kt - 1.13767164445357*C2*kt**2 + 0.102546236841415*kl**2*kt**2 - 0.678971262570841*kl*kt**3 + 0.863892806051557*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_0p00_hbbhtt' : '0.374141164376642*C2**2 - 0.591763955962986*C2*kl*kt - 0.661608944698771*C2*kt**2 - 0.044170931259883*kl**2*kt**2 + 0.14955137353324*kl*kt**3 + 0.28746778032213*kt**4', 
                'ggHH_kl_2p45_kt_1p00_c2_0p00_hbbhtt' : '0.370221552943913*C2**2 - 1.05407365002462*C2*kl*kt - 0.186168552337499*C2*kt**2 - 0.131783317320603*kl**2*kt**2 + 0.704568948518136*kl*kt**3 - 0.184053000606413*kt**4', 
                'ggHH_kl_0p00_kt_1p00_c2_1p00_hbbhtt' : '4.44089209850063e-15*C2**2 - 1.0*C2*kl*kt + 0.999999999999992*C2*kt**2 + 3.81639164714898e-16*kl**2*kt**2 - 2.44249065417534e-15*kl*kt**3 + 3.5527136788005e-15*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_0p35_hbbhtt' : '-1.07816711590293*C2**2 + 2.15633423180586*C2*kl*kt + 1.07816711590291*C2*kt**2 - 9.15933995315754e-16*kl**2*kt**2 + 2.22044604925031e-15*kl*kt**3 + 9.10382880192628e-15*kt**4', 
                'ggHH_kl_1p00_kt_1p00_c2_3p00_hbbhtt' : '0.12578616352201*C2**2 + 0.0817610062893148*C2*kl*kt - 0.125786163522007*C2*kt**2 + 5.55111512312578e-17*kl**2*kt**2 - 6.66133814775094e-16*kl*kt**3 - 1.11022302462516e-15*kt**4'
}





kappa_list = {'ggHH_kl_m20p00_kt_1p00_c2_2p24_hbbhtt' : {'kl': -20, 'kt': 1, 'C2': 2.24}}
lep_list = ['eTau','muTau','tauTau']
cat_list = ['boosted','classDY','classGGF','classTT','classttH','classVBF','res1b','res2b']
unc_list = ['CMS_scale_j_HF','CMS_scale_j_RelBal','CMS_scale_j_FlavQCD','CMS_scale_j_EC2','CMS_scale_j_BBEC1','CMS_scale_j_Abs','CMS_btag_LF_2016_2017_2018','CMS_btag_cferr1_2016_2017_2018','CMS_btag_cferr2_2016_2017_2018','CMS_btag_HF_2016_2017_2018','CMS_bbtt_2016_etauFR_barrel','CMS_bbtt_2016_etauFR_endcap','CMS_bbtt_2016_jetTauFakes_Barrel','CMS_bbtt_2016_jetTauFakes_Endcap','CMS_bbtt_2016_trigSFele','CMS_btag_hfstats1_2016','CMS_btag_hfstats2_2016','CMS_btag_lfstats1_2016','CMS_btag_lfstats2_2016','CMS_eff_j_PUJET_id_2016','CMS_eff_t_id_pt20to25_2016','CMS_eff_t_id_pt25to30_2016','CMS_eff_t_id_pt30to35_2016','CMS_eff_t_id_pt35to40_2016','CMS_eff_t_id_pt40toInf_2016','CMS_res_j_2016','CMS_scale_j_Abs_2016','CMS_scale_j_BBEC1_2016','CMS_scale_j_EC2_2016','CMS_scale_j_HF_2016','CMS_scale_j_RelSample_2016','CMS_scale_t_DM0_2016','CMS_scale_t_DM10_2016','CMS_scale_t_DM11_2016','CMS_scale_t_DM1_2016','CMS_scale_t_eFake_2016_DM0','CMS_scale_t_eFake_2016_DM1','CMS_scale_t_muFake_2016','CMS_bbtt_2017_etauFR_barrel','CMS_bbtt_2017_etauFR_endcap','CMS_bbtt_2017_jetTauFakes_Barrel','CMS_bbtt_2017_jetTauFakes_Endcap','CMS_bbtt_2017_trigSFele','CMS_btag_hfstats1_2017','CMS_btag_hfstats2_2017','CMS_btag_lfstats1_2017','CMS_btag_lfstats2_2017','CMS_eff_j_PUJET_id_2017','CMS_eff_t_id_pt20to25_2017','CMS_eff_t_id_pt25to30_2017','CMS_eff_t_id_pt30to35_2017','CMS_eff_t_id_pt35to40_2017','CMS_eff_t_id_pt40toInf_2017','CMS_res_j_2017','CMS_scale_j_Abs_2017','CMS_scale_j_BBEC1_2017','CMS_scale_j_EC2_2017','CMS_scale_j_HF_2017','CMS_scale_j_RelSample_2017','CMS_scale_t_DM0_2017','CMS_scale_t_DM10_2017','CMS_scale_t_DM11_2017','CMS_scale_t_DM1_2017','CMS_scale_t_eFake_2017_DM0','CMS_scale_t_eFake_2017_DM1','CMS_scale_t_muFake_2017','CMS_bbtt_2018_etauFR_barrel','CMS_bbtt_2018_etauFR_endcap','CMS_bbtt_2018_jetTauFakes_Barrel','CMS_bbtt_2018_jetTauFakes_Endcap','CMS_bbtt_2018_trigSFele','CMS_btag_hfstats1_2018','CMS_btag_hfstats2_2018','CMS_btag_lfstats1_2018','CMS_btag_lfstats2_2018','CMS_eff_j_PUJET_id_2018','CMS_eff_t_id_pt20to25_2018','CMS_eff_t_id_pt25to30_2018','CMS_eff_t_id_pt30to35_2018','CMS_eff_t_id_pt35to40_2018','CMS_eff_t_id_pt40toInf_2018','CMS_l1_ecal_prefiring_2018','CMS_res_j_2018','CMS_scale_j_Abs_2018','CMS_scale_j_BBEC1_2018','CMS_scale_j_EC2_2018','CMS_scale_j_HF_2018','CMS_scale_j_RelSample_2018','CMS_scale_t_DM0_2018','CMS_scale_t_DM10_2018','CMS_scale_t_DM11_2018','CMS_scale_t_DM1_2018','CMS_scale_t_eFake_2018_DM0','CMS_scale_t_eFake_2018_DM1','CMS_scale_t_muFake_2018']
unc_list_2016 = ['CMS_scale_j_HF','CMS_scale_j_RelBal','CMS_scale_j_FlavQCD','CMS_scale_j_EC2','CMS_scale_j_BBEC1','CMS_scale_j_Abs','CMS_btag_LF_2016_2017_2018','CMS_btag_cferr1_2016_2017_2018','CMS_btag_cferr2_2016_2017_2018','CMS_btag_HF_2016_2017_2018','CMS_bbtt_2016_etauFR_barrel','CMS_bbtt_2016_etauFR_endcap','CMS_bbtt_2016_jetTauFakes_Barrel','CMS_bbtt_2016_jetTauFakes_Endcap','CMS_bbtt_2016_trigSFele','CMS_btag_hfstats1_2016','CMS_btag_hfstats2_2016','CMS_btag_lfstats1_2016','CMS_btag_lfstats2_2016','CMS_eff_j_PUJET_id_2016','CMS_eff_t_id_pt20to25_2016','CMS_eff_t_id_pt25to30_2016','CMS_eff_t_id_pt30to35_2016','CMS_eff_t_id_pt35to40_2016','CMS_eff_t_id_pt40toInf_2016','CMS_res_j_2016','CMS_scale_j_Abs_2016','CMS_scale_j_BBEC1_2016','CMS_scale_j_EC2_2016','CMS_scale_j_HF_2016','CMS_scale_j_RelSample_2016','CMS_scale_t_DM0_2016','CMS_scale_t_DM10_2016','CMS_scale_t_DM11_2016','CMS_scale_t_DM1_2016','CMS_scale_t_eFake_2016_DM0','CMS_scale_t_eFake_2016_DM1','CMS_scale_t_muFake_2016']
unc_list_2017 = ['CMS_scale_j_HF','CMS_scale_j_RelBal','CMS_scale_j_FlavQCD','CMS_scale_j_EC2','CMS_scale_j_BBEC1','CMS_scale_j_Abs','CMS_btag_LF_2016_2017_2018','CMS_btag_cferr1_2016_2017_2018','CMS_btag_cferr2_2016_2017_2018','CMS_btag_HF_2016_2017_2018','CMS_bbtt_2017_etauFR_barrel','CMS_bbtt_2017_etauFR_endcap','CMS_bbtt_2017_jetTauFakes_Barrel','CMS_bbtt_2017_jetTauFakes_Endcap','CMS_bbtt_2017_trigSFele','CMS_btag_hfstats1_2017','CMS_btag_hfstats2_2017','CMS_btag_lfstats1_2017','CMS_btag_lfstats2_2017','CMS_eff_j_PUJET_id_2017','CMS_eff_t_id_pt20to25_2017','CMS_eff_t_id_pt25to30_2017','CMS_eff_t_id_pt30to35_2017','CMS_eff_t_id_pt35to40_2017','CMS_eff_t_id_pt40toInf_2017','CMS_res_j_2017','CMS_scale_j_Abs_2017','CMS_scale_j_BBEC1_2017','CMS_scale_j_EC2_2017','CMS_scale_j_HF_2017','CMS_scale_j_RelSample_2017','CMS_scale_t_DM0_2017','CMS_scale_t_DM10_2017','CMS_scale_t_DM11_2017','CMS_scale_t_DM1_2017','CMS_scale_t_eFake_2017_DM0','CMS_scale_t_eFake_2017_DM1','CMS_scale_t_muFake_2017']
unc_list_2018 = ['CMS_scale_j_HF','CMS_scale_j_RelBal','CMS_scale_j_FlavQCD','CMS_scale_j_EC2','CMS_scale_j_BBEC1','CMS_scale_j_Abs','CMS_btag_LF_2016_2017_2018','CMS_btag_cferr1_2016_2017_2018','CMS_btag_cferr2_2016_2017_2018','CMS_btag_HF_2016_2017_2018','CMS_bbtt_2018_etauFR_barrel','CMS_bbtt_2018_etauFR_endcap','CMS_bbtt_2018_jetTauFakes_Barrel','CMS_bbtt_2018_jetTauFakes_Endcap','CMS_bbtt_2018_trigSFele','CMS_btag_hfstats1_2018','CMS_btag_hfstats2_2018','CMS_btag_lfstats1_2018','CMS_btag_lfstats2_2018','CMS_eff_j_PUJET_id_2018','CMS_eff_t_id_pt20to25_2018','CMS_eff_t_id_pt25to30_2018','CMS_eff_t_id_pt30to35_2018','CMS_eff_t_id_pt35to40_2018','CMS_eff_t_id_pt40toInf_2018','CMS_res_j_2018','CMS_scale_j_Abs_2018','CMS_scale_j_BBEC1_2018','CMS_scale_j_EC2_2018','CMS_scale_j_HF_2018','CMS_scale_j_RelSample_2018','CMS_scale_t_DM0_2018','CMS_scale_t_DM10_2018','CMS_scale_t_DM11_2018','CMS_scale_t_DM1_2018','CMS_scale_t_eFake_2018_DM0','CMS_scale_t_eFake_2018_DM1','CMS_scale_t_muFake_2018']
year_list = ['2016','2017','2018']
path_for_histograms = "/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/HH_combination"

for cat in cat_list:
    for lep in  lep_list:
        for year in year_list:
            file = ROOT.TFile("%s/hh_%s_%s_%s_13TeV.input.root"%(path_for_histograms,cat,lep,year),"READ")
            output_file = ROOT.TFile("%s/new_hist_alt2/hh_%s_%s_%s_13TeV.input.root"%(path_for_histograms,cat,lep,year), "RECREATE")

            for key in file.GetListOfKeys():
                obj = key.ReadObj()
                if isinstance(obj, ROOT.TH1F):
                    output_file.cd()
                    obj_clone = obj.Clone()  
                    obj_clone.Write()   

            for kappa_name, values in kaappa_list.items():
                kl = values['kl']
                kt = values['kt']
                C2 = values['C2']
                combined_histogram = None
                

                for basis in reweight_alt2:
                    
                    
                    hist_basis = file.Get(basis)
                    

                    if not hist_basis:
                        print("no %s"%(hist_basis))
                        continue

                    weight =  eval(reweight_alt2[basis])

                    if combined_histogram is None:
                        # print("now is none")
                        # print(basis)
                        combined_histogram = hist_basis.Clone(kappa_name)
                        combined_histogram.SetTitle(kappa_name)
                        # print(weight)
                        combined_histogram.SetName(kappa_name)
                        combined_histogram.Scale(weight)
                    else:
                        # print(basis)
                        # print(weight)
                        hist_temp = hist_basis.Clone()
                        hist_temp.Scale(weight)
                        combined_histogram.Add(hist_temp)  



                combined_histogram.Write()
                print("%s already done"%kappa_name)

                if year == '2016': unc_list_year = unc_list_2016
                if year == '2017': unc_list_year = unc_list_2017
                if year == '2018': unc_list_year = unc_list_2018



                for unc in unc_list_year:
                    combined_up = None
                    combined_down = None
                    for basis in reweight_alt2:
                        
                        hist_up = file.Get('%s_%sUp'%(basis,unc))
                        hist_down = file.Get('%s_%sDown'%(basis,unc))

                        if not hist_up:
                            print("no %s"%(hist_up))
                            print("nooooooooooooooooo!")
                            print("nooooooooooooooooo! %s_%sUp in %s/hh_%s_%s_%s_13TeV.input.root"%(basis,unc,path_for_histograms,cat,lep,year))
                            continue

                        if not hist_down:
                            print("no %s"%(hist_down))
                            print("nooooooooooooooooo!")
                            print("nooooooooooooooooo! %s_%sDown in %s/hh_%s_%s_%s_13TeV.input.root"%(basis,unc,path_for_histograms,cat,lep,year))


                            continue

                        weight =  eval(reweight_alt2[basis])

                        if combined_up is None:
                            combined_up = hist_up.Clone()
                            combined_up.SetTitle('%s_%sUp'%(kappa_name,unc))
                            combined_up.SetName('%s_%sUp'%(kappa_name,unc))
                            combined_up.Scale(weight)
                        else:
                            hist_temp_up = hist_up.Clone()
                            hist_temp_up.Scale(weight)
                            combined_up.Add(hist_temp)  

                        if combined_down is None:
                            combined_down = hist_down.Clone()
                            combined_down.SetTitle('%s_%sDown'%(kappa_name,unc))
                            combined_down.SetName('%s_%sDown'%(kappa_name,unc))
                            combined_down.Scale(weight)
                        else:
                            hist_temp_down = hist_down.Clone()
                            hist_temp_down.Scale(weight)
                            combined_down.Add(hist_temp)  



                    combined_up.Write()
                    combined_down.Write()
                    print("%s_%s already done"%(kappa_name,unc))
                



            file.Close()
            output_file.Close()
