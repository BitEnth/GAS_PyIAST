# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 14:09:30 2021

@author: Alison Elizabeth
"""

import pandas as pd
import numpy as np
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

total_pressure = 0.1  # total pressure (bar)
gas_proportion = np.array([0.1, 0.9])
row_num = 120
i = 0
pressure_part = gas_proportion # the pressure of each gas component
component_loading = fi.array_proportion_n(row_num)
amf_guess = fi.array_proportion()
selectivity = fi.array_proportion_n(row_num) # initial the selectivity array

# Perform IAST calculation
while i < row_num:
    print("Out "+str(i))
    try:
        print(total_pressure)
        pressure_part = gas_proportion * total_pressure
        component_loading[i] = pyiast.iast(pressure_part, 
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
                component_loading[i] = pyiast.iast(pressure_part, 
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
        total_pressure = total_pressure + 0.01

# Calculate selectivity of each proportion
i = 0
j = 0
total_pressure = 0.1
while i < row_num:
    try:
        selectivity[i, j] = total_pressure
        j = j+1
        selectivity[i, j] = fi.cal_selectivity(component_loading[i], pressure_part)
    except Exception as e:
        print(e)
        pass
    finally:
        i = i+1
        j = 0
        total_pressure = total_pressure + 0.01

# Write selectivity to csv file
headers = ['CO2/N2', 'Selectivity']
try:
    with open('selectivity_PI2_Pressure.csv', 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(selectivity)
except Exception as e:
    print(e)


    

