import sympy as sp
import ROOT
import uproot
import numpy as np
import matplotlib.pyplot as plt
from array import array

xs_table = {'HHHTo6B_c3_0_d4_99'            :0.0010357238013624323,
            'HHHTo6B_c3_0_d4_minus1'        :7.158998771957761e-06,
            'HHHTo6B_c3_19_d4_19'           :0.026036314518323205,
            'HHHTo6B_c3_1_d4_0'             :5.070957463470081e-06,
            'HHHTo6B_c3_1_d4_2'             :2.7952492445696003e-06,
            'HHHTo6B_c3_2_d4_minus1'        :1.0094504339046402e-05,
            'HHHTo6B_c3_4_d4_9'             :4.3104126160076803e-05,
            'HHHTo6B_c3_minus1_d4_0'        :1.9833429268889604e-05,
            'HHHTo6B_c3_minus1_d4_minus1'    :1.9110417803509764e-05,
            'HHHTo6B_c3_minus1p5_d4_minus0p5':3.40368512253952e-05
}

br = 0.5824

for basis in xs_table:
    xs_br = xs_table[basis]
    xs = xs_br/(br*br*br)
    print("{} : {:.6g}".format(basis, xs))