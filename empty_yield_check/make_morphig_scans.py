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
    return 0.000561288888888889*k4**2 + 0.00158596086279662*k4*kl**2 - 0.0087459608627966*k4*kl + 0.00309871111111112*k4 + 0.00131512995806449*kl**4 - 0.0137965222529057*kl**3 + 0.0608926961894692*kl**2 - 0.108911303894628*kl + 0.09674 

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

sfData_={
    'k3_20p0_k4_20p0': '9.06091847289793e-6*k3**4 - 4.9300725444354e-5*k3**3 - 1.28986682294749e-5*k3**2*k4 + 7.41895333895021e-5*k3**2 + 4.88255754744921e-5*k3*k4 - 2.35068699375642e-5*k3 + 1.04428564804817e-7*k4**2 - 4.64741922903036e-5*k4',
    'k3_2p0_k4_3p0': '0.00181859908941073*k3**4 + 0.0612344145588463*k3**3 - 0.117052946187404*k3**2*k4 - 0.0852248165990747*k3**2 + 0.495450856752831*k3*k4 - 0.34453745664648*k3 - 0.00366709259597299*k4**2 - 0.00802155837215495*k4',
    'k3_1p0_k4_1p0': '-0.0156567767640078*k3**4 + 0.296450661053703*k3**3 + 0.116113507117289*k3**2*k4 - 1.17541762393027*k3**2 - 0.943320520412559*k3*k4 + 1.28092989493571*k3 - 0.00623794854805879*k4**2 + 1.4471388065482*k4',
    'k3_3p0_k4_0p0': '-0.00432741529694681*k3**4 + 0.134315219432959*k3**3 - 0.0348180673391588*k3**2*k4 - 0.254218287446726*k3**2 - 0.0121776760133018*k3*k4 + 0.00399143379444837*k3 - 0.00120239049516266*k4**2 + 0.16843718336389*k4',
    'k3_0p0_k4_0p0': '0.00269506107191331*k3**4 + 0.0869752273166167*k3**3 - 0.173807100320902*k3**2*k4 - 0.32776033936777*k3**2 + 1.06104582179224*k3*k4 - 0.205596010021244*k3 + 0.00556313938999517*k4**2 - 1.44911579986085*k4 + 1.0',
    'k3_m0p5_k4_0p5': '0.00178625756289069*k3**4 - 0.128966102905578*k3**3 + 0.0878144535538641*k3**2*k4 + 0.614548792715285*k3**2 - 0.499940475718061*k3*k4 - 0.7311804061937*k3 - 0.00243811458821102*k4**2 + 0.65837559557351*k4',
    'k3_1p0_k4_100p0': '3.54406639377261e-6*k3**4 - 8.23419233486239e-5*k3**3 + 3.68602946798598e-6*k3**2*k4 + 0.000190060163750484*k3**2 - 0.000133213138375878*k3*k4 + 7.52070262542428e-5*k3 + 0.0001028747943406*k4**2 - 0.000159817018482608*k4',
    'k3_5p0_k4_10p0': '-0.000544382627375349*k3**4 + 0.00482523670822783*k3**3 + 0.00769645658563427*k3**2*k4 - 0.0138311282893779*k3**2 - 0.0199714878689513*k3*k4 + 0.0127645854332177*k3 + 3.21431122469228e-5*k4**2 + 0.00902857694637784*k4',
    'k3_2p0_k4_1p0': '0.0142160519792486*k3**4 - 0.454703013515982*k3**3 + 0.114062909229438*k3**2*k4 + 1.2416391532208*k3**2 - 0.0810021309692927*k3*k4 - 0.0164237414582671*k3 + 0.00784728450225797*k4**2 - 0.825636512988201*k4'
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

source_basis=['k3_20p0_k4_20p0', 'k3_2p0_k4_3p0', 'k3_1p0_k4_1p0',
              'k3_3p0_k4_0p0', 'k3_0p0_k4_0p0', 'k3_m0p5_k4_0p5',
              'k3_1p0_k4_100p0', 'k3_5p0_k4_10p0', 'k3_2p0_k4_1p0']

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
def k3_20p0_k4_20p0_eval(k3=1.0,k4=1.0):
    return 9.06091847289793e-6*k3**4 - 4.9300725444354e-5*k3**3 - 1.28986682294749e-5*k3**2*k4 + 7.41895333895021e-5*k3**2 + 4.88255754744921e-5*k3*k4 - 2.35068699375642e-5*k3 + 1.04428564804817e-7*k4**2 - 4.64741922903036e-5*k4


def k3_2p0_k4_3p0_eval(k3=1.0,k4=1.0):
    return 0.00181859908941073*k3**4 + 0.0612344145588463*k3**3 - 0.117052946187404*k3**2*k4 - 0.0852248165990747*k3**2 + 0.495450856752831*k3*k4 - 0.34453745664648*k3 - 0.00366709259597299*k4**2 - 0.00802155837215495*k4


def k3_1p0_k4_1p0_eval(k3=1.0,k4=1.0):
    return -0.0156567767640078*k3**4 + 0.296450661053703*k3**3 + 0.116113507117289*k3**2*k4 - 1.17541762393027*k3**2 - 0.943320520412559*k3*k4 + 1.28092989493571*k3 - 0.00623794854805879*k4**2 + 1.4471388065482*k4


def k3_3p0_k4_0p0_eval(k3=1.0,k4=1.0):
    return -0.00432741529694681*k3**4 + 0.134315219432959*k3**3 - 0.0348180673391588*k3**2*k4 - 0.254218287446726*k3**2 - 0.0121776760133018*k3*k4 + 0.00399143379444837*k3 - 0.00120239049516266*k4**2 + 0.16843718336389*k4


def k3_0p0_k4_0p0_eval(k3=1.0,k4=1.0):
    return 0.00269506107191331*k3**4 + 0.0869752273166167*k3**3 - 0.173807100320902*k3**2*k4 - 0.32776033936777*k3**2 + 1.06104582179224*k3*k4 - 0.205596010021244*k3 + 0.00556313938999517*k4**2 - 1.44911579986085*k4 + 1.0


def k3_m0p5_k4_0p5_eval(k3=1.0,k4=1.0):
    return 0.00178625756289069*k3**4 - 0.128966102905578*k3**3 + 0.0878144535538641*k3**2*k4 + 0.614548792715285*k3**2 - 0.499940475718061*k3*k4 - 0.7311804061937*k3 - 0.00243811458821102*k4**2 + 0.65837559557351*k4


def k3_1p0_k4_100p0_eval(k3=1.0,k4=1.0):
    return 3.54406639377261e-6*k3**4 - 8.23419233486239e-5*k3**3 + 3.68602946798598e-6*k3**2*k4 + 0.000190060163750484*k3**2 - 0.000133213138375878*k3*k4 + 7.52070262542428e-5*k3 + 0.0001028747943406*k4**2 - 0.000159817018482608*k4


def k3_5p0_k4_10p0_eval(k3=1.0,k4=1.0):
    return -0.000544382627375349*k3**4 + 0.00482523670822783*k3**3 + 0.00769645658563427*k3**2*k4 - 0.0138311282893779*k3**2 - 0.0199714878689513*k3*k4 + 0.0127645854332177*k3 + 3.21431122469228e-5*k4**2 + 0.00902857694637784*k4


def k3_2p0_k4_1p0_eval(k3=1.0,k4=1.0):
    return 0.0142160519792486*k3**4 - 0.454703013515982*k3**3 + 0.114062909229438*k3**2*k4 + 1.2416391532208*k3**2 - 0.0810021309692927*k3*k4 - 0.0164237414582671*k3 + 0.00784728450225797*k4**2 - 0.825636512988201*k4

funtion_store={}
funtion_store['k3_20p0_k4_20p0']=k3_20p0_k4_20p0_eval
funtion_store['k3_2p0_k4_3p0']=k3_2p0_k4_3p0_eval
funtion_store['k3_1p0_k4_1p0']=k3_1p0_k4_1p0_eval
funtion_store['k3_3p0_k4_0p0']=k3_3p0_k4_0p0_eval
funtion_store['k3_0p0_k4_0p0']=k3_0p0_k4_0p0_eval
funtion_store['k3_m0p5_k4_0p5']=k3_m0p5_k4_0p5_eval
funtion_store['k3_1p0_k4_100p0']=k3_1p0_k4_100p0_eval
funtion_store['k3_5p0_k4_10p0']=k3_5p0_k4_10p0_eval
funtion_store['k3_2p0_k4_1p0']=k3_2p0_k4_1p0_eval
 

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




