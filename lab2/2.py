import pyglet
from pyglet.gl import *
from pyglet.window import key
from random import randint
import math

FILE = "cestice\\explosion.bmp"

tekstura = pyglet.image.load(FILE)
window = pyglet.window.Window(1000, 800)

OSVJEZI_PERIOD = 0.02
Y = 800
MAX_CESTICA = 200
NOVIH_CESTICA = 2
a = 2
v_0 = 2
ZIVOT = 6
delta_t = 0.1
SCALING = 0.5

class Cestica:
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(img=tekstura)
        self.sprite.scale = SCALING
        self.sprite.x = [-1, 1][randint(0,1)] * randint(0, 100)
        self.sprite.y = randint(0, 100)
        self.sprite.y = [-1, 1][randint(0,1)] * randint(0, (int)(math.sqrt(100 ** 2 - self.sprite.x ** 2)))
        self.sprite.x += 400
        self.sprite.y += 400
        self.zivot = randint(1, ZIVOT)
        self.t = 0


cestice = []
vjetar_x = 0

def osvjezi(arg):
    global cestice, MAX_CESTICA, vjetar_x, v_0, delta_t, a, NOVIH_CESTICA
    cestice = [cestica for cestica in cestice if cestica.t <= cestica.zivot]
    dostupno = MAX_CESTICA - len(cestice)
    if dostupno >= NOVIH_CESTICA:
        for i in range(NOVIH_CESTICA):
            cestice.append(Cestica())
    elif dostupno > 0:
        for i in range(dostupno):
            cestice.append(Cestica())
    for cestica in cestice:
        cestica.sprite.x += vjetar_x * cestica.t
        cestica.sprite.y -= v_0 * cestica.t + 0.5 * a * (cestica.t ** 2)
        cestica.t += delta_t
        cestica.sprite.opacity = (int)(((1 - cestica.t) / cestica.zivot) * 255)

pyglet.clock.schedule_interval(osvjezi, OSVJEZI_PERIOD)

@window.event
def on_draw():
    window.clear()

    for cestica in cestice:
        cestica.sprite.draw()

@window.event
def on_key_press(symbol, modifiers):
    global Y, a, delta_t, vjetar_x, NOVIH_CESTICA, MAX_CESTICA
    if symbol == key.W:
        MAX_CESTICA += 20
        print(MAX_CESTICA)
    elif symbol == key.S:
        if MAX_CESTICA > 20:
            MAX_CESTICA -= 20
        print(MAX_CESTICA)
    elif symbol == key.UP:
        if NOVIH_CESTICA > 0:
            NOVIH_CESTICA *= 2
        else:
            NOVIH_CESTICA = 1
        print(NOVIH_CESTICA)
    elif symbol == key.NUM_0:
        NOVIH_CESTICA = 0
        print(NOVIH_CESTICA)
    elif symbol == key.DOWN:
        if NOVIH_CESTICA >= 1:
            NOVIH_CESTICA //= 2
        print(NOVIH_CESTICA)
    elif symbol == key.RIGHT:
        vjetar_x += 1
        print(vjetar_x)
    elif symbol == key.LEFT:
        vjetar_x -= 1
        print(vjetar_x)
    elif symbol == key.PLUS:
        a += 0.2
        print(a)
    elif symbol == key.MINUS:
        if a >= 0.2:
            a -= 0.2
        print(a)


pyglet.app.run()