import numpy as np
import cv2
import pathlib
import os.path as op
# 转到RGB
image_height = 2160
image_width = 3840

def yuv_NV21_to_rgb8(yuv_path):
    global image_height,image_width
    path=str(yuv_path)
    write_name=op.splitext(path)[0]+'.bmp'
    with open(yuv_path, 'rb') as f:
        yuv = f.read()
    Y = []
    U = []
    V = []
    for i in range(image_height):
        for j in range(image_width):
            Y.append(yuv[i * image_width + j])
            V.append(yuv[(i // 2 + image_height) * image_width + (j // 2) * 2])
            U.append(yuv[(i // 2 + image_height) * image_width + (j // 2) * 2 + 1])

    mean_lum = np.mean(Y)
    print(mean_lum)

    R = []
    G = []
    B = []

    for i in range(image_height):
        for j in range(image_width):
            B.append(min(
                max(1.164383 * (Y[i * image_width + j] - 16.0) + 2.017230 * (U[i * image_width + j] - 128.0), 0),
                255))
            G.append(min(max(1.164383 * (Y[i * image_width + j] - 16.0) - 0.391762 * (
                        U[i * image_width + j] - 128.0) - 0.812969 * (V[i * image_width + j] - 128.0), 0), 255))
            R.append(min(
                max(1.164383 * (Y[i * image_width + j] - 16.0) + 1.596016 * (V[i * image_width + j] - 128.0), 0),
                255))

    R = np.array(R).reshape((image_height, image_width))
    G = np.array(G).reshape((image_height, image_width))
    B = np.array(B).reshape((image_height, image_width))
    try:
        image_opencv = cv2.merge([B, G, R])
        cv2.imwrite(write_name, image_opencv)
    except Exception:
        print(write_name)
count=0
root=r'/mnt57/Distribute/DATA-distribute2/ywh/1216612/20210202/训练集/scene1/1'
for y in pathlib.Path(root).glob('**/*.yuv'):
    yuv_NV21_to_rgb8(y)
    count+=1
print(count)
