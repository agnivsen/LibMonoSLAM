# -*- coding: utf-8 -*-

import Parameters as param
import numpy as np

class Triangulation:
    
    def __init__(self):
        0;
    
    def filterPosition(self, features, featureMap, featureMapProj, _xMap, _yMap, _zMap, index, fx, fy, fz):
        """ Finding the particle with least variation in 3D position. From a set of randomly initialized depth particle, this module finds the particle(s) which shows least variation in position, when viewed from different angles
    
        Keyword arguments:
        
        
        """
        vecCounter = 0
        #print "here"
        #print len(features)
        
        for p in range(0,len(features)):
            for q in range(0,param.MAX_FEATURES):
                if (int(features[p][0]) == featureMap[index][q][0]) and (int(features[p][1]) == featureMap[index][q][1]):
                    for r in range(0,len(fx)):
                        #print index,q,r,vecCounter
                        if ((vecCounter)%param.PARTICLE_COUNT == 0):
                            vecCounter = 0
                        featureMapProj[index][q][vecCounter][0] = fx[r]
                        featureMapProj[index][q][vecCounter][1] = fy[r]
                        featureMapProj[index][q][vecCounter][2] = fz[r]  
                        vecCounter += 1
                        #print "Feature: {},{},{}" .format(featureMapProj[index][q][vecCounter][0],featureMapProj[index][q][vecCounter][1],featureMapProj[index][q][vecCounter][2])
                        #print r
                        
                    currDepth = index
                    vecLength = 0
                    vecStart = 0
                    for s in range(0,param.MAX_OBSERVATION):
                        if(currDepth>0):
                            if(featureMapProj[currDepth][q][0][0] != 0) and (featureMapProj[currDepth][q][0][1] != 0) and (featureMapProj[currDepth][q][0][2] != 0):
                                vecLength += 1
                                vecStart = currDepth
                            currDepth -= 1
                    #print vecLength,vecStart
                    if (vecLength > 1):         #found feature points which have been continiously tracked for more than two frames
                        xFeat = []
                        yFeat = []
                        zFeat = []
                        
                        minSD = -1
                        minSDVal = 1000
                        
                        for u in range(0,param.PARTICLE_COUNT):
                            for t in range(vecStart,index):
                                if(featureMapProj[t][q][0][0] != 0) and (featureMapProj[t][q][0][1] != 0) and (featureMapProj[t][q][0][2] != 0):
                                    xFeat.append(featureMapProj[t][q][u][0])
                                    yFeat.append(featureMapProj[t][q][u][1])
                                    zFeat.append(featureMapProj[t][q][u][2])
                            x_sd = np.std(xFeat)
                            y_sd = np.std(yFeat)
                            z_sd = np.std(zFeat)
                            
                            totalSD = x_sd + y_sd + z_sd
                            
                            if(totalSD < minSDVal):
                                minSD = u
                                minSDVal = totalSD
                                
                        if(minSD != -1):
                            _xMap.append(featureMapProj[index][q][minSD][0])
                            _yMap.append(featureMapProj[index][q][minSD][1])
                            _zMap.append(featureMapProj[index][q][minSD][2])
                            
            
            
        return _xMap, _yMap, _zMap, featureMapProj
                                
                                
