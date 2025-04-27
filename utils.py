# Script to store labels and cut definitions
import random
import ROOT

q = random.uniform(0,1)

luminosities = {#'2016' : 36330.0,
                '2016APV' : 19207.0,
                '2016PostAPV' : 17122.0,
                '2016' : 17122.0,
                '2017' : 41480.0,
                '2018' : 59830.0,
                '2022' : 8174.68,
                '2022EE': 27007.2,
                '2023' : 17628.0,
                '2023BPix' : 9525.0, 
        }


hlt_paths = {
       #'2016' : '( HLT_QuadJet45_TripleBTagCSV_p087||  HLT_PFHT400_SixJet30_DoubleBTagCSV_p056||  HLT_PFHT450_SixJet40_BTagCSV_p056||  HLT_AK8PFJet360_TrimMass30||  HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20||  HLT_AK8PFJet450||  HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200||  HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20||  HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20||  HLT_PFJet450 ||  HLT_QuadJet45_DoubleBTagCSV_p087 )',
        '2016' : '( HLT_QuadJet45_TripleBTagCSV_p087 || HLT_DoubleJet90_Double30_TripleBTagCSV_p087)',
        #'2016PostAPV' : '( HLT_QuadJet45_TripleBTagCSV_p087 || HLT_DoubleJet90_Double30_TripleBTagCSV_p087)',
        #'2016APV' : '( HLT_QuadJet45_TripleBTagCSV_p087||  HLT_PFHT400_SixJet30_DoubleBTagCSV_p056||  HLT_PFHT450_SixJet40_BTagCSV_p056||  HLT_AK8PFJet360_TrimMass30||  HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20||  HLT_AK8PFJet450||  HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200||  HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20||  HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20||  HLT_PFJet450||  HLT_PFMET120_BTagCSV_p067||  HLT_QuadJet45_DoubleBTagCSV_p087 )',
        #'2016APV' : '( HLT_QuadJet45_TripleBTagCSV_p087)',
#        '2016PostAPV' : '( HLT_QuadJet45_TripleBTagCSV_p087||  HLT_PFHT400_SixJet30_DoubleBTagCSV_p056||  HLT_PFHT450_SixJet40_BTagCSV_p056||  HLT_AK8PFJet360_TrimMass30||  HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20||  HLT_AK8PFJet450||  HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200||  HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20||  HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20||  HLT_PFJet450||  HLT_QuadJet45_DoubleBTagCSV_p087 )',
             #'2017' : '(HLT_PFJet450 || HLT_PFJet500 || HLT_PFHT1050 || HLT_AK8PFJet550 || HLT_AK8PFJet360_TrimMass30 || HLT_AK8PFJet400_TrimMass30 || HLT_AK8PFHT750_TrimMass50 || HLT_AK8PFJet330_PFAK8BTagCSV_p17 || HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0 || HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1 || HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 || HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2 || HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 || HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1 || HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2 || HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07 )',
             #'2017' : '(HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0  || HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07)',

            '2017' : '(HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0)',

             #'2018' : '(HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5||HLT_PFHT1050||HLT_PFJet500||HLT_AK8PFJet500||HLT_AK8PFJet400_TrimMass30||HLT_AK8PFHT800_TrimMass50||HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4||HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1||HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2||HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94||HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59||HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17||HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1||HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2|| HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1)',
             '2018' : '(HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5)',
             '2022' : '((HLT_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65 || HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65 || HLT_QuadPFJet70_50_45_35_PFBTagParticleNet_2BTagSum0p65 || HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5 || HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59))',

             '2022EE' : '(HLT_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65 || HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65 || HLT_QuadPFJet70_50_45_35_PFBTagParticleNet_2BTagSum0p65 || HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5 || HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59)'
        }



