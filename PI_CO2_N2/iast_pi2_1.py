#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 11:08:30 2021

@author: root
"""

import pandas as pd
import pyiast
import csv
import func_iast as fi

df_pi2_co2 = pd.read_csv("PI-2-CO2-Ads-195K.csv")
df_pi2_n2 = pd.read_csv("PI-2-N2-Ads-195K.csv")

# Fit the isothermal data from experiment
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
i = 0
pressure_part = fi.array_proportion() * total_pressure # the pressure of each gas component
component_loading = fi.array_proportion()
amf_guess = fi.array_proportion()
selectivity = fi.array_proportion() # initial the selectivity array

# Perform IAST calculation
while i < 9:
    print("Out "+str(i))
    try:
        print(pressure_part[i])
        component_loading[i] = pyiast.iast(pressure_part[i], 
                                    [pi2_co2_isotherm, pi2_n2_isotherm],
                                    verboseflag=False,
                                    warningoff=True,
                                    adsorbed_mole_fraction_guess= [0.1, 0.9])
    except:
        print("change adsorbed_mole_fraction_guess")
        j = 1
        while j < 9:
            print("Inner " + str(j))
            try:
                component_loading[i] = pyiast.iast(pressure_part[i], 
                                    [pi2_co2_isotherm, pi2_n2_isotherm],
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

# Calculate selectivity of each proportion
i = 0
j = 0
while i < 9:
    try:
        selectivity[i, j] = pressure_part[i, j]/pressure_part[i, j+1]
        j = j+1
        selectivity[i, j] = fi.cal_selectivity(component_loading[i], pressure_part[i])
    except Exception as e:
        print(e)
        pass
    finally:
        i = i+1
        j = 0

# Write selectivity to csv file
headers = ['CO2/N2', 'Selectivity']
try:
    with open('selectivity_PI2.csv', 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(selectivity)
except Exception as e:
    print(e)


    

