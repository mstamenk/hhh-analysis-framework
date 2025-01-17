import glob,os
import json
import numpy as np
import argparse
import matplotlib.pyplot as plt
from sympy import sympify
from matplotlib.colors import LogNorm
"""

Usage

python3 make_morphig_scans.py -i <YIELD_JSON> -d <DESTINATION> -c CAT0,CAT1,CAT2,CAT3,CAT4 -d reweight_extrapolations/

eg. python3 python/make_morphig_scans.py  -i kappaScan_yields.json -d results/morphing/sept19/ -t v1 

"""

parser = argparse.ArgumentParser()
parser.add_argument('-t',"--tag" , help="Tag",default='v0' )
parser.add_argument("-i","--inputJson",help="Input json file")
parser.add_argument("-d","--destination",help="Destination folder",default='./')
parser.add_argument("-c","--cats",help="Categories to process",default='CAT0')
args = parser.parse_args()

prefix=args.destination
catsToProcess=args.cats.split(",")

if not os.path.exists(prefix):
    cmd=f"mkdir -p {prefix}"
    print(f"[]$ {cmd}")
    os.system(cmd)

with open(args.inputJson) as f:
    yld_data=json.load(f)
# yld_data['c3_0_d4_0']=yld_data['ggHHH']


def getXSec(kl,k4): 
    return 0.00056211881548697*k4**2 + 0.00160902810704708*k4*kl**2 - 0.00869046450312655*k4*kl + 0.00293635270939005*k4 + 0.00131944405537002*kl**4 - 0.0139200207121885*kl**3 + 0.0611291498682321*kl**2 - 0.108945577838385*kl + 0.0967399694981736

def getk3k4FromKey(key):
    k3=float(key.split('_')[1].replace('m','-').replace('p','.'))
    k4=float(key.split('_')[3].replace('m','-').replace('p','.'))
    return k3,k4
def getk3k4FromC3D4Key(key):
    k3=float(key.split('_')[1].replace('m','-').replace('p','.'))+1
    k4=float(key.split('_')[3].replace('m','-').replace('p','.'))+1
    return k3,k4

def getXsectionForName(key):
    k3,k4=getk3k4FromKey(key)
    return getXSec(k3,k4)


##new kappa reweight basis marix
sfData_={
        'k3_1p0_k4_1p0': '-0.000230194469139919*k4**2 + 9.54258784280229e-5*k4*kl**2 - 0.000231704186554263*k4*kl + 0.0026522113472382*k4 + 0.000207881988272513*kl**4 - 0.0015765095632233*kl**3 - 0.0256643317935326*kl**2 + 0.114807536504801*kl + 0.90993968429371', 
        'k3_m13p0_k4_m100p0': '8.20464301255096e-6*k4**2 - 2.46190508295945e-5*k4*kl**2 + 8.84640077878213e-5*k4*kl + 0.000621767900414949*k4 + 1.21934967879285e-6*kl**4 - 0.000173939061075318*kl**3 + 0.000630523539889504*kl**2 + 0.00523654496423241*kl - 0.00638816629311111', 
        'k3_m10p0_k4_100p0': '-4.43061860508466e-5*k4**2 + 8.62762694980419e-5*k4*kl**2 - 0.000176456811547389*k4*kl - 0.00278084117397017*k4 + 4.40630334709723e-5*kl**4 - 0.000321325699701906*kl**3 - 0.000220709394123219*kl**2 + 0.0055792657803688*kl - 0.00216596581794429', 
        'k3_m4p0_k4_m20p0': '-0.000248917152640527*k4**2 + 0.000348323369668199*k4*kl**2 + 0.00108337940646609*k4*kl - 0.0234922163312777*k4 + 0.000103283880431471*kl**4 + 0.000388557485587008*kl**3 + 0.00581764837624364*kl**2 - 0.108772070181777*kl + 0.124772011147299', 
        'k3_m5p0_k4_30p0': '0.000300427861435221*k4**2 - 0.000407618813120411*k4*kl**2 - 0.000714216837965591*k4*kl + 0.0227885029003744*k4 - 0.000227624988813943*kl**4 + 0.00106597902957647*kl**3 + 0.00815697572605992*kl**2 - 0.0578487417123934*kl + 0.0268863168348473', 
        'k3_3p0_k4_m60p0': '0.00027126764921162*k4**2 - 0.000118795109896901*k4*kl**2 - 0.000184518679040965*k4*kl + 0.000941006989380806*k4 - 8.98184883809277e-5*kl**4 + 0.000578103818131512*kl**3 - 0.00321587668515312*kl**2 + 0.000662457379625349*kl + 0.00115617312612263', 
        'k3_8p0_k4_50p0': '9.89129520176692e-5*k4**2 + 1.76231895833318e-5*k4*kl**2 + 0.000862047385040645*k4*kl + 0.00329406251152581*k4 - 1.39820985427112e-5*kl**4 + 0.000494525139577925*kl**3 - 2.47848477085572e-6*kl**2 - 0.000602218359509962*kl - 0.00414849223492184', 
        'k3_8p0_k4_m20p0': '-0.000160185233270587*k4**2 + 4.53248560581442e-6*k4*kl**2 - 0.000708585889017221*k4*kl - 0.00410154925423102*k4 - 3.81606926576041e-5*kl**4 - 0.000572739459174484*kl**3 + 0.0158243756883029*kl**2 + 0.0459296273390511*kl - 0.0561773149846089', 
        'k3_16p0_k4_m80p0': '4.7899354248186e-6*k4**2 - 1.14821893650352e-6*k4*kl**2 - 1.8408395169128e-5*k4*kl + 7.70551105446908e-5*k4 + 1.31380165414369e-5*kl**4 + 0.000117348310302089*kl**3 - 0.00132612697291617*kl**2 - 0.00499240171439825*kl + 0.00612575392860702'   
}



