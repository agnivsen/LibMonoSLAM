# -*- coding: utf-8 -*-
import math
import Parameters as param


class Localization:
    
    imageName = ''
    firstBlock = ''
    secondBlock = ''
    
    firstImageName = ''
    secondImageName = ''
    
    
    def __init__(self, imageName):
        """assign the image name for which the closest trajectory parameter is to be extracted from ground truth
        
        Keyword arguments:
        imageName -- the image name which needs to be assigned
        
        Example: l = Localization('1305031108.611407')
        """
        
        self.imageName = imageName;
        
    
    # And He said, "Thou shall not countenance the extended pain of the extended Kalman filter. Not as long as you seek refuge in my abode!"
    def staticLocalizationFrmGT(self, pathToGT, prevImageName, index):  
        """ parsing the (X,Y,Z) position and unit quaternion from ground truth file, provided in text format
    
        Keyword arguments:
        pathToGT -- Fully qualified path to the ground truth file (provided with the RGB-D dataset)
        prevImageName -- Leave it blank, i.e: ''
        index -- make it zero (0)
        
        Example: l.staticLocalizationFrmGT(r'D:\rgbd_dataset_freiburg1_xyz\groundtruth.txt','',0)
        """
    
        gtFile = open(pathToGT,'r')     #Open GT file in read-only mode
        
        minFirst = 10000
        minFirstVal = 0
         
        template = long(self.imageName.split('.')[index])
        if(index==1):
            template = (template - (template%100))/100
        
        for i in range(0,param.GT_HEADER_END_LINE):    #discard the first three line, header data
            gtFile.readline()
            
        for i in range(0,param.GT_DATA_SIZE):
            r = gtFile.readline()
            #print "val: " + r.split(' ')[0].split('.')[0] + "," + r.split(' ')[0].split('.')[1]
            firstBlock = long(r.split(' ')[0].split('.')[0])
            secondBlock = long(r.split(' ')[0].split('.')[1])
               
            if (index == 0):
                currentActive = firstBlock
                if (math.fabs(currentActive - template) < minFirst):
                    minFirst = math.fabs(currentActive - template)
                    minFirstVal = currentActive
                
            else:
                currentActive = secondBlock
                if (firstBlock == long(prevImageName)):
                    if (math.fabs(currentActive - template) < minFirst):
                        minFirst = math.fabs(currentActive - template) 
                        minFirstVal = currentActive
                        tx = float(r.split(' ')[1])     #assign the values of the XYZ position and unit quaternion sequentially
                        ty = float(r.split(' ')[2])
                        tz = float(r.split(' ')[3])
                        qx = float(r.split(' ')[4])
                        qy = float(r.split(' ')[5])
                        qz = float(r.split(' ')[6])
                        qw = float(r.split(' ')[7])     #no sanity-checking mechanism implemented. Therefore, error in data format will have disastrous consequences
                                    
             
        index+=1;
        
        
        if (index < 2):
            l = Localization(self.imageName)
            self.firstBlock = str(minFirstVal)
            return l.staticLocalizationFrmGT(pathToGT,str(minFirstVal),index)
        else:
            blck =  str(minFirstVal)
            if (len(blck) == 2):
                blck = "00" + blck
            elif (len(blck) == 3):
                blck = "0" + blck
                
            self.secondBlock = blck
            return tx, ty, tz, qx, qy, qz, qw, str(prevImageName), blck
            
            

        """#EXAMPLE:
        l = Localization('1305031108.611407')
        tx, ty, tz, qx, qy, qz, qw = l.staticLocalizationFrmGT(r'D:\Documents\Data\MonoSlam\TranslationalData\rgbd_dataset_freiburg1_xyz\groundtruth.txt','',0)
        print tx, ty, tz, qx, qy, qz, qw
        """     

    def getDataBetweenImagesGT(self, firstImage, secondImage, gtFilePath):
        """ parsing the (X,Y,Z) position and unit quaternion from ground truth file, for a range inbetween firstImage and secondImage
    
        Keyword arguments:
        firstImage: starting image name, will look for a timestamp closest to the image timestamp
        secondImage: ending image name
        gtFilePath: location of thes ground truth file
        """
         
        size = 0
        
        _tx = []
        _ty = []
        _tz = []
        _qx = []
        _qy = []
        _qz = []
        _qw = []
         
        firstImage = firstImage[:-4]
        secondImage =  secondImage[:-4]
         
        firstGT = ''
        secondGT = ''
         
        if (param.DEBUG==1):
             print firstImage, secondImage
             
        l = Localization(firstImage)
        tx, ty, tz, qx, qy, qz, qw, fBlock, sBlock = l.staticLocalizationFrmGT(gtFilePath,'',0)
        
        _tx.append(tx)
        _ty.append(ty)
        _tz.append(tz)
        _qx.append(qx)
        _qy.append(qy)
        _qz.append(qz)
        _qw.append(qw)
        
        firstGT = fBlock + '.' + sBlock
         
        l = Localization(secondImage)
        tx, ty, tz, qx, qy, qz, qw, fBlock, sBlock = l.staticLocalizationFrmGT(gtFilePath,'',0)
         
        secondGT = fBlock + '.' + sBlock
         
        if (param.DEBUG==1):
             print "First GT: {}, Second GT: {}" .format(firstGT, secondGT)
         
        
        gtFile = open(gtFilePath,'r')     #Open GT file in read-only mode
        
        for i in range(0,3):    #discard the first three line, header data
            gtFile.readline()
            
        blockIndicator = 0         # indicates a stage between firstGT and secondGT
        multipleBlocks = 0         # indicates firstGT has been encountered twice in the file
            
        for i in range(0,param.GT_DATA_SIZE):
             
             r = gtFile.readline()
             target = r.split(' ')[0].split('.')[0] + '.' + r.split(' ')[0].split('.')[1]
             
             
             if (target == firstGT) and (multipleBlocks == 0):
                 multipleBlocks = 1
                 blockIndicator = 1
             elif (target == firstGT) and (multipleBlocks == 1):
                 print "ERROR: Data Inconsistency in trajectory ground truth file. Multiple entries for same time stamp - firstGT."
                 multipleBlocks = 2
             elif (target == secondGT) and (blockIndicator == 1):
                 blockIndicator = 0
             elif (target == secondGT) and (blockIndicator == 0):
                 print "ERROR: Data Inconsistency in trajectory ground truth file. Multiple/incorrect entries for same time stamp - secondGT."
                 multipleBlocks = 2
              
             if (blockIndicator == 1) and (multipleBlocks == 1):
                 size += 1
                 _tx.append(r.split(' ')[1])
                 _ty.append(r.split(' ')[2])
                 _tz.append(r.split(' ')[3])
                 _qx.append(r.split(' ')[4])
                 _qy.append(r.split(' ')[5])
                 _qz.append(r.split(' ')[6])
                 _qw.append(r.split(' ')[7])
                     
        _tx.append(tx)
        _ty.append(ty)
        _tz.append(tz)
        _qx.append(qx)
        _qy.append(qy)
        _qz.append(qz)
        _qw.append(qw)
        
        size += 2       # for the starting and ending element
        
        return _tx, _ty, _tz, _qx, _qy, _qz, _qw, size        