phi_bins = 5
eta_bins = 10
histograms_dict = {
        'h1_t3_mass'  : { "nbins" : 13 , "xmin" : 70 , "xmax" : 200, "label" : 'm(H1) (GeV)'},
        'h2_t3_mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'm(H2) (GeV)'},
        'h3_t3_mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'm(H3) (GeV)'},
        'h1_spanet_boosted_mass'  : { "nbins" : 13 , "xmin" : 70 , "xmax" : 200, "label" : 'm(H1) (GeV)'},
        'h2_spanet_boosted_mass'  : { "nbins" : 13 , "xmin" : 70 , "xmax" : 200, "label" : 'm(H2) (GeV)'},
        'h3_spanet_boosted_mass'  : { "nbins" : 13 , "xmin" : 70 , "xmax" : 200, "label" : 'm(H3) (GeV)'},

        #'h1_spanet_boosted_mass'  : { "nbins" : 13 , "xmin" : 70 , "xmax" : 200, "label" : 'm(H1) (GeV)'},
        #'h2_spanet_boosted_mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'm(H2) (GeV)'},
        #'h3_spanet_boosted_mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'm(H3) (GeV)'},

        #'h1_spanet_mass'  : { "nbins" : 13 , "xmin" : 70 , "xmax" : 200, "label" : 'm(H1) (GeV)'},
        #'h2_spanet_mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'm(H2) (GeV)'},
        #'h3_spanet_mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'm(H3) (GeV)'},

        #'h_fit_mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'm(H) fitted (GeV)'},

        #'h1_t3_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H1)'},
        #'h2_t3_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H2)'},
        #'h3_t3_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H3)'},

        'h1_spanet_boosted_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H1)'},
        'h2_spanet_boosted_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H2)'},
        'h3_spanet_boosted_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H3)'},

        #'h1_spanet_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H1)'},
        #'h2_spanet_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H2)'},
        #'h3_spanet_pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'p_{T}(H3)'},

        #'h1_t3_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H1)'},
        #'h2_t3_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H2)'},
        #'h3_t3_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H3)'},

        'h1_spanet_boosted_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H1)'},
        'h2_spanet_boosted_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H2)'},
        'h3_spanet_boosted_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H3)'},

        #'h1_spanet_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H1)'},
        #'h2_spanet_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H2)'},
        #'h3_spanet_eta'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 3, "label" : '#eta(H3)'},

        #'h1_t3_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H1)'},
        #'h2_t3_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H2)'},
        #'h3_t3_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H3)'},

        'h1_spanet_boosted_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H1)'},
        'h2_spanet_boosted_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H2)'},
        'h3_spanet_boosted_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H3)'},

        #'h1_spanet_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H1)'},
        #'h2_spanet_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H2)'},
        #'h3_spanet_phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(H3)'},

        'h1_t3_dRjets'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 5.0, "label" : '#Delta R(j1,j2) H1'},
        'h2_t3_dRjets'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 5.0, "label" : '#Delta R(j3,j4) H2'},
        'h3_t3_dRjets'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 5.0, "label" : '#Delta R(j5,j6) H3'},

        #'h1_t3_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H1 truth matched'},
        #'h2_t3_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H2 truth matched'},
        #'h3_t3_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H3 truth matched'},

        #'h1_spanet_boosted_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H1 truth matched'},
        #'h2_spanet_boosted_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H2 truth matched'},
        #'h3_spanet_boosted_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H3 truth matched'},

        #'h1_spanet_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H1 truth matched'},
        #'h2_spanet_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H2 truth matched'},
        #'h3_spanet_match'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'H3 truth matched'},

        #'bcand1Pt'  : { "nbins" : 50 , "xmin" : 0 , "xmax" : 500, "label" : 'b-candidate 1 p_{T} (GeV)'},
        #'bcand2Pt'  : { "nbins" : 50 , "xmin" : 0 , "xmax" : 500, "label" : 'b-candidate 2 p_{T} (GeV)'},
        #'bcand3Pt'  : { "nbins" : 45 , "xmin" : 0 , "xmax" : 450, "label" : 'b-candidate 3 p_{T} (GeV)'},
        #'bcand4Pt'  : { "nbins" : 35 , "xmin" : 0 , "xmax" : 350, "label" : 'b-candidate 4 p_{T} (GeV)'},
        #'bcand5Pt'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 250, "label" : 'b-candidate 5 p_{T} (GeV)'},
        #'bcand6Pt'  : { "nbins" : 15 , "xmin" : 0 , "xmax" : 150, "label" : 'b-candidate 6 p_{T} (GeV)'},

        #'bcand1Eta'  : { "nbins" : eta_bins , "xmin" : 0 , "xmax" : 2.5, "label" : 'b-candidate  1 #eta'},
        #'bcand2Eta'  : { "nbins" : eta_bins , "xmin" : 0 , "xmax" : 2.5, "label" : 'b-candidate  2 #eta'},
        #'bcand3Eta'  : { "nbins" : eta_bins , "xmin" : 0 , "xmax" : 2.5, "label" : 'b-candidate  3 #eta'},
        #'bcand4Eta'  : { "nbins" : eta_bins , "xmin" : 0 , "xmax" : 2.5, "label" : 'b-candidate  4 #eta'},
        #'bcand5Eta'  : { "nbins" : eta_bins , "xmin" : 0 , "xmax" : 2.5, "label" : 'b-candidate  5 #eta'},
        #'bcand6Eta'  : { "nbins" : eta_bins , "xmin" : 0 , "xmax" : 2.5, "label" : 'b-candidate  6 #eta'},

        'jet1Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  1 #phi'},
        'jet2Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  2 #phi'},
        'jet3Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  3 #phi'},
        'jet4Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  4 #phi'},
        'jet5Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  5 #phi'},
        'jet6Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  5 #phi'},

         'jet7Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  7 #phi'},
        'jet8Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  8 #phi'},
        'jet9Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  9 #phi'},

         'jet10Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : 'b-candidate  10 #phi'},


        'jet1Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  1 Mass'},
        'jet2Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  2 Mass'},
        'jet3Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  3 Mass'},
        'jet4Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  4 Mass'},
        'jet5Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  5 Mass'},
        'jet6Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  6 Mass'},
        'jet7Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  7 Mass'},
        'jet8Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  8 Mass'},
        'jet9Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  9 Mass'},
        'jet10Mass'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 100, "label" : 'b-candidate  10 Mass'},

        #'bcand1DeepFlavB'  : { "nbins" : 40 , "xmin" : 0 , "xmax" : 1, "label" : 'Jet 1 b-tag score'},
        #'bcand2DeepFlavB'  : { "nbins" : 40 , "xmin" : 0 , "xmax" : 1, "label" : 'Jet 2 b-tag score'},
        #'bcand3DeepFlavB'  : { "nbins" : 40 , "xmin" : 0 , "xmax" : 1, "label" : 'Jet 3 b-tag score'},
        #'bcand4DeepFlavB'  : { "nbins" : 40 , "xmin" : 0 , "xmax" : 1, "label" : 'Jet 4 b-tag score'},
        #'bcand5DeepFlavB'  : { "nbins" : 40 , "xmin" : 0 , "xmax" : 1, "label" : 'Jet 5 b-tag score'},
        #'bcand6DeepFlavB'  : { "nbins" : 40 , "xmin" : 0 , "xmax" : 1, "label" : 'Jet 6 b-tag score'},

        #'bcand1HiggsMatched'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'Jet 1 truth matched'},
        #'bcand2HiggsMatched'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'Jet 2 truth matched'},
        #'bcand3HiggsMatched'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'Jet 3 truth matched'},
        #'bcand4HiggsMatched'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'Jet 4 truth matched'},
        #'bcand5HiggsMatched'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'Jet 5 truth matched'},
        #'bcand6HiggsMatched'  : { "nbins" : 2 , "xmin" : 0 , "xmax" : 2, "label" : 'Jet 6 truth matched'},

        'fatJet1Mass'  : { "nbins" : 13 , "xmin" : 70 , "xmax" : 200, "label" : 'fatJet1 mass regressed (GeV)'},
        'fatJet2Mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'fatJet2 mass regressed (GeV)'},
        'fatJet3Mass'  : { "nbins" : 30 , "xmin" : 0 , "xmax" : 300, "label" : 'fatJet3 mass regressed (GeV)'},

        'fatJet1Pt'  : { "nbins" : 50 , "xmin" : 150 , "xmax" : 1000, "label" : 'p_{T}(fatJet1) (GeV)'},
        'fatJet2Pt'  : { "nbins" : 50 , "xmin" : 150 , "xmax" : 1000, "label" : 'p_{T}(fatJet2) (GeV)'},
        'fatJet3Pt'  : { "nbins" : 50 , "xmin" : 150 , "xmax" : 1000, "label" : 'p_{T}(fatJet3) (GeV)'},

        'fatJet1Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : '#eta(fatJet1)'},
        'fatJet2Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : '#eta(fatJet2)'},
        'fatJet3Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : '#eta(fatJet3)'},

        'fatJet1Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(fatJet1)'},
        'fatJet2Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(fatJet2)'},
        'fatJet3Phi'  : { "nbins" : phi_bins , "xmin" : 0 , "xmax" : 3.2, "label" : '#phi(fatJet3)'},

        'fatJet1PNetXbb'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet Xbb(fatJet1)'},
        'fatJet2PNetXbb'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet Xbb(fatJet2)'},
        'fatJet3PNetXbb'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet Xbb(fatJet3)'},

        'fatJet1PNetXjj'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet Xjj(fatJet1)'},
        'fatJet2PNetXjj'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet Xjj(fatJet2)'},
        'fatJet3PNetXjj'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet Xjj(fatJet3)'},

        'fatJet1PNetQCD'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet QCD(fatJet1)'},
        'fatJet2PNetQCD'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet QCD(fatJet2)'},
        'fatJet3PNetQCD'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'PNet QCD(fatJet3)'},

        #'HHH_mass'   : { "nbins" : 80 , "xmin" : 0 , "xmax" : 1600, "label" : 'm(HHH) (GeV)'},
        #'HHH_pt'     : { "nbins" : 80 , "xmin" : 0 , "xmax" : 800, "label" : 'p_{T}(HHH) (GeV)'},
        #'HHH_eta'    : { "nbins" : 15 , "xmin" : 0 , "xmax" : 2.5, "label" : '#eta(HHH) (GeV)'},

        #'nfatjets'    : { "nbins" : 5 , "xmin" : 0 , "xmax" : 5, "label" : 'N fat-jets'},
        'nprobejets'  : { "nbins" : 5 , "xmin" : 0 , "xmax" : 5, "label" : 'N fat-jets'},
        'nbtags'      : { "nbins" : 10 , "xmin" : 0 , "xmax" : 10, "label" : 'N b-tags'},

        'nloosebtags'   : { "nbins" : 10 , "xmin" : 0 , "xmax" : 10, "label" : 'N loose b-tags'},
        'nmediumbtags'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 10, "label" : 'N meidum b-tags'},
        'ntightbtags'   : { "nbins" : 10 , "xmin" : 0 , "xmax" : 10, "label" : 'N tight b-tags'},

        'nsmalljets' : { "nbins" : 12 , "xmin" : 0 , "xmax" : 12, "label" : 'NAK4 jets'},
        'nfatjets' :  { "nbins" : 7 , "xmin" : 0 , "xmax" : 7, "label" : 'NAK8 jets'},

        'ht'   : { "nbins" : 90 , "xmin" : 0 , "xmax" : 1800, "label" : 'Event HT [GeV]'},
        'met'  : { "nbins" : 25 , "xmin" : 0 , "xmax" : 500, "label" : 'E_{T}^{miss} [GeV]'},
        'bdt'  : { "nbins" : 20 , "xmin" : -1 , "xmax" : 1, "label" : 'BDT output score'},
        #'mva'  : { "nbins" : 10 , "xmin" : 0.0 , "xmax" : 1.0, "label" : 'BDT output score'},
        #'mvaBoosted'  : { "nbins" : 20 , "xmin" : -0.6 , "xmax" : 0.8, "label" : 'BDT output score (boosted)'},
        'ProbHHH'  : { "nbins" : 40, "xmin" : 0 , "xmax" : 1.0, "label" : 'ProbHHH'},
        'ProbHH4b'  : { "nbins" : 40, "xmin" : 0 , "xmax" : 1.0, "label" : 'ProbHH4b'},
        'ProbHHH4b2tau'  : { "nbins" : 40, "xmin" : 0 , "xmax" : 1.0, "label" : 'ProbHHH4b2tau'},
        'ProbMultiH'  : { "nbins" : 40, "xmin" : 0.2 , "xmax" : 1.0, "label" : 'Prob multi-Higgs'},
        'ProbVV'  : { "nbins" : 40, "xmin" : 0.2 , "xmax" : 1.0, "label" : 'ProbVV'},

        'jet1PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 1 PNetB b-score'},
        'jet2PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 2 PNetB b-score'},
        'jet3PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 3 PNetB b-score'},
        'jet4PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 4 PNetB b-score'},
        'jet5PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 5 PNetB b-score'},
        'jet6PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 6 PNetB b-score'},
        'jet7PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 7 PNetB b-score'},
        'jet8PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 8 PNetB b-score'},
        'jet9PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 9 PNetB b-score'},
        'jet10PNetB'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 1, "label" : 'jet 10 PNetB b-score'},

        'jet1HadronFlavour'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 20, "label" : 'jet 1 hadron flavour'},
        'jet2HadronFlavour'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 20, "label" : 'jet 2 hadron flavour'},
        'jet3HadronFlavour'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 20, "label" : 'jet 3 hadron flavour'},
        'jet4HadronFlavour'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 20, "label" : 'jet 4 hadron flavour'},
        'jet5HadronFlavour'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 20, "label" : 'jet 5 hadron flavour'},
        'jet6HadronFlavour'  : { "nbins" : 20 , "xmin" : 0 , "xmax" : 20, "label" : 'jet 6 hadron flavour'},


        'jet1Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 1 p_{T} (GeV)'},
        'jet2Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 2 p_{T} (GeV)'},
        'jet3Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 3 p_{T} (GeV)'},
        'jet4Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 4 p_{T} (GeV)'},
        'jet5Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 5 p_{T} (GeV)'},
        'jet6Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 6 p_{T} (GeV)'},
        'jet7Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 7 p_{T} (GeV)'},
        'jet8Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 8 p_{T} (GeV)'},
        'jet9Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 9 p_{T} (GeV)'},
        'jet10Pt'  : { "nbins" : 25 , "xmin" : 20 , "xmax" : 500, "label" : 'jet 10 p_{T} (GeV)'},

        'jet1Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 1 #eta'},
        'jet2Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 2 #eta'},
        'jet3Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 3 #eta'},
        'jet4Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 4 #eta'},
        'jet5Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 5 #eta'},
        'jet6Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 6 #eta'},
        'jet7Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 7 #eta'},
        'jet8Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 8 #eta'},
        'jet9Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 9 #eta'},
        'jet10Eta'  : { "nbins" : 10 , "xmin" : 0 , "xmax" : 2.5, "label" : 'Jet 10 #eta'},

        # skip phi up to put that more automatic

}


