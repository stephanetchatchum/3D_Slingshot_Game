import numpy as np
from slingshot.physics.energy import calculate_total_energy
from slingshot.simulation.system import simulate_step
import math

def test_total_energy():
    sun_position = np.array([0.0, 0.0, 0.0])
    planet_position = np.array([5.0, 0.0, 0.0])

    sun_velocity = np.array([0.0, 0.0, 0.0])
    planet_velocity = np.array([0.0, 0.0, 0.0])

    E = calculate_total_energy(1, 10, 3, sun_velocity, planet_velocity, sun_position, planet_position)

    assert np.isclose(-6, E)

def test_rk4_conserves_energy():
    G = 1
    m_sun = 10
    m_planet = 3
    dt = 0.1
    sun_position = np.array([0.0, 0.0, 0.0])
    planet_position = np.array([5.0, 0.0, 0.0])

    relative_position = planet_position - sun_position
    distance = np.linalg.norm(relative_position)
    relative_speed = math.sqrt((G*(m_sun+m_planet)/distance))

    orbital_normal = np.array([0,0,1])
    direction = np.cross(orbital_normal, relative_position)
    direction = direction / np.linalg.norm(direction)

    relative_velocity = relative_speed * direction

    sun_velocity = -(m_planet*relative_velocity)/(m_planet+m_sun)
    planet_velocity = (m_sun*relative_velocity)/(m_planet+m_sun)

    initial_energy = calculate_total_energy(
        G, m_sun, m_planet,
        sun_velocity, planet_velocity,
        sun_position, planet_position
    )

    for _ in range(10000):
        sun_position, sun_velocity, planet_position, planet_velocity = simulate_step(
            G, sun_position, sun_velocity,
            planet_position, planet_velocity,
            m_sun, m_planet, dt
        )

    final_energy = calculate_total_energy(
        G, m_sun, m_planet,
        sun_velocity, planet_velocity,
        sun_position, planet_position
    )

    relative_error = (abs(final_energy-initial_energy))/(abs(initial_energy))

    assert relative_error < 1e-6

    print(f"Relative energy error: {relative_error:.12e}")


def test_rk4_accuracy_improves_with_smaller_timestep():
    G = 1
    m_sun = 10
    m_planet = 3
    dt = 0.05
    sun_position = np.array([0.0, 0.0, 0.0])
    planet_position = np.array([5.0, 0.0, 0.0])

    relative_position = planet_position - sun_position
    distance = np.linalg.norm(relative_position)
    relative_speed = math.sqrt((G*(m_sun+m_planet)/distance))

    orbital_normal = np.array([0,0,1])
    direction = np.cross(orbital_normal, relative_position)
    direction = direction / np.linalg.norm(direction)

    relative_velocity = relative_speed * direction

    sun_velocity = -(m_planet*relative_velocity)/(m_planet+m_sun)
    planet_velocity = (m_sun*relative_velocity)/(m_planet+m_sun)

    initial_energy = calculate_total_energy(
        G, m_sun, m_planet,
        sun_velocity, planet_velocity,
        sun_position, planet_position
    )

    for _ in range(10000):
        sun_position, sun_velocity, planet_position, planet_velocity = simulate_step(
            G, sun_position, sun_velocity,
            planet_position, planet_velocity,
            m_sun, m_planet, dt
        )

    final_energy = calculate_total_energy(
        G, m_sun, m_planet,
        sun_velocity, planet_velocity,
        sun_position, planet_position
    )

    relative_error = (abs(final_energy-initial_energy))/(abs(initial_energy))

    assert relative_error < 1e-6

    print(f"Relative energy error: {relative_error:.12e}")