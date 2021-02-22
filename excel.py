# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 16:19:35 2020
Function: Excel IO
@author: Administrator
"""

import csv,os

path='/mnt57/TestSetNew/ID1215005/jieguo'
ls=os.listdir(path)
ls.sort()
excel_path='/mnt57/TestSetNew/ID1215005/ITS结果记录.xlsx'
with open(excel_path, 'w', newline='') as csvfile:
    fieldnames = ['图片名', '结果']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,dialect='excel-tab')

    writer.writeheader()
    for i in range(len(ls)):
        writer.writerow({'图片名': ls[i]})