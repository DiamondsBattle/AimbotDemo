from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import arctan, pi, sqrt


radToDeg = lambda rad: rad * (180 / pi)


def getAngleDif(f, t):
    # The camera has a top offset to the body, so we are using camera_pivot
    # to get the camera's position and not the body's
    h_dif = arctan((f.z - t.z) / (f.x - t.x))
    f_y = f.camera_pivot.y + f.y + 3
    v_dif = arctan((t.y - f_y + 3) / sqrt((t.z - f.z)**2 + (t.x - f.x)**2))

    if t.x - f.x < 0:
        return 360 - radToDeg(h_dif) - 90, radToDeg(-v_dif)
    elif t.x - f.x > 0:
        return 360 - radToDeg(h_dif) + 90, radToDeg(-v_dif)


def update():
    if held_keys['x']:
        me.rotation_y, me.camera_pivot.rotation_x = getAngleDif(me, enemy)


app = Ursina()

window.vsync = True

ground = Entity(model='cube', color=color.rgba(0, 0, 0, .2), texture='white_cube', scale=Vec3(100, 1, 100), position=Vec3(2, -2, 2), collider='box', texture_scale=(2, 2, 1))

enemy = Entity(model='cube', color=color.red, texture='white_cube', position=Vec3(2, 1, 2))
enemy.animate_position(Vec3(7, 4, 2), duration=3)
enemy.animate_position(Vec3(-7, -4, -2), duration=3, delay=3)
me = FirstPersonController(position=Vec3(4, 2, -4))
# QWERTY to AZERTY rebinds
input_handler.rebind('z', 'w')
input_handler.rebind('q', 'a')


app.run()