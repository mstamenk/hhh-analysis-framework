# Script to check log output

import os, glob
import re


path = 'log'

files = glob.glob(path + '/*')

ok = 0
fail = 0
run = 0

running = []
failed = []

res = 'ResidentSetSize'
term = 'Normal termination'

for f in files:
    with open(f,'r') as f_in:
        text = f_in.read()
    



    if 'Normal termination' in text:
        if 'return value 0' in text:
            ok += 1 
        else:
            if text.rfind(term) > text.rfind(res):
                fail += 1
                failed.append(f)
            else:
                run += 1 
                running.append(f)

    else:
        run += 1
        running.append(f)

print()
print("Runningjobs:")
for el in running:
    print(el)
print()
print("Failed jobs:")
for el in failed:
    print(el)
print()
print("Finished files:", ok)
print("Failed jobs", fail)
print("Running", run)
print()


resub = False
for el in failed:
    cmd =  'condor_submit %s\n'%(el.replace('job','submit').replace('.log','').replace('log/','jobs/'))
    if resub:
        os.system(cmd)

#print(resub)
