def rk4_step(state, dt, derivative_func, *args):
    #k1
    k1 = derivative_func(state, *args)

    #k2
    midpoint_state = tuple(
        y + (dt/2)*k
        for y, k in zip(state, k1)
    )

    k2 = derivative_func(midpoint_state, *args)

    #k3
    midpoint_state = tuple(
        y + (dt/2)*k
        for y, k in zip(state, k2)
    )

    
    k3 = derivative_func(midpoint_state, *args)

    #k4
    end_state = tuple(
        y + dt*k
        for y, k in zip(state, k3)
    )
        
    k4 = derivative_func(end_state, *args)

    new_state = tuple(
        y + (dt/6)*(a+2*b+2*c+d)
        for y, a, b, c, d in zip(state, k1, k2, k3, k4)
    )

    return new_state