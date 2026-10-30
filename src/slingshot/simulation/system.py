from ..physics.gravity import calculate_accelerations
from .integrator import update_position, update_velocity

def simulate_step(G, sun_position, sun_velocity, planet_position, planet_velocity, m_sun, m_planet, dt):
    planet_acceleration, sun_acceleration = calculate_accelerations(G, m_sun, m_planet, sun_position, planet_position)

    new_sun_position = update_position(sun_velocity, sun_position, dt)
    new_sun_velocity = update_velocity(sun_acceleration, sun_velocity, dt)

    new_planet_position = update_position(planet_velocity, planet_position, dt)
    new_planet_velocity = update_velocity(planet_acceleration, planet_velocity, dt)

    return new_sun_position, new_sun_velocity, new_planet_position, new_planet_velocity