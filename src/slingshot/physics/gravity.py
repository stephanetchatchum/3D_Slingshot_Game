import numpy as np

sun_position = np.array([0,0,0])
planet_position = np.array([5,0,0])

sun_velocity = np.array([0, -0.18257, 0])
planet_velocity = np.array([0, 0.36513, 0])
dt = 0.01

G = 1
m_sun = 1
m_planet = 0.5

def calculate_accelerations(G, m_sun, m_planet, sun_position, planet_position):
    separation = sun_position - planet_position
    distance = np.linalg.norm(separation)

    if distance == 0:
        raise ValueError("The two bodies cannot occupy the same position.")

    planet_acceleration = (G*m_sun*separation)/(distance**3)
    sun_acceleration = (G*m_planet*-separation)/(distance**3)

    return planet_acceleration, sun_acceleration
