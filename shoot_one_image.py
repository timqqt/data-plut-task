'''
Created on 05.11.2019

@author: Fanjie Kong

* shoot one image from a fixed position
Note: data/camera.fbx is required

'''
from scripting import *


# get a CityEngine instance
ce = CE()



'''
parse lines and look for id
prepare cam data in array
non-generic, works for specific fbx part only
'''
def parseLine(lines, id):
    data = False
    for line in lines:
        if line.find(id) >=0 :
            data = line.partition(id)[2]
            break
    if data:
        data = data[:len(data)-1] # strip \n
        data = data.split(",")        
    return data

'''
parse lines from fbx file that store cam data
'''
def parseFbxCam(filename):
    f=open(filename)
    lines = f.readlines()
    cnt = 0
    loc =  parseLine(lines, 'Property: "Lcl Translation", "Lcl Translation", "A+",')
    rot =  parseLine(lines, 'Property: "Lcl Rotation", "Lcl Rotation", "A+",')
    return [loc,rot]



'''
helper functions
'''
def setCamPosV(v, vec):
    v.setCameraPosition(vec[0], vec[1], vec[2])
    
def setCamRotV(v, vec):
    v.setCameraRotation(vec[0], vec[1], vec[2])



'''
sets camera on first CE viewport
'''
def setCamData(data):
    v = ce.getObjectsFrom(ce.get3DViews(), ce.isViewport)[0]
    setCamPosV(v, data[0])
    setCamRotV(v, data[1])
    return v





'''
master function
'''
def importFbxCamera(fbxfile):
   
    data = parseFbxCam(fbxfile)
    if(data[0] and data[1]) :
        data[0][0]='599487.6436767578'
        data[0][1] = '2500'
        data[0][2]= '-5340307.977809906'
        data[1][0] = data[1][1]='-90.00'
        v = setCamData(data)
        print "Camera set to "+str(data)
        return v
    else:
        print "No camera data found in file "+file

def exportImages(directory, v, Tag=""):
   path = directory + "\_" + Tag + "_RGB.png"
   v.snapshot(path)

def exportGroundtruths(directory, v, Tag=""):
   path = directory + "\_" + Tag + "_GT.png"
   v.snapshot(path)
   
if __name__ == '__main__':
    camfile = ce.toFSPath("data/camera.fbx")
    view = importFbxCamera(camfile)
    #exportImages(ce.toFSPath('images'), view, Tag='Vienna_5')
    # exportGroundtruths(ce.toFSPath('images'), view, Tag='Vienna_5')