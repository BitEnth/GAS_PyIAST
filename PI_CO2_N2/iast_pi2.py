# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 14:28:41 2021

@author: Alison Elizabeth
"""

import pandas as pd
import pyiast
import numpy as np
df_pi2_co2 = pd.read_csv("PI-2-CO2-Ads-195K.csv")
df_pi2_n2 = pd.read_csv("PI-2-N2-Ads-195K.csv")
pi2_co2_isotherm = pyiast.InterpolatorIsotherm(df_pi2_co2,
                                    loading_key="n_PI-2-CO2",
                                    pressure_key="P/P0",
                                     fill_value=df_pi2_co2['n_PI-2-CO2'].max())
pi2_n2_isotherm = pyiast.InterpolatorIsotherm(df_pi2_n2, 
                                              loading_key="n_PI-2-N2",
                                              pressure_key="P/P0",
                                              fill_value=df_pi2_n2['n_PI-2-N2'].max())
#pyiast.plot_isotherm(pi2_n2_isotherm)
total_pressure = 1  # total pressure (bar)
y = np.array([0.4, 0.6])  # gas mole fractions
# partial pressures are now P_total * y
# Perform IAST calculation
q = pyiast.iast(total_pressure * y, 
                [pi2_co2_isotherm, pi2_n2_isotherm],
                verboseflag=True,
                warningoff=False,
                adsorbed_mole_fraction_guess= [0.1,0.9])
# returns q = array([4.4612935, 13.86364776])