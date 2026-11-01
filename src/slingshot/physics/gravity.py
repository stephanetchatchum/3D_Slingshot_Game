import numpy as np

def calculate_accelerations(G, m_sun, m_planet, sun_position, planet_position):
    separation = sun_position - planet_position
    distance = np.linalg.norm(separation)

    if distance == 0:
        raise ValueError("The two bodies cannot occupy the same position.")

    planet_acceleration = (G*m_sun*separation)/(distance**3)
    sun_acceleration = (G*m_planet*-separation)/(distance**3)

    return planet_acceleration, sun_acceleration
