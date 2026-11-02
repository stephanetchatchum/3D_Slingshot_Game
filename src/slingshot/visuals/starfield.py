import random
from ursina import Entity, Mesh, Vec3, color


def create_starfield(count=1500, radius=400, seed=1):
    """Random points on a big sphere around the scene = a starry sky."""
    rng = random.Random(seed)
    points = []
    while len(points) < count:
        v = Vec3(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
        if 0.01 < v.length() <= 1:                   # keep points inside the unit ball,
            points.append(v.normalized() * radius)   # then push them onto the sphere
    return Entity(
        model=Mesh(vertices=points, mode='point', thickness=2),
        color=color.white,
        unlit=True,
    )