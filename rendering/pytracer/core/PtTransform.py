import PtCommon
import PtGeom

import math
import copy

class PtMatrix():
    def __init__(self,*args):
        if len(args) > 0 and type(args[0]) == list and len(args[0]) == 16:
            self.m = copy.copy(args[0])
        else:
            self.m = [1.,0.,0.,0.,
                      0.,1.,0.,0.,
                      0.,0.,1.,0.,
                      0.,0.,0.,1.]

    def fromList(self,lst):
        self.m = copy.copy(lst)
    
    @property
    def identity(self):
        for i in range(4):
            for j in range(4):
                if i == j:
                    self.m[i*4 + j] = 1.
                else:
                    self.m[i*4+j] = 0.
    @property
    def determinant(self):
        m = self.m
        c0 = m[0] * (m[10]*m[15]*m[5]-m[14]*m[11]*m[5] +
                           m[6]*m[15]*-m[9]-m[14]*m[7]*-m[9] + 
                           m[6]*m[11]*m[13]-m[10]*m[7]*m[13]);
        c1 =-m[4] * (m[10]*m[15]*m[1]-m[14]*m[11]*m[1] +
                           m[2]*m[15]*-m[9]-m[14]*m[3]*-m[9] +
                           m[2]*m[11]*m[13]-m[10]*m[3]*m[13]);
        c2 = m[8] * (m[6] *m[15]*m[1]-m[14]*m[7] *m[1] +
                           m[2]*m[15]*-m[5]-m[14]*m[3]*-m[5] +
                           m[2]*m[7] *m[13]-m[6] *m[3]*m[13]);
        c3 = -m[12]*(m[6] *m[11]*m[1]-m[10]*m[7] *m[1] +
                           m[2]*m[11]*-m[5]-m[10]*m[3]*-m[5] +
                           m[2]*m[7] *m[9] -m[6] *m[3]*m[9]);
        return c0 + c1 + c2 + c3;


    @property
    def transpose(self):
        m = self.m
        tmp = [0,0,0,0,
               0,0,0,0,
               0,0,0,0,
               0,0,0,0]
        tmp[0]=m[0];  tmp[1]=m[4];  tmp[2]=m[8];   tmp[3]=m[12];
        tmp[4]=m[1];  tmp[5]=m[5];  tmp[6]=m[9];   tmp[7]=m[13];
        tmp[8]=m[2];  tmp[9]=m[6];  tmp[10]=m[10]; tmp[11]=m[14];
        tmp[12]=m[3]; tmp[13]=m[7]; tmp[14]=m[11]; tmp[15]=m[15];
        self.m = tmp


    @property
    def invert(self):	
        d = copy.copy(self.m)
        m = self.m
        dtr = 1./self.determinant

        ## Row 1
        d[0] = (m[10]*m[15]*m[5] - m[11]*m[14]*m[5]  + 
                m[6] *m[15]*-m[9]- m[7] *m[14]*-m[9] + 
                m[6] *m[11]*m[13]- m[7] *m[10]*m[13])*dtr;
        d[1] = -1*(m[10]*m[15]*m[4] - m[11]*m[14]*m[4] +
                   m[6]*m[15]*-m[8] - m[7]*m[14]*-m[8] +
                   m[6]*m[11]*m[12] - m[7]*m[10]*m[12])*dtr;
        d[2] = (m[9]*m[15]*m[4] - m[11]*m[13]*m[4] +
                m[5]*m[15]*-m[8]- m[7]*m[13]*-m[8] +
                m[5]*m[11]*m[12]- m[7]*m[9]*m[12])*dtr;
        d[3] = -1*(m[9]*m[14]*m[4] - m[10]*m[13]*m[4] +
                   m[5]*m[14]*-m[8]- m[6]*m[13]*-m[8]  +
                   m[5]*m[10]*m[12]- m[6]*m[9]*m[12])*dtr;
        ## Row 2
        d[4] = -1*(m[10]*m[15]*m[1] - m[11]*m[14]*m[1] +
                   m[2]*m[15]*-m[9] - m[3]*m[14]*-m[9]  +
                   m[2]*m[11]*m[13] - m[3]*m[10]*m[13])*dtr;
        d[5] = (m[10]*m[15]*m[0] - m[11]*m[14]*m[0] +
                m[2]*m[15]*-m[8] - m[3]*m[14]*-m[8]  +
                m[2]*m[11]*m[12] - m[3]*m[10]*m[12])*dtr;
        d[6] = -1*(m[9]*m[15]*m[0] - m[11]*m[13]*m[0] +
                   m[1]*m[15]*-m[8]- m[3]*m[13]*-m[8] +
                   m[1]*m[11]*m[12]- m[3]*m[9]*m[12])*dtr;
        d[7] = (m[9]*m[14]*m[0] - m[10]*m[13]*m[0] +
                m[1]*m[14]*-m[8]- m[2]*m[13]*-m[8] +
                m[1]*m[10]*m[12]- m[2]*m[9]*m[12])*dtr;
        d[12] = -1*(m[6]*m[11]*m[1]- m[7]*m[10]*m[1] +
                   m[2]*m[11]*-m[5]- m[3]*m[10]*-m[5]+
                   m[2]*m[7]*m[9]  - m[3]*m[6]*m[9])*dtr;
        ## Row 3
        d[8] = (m[6]*m[15]*m[1]  - m[7]*m[14]*m[1]  + 
                m[2] *m[15]*-m[5]- m[3] *m[14]*-m[5]+ 
                m[2] *m[7]*m[13] - m[3] *m[6]*m[13])*dtr;
        d[9] = -1*(m[6]*m[15]*m[0] - m[7]*m[14]*m[0] +
                   m[2]*m[15]*-m[4]- m[3]*m[14]*-m[4]+
                   m[2]*m[7]*m[12] - m[3]*m[6]*m[12])*dtr;
        d[10] = (m[5]*m[15]*m[0]- m[7]*m[13]*m[0] +
                m[1]*m[15]*-m[4]- m[3]*m[13]*-m[4]+
                m[1]*m[7]*m[12] - m[3]*m[5]*m[12])*dtr;
        d[11] = -1*(m[5]*m[14]*m[0]- m[6]*m[13]*m[0] +
                   m[1]*m[14]*-m[4]- m[2]*m[13]*-m[4]+
                   m[1]*m[6]*m[12] - m[2]*m[5]*m[12])*dtr;
        ## Row 4
        d[12] = -1*(m[6]*m[11]*m[1] - m[7]*m[10]*m[1] +
                    m[2]*m[11]*-m[5]- m[3]*m[10]*-m[5]+
                    m[2]*m[7]*m[9]  - m[3]*m[6]*m[9])*dtr

        d[13] = (m[6]*m[11]*m[0]- m[7]*m[10]*m[0] +
                m[2]*m[11]*-m[4]- m[3]*m[10]*-m[4]+
                m[2]*m[7]*m[8]  - m[3]*m[6]*m[8])*dtr

        d[14] = -1*(m[5]*m[11]*m[0] - m[7]*m[9]*m[0] +
                    m[1]*m[11]*-m[4]- m[3]*m[9]*-m[4]+
                    m[1]*m[7]*m[8]  - m[3]*m[5]*m[8])*dtr

        d[15] = (m[5]*m[10]*m[0] - m[6]*m[9]*m[0] +
                 m[1]*m[10]*-m[4]- m[2]*m[9]*-m[4]+
                 m[1]*m[6]*m[8]  - m[2]*m[5]*m[8])*dtr

        dst = self.__class__()
        dst.fromList(d)
        dst.transpose
        self.m = copy.copy(dst.m)

    def __getitem__(self,key):
        return self.m[key]

    def __setitem__(self,key,value):
        self.m[key] = float(value)
	
    def __str__(self):
        stout = ""
        for i in range(4):
            stout += "%.10f %.10f %.10f %.10f\n" %(self.m[i*4],self.m[i*4+1],
                                                   self.m[i*4+2],self.m[i*4+3])
        return stout
	  
