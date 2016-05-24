# -*- coding: utf-8 -*-
""" @file bokeh_calculator.py
@brief ボケ画像の判定を行います。
@author KCCS Yuzo Otomo
@date 2016/05/09 Yuzo Otomo コメント追加 & UTF8に変更
"""
import numpy as np
import os
import skimage.exposure
from skimage.color import rgb2gray
import math

class BokehDetector:
    """ボケ画像の判定を行います。
    Attribute:
        bias :  ボケ判定の際のカットオフの値を決めます。 default 2.
    """
    #set init
    def __init__(self,bias=2.):
        #if calculate low scale
        self.bias = bias
    
    #img ... np.darray (color image)
    #det ... dlib.rectangle  (default : all)
    def getValue(self,img,det=None,power_of_two=True):
        """画像のボケ具合を測定します。
        Args:
            img:画像
            det:画像における範囲 default None
            power_of_two:画像を2の階上にし計算速度を速めます。
        Returns:
            ボケ具合の数値
        """
        #make cut image
        if det == None:
            cut_img = img
            nw = int(img.shape[1])/10
            nh = int(img.shape[0])/10
        else:
            dtop = 0 if det.top()<0 else det.top()
            dbot = img.shape[0] if det.bottom() > img.shape[0] else det.bottom()+1
            dlft = 0 if det.left()<0 else det.left()
            drgt = img.shape[1] if det.right() > img.shape[1] else det.right()+1
            
            cut_img = img[dtop:dbot,dlft:drgt,:]
            nw = (drgt-dlft)/10
            nh = (dbot-dtop)/10
        if power_of_two:
            tmp_w = cut_img.shape[1]
            tmp_h = cut_img.shape[0]
            
            for i in range(9):
                cut_h = tmp_h-2**(i-1)
                hi = i
                if tmp_h < 2**i:
                    break
            for i in range(9):
                cut_w = tmp_w-2**(i-1)
                wi = i
                if tmp_w < 2**i:
                    break
            cut_img = cut_img[math.ceil(cut_h/2.):math.ceil(-cut_h/2.),
                              math.ceil(cut_w/2.):math.ceil(-cut_w/2.)]
            nw = 2**wi / 6
            nh = 2**hi / 6

        #make gray "equalize histogram" image
        tmp_gray = rgb2gray(cut_img)
        #tmp_gray = skimage.exposure.equalize_hist(tmp_gray)
        #im_min = np.min(tmp_gray)
        #im_max = np.max(tmp_gray)
        #fft & make power
        ft = np.fft.fft2(tmp_gray)
        shift_ft = np.fft.fftshift(ft)
        Pow = np.log10(np.abs(shift_ft)**2) +self.bias
        Pow[Pow<0]=0
        Pow = Pow * 30
        Pow[Pow>255]=255
        
        nr = min(nw,nh)
        
        #calculate value
        ltarr = np.tril(Pow[  0:nr,  0:nr][::-1])[::-1]
        rtarr = np.tril(Pow[-nr:  ,  0:nr])
        lbarr = np.triu(Pow[  0:nr,-nr:  ])
        rbarr = np.triu(Pow[-nr:  ,-nr:  ][::-1])[::-1]
        num = nr*(nr+1)/2
        lt=np.sum(ltarr)/num
        rt=np.sum(rtarr)/num
        lb=np.sum(lbarr)/num
        rb=np.sum(rbarr)/num
        
        return lt+rt+lb+rb

if __name__ == "__main__":
    import skimage.io
    import dlib
    import pandas as pd
    import time
    result3 = pd.DataFrame()
    detector = dlib.get_frontal_face_detector()
    for i in range(1,910,1):
        
        #fname = sample_sep_video_dir+"frame"+str(i)+".jpg"
        fname ="C:\\Users\\130350183\\Desktop\\test\\P4210129\\"+str(i).zfill(6)+".png"
        fname ="C:\\Users\\130350183\\Desktop\\raw_movie\\P4210129\\frame"+str(i)+".jpg"
        if not os.path.isfile(fname):
            continue
        
        img = skimage.io.imread(fname)
        dets = detector(img,0)
        bd = BokehDetector()
        for j, d in enumerate(dets):
            start = time.time()
            result = bd.getValue(img,d)
            end = time.time()
            result3 = result3.append(pd.DataFrame({"num":result},index=[fname]))
            break
    result3.to_csv("res6_jpg.csv")