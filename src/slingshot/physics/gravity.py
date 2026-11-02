import numpy as np

def calculate_accelerations(G, m_sun, m_planet, sun_position, planet_position):
    separation = sun_position - planet_position
    distance = np.linalg.norm(separation)

    if distance == 0:
        raise ValueError("The two bodies cannot occupy the same position.")

    planet_acceleration = (G*m_sun*separation)/(distance**3)
    sun_acceleration = (G*m_planet*-separation)/(distance**3)

    return planet_acceleration, sun_acceleration

def calculate_probe_acceleration(G, m_sun, m_planet, sun_position, planet_position, probe_position):
    probe_planet_separation = probe_position - planet_position
    probe_sun_separation = probe_position - sun_position

    probe_planet_distance = np.linalg.norm(probe_planet_separation)
    probe_sun_distance = np.linalg.norm(probe_sun_separation)

    if probe_planet_distance == 0 or probe_sun_distance == 0:
        raise ValueError("The Probe cannot be at the same position as the sun or planet")

    _sun_acceleration = (G*m_sun*probe_sun_separation)/probe_sun_distance**3
    _planet_acceleration = (G*m_planet*probe_planet_separation)/probe_planet_distance**3

    probe_acceleration = -(_sun_acceleration + _planet_acceleration)

    return probe_acceleration