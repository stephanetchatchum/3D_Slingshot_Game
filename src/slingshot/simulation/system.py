from ..physics.gravity import calculate_accelerations, calculate_probe_acceleration
from .integrator import rk4_step

def derivatives(state, G, m_sun, m_planet):
    sun_position, planet_position, probe_position, sun_velocity, planet_velocity, probe_velocity = state

    planet_acceleration, sun_acceleration = calculate_accelerations(G, m_sun, m_planet, sun_position, planet_position)

    probe_acceleration = calculate_probe_acceleration(G, m_sun, m_planet, sun_position, planet_position, probe_position)

    return sun_velocity, planet_velocity, probe_velocity, sun_acceleration, planet_acceleration, probe_acceleration

def simulate_step(G, sun_position, sun_velocity, planet_position, planet_velocity, probe_position, probe_velocity, m_sun, m_planet, dt):
    state = (sun_position, planet_position, probe_position, sun_velocity, planet_velocity, probe_velocity)

    new_state = rk4_step(state, dt, derivatives, G, m_sun, m_planet)

    new_sun_position, new_planet_position, new_probe_position, new_sun_velocity, new_planet_velocity, new_probe_velocity = new_state
    
    return new_sun_position, new_planet_position, new_probe_position, new_sun_velocity, new_planet_velocity, new_probe_velocity