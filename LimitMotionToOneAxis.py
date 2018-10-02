import c4d
from c4d.modules import mograph as mo
#Welcome to the world of Python

def dmain():
    MY_ARR_ID = 1041427 # have a unique ID from Plugin Cafe
    md = mo.GeGetMoData(op)
    if md is None: return False

    # A proper DescID is needed for AddArray()
    # Especially set the correct data type here!
    did = c4d.DescID(c4d.DescLevel(MY_ARR_ID, c4d.DTYPE_MATRIX, 0))

    myArr = md.GetArray(MY_ARR_ID)
    if myArr is None: # check, if the array has already been added earlier on
        idxArr = md.AddArray(did, "my array", 0)
        if idxArr == c4d.NOTOK:
            print "Error" # handle error here
            return False
        
        # Finally fill the array with the current matrice
        marr = md.GetArray(c4d.MODATA_MATRIX)
        md.SetArray(MY_ARR_ID, marr, True)
        
    else:
        previousMarr = md.GetArray(MY_ARR_ID)
        marr = md.GetArray(c4d.MODATA_MATRIX)
        copyMarr = marr #copy the list in order tosave data before we do any move
        
        # Do your calculation
        cnt = md.GetCount()
        for i in reversed(xrange(0, cnt)):
            print previousMarr[i].off
            v = marr[i].off - previousMarr[i].off
            vList = {"x":abs(v.x), "y":abs(v.y), "z":abs(v.z)}
            vList = sorted(vList.iteritems(), key=lambda (k,v): (v,k), reverse=True)
            if vList[0][0] == "x":
                newV = c4d.Vector(v.x, 0,0)
            elif vList[0][0] == "y":
                newV = c4d.Vector(0,v.y,0)
            else:
                newV = c4d.Vector(0,0,v.z)
            marr[i].off = previousMarr[i].off + newV
    
        # Set the array with the initial state + the new matrice
        md.SetArray(c4d.MODATA_MATRIX, marr, True)
        md.SetArray(MY_ARR_ID, copyMarr, True)
        
    return True

def main():
    MY_ARR_ID = 1041427 # have a unique ID from Plugin Cafe
    md = mo.GeGetMoData(op)
    if md is None: return False

    # A proper DescID is needed for AddArray()
    # Especially set the correct data type here!
    did = c4d.DescID(c4d.DescLevel(MY_ARR_ID, c4d.DTYPE_MATRIX, 0))

    myArr = md.GetArray(MY_ARR_ID)
    if myArr is None: # check, if the array has already been added earlier on
        print "None"
        idxArr = md.AddArray(did, "my array", 0)
        if idxArr == c4d.NOTOK:
            print "Error" # handle error here
            return False
        
        # Finally fill the array with the current matrice
        marr = md.GetArray(c4d.MODATA_MATRIX)
        md.SetArray(MY_ARR_ID, marr, True)
        
    else:
        previousMarr = md.GetArray(MY_ARR_ID)
        marr = md.GetArray(c4d.MODATA_MATRIX)
        copyMarr = marr #copy the list in order tosave data before we do any move
        
        # Do your calculation
        fall = md.GetFalloffs()
        cnt = md.GetCount()
        for i in reversed(xrange(0, cnt)):
            print previousMarr[i].off
            print marr[i].off
            marr[i].off = marr[i].off+fall[cnt-i-1]*100.0
    
        # Set the array with the initial state + the new matrice
        md.SetArray(c4d.MODATA_MATRIX, marr, True)
        md.SetArray(MY_ARR_ID, copyMarr, True)
        
    return True