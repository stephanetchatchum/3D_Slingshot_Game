from ursina import Entity, Mesh, color

MAX_POINTS = 4000   # old points are dropped, so trails never slow the app down


def create_trail(trail_color, thickness=2):
    return Entity(
        model=Mesh(vertices=[], mode='line', thickness=thickness),
        color=trail_color,
        unlit=True,
    )


def update_trail(trail, path):
    """Draw `path`, fading from transparent (old) to opaque (new)."""
    del path[:-MAX_POINTS]
    n = len(path)
    if n < 2:
        return
    trail.model.vertices = path
    trail.model.colors = [color.rgba(1, 1, 1, (i / n) ** 1.5) for i in range(n)]
    trail.model.generate()