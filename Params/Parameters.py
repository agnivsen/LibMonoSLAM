# -*- coding: utf-8 -*-

PATH = r"D:\\Documents\\Data\\MSL\\FRBG3_1\\rgbd_dataset_freiburg3_long_office_household\\rgb\\"   #Path where the RGB files are stored
_2D_FEATURE_DUMP_PATH = "D:\\Documents\\CasualDocs\\MSL_Results\\Output.csv"               #Path to dump feature vectors

GROUND_TRUTH_FILE = r"D:\\Documents\\Data\MSL\\FRBG3_1\\rgbd_dataset_freiburg3_long_office_household\\groundtruth.txt" #Ground truth file for the camera position, as given in the computer vision dataset from Technische Universität München
""" Check: http://vision.in.tum.de/data/datasets/rgbd-dataset/download# 
    for more details  """
""" For the first iteration, the camera position is being read from a ground truth file (which has been obtained by externally tracking the camera).
    This saves us the necessity of implementing the Extended Kalman Filter at the very onset.
    We use this as an oppurtunity to build and debug our test environment, as well as coding the module for initializing depth vectors from features.
    Please check documentation for "Iteration-1", for more details regarding this approach"""    


DEBUG = 0                                       # enable/disable debug dumps. 1 turns it on, 0 switches it off
VR = 1                                         # Enable/disable visual representation OR graphs
IS_INVERSE_DEPTH_PARAMETRIZATION = 0            # assign 1 to this variavle if using Inverse Depth Parameterization, assign 0 is using XYZ representation
IS_LOCALIZATION_FROM_GT = 1                     # assign 1 to indicate that the current position of camera is being read from Groundtruth file (and not using SFM/homography estimation)
GT_DATA_SIZE = 5000                             # Number of entries in position GT file

PARTICLE_FILTER = 1                             #Enables feature depth mapping using particle filtering
PARTICLE_INIT_DEPTH = 0.5                       # Depth at which the depth-particles would be initiated from
PARTICLE_COUNT = 100                            # Number of depth-particles
PARTICLE_INTERVAL = 0.045                       # Seperation at which the depth-particles are intialized
""" Check https://www.doc.ic.ac.uk/~ajd/Publications/civera_etal_tro2008.pdf for more details on Inverse Depth Parametrization for Monocular SLAM """

GT_START_INDEX = 0                              # Line number of ground truth file at which we should start reading the position from
GT_END_INDEX = 400#GT_DATA_SIZE                     # Line number of ground truth file at which we should end reading the position
GT_HEADER_END_LINE = 3                          # Line number at which the ground truth file's header information ends


FEATURE_SIZE = 10                                   # Number of features to be extracted from each frame/image
MAX_OBSERVATION = GT_END_INDEX - GT_START_INDEX + 1 # Maximum number of frames/images/observations allowed in a single session
MAX_FEATURES = FEATURE_SIZE * MAX_OBSERVATION       # Maximum possible number of feature points extracted in one session

MIN_FEATURE_DISTANCE = 2                        # Minimum Eucledian distance between two consecutive feature positions on image plane (pixel coordinates), as obtained from Shi-Tomasi feature detector

WORLD_SCALE_X = 100                            # Scale of the entire map along X - axis
WORLD_SCALE_Y = 100                            # Scale of the entire map along Y - axis
WORLD_SCALE_Z = 100                            # Scale of the entire map along Z - axis


""" ****CAMERA STATE SPACE REPRESENTATION**** """
POSITION_VECTOR_SIZE = 3                        # Defining the size of the vector representing the position of the camera
QUATERNION_SIZE = 4                             # Defining the size of the unit quaternion representing the current orientation of the camera
TRANSLATIONAL_VELOCITY_VECTOR_SIZE = 3          # Defining the size of the vector representing the instantenous translational velocity of the camera
ANGULAR_VELOCITY_VECTOR_SIZE = 3                # Defining the size of the vector representing the instantenous angular velocity of the camera



""" **********CAMERA INTRINSIC PARAMETER************ """
""" Intrinsic parameter for RGB-D SLAM dataset of Technische Universität München, camera: Freiburg 1"""
""" For additional details, please refer: http://vision.in.tum.de/data/datasets/rgbd-dataset/file_formats#intrinsic_camera_calibration_of_the_kinect"""
"""
#   ***Parameters for FRBG 1***
Fu = 517.3
Fv = 516.5
Cu = 318.6
Cv = 255.3

d0 = 0.2624
d1 = -0.9531
d2 = -0.0054
d3 = 0.0026
d4 = 1.1633
"""

#   ***Parameters for FRBG 3***
Fu = 535.4
Fv = 539.2
Cu = 320.1
Cv = 247.6

d0 = 0
d1 = 0
d2 = 0
d3 = 0
d4 = 0
