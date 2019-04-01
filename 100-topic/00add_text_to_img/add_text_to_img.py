# -*- coding: utf-8 -*-
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

'''
功能：图片右上角加数字
'''
# 打开底版图片
# image_file = "/Users/openerp/dev/python_practice/icons/folder-music-icon.png"
image_file = r"F:\dev\python_practice\icons\folder-music-icon.png"

im = Image.open(image_file)
# font = ImageFont.truetype('Arial/Arial.ttf', 300)
#  字体必须大于等于19才可以输出汉字

# 在图片上添加文字 1
draw = ImageDraw.Draw(im)
fontsize = min(im.size)/5
draw.text((im.size[1]-fontsize, 1), '4', fill=(255, 0, 0), font=None)
draw = ImageDraw.Draw(im)
# (im.size[1]-fontsize, 1)为添加文字的位置，'4'为显示的显示的字, fill=(255, 0, 0)为填充文字的颜色，
# font为文字的字体，font可以自定义,None为没有样式.
# 自定义方法为font = ImageFont.truetype ("Arial.ttf",16),16为字体大小

# 使用PIL库对图片进行操作:http://www.cnblogs.com/meitian/p/3699223.html

# 保存
# windows目录前加r或R，则字符串不会对\转议
# im.save("/Users/openerp/dev/python_practice/icons/folder-music-icon-1.png")
im.save(r"F:\dev\python_practice\icons\folder-music-icon-1.png")
