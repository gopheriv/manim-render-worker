from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # Shared physics helpers (normalized units)
        def planck_norm(x):
            if x <= 0:
                return 0.0
            return (x**3) / (math.exp(x) - 1) * 0.703

        def rayleigh_jeans_norm(x):
            return 0.409 * x**2

        # ===== HOOK: Bar heats to 5800 K =====
        # BEAT A1.B1 | 0.00-5.00 s
        title = Text("Blackbody Spectrum", font_size=36, color=WHITE).to_edge(UP, buff=0.25)

        bar = Rectangle(width=0.5, height=2.4, fill_opacity=1, color=BLACK, stroke_width=1)
        bar.move_to(LEFT * 5.2 + DOWN * 0.2)
        bar_label = Text("Tungsten bar", font_size=22, color=WHITE).next_to(bar, DOWN, buff=0.15)

        T_tracker = ValueTracker(0)
        T_readout = DecimalNumber(0, num_decimal_places=0, font_size=36, color=WHITE)
        T_readout.next_to(bar, UP, buff=0.4)
        T_unit = Text("K", font_size=28, color=WHITE).next_to(T_readout, RIGHT, buff=0.05)

        heat_colors = [MAROON, RED, ORANGE, YELLOW, WHITE]

        def get_bar_color():
            t = min(max(T_tracker.get_value() / 5800.0, 0), 1)
            idx_f = t * (len(heat_colors) - 1)
            idx = int(idx_f)
            if idx >= len(heat_colors) - 1:
                return heat_colors[-1]
            frac = idx_f - idx
            return interpolate_color(heat_colors[idx], heat_colors[idx + 1], frac)

        bar.add_updater(lambda m: m.set_fill(get_bar_color(), opacity=1))
        T_readout.add_updater(lambda m: m.set_value(T_tracker.get_value()))

        self.add(title, bar, T_readout, T_unit, bar_label)
        self.play(T_tracker.animate.set_value(5800), run_time=4.5, rate_func=linear)
        self.wait(0.5)

        # ===== ESTABLISH: Prism and measured spectrum =====
        # BEAT A2.B1 | 5.00-11.00 s
        prism = Polygon(
            np.array([0, -0.6, 0]),
            np.array([0.5, 0.5, 0]),
            np.array([-0.5, 0.5, 0]),
            color=WHITE, fill_opacity=0.2, stroke_color=WHITE, stroke_width=2
        ).move_to(LEFT * 2 + DOWN * 0.2)

        rainbow_bands = VGroup()
        rainbow_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for i, col in enumerate(rainbow_colors):
            band = Line(
                prism.get_right() + RIGHT * 0.05,
                prism.get_right() + RIGHT * 1.5 + UP * (i - 2.5) * 0.12,
                color=col, stroke_width=3
            )
            rainbow_bands.add(band)

        axes = Axes(
            x_range=[0, 3.2, 1],
            y_range=[0, 1.3, 0.5],
            x_length=5.0,
            y_length=3.8,
            tips=False,
            axis_config={"stroke_width": 2, "color": GRAY}
        ).move_to(RIGHT * 2.3 + DOWN * 0.2)

        x_label = MathTex(r"\nu", font_size=30, color=WHITE).next_to(axes.x_axis, RIGHT, buff=0.15)
        y_label = MathTex(r"B_\nu", font_size=30, color=WHITE).next_to(axes.y_axis, UP, buff=0.1)

        measured_curve = axes.plot(planck_norm, color=ORANGE, stroke_width=4)

        beam = Line(bar.get_right(), prism.get_left(), color=YELLOW, stroke_width=2, stroke_opacity=0.6)

        self.play(
            FadeIn(prism, scale=0.8),
            Create(beam),
            run_time=0.6
        )
        self.play(
            LaggedStart(*[Create(b) for b in rainbow_bands], lag_ratio=0.05),
            run_time=0.5
        )
        self.play(
            Create(axes),
            Write(x_label), Write(y_label),
            run_time=1.0
        )
        self.play(Create(measured_curve), run_time=2.0)
        self.wait(1.9)

        # ===== EVOLVE: Rayleigh-Jeans catastrophe =====
        # BEAT A3.B1 | 11.00-15.00 s
        rj_curve = DashedVMobject(
            axes.plot(rayleigh_jeans_norm, color=BLUE, stroke_width=3),
            num_dashes=40
        )
        rj_eq = MathTex(r"B_{\nu}=\frac{2\nu^{2}kT}{c^{2}}", font_size=28, color=BLUE)
        rj_eq.next_to(axes, UP, buff=0.2)

        self.play(Create(rj_curve), Write(rj_eq), run_time=2.5)
        self.wait(1.5)

        # BEAT A3.B2 | 15.00-19.00 s
        uv_label = Text("ULTRAVIOLET CATASTROPHE", font_size=24, color=BLUE, weight=BOLD)
        uv_label.move_to(axes.c2p(2.5, 1.25))
        arrow = Arrow(
            axes.c2p(2.3, 0.9),
            axes.c2p(2.3, 1.2),
            color=BLUE,
            stroke_width=4,
            buff=0
        )

        self.play(Create(arrow), Write(uv_label), run_time=2.0)
        self.wait(2.0)

        # ===== REVEAL: Planck equation and fade R-J =====
        # BEAT A4.B1 | 19.00-23.00 s
        data_points = VGroup()
        for x_val in np.linspace(0.4, 2.8, 8):
            y_val = planck_norm(x_val)
            pt = Dot(axes.c2p(x_val, y_val), color=WHITE, radius=0.05)
            data_points.add(pt)

        planck_eq = MathTex(
            r"B_{\nu}=\frac{2h\nu^{3}}{c^{2}}\,\frac{1}{e^{h\nu/kT}-1}",
            font_size=28,
            color=ORANGE
        )
        planck_eq_box = SurroundingRectangle(planck_eq, color=WHITE, buff=0.15, stroke_width=1.5)
        planck_eq_group = VGroup(planck_eq, planck_eq_box)
        planck_eq_group.to_edge(LEFT, buff=0.4).shift(DOWN * 1.8)

        self.play(
            FadeIn(data_points),
            Write(planck_eq),
            Create(planck_eq_box),
            run_time=2.5
        )
        self.wait(1.5)

        # BEAT A4.B2 | 23.00-26.00 s
        h_annot = MathTex(r"h = 6.626 \times 10^{-34}\text{ J·s}", font_size=22, color=YELLOW)
        h_annot.next_to(planck_eq_group, DOWN, buff=0.25)

        self.play(
            rj_curve.animate.set_opacity(0.2),
            FadeIn(h_annot, shift=UP * 0.2),
            run_time=2.0
        )
        self.wait(1.0)

        # ===== RECAP: Final comparison =====
        # BEAT A5.B1 | 26.00-30.00 s

        bar.clear_updaters()
        T_readout.clear_updaters()

        flicker_t = ValueTracker(0)

        def flicker_val():
            return 5800 + int(2 * math.sin(flicker_t.get_value() * 3))

        T_readout.add_updater(lambda m: m.set_value(flicker_val()))

        planck_eq_group.move_to(UP * 3.2)

        T_stamp = Text("T = 5800 K", font_size=30, color=YELLOW, weight=BOLD)
        T_stamp.next_to(planck_eq_group, RIGHT, buff=0.5)

        E_eq = MathTex(r"E = n h \nu", font_size=44, color=WHITE)
        E_eq.to_edge(DOWN, buff=0.4)
        E_note = Text("n is an integer", font_size=22, color=GRAY).next_to(E_eq, RIGHT, buff=0.2)

        graph_group = VGroup(axes, x_label, y_label, measured_curve, rj_curve, data_points)

        self.play(
            FadeOut(prism),
            FadeOut(rainbow_bands),
            FadeOut(beam),
            FadeOut(bar_label),
            FadeOut(uv_label),
            FadeOut(arrow),
            FadeOut(rj_eq),
            FadeOut(h_annot),
            run_time=1.0
        )
        self.play(
            graph_group.animate.move_to(ORIGIN + DOWN * 0.2),
            FadeIn(planck_eq_group),
            Write(T_stamp),
            Write(E_eq),
            Write(E_note),
            run_time=1.5
        )
        self.play(measured_curve.animate.set_stroke(width=5.5), run_time=0.75)
        self.play(measured_curve.animate.set_stroke(width=3.5), run_time=0.75)