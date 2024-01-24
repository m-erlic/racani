FILE = "C:\\Users\\marij\\Desktop\\Racunalna animacija\\objekti\\bird.obj"
PATH_FILE = "C:\\Users\\marij\\Desktop\\Racunalna animacija\\1lab\\putanja.txt"
STEP_PERIOD = 0.1

import numpy as np
import pyglet as pg
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import pyglet.gl as gl
import math

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getAsArray(self):
        return np.array([self.x, self.y, self.z])

class Polygon:
    def __init__(self, polygonVertices):
        self.vertices = polygonVertices

vertices = []
polygons = []

def readObject():
    global vertices, polygons

    file = open(FILE, "r")
    lines = file.readlines()
                         
    for line in lines:
        line = line.strip()

        if len(line) == 0 or line[0] == "#" or line[0] == "g":
            continue

        elif line[0] == "v":
            coordinates = line.split(" ")
            vertices.append(Vertex(float(coordinates[1]), float(coordinates[2]), float(coordinates[3])))

        elif line[0] == "f":
            polygonVerticesStr = line[1:].strip().split(" ")
            polygonVertices = []
            for pv in polygonVerticesStr:
                polygonVertices.append(int(pv) - 1)
            polygons.append(Polygon(polygonVertices))

readObject()

x_min = vertices[0].x
x_max = vertices[0].x
y_min = vertices[0].y
y_max = vertices[0].y
z_min = vertices[0].z
z_max = vertices[0].z

def findMinAndMax():
    global vertices, x_min, x_max, y_min, y_max, z_min, z_max

    for v in vertices:
        if v.x < x_min:
            x_min = v.x
        if v.x > x_max:
            x_max = v.x
        if v.y < y_min:
            y_min = v.y
        if v.y > y_max:
            y_max = v.y
        if v.z < z_min:
            z_min = v.z
        if v.z > z_max:
            z_max = v.z

findMinAndMax()

def findCenter():
    global x_min, x_max, y_min, y_max, z_min, z_max

    x = (x_min + x_max) / 2
    y = (y_min + y_max) / 2
    z = (z_min + z_max) / 2

    return Vertex(x, y, z)

center = findCenter()

def translateToTheOrigin():
    global vertices, center

    for v in vertices:
        v.x = v.x - center.x
        v.y = v.y - center.y
        v.z = v.z - center.z

translateToTheOrigin()

def scaleNumber(n, min, max, a, b):
    return (b - a) * (n-min)/(max-min) + a

x_min = vertices[0].x
x_max = vertices[0].x
y_min = vertices[0].y
y_max = vertices[0].y
z_min = vertices[0].z
z_max = vertices[0].z

findMinAndMax()

def scaleObject():
    global vertices, x_min, x_max, y_min, y_max, z_min, z_max

    for v in vertices:
        v.x = scaleNumber(v.x, x_min, x_max, -1, 1)
        v.y = scaleNumber(v.y, y_min, y_max, -1, 1)
        v.z = scaleNumber(v.z, z_min, z_max, -1, 1)

scaleObject()

#for v in vertices:
#    print(str(v.x) + " " + str(v.y) + " " + str(v.z))

pathVertices = []

def readPath():
    global pathVertices

    file = open(PATH_FILE, "r")
    lines = file.readlines()

    for line in lines:
        line = line.strip()
   
        coordinates = line.split(" ")
        pathVertices.append(Vertex(float(coordinates[0]), float(coordinates[1]), float(coordinates[2])))

readPath()

B_i_3 = (1.0 / 6) * np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 0, 3, 0],
    [1, 4, 1, 0]
])

segments = []

for i in range(len(pathVertices) - 3):
    segment = [pathVertices[i], pathVertices[i + 1], pathVertices[i + 2], pathVertices[i + 3]]
    segments.append(segment)

t_100_s = range(0, 100, 5)
path = []
tangents = []
dcm = []

for segment in segments:
    for t_100 in t_100_s:
        t = t_100 / 100.0

        T_3 = np.array([t ** 3, t ** 2, t, 1])
        R_i = np.array([
            segment[0].getAsArray(),
            segment[1].getAsArray(),
            segment[2].getAsArray(),
            segment[3].getAsArray()
        ])

        p_i_t = np.matmul(np.matmul(T_3, B_i_3), R_i)
        path.append(p_i_t)

        T_3_d = np.array([t ** 2, t, 1])
        B_i_3_d = (1 / 2.0) * np.array([
            [-1, 3, -3, 1],
            [2, -4, 2, 0],
            [-1, 0, 1, 0]
        ])
        
        p_i_t_tangent = np.matmul(np.matmul(T_3_d, B_i_3_d), R_i)
        tangents.append(p_i_t_tangent)

        T_3_dd = np.array([2 * t, 1, 0])
        p_i_t_tangent_d = np.matmul(np.matmul(T_3_d, B_i_3_d), R_i)
        
        u_t = np.cross(p_i_t_tangent, p_i_t_tangent_d)     
        w_t = np.cross(p_i_t_tangent, u_t)   

        dcm.append(np.array(
            [
                [p_i_t_tangent[0], u_t[0], w_t[0]],
                [p_i_t_tangent[1], u_t[1], w_t[1]],
                [p_i_t_tangent[2], u_t[2], w_t[2]],
            ]
        ))

