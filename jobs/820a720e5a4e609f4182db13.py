from manim import *
import numpy as np

# Constants
b_Wien = 0.002897771955
c = 299792458.0
h = 6.62607015e-34
k_B = 1.380649e-23


class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = "#0A0E1A"

        PRIMARY = "#FFB347"
        SECONDARY = "#7FDBFF"
        ACCENT = "#FFD27F"
        DIM_GRAY = "#5A5A5A"

        # ---------------- HOOK ----------------
        # BEAT A1.B1 | 0.00-2.00 s
        filament = Line(UP * 1.5, DOWN * 1.5, color=PRIMARY, stroke_width=4)
        filament.move_to(np.array([0.0, 0.0, 0.0]))
        post_left = Line(UP * 1.8, DOWN * 1.8, color=GRAY, stroke_width=3).move_to(np.array([-0.4, 0.0, 0.0]))
        post_right = Line(UP * 1.8, DOWN * 1.8, color=GRAY, stroke_width=3).move_to(np.array([0.4, 0.0, 0.0]))
        filament.set_opacity(0.5)
        filament_g = VGroup(post_left, filament, post_right)
        self.play(FadeIn(filament_g, run_time=0.5), run_time=0.6)
        self.play(filament.animate.set_opacity(0.9), run_time=0.8)
        self.wait(0.6)

        # BEAT A1.B2 | 2.00-3.80 s
        spark = Dot(color=SECONDARY, radius=0.12).move_to(np.array([0.0, 0.6, 0.0]))
        spark2 = Dot(color=SECONDARY, radius=0.1).move_to(np.array([0.0, -0.4, 0.0]))
        self.play(FadeIn(spark, scale=0.5), FadeIn(spark2, scale=0.5), filament.animate.set_color("#FFE4B5").set_opacity(1.0), run_time=0.6)
        self.play(FadeOut(spark), FadeOut(spark2), run_time=0.4)
        self.wait(0.5)

        # BEAT A1.B3 | 3.80-5.50 s
        t_tracker = ValueTracker(3000)
        t_readout = DecimalNumber(3000, num_decimal_places=0, color=ACCENT).scale(0.5)
        t_readout.next_to(filament, DOWN, buff=0.5)
        t_readout.add_updater(lambda m: m.set_value(t_tracker.get_value()))
        t_label = Text("T", color=ACCENT).scale(0.4).next_to(t_readout, LEFT, buff=0.1)
        t_unit = Text("K", color=ACCENT).scale(0.4).next_to(t_readout, RIGHT, buff=0.1)
        self.play(FadeIn(VGroup(t_label, t_readout, t_unit), shift=UP * 0.2), run_time=0.5)
        self.play(t_tracker.animate.set_value(3050), run_time=0.4)
        self.wait(0.5)

        # ---------------- ESTABLISH ----------------
        # BEAT A2.B1 | 5.50-8.10 s
        axes = Axes(
            x_range=[0, 3.0, 0.5],
            y_range=[0, 5, 1],
            x_length=4.0,
            y_length=3.5,
            axis_config={"color": GRAY, "stroke_opacity": 0.5},
            tips=False,
        )
        axes.move_to(np.array([-3.2, -0.3, 0.0]))
        x_label = Text("wavelength λ (μm)", color=GRAY, font_size=20).next_to(axes.x_axis, DOWN, buff=0.15)
        y_label = Text("spectral radiance", color=GRAY, font_size=20).next_to(axes.y_axis, LEFT, buff=0.15).rotate(90 * DEGREES)
        plot_frame = VGroup(axes, x_label, y_label)

        def rj_curve(lam):
            T_val = t_tracker.get_value()
            return 0.8 * (0.3 / (lam + 0.05))

        rj = always_redraw(lambda: axes.plot(
            lambda lam: 0.8 * (0.3 / (lam + 0.05)),
            x_range=[0.05, 2.5],
            color=SECONDARY,
            stroke_width=2.5,
        ))
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.7)
        self.play(Create(rj), run_time=1.0)
        self.wait(0.9)

        # BEAT A2.B2 | 8.10-9.70 s
        uv_tag = Text("ultraviolet catastrophe", color=PRIMARY, font_size=22).move_to(np.array([-5.0, 2.0, 0.0]))
        uv_arrow = Arrow(uv_tag.get_right(), np.array([-3.8, 1.2, 0.0]), color=PRIMARY, buff=0.1, stroke_width=2)
        self.play(FadeIn(uv_tag, shift=RIGHT * 0.2), Create(uv_arrow), run_time=0.5)
        self.wait(0.8)

        # BEAT A2.B3 | 9.70-11.50 s
        dim_filament = filament.copy().set_color(DIM_GRAY).set_opacity(0.4)
        self.play(
            filament.animate.set_color(DIM_GRAY).set_opacity(0.4),
            t_readout.animate.set_opacity(0.3),
            t_label.animate.set_opacity(0.3),
            t_unit.animate.set_opacity(0.3),
            run_time=0.6,
        )
        self.wait(0.9)

        # ---------------- EVOLVE ----------------
        # BEAT A3.B1 | 11.50-14.50 s
        def planck_curve(lam, T):
            if lam < 0.01:
                return 0
            exponent = (h * c) / (lam * 1e-6 * k_B * T)
            if exponent > 500:
                return 0
            B = (2 * h * c * c / (lam * 1e-6) ** 5) / (np.exp(exponent) - 1)
            return B * 1e14

        planck = always_redraw(lambda: axes.plot(
            lambda lam: min(planck_curve(lam, t_tracker.get_value()), 5),
            x_range=[0.05, 2.5],
            color=PRIMARY,
            stroke_width=3.5,
        ))
        self.play(Create(planck), run_time=1.5)
        self.wait(1.2)

        # BEAT A3.B2 | 14.50-17.00 s
        peak_dot = always_redraw(lambda: Dot(
            color=ACCENT,
            radius=0.1,
            point=axes.c2p(b_Wien * 1e6 / t_tracker.get_value(), min(planck_curve(b_Wien * 1e6 / t_tracker.get_value(), t_tracker.get_value()), 5)),
        ))
        guide_line = always_redraw(lambda: DashedLine(
            start=axes.c2p(b_Wien * 1e6 / t_tracker.get_value(), min(planck_curve(b_Wien * 1e6 / t_tracker.get_value(), t_tracker.get_value()), 5)),
            end=axes.c2p(b_Wien * 1e6 / t_tracker.get_value(), 0),
            color=ACCENT,
            stroke_width=2,
        ))
        peak_val = DecimalNumber(0.965, num_decimal_places=2, color=ACCENT).scale(0.45)
        peak_val.add_updater(lambda m: m.set_value(b_Wien * 1e6 / t_tracker.get_value()))
        peak_val.next_to(axes.x_axis, UP, buff=0.1).add_updater(lambda m: m.move_to(axes.c2p(b_Wien * 1e6 / t_tracker.get_value(), 0) + UP * 0.25))
        peak_label = Text("λ_peak =", color=ACCENT, font_size=22).next_to(peak_val, LEFT, buff=0.1).add_updater(lambda m: m.next_to(peak_val, LEFT, buff=0.1))
        b_wien_label = Text("b_Wien = 2.898e-3 m·K", color=GRAY, font_size=18).move_to(np.array([-3.2, 2.8, 0.0]))
        self.add(peak_dot, guide_line, peak_val, peak_label, b_wien_label)
        self.play(FadeIn(peak_dot), Create(guide_line), FadeIn(peak_val), FadeIn(peak_label), FadeIn(b_wien_label), run_time=0.7)
        self.wait(1.5)

        # BEAT A3.B3 | 17.00-19.00 s
        self.play(
            t_tracker.animate.set_value(4500),
            t_readout.animate.set_opacity(1.0),
            t_label.animate.set_opacity(1.0),
            t_unit.animate.set_opacity(1.0),
            filament.animate.set_color(PRIMARY).set_opacity(1.0),
            run_time=1.4,
        )
        self.wait(0.6)

        # ---------------- REVEAL ----------------
        # BEAT A4.B1 | 19.00-21.80 s
        new_axes = Axes(
            x_range=[0, 3.0, 0.5],
            y_range=[0, 5, 1],
            x_length=4.5,
            y_length=3.8,
            axis_config={"color": GRAY, "stroke_opacity": 0.5},
            tips=False,
        )
        new_axes.move_to(np.array([-3.0, -0.3, 0.0]))
        rj2 = new_axes.plot(
            lambda lam: 0.8 * (0.3 / (lam + 0.05)),
            x_range=[0.05, 2.5],
            color=SECONDARY,
            stroke_width=1.5,
            stroke_opacity=0.4,
        )
        planck2 = new_axes.plot(
            lambda lam: min(planck_curve(lam, t_tracker.get_value()), 5),
            x_range=[0.05, 2.5],
            color=PRIMARY,
            stroke_width=3.5,
        )
        peak_dot2 = Dot(
            color=ACCENT,
            radius=0.1,
            point=new_axes.c2p(b_Wien * 1e6 / t_tracker.get_value(), min(planck_curve(b_Wien * 1e6 / t_tracker.get_value(), t_tracker.get_value()), 5)),
        )
        x_label2 = Text("wavelength λ (μm)", color=GRAY, font_size=20).next_to(new_axes.x_axis, DOWN, buff=0.15)
        y_label2 = Text("spectral radiance", color=GRAY, font_size=20).next_to(new_axes.y_axis, LEFT, buff=0.15).rotate(90 * DEGREES)

        self.play(
            Transform(axes, new_axes),
            Transform(x_label, x_label2),
            Transform(y_label, y_label2),
            Transform(rj, rj2),
            Transform(planck, planck2),
            Transform(peak_dot, peak_dot2),
            FadeOut(guide_line),
            FadeOut(uv_tag),
            FadeOut(uv_arrow),
            FadeOut(peak_val),
            FadeOut(peak_label),
            FadeOut(b_wien_label),
            run_time=1.6,
        )
        self.wait(1.0)

        # BEAT A4.B2 | 21.80-24.00 s
        eq = MathTex(
            r"B_\nu(\nu,T) = \frac{2h\nu^3/c^2}{e^{h\nu/k_B T} - 1}",
            color=ACCENT,
        ).scale(0.7)
        eq.move_to(np.array([0.0, 2.8, 0.0]))
        h_const = Text("h = 6.626e-34 J·s", color=GRAY, font_size=18).move_to(np.array([5.0, -3.0, 0.0]))
        c_const = Text("c = 2.998e8 m/s", color=GRAY, font_size=18).move_to(np.array([5.0, -3.3, 0.0])).align_to(h_const, RIGHT)
        kb_const = Text("k_B = 1.381e-23 J/K", color=GRAY, font_size=18).move_to(np.array([5.0, -3.6, 0.0])).align_to(h_const, RIGHT)
        self.play(FadeIn(eq, shift=DOWN * 0.2), FadeIn(VGroup(h_const, c_const, kb_const)), run_time=0.8)
        self.wait(1.2)

        # BEAT A4.B3 | 24.00-25.50 s
        annotation = Text(
            "Quantization cures the ultraviolet catastrophe",
            color=SECONDARY,
            font_size=32,
        ).move_to(np.array([0.0, 3.4, 0.0]))
        self.play(
            filament.animate.set_color("#FFFFFF").set_opacity(1.0),
            FadeIn(annotation, shift=DOWN * 0.2),
            run_time=0.5,
        )
        self.play(peak_dot.animate.scale(1.4), run_time=0.2)
        self.play(peak_dot.animate.scale(1 / 1.4), run_time=0.2)
        self.wait(0.6)

        # ---------------- RECAP ----------------
        # BEAT A5.B1 | 25.50-27.30 s
        self.play(
            FadeOut(eq),
            FadeOut(h_const),
            FadeOut(c_const),
            FadeOut(kb_const),
            FadeOut(annotation),
            filament.animate.set_color(PRIMARY),
            run_time=1.0,
        )
        rj_label = Text("Rayleigh-Jeans diverges", color=SECONDARY, font_size=22).move_to(np.array([-4.0, 2.0, 0.0]))
        planck_label = Text("Planck stays finite", color=PRIMARY, font_size=22).move_to(np.array([-4.0, 1.5, 0.0]))
        self.play(FadeIn(rj_label), FadeIn(planck_label), run_time=0.4)
        self.wait(0.4)

        # BEAT A5.B2 | 27.30-29.00 s
        planck_4500 = axes.plot(
            lambda lam: min(planck_curve(lam, 4500), 5),
            x_range=[0.05, 2.5],
            color=PRIMARY,
            stroke_width=3.0,
        )
        planck_6000 = axes.plot(
            lambda lam: min(planck_curve(lam, 6000), 5),
            x_range=[0.05, 2.5],
            color="#FFA07A",
            stroke_width=3.0,
        )
        label_4500 = Text("λ_peak = 0.64 μm", color=PRIMARY, font_size=20).move_to(np.array([-3.0, 2.2, 0.0]))
        label_6000 = Text("λ_peak = 0.48 μm", color="#FFA07A", font_size=20).move_to(np.array([-3.0, 1.85, 0.0]))

        self.play(t_tracker.animate.set_value(6000), Create(planck_6000), FadeIn(label_4500), FadeIn(label_6000), run_time=0.9)
        self.wait(0.6)

        # BEAT A5.B3 | 29.00-30.00 s
        final_text = Text(
            "Thermal radiation: quantized, finite, beautiful.",
            color=ACCENT,
            font_size=28,
        ).move_to(np.array([0.0, 3.4, 0.0]))

        breath_tracker = ValueTracker(0.0)

        def update_filament(m):
            val = 0.95 + 0.05 * np.sin(breath_tracker.get_value())
            m.set_opacity(val)
            if breath_tracker.get_value() % (2 * np.pi) < np.pi:
                m.set_color(PRIMARY)
            else:
                m.set_color("#FFE4B5")

        filament.add_updater(update_filament)

        peak_pulse = always_redraw(lambda: Dot(
            color=ACCENT,
            radius=0.1 * (1.0 + 0.15 * np.sin(breath_tracker.get_value())),
            point=axes.c2p(b_Wien * 1e6 / t_tracker.get_value(), min(planck_curve(b_Wien * 1e6 / t_tracker.get_value(), t_tracker.get_value()), 5)),
        ))

        shimmer_line = always_redraw(lambda: axes.plot(
            lambda lam: min(planck_curve(lam, t_tracker.get_value()), 5) + 0.15 * np.sin(20 * lam - 5 * breath_tracker.get_value()),
            x_range=[0.05, 2.5],
            color=ACCENT,
            stroke_width=1.0,
            stroke_opacity=0.3,
        ))

        self.add(peak_pulse, shimmer_line)
        self.play(
            FadeIn(final_text, shift=DOWN * 0.2),
            FadeOut(rj_label),
            FadeOut(planck_label),
            FadeOut(label_4500),
            FadeOut(label_6000),
            run_time=0.5,
        )

        self.play(breath_tracker.animate.set_value(2 * np.pi * 5), run_time=2.0, rate_func=linear)

        self.wait(2.0)