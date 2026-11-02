import numpy as np
from slingshot.physics.gravity import calculate_accelerations, calculate_probe_acceleration

def test_gravitational_acceleration():
    sun_position = np.array([0.0, 0.0, 0.0])
    planet_position = np.array([5.0, 0.0, 0.0])

    planet_acceleration, sun_acceleration = calculate_accelerations(
        1, 10, 3, sun_position, planet_position
    )

    expected_planet_acceleration = np.array([-0.4, 0.0, 0.0])

    assert np.allclose(planet_acceleration, expected_planet_acceleration)

def test_gravitational_forces_are_equal_and_opposite():
    sun_position = np.array([0.0, 0.0, 0.0])
    planet_position = np.array([5.0, 0.0, 0.0])

    planet_acceleration, sun_acceleration = calculate_accelerations(
        1, 10, 3, sun_position, planet_position
    )

    planet_force = 3*planet_acceleration
    sun_force = 10*sun_acceleration

    assert np.allclose(planet_force, -sun_force)

def test_probe_acceleration():
    sun_position = np.array([0.0, 0.0, 0.0])
    planet_position = np.array([5.0, 0.0, 0.0])
    probe_position = np.array([2.0, 0.0, 0.0])

    acceleration = calculate_probe_acceleration(1, 10, 3, sun_position, planet_position, probe_position)

    expected = np.array([-2.1666666667, 0.0, 0.0])

    assert np.allclose(acceleration, expected)
