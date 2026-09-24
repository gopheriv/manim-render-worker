from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
            # ============================================================
            # BEAT A1.B1 | 0.00-3.50 s — HOOK: A star's promise vs. a prediction's failure
            # ============================================================
            title = Text("Blackbody Spectrum", color="#F8FAFC").scale(0.5).to_edge(UP, buff=0.4)
            subtitle = Text("Planck vs. Rayleigh-Jeans", color="#22D3EE").scale(0.3)
            subtitle.next_to(title, DOWN, buff=0.15)
            self.play(Write(title), run_time=1.2)
            self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.6)
            self.wait(1.2)

            # ============================================================
            # BEAT A2.B1 | 3.50-13.00 s — ESTABLISH: the stage (axes) and the RJ curve
            # ============================================================
            # Build axes once — DO NOT rebuild inside updaters.
            T_val = 5800.0
            h = 6.626e-34
            c_light = 3e8
            k_B = 1.381e-23
            # Scale factor to keep things visible. We work in scaled frequency and energy units.
            # Use dimensionless units: x = h*nu / (k_B T); then Planck: x^3 / (e^x - 1)
            # We plot y(u) vs u where u = nu/nu_peak_approx, but simpler: just plot x in [0, 8].
            x_max = 8.0

            def planck_scaled(x):
                # x is dimensionless frequency: h*nu / (k_B T)
                x_safe = np.maximum(x, 1e-9)
                return (x_safe ** 3) / (np.exp(x_safe) - 1.0)

            def rayleigh_jeans_scaled(x):
                # Classical: u_RJ = k_B T * 8 pi nu^2 / c^3 -> in x-units: x^2
                return x ** 2

            axes = Axes(
                x_range=[0, x_max, 1],
                y_range=[0, 7.5, 2],
                x_length=8.0,
                y_length=3.4,
                tips=False,
                axis_config={"stroke_color": GREY_B, "stroke_width": 1.5},
            ).to_edge(DOWN, buff=0.55)
            x_lab = MathTex(r"x = \dfrac{h\nu}{k_B T}", color=GREY_B).scale(0.35)
            x_lab.next_to(axes.x_axis, RIGHT, buff=0.15)
            y_lab = MathTex(r"\dfrac{u(\nu)}{u_{max}}", color=GREY_B).scale(0.35)
            y_lab.next_to(axes.y_axis, UP, buff=0.1).shift(RIGHT * 0.05)

            # Rayleigh-Jeans curve: classical prediction (diverges as x^2)
            rj_curve = axes.plot(rayleigh_jeans_scaled, color=RED_C, x_range=[0.001, x_max, 200])
            rj_label = Text("Rayleigh-Jeans", color=RED_C).scale(0.28)
            rj_label.move_to(axes.c2p(6.5, 45)).shift(UP * 0.0)

            # Fade scaffolding first
            self.play(
                Create(axes, run_time=1.2, rate_func=smooth),
                FadeIn(x_lab, run_time=0.8),
                FadeIn(y_lab, run_time=0.8),
            )
            self.play(Create(rj_curve, run_time=3.2, rate_func=linear))
            self.play(FadeIn(rj_label, shift=LEFT * 0.1, run_time=0.6))
            self.wait(2.2)

            # Glow hint: thin bright on top of wide dim
            rj_glow = axes.plot(rayleigh_jeans_scaled, color=RED_A, stroke_width=10,
                                x_range=[0.001, x_max, 200])
            rj_glow.set_opacity(0.25)
            self.add(rj_glow)

            # ============================================================
            # BEAT A3.B1 | 13.00-20.00 s — REVEAL the ultraviolet catastrophe
            # ============================================================
            cat_text = Text("Ultraviolet Catastrophe", color=RED_A).scale(0.4)
            cat_text.to_edge(LEFT, buff=0.6).shift(UP * 1.6)
            cat_arrow = Arrow(
                cat_text.get_right() + RIGHT * 0.1,
                axes.c2p(7.5, 56),
                color=RED_A,
                buff=0.05,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.08,
            )
            self.play(FadeIn(cat_text, shift=RIGHT * 0.15, run_time=0.6))
            self.play(GrowArrow(cat_arrow, run_time=0.7))
            # Pulse the catastrophe zone — make it feel like a failure
            self.play(
                Flash(axes.c2p(7.5, 56), color=RED_A, flash_radius=0.35, line_length=0.2,
                      num_lines=12, run_time=0.9),
                Circumscribe(cat_text, color=RED_A, run_time=0.9),
            )
            self.wait(2.0)

            # ============================================================
            # BEAT A4.B1 | 20.00-26.50 s — EVOLVE: replace RJ with Planck (discrete energies)
            # ============================================================
            # Planck curve
            planck_curve = axes.plot(planck_scaled, color="#22D3EE",
                                      x_range=[0.001, x_max, 400])
            planck_glow = axes.plot(planck_scaled, color=TEAL_A, stroke_width=10,
                                     x_range=[0.001, x_max, 400])
            planck_glow.set_opacity(0.25)
            planck_label = Text("Planck", color="#22D3EE").scale(0.32)
            planck_label.move_to(axes.c2p(2.6, 5.3))

            # Hero equation: discrete energies E = h*nu
            eq_quantum = MathTex(r"E = h\nu", color=GOLD).scale(0.6)
            eq_quantum.to_edge(RIGHT, buff=0.7).shift(UP * 1.7)

            # Transform the classical curve into the quantum curve — same axes, new physics
            self.play(
                FadeOut(rj_label, run_time=0.4),
                ReplacementTransform(rj_curve, planck_curve, run_time=3.6, rate_func=smooth),
                ReplacementTransform(rj_glow, planck_glow, run_time=3.6, rate_func=smooth),
            )
            self.play(
                FadeIn(planck_label, shift=DOWN * 0.1, run_time=0.5),
                Write(eq_quantum, run_time=1.2),
            )
            self.wait(2.0)

            # ============================================================
            # BEAT A5.B1 | 26.50-30.00 s — RECAP: peak marker + idle loop
            # ============================================================
            # Highlight peak position (Planck peak at x ≈ 2.82)
            peak_x = 2.821
            peak_marker = Dot(axes.c2p(peak_x, planck_scaled(peak_x)), color=GOLD, radius=0.08)
            peak_line = DashedLine(
                axes.c2p(peak_x, 0),
                axes.c2p(peak_x, planck_scaled(peak_x)),
                color=GOLD,
                stroke_width=2,
                dash_length=0.08,
            ).set_opacity(0.7)
            peak_tag = MathTex(r"x_{peak}\!\approx\!2.82", color=GOLD).scale(0.32)
            peak_tag.next_to(peak_marker, UP, buff=0.12)

            recap = Text("Discrete energies  →  finite tail", color="#F8FAFC").scale(0.32)
            recap.to_edge(DOWN, buff=0.15).shift(LEFT * 0.5)

            self.play(
                Create(peak_line, run_time=0.6),
                FadeIn(peak_marker, scale=0.5, run_time=0.4),
                Write(peak_tag, run_time=0.7),
            )
            self.play(FadeIn(recap, shift=UP * 0.1, run_time=0.7))
            self.wait(1.6)

            # Living idle loop: a small marker slides along the Planck curve as t advances.
            # We use a single ValueTracker; curve is precomputed and never rebuilt.
            t_loop = ValueTracker(0.0)
            slider = Dot(color="#F8FAFC", radius=0.06)
            slider.add_updater(lambda m: m.move_to(
                axes.c2p(t_loop.get_value() % x_max,
                         planck_scaled(t_loop.get_value() % x_max))
            ))
            self.add(slider)
            self.play(t_loop.animate.set_value(3 * x_max), run_time=2.8, rate_func=linear)
            self.play(t_loop.animate.set_value(4 * x_max), run_time=2.0, rate_func=linear)
            self.wait(2.0)