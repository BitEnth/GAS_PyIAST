# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 14:09:30 2021

@author: Alison Elizabeth
"""

import pandas as pd
import pyiast
import numpy as np
import func_iast as fi
df_pi1_co2 = pd.read_csv("PI-1-CO2-Ads-195K.csv")
df_pi1_n2 = pd.read_csv("PI-1-N2-Ads-195K.csv")
pi1_co2_isotherm = pyiast.InterpolatorIsotherm(df_pi1_co2,
                                    loading_key="n_PI-1-CO2",
                                    pressure_key="P/P0",
                                     fill_value=df_pi1_co2['n_PI-1-CO2'].max())
pi1_n2_isotherm = pyiast.InterpolatorIsotherm(df_pi1_n2, 
                                              loading_key="n_PI-1-N2",
                                              pressure_key="P/P0",
                                              fill_value=df_pi1_n2['n_PI-1-N2'].max())
#pyiast.plot_isotherm(pi2_n2_isotherm)
total_pressure = 1  # total pressure (bar)
y = np.array([0.9, 0.1])  # gas mole fractions
# partial pressures are now P_total * y
# Perform IAST calculation
q = pyiast.iast(total_pressure * y, 
                [pi1_co2_isotherm, pi1_n2_isotherm],
                verboseflag=False,
                warningoff=False,
                adsorbed_mole_fraction_guess= [0.3,0.7])
print(q)
s = fi.cal_selectivity(q, y)
# returns q = array([4.4612935, 13.86364776])
