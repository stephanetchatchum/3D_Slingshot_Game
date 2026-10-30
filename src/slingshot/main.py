from ursina import *

app = Ursina()

sun = Entity(
    model='sphere',
    color=color.yellow,
    scale=3
)

planet = Entity(
    model='sphere',
    color=color.blue,
    scale=1,
    position=(5, 0, 0)
)

DirectionalLight()
AmbientLight()
EditorCamera()
app.run()