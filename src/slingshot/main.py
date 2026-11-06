from ursina import *
from .simulation.system import simulate_step
from .visuals.celestial_bodies import create_sun, create_planet, create_probe
from .visuals.trails import create_trail, update_trail
from .visuals.starfield import create_starfield
import numpy as np
import math
from .ui.dashboard import Dashboard

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
    position=(3.3, -0.8, 0),        # the point the camera orbits around (middle of the scene)
    rotation=(13.7, -13.9, 0),      # viewing angle
    move_speed=15,
    rotation_speed=150,
    zoom_speed=1.5
)
editor_camera.target_z = -32       # how far the camera sits from that point
camera.z = -32
camera.position = (0, 0, -25)
camera.look_at(Vec3(5, 0, 0))

physics_accumulator = 0.0
physics_time_step = 0.001

sun_path = []
planet_path = []
probe_path = []

simulation_time = 0

paused = False
closest_approach = float('inf')


def reset_simulation():
    global G, m_planet, time_scale
    global physics_accumulator, simulation_time, closest_approach
    global sun_position, sun_velocity, planet_position, planet_velocity
    global probe_position, probe_velocity

    G = dashboard.value('G')
    m_planet = dashboard.value('planet_mass')
    time_scale = dashboard.value('time_scale')

    sun_position = np.array([0.0, 0.0, 0.0])
    planet_position = np.array([10.0, 0.0, 0.0])
    probe_position = np.array([10.8, -2.0, 0.0])
    probe_velocity = np.array([0.0, dashboard.value('probe_speed'), 0.0])

    relative_position = planet_position - sun_position
    distance = np.linalg.norm(relative_position)
    relative_speed = math.sqrt(G * (m_sun + m_planet) / distance)
    direction = np.cross(orbital_normal, relative_position)
    direction = direction / np.linalg.norm(direction)
    relative_velocity = relative_speed * direction
    sun_velocity = -(m_planet * relative_velocity) / (m_planet + m_sun)
    planet_velocity = (m_sun * relative_velocity) / (m_planet + m_sun)

    physics_accumulator = 0.0
    simulation_time = 0
    closest_approach = float('inf')
    for path in (sun_path, planet_path, probe_path):
        path.clear()
    for trail in (sun_trail, planet_trail, probe_trail):
        trail.model.vertices = []
        trail.model.generate()


def toggle_pause():
    global paused
    paused = not paused
    dashboard.set_paused(paused)


dashboard = Dashboard(
    defaults={'planet_mass': m_planet, 'G': G, 'probe_speed': 3, 'time_scale': time_scale},
    on_reset=reset_simulation,
    on_toggle_pause=toggle_pause,
)

dashboard_visible = True
follow_options = [None, 'probe', 'planet', 'sun']
follow_index = 0


def input(key):
    global dashboard_visible, follow_index
    if key == 'space':
        toggle_pause()
    elif key == 'r':
        reset_simulation()
    elif key == 'h':
        dashboard_visible = not dashboard_visible
        dashboard.set_visible(dashboard_visible)
    elif key == 'c':
        follow_index = (follow_index + 1) % len(follow_options)
        name = follow_options[follow_index]
        if name is None:                      # back to the default view
            editor_camera.position = Vec3(3.3, -0.8, 0)
            editor_camera.target_z = -32
        else:                                 # follow a body, at a sensible distance
            editor_camera.target_z = {'probe': -8, 'planet': -10, 'sun': -25}[name]

def update():
    global physics_accumulator
    global sun_position, sun_velocity
    global planet_position, planet_velocity, time_scale
    global probe_position, probe_velocity, simulation_time
    global closest_approach

    time_scale = dashboard.value('time_scale')
    editor_camera.target_z = clamp(editor_camera.target_z, -150, -4)   # limit zoom

    # camera follows the chosen body (press C to cycle: free, probe, planet, sun)
    target = {'probe': probe_position, 'planet': planet_position, 'sun': sun_position}.get(follow_options[follow_index])
    if target is not None:
        editor_camera.position = lerp(editor_camera.position, Vec3(*target), 5 * time.dt)

    if paused:
        return
    physics_accumulator += min(time.dt, 0.05) * time_scale

    while physics_accumulator >= physics_time_step:
        sun_position, planet_position, probe_position, sun_velocity, planet_velocity, probe_velocity = simulate_step(
            G, sun_position, sun_velocity, 
            planet_position, planet_velocity, 
            probe_position, probe_velocity, m_sun, 
            m_planet, physics_time_step
        )
        simulation_time += physics_time_step
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

    closest_approach = min(closest_approach, np.linalg.norm(probe_position - planet_position))
    dashboard.show_results({
        'time': simulation_time,
        'probe_speed': np.linalg.norm(probe_velocity - sun_velocity),
        'distance': np.linalg.norm(probe_position - planet_position),
        'closest': closest_approach if closest_approach != float('inf') else 0.0,
    })

app.run()