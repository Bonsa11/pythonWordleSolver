# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:15:50 2020

@author: Sam
"""

def normalise(v):
    v = (v-min(v))/(max(v)-min(v))
    return(v)