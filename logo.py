
#功能：将车牌信息打印在图片左上角，用于全息路网测试结果的比对


from PIL import Image, ImageDraw, ImageFont
import os
# get an image

path='/mnt57/TestSetNew/ID1215005/res.txt'
dst='/mnt57/TestSetNew/ID1215005/jieguo'
count=0
with open(path,'r',encoding='gbk') as f:

    for line in f:
        img,value=line.split(' ')
        value=value.strip('\n')
        
        base = Image.open(img).convert("RGBA")
        
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", base.size, (255,255,255,0))
        
        # get a font
        fnt = ImageFont.truetype("simhei.ttf", 20, encoding='gbk')
        # get a drawing context
        d = ImageDraw.Draw(txt)
        
        d.text((10,4), value, font=fnt, fill=(255,0,0,255))
        
        out = Image.alpha_composite(base, txt)
        
        out = out.convert('RGB')
        
    #        if not os.path.exists('/mnt57/TestSetNew/ID1215005/jieguo'):
    #            os.mkdir('/mnt57/TestSetNew/ID1215005/jieguo')
        
        out.save(os.path.join(dst,os.path.basename(img)))
        count+=1
        print('\r'+str(count),end='')
    
    