#doing this ordered dictionary to make sure of the drawing order
# [color, marker size, line size, legend label , add in legend]
hist_properties = {'JetHT' : [ROOT.kBlack, 0.8, 0, 'Data', True] ,
                   'JetHT-btagSF' : [ROOT.kBlack, 0.8, 0, 'Data', True],
                   'BTagCSV' : [ROOT.kBlack, 0.8, 0, 'Data', True],
                   'data_obs' : [ROOT.kBlack, 0.8, 0, 'Data', True],
                   'ZZZ' : [ROOT.kGreen, 0, 0, 'VVV', True],
                   'WWW' : [ROOT.kGreen, 0, 0, 'VVV', False],
                   'WZZ' : [ROOT.kGreen, 0, 0, 'VVV', False],
                   'WWZ' : [ROOT.kGreen, 0, 0, 'VVV', False],
                   'TT' : [ROOT.kBlue, 0,0, 't#bar{t}', True],
                   'TTToHadronic' : [ROOT.kBlue, 0,0, 't#bar{t}', True],
                   'TTto4Q' : [ROOT.kBlue, 0,0, 't#bar{t}', True],
                   'TTtoLNu2Q' : [ROOT.kBlue, 0,0, 't#bar{t}', True],

                   'TTToSemiLeptonic' : [ROOT.kBlue, 0,0, 't#bar{t}', False],
                   'ZZTo4Q' : [ROOT.kGray, 0, 0, 'VV', True],
                   'ZZ' : [ROOT.kGray, 0, 0, 'VV', True],
                   'WWTo4Q' : [ROOT.kGray, 0, 0, 'VV', False],
                   'ZJetsToQQ'   : [ROOT.kCyan, 0, 0, 'V+jets', True],
                   'Zto2Q-4Jets'   : [ROOT.kCyan, 0, 0, 'V+jets', True],
                   'WJetsToQQ'   : [ROOT.kCyan, 0, 0, 'V+jets', False],
                  'Wto2Q-3Jets'   : [ROOT.kCyan, 0, 0, 'V+jets', False],
                   'QCD'   : [ROOT.kOrange, 0, 0, 'QCD', True],
                   'QCD_mc'   : [ROOT.kOrange, 0, 0, 'QCD', True],
                   'QCD_datadriven'   : [ROOT.kOrange, 0, 0, 'Bkg model', True],
                   'QCD-4Jets'   : [ROOT.kOrange, 0, 0, 'QCD', True],
                   'QCD_bEnriched'   : [ROOT.kOrange + 1, 0, 0, 'QCD b-enriched', True],
                   'QCD6B'   : [ROOT.kOrange + 2, 0, 0, 'QCD6B', True],
                   'DYJetsToLL'   : [ROOT.kYellow + 2, 0, 0, 'DY + jets', True],
                   'GluGluToHHHTo6B_SM' : [ROOT.kRed, 0,3, 'SM HHH', True],
                   'GluGluToHHHTo4B2Tau_SM' : [ROOT.kRed, 0,3, 'SM HHH4b2tau', True],
                   'GluGluToHHH' : [ROOT.kRed, 0,3, 'SM HHH', True],
                   'GluGluToHHTo4B_cHHH1' : [ROOT.kViolet + 2, 0,3, 'SM HH', True],
                   'GluGluToHHTo2B2Tau' : [ROOT.kViolet + 3, 0,3, 'SM HH2b2tau', True],
                   'QCD_datadriven_data' : [ROOT.kOrange + 3, 0,3, 'Background model', True],

        }

def addLabel_CMS_preliminary(luminosity) :

    x0 = 0.1
    y0 = 0.988
    ypreliminary = 0.988
    xlumi = 0.69
    label_cms = ROOT.TPaveText(x0, y0, x0 + 0.0950, y0, "NDC")
    label_cms.AddText("CMS")
    label_cms.SetTextFont(61)
    label_cms.SetTextAlign(13)
    label_cms.SetTextSize(0.045)
    label_cms.SetTextColor(1)
    label_cms.SetFillStyle(0)
    label_cms.SetBorderSize(0)
    label_preliminary = ROOT.TPaveText(x0 + 0.0950, ypreliminary, x0 + 0.2950, ypreliminary, "NDC")
    label_preliminary.AddText("Internal")
    label_preliminary.SetTextFont(52)
    label_preliminary.SetTextAlign(13)
    label_preliminary.SetTextSize(0.0450)
    label_preliminary.SetTextColor(1)
    label_preliminary.SetFillStyle(0)
    label_preliminary.SetBorderSize(0)
    label_luminosity = ROOT.TPaveText(xlumi, y0 + 0.01, xlumi, y0 + 0.01, "NDC")
    label_luminosity.AddText("%s fb^{-1} (13 TeV)" % (str(round(luminosity/1000.0,1))))
    label_luminosity.SetTextFont(42)
    label_luminosity.SetTextAlign(13)
    label_luminosity.SetTextSize(0.045)
    label_luminosity.SetTextColor(1)
    label_luminosity.SetFillStyle(0)
    label_luminosity.SetBorderSize(0)

    return [label_cms, label_preliminary, label_luminosity]


