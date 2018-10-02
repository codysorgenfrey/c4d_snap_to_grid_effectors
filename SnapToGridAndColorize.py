import c4d
from c4d.modules import mograph as mo
#Welcome to the world of Python

def snap(v, mult, validate):
    vals = [int(round(v.x / mult)) * mult, int(round(v.y / mult)) * mult, int(round(v.z / mult)) * mult]
    if validate:
        for i in vals:
            if i == 0:
                i = mult
    return c4d.Vector(vals[0], vals[1], vals[2])

def main():
    md = mo.GeGetMoData(op)
    if md is None: return False
    
    cnt = md.GetCount()
    marr = md.GetArray(c4d.MODATA_MATRIX)
    curFrame = doc.GetTime().GetFrame(doc.GetFps())
    cd = md.GetArray(c4d.MODATA_COLOR)
    snapOff = float(op[c4d.ID_USERDATA,2])
    snapRot = c4d.utils.DegToRad(float(op[c4d.ID_USERDATA,3]))
    snapScale = float(op[c4d.ID_USERDATA,4])
    scaleOnZ = bool(op[c4d.ID_USERDATA,5])
    colorize = op[c4d.ID_USERDATA,6]
    irs = c4d.modules.render.InitRenderStruct()
    if not colorize.InitRender(irs):
        return False
    
    for i in reversed(xrange(0, cnt)):
        scale = c4d.Vector(marr[i].v1.GetLength(),marr[i].v2.GetLength(),marr[i].v3.GetLength())
        scale = snap(scale, snapScale, True)
        
        rot = c4d.utils.MatrixToHPB(marr[i])
        rot = snap(rot, snapRot, False)
       
        newMarr = c4d.utils.HPBToMatrix(rot)
       
        marr[i].v1 = newMarr.v1.GetNormalized() * scale.x
        marr[i].v2 = newMarr.v2.GetNormalized() * scale.y
        marr[i].v3 = newMarr.v3
        if scaleOnZ:
            marr[i].v3 = marr[i].v3.GetNormalized() * scale.z
        
        marr[i].off = snap(marr[i].off, snapOff, False)
        
        cd[i] = colorize.CalcGradientPixel(((cd[i][0] + 1 )*.5))

    colorize.FreeRender()
    md.SetArray(c4d.MODATA_MATRIX, marr, True)
    md.SetArray(c4d.MODATA_COLOR, cd, True)
    return True