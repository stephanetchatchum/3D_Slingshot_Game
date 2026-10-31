def update_velocity(acceleration, velocity, dt):
    velocity = velocity + acceleration*dt

    return velocity

def update_position(velocity, position, dt):
    position = position + velocity*dt

    return position

def rk4_step(state, dt, derivative_func, G, m_sun, m_planet):
    #k1
    sun_position, planet_position, sun_velocity, planet_velocity = state

    sun_velocity, planet_velocity, sun_acceleration, planet_acceleration = derivative_func(G, sun_position, sun_velocity, planet_position, planet_velocity, m_sun, m_planet)

    k1 = (sun_velocity, planet_velocity, sun_acceleration, planet_acceleration)

    #k2
    midpoint_state = tuple(
        y + (dt/2)*k
        for y, k in zip(state, k1)
    )

    sun_position, planet_position, sun_velocity, planet_velocity = midpoint_state

    sun_velocity, planet_velocity, sun_acceleration, planet_acceleration = derivative_func(G, sun_position, sun_velocity, planet_position, planet_velocity, m_sun, m_planet)

    k2 = (sun_velocity, planet_velocity, sun_acceleration, planet_acceleration)

    #k3
    midpoint_state = tuple(
        y + (dt/2)*k
        for y, k in zip(state, k2)
    )

    sun_position, planet_position, sun_velocity, planet_velocity = midpoint_state
    
    sun_velocity, planet_velocity, sun_acceleration, planet_acceleration = derivative_func(G, sun_position, sun_velocity, planet_position, planet_velocity, m_sun, m_planet)
    
    k3 = (sun_velocity, planet_velocity, sun_acceleration, planet_acceleration)

    #k4
    end_state = tuple(
        y + dt*k
        for y, k in zip(state, k3)
    )

    sun_position, planet_position, sun_velocity, planet_velocity = end_state
        
    sun_velocity, planet_velocity, sun_acceleration, planet_acceleration = derivative_func(G, sun_position, sun_velocity, planet_position, planet_velocity, m_sun, m_planet)
        
    k4 = (sun_velocity, planet_velocity, sun_acceleration, planet_acceleration)


    new_state = tuple(
        y + (dt/6)*(a+2*b+2*c+d)
        for y, a, b, c, d in zip(state, k1, k2, k3, k4)
    )

    return new_state