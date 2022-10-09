from cmath import sqrt
import math
import numpy
import boto3
from math import sqrt

#width = 0.0048
#height = 0.0036
#focal = 0.004

#width = 0.00766
#height = 0.00574
#focal = 0.0057

width = 0.004 #Width of camera (m)
height = 0.003 #Height of camera (m)
focal = 0.0016 #Focal length of camera (m)

d = .131 #Length of sides of square (m)


# Calculates the vector direction of the line based on screen positions
def calcLineVector(u,v):
    U = u*width
    V = v*height
    X=U/focal
    Y=V/focal
    Z=1
    Mag=sqrt((X*X)+(Y*Y)+(Z*Z))
    x=X/Mag
    y=Y/Mag
    z=Z/Mag
    return [x,y,z]

# Calculates the position on one line2 if given the distance from position on line1
def solveVar(v1, v2, t):
    a = 1
    b = - 2 * t * ( v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2] )
    c = (t*t)-(d*d)
    ins = (b**2 - 4*a*c)
    #print(b**2)
    #print(4*a*c)
    s=0
    if  (ins < 0):
        print("COMPLEX BELOW")

        s = (-b - (-ins)**(1/2))/(2*a)
    else:
        s = (-b - (ins)**(1/2))/(2*a)
    return s


# Determines the maximum distance that the shape could be
def maxDist(v1, v2):
    #a = (v2[0])**2 + (v2[1])**2 + (v2[2])**2
    #b = 2 * (v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2])
    #c =  (v1[0])**2 + (v1[1])**2 + (v1[2])**2
    #return ((-4*(d**2)*a)/((b**2)-(4*a*c)))**(1/2)
    c = (v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])/(v2[0]**2+v2[1]**2+v2[2]**2)
    print("START")
    broken = d/(((v1[0]-c*v2[0])**2+(v1[1]-c*v2[1])**2+(v1[2]-c*v2[2])**2)**(1/2))
    print(sqrt(1-(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])**2))
    new = (d/sqrt((1-(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])**2)))
    print(new)
    return new

#Calculates the locations of the coordinates in 3D space
def calcInt(one, two, three): 
    w1 = calcLineVector(one[0],one[1])
    w2 = calcLineVector(two[0],two[1])
    w3 = calcLineVector(three[0],three[1])
    


    print(w1)
    print(w2)
    print(w3)

    max1, max2 = maxDist(w1, w2), maxDist(w1,w3)
    #print(max1)
    #print(max2)
    ma = min(max1, max2)
    ma = ma
    mi = d

    error = 1

    tVal = 0
    s = 0
    r = 0

    for i in range(100):
        tVal = (ma + mi)/2
        s = solveVar(w1,w2,tVal)
        r = solveVar(w1,w3,tVal)
    
        #print("OUTPUTS")
        #print(((tVal*w1[0]-s*w2[0])**2 + (tVal*w1[1]-s*w2[1])**2 + (tVal*w1[2]-s*w2[2])**2 )**(1/2))
        #print(((tVal*w1[0]-r*w3[0])**2 + (tVal*w1[1]-r*w3[1])**2 + (tVal*w1[2]-r*w3[2])**2 )**(1/2))
        

        
        dist = ((s*w2[0]-r*w3[0])**2 + (s*w2[1]-r*w3[1])**2 + (s*w2[2]-r*w3[2])**2 )**(1/2)



        error = dist - ((2**(1/2))*d)
        

        if (error < 0):
            mi = tVal
        else:
            ma = tVal
        #print ((ma+ mi)/2)
    print((ma+mi)/2)
    return w1, w2, w3, tVal, s, r
    
        
#THIS IS FOR d=0.085

#vOne = [1988/4032-.5, 1565/3024-.5]
#vTwo = [2171/4032-.5, 1629/3024-.5]
#vThree = [1929/4032-.5, 1751/3024-.5]

#vOne = [2145/4032-.5, 1564/3024-.5]
#vTwo = [2262/4032-.5, 1632/3024-.5]
#vThree = [2080/4032-.5, 1678/3024-.5] 

#
#vOne = [2030/4032-.5, 1364/3024-.5]
#vTwo = [1977/4032-.5, 1403/3024-.5]
#vThree = [2077/4032-.5, 1411/3024-.5] 

#Like 4 meters
#vOne = [2117/4032-.5, 1334/3024-.5]
#vTwo = [2087/4032-.5, 1359/3024-.5]
#vThree = [2135/4032-.5, 1368/3024-.5] 

#d=0.1398
#vOne = [2045/4032-.5, 1690/3024-.5]
#vTwo = [1991/4032-.5, 1737/3024-.5]
#vThree = [2116/4032-.5, 1725/3024-.5]

#d=0.131
#Pixel data of our program
vOne = [2210/4032-.5, 1493/3024-.5]
vTwo = [2296/4032-.5, 1547/3024-.5]
vThree = [2137/4032-.5, 1548/3024-.5]




vec1, vec2, vec3, tV, sV, rV = calcInt(vOne, vTwo, vThree)

p1 = [tV*vec1[0],tV*vec1[1],tV*vec1[2]]
p2 = [sV*vec2[0],sV*vec2[1],sV*vec2[2]]
p3 = [rV*vec3[0],rV*vec3[1],rV*vec1[2]]

tvec1 = [p1[0]-p2[0],p1[1]-p2[1],p1[2]-p2[2]]
tvec2 = [p1[0]-p3[0],p1[1]-p3[1],p1[2]-p3[2]]


crossVec = numpy.cross(tvec2, tvec1)
if (crossVec[2] < 0):
    crossVec[0]=-crossVec[0]
    crossVec[1]=-crossVec[1]
    crossVec[2]=-crossVec[2]

crossMag = numpy.sqrt(crossVec.dot(crossVec))
heightVector = numpy.dot(p1, crossVec)/(crossMag**2) * crossVec

centerVec = (numpy.array(p2)+numpy.array(p3))/2
centerFlatVec = centerVec - heightVector


towMid = numpy.array(p1)-centerVec






theta = numpy.arccos((towMid.dot(centerFlatVec))/(numpy.sqrt(towMid.dot(towMid))*numpy.sqrt(centerFlatVec.dot(centerFlatVec))))

print("Height")
print(str(numpy.sqrt(heightVector.dot(heightVector)))+" m")

print("Distance")
print(str(numpy.sqrt(centerVec.dot(centerVec)))+" m")

print("Theta")
print(str(theta*180/math.pi+90)+"°")


phi = numpy.arcsin((numpy.sqrt(heightVector.dot(heightVector)))/(numpy.sqrt(centerVec.dot(centerVec))))

print("Phi")
print(str(phi*180/math.pi)+"°")

center = numpy.array([(p2[0]+p3[0])/2, (p2[1]+p3[1])/2, (p2[2]+p3[2])/2])



