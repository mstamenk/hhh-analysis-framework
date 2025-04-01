import os


year = '2017'

script = 'python3 prepare_uniform_draw_samples.py --year %s '%year

for ak4 in ['4','5','6','7','8','9','10']:
#for ak4 in ['4']:
    for ak8 in ['0','1','2','3']:
        lab = 'ak4_%s_ak8_%s'%(ak4,ak8)
        cmd = script + ' --lab %s'%lab 
        os.system(cmd)
