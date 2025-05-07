# Script to check log output

import os, glob

path = 'log'

files = glob.glob(path + '/*')

ok = 0
fail = 0
run = 0

running = []
failed = []

for f in files:
    with open(f,'r') as f_in:
        text = f_in.read()
    if 'Normal termination' in text:
        if 'return value 0' in text:
            ok += 1 
        else:
            fail += 1
            failed.append(f)

    else:
        run += 1
        running.append(f)

print()
print("Finished files:", ok)
print("Failed jobs", fail)
print("Running", run)
print()

print("Failed jobs:")
for el in failed:
    print(el)
print()
print("Runningjobs:")
for el in running:
    print(el)


