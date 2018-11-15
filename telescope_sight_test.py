# -*- coding:utf-8 -*-
import os
from PIL import Image
'''
   @author:xuliu
'''
def cut(id): #openimage
    name1 = old_image_path + id
    name2 = new_image_path +"cut_" + id[0:4]
    im =Image.open(name1)

    im_width = im.size[0]
    im_height = im.size[0]
    scale = 2

    dx = im_width/scale/2
    dy = im_height/scale/2
    vx = im_width/scale
    vy = im_height/scale
    x1 = 0
    y1 = 0
    x2 = vx
    y2 = vy
    # name3 = name2 + str(1) + ".jpg"
    # im2 = im.crop((100, 100, 100, 100))
    # im2.save(name3)
    while x2 <= im_width:
        while y2 <= im_height:
            name3 = name2 +'_x' + str(n) + '.jpg'
            im2 = im.crop((y1, x1, y2, x2))
            im2.save(name3)
            y1 = y1 + dy
            y2 = y1 + im_height/scale
            n = n + 1
        x1 = x1 + dx
        x2 = x1 + im_width/scale
        y1 = 0
        y2 = im_height/scale
    print "cut image numbers"
    return n-1


old_image_path = "/home/bidlc/image/"
new_image_path = "/home/bidlc/image_cut/"
mumimg = len(os.listdir(old_image_path))
img_Lists = os.listdir(old_image_path)




if __name__=="__main__":
    for findex in range(len(img_Lists)):
        id = img_Lists[findex]
        res = cut(id)
        print res