window = pyglet.window.Window(1000, 800)

X = 0
Y = -1
Z = -4

X_rot = -30
Y_rot = 0
Z_rot = 0

def drawPath():
    global path

    glBegin(GL_POINTS)

    for p in path:
        p_x = p[0] / 20
        p_y = p[1] / 20
        p_z = p[2] / 20
        glVertex3f(p_x, p_y, p_z)

    glEnd()



def drawTangents():
    glBegin(GL_LINES)

    for i in range(len(path)):
        start = path[i]
        end = np.add(path[i], tangents[i])
        glVertex3f(start[0] / 20, start[1] / 20, start[2] / 20)
        glVertex3f(end[0] / 20, end[1] / 20, end[2] / 20)
        if i == 10:
            print(start)
            print(end)

    glEnd()

i = 0

def drawTangent():
    global i
    
    glBegin(GL_LINES)

    start = path[i]
    end = np.add(path[i], tangents[i])
    glVertex3f(start[0] / 20, start[1] / 20, start[2] / 20)
    glVertex3f(end[0] / 20, end[1] / 20, end[2] / 20)

    glEnd()


def drawPolygon(vertices):
    global i

    x_min = vertices[-1][0]
    x_max = vertices[-1][0]
    y_min = vertices[-1][1]
    y_max = vertices[-1][1]
    z_min = vertices[-1][1]
    z_max = vertices[-1][1]
    
    for j in range(0, len(vertices)):
        if j == len(vertices) - 1:
            xs = vertices[j][0]
            ys = vertices[j][1]
            zs = vertices[j][2]
            xe = vertices[0][0]
            ye = vertices[0][1]
            ze = vertices[0][2]
        else:
            xs = vertices[j][0]
            ys = vertices[j][1]
            zs = vertices[j][2]
            xe = vertices[j + 1][0]
            ye = vertices[j + 1][1]
            ze = vertices[j + 1][2]
            if xs < x_min:
                x_min = xs
            elif xs > x_max:
                x_max = xs 
            if ys < y_min:
                y_min = ys
            elif ys > y_max:
                y_max = ys 
            if zs < z_min:
                z_min = zs
            elif zs > z_max:
                z_max = zs
        glBegin(GL_LINES)
        glVertex3f(xs / 20, ys / 20, zs / 20)
        glVertex3f(xe / 20, ye / 20, ze / 20)
        glEnd()


def drawObject():
    for polygon in polygons:
        polygonVertices = []
        for v in polygon.vertices:
            polygonVertices.append(vertices[v].getAsArray())
        drawPolygon(polygonVertices)

def drawObjectDCM():
    for polygon in polygons:
        polygonVertices = []
        for v in polygon.vertices:
            polygonVertices.append(np.matmul(dcm[i], vertices[v].getAsArray()))
        drawPolygon(polygonVertices)

def calculateAngle():
    global i

    s = np.array([0, 0, 1])
    e = tangents[i]

    return math.degrees(math.acos(np.dot(s, e) / (np.linalg.norm(s) * np.linalg.norm(e))))

def calculateAxis():
    global i

    s = np.array([0, 0, 1])
    e = tangents[i]

    return np.cross(s, e)

def nextStep(arg):
    global i

    if i < len(path) - 1:
        i += 1

@window.event
def on_draw():
    global i 

    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, (window.width / window.height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(X, Y, Z) 

    glRotatef(X_rot, 1, 0, 0)
    glRotatef(Y_rot, 0, 1, 0)
    glRotatef(Z_rot, 0, 0, 1)

    drawPath()
    drawTangent()

    glTranslatef(path[i][0] / 20, path[i][1] / 20, path[i][2] / 20)
    
    angle = calculateAngle()
    axis = calculateAxis()
    glRotatef(angle, axis[0], axis[1], axis[2])

    drawObject()

    #drawObjectDCM()

    pg.clock.schedule_once(nextStep, STEP_PERIOD)

    
        

@window.event
def on_key_press(symbol, modifiers):
    global X, Y, Z, X_rot, Y_rot, Z_rot
    if symbol == key.RIGHT:
        Y -= 0.1
    elif symbol == key.LEFT:
        Y += 0.1
    elif symbol == key.UP:
        X -= 0.1
    elif symbol == key.DOWN:
        X += 0.1
    elif symbol == key.MINUS:
        Z -= 0.1
    elif symbol == key.PLUS:
        Z += 0.1
    elif symbol == key.Q:
        X_rot += 1
    elif symbol == key.A:
        X_rot -= 1
    elif symbol == key.W:
        Y_rot += 1
    elif symbol == key.S:
        Y_rot -= 1
    elif symbol == key.E:
        Z_rot += 1
    elif symbol == key.D:
        Z_rot -= 1

pyglet.app.run()