from ursina import Button, Entity, Text, camera, color
from ursina.prefabs.slider import Slider

PANEL_COLOR = color.rgba(8 / 255, 12 / 255, 28 / 255, 0.78)
ACCENT = color.rgb32(120, 200, 255)


class Dashboard(Entity):
    """Left panel: controls. Right panel: results. Only draws; never touches the physics."""

    def __init__(self, defaults, on_reset, on_toggle_pause):
        super().__init__(parent=camera.ui)

        # ---------- controls panel (left) ----------
        Entity(parent=self, model='quad', color=PANEL_COLOR, scale=(0.34, 0.50),
               position=(-0.58, 0.18), z=1)
        Text(parent=self, text='SIMULATION CONTROLS', position=(-0.73, 0.425),
             scale=0.9, color=ACCENT)

        self.sliders = {}
        rows = [
            ('planet_mass', 'Planet mass m', 0.5, 12),
            ('G', 'Gravitational constant G', 0.2, 3),
            ('probe_speed', 'Probe speed v', 0.0, 6),
            ('time_scale', 'Time scale (live)', 0.1, 5),
        ]
        y = 0.32
        for key, label, lo, hi in rows:
            slider = Slider(lo, hi, default=defaults[key], text=label, dynamic=True,
                            parent=self, position=(-0.72, y), scale=0.62)
            slider.label.origin = (-0.5, 0)      # left-aligned, above the bar
            slider.label.position = (0, 0.065)
            slider.label.scale = 1.25
            self.sliders[key] = slider
            y -= 0.075

        self.pause_button = Button(text='Pause (Space)', parent=self, scale=(0.155, 0.045),
                                   position=(-0.65, -0.02), color=color.rgb32(30, 60, 110))
        self.pause_button.on_click = on_toggle_pause
        self.reset_button = Button(text='Reset (R)', parent=self, scale=(0.155, 0.045),
                                   position=(-0.49, -0.02), color=color.rgb32(110, 50, 40))
        self.reset_button.on_click = on_reset
        Text(parent=self, text='Mass, G and speed apply on Reset.', position=(-0.73, -0.065),
             scale=0.6, color=color.rgba(1, 1, 1, 0.6))

        Text(parent=self, text='H hide panels  |  C camera  |  Space pause  |  R reset',
             position=(-0.73, -0.095), scale=0.55, color=color.rgba(1, 1, 1, 0.6))

        # ---------- results panel (right) ----------
        Entity(parent=self, model='quad', color=PANEL_COLOR, scale=(0.36, 0.30),
               position=(0.58, 0.31), z=1)
        Text(parent=self, text='RESULTS', position=(0.42, 0.45), scale=0.9, color=ACCENT)
        self.results_text = Text(parent=self, text='', position=(0.42, 0.40), scale=0.8,
                                 line_height=1.4)

    def value(self, key):
        return self.sliders[key].value

    def set_visible(self, visible):
        self.enabled = visible

    def set_paused(self, paused):
        self.pause_button.text = 'Resume (Space)' if paused else 'Pause (Space)'

    def show_results(self, r):
        self.results_text.text = (
            f'Simulation time:      {r["time"]:.1f}\n'
            f'Probe speed (vs Sun): {r["probe_speed"]:.2f}\n'
            f'Distance to planet:   {r["distance"]:.2f}\n'
            f'Closest approach:     {r["closest"]:.2f}\n'
            f'Speed change at flyby: pending'
        )