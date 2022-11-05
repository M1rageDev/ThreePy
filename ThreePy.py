import pygame as pg
from math import sin, cos, radians

# constants
FOCAL_LENGTH = 256

# code
def stripListNL(x):
    r = []

    for e in x:
        r.append(e.replace("\n", ""))

    return e

def inRange(x, start, end):
    if start <= x <= end:
        return True
    else:
        return False

def sublist(x, start, end):
    r = []

    for i, e in enumerate(x):
        if inRange(i, start, end):
            r.append(e)

    return r

def strListToIntList(x):
    r = []

    for e in x:
        r.append(int(e))

    return r

def tuple2ListContents(x):
    y = list(x)
    for i, item in enumerate(y):
        y[i] = list(item)

    return y

def multiplyList(x, y):
    r = []

    for i in x:
        r.append(i * y)

    return r

def add2Lists(x, y):
    r = []

    for i, e in enumerate(x):
        r.append(e + y[i])

    return r

def matrixMult(x, y):
    x0 = x[0]
    x1 = x[1]
    x2 = x[2]

    mX = x0[0] * y[0] + x0[1] * y[1] + x0[2] * y[2]
    mY = x1[0] * y[0] + x1[1] * y[1] + x1[2] * y[2]
    mZ = x2[0] * y[0] + x2[1] * y[1] + x2[2] * y[2]

    return mX, mY, mZ

def RotationMatrix(axis, theta):
    if axis == "x":
        return [
            [1, 0, 0],
            [0, cos(radians(theta % 360)), sin(radians(theta % 360))],
            [0, -sin(radians(theta % 360)), cos(radians(theta % 360))]
        ]
    elif axis == "y":
        return [
            [cos(radians(theta % 360)), 0, sin(radians(theta % 360))],
            [0, 1, 0],
            [-sin(radians(theta % 360)), 0, cos(radians(theta % 360))]
        ]
    elif axis == "z":
        return [
            [cos(radians(theta % 360)), -sin(radians(theta % 360)), 0],
            [sin(radians(theta % 360)), cos(radians(theta % 360)), 0],
            [0, 0, 1]
        ]

class Mesh:
    def __init__(self, vertexTable, edgeTable):
        self.vertexTable = tuple2ListContents(vertexTable.copy())
        self.edgeTable = tuple2ListContents(edgeTable.copy())
        self.dotSize = 2

    @staticmethod
    def importFrom(filename):
        r = Mesh([], [])
        with open(filename, "r") as f:
            rl = f.readlines()

            vT = rl[0].split("**/**")[0].split(",")
            eT = rl[0].split("**/**")[1].split(",")

            for v in vT:
                r.vertexTable.append(strListToIntList(v.split(" ")))
            for e in eT:
                r.edgeTable.append(strListToIntList(e.split(" ")))

        return r

    def copy(self):
        r = Mesh(self.vertexTable.copy(), self.edgeTable.copy())
        r.dotSize = self.dotSize
        return r

    def offset(self, pos):
        for i, v in enumerate(self.vertexTable):
            v = list(v)
            v[0] += pos[0]
            v[1] += pos[1]
            v[2] += pos[2]
            self.vertexTable[i] = v

        return self

class RenderObject:
    def __init__(self, mesh: Mesh, position, rotation, flags=None):
        self.mesh = mesh.copy()
        self.orgMesh = mesh.copy()
        self.pos = list(position)
        self.rot = list(rotation)
        self.color = (0, 0, 0)

        if flags is not None:
            if "color" in flags.keys():
                self.color = flags["color"]

        self.updatePos()
        self.updateRot()

    def updatePos(self):
        self.mesh.offset(self.pos)
        self.pos = [0, 0, 0]

    def updateRot(self):
        rX = self.rot[0]
        rY = self.rot[1]
        rZ = self.rot[2]
        oVT = self.orgMesh.vertexTable
        vT = self.mesh.vertexTable

        for i, v in enumerate(oVT):
            vT[i] = matrixMult(RotationMatrix("x", rX), matrixMult(RotationMatrix("y", rY), matrixMult(RotationMatrix("z", rZ), v)))

    def updatePose(self):
        self.updatePos()
        self.updateRot()

class ThreePyRenderer:
    camPos = [0, 0, 0]

    @staticmethod
    def render(plane: pg.Surface, obj: RenderObject):
        p = plane
        pHx = plane.get_width() / 2
        pHy = plane.get_height() / 2
        vT = obj.mesh.vertexTable.copy()
        eT = obj.mesh.edgeTable.copy()
        dS = obj.mesh.dotSize
        pVs = []

        for v in vT:
            x, y, z = add2Lists(v, NewellRenderer.camPos)
            pX = pHx + (FOCAL_LENGTH * x) // (z + FOCAL_LENGTH)
            pY = pHy + (FOCAL_LENGTH * y) // (z + FOCAL_LENGTH)
            pVs.append((pX, pY))

            pg.draw.circle(p, obj.color, (pX, pY), dS)

        for e in eT:
            pg.draw.line(p, obj.color, pVs[e[0]], pVs[e[1]], 4)
