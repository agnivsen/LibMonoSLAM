# LibMonoSLAM

## Introduction:

This project aims to implement SLAM using the input from a single Monocular camera. 

There are plenty of different algorithms for MonoSLAM. The basic framework for this particular implementation is inspired by [MonoSLAM: Real-Time Single Camera SLAM](http://www.robots.ox.ac.uk/~lav/Papers/davison_etal_pami2007/davison_etal_pami2007.pdf). However, this is not an exact replica of the framework proposed in that research work.

###### Current status: 

Only the particle filtering has been implemented as of now (reading pose estimates from GT)

******

## How to run this code:

### Environment Setup:

#### You are going to need - 

1. Python 2.7.9 
2. Some IDE for Python, preferably [Spyder IDE](https://pythonhosted.org/spyder/). 
  In Windows environment, Spyder is already included in [WinPython](https://winpython.github.io/)
  For Mac and Linux, please consult the documentation
3. OpenCV needs to be installed and linked with Python in your system. Here are some useful links for that:

* [OpenCV-Python interface in Windows](http://opencvpython.blogspot.sg/2012/05/install-opencv-in-windows-for-python.html)
* [Setting up OpenCV with Python support in Mac OSX](https://jjyap.wordpress.com/2014/05/24/installing-opencv-2-4-9-on-mac-osx-with-python-support/)
* [OpenCV installation for Python in Ubuntu](https://www.raben.com/content/opencv-installation-ubuntu-1204)
* [Python bindings for OpenCV in Debian](https://packages.debian.org/wheezy/python/python-opencv)


#### How to run - 

Download the code and open it up in Spyder (or anything else). Fire up the *Driver.py* module.




******

* To report any issues or bugs in the code, please use the [Bug Tracker Form](https://docs.google.com/forms/d/1SGzC2KDswoRyXoLRjfdaEvnfytM6mSNvjWx5rJ86UGg/viewform?usp=send_form) form.  

* To view existing bugs, please check the [Bug Tracker](https://docs.google.com/spreadsheets/d/1vhENzZWOP2QLKMHWm5zqbSzBfq6mTCorqYr-PZuy8W4/edit?usp=sharing)


******

## Dataset

This application is based on an extensive, offline dataset, created and maintained by [Technische Universität München (TUM)](https://www.tum.de/). The dataset contains hours of video captured by a depth-mapping camera. The dataset provides us with image sequence, as well as depth maps and unit quaternions describing the position and orientation of the camera w.r.t the world coordinates. 

[Link to RGB-D SLAM dataset.](http://vision.in.tum.de/data/datasets/rgbd-dataset/download#)

[Detailed description of the dataset is available here.] (http://ais.informatik.uni-freiburg.de/publications/papers/sturm12iros.pdf)

Here, we use the image sequence to perform offline MonoSLAM and use the depth map + unit quaternion as ground truth for validating our algorithm.

We use the *Sequence 'freiburg3_long_office_household' dataset*, which has been captured using an Asus Xtion motion sensor.

### How to link the dataset with the source code:

After downloading the Sequence 'freiburg3_long_office_household' dataset from TUM's website, the following changes must be done to the source code:

* Open the Parameters.py file and set the value of the *PATH* variable to the folder containing the RGB images from the TUM dataset

* In the same Parameters.py file, set the *GROUND_TRUTH_FILE* variable to the text file containing the ground truth trajectory (this is required, as of now, since the SFM module have not been implemented yet)




