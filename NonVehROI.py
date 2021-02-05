# -*- coding: UTF-8 -*-
'''
@File    :   choice_data.py
@IDE    ：PyCharm
@Author ：XieXu
@Date   ：2020/12/4 10:28
'''

import numpy as np
import sys, os
import glob

caffe_root = '/home/manzp/caffe-ssd-quant/'
sys.path.insert(0, caffe_root + 'python')
import caffe
import cv2
import sys
import random


'''
调用方式: python choice_data.py ./testpic/ ./save/ 0.1
参数1： jpg 文件夹路径
参数2： 保存文件夹路径
参数3： 检测为目标的阈值，推荐为 0.1

*********************** 注意 ***********************

1.CAFFE 路径切换为自己本地版本
'''

net_file = 'deploy_res18_fpn_ori.prototxt'
caffe_model = 'ssd_res18_fpn_iter_180000_ori.caffemodel'

# test_dir = sys.argv[1]
# save_path = sys.argv[2]
# threshold = sys.argv[3]

test_dir = r'/mnt57/Distribute/DATA-distribute2/ywh/1205426/12.17'  # 图片路径
save_path = test_dir + '_output'  # 输出路径
threshold = 0.1  # 检测为目标的阈值  推荐为 0.1


if not os.path.exists(test_dir):
   print("{} is not exists !!!".format(test_dir))
if not os.path.exists(save_path):
    os.makedirs(save_path)

caffe.set_device(1)  # 使用gpu号
caffe.set_mode_gpu()

if not os.path.exists(caffe_model):
    print(caffe_model + " does not exist")
    exit()
if not os.path.exists(net_file):
    print(net_file + " does not exist")
    exit()
net = caffe.Net(net_file, caffe_model, caffe.TEST)

CLASSES = ('background', 'car', 'human', 'bicycle', 'electrotricycle', 'MASK')


def preprocess(src):
    img = cv2.resize(src, (512, 512))
    img = img - 127.5
    img = img / 127.5
    return img


def postprocess(img, out):
    h = img.shape[0]
    w = img.shape[1]
    box = out['detection_out'][0, 0, :, 3:7] * np.array([w, h, w, h])

    cls = out['detection_out'][0, 0, :, 1]
    conf = out['detection_out'][0, 0, :, 2]
    return (box.astype(np.int32), conf, cls)

obj_cnt = 0
def detect(imgfile):
    origimg = cv2.imread(imgfile)
    basename = os.path.basename(imgfile)
    h_ori = origimg.shape[0]
    h, w, c = origimg.shape
    img = preprocess(origimg)

    img = img.astype(np.float32)
    img = img.transpose((2, 0, 1))

    net.blobs['data'].data[...] = img
    out = net.forward()

    box, conf, cls = postprocess(origimg, out)
    for i in range(len(box)):
        x_r = random.randint(0,20)
        y_r = random.randint(0,20)
        xmin = box[i][0]-x_r
        ymin = box[i][1]-y_r
        xmax = box[i][2]+x_r
        ymax = box[i][3]+y_r
        if xmin < 0:
            xmin = 0
        if ymin < 0:
            ymin = 0
        if xmax > w:
            xmax = w
        if ymax > h:
            ymax = h
        if int(cls[i]) == 3:
            # if True:
            if conf[i] > float(threshold):
                global obj_cnt
                crop_img = origimg[ymin:ymax, xmin:xmax, :]
                ch, cw, cc = crop_img.shape
                if ch < 100 or cw < 100:
                    continue
                if ymax < int(h / 2):
                    continue
                cv2.imwrite(save_path + '/' + str(obj_cnt)+'.jpg', crop_img)
                obj_cnt += 1



cnt = 0
for root, dirs, files in os.walk(test_dir):
    for file in files:
        img = os.path.join(root, file)
        try:
            detect(img)
            cnt += 1
            if cnt % 1 == 0:
                print("processing {} image save {} image...".format(cnt,obj_cnt))
        except:
            print("Error img path {} !!".format(img))
            continue
# img_list = glob.glob(test_dir + "/*.jpg")
# cnt = 0
# for img in img_list:
#     try:
#         detect(img)
#         cnt += 1
#         if cnt % 1 == 0:
#             print("processing {} image save {} image...".format(cnt,obj_cnt))
#     except:
#         print("Error img path {} !!".format(img))
#         continue