# -*- coding: utf-8 -*-
#!/usr/bin/env python

# MonoSLAM Project


import sys


sys.path.append('Params')               # connecting the directory containing Parameters.py
sys.path.append('Tools')  

import numpy as np
import math
from scipy.spatial import distance
import time
import datetime

import transformations as trnsfrm

from OpticalFlow import OpticalFlow
from ReadData import ReadData
from Localization import Localization
from XYZFeatures import XYZFeatures
from Triangulation import Triangulation
import Parameters as param
import Visualizations as VR

"""
__author__ = "Agniv Sen"
__copyright__ = "Copyright 2015, MonoSLAM Project"
__credits__ = []
__license__ = "GNU GPL"
__version__ = "0.0.1"
__maintainer__ = "Agniv Sen"
__email__ = "i.agniva@gmail.com"
__status__ = "Protoyping"

"""



# ****************************************************
# This is the entry point of this entire project. 
# For someone who wants to understand the code flow, please start from this point
# ****************************************************


rd = ReadData();    #Initializing File Reader Class



featureMap = np.zeros((param.MAX_OBSERVATION, param.MAX_FEATURES,2))
featureMapProj = np.zeros((param.MAX_OBSERVATION, param.MAX_FEATURES,param.PARTICLE_COUNT,3))
featureStore = np.zeros((param.FEATURE_SIZE))
world = np.zeros((param.WORLD_SCALE_X, param.WORLD_SCALE_Y, param.WORLD_SCALE_Z));

stateVectorSize = (param.POSITION_VECTOR_SIZE + param.QUATERNION_SIZE + param.TRANSLATIONAL_VELOCITY_VECTOR_SIZE + param.ANGULAR_VELOCITY_VECTOR_SIZE)
cameraState = np.zeros((stateVectorSize))

# Variables for archiving position vector, quaternion and features
_x = []
_y = []
_z = []
_xq = []
_yq = []
_zq = []
_w = []
_fx = []
_fy = []
_fz = []
_c = []
_xMap = []
_yMap = []
_zMap = []
#the preceding variables are there for maintaining history and visual representation only

if (param.DEBUG==1):
    ts = time.time()
    print "System started at {}" .format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    

