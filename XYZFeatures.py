# -*- coding: utf-8 -*-

import numpy as np
import Parameters as param
import transformations as trnsfrm

class XYZFeatures:
    
    def __init__(self):
        0;
        
    def projectXYZFeatures(self, features, eulerAngle, cameraState):
        """ projecting the features from n-dimensional state to (n+1) dimensional state, i.e, 2D to 3D in this case
        Random particles are initiated along the line joining the camera optical center and the feature
    
        Keyword arguments:
        features - features detected from the current image
        eulerAngle - the Euler angles describing the current camera state
        cameraState - the quaternions describing the current camera state
        
        """
        
        _x = []
        _y = []
        _z = []
        
        
        origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)

        """
        Given:
        T_wo = [[R_wo,t_wo],[0T,1]] = [[R_owT, -(R_owT).t_ow],[0T,1]]
        
        We represent:
        
        A = R_owT
        B = -(R_owT).t_ow
        C = 0T
        
        """                
        rX = trnsfrm.rotation_matrix(eulerAngle[0],xaxis)              #Deriving the rotation matrices from Euler angles
        rY = trnsfrm.rotation_matrix(eulerAngle[1],yaxis)
        rZ = trnsfrm.rotation_matrix(eulerAngle[2],zaxis)
       
        R_ow = trnsfrm.concatenate_matrices(rX, rY, rZ)                #Combined rotational matrix
        R_ow = np.delete(R_ow, (3), axis=0)
        R_ow = np.delete(R_ow, (3), axis=1)
        
        t_ow = np.array([[cameraState[0],cameraState[1],cameraState[2]]])
        t_ow = np.transpose(t_ow)
        
        R_owT = np.transpose(R_ow)
        B = np.dot(-R_owT,t_ow)
        
        interim = np.hstack([R_owT,B])
        
        t_base = np.array([0,0,0,1])
        
        T_wo = np.vstack([interim,t_base])
        
        K = np.array([[1/param.Fu,0,(-param.Cu/param.Fu)],[0,1/param.Fv,(-param.Cv/param.Fv)],[0,0,1]]) #matrix for mapping points in image plane to real world, with origin in point of focus
        
        for i in range(0,len(features)):
            pix_c = np.array([[features[i][0]],[features[i][1]],[1]])           #pixel coordinates in image plane, distorted
            dist_c = np.dot(K,pix_c)                                            #real world X,Y coordinate + distorted ????
            
            
            
            """ The undistort step is being neglected for the moment, we are currently working with an already undistorted image database """   
            #To implement undistorion later, when required!
            

            depth = param.PARTICLE_INIT_DEPTH
            
            for looper in range(0,param.PARTICLE_COUNT):
                dist_c_depth = np.array([[dist_c[0]*depth],[dist_c[1]*depth],[depth],[1]])
                world_c = np.dot(T_wo,dist_c_depth)
                
                _x.append(world_c[0])
                _y.append(world_c[1])
                _z.append(world_c[2])
                
                depth += param.PARTICLE_INTERVAL
                
            
            #if (param.DEBUG==1):
                #print "Features in XYZ Projection: {},{}" .format(features[i][0],features[i][1])
        
        if (param.DEBUG==1): 
            print "Rotational Matrix ::"
            print R_ow
            
            print "Interim Matrix ::"
            print interim
            
            print "Transpose world w.r.t origin ::"
            print T_wo
            
        return _x,_y,_z
        
        
        """
        for i in range(0,len(features)):
            if (param.DEBUG==1):
                print features[i][0],features[i][1]
        """
