from ursina import *
from .simulation.system import simulate_step
import numpy as np
import math

G = 1
m_sun = 7
m_planet = 3

sun_position = np.array([0,0,0])
planet_position = np.array([10,0,0])
probe_position = np.array([10.8,-2,0])
probe_velocity = np.array([0,3,0])
relative_position = planet_position - sun_position
distance = np.linalg.norm(relative_position)
relative_speed = math.sqrt((G*(m_sun+m_planet)/distance))

orbital_normal = np.array([0,0,1])
direction = np.cross(orbital_normal, relative_position)
direction = direction / np.linalg.norm(direction)

relative_velocity = relative_speed * direction

sun_velocity = -(m_planet*relative_velocity)/(m_planet+m_sun)
planet_velocity = (m_sun*relative_velocity)/(m_planet+m_sun)

time_scale = 1

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
    position=(10, 0, 0)
)

probe = Entity(
    model='sphere',
    color=color.white,
    scale=0.3,
    position=probe_position
)

sun_trail = Entity(
    model=Mesh(vertices=[], mode='line', thickness=3),
    color=color.yellow
)

planet_trail = Entity(
    model=Mesh(vertices=[], mode='line', thickness=2),
    color=color.azure
)

probe_trail = Entity(
    model=Mesh(vertices=[], mode='line', thickness=2),
    color=color.white
)

DirectionalLight()
AmbientLight()
EditorCamera()

physics_accumulator = 0.0
physics_time_step = 0.001

sun_path = []
planet_path = []
probe_path = []

simulation_time = 0

def update():
    global physics_accumulator
    global sun_position, sun_velocity
    global planet_position, planet_velocity, time_scale
    global probe_position, probe_velocity, simulation_time
    physics_accumulator += min(time.dt, 0.05) * time_scale

    while physics_accumulator >= physics_time_step:
        sun_position, planet_position, probe_position, sun_velocity, planet_velocity, probe_velocity = simulate_step(
            G, sun_position, sun_velocity, 
            planet_position, planet_velocity, 
            probe_position, probe_velocity, m_sun, 
            m_planet, physics_time_step
        )
        physics_accumulator -= physics_time_step

    sun.position = Vec3(*sun_position)
    planet.position = Vec3(*planet_position)
    probe.position = Vec3(*probe_position)


    sun_path.append(Vec3(*sun_position))
    planet_path.append(Vec3(*planet_position))
    probe_path.append(Vec3(*probe_position))

    sun_trail.model.vertices = sun_path
    if len(sun_path) >= 2:
        sun_trail.model.vertices = sun_path
        sun_trail.model.generate()

    if len(planet_path) >= 2:
        planet_trail.model.vertices = planet_path
        planet_trail.model.generate()

    if len(probe_path) >= 2:
        probe_trail.model.vertices = probe_path
        probe_trail.model.generate()

app.run()