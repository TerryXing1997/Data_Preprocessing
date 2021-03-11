# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:52:48 2021

@author: Administrator
"""
import pandas as pd
import xml.etree.ElementTree as ET
import os.path as op

def compare(string):
    global attr,EMdic,dt
    img,value=string.rsplit(' ',1)
    value=value.strip('\n')
    ls=img.rsplit('/',4)
    changjing=ls[1]
    tianqi=ls[2]
    ls[-1],n=ls[-1].rsplit('_',1)
    ls[-1]=ls[-1]+'.xml'
    n=n.split('.')[0]
    ls.remove('小图')
    t=0
    
    xml_path='/'.join(ls)
    tree=ET.parse(xml_path)
    root=tree.getroot()
    for i in root.iter('object'):
        if i[0].text=='none':
            if t==int(n):
                key=i.find(attr).text
                if key not in EMdic:
                    break
                elif EMdic[key]==int(value):
                    dt.loc[(changjing,tianqi,'right'),[key]]+=1
                else:
                    dt.loc[(changjing,tianqi,'wrong'),[key]]+=1
                dt.loc[(changjing,tianqi,'total'),[key]]+=1
                break
            t+=1
        
            
df=pd.read_excel('/tmp/实际分类Enum.xlsx')
attr='cheliangleixing'
tmp=df.loc[0:9,['EMVehType','enum']].to_numpy()
EMdic=dict(tmp)

ds=pd.DataFrame(index=pd.MultiIndex.from_product([["白天","夜晚"],["晴天","阴天","雨天","雪天"],
                                                  ["逆光","背光","未知"]]))
mulu=list(ds.index)
mulu=[''.join(i) for i in mulu]

dt=pd.DataFrame(0,columns=["汇总"]+list(EMdic.keys()),dtype=int,
                index=pd.MultiIndex.from_product([["车卡场景","普通场景"],mulu,
                                                  ['right','wrong','total','ER']]))

dh=pd.DataFrame(0,columns=dt.columns,dtype=int,
                index=pd.MultiIndex.from_product([["汇总"],[''],
                                                  ['right','wrong','total','ER']]))
    
dt=dh.append(dt)

count=0
path=op.join('/mnt57/TestSetNew/ID1215005/VehAttri',attr+'.txt')
with open(path,'r') as f:
    for line in f:
        try:
            compare(line)
            count+=1
            print('\r'+str(count),end='')
        except Exception as e:
            print(e)
            
di=[list(i) for i in dt.index]

for i in di:
    if i[2]=='right':
        for j in dt.columns:
            dt.loc[('汇总','','right'),[j]]+=dt.loc[tuple(i),[j]]

    elif i[2]=='wrong':
        for j in dt.columns:
            dt.loc[('汇总','','wrong'),[j]]+=dt.loc[tuple(i),[j]]

    elif i[2]=='total':
        for j in dt.columns:
            dt.loc[('汇总','','total'),[j]]+=dt.loc[tuple(i),[j]]
            
#pdb.set_trace()

for i in di:
    if i[2]!='ER':
        for j in dt.columns:
            dt.loc[tuple(i),['汇总']]+=int(dt.loc[tuple(i),[j]])

#pdb.set_trace()
      
for i in di:
    if i[2]=='ER':
        for j in dt.columns:
            if int(dt.loc[tuple(i[0:2]+['total']),[j]])!=0:
                dt.loc[tuple(i),[j]]=dt.loc[tuple(i[0:2]+['wrong']),[j]]/dt.loc[tuple(i[0:2]+['total']),[j]]

dt.to_excel('cheliangleixing.xlsx',sheet_name='车辆类型')
