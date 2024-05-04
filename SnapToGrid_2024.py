import c4d
from c4d.modules import mograph as mo

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
    snapOff = float(op[c4d.ID_USERDATA,2]) # float control units
    snapRot = float(op[c4d.ID_USERDATA,3]) # float control degrees
    snapScale = float(op[c4d.ID_USERDATA,4]) # float control real
    scaleOnZ = bool(op[c4d.ID_USERDATA,5]) # bool control

    for i in reversed(range(0, cnt)):
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

    md.SetArray(c4d.MODATA_MATRIX, marr, op[c4d.FIELDS].HasContent())


    return True