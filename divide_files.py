import os
import shutil

source_path = r'Z:\Distribute\DATA-distribute2\ywh\1205426\0125_\white'  # 需要被分成具体几份的路径
#save_path = source_path + '_r'  # 分出来输出的 路径
#if not os.path.exists(save_path):
#	os.mkdir(save_path)
FILE_COUNT = 0
FOLDER_COUNT = 0
bsize = 30000  # 一个文件夹放多少个文件
for file_name in os.listdir(source_path):
    if FILE_COUNT % bsize == 0:  # 
        FOLDER_COUNT += 1
    file_path = os.path.join(source_path, file_name)
    save_folder_path = os.path.join(source_path, str(FOLDER_COUNT))
    if not os.path.exists(save_folder_path):
        os.mkdir(save_folder_path)
    shutil.move(file_path, save_folder_path)
    print(FILE_COUNT, save_folder_path)
    FILE_COUNT += 1
    

    
