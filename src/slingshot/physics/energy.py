import numpy as np

def calculate_total_energy(G, m_sun, m_planet, sun_velocity, planet_velocity, sun_position, planet_position):
    K = (0.5*m_sun*(np.linalg.norm(sun_velocity)**2)) + (0.5*m_planet*(np.linalg.norm(planet_velocity)**2))
    U = (-G*m_sun*m_planet)/(np.linalg.norm(planet_position-sun_position))

    E = K+U

    return E