class PtTransform():
    def __init__(self,*args):
        if len(args) > 0 and args[0].__class__.__name__ == "PtMatrix":
            self.m = args[0] 
        else:
            self.m = PtMatrix()

        self.mInv = copy.copy(self.m)
        self.mInv.invert

def PiTranslate(*args):
    if len(args) > 0 and type(args[0]) == list:
        vec = args[0]
        x = float(vec[0])
        y = float(vec[1])
        z = float(vec[2])
    elif len(args) and args[0].__class__.__name__ == "PtVector":
        vec = args[0]
        x = vec.x
        y = vec.y
        z = vec.z;
    elif len(args) == 0:
        x = 0.
        y = 0.
        z = 0.
    else:  
        raise PtCommon.PtTypeError("PiTranslate requires a list or a PtVector")

    l = [1.,0.,0.,x,
         0.,1.,0.,y,
         0.,0.,1.,z,
         0.,0.,0.,1.]
    mat = PtMatrix(l)
    return PtTransform(mat)

def PiScale(*args):
    if len(args) > 0 and type(args[0]) == list:
        vec = args[0]
        x = float(vec[0])
        y = float(vec[1])
        z = float(vec[2])
    elif len(args) > 0 and args[0].__class__.__name__ == "PtVector":
        vec = args[0]
        x = vec.x
        y = vec.y
        z = vec.z;
    elif len(args) == 0:
        x = 1.
        y = 1.
        z = 1.
    else:
        raise PtCommon.PtTypeError("PiScale requires a list or a PtVector")

    m = PtMatrix([x,0.,0.,0.,
                  0.,y,0.,0.,
                  0.,0.,z,0.,
                  0.,0.,0.,1.])
    mi = PtMatrix([1./x,0.,0.,0.,
                  0.,1./y,0.,0.,
                  0.,0.,1./z,0.,
                  0.,0.,0.,1.])
    t = PtTransform()
    t.m = m
    t.mInv =mi
    return t


def PiRotateX(angle):
    sin_t = math.sin(float(angle))
    cos_t = math.cos(float(angle))
    rotl = [1.,0.,   0.,    0.,
            0.,cos_t,-sin_t,0.,
            0.,sin_t,cos_t ,0.,
            0.,0.,   0.,    1.]
    rotm = PtMatrix(rotl)
    return PtTransform(rotm)

def PiRotateY(angle):
    sin_t = math.sin(float(angle))
    cos_t = math.cos(float(angle))
    rotl = [cos_t, 0., sin_t,0.,
            0.,    1., 0     ,0.,
            -sin_t,0., cos_t, 0.,
            0.,    0., 0.,    1.]
    rotm = PtMatrix(rotl)
    return PtTransform(rotm)

def PiRotateZ(angle):
    sin_t = math.sin(float(angle))
    cos_t = math.cos(float(angle))
    rotl = [cos_t, -sin_t, 0., 0.,
            sin_t, cos_t,  0.,0.,
            0.,    0.,     1.,0.,
            0.,    0.,     0.,1.]
    rotm = PtMatrix(rotl)
    return PtTransform(rotm)

# ////////////
# // TO DO: rotate by axis
#/////////////
