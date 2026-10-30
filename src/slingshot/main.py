from ursina import *
from .simulation.system import simulate_step
import numpy as np
import math

G = 1
m_sun = 1
m_planet = 0.5
dt = 0.01

sun_position = np.array([0,0,0])
planet_position = np.array([5,0,0])
relative_position = planet_position - sun_position
distance = np.linalg.norm(relative_position)
relative_speed = math.sqrt((G*(m_sun+m_planet)/distance))

orbital_normal = np.array([0,0,1])
direction = np.cross(orbital_normal, relative_position)
direction = direction / np.linalg.norm(direction)

relative_velocity = relative_speed * direction

sun_velocity = -(m_planet*relative_velocity)/(m_planet+m_sun)
planet_velocity = (m_sun*relative_velocity)/(m_planet+m_sun)

time_scale = 10

app = Ursina()

sun = Entity(
    model='sphere',
    color=color.yellow,
    scale=2
)

planet = Entity(
    model='sphere',
    color=color.blue,
    scale=1,
    position=(5, 0, 0)
)

sun_trail = Entity(
    model=Mesh(vertices=[], mode='line', thickness=2),
    color=color.yellow
)

planet_trail = Entity(
    model=Mesh(vertices=[], mode='line', thickness=2),
    color=color.azure
)

DirectionalLight()
AmbientLight()
EditorCamera()

physics_accumulator = 0.0
physics_time_step = 0.01

sun_path = []
planet_path = []

def update():
    global physics_accumulator
    global sun_position, sun_velocity
    global planet_position, planet_velocity, time_scale
    physics_accumulator += time.dt * time_scale

    while physics_accumulator >= physics_time_step:
        sun_position, sun_velocity, planet_position, planet_velocity = simulate_step(
            G, sun_position, sun_velocity,
            planet_position, planet_velocity,
            m_sun, m_planet, physics_time_step
        )
        physics_accumulator -= physics_time_step

    sun.position = Vec3(*sun_position)
    planet.position = Vec3(*planet_position)

    sun_path.append(Vec3(*sun_position))
    planet_path.append(Vec3(*planet_position))

    sun_trail.model.vertices = sun_path
    if len(sun_path) >= 2:
        sun_trail.model.vertices = sun_path
        sun_trail.model.generate()

    if len(planet_path) >= 2:
        planet_trail.model.vertices = planet_path
        planet_trail.model.generate()

app.run()