from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # Palette
        PRIMARY = "#FF6B35"
        SECONDARY = "#3D5A80"
        ACCENT = "#FFD166"
        BG = "#0E1116"
        WHITE_GLOW = "#FFE9C9"

        self.camera.background_color = BG

        # ---------------------------------------------------------------- HOOK
        # BEAT A1.B1 | 0.00-4.00 s
        # A solid black furnace body fades in and its circular mouth begins to
        # glow deep orange, as if heating up.

        furnace_body = RoundedRectangle(
            width=2.6, height=3.2, corner_radius=0.15,
            fill_color="#1A1A1F", fill_opacity=1.0,
            stroke_color="#2A2A30", stroke_width=2,
        ).move_to(LEFT * 4.0 + DOWN * 0.2)

        aperture_rim = Circle(radius=0.55, color="#2A2A30",
                              stroke_width=3, fill_opacity=0).move_to(
            furnace_body.get_center() + UP * 0.4)

        glow_tracker = ValueTracker(0.0)

        def make_aperture():
            t = glow_tracker.get_value()
            return Circle(
                radius=0.5,
                color=interpolate_color(
                    ManimColor("#5A1100"),
                    ManimColor("#FFB070"),
                    t),
                fill_opacity=0.65 + 0.35 * t,
                stroke_opacity=0.0,
            ).move_to(aperture_rim.get_center())

        aperture = always_redraw(make_aperture)

        kicker = Text("Blackbody radiation", color=ACCENT,
                      font_size=27).next_to(furnace_body, DOWN, buff=0.25)

        self.play(FadeIn(furnace_body, shift=RIGHT * 0.2),
                  FadeIn(aperture_rim), run_time=0.9)
        self.add(aperture)
        self.play(glow_tracker.animate.set_value(1.0),
                  FadeIn(kicker, shift=UP * 0.15), run_time=2.6,
                  rate_func=smooth)
        self.wait(0.5)

        # ---------------------------------------------------------- ESTABLISH
        # BEAT A2.B1 | 4.00-10.00 s
        # White light emerges from the aperture, hits a glass prism at center,
        # and fans out into a visible spectrum strip painted across the right
        # wall.

        light_ray = Line(aperture.get_center(),
                         aperture.get_center() + RIGHT * 3.4,
                         stroke_width=5, color=WHITE_GLOW)

        prism = Polygon(
            np.array([0.0, 0.45, 0.0]),
            np.array([-0.45, -0.3, 0.0]),
            np.array([0.45, -0.3, 0.0]),
            fill_color="#B7C7D9", fill_opacity=0.55,
            stroke_color="#E2E8F0", stroke_width=1.5,
        ).move_to(aperture.get_center() + RIGHT * 3.4 + UP * 0.3)

        # Rainbow fan: seven colored bars that emerge from the prism.
        band_colors = [
            "#7A1F8B",  # violet
            "#3F51B5",  # blue
            "#1FA9DC",   # teal-blue
            "#22C55E",  # green
            "#FACC15",  # yellow
            "#F97316",  # orange
            "#DC2626",  # red
        ]
        band_origin = prism.get_right() + RIGHT * 0.05 + DOWN * 0.05
        bands = VGroup()
        for i, c in enumerate(band_colors):
            angle = -math.radians(28) + i * math.radians(56 / 6)
            end = band_origin + RIGHT * 3.6 * np.array(
                [math.cos(angle), math.sin(angle), 0])
            bands.add(Line(band_origin, end,
                           stroke_width=8, color=c,
                           stroke_opacity=0.9))

        spectrum_caption = Text("Visible Spectrum", color=ACCENT,
                               font_size=30).move_to(RIGHT * 3.6 + UP * 1.7)

        self.play(Create(light_ray), run_time=0.6)
        self.play(FadeIn(prism, scale=0.9), run_time=0.6)
        self.play(LaggedStart(*[Create(b) for b in bands],
                              lag_ratio=0.08),
                  FadeIn(spectrum_caption, shift=UP * 0.2),
                  run_time=3.6)
        self.wait(1.2)

        # ------------------------------------------------------------- EVOLVE
        # BEAT A3.B1 | 10.00-15.00 s
        # A line graph fades in: the classical Rayleigh-Jeans curve rises and
        # then spikes sharply toward the ultraviolet end of the wavelength
        # axis, labeled with axes and units.

        axes = Axes(
            x_range=[0.2, 4.0, 1.0],
            y_range=[0, 12, 3],
            x_length=6.2, y_length=3.2,
            axis_config={"stroke_color": "#5B6B82",
                         "include_tip": False,
                         "stroke_width": 1.5},
            tips=False,
        ).to_edge(RIGHT, buff=1.45).shift(DOWN * 0.2)

        x_label = Text("Wavelength (um)", color="#9AA7B8",
                       font_size=22).next_to(axes.x_axis, DOWN, buff=0.15)
        y_label = Text("Relative radiance", color="#9AA7B8",
                       font_size=22).rotate(90 * DEGREES).next_to(
                           axes.y_axis, LEFT, buff=0.16)

        # Rayleigh-Jeans ~ 2*c*k*T / lambda^4, scaled for visualization.
        T = 5800.0
        rj = axes.plot(
            lambda x: min(11.5, 18.0 / (x ** 4)),
            x_range=[0.32, 3.6], color=SECONDARY, stroke_width=4,
        )
        classical_label = Text("Rayleigh-Jeans model",
                               color=SECONDARY, font_size=22).next_to(
            axes, UP, buff=0.2).align_to(axes, LEFT)

        self.play(FadeOut(light_ray), FadeOut(prism),
                  FadeOut(bands), FadeOut(spectrum_caption),
                  run_time=0.4)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label),
                  run_time=1.0)
        self.play(Create(rj), FadeIn(classical_label, shift=DOWN * 0.1),
                  run_time=2.4)
        self.wait(1.2)

        # BEAT A3.B2 | 15.00-19.00 s
        # A live readout near the curve displays the temperature 5800 K and
        # the divergence climbs without bound as wavelength shrinks.

        temp_tracker = ValueTracker(5800.0)
        temp_value = DecimalNumber(
            temp_tracker.get_value(), num_decimal_places=0,
            color=ACCENT, font_size=24,
        )
        temp_value.add_updater(lambda mob: mob.set_value(temp_tracker.get_value()))
        readout = VGroup(
            Text("T =", color=ACCENT, font_size=24),
            temp_value,
            Text("K", color=ACCENT, font_size=24),
        ).arrange(RIGHT, buff=0.08).next_to(
            axes, UP, buff=0.2).align_to(axes, RIGHT)

        # Start on the long-wavelength side so the marker visibly climbs as
        # it sweeps toward shorter wavelengths and the classical divergence.
        uv_x = ValueTracker(2.0)
        uv_marker = always_redraw(lambda: Dot(
            axes.c2p(
                uv_x.get_value(),
                min(11.5, 18.0 / (uv_x.get_value() ** 4)),
            ),
            color=PRIMARY, radius=0.09))

        catastrophe = Text("UV catastrophe", color=PRIMARY,
                           font_size=22).move_to(axes.c2p(2.8, 9.4))

        self.play(FadeIn(readout), FadeIn(catastrophe, shift=UP * 0.15),
                  run_time=0.9)
        self.add(uv_marker)
        # The classical curve "climbs without bound": the marker rides the
        # runaway tail while the displayed value climbs.
        self.play(temp_tracker.animate.set_value(5800.0),
                  uv_x.animate.set_value(0.32),
                  run_time=2.4, rate_func=smooth)
        self.wait(0.7)

        # ------------------------------------------------------------ REVEAL
        # BEAT A4.B1 | 19.00-26.00 s
        # The wild classical curve is wiped; Planck's distribution draws in
        # smoothly, peaking in the visible band and decaying to zero in the
        # ultraviolet — the measured spectrum.

        # Planck spectral radiance (arbitrary units) for the same T.
        # B ~ x^{-5} / (exp(C2/(T*x)) - 1)
        def planck(x):
            C2 = 14388.0  # micrometer·kelvin
            x = np.asarray(x)
            with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
                arg = np.where(C2 / (T * x) > 700, 700.0, C2 / (T * x))
                val = (x ** -5) / (np.exp(arg) - 1.0)
            return val

        xs = np.linspace(0.32, 3.6, 400)
        ys = planck(xs)
        peak = float(np.max(ys))
        scale = 10.0 / peak

        planck_curve = axes.plot(
            lambda x: float(planck(np.array([x]))[0] * scale),
            x_range=[0.32, 3.6], color=PRIMARY, stroke_width=4,
        )
        planck_label = Text("Planck spectrum", color=PRIMARY,
                            font_size=22).next_to(axes, UP, buff=0.2) \
            .align_to(axes, LEFT)

        # Wipe the wild curve and reveal the finite one.
        self.play(FadeOut(rj, run_time=0.3),
                  FadeOut(classical_label, run_time=0.3),
                  FadeOut(uv_marker, run_time=0.3),
                  FadeOut(catastrophe, run_time=0.3),
                  run_time=0.6)
        self.play(Create(planck_curve), FadeIn(planck_label,
                                               shift=DOWN * 0.1),
                  run_time=4.8, rate_func=smooth)
        # Subtle highlight tick where the peak lives (visible band).
        peak_x = float(xs[np.argmax(ys)])
        peak_tick = DashedLine(
            axes.c2p(peak_x, 0), axes.c2p(peak_x, 11.0),
            color=ACCENT, stroke_width=2, dash_length=0.08,
        )
        peak_anno = Text("visible peak", color=ACCENT, font_size=24) \
            .next_to(peak_tick, UP, buff=0.1)
        self.play(Create(peak_tick), FadeIn(peak_anno), run_time=1.0)
        self.wait(0.6)

        # ------------------------------------------------------------- RECAP
        # BEAT A5.B1 | 26.00-30.00 s
        # The hero composition holds: glowing furnace, fanned spectrum, and
        # the finite Planck curve annotated with E = h·ν, as a small loop
        # breathes in the furnace glow.

        # Bring furnace and rainbow back for the hero frame.
        hero_label = MathTex(r"E \;=\; h\,\nu",
                             color=ACCENT, font_size=44)
        hero_label.set_color_by_tex("h", ACCENT)
        hero_label.move_to(axes.get_bottom() + DOWN * 1.05)

        self.play(FadeIn(hero_label, shift=RIGHT * 0.15),
                  run_time=0.6)

        # Breathing pulse for the furnace aperture (idle loop).
        breath = ValueTracker(0.0)

        def breathing_color():
            t = breath.get_value()
            return interpolate_color(
                ManimColor("#5A1100"),
                ManimColor("#FFB070"),
                0.55 + 0.45 * math.sin(t))

        aperture.add_updater(lambda m: m.set_color(breathing_color()))

        self.play(breath.animate.set_value(2 * math.pi),
                  run_time=3.0, rate_func=linear)
        self.wait(0.4)
