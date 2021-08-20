#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 15:21:16 2021

@author: root

IAST_Functions
"""
import numpy as np

def cal_selectivity(component_loadings, partial_pressures):
    """
    Calculate selectivity as a function of component loadings and bulk gas
    pressures

    :param component_loadings: numpy two demensions array of component loadings
    :param partial_pressures: 2D array of partial pressures of components
    """
    n_components = np.size(component_loadings)
    for i in range(n_components):
        for j in range(i + 1, n_components):
                  selectivity = (component_loadings[i] / component_loadings[j] /
                   (partial_pressures[i] / partial_pressures[j]))
    return selectivity

def array_proportion():

    a =  np.arange(18).reshape(9,2).astype(np.float64)
    i = 0
    j = 0
    x = 0.1
    y = 0.9
    while i < 9:
        a[i,j] = x
        j = j+1
        a[i,j] = y
        i = i+1
        x = x + 0.1
        y = y - 0.1
        j = 0
    
    return a
