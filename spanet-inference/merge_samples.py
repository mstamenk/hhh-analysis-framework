import os, glob



# argument parser
import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('-v','--version', default='v28-QCD-modelling') # version of NanoNN production
parser.add_argument('--year', default='2018') # year
parser.add_argument('--typename', default='categorisation-spanet-boosted-classification') # typename
parser.add_argument('--regime', default='inclusive-weights') # regime
parser.add_argument('--inpath',default = '/users/mstamenk/scratch/mstamenk')
parser.add_argument('--outpath',default = '/users/mstamenk/scratch/mstamenk/eos-triple-h')
args = parser.parse_args()

year = args.year
version = args.version
typename = args.typename
regime = args.regime

path = os.path.join(args.inpath, version, 'mva-inputs-%s-%s'%(year,typename), regime)
files = glob.glob(os.path.join(path, '*.root'))

#files = [f for f in files if 'HHH' in f or 'HH' in f]

samples = []

ttsemileptonic = []
qcd = []
btagcsv = []

for f in files:
    sample = os.path.basename(f)
    splits = sample.split('_')

    sample_type = splits[0]
    if len(splits) > 2:
        sample_type = splits[0] + '_' + splits[1]
    samples.append(sample_type)

    if 'TTToSemiLeptonic' in f:
        ttsemileptonic.append(f)
    if 'QCD' in f and "bEnriched" not in f:
        qcd.append(f)
    if 'BTagCSV' in f:
        btagcsv.append(f)

samples = list(set(samples))

print(samples)

output_path = os.path.join(args.outpath, '%s-merged-selection'%version, 'mva-inputs-%s-%s'%(year,typename), regime)

if not os.path.isdir(output_path):
    os.makedirs(output_path)

for sample in samples:
    cmd = 'hadd -f -j -n 0 %s %s'%(os.path.join(output_path, '%s.root'%sample),os.path.join(path,'%s_*.root'%sample))
    print(cmd)
    #if 'QCD' in sample and "bEnriched" not in sample: continue
    #if 'TTToSemiLeptonic' in sample: continue
    #if 'BTagCSV' in sample: continue
    os.system(cmd)

# Special case for TTToSemiLeptonic because files too large
'''
print(ttsemileptonic)
third_index = len(ttsemileptonic) // 3

print(third_index)

ttsemileptonic_part1 = ttsemileptonic[:third_index]
ttsemileptonic_part2 = ttsemileptonic[third_index:2*third_index]
ttsemileptonic_part3 = ttsemileptonic[2*third_index:]
cmd_1 = 'hadd -f -j -n 0 %s/TTToSemiLeptonic_part1.root '%(output_path)

for el in ttsemileptonic_part1:
    cmd_1 += '%s '%el

print(cmd_1)
os.system(cmd_1)

cmd_2 = 'hadd -f -j -n 0 %s/TTToSemiLeptonic_part2.root '%(output_path)

for el in ttsemileptonic_part2:
    cmd_2 += '%s '%el

print(cmd_2)
os.system(cmd_2)

cmd_3 = 'hadd -f -j -n 0 %s/TTToSemiLeptonic_part3.root '%(output_path)

for el in ttsemileptonic_part3:
    cmd_3 += '%s '%el

print(cmd_3)
os.system(cmd_3)

cmd_4 = 'hadd -f %s/TTToSemiLeptonic.root %s/TTToSemiLeptonic_part1.root %s/TTToSemiLeptonic_part2.root %s/TTToSemiLeptonic_part3.root'%(output_path,output_path,output_path,output_path)

print(cmd_4)
os.system(cmd_4)

# Special case for QCD.root

cmd_qcd = 'hadd -f -j -n 0 %s/QCD.root '%output_path

for f in qcd:
    cmd_qcd += '%s '%f

print(cmd_qcd)
os.system(cmd_qcd)

# Special case for BTagCSV
if len(btagcsv) > 0:
    middle_index = len(btagcsv) // 2

    print(middle_index)

    btagcsv_part1 = btagcsv[:middle_index]
    btagcsv_part2 = btagcsv[middle_index:]

    cmd_1 = 'hadd -f -j -n 0 %s/BTagCSV_part1.root '%(output_path)

    for el in btagcsv_part1:
        cmd_1 += '%s '%el

    print(cmd_1)
    os.system(cmd_1)

    cmd_2 = 'hadd -f -j -n 0 %s/BTagCSV_part2.root '%(output_path)

    for el in btagcsv_part2:
        cmd_2 += '%s '%el

    print(cmd_2)
    os.system(cmd_2)

    cmd_3 = 'hadd -f %s/BTagCSV.root %s/BTagCSV_part1.root %s/BTagCSV_part2.root'%(output_path,output_path,output_path)
    print(cmd_3)
    os.system(cmd_3)
'''
