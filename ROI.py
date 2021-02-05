# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 11:12:53 2020

Function: Filtering the test data set with the features you want

@author: Terry Xing
"""

import xml.etree.ElementTree as ET
from PIL import Image
import os,pathlib
import os.path as op
#定义处理单个xml文件的函数
def xml_process(xml_file):
    save_path=op.join(op.dirname(xml_file),'小图')
    if not op.exists(save_path):
        os.mkdir(save_path)
    tree=ET.parse(xml_file)
    root=tree.getroot()
    img_file=str(xml_file).replace('.xml','.jpg')
    if any(root.iter('object')):
        img=Image.open(img_file)
        n=0
        for i in root.iter('object'):
            if 'none'!=i[0].text:
                continue
            bndbox=i.find('bndbox')
            pos=tuple(map(int,[bndbox[0].text,bndbox[1].text,
                               bndbox[2].text,bndbox[3].text]))
            #裁剪图像并命名
            cropped=img.crop(pos)
            img_name=op.splitext(op.basename(img_file))[0]+'_'+str(n)+'.jpg'
            cropped.save(op.join(save_path,img_name))
            n+=1
        
path=r'D:\熊超\新视综\机动车组件输出及属性说明\ShiZongVehicleProperty\分类'
#打印计数
count=0
for x in pathlib.Path(path).glob('**\\*.xml'):
    try:
        xml_process(x)
        count+=1
        print('\r'+str(count),end='')
    except:
        pass















