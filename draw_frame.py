import os
import cv2 
from collections import Iterable

########################################
#       检测字符串中含有的汉字个数函数    #
########################################
def check_chinese_count(args):
    count=0
    if not isinstance(args,Iterable):
        return 0
    for word in args:
        if '\u4e00' <= word <= '\u9fff': 
            count+=1
    return count
##############################################
#             cmd显示输出设置                 #
##############################################
def cmd_show(show_args,show_args_tag,chinese_count=0,show_first_line=False,show_last_line=False,set_tag_long=80):
    if show_first_line==True:
        print('+%s+'%('-'*set_tag_long))
    type_len=len(show_args_tag)+len(str(show_args))
    should_space_half_len=(set_tag_long-type_len)//2
    last_space=set_tag_long-type_len-should_space_half_len-chinese_count-check_chinese_count(show_args)
    print('|%s%s%s%s|'%(' '*should_space_half_len,show_args_tag,show_args,' '*last_space))
    if show_last_line==True:
        print('+%s+'%('-'*set_tag_long))

####################################################################################
#      读取文件夹内视频文件，并设置间隔截取视频内的图片保存到指定文件夹下面              #
####################################################################################
def read_video_imformation(video_path,save_pic_path,save_log_txt,a_few_pictures_per_second=1,time_frame=25):  
    tuple=os.walk(video_path)
    COUNT_TIME=0
    frame=0
    failed_list=[]
    
    for folder_path_tuple,folder_name_tuple,file_name_tuple in tuple:
        for file_name in file_name_tuple:
            f=open(save_log_txt,'a')
            COUNT_TIME+=1
            ################################################
            #   此处是跳过之前已经处理好的视频                #
            ################################################
            # if COUNT_TIME<=49:                           #
                # print('跳过第 %s 个视频'%COUNT_TIME)      #
                # continue                                 #
            ################################################
            COUNT_PAGE=0
            file_name_no_suffix=os.path.splitext(file_name)[0]
            file_path=os.path.join(folder_path_tuple,file_name)
            folder_path=file_path[:file_path.rfind('\\')]
            vc=cv2.VideoCapture(file_path)
            n_frames=int(vc.get(7))                   #视频总共帧数
            rate=vc.get(5)                            #帧速率

            cmd_show(rate,'the frame type:',0,True)

            if isinstance(rate,int)==False and isinstance(rate,float)==False:
                print(file_path,'视频帧率解码失败')
                failed_list.append(file_path)
                continue
            try:
                a_few_pictures_per_second_rate=int(rate/a_few_pictures_per_second)
            except:
                continue

            cmd_show(a_few_pictures_per_second_rate,'每隔n帧抽一张:',6)

            if rate==0:
                failed_list.append(file_path)
                continue
            shipinshichang=n_frames/rate #视频时间

            cmd_show(folder_path,'文件夹:',3)
            cmd_show(file_name,'文件名:',3)
            cmd_show(n_frames,'总帧数:',3)
            cmd_show(rate,'帧率:',2)
            cmd_show(shipinshichang,'视频时长:',4,show_last_line=True)         
            
            ret,frame_pic=vc.read()
            while ret:
                ret,frame_pic=vc.read()
                #######################################################
                #              抽帧间隔方式                            #
                #######################################################
                if frame%a_few_pictures_per_second_rate==0:   #使用时间#
                # if frame%1==0:                              #每帧都抽#
                # if frame%time_frame==0:                     #使用跳帧#
                #######################################################
                    COUNT_PAGE+=1
                    try:
                        total_cut_count=n_frames/a_few_pictures_per_second_rate
                    except:
                        total_cut_count=None
                    pic_name=file_name_no_suffix+'_'+str(COUNT_PAGE)+'.jpg'
                    pic=os.path.join(save_pic_path,pic_name)

                    try:
                        cv2.imencode('.jpg',frame_pic)[1].tofile(pic)
                    except:
                        try:
                            cv2.imwrite(pic,frame_pic)
                        except:
                            pass
                    print('第 %s 个视频第 %s/%s 张，图片名:%s'%(COUNT_TIME,COUNT_PAGE,int(total_cut_count),pic_name))
                    f.write('第 %s 个视频第 %s/%s 张，图片名:%s\n'%(COUNT_TIME,COUNT_PAGE,int(total_cut_count),pic_name))
                    #pic_list.append(frame_pic)
					#cv2.waitKey(10)           #时间延迟
                frame+=1
            vc.release()
    
    f.write('failed file : '%failed_list)
    print(failed_list)
    f.close()

if __name__=='__main__':
    ##########################################################################
    #                       需要手动修改参数                                  #
    ##########################################################################
    #    1.输入视频路径                                                       #
    #    2.输出图片路径                                                       #
    #    3.输出log文件记录路径                                                 #
    #    4.间隔帧率                                                           #
    #    5.一秒几张                                                           #
    shipin_path=r'D:\熊超\全息路网\video\res'                                                    #
    save_pic_path=r'D:\熊超\全息路网\video\res'                                              #
    save_log_txt=save_pic_path+r'\log.txt'                                   #
    time_frame=1                                                             #
    a_few_pictures_per_second=1                                               #
    ##########################################################################


    if os.path.exists(save_pic_path)==False:
        os.mkdir(save_pic_path)

    read_video_imformation(shipin_path,save_pic_path,save_log_txt,a_few_pictures_per_second,time_frame) #视频路径，保存图片路径，帧数间隔


	

	
	
	
	
	
	