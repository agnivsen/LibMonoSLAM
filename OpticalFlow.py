# -*- coding: utf-8 -*-

"""
Implements Corner Detection and Optical Flow tracking using LK method.
All image processing uses OpenCV

"""

import cv2
#import cv
import numpy as np
from matplotlib import pyplot as plt

class OpticalFlow:

    firstImage = "";
    secondImage = "";
    uiStatus = 0;
    prevFeatures = np.zeros((10,2));

    def __init__(self, firstImage, secondImage, uiStatus):
        print firstImage
        self.firstImage = firstImage;
        self.secondImage = secondImage;
        self.uiStatus = uiStatus
    
    def computeFlow(self, featureSize):     #compute the flow between firstImage and secondImage, based on features detected in the first image using Shi-Tomasi feature detector
                            
        # Parameters for lucas kanade optical flow
        lk_params = dict( winSize  = (15,15),
                          maxLevel = 2,
                          criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
                          
        # Create some random colors
        color = np.random.randint(0,255,(100,3))
        
                            
        
        #img = cv2.imread('D:\\Documents\\Data\\MonoSlam\\TranslationalData\\TestStereo\\1305031108.611407.png')
        img = cv2.imread(self.firstImage)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        corners = cv2.goodFeaturesToTrack(gray,featureSize,0.01,10)
        
        
        # Create a mask image for drawing purposes
        mask = np.zeros_like(img)
        
        #new_img = cv2.imread('D:\\Documents\\Data\\MonoSlam\\TranslationalData\\TestStereo\\1305031108.643303.png')
        new_img = cv2.imread(self.secondImage)
        new_gray = cv2.cvtColor(new_img,cv2.COLOR_BGR2GRAY)
        
        #calculate the optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(gray, new_gray, corners, None, **lk_params)
        
        # Select good points
        good_new = p1[st==1]
        good_old = corners[st==1]
            
            
        counter = 0
        #print "{"
        
        features = [[0]*10 for i in range(10)]
        
         # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            counter+=1
            a,b = new.ravel()
            c,d = old.ravel()
            #print "{ %d, %d}," % (c,  d)
            #print "{ %d, %d},\n" % (a, b)
            features[i][0] = a
            features[i][1] = b
            self.prevFeatures[i][0] = c
            self.prevFeatures[i][1] = d
            cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            cv2.circle(new_img,(a,b),5,color[i].tolist(),-1)
        final = cv2.add(new_img,mask)
        #print "}\n\n"
        
        if(self.uiStatus > 0):
            cv2.imshow('frame',final)
            k = cv2.waitKey(30)
            
        return features
        





