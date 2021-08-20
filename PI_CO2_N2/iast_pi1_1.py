# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 14:09:30 2021

@author: Alison Elizabeth
"""

import pandas as pd
import pyiast
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
i = 0
p = fi.array_proportion()
component_loading = fi.array_proportion()
amf_guess = fi.array_proportion()
selectivity = fi.array_proportion()
exception_rf = """Root finding for gas phase mole fractions failed.
        This is likely because the default guess in pyIAST is not good enough.
        Try a different starting guess for the gas phase mole fractions by
        passing an array or list gas_mole_fraction_guess to this function."""
# partial pressures are now P_total * y
# Perform IAST calculation
while i < 9:
    print("Out"+str(i))
    try:
        print(p[i])
        component_loading[i] = pyiast.iast(total_pressure * p[i], 
                                    [pi1_co2_isotherm, pi1_n2_isotherm],
                                    verboseflag=False,
                                    warningoff=True,
                                    adsorbed_mole_fraction_guess= [0.1, 0.9])
    except Exception as e:
        if str(e) is exception_rf:
            print(exception_rf)
        else:
            print(e)
        j = 1
        while j < 9:
            print(j)
            try:
                component_loading[i] = pyiast.iast(total_pressure * p[i], 
                                    [pi1_co2_isotherm, pi1_n2_isotherm],
                                    verboseflag=False,
                                    warningoff=True,
                                    adsorbed_mole_fraction_guess= amf_guess[j])
                break
            except:
                j = j+1
                pass
        pass
    finally:
        i = i+1

# Calculate selectivity of each component
i = 0
j = 0
while i < 9:
    try:
        selectivity[i, j] = p[i, j]/p[i, j+1]
        j = j+1
        selectivity[i, j] = fi.cal_selectivity(component_loading[i], p[i])
    except Exception as e:
        print(e)
        pass
    finally:
        i = i+1
        j = 0
        
print(selectivity)

