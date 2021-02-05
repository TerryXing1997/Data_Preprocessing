# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:10:24 2020
time
@author: Terry Xing

"""
import timeit,random

for i in range(10000,1000001,20000):
    t=timeit.Timer("random.randrange(%d) in x"%i,
                   "from __main__ import random,x")
    x={j:None for j in range(i)}
    time_one=t.timeit(number=1000)
    x=list(range(i))
    time_two=t.timeit(number=1000)
    print("%d,%10.3f,%10.3f"%(i,time_one,time_two))