for i in range(param.GT_START_INDEX,param.GT_END_INDEX):  # !...to replace this loop by something else in an online system...!
    
    imageName1 = rd.readFrameStatic(i,param.PATH)
    imageName2 = rd.readFrameStatic(i+1,param.PATH)
    IMG1 = param.PATH + imageName1
    IMG2 = param.PATH + imageName2
    
        
    OptFlow = OpticalFlow(IMG1,IMG2,0)
    
    features = OptFlow.computeFlow(param.FEATURE_SIZE)              #Features of IMG1
    prevFeatures= OptFlow.prevFeatures                              #Features of IMG2
    
    featureSize = len(features)
    prevFeatureSize = len(prevFeatures)
    
    if(featureSize == prevFeatureSize):
        count = 0
        for featureIndex in range(0,param.FEATURE_SIZE):                       #Iterating through the entire set of images
            
            flag = 0
            
            """
            Creating a datastructure featureMap, which is a 3D array storing the feature points of the entire session
            """
            
            for arrayCount in range(0, param.MAX_FEATURES-1):   
                
                firstPt = (featureMap[i][arrayCount][0],featureMap[i][arrayCount][1])
                secondPt = (features[featureIndex][0],features[featureIndex][1])
                
                #if (int(featureMap[i][arrayCount][0]) == int(features[featureIndex][0])) and (int(featureMap[i][arrayCount][1]) == int(features[featureIndex][1])):
                if (distance.euclidean(firstPt,secondPt) < param.MIN_FEATURE_DISTANCE):
                       featureMap[i+1][arrayCount][0] = prevFeatures[featureIndex][0]
                       featureMap[i+1][arrayCount][1] = prevFeatures[featureIndex][1]
                       flag = 1
                       
                       
                elif ((featureMap[i][arrayCount][0] == 0) and (featureMap[i][arrayCount][1] == 0)) and ((featureMap[i][arrayCount-1][0] != 0) or (featureMap[i][arrayCount-1][1] != 0)):
                       count=arrayCount
                        
                                    
            if(flag==0):
                featureMap[i+1][count][0] = prevFeatures[featureIndex][0]
                featureMap[i+1][count][1] = prevFeatures[featureIndex][1]
                
                featureMap[i][count][0] = features[featureIndex][0]
                featureMap[i][count][1] = features[featureIndex][1]
                count += 1
                
            
        if ((param.IS_INVERSE_DEPTH_PARAMETRIZATION == 0) and (param.IS_LOCALIZATION_FROM_GT == 1)):           # Only XYZ representation available in the first iteration
            
            l = Localization("")
            #tx, ty, tz, qx, qy, qz, qw, fBlock, sBlock = l.staticLocalizationFrmGT(param.GROUND_TRUTH_FILE,'',0)
            
            _tx, _ty, _tz, _qx, _qy, _qz, _qw, size = l.getDataBetweenImagesGT(imageName1, imageName2, param.GROUND_TRUTH_FILE)
            
            _w.append(_w)
            
            if (param.DEBUG==1):  
                print "Size of interim quaternions {}" .format(size)
            
            for q in range(0,size):
                #if (param.DEBUG==1):
                    #print "GT tuple : {},{},{},{},{},{}, {}" .format(_tx[q], _ty[q], _tz[q], _qx[q], _qy[q], _qz[q], _qw[q])
                    
                if (q==0) and (i==0):
                     cameraState[3] = float(_qw[q])
                     cameraState[4] = float(_qx[q])
                     cameraState[5] = float(_qy[q])
                     cameraState[6] = float(_qz[q])
                     
                elif (q > 0):
                     #quaternion = trnsfrm.quaternion_multiply([float(_qw[q]), float(_qx[q]), float(_qy[q]), float(_qz[q])],[cameraState[3],cameraState[4],cameraState[5],cameraState[6]])
                     cameraState[3] = float(_qw[q])#quaternion[0]
                     cameraState[4] = float(_qx[q])#quaternion[1]
                     cameraState[5] = float(_qy[q])#quaternion[2]
                     cameraState[6] = float(_qz[q])#quaternion[3]
                
                if (param.DEBUG==1):                   
                     M = trnsfrm.quaternion_matrix([cameraState[3],cameraState[4],cameraState[5],cameraState[6]])
                     #print M
                     
            cameraState[0] = float(_tx[0])
            cameraState[1] = float(_ty[0])
            cameraState[2] = float(_tz[0])
            
              
            print "Current Position : {}" .format(i)
                
            _x.append(cameraState[0])
            _y.append(cameraState[1])
            _z.append(cameraState[2])
        
        
            eulerAngle = trnsfrm.euler_from_quaternion([cameraState[3],cameraState[4],cameraState[5],cameraState[6]])
            _xq.append(math.radians(eulerAngle[0]))       #Storing euler angles for maintaining history and visualizations
            _yq.append(math.radians(eulerAngle[1]))
            _zq.append(math.radians(eulerAngle[2]))
            
            if (param.PARTICLE_FILTER == 1):
                xyz = XYZFeatures()
                fx,fy,fz = xyz.projectXYZFeatures(features, eulerAngle, cameraState)
                
                
                """  This is the triangulation block for the generated 'particles'. The efficacy of this part of the code is highly suspicious!  """
                

                triangle = Triangulation()
                _xMap, _yMap, _zMap, featureMapProj = triangle.filterPosition(features, featureMap, featureMapProj, _xMap, _yMap, _zMap, i+1, fx, fy, fz)
                
                
                """ Triangulation block ends  """
                        
                for feat in range(0,len(fx)):       
                    _fx.append(fx[feat])
                    _fy.append(fy[feat])
                    _fz.append(fz[feat])
                    _c.append(1/(i+1))

                
                

if (param.DEBUG==0):
    text_file = open(param._2D_FEATURE_DUMP_PATH, "a")
    text_file.write("\n\n")
             
    for i in range (param.GT_START_INDEX,param.GT_END_INDEX):
        for j in range (0,param.MAX_FEATURES):
            text_file.write("%d,%d,," % (featureMap[i][j][0],featureMap[i][j][1]))      
            
        text_file.write("\n")
        
    text_file.close()

if (param.VR == 1):
    VR.plotPosition(_x,_y,_z)
    VR.plotFeaturesBlue(_xMap,_yMap,_zMap)
    VR.plotVector(_x,_y,_z,_xq,_yq,_zq)   
    
    #VR.plotFeatures(_fx,_fy,_fz,_c)     