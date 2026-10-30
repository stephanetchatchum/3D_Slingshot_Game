from ..physics.gravity import calculate_accelerations
from .integrator import rk4_step

def derivatives(G, sun_position, sun_velocity, planet_position, planet_velocity, m_sun, m_planet):
    planet_acceleration, sun_acceleration = calculate_accelerations(G, m_sun, m_planet, sun_position, planet_position)

    return sun_velocity, planet_velocity, sun_acceleration, planet_acceleration

def simulate_step(G, sun_position, sun_velocity, planet_position, planet_velocity, m_sun, m_planet, dt):
    state = (sun_position, planet_position, sun_velocity, planet_velocity)

    new_state = rk4_step(state, dt, derivatives, G, m_sun, m_planet)

    new_sun_position, new_planet_position, new_sun_velocity, new_planet_velocity = new_state
    
    return new_sun_position, new_sun_velocity, new_planet_position, new_planet_velocity