sfData={ky : sympify(sfData_[ky])  for ky in sfData_}
print(f"Loaded {len(sfData)} Formulas")

yield_store={}
for ky in yld_data:
    
    if ('c3' not in ky):
        continue
    
    k3,k4=getk3k4FromC3D4Key(ky)
    prc=f"k3_{k3:.1f}_k4_{k4:.1f}".replace(".","p").replace("-","m")  
    yield_store[prc]=yld_data[ky]

source_basis=['k3_1p0_k4_1p0', 'k3_m13p0_k4_m100p0', 'k3_m10p0_k4_100p0',
              'k3_m4p0_k4_m20p0', 'k3_m5p0_k4_30p0', 'k3_3p0_k4_m60p0',
              'k3_8p0_k4_50p0', 'k3_8p0_k4_m20p0', 'k3_16p0_k4_m80p0']

basis_v2=[]
x=[-13 ,-10, -4,-5   , 1 , 3, 8  ,   8  , 16 ]
y=[-100,100,-20,30 , 1 ,-60, 50 , -20  , -80 ]
for i,j in zip(x,y):
    basis_v2.append( f"k3_{i:.1f}_k4_{j:.1f}".replace(".","p").replace("-","m") )

# TEMPLATE MAKER
# template="""
# def KEY_eval(k3=1.0,k4=1.0):
#     return FRMLA
# """
# for ky in sfData:
#     print(template.replace('KEY',ky).replace('FRMLA',str(sfData[ky])))

# for ky in sfData:    
#     print(f"funtion_store['{ky}']={ky}_eval")

        
def k3_1p0_k4_1p0_eval(k3=1.0,k4=1.0):
    return -0.000230194469139919*k4**2 + 9.54258784280229e-5*k4*k3**2 - 0.000231704186554263*k4*k3 + 0.0026522113472382*k4 + 0.000207881988272513*k3**4 - 0.0015765095632233*k3**3 - 0.0256643317935326*k3**2 + 0.114807536504801*k3 + 0.90993968429371


def k3_m13p0_k4_m100p0_eval(k3=1.0,k4=1.0):
    return 8.20464301255096e-6*k4**2 - 2.46190508295945e-5*k4*k3**2 + 8.84640077878213e-5*k4*k3 + 0.000621767900414949*k4 + 1.21934967879285e-6*k3**4 - 0.000173939061075318*k3**3 + 0.000630523539889504*k3**2 + 0.00523654496423241*k3 - 0.00638816629311111


def k3_m10p0_k4_100p0_eval(k3=1.0,k4=1.0):
    return -4.43061860508466e-5*k4**2 + 8.62762694980419e-5*k4*k3**2 - 0.000176456811547389*k4*k3 - 0.00278084117397017*k4 + 4.40630334709723e-5*k3**4 - 0.000321325699701906*k3**3 - 0.000220709394123219*k3**2 + 0.0055792657803688*k3 - 0.00216596581794429


def k3_m4p0_k4_m20p0_eval(k3=1.0,k4=1.0):
    return -0.000248917152640527*k4**2 + 0.000348323369668199*k4*k3**2 + 0.00108337940646609*k4*k3 - 0.0234922163312777*k4 + 0.000103283880431471*k3**4 + 0.000388557485587008*k3**3 + 0.00581764837624364*k3**2 - 0.108772070181777*k3 + 0.124772011147299


def k3_m5p0_k4_30p0_eval(k3=1.0,k4=1.0):
    return 0.000300427861435221*k4**2 - 0.000407618813120411*k4*k3**2 - 0.000714216837965591*k4*k3 + 0.0227885029003744*k4 - 0.000227624988813943*k3**4 + 0.00106597902957647*k3**3 + 0.00815697572605992*k3**2 - 0.0578487417123934*k3 + 0.0268863168348473


def k3_3p0_k4_m60p0_eval(k3=1.0,k4=1.0):
    return 0.00027126764921162*k4**2 - 0.000118795109896901*k4*k3**2 - 0.000184518679040965*k4*k3 + 0.000941006989380806*k4 - 8.98184883809277e-5*k3**4 + 0.000578103818131512*k3**3 - 0.00321587668515312*k3**2 + 0.000662457379625349*k3 + 0.00115617312612263


