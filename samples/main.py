from ThreePy import *
import pygame as pg

pg.init()
window = pg.display.set_mode((640, 480))

# meshes
cubeMesh = Mesh.importFrom("sample_models/cube.msh")

# scene
cube = RenderObject(cubeMesh.copy(), (0, 0, 0), (0, 0, 0), {"color": (100, 100, 100)})

# main loop
running = True
clock = pg.time.Clock()
while running:
    window.fill((255, 255, 255))
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        NewellRenderer.camPos[2] -= 2
    if keys[pg.K_s]:
        NewellRenderer.camPos[2] += 2
    if keys[pg.K_a]:
        NewellRenderer.camPos[0] += 2
    if keys[pg.K_d]:
        NewellRenderer.camPos[0] -= 2
    if keys[pg.K_UP]:
        NewellRenderer.camPos[1] += 2
    if keys[pg.K_DOWN]:
        NewellRenderer.camPos[1] -= 2

    if keys[pg.K_RIGHT]:
        cube.rot[1] += 1
        cube.updateRot()
    if keys[pg.K_LEFT]:
        cube.rot[1] -= 1
        cube.updateRot()

    NewellRenderer.render(window, cube)

    pg.display.flip()
    clock.tick(60)