def clean_variables(variables) :
    #for testing in ["HLT", "LHE", "v_", "L1_", "l1PreFiringWeight", "trigger", "vbf", "lep",  "pu", "_Up", "_Down", 'passmetfilters', 'PSWeight', "boostedTau", "boostedTau_"] :
    #    for var in variables :
    #        if str(var).find(testing) != -1:
    #            variables.remove(var)
    ls_to_remove = ["HLT", "LHE", "v_", "L1_", "l1PreFiringWeight", "trigger", "vbf", "lep",  "pu", "_Up", "_Down", 'passmetfilters', 'PSWeight', "boostedTau", "boostedTau_",'L1_']
    variables = [el for el in variables if not any(ext in el for ext in ls_to_remove)]

    # remove variables based on 6 first btags to not confuse
    for var in ['nloosebtags', 'nmediumbtags', 'ntightbtags'] :
        variables.remove(var)

    for var in [ 'LHEReweightingWeight', 'LHEScaleWeightNormNew', 'fatJet3PtOverMHH_JMS_Down', 'fatJet3PtOverMHH_MassRegressed_JMS_Down', 'genHiggs1Eta', 'genHiggs1Phi', 'genHiggs1Pt', 'genHiggs2Eta', 'genHiggs2Phi', 'genHiggs2Pt', 'genHiggs3Eta', 'genHiggs3Phi', 'genHiggs3Pt', 'genTtbarId', 'genWeight', "xsecWeight", "nfatjets", 'l1PreFiringWeightDown', 'lep1Id', 'lep1Pt', 'lep2Id', 'lep2Pt', "eventWeightBTagSF", "eventWeightBTagCorrected", "weight", "PV_npvs", "boostedTau_phi", "boostedTau_rawAntiEleCat2018", "boostedTau_eta", "boostedTau_idMVAoldDM2017v2", "boostedTau_leadTkDeltaPhi", "boostedTau_rawMVAoldDM2017v2", 'boostedTau_rawIsodR03', 'HLT_AK8PFHT800_TrimMass50', 'HLT_AK8PFHT900_TrimMass50', 'HLT_AK8PFJet200', 'HLT_AK8PFJet320', 'HLT_AK8PFJet330_PFAK8BTagCSV_p17', 'HLT_AK8PFJet380_TrimMass30', 'HLT_AK8PFJet400', 'HLT_AK8PFJet420_TrimMass30', 'HLT_AK8PFJet500', 'HLT_AK8PFJet60', 'HLT_AK8PFJetFwd140', 'HLT_AK8PFJetFwd260', 'HLT_AK8PFJetFwd40', 'HLT_AK8PFJetFwd450', 'HLT_AK8PFJetFwd60', 'HLT_Ele27_WPTight_Gsf', 'HLT_HT300PT30_QuadJet_75_60_45_40', 'HLT_PFHT380_SixPFJet32', 'HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2', 'HLT_PFHT430_SixJet40_BTagCSV_p080', 'HLT_PFMET120_PFMHT120_IDTight_PFHT60', 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_HFCleaned', 'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight', 'HLT_PFMETTypeOne100_PFMHT100_IDTight_PFHT60', 'HLT_PFMETTypeOne120_PFMHT120_IDTight', 'HLT_Ele32_WPTight_Gsf_L1DoubleEG', 'HLT_Ele38_WPTight_Gsf', 'HLT_IsoMu20', 'HLT_IsoMu24_eta2p1', 'HLT_IsoMu30', 'HLT_Mu55', 'HLT_PFHT180', 'HLT_PFHT300PT30_QuadPFJet_75_60_45_40', 'HLT_PFHT350', 'HLT_PFHT370', 'HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2', 'HLT_PFHT430', 'HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5', 'HLT_PFHT500_PFMET110_PFMHT110_IDTight', 'HLT_PFHT590', 'HLT_PFHT700_PFMET85_PFMHT85_IDTight', 'HLT_PFHT780', 'HLT_PFHT800_PFMET85_PFMHT85_IDTight', 'HLT_PFJet140', 'HLT_PFJet260', 'HLT_PFJet40', 'HLT_PFJet450', 'HLT_PFJet550', 'HLT_PFJet80', 'HLT_PFJetFwd200', 'HLT_PFJetFwd320', 'HLT_PFJetFwd400', 'HLT_PFJetFwd500', 'HLT_PFJetFwd80', 'HLT_PFMET100_PFMHT100_IDTight_PFHT60', 'HLT_PFMET110_PFMHT110_IDTight_CaloBTagCSV_3p1', 'HLT_PFMET120_PFMHT120_IDTight_CaloBTagCSV_3p1', 'HLT_PFMET130_PFMHT130_IDTight', 'HLT_PFMET140_PFMHT140_IDTight', 'HLT_PFMET200_HBHECleaned', 'HLT_PFMET200_NotCleaned', 'HLT_PFMET300_HBHECleaned', 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight', 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60', 'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight', 'HLT_PFMETTypeOne110_PFMHT110_IDTight', 'HLT_PFMETTypeOne120_PFMHT120_IDTight_PFHT60', 'HLT_PFMETTypeOne140_PFMHT140_IDTight', 'HLT_Photon175', 'HLT_QuadPFJet103_88_75_15_BTagCSV_p013_VBF2', 'HLT_QuadPFJet105_88_76_15', 'HLT_QuadPFJet105_90_76_15_DoubleBTagCSV_p013_p08_VBF1', 'HLT_QuadPFJet111_90_80_15_BTagCSV_p013_VBF2', 'HLT_QuadPFJet98_83_71_15', 'HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1', 'L1_HTT280er_QuadJet_70_55_40_35_er2p5', 'L1_HTT320er_QuadJet_70_55_40_40_er2p4', 'L1_HTT320er_QuadJet_70_55_45_45_er2p5', 'L1_HTT450er', 'nfatjets', 'ptj2_over_ptj1', 'ptj3_over_ptj1', 'ptj3_over_ptj2', 'rho', 'LHE_Vpt', 'fatJet2PtOverMHH_JMS_Down', 'fatJet2PtOverMHH_MassRegressed_JMS_Down', 'mva', 'nLHEReweightingWeight', 'nbtags',  'puWeightDown', 'triggerEffMC3DWeight', 'triggerEffWeight', 'l1PreFiringWeightDown', 'lep1Id', 'lep1Pt', 'lep2Id', 'lep2Pt', 'v_1', 'v_11', 'v_13', 'v_15', 'v_17', 'v_19', 'v_20', 'v_22', 'v_24', 'v_26', 'v_28', 'v_3', 'v_31', 'v_33', 'v_35', 'v_37', 'v_39', 'v_40', 'v_42', 'v_44', 'v_46', 'v_48', 'v_5', 'v_51', 'v_53', 'v_55', 'v_57', 'v_59', 'v_60', 'v_7', 'v_9', 'vbffatJet1PNetXbb', 'vbffatJet1Pt', 'vbffatJet2PNetXbb', 'vbffatJet2Pt', 'vbfjet1Mass', 'vbfjet1Pt', 'vbfjet2Mass', 'vbfjet2Pt', 'boostedTau_pt', 'boostedTau_idAntiMu', 'boostedTau_jetIdx', 'boostedTau_mass', 'h1h2_mass_squared', 'h2h3_mass_squared', 'deltaEta_j1j3', 'deltaPhi_j1j3', 'deltaR_j1j3', 'mj3_over_mj1', 'mj3_over_mj1_MassRegressed', 'deltaEta_j2j3', 'deltaPhi_j2j3', 'deltaR_j2j3', 'mj3_over_mj2', 'mj3_over_mj2_MassRegressed', 'isVBFtag', 'dijetmass', 'nsmalljets',  'jet7BTagSF', 'jet8BTagSF', 'jet9BTagSF', 'jet10BTagSF', 'ratioPerEvent', "LHEPdfWeightNorm", "LHEScaleWeight", 'hh_eta_JMS_Down', 'hh_eta_MassRegressed_JMS_Down', 'hh_mass_JMS_Down', 'hh_mass_MassRegressed_JMS_Down', 'hh_pt_JMS_Down', 'hh_pt_MassRegressed', 'hh_pt_MassRegressed_JMS_Down',  'hhh_eta_JMS_Down', 'hhh_eta_MassRegressed_JMS_Down', 'hhh_mass_JMS_Down', 'hhh_mass_MassRegressed_JMS_Down', 'fatJet1PtOverMHH_JMS_Down', 'fatJet1PtOverMHH_MassRegressed_JMS_Down',  'eventWeight', 'hhh_pt_JMS_Down', 'hhh_pt_MassRegressed', 'hhh_pt_MassRegressed_JMS_Down', 'mj2_over_mj1', 'mj2_over_mj1_MassRegressed'] :
        try :
            variables.remove(var)
        except:
            pass

    for hhhvar in ['hhh_resolved_mass', 'hhh_resolved_pt', 'hhh_t3_pt', 'hhh_mass', 'hhh_pt', "hh_eta", "hh_mass", "hh_phi", "hh_pt", "hhh_eta", "hhh_phi",] :
        #print("removed %s" % hhhvar)
        try:
            variables.remove(hhhvar)
        except:
            continue

    # those above are not what we think they are
    for hhhvar in [ 'eta_MassRegressed', 'phi_MassRegressed', 'mass_MassRegressed'] :
        variables.remove('hhh_{}'.format(hhhvar))
        variables.remove('hh_{}'.format(hhhvar))

    for jet_number in range(1,11) :
        for jetvar in ['DeepFlavB', 'HiggsMatched', 'HasMuon', 'HasElectron', 'FatJetMatched', 'HiggsMatchedIndex', 'MatchedGenPt', 'JetId', 'PuId', 'HadronFlavour', 'FatJetMatchedIndex', 'RawFactor', 'LooseBTagEffSF', 'MediumBTagEffSF', 'TightBTagEffSF'] :
            try :
                variables.remove('jet{}{}'.format(jet_number,jetvar))
            except:
                pass

    for jet_number in range(1,7) :
        for jetvar in ['DeepFlavB', 'BTagSF', 'TightTTWeight', 'MediumTTWeight', 'LooseTTWeight', 'HiggsMatched', 'HasMuon', 'HasElectron', 'FatJetMatched', 'HiggsMatchedIndex', 'MatchedGenPt', 'JetId', 'PuId', 'HadronFlavour', 'FatJetMatchedIndex', 'RawFactor'] :
            try :
                variables.remove('bcand{}{}'.format(jet_number,jetvar))
            except:
                pass

    for jet_number in range(1,4) :
        variables.remove('h{}_t3_match'.format(jet_number))
        variables.remove('h{}_t2_dRjets'.format(jet_number))
        for hvar in ["pt", "eta", "phi", "mass", "match"] :
            variables.remove('h{}_t2_{}'.format(jet_number, hvar))
            variables.remove('h{}_{}'.format(jet_number, hvar))

        # MassRegressed is saved as Mass simply
        for fatvar in ["HasBJetCSVLoose", "MassSD", "HasMuon", "HasElectron", "HiggsMatched", "OppositeHemisphereHasBJet", "NSubJets", "HiggsMatchedIndex", "GenMatchIndex", "MassRegressed_UnCorrected", "PtOverMHH_MassRegressed", "PtOverMSD", "PtOverMRegressed", "MassSD_noJMS", "RawFactor", "MassRegressed_JMS_Down", "MassSD_JMS_Down", "MassRegressed", 'Tau3OverTau2', 'PtOverMHH', 'MatchedGenPt', "MassSD_UnCorrected"] :
            try :
                variables.remove('fatJet{}{}'.format(jet_number,fatvar))
            except:
                pass
        
    for hhhvar in ['hhh_resolved_mass', 'hhh_resolved_pt', 'hhh_t3_pt', 'hhh_mass', 'hhh_pt', "hh_eta", "hh_mass", "hh_phi", "hh_pt", "hhh_eta", "hhh_phi",] :
        #print("removed %s" % hhhvar)
        try :
            variables.remove(hhhvar)
        except:
            pass

    return variables




# 2018
wps = { 'loose'  : '0.0490',
        'medium' : '0.2783',
        'tight'  : '0.7100',
        }

wps_years = { 'loose' : {'2016APV': 0.0508, '2016': 0.0480, '2016PostAPV': 0.0480, '2017': 0.0532, '2018': 0.0490, '2022': 0.0490, '2022EE': 0.0490},
              'medium': {'2016APV': 0.2598, '2016': 0.2489, '2016PostAPV': 0.2489, '2017': 0.3040, '2018': 0.2783,'2022': 0.0490, '2022EE': 0.0490},
              'tight' : {'2016APV': 0.6502, '2016': 0.6377, '2016PostAPV': 0.6377, '2017': 0.7476, '2018': 0.7100, '2022': 0.0490, '2022EE': 0.0490},
        }

label_dict = {'L': [wps_years['loose'],'Loose'],
              'M': [wps_years['medium'],'Medium'],
              'T': [wps_years['tight'],'Tight'],
              }

def get_scans(year):
    scans = {}
    for j1 in ['L','M','T']:
        for j2 in ['L','M','T']:
            for j3 in ['L','M','T']:
                for j4 in ['L','M','T']:
                    for j5 in ['L','M','T']:
                        for j6 in ['L','M','T']:
                            cut = '(bcand1DeepFlavB > %f && bcand2DeepFlavB > %f && bcand3DeepFlavB > %f && bcand4DeepFlavB > %f && bcand5DeepFlavB > %f && bcand6DeepFlavB > %f)'%(label_dict[j1][0][year],label_dict[j2][0][year],label_dict[j3][0][year],label_dict[j4][0][year],label_dict[j5][0][year],label_dict[j6][0][year])
                            weight = 'eventWeight * bcand1%sBTagEffSF * bcand2%sBTagEffSF * bcand3%sBTagEffSF * bcand4%sBTagEffSF * bcand5%sBTagEffSF * bcand6%sBTagEffSF'%(label_dict[j1][1],label_dict[j2][1],label_dict[j3][1],label_dict[j4][1],label_dict[j5][1],label_dict[j6][1])
                            weightTT = '%s * bcand1%sTTWeight * bcand2%sTTWeight * bcand3%sTTWeight * bcand4%sTTWeight * bcand5%sTTWeight * bcand6%sTTWeight'%(weight,label_dict[j1][1],label_dict[j2][1],label_dict[j3][1],label_dict[j4][1],label_dict[j5][1],label_dict[j6][1])
                            point = j1+j2+j3+j4+j5+j6
                            scans[point] = [cut,weight,weightTT]
    return scans

tags = {'5tag' :  'bcand1DeepFlavB > %s && bcand2DeepFlavB > %s && bcand3DeepFlavB > %s && bcand4DeepFlavB > %s && bcand5DeepFlavB > %s && bcand6DeepFlavB < %s  ',
        '6tag' :  'bcand1DeepFlavB > %s && bcand2DeepFlavB > %s && bcand3DeepFlavB > %s && bcand4DeepFlavB > %s && bcand5DeepFlavB > %s && bcand6DeepFlavB > %s  ',
        '4tag' :  'bcand1DeepFlavB > %s && bcand2DeepFlavB > %s && bcand3DeepFlavB > %s && bcand4DeepFlavB > %s && bcand5DeepFlavB < %s && bcand6DeepFlavB < %s  ',
        '3tag' :  'bcand1DeepFlavB > %s && bcand2DeepFlavB > %s && bcand3DeepFlavB > %s && bcand4DeepFlavB < %s && bcand5DeepFlavB < %s && bcand6DeepFlavB < %s  ',
        '2tag' :  'bcand1DeepFlavB > %s && bcand2DeepFlavB > %s && bcand3DeepFlavB < %s && bcand4DeepFlavB < %s && bcand5DeepFlavB < %s && bcand6DeepFlavB < %s  ',
        '1tag' :  'bcand1DeepFlavB > %s && bcand2DeepFlavB < %s && bcand3DeepFlavB < %s && bcand4DeepFlavB < %s && bcand5DeepFlavB < %s && bcand6DeepFlavB < %s  ',
        '0tag' :  'bcand1DeepFlavB < %s && bcand2DeepFlavB < %s && bcand3DeepFlavB < %s && bcand4DeepFlavB < %s && bcand5DeepFlavB < %s && bcand6DeepFlavB < %s  ',
        '0ptag' :  '1',

        }

#tags = {'high': 'bcand1DeepFlavB > %s && bcand2DeepFlavB > %s && bcand3DeepFlavB > %s && bcand4DeepFlavB > %s && bcand5DeepFlavB > %s && bcand6DeepFlavB > %s'%(wps['tight'], wps['tight'], wps['tight'], wps['tight'], wps['tight'], wps['tight']),
#         'middle' : '(bcand1DeepFlavB < %s && bcand1DeepFlavB > %s) && (bcand2DeepFlavB < %s && bcand2DeepFlavB > %s) && (bcand3DeepFlavB < %s && bcand3DeepFlavB > %s) && (bcand4DeepFlavB < %s && bcand4DeepFlavB > %s) && (bcand5DeepFlavB < %s && bcand5DeepFlavB > %s) && (bcand6DeepFlavB < %s && bcand6DeepFlavB > %s)'%(wps['tight'], wps['medium'],wps['tight'], wps['medium'],wps['tight'], wps['medium'],wps['tight'], wps['medium'],wps['tight'], wps['medium'],wps['tight'], wps['medium']),
#         'low' : '(bcand1DeepFlavB < %s && bcand1DeepFlavB > %s) && (bcand2DeepFlavB < %s && bcand2DeepFlavB > %s) && (bcand3DeepFlavB < %s && bcand3DeepFlavB > %s) && (bcand4DeepFlavB < %s && bcand4DeepFlavB > %s) && (bcand5DeepFlavB < %s && bcand5DeepFlavB > %s) && (bcand6DeepFlavB < %s && bcand6DeepFlavB > %s)'%(wps['medium'], wps['loose'],wps['medium'], wps['loose'],wps['medium'], wps['loose'],wps['medium'], wps['loose'],wps['medium'], wps['loose'],wps['medium'], wps['loose']),
#
#        }

# 2016
# HLT_QuadJet45_TripleBTagCSV_p087                              36.47/36.47
# HLT_PFHT400_SixJet30_DoubleBTagCSV_p056
# HLT_PFHT450_SixJet40_BTagCSV_p056
# HLT_AK8PFJet360_TrimMass30
# HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20

# HLT_AK8PFJet450                                               33.64/36.47

# HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200                     25.36/36.47
# HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq460                         25.36/36.47

# HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20               20.20/36.47
# HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20                  20.20/36.47

# HLT_PFJet450                                                  16.94/36.47
# HLT_PFMET120_BTagCSV_p067                                     16.94/36.47

# HLT_QuadJet45_DoubleBTagCSV_p087                              1.29/36.47

# 2017

# HLT_PFJet500
# HLT_PFHT1050
# HLT_AK8PFJet550

# HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0     36.67/41.48
# HLT_AK8PFJet400_TrimMass30                                    36.67/41.48

# HLT_AK8PFHT750_TrimMass50                                     30.90/41.48

# HLT_AK8PFJet360_TrimMass30                                    28.23/41.48
# HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1                 28.23/41.48

# HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2                17.68/41.48

# HLT_PFJet450                                                  10.45/41.48

# HLT_AK8PFJet330_PFAK8BTagCSV_p17                              7.73/41.48
# HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2                    7.73/41.48

# HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2                    5.30/41.48
# HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5                          5.30/41.48
# HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1          5.30/41.48

# 2018
# HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 59.96/59.96
# HLT_PFHT1050
# HLT_PFJet500
# HLT_AK8PFJet500
# HLT_AK8PFJet400_TrimMass30
# HLT_AK8PFHT800_TrimMass50

# HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4            54.44/59.74
# HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1    54.44/59.74
# HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2              54.44/59.74

# HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94               42.28/59.96
# HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59                     42.28/59.96

# HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17               22.74/59.96

# HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1     9.25/59.96
# HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2               9.25/59.74

# HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1             1.41/59.96


hlt_sf_2016 = """
float getTriggerSF(int HLT_QuadJet45_TripleBTagCSV_p087, int HLT_PFHT400_SixJet30_DoubleBTagCSV_p056, int HLT_PFHT450_SixJet40_BTagCSV_p056, int HLT_AK8PFJet360_TrimMass30, int HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20, int HLT_AK8PFJet450, int HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200, int HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq460, int HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20, int HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20, int HLT_PFJet450, int HLT_QuadJet45_DoubleBTagCSV_p087 ){
    float triggerSF = 1;
        if (HLT_QuadJet45_TripleBTagCSV_p087 || HLT_PFHT400_SixJet30_DoubleBTagCSV_p056 || HLT_PFHT450_SixJet40_BTagCSV_p056 || HLT_AK8PFJet360_TrimMass30 || HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20) {triggerSF = 1;}
        else if (HLT_AK8PFJet450) {triggerSF = 33.64/36.47;}
        else if (HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200 || HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq460) {triggerSF=25.36/36.47;}
        else if (HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20 || HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20) {triggerSF = 20.20/36.47;}
        else if (HLT_PFJet450) {triggerSF = 16.94/36.47;}
        else if (HLT_QuadJet45_DoubleBTagCSV_p087) {triggerSF=1.29/36.47;}

    return triggerSF;
}
"""

hlt_sf_2017 = """
float getTriggerSF(int HLT_PFJet450, int HLT_PFJet500, int HLT_PFHT1050, int HLT_AK8PFJet550, int HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0, int HLT_AK8PFJet360_TrimMass30, int HLT_AK8PFHT750_TrimMass50, int HLT_AK8PFJet400_TrimMass30, int HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1, int HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2, int HLT_AK8PFJet330_PFAK8BTagCSV_p17, int HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2, int HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2, int HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5, int HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1 ){
    float triggerSF = 1;
        if (HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0) {triggerSF = 41.48/41.48;}
        else if (HLT_PFJet500 || HLT_PFHT1050 || HLT_AK8PFJet550) {triggerSF = 1;}
        else if (HLT_AK8PFJet400_TrimMass30 ) {triggerSF = 36.67/41.48;}
        else if (HLT_AK8PFHT750_TrimMass50) {triggerSF=30.90/41.48;}
        else if (HLT_AK8PFJet360_TrimMass30 || HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1) {triggerSF = 28.23/41.48;}
        else if (HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2) {triggerSF = 17.68/41.48;}
        else if (HLT_PFJet450) {triggerSF=10.45/41.48;}
        else if (HLT_AK8PFJet330_PFAK8BTagCSV_p17 || HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2) {triggerSF=7.73/41.48;}
        else if (HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 || HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 || HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1) {triggerSF=5.30/41.48;}

    return triggerSF;
}
"""

hlt_sf_2018 = """
float getTriggerSF( int HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5, int HLT_PFHT1050, int HLT_PFJet500, int HLT_AK8PFJet500, int HLT_AK8PFJet400_TrimMass30, int HLT_AK8PFHT800_TrimMass50, int HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4, int HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1, int HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2, int HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94, int HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59, int HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17, int HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1, int HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2, int HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1 ){
    float triggerSF = 1;
        if (HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 || HLT_PFHT1050 || HLT_PFJet500 || HLT_AK8PFJet500 || HLT_AK8PFJet400_TrimMass30 || HLT_AK8PFHT800_TrimMass50) {triggerSF = 1;}
        else if ( HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 || HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1 || HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2) {triggerSF = 54.44/59.74;}
        else if (HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 || HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59) {triggerSF=42.28/59.96;}
        else if (HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17) {triggerSF = 22.74/59.96;}
        else if (HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1 || HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2) {triggerSF = 9.25/59.96;}
        else if (HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1) {triggerSF=1.41/59.96;}

    return triggerSF;
}
"""

hlt_sf_2022 = """
float getTriggerSF(){
    float triggerSF = 1;
    return triggerSF;
}
"""




hlt_method_2016 = 'getTriggerSF( HLT_QuadJet45_TripleBTagCSV_p087,  HLT_PFHT400_SixJet30_DoubleBTagCSV_p056,  HLT_PFHT450_SixJet40_BTagCSV_p056,  HLT_AK8PFJet360_TrimMass30,  HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20,  HLT_AK8PFJet450,  HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200,  HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq460,  HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20,  HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20,  HLT_PFJet450,  HLT_QuadJet45_DoubleBTagCSV_p087 );'

hlt_method_2017 = ' getTriggerSF( HLT_PFJet450,  HLT_PFJet500,  HLT_PFHT1050,  HLT_AK8PFJet550,  HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0,  HLT_AK8PFJet360_TrimMass30,  HLT_AK8PFHT750_TrimMass50,  HLT_AK8PFJet400_TrimMass30,  HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1,  HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2,  HLT_AK8PFJet330_PFAK8BTagCSV_p17,  HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2,  HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2,  HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5,  HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1 );'

hlt_method_2018 = ' getTriggerSF(HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5,HLT_PFHT1050,HLT_PFJet500,HLT_AK8PFJet500,HLT_AK8PFJet400_TrimMass30,HLT_AK8PFHT800_TrimMass50,HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4,HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1,HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2,HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94,HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17,HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1,HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2, HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1);'

hlt_method_2022 = 'getTriggerSF()'


triggersCorrections = {
                       '2016' : [hlt_sf_2016,hlt_method_2016],
                       '2017' : [hlt_sf_2017,hlt_method_2017],
                       '2018' : [hlt_sf_2018,hlt_method_2018],
                       '2022' : [hlt_sf_2022,hlt_method_2022],
                       '2022EE' : [hlt_sf_2022,hlt_method_2022],
        }

computeMHHH = '''
    float computeMHHH(int type, float h1_t3_mass, float h1_t3_pt, float h1_t3_eta, float h1_t3_phi,float h2_t3_mass, float h2_t3_pt, float h2_t3_eta, float h2_t3_phi, float h3_t3_mass, float h3_t3_pt, float h3_t3_eta, float h3_t3_phi) {
        TLorentzVector h1;
        TLorentzVector h2;
        TLorentzVector h3;

        h1.SetPtEtaPhiM(h1_t3_pt, h1_t3_eta, h1_t3_phi, h1_t3_mass);
        h2.SetPtEtaPhiM(h2_t3_pt, h2_t3_eta, h2_t3_phi, h2_t3_mass);
        h3.SetPtEtaPhiM(h3_t3_pt, h3_t3_eta, h3_t3_phi, h3_t3_mass);

        if (type == 0)
            return (h1+h2+h3).M();
        else if (type == 1)
            return (h1+h2+h3).Pt();
        else if (type == 2)
            return (h1+h2+h3).Eta();
        else return 0;
    }

'''

def init_mhhh():
    ROOT.gInterpreter.Declare(computeMHHH)

def addMHHH(df):
    df = df.Define('mHHH', 'computeMHHH(0,h1_t3_mass,h1_t3_pt,h1_t3_eta,h1_t3_phi,h2_t3_mass,h2_t3_pt,h2_t3_eta,h2_t3_phi,h3_t3_mass,h3_t3_pt,h3_t3_eta,h3_t3_phi)') # for compatibility with boosted BDT
    df = df.Define('HHH_mass', 'computeMHHH(0, h1_t3_mass,h1_t3_pt,h1_t3_eta,h1_t3_phi,h2_t3_mass,h2_t3_pt,h2_t3_eta,h2_t3_phi,h3_t3_mass,h3_t3_pt,h3_t3_eta,h3_t3_phi)')
    df = df.Define('HHH_pt', 'computeMHHH(1, h1_t3_mass,h1_t3_pt,h1_t3_eta,h1_t3_phi,h2_t3_mass,h2_t3_pt,h2_t3_eta,h2_t3_phi,h3_t3_mass,h3_t3_pt,h3_t3_eta,h3_t3_phi)')
    df = df.Define('HHH_eta', 'computeMHHH(2, h1_t3_mass,h1_t3_pt,h1_t3_eta,h1_t3_phi,h2_t3_mass,h2_t3_pt,h2_t3_eta,h2_t3_phi,h3_t3_mass,h3_t3_pt,h3_t3_eta,h3_t3_phi)')
    return df

def drawText(x, y, text, color = ROOT.kBlack, fontsize = 0.05, font = 42, doNDC = True, alignment = 12):
    tex = ROOT.TLatex()
    if doNDC:
        tex.SetNDC()
    ROOT.SetOwnership(tex, False)
    tex.SetTextAlign(alignment)
    tex.SetTextSize(fontsize)
    tex.SetTextFont(font)
    tex.SetTextColor(color)
    tex.DrawLatex(x, y, text)

mva_variables = ['h_fit_mass','h1_t3_mass','h2_t3_mass','h3_t3_mass','h2_t3_dRjets','h3_t3_dRjets','jet1Pt','jet2Pt','jet3Pt','jet4Pt','jet5Pt','jet6Pt','jet1Eta','jet2Eta','jet3Eta','jet4Eta','jet5Eta','jet6Eta','jet1Phi','jet2Phi','jet3Phi','jet4Phi','jet5Phi','jet6Phi','jet1DeepFlavB','jet2DeepFlavB','jet3DeepFlavB','jet4DeepFlavB','jet5DeepFlavB','jet6DeepFlavB','fatJet1Mass','fatJet1Pt','fatJet1Eta','fatJet1PNetXbb','fatJet1PNetQCD','fatJet2Mass','fatJet2Pt','fatJet2Eta','fatJet2PNetXbb','fatJet3Mass','fatJet3Pt','fatJet3Eta','fatJet3PNetXbb','fatJet2PNetQCD','fatJet3PNetQCD','jet7Pt','jet7Eta','jet7Phi','jet7DeepFlavB','jet8Pt','jet8Eta','jet8Phi','jet8DeepFlavB','jet9Pt','jet9Eta','jet9Phi','jet9DeepFlavB','jet10Pt','jet10Eta','jet10Phi','jet10DeepFlavB','mHHH','nloosebtags','nmediumbtags','ntightbtags','ht','met','lep1Pt','lep1Eta','lep1Phi','lep2Pt','lep2Eta','lep2Phi','nsmalljets','nfatjets','ntaus','nleps','tau1Pt','tau1Eta','tau1Phi','tau1Mass', 'tau2Pt','tau2Eta','tau2Phi','tau2Mass','lep1Pt','lep1Eta','lep1Phi','lep2Pt','lep2Eta','lep2Phi']

#save_variables = ['h_fit_mass','h1_t3_mass','h2_t3_mass','h3_t3_mass','h2_t3_dRjets','h3_t3_dRjets','jet1Pt','jet2Pt','jet3Pt','jet4Pt','jet5Pt','jet6Pt','jet1Eta','jet2Eta','jet3Eta','jet4Eta','jet5Eta','jet6Eta','jet1Phi','jet2Phi','jet3Phi','jet4Phi','jet5Phi','jet6Phi','jet1DeepFlavB','jet2DeepFlavB','jet3DeepFlavB','jet4DeepFlavB','jet5DeepFlavB','jet6DeepFlavB','fatJet1Mass','fatJet1Pt','fatJet1Eta','fatJet2Mass','fatJet1PNetXbb','fatJet2Pt','fatJet2Eta','fatJet2PNetXbb','fatJet3Mass','fatJet3Pt','fatJet3Eta','fatJet3PNetXbb','fatJet2PNetQCD','fatJet3PNetQCD','jet7Pt','jet7Eta','jet7Phi','jet7DeepFlavB','jet8Pt','jet8Eta','jet8Phi','jet8DeepFlavB','jet9Pt','jet9Eta','jet9Phi','jet9DeepFlavB','jet10Pt','jet10Eta','jet10Phi','jet10DeepFlavB','mHHH','nloosebtags','nmediumbtags','ntightbtags','ht','met','lep1Pt','lep1Eta','lep1Phi','lep2Pt','lep2Eta','lep2Phi','nsmalljets','nfatjets','event']

save_variables = list(histograms_dict.keys()) + ['event','nsmalljets','nfatjets','bcand1Mass','bcand2Mass','bcand1bRegCorr','bcand2bRegCorr','bcand1DeepFlavB','bcand2DeepFlavB','ntaus','nleps','tau1Pt','tau1Eta','tau1Phi','tau1Mass', 'tau2Pt','tau2Eta','tau2Phi','tau2Mass','lep1Pt','lep1Eta','lep1Phi','lep2Pt','lep2Eta','lep2Phi']#,'ProbHHH','ProbQCD','ProbTT','ProbVV','ProbVJets','ProbHH4b','ProbHH2b2tau','ProbHHH4b2tau','ProbDY']

from calibrations import btag_init, addBTagSF, addBTagEffSF

def initialise_df(df,year,proc):

    lumi = luminosities[year]
    if '2016' in year:
        df = df.Define('triggerSF', triggersCorrections['2016'][1] )
        #df = df.Define('triggerSF', '1')
        
    else:
        df = df.Define('triggerSF', triggersCorrections[year][1] )
    #cutWeight = '(%f * weight * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF)'%(lumi)
    cutWeight = '(%f * xsecWeight * l1PreFiringWeight * puWeight * genWeight * triggerSF * fatJetFlavTagWeight * flavTagWeight)'%(lumi)
    if 'JetHT' in proc or 'BTagCSV' in proc or 'SingleMuon' in proc or 'JetMET' in proc:
        df = df.Define('eventWeight','1')
    else:
        df = df.Define('eventWeight',cutWeight)
    df = addMHHH(df)

    wp_loose = wps_years['loose'][year]
    wp_medium = wps_years['medium'][year]
    wp_tight = wps_years['tight'][year]

    count_loose = []
    count_medium = []
    count_tight = []

    #for jet in ['jet1','jet2','jet3','jet4','jet5','jet6','jet7','jet8','jet9','jet10']:
    #    count_loose.append('int(%sDeepFlavB > %f)'%(jet,wp_loose))
    #    count_medium.append('int(%sDeepFlavB > %f)'%(jet,wp_medium))
    #    count_tight.append('int(%sDeepFlavB > %f)'%(jet,wp_tight))

    #nloose = '+'.join(count_loose)
    #nmedium = '+'.join(count_medium)
    #ntight = '+'.join(count_tight)


    #df = df.Define('nloosebtags',nloose)
    #df = df.Define('nmediumbtags',nmedium)
    #df = df.Define('ntightbtags',ntight)

    #df = addBTagEffSF(df,proc,'loose')
    #df = addBTagEffSF(df,proc,'medium')
    #df = addBTagEffSF(df,proc,'tight')

    return df




getmax = '''
int get_max_prob(float ProbHHH, float ProbQCD, float ProbTT, float ProbVJets, float ProbVV, float ProbHHH4b2tau, float ProbHH4b, float ProbHH2b2tau){
    std::vector<float> probs;
    probs.push_back(ProbHHH); // 1
    probs.push_back(ProbQCD); // 2
    probs.push_back(ProbTT); // 3
    probs.push_back(ProbVJets); // 4
    probs.push_back(ProbVV); // 5
    probs.push_back(ProbHHH4b2tau); // 6
    probs.push_back(ProbHH4b); // 7
    probs.push_back(ProbHH2b2tau); // 8
    //probs.push_back(ProbDY); // 9

    auto it = std::max_element(probs.begin(), probs.end());
    int index = std::distance(probs.begin(), it);

    //std::cout << index << " " << probs[index] << std::endl;

    return index + 1;

}

'''

def init_get_max_prob():
    ROOT.gInterpreter.Declare(getmax)


getmaxcat = '''
int get_max_cat(float Prob3bh0h, float Prob2bh1h, float Prob1bh2h, float Prob0bh3h, float Prob2bh0h, float Prob1bh1h, float Prob0bh2h, float Prob1bh0h, float Prob0bh1h, float Prob0bh0h){
    std::vector<float> probs;
    probs.push_back(Prob0bh0h); // 0

    probs.push_back(Prob3bh0h); // 1
    probs.push_back(Prob2bh1h); // 2
    probs.push_back(Prob1bh2h); // 3
    probs.push_back(Prob0bh3h); // 4
    probs.push_back(Prob2bh0h); // 5
    probs.push_back(Prob1bh1h); // 6
    probs.push_back(Prob0bh2h); // 7
    probs.push_back(Prob1bh0h); // 8
    probs.push_back(Prob0bh1h); // 9

    auto it = std::max_element(probs.begin(), probs.end());
    int index = std::distance(probs.begin(), it);

    //std::cout << index << " " << probs[index] << std::endl;

    return index;

}

'''

def init_get_max_cat():
    ROOT.gInterpreter.Declare(getmaxcat)






cat = '''
    int categorisation(int nAK4HiggsReco, int nAK8HiggsReco){
        int ret(0);

        // 3 reco Higgs
        if (nAK8HiggsReco == 3 &&  nAK4HiggsReco == 0) {ret = 1;}
        else if (nAK8HiggsReco == 2 && nAK4HiggsReco == 1) {ret = 2;}
        else if (nAK8HiggsReco == 1 && nAK4HiggsReco == 2) {ret = 3;}
        else if (nAK8HiggsReco == 0 && nAK4HiggsReco == 3) {ret = 4;}

        // 2 reco Higgs
        else if (nAK8HiggsReco == 2 && nAK4HiggsReco == 0) {ret = 5;}
        else if (nAK8HiggsReco == 1 && nAK4HiggsReco == 1) {ret = 6;}
        else if (nAK8HiggsReco == 0 && nAK4HiggsReco == 2) {ret = 7;}

        // 1 reco Higgs
        else if (nAK8HiggsReco == 1 && nAK4HiggsReco == 0) {ret = 8;}
        else if (nAK8HiggsReco == 0 && nAK4HiggsReco == 1) {ret = 9;}

        // 0 reco Higgs
        else  {ret = 0;}

        return ret;

    }
'''

ROOT.gInterpreter.Declare(cat)


def matching_variables(df):
    higgsmatched = []
    h1match = []
    h2match = []
    h3match = []
    for j in ['jet1','jet2','jet3','jet4','jet5','jet6','jet7','jet8','jet9','jet10']:
        higgsmatched.append('int(%sHiggsMatched)'%j)
        h1match.append('int(%sHiggsMatchedIndex == 1 && %sFatJetMatched == 0)'%(j,j))
        h2match.append('int(%sHiggsMatchedIndex == 2 && %sFatJetMatched == 0)'%(j,j))
        h3match.append('int(%sHiggsMatchedIndex == 3 && %sFatJetMatched == 0)'%(j,j))

    higgsMatchVar = '+'.join(higgsmatched)
    h1MatchVar = '+'.join(h1match)
    h2MatchVar = '+'.join(h2match)
    h3MatchVar = '+'.join(h3match)

    fatjetmatched = []
    fj_h1match = []
    fj_h2match = []
    fj_h3match = []
    for j in ['fatJet1','fatJet2','fatJet3']:
        fatjetmatched.append('int(%sHiggsMatched)'%j)
        fj_h1match.append('int(%sHiggsMatchedIndex == 1)'%j)
        fj_h2match.append('int(%sHiggsMatchedIndex == 2)'%j)
        fj_h3match.append('int(%sHiggsMatchedIndex == 3)'%j)

    fjMatchVar = '+'.join(fatjetmatched)
    fj_h1MatchVar = '+'.join(fj_h1match)
    fj_h2MatchVar = '+'.join(fj_h2match)
    fj_h3MatchVar = '+'.join(fj_h3match)

    df = df.Define('nAK4matched', higgsMatchVar)
    df = df.Define('nAK8matched', fjMatchVar)
    df = df.Define('h1Match',h1MatchVar)
    df = df.Define('h2Match',h2MatchVar)
    df = df.Define('h3Match',h3MatchVar)
    df = df.Define('fj_h1Match',fj_h1MatchVar)
    df = df.Define('fj_h2Match',fj_h2MatchVar)
    df = df.Define('fj_h3Match',fj_h3MatchVar)

    df = df.Define('nAK4HiggsReco', 'int(h1Match >= 2)+ int(h2Match >= 2)+ int(h3Match >= 2)')
    df = df.Define('nAK8HiggsReco', 'int(fj_h1Match >= 1)+ int(fj_h2Match >= 1)+ int(fj_h3Match >= 1)')
    df = df.Define('categorisation','categorisation( nAK4HiggsReco,nAK8HiggsReco)')

    return df


def applySelection(df, year):
    print("Applying selection: passmetfilter")
    df = df.Filter('passmetfilters')
    print("Applying nsmalljets >= 4 || nprobejets > 0")
    df = df.Filter('nsmalljets >= 4 || nprobejets > 0')
    print("Applying trigger")
    if '2016' in year:
        hlt = hlt_paths['2016']
    else:
        hlt = hlt_paths[year]
    df = df.Filter(hlt)
    print("Filter jet veto")
    #df = df.Filter('PassJetVeto == 1')
    print("filter HT")
    
    df = df.Filter('ht > 450')

    return df
