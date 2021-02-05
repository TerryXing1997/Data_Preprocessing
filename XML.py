# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 14:34:13 2020

@author: Terry Xing
"""

"""
ET：ElementTree、Element
ElementTree：整个文档的交互
    tree = ET.parse('country_data.xml')将文件解析成树
    root = tree.getroot()用根节点解析
    root = ET.fromstring(text, parser=None)从字符串中解析
    root = ET.fromstringlist(sequence, parser=None)从字符串列表中解析
    
    tree.write('output.xml')生成文件
    indent(tree, space=" ", level=0)向子节点添加空格实现直观的缩进
    
Element：树中的节点
    Element.tag：标签名
    Element.attrib：属性字典
    Element.get('')：从属性字典中获取指定属性
    Element.text：读取文本字符串
    Element.iter('')：遍历所有子节点
    for child in root：迭代访问一级子节点
    root[0][1].text：索引访问嵌套子节点
    Element.findall('')：仅查找当前节点的直接子节点中带有指定标签的节点
    Element.find('')：找带有特定标签的第一个子节点
    
    Element.set('','')：方法添加和修改属性
    Element.append(Element)：添加新的子节点
    Element.remove(Element)：删除节点
    a=ET.Element('a')；b=ET.SubElement(a,'b')：创建子节点
    ET.dump(a)：接上，显示a节点
    
    ET.iselement(element)判断是否为节点
    
    
    
"""
import xml.etree.ElementTree as ET