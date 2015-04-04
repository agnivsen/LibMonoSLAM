# -*- coding: utf-8 -*-
from OpticalFlow import OpticalFlow
from ReadData import ReadData
import numpy as np
import csv

# ****************************************************
"""
  
  The following terminology will be used throughout the code comments:
   Session: One single run of the code, from start to end. 

"""
# ****************************************************

PATH = r"D:\\Documents\\Data\\MonoSlam\\TranslationalData\\rgbd_dataset_freiburg1_xyz\\rgb\\"
_2D_FEATURE_DUMP_PATH = "D:\\Documents\\CasualDocs\\MonoSLAM_Results\\Output.csv"

FEATURE_SIZE = 10                               # Number of features to be extracted from each frame/image
MAX_OBSERVATION = 3600                          # Maximum number of frames/images/observations allowed in a single session
MAX_FEATURES = FEATURE_SIZE * MAX_OBSERVATION   # Maximum possible number of feature points extracted in one session


rd = ReadData();    #Initializing File Reader Class

# This is the entry point of this entire project. 
# For someone who wants to understand the code flow, please start fromt this point

featureMap = np.zeros((MAX_OBSERVATION, MAX_FEATURES,2))
featureStore = np.zeros((FEATURE_SIZE))

for i in range(0,790):
    
    IMG1 = PATH + rd.readFrameStatic(i,PATH)
    IMG2 = PATH + rd.readFrameStatic(i+1,PATH)
        
    OptFlow = OpticalFlow(IMG1,IMG2,0)
    
    features = OptFlow.computeFlow(FEATURE_SIZE)
    prevFeatures = OptFlow.prevFeatures
    
    featureSize = len(features)
    prevFeatureSize = len(prevFeatures)
    
    #print ((featureSize, prevFeatureSize))
    
    if(featureSize == prevFeatureSize):
        for featureIndex in range(0,FEATURE_SIZE):
            count = 0
            flag = 0
            
            for arrayCount in range(0, MAX_FEATURES-1):
                if (int(featureMap[i][arrayCount][0]) == int(prevFeatures[featureIndex][0])) and (int(featureMap[i][arrayCount][1]) == int(prevFeatures[featureIndex][1])):
                       featureMap[i+1][arrayCount][0] = int(features[featureIndex][0])
                       featureMap[i+1][arrayCount][1] = int(features[featureIndex][1])
                       flag = 1
                elif ((featureMap[i][arrayCount][0] == 0) and (featureMap[i][arrayCount][1] == 0)) and ((featureMap[i][arrayCount-1][0] != 0) or (featureMap[i][arrayCount-1][1] != 0)):
                       count=arrayCount
                        
            
                        
            if(flag==0):
                featureMap[i][count][0] = int(prevFeatures[featureIndex][0])
                featureMap[i][count][1] = int(prevFeatures[featureIndex][1])
                
                featureMap[i+1][count][0] = int(features[featureIndex][0])
                featureMap[i+1][count][1] = int(features[featureIndex][1])
                

text_file = open(_2D_FEATURE_DUMP_PATH, "w")
         
for i in range (0,790):
    for j in range (0,MAX_OBSERVATION-1):
        text_file.write("%f,%f,," % (featureMap[i][j][0],featureMap[i][j][1]))      
        
    text_file.write("\n")
    
text_file.close()



     

