import numpy as np
from slingshot.physics.gravity import calculate_accelerations
def test_gravitational_acceleration():
    sun_position = np.array([0.0, 0.0, 0.0])
    planet_position = np.array([5.0, 0.0, 0.0])

    planet_acceleration, sun_acceleration = calculate_accelerations(
        1, 10, 3, sun_position, planet_position
    )

    expected_planet_acceleration = np.array([-0.4, 0.0, 0.0])

    assert np.allclose(planet_acceleration, expected_planet_acceleration)