#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 15:39:10 2021

@author: root
"""

import numpy as np

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

print(a)