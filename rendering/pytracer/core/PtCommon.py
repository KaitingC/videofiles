import os,random

# Data Types
TDC_TYPE_INT        = 0x01
TDC_TYPE_FLOAT      = 0x02
TDC_TYPE_POINT      = 0x03
TDC_TYPE_POINT2     = 0x04
TDC_TYPE_VECTOR     = 0x05
TDC_TYPE_STRING     = 0x06
TDC_TYPE_MATRIX     = 0x07

dataTypeToStrDict   = {TDC_TYPE_INT:"int",
                       TDC_TYPE_FLOAT:"float",
                       TDC_TYPE_POINT:"point",
                       TDC_TYPE_POINT2:"point2",
                       TDC_TYPE_VECTOR:"vector",
                       TDC_TYPE_MATRIX:"matrix"}

#plugin Types
TDC_PLUGIN_CAMERA   = 0x00
TDC_PLUGIN_DRIVER   = 0x01
TDC_PLUGIN_SHAPE    = 0x02

rootDir= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def dataTypeToStr(dataType):
    if dataType in dataTypeToStrDict.keys():
        return dataTypeToStrDict[dataType]

def getRandomName(baseName,hashLength=16):
    letters     ='abcdefghijklmnopqrstuvwxyz'
    ucletters   = letters.upper()
    numbers     = '0123456789'*2
    all         = letters+ucletters+numbers

    return "%s_%s"%(baseName,"".join(random.sample(all,
                                                   hashLength if hashLength < len(all) else len(all))))

def clamp(x,mi,ma):
    return max(mi, min(x,ma))

class PtTypeError(Exception):
    def __init__(self,value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
