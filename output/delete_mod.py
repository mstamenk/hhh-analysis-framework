import os

# version = 'v33_new'
version = 'tmp_samples'
# year_list = ['2018','2017','2016_merged','run2']
# year_list = ['run2_separate']
year_list = ['v34_2016_test2']
category_list = ['ProbHHH6b_2bh0h_inclusive_CR','ProbHHH6b_1bh1h_inclusive_CR','ProbHHH6b_0bh2h_inclusive_CR','ProbHHH6b_0bh3h_inclusive_CR','ProbHHH6b_1bh2h_inclusive_CR','ProbHHH6b_2bh1h_inclusive_CR','ProbHHH6b_3bh0h_inclusive_CR','ProbHHH6b_0bh0h_inclusive_CR','ProbHHH6b_1Higgs_inclusive_CR','ProbHHH6b_2Higgs_inclusive_CR','ProbHHH6b_3Higgs_inclusive_CR']
# category_list = ['ProbHH4b_2bh0h_inclusive_CR','ProbHH4b_1bh1h_inclusive_CR','ProbHH4b_0bh2h_inclusive_CR','ProbHH4b_0bh3h_inclusive_CR','ProbHH4b_1bh2h_inclusive_CR','ProbHH4b_2bh1h_inclusive_CR','ProbHH4b_3bh0h_inclusive_CR','ProbHH4b_0bh0h_inclusive_CR','ProbHH4b_1Higgs_inclusive_CR','ProbHH4b_2Higgs_inclusive_CR','ProbHH4b_3Higgs_inclusive_CR']
var = 'ProbMultiH'
for year in year_list:
    for cat in category_list:
        # file_path = "%s/%s/%s/histograms_%s_sepa_era_mod.root"%(version,year,cat,var)
        file_path = "%s/%s/%s/histograms/histograms_%s_fixAsy_mod.root"%(version,year,cat,var)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"already delete: {file_path}")
        else:
            print(f"file not exist: {file_path}")
