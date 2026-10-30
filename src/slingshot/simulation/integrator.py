def update_velocity(acceleration, velocity, dt):
    velocity = velocity + acceleration*dt

    return velocity

def update_position(velocity, position, dt):
    position = position + velocity*dt

    return position