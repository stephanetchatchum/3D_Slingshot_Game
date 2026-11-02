from ursina import *
from .simulation.system import simulate_step
from .visuals.celestial_bodies import create_sun, create_planet, create_probe
from .visuals.trails import create_trail, update_trail
from .visuals.starfield import create_starfield
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
window.color = color.Color(0.01, 0.02, 0.06, 1) 
create_starfield()

sun = create_sun()

planet = create_planet()

probe = create_probe(probe_position)

sun_trail = create_trail(color.orange, 2)
planet_trail = create_trail(color.azure, 2)
probe_trail = create_trail(color.white, 2)

AmbientLight(color=color.rgba32(20, 20, 30, 255))
DirectionalLight(
    color=color.white,
    direction=(1, -1, -1)
)



editor_camera = EditorCamera(
    rotation=(20, -35, 0),
    position=(0, 0, -15),
    move_speed=15,
    rotation_speed=150,
    zoom_speed=1.5
)

camera.position = (0, 0, -25)
camera.look_at(Vec3(5, 0, 0))

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

    planet.rotation_y += 20 * time.dt * time_scale
    planet.clouds.rotation_y += 4 * time.dt * time_scale
    sun.rotation_y += 3 * time.dt * time_scale

    sun_path.append(Vec3(*sun_position))
    planet_path.append(Vec3(*planet_position))
    probe_path.append(Vec3(*probe_position))

    update_trail(sun_trail, sun_path)
    update_trail(planet_trail, planet_path)
    update_trail(probe_trail, probe_path)

app.run()