# -*- coding: utf-8 -*-

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import Parameters as param


def plotPosition( x, y, z):
        """
        Simple 3D plot of the (x,y,z) coordinates.
        x, y, z needs to be an array
        """
        
        plt.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(x, y, z, label='parametric curve')
        ax.legend()
        plt.show()
        
def plotFeatures( x, y, z, color):
        """
        Simple 3D plot of the (x,y,z) coordinates.
        x, y, z needs to be an array
        """
        plt.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c=color, marker='o')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()
        
def plotFeaturesBlue( x, y, z):
        """
        Simple 3D plot of the (x,y,z) coordinates.
        x, y, z needs to be an array
        """
        plt.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c='r', marker='o')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()
        
def plotVector(x,y,z,u,v,w):
        """
        3D quiver plot.
        X, Y, Z: denotes the 3D position
        u, v, w: denotes roll, pitch and yaw of the vector
        """
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        
        if (param.DEBUG==1):
            print "Euler angles:  {} || {} || {}" .format(u,v,w)
       
        ax.quiver(x, y, z, u, v, w, arrow_length_ratio = 0.1, length = 0.1)
        
        plt.show()
        
        




