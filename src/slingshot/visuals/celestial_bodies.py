import numpy as np
from PIL import Image
from ursina import Entity, PointLight, Texture, color


def _fbm(w, h, octaves=6, seed=0):
    """Fractal noise in [0, 1], wraps horizontally so sphere UVs have no seam."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w))
    amp, total = 1.0, 0.0
    for o in range(octaves):
        n = 2 ** (o + 2)
        grid = rng.random((n, n + 1))
        grid[:, -1] = grid[:, 0]
        layer = Image.fromarray((grid * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += amp * np.asarray(layer) / 255
        total += amp
        amp *= 0.5
    out /= total
    return (out - out.min()) / (out.max() - out.min())


def _tex(arr):
    return Texture(Image.fromarray(arr.astype(np.uint8)))


def _glow_texture(rgb, size=256, power=2.5):
    y, x = np.mgrid[-1:1:size * 1j, -1:1:size * 1j]
    r = np.clip(np.sqrt(x * x + y * y), 0, 1)
    img = np.zeros((size, size, 4))
    img[..., :3] = rgb
    img[..., 3] = 255 * (1 - r) ** power
    return _tex(img)


def _glow(parent, rgb, scale, power=2.5):
    return Entity(parent=parent, model='quad', texture=_glow_texture(rgb, power=power),
                  billboard=True, scale=scale, unlit=True)


def create_sun():
    w, h = 1024, 512
    n = _fbm(w, h, octaves=7, seed=3)
    img = np.zeros((h, w, 3))
    img[..., 0] = 255
    img[..., 1] = 110 + 145 * n
    img[..., 2] = 10 + 70 * n ** 2
    sun = Entity(model='sphere', texture=_tex(img), scale=2, unlit=True)

    _glow(sun, (255, 170, 60), scale=3.2, power=2.0)
    _glow(sun, (255, 120, 30), scale=6.0, power=3.0)
    PointLight(parent=sun, color=color.rgb32(255, 230, 190))
    return sun


def create_planet():
    w, h = 1024, 512
    height = _fbm(w, h, octaves=6, seed=7)
    lat = np.abs(np.linspace(-1, 1, h))[:, None] * np.ones((1, w))

    img = np.zeros((h, w, 3))
    sea = 0.52
    ocean = height < sea
    depth = height / sea
    img[ocean] = np.stack([10 + 30 * depth, 40 + 80 * depth, 110 + 100 * depth], -1)[ocean]

    elev = np.clip((height - sea) / (1 - sea), 0, 1)
    land = np.stack([40 + 130 * elev, 110 + 20 * elev - 50 * elev ** 2, 40 + 70 * elev], -1)
    img[~ocean] = land[~ocean]

    ice = (lat + (height - 0.5) * 0.25) > 0.85
    img[ice] = 240

    planet = Entity(model='sphere', texture=_tex(img), scale=1)

    c = _fbm(w, h, octaves=6, seed=21)
    c = np.clip((c - 0.5) * 3.0, 0, 1)
    clouds = np.zeros((h, w, 4))
    clouds[..., :3] = 255
    clouds[..., 3] = c * 200
    planet.clouds = Entity(parent=planet, model='sphere', texture=_tex(clouds),
                           scale=1.03, unlit=True)

    _glow(planet, (90, 160, 255), scale=1.6, power=4.0)  # atmosphere halo
    return planet


def create_probe(probe_position):
    probe = Entity(model='sphere', color=color.white, scale=0.3,
                   position=probe_position, unlit=True)
    _glow(probe, (255, 255, 255), scale=2.5, power=3.0)
    return probe