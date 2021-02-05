# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:51:10 2020
实现功能：xml与图片一一对应,筛选出多余文件
注意事项：整个文件夹内不能存在重复的文件
@author: Terry Xing
"""

import pathlib,shutil,os,time
import os.path as op
def func(src,dst):
    global path
    for s in src.keys():
        if s in dst:
            try:
                shutil.move(src[s],op.dirname(dst[s]))
            except:
                del dst[s]
            else:
                del dst[s]
    for d in dst.keys():
        try:
            shutil.move(dst[d],path)
        except:
            pass
        
time_start=time.time()

#设置最长公共路径,windows系统下以'\\'或'/'为间隔
root='D:\\2pi'

#记录root目录下所有xml文件和jpg文件路径信息
xml=list(pathlib.Path(root).glob('**\\*.xml'))
img=list(pathlib.Path(root).glob('**\\*.jpg'))#如果是其他图片格式，需修改
xml={op.splitext(op.basename(x))[0]:str(x) for x in xml}
img={op.splitext(op.basename(i))[0]:str(i) for i in img}
#创建文件夹
path=op.join(root,'left')#修改文件夹名称
if not op.exists(path):
    os.mkdir(path)

#对比移动
func(xml,img)#xml剪切到图片目录下，不用需注释
#func(img,xml)#图片剪切到xml目录下，不用需注释

time_end=time.time()
print('totally cost:',time_end-time_start)