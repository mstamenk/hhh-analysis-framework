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
parser.add_argument('--outsize',default = 1.0) # Maximum output filesize in GB
args = parser.parse_args()

year = args.year
version = args.version
typename = args.typename
regime = args.regime
outsize = args.outsize * 1024 # MB

path = os.path.join(args.inpath, version, 'mva-inputs-%s-%s'%(year,typename), regime)
files = glob.glob(os.path.join(path, '*.root'))

samples = {}
sizes = {}

for f in files:
    sample = os.path.basename(f)
    splits = sample.split('_tree_')

    sample_type = splits[0]
    if sample_type not in samples:
        samples[sample_type] = []
        sizes[sample_type] = []
    samples[sample_type].append(f)
    sizes[sample_type].append(float(os.path.getsize(f))/1024/1024) # MB

#print(samples)

output_path = os.path.join(args.outpath, '%s-merged-selection'%version, 'mva-inputs-%s-%s'%(year,typename), regime)

if not os.path.isdir(output_path):
    os.makedirs(output_path)

for sample in samples:
    fullsize = sum(sizes[sample])
    noutputs = int(fullsize / outsize)+1

    i = 0
    part = 0
    while i<len(samples[sample]):
        tohadd = []
        tohadd.append(i)
        i+=1
        while i<len(samples[sample]):
            if sum([sizes[sample][j] for j in tohadd]) + sizes[sample][i] < outsize:
                tohadd.append(i)
                i+=1
            else:
                break
        part+=1
        partstr = "_part"+str(part)
        if part==1 and i==len(samples[sample]): partstr=""
        cmd = f'hadd -f -j -n 0 {os.path.join(output_path, sample+partstr+".root")} {" ".join([samples[sample][j] for j in tohadd])}'
        print(">>> "+cmd)
        os.system(cmd)