def k3_8p0_k4_50p0_eval(k3=1.0,k4=1.0):
    return 9.89129520176692e-5*k4**2 + 1.76231895833318e-5*k4*k3**2 + 0.000862047385040645*k4*k3 + 0.00329406251152581*k4 - 1.39820985427112e-5*k3**4 + 0.000494525139577925*k3**3 - 2.47848477085572e-6*k3**2 - 0.000602218359509962*k3 - 0.00414849223492184


def k3_8p0_k4_m20p0_eval(k3=1.0,k4=1.0):
    return -0.000160185233270587*k4**2 + 4.53248560581442e-6*k4*k3**2 - 0.000708585889017221*k4*k3 - 0.00410154925423102*k4 - 3.81606926576041e-5*k3**4 - 0.000572739459174484*k3**3 + 0.0158243756883029*k3**2 + 0.0459296273390511*k3 - 0.0561773149846089


def k3_16p0_k4_m80p0_eval(k3=1.0,k4=1.0):
    return 4.7899354248186e-6*k4**2 - 1.14821893650352e-6*k4*k3**2 - 1.8408395169128e-5*k4*k3 + 7.70551105446908e-5*k4 + 1.31380165414369e-5*k3**4 + 0.000117348310302089*k3**3 - 0.00132612697291617*k3**2 - 0.00499240171439825*k3 + 0.00612575392860702

funtion_store={}
funtion_store['k3_1p0_k4_1p0']=k3_1p0_k4_1p0_eval
funtion_store['k3_m13p0_k4_m100p0']=k3_m13p0_k4_m100p0_eval
funtion_store['k3_m10p0_k4_100p0']=k3_m10p0_k4_100p0_eval
funtion_store['k3_m4p0_k4_m20p0']=k3_m4p0_k4_m20p0_eval
funtion_store['k3_m5p0_k4_30p0']=k3_m5p0_k4_30p0_eval
funtion_store['k3_3p0_k4_m60p0']=k3_3p0_k4_m60p0_eval
funtion_store['k3_8p0_k4_50p0']=k3_8p0_k4_50p0_eval
funtion_store['k3_8p0_k4_m20p0']=k3_8p0_k4_m20p0_eval
funtion_store['k3_16p0_k4_m80p0']=k3_16p0_k4_m80p0_eval
 


k3_arr_=np.arange(-20 , 20,0.2)
k4_arr_=np.arange(-120,120,5.0)
target_k3=np.array(x)
target_k4=np.array(y)
k3_arr,k4_arr = np.meshgrid(k3_arr_, k4_arr_)

eras = list(yield_store['k3_1p0_k4_1p0'][catsToProcess[0]]['nominal'].keys())+ ['merged']


for ERA in eras:
    for cat in catsToProcess:
        yieldX={}
        for ky in funtion_store:
            #     print(yield_store[ky][cat]['nominal'])
            yld=0.0
            if ERA=='merged':
                for era in yield_store[ky][cat]['nominal']:
                    yld+=yield_store[ky][cat]['nominal'][era][0]
            else:
                yld=yield_store[ky][cat]['nominal'][ERA][0]
            yieldX[ky]=yld

        scale_factor_store={}
        yield_scaled={}
        yield_morphed=None
        for ky in funtion_store:
            scale_factor_store[ky]=funtion_store[ky](k3_arr,k4_arr)
            yield_scaled[ky]=scale_factor_store[ky]*yieldX[ky]
            if yield_morphed is None:
                yield_morphed=np.array(yield_scaled[ky])
            else:
                yield_morphed+=yield_scaled[ky]
        mask=yield_morphed<0.0
        ln=np.sum(yield_morphed < 1e10)
        print(f"Era : {ERA} , {cat}  | % of items in the morphed set with -ve yields : ",np.sum(mask)*100.0/ln," %")
        f,ax=plt.subplots(1,1,figsize=(8,8),dpi=150)
        ax=[ax]
        # pc=ax[0].pcolormesh(k3_arr,k4_arr,yield_morphed,cmap='jet',norm='log')
        pc = ax[0].pcolormesh(k3_arr, k4_arr, yield_morphed, cmap='jet', norm=LogNorm())
        plt.colorbar(pc,ax=ax[0])
        plt.text(-15.0,80,f"{ERA} , {cat}",bbox=dict(boxstyle="round",fc='w'),color='m',fontsize=12)
        foutname=f'{prefix}/{ERA}_{cat}_{args.tag}.png'
        print("  Exporting file ",foutname)
        plt.ylabel(r"$\kappa_{\lambda4}$",fontsize=16,loc='top')
        plt.xlabel(r"$\kappa_{\lambda3}$",fontsize=16,loc='right')
        plt.savefig(foutname,bbox_inches='tight')    
        plt.close(f)




