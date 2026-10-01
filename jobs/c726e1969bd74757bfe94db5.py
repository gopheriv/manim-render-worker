from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # =====================================================================
        # ACT I — HOOK: warm glow appears, hint at the spectrum to come
        # =====================================================================
        # BEAT A1.B1 | 0.00-2.50 s
        title = Text("Blackbody Radiation", color=WHITE).scale(0.55).to_edge(UP, buff=0.4)
        sub = Text("how temperature shapes the spectrum", color=BLUE_B).scale(0.32)
        sub.next_to(title, DOWN, buff=0.18)
        # a glowing ember dot grows
        ember = Dot(radius=0.18, color=ORANGE).move_to(DOWN * 2.2)
        ember_glow = Dot(radius=0.55, color=ORANGE).set_opacity(0.25).move_to(ember.get_center())
        self.play(FadeIn(ember_glow, scale=1.6), FadeIn(ember, scale=0.6), run_time=0.8)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.6)
        self.wait(0.1)

        # =====================================================================
        # ACT II — ESTABLISH: name the law, draw the axes, plot 3000 K
        # =====================================================================
        # BEAT A2.B1 | 2.50-8.00 s
        self.play(FadeOut(ember_glow), FadeOut(ember), run_time=0.4)

        axes = Axes(
            x_range=[0.2, 3.0, 0.4],
            y_range=[0, 18, 3],
            x_length=10.5,
            y_length=4.8,
            tips=False,
            axis_config={"stroke_opacity": 0.6, "color": GREY_B},
        ).move_to(DOWN * 0.2)
        x_lbl = Text("Wavelength λ (μm)", color=GREY_A).scale(0.30).next_to(axes.x_axis, RIGHT, buff=0.15)
        y_lbl = MathTex(r"B_\lambda \;\;(10^{12}\,\mathrm{W\,m^{-2}\,sr^{-1}\,m^{-1}})",
                        color=GREY_A).scale(0.32).next_to(axes.y_axis, UP, buff=0.1)
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=1.0)

        # Planck's law in wavelength form (constants pre-baked for μm units)
        # B_lambda(T, t [μm]) = 119.1 / (t^5 (exp(14380/(T t)) - 1))
        T_VALS = [3000, 4000, 5000, 6000]
        C_LAW = 119.1
        U_BIG = 14380.0  # hc/k_B in μm·K

        def B_law(t_um, T):
            u = U_BIG / (T * t_um)
            return C_LAW / (t_um ** 5 * (math.exp(u) - 1.0))

        def lambda_max(T):
            return 2.898e6 / T  # nm; convert to μm → /1000
            # using b = 2.898e6 nm·K → lambda_max(μm) = 2898/T

        lam_max_um = lambda_max(3000) / 1000.0  # ~0.966 μm

        curve_3k = axes.plot(lambda t: B_law(t, 3000), x_range=[0.2, 3.0], color=ORANGE, stroke_width=4)
        curve_3k_glow = axes.plot(lambda t: B_law(t, 3000), x_range=[0.2, 3.0],
                                  color=ORANGE, stroke_width=14, stroke_opacity=0.18)
        self.play(Create(curve_3k_glow), Create(curve_3k), run_time=1.8)

        planck_eq = MathTex(r"B_\lambda(T,\lambda)=\frac{2hc^{2}}{\lambda^{5}(e^{hc/\lambda k_{B}T}-1)}",
                            color=ORANGE).scale(0.42).to_corner(UL).shift(DOWN * 1.05 + RIGHT * 0.2)
        self.play(Write(planck_eq), run_time=1.4)
        self.wait(0.2)

        # Mark the 3000 K peak with a live readout (Wien's law)
        peak_dot_3k = Dot(axes.c2p(lam_max_um, B_law(lam_max_um, 3000)), color=YELLOW, radius=0.08)
        peak_label_3k = MathTex(r"\lambda_{\max}\!\cdot\!T = 2.898\times10^{-3}\,\mathrm{m\,K}",
                                color=YELLOW).scale(0.34).next_to(peak_dot_3k, UP, buff=0.18)
        vline_3k = DashedLine(axes.c2p(lam_max_um, 0), axes.c2p(lam_max_um, B_law(lam_max_um, 3000)),
                              color=YELLOW, stroke_width=2, stroke_opacity=0.55)
        self.play(Create(vline_3k), FadeIn(peak_dot_3k, scale=1.3), Write(peak_label_3k), run_time=1.0)
        self.wait(0.1)

        # =====================================================================
        # ACT III — EVOLVE: temperature rises, the spectrum shifts and grows
        # =====================================================================
        # BEAT A3.B1 | 8.00-19.50 s
        # Fade the 3k label, prepare a temperature tracker driving the curve transform
        self.play(FadeOut(peak_label_3k), FadeOut(peak_dot_3k), FadeOut(vline_3k),
                  FadeOut(planck_eq), run_time=0.5)

        # Build static spectra for 4000, 5000, 6000 K (created once, transformed)
        curve_4k = axes.plot(lambda t: B_law(t, 4000), x_range=[0.2, 3.0], color=YELLOW, stroke_width=4)
        curve_4k_glow = axes.plot(lambda t: B_law(t, 4000), x_range=[0.2, 3.0],
                                  color=YELLOW, stroke_width=14, stroke_opacity=0.18)
        curve_5k = axes.plot(lambda t: B_law(t, 5000), x_range=[0.2, 3.0], color=GREEN_C, stroke_width=4)
        curve_5k_glow = axes.plot(lambda t: B_law(t, 5000), x_range=[0.2, 3.0],
                                  color=GREEN_C, stroke_width=14, stroke_opacity=0.18)
        curve_6k = axes.plot(lambda t: B_law(t, 6000), x_range=[0.2, 3.0], color=WHITE, stroke_width=4)
        curve_6k_glow = axes.plot(lambda t: B_law(t, 6000), x_range=[0.2, 3.0],
                                  color=WHITE, stroke_width=14, stroke_opacity=0.18)

        # Live temperature readout at lower-left
        T_tracker = ValueTracker(3000)
        T_number = DecimalNumber(3000, num_decimal_places=0, color=ORANGE).scale(0.45)
        T_unit = Text("K", color=ORANGE).scale(0.35)
        T_label = Text("T =", color=GREY_A).scale(0.35)
        T_group = VGroup(T_label, T_number, T_unit).arrange(RIGHT, buff=0.12).to_corner(DL, buff=0.45)

        # Update the displayed T number
        T_number.add_updater(lambda m: m.set_value(T_tracker.get_value()))

        # Color the readout based on T (visual cue)
        def t_color():
            v = T_tracker.get_value()
            if v < 3500:
                return ORANGE
            elif v < 4500:
                return YELLOW
            elif v < 5500:
                return GREEN_C
            return WHITE

        T_number.add_updater(lambda m: m.set_color(t_color()))
        T_unit.add_updater(lambda m: m.set_color(t_color()))

        self.add(T_number, T_unit, T_label)

        # Hero legend: peak-shift dots that we morph position of via Transform
        peak_marker = Dot(axes.c2p(lam_max_um, B_law(lam_max_um, 3000)), color=YELLOW, radius=0.10)
        peak_vline = DashedLine(axes.c2p(lam_max_um, 0), axes.c2p(lam_max_um, B_law(lam_max_um, 3000)),
                                color=YELLOW, stroke_width=2, stroke_opacity=0.7)

        wien_eq = MathTex(r"\lambda_{\max}\,T = b = 2.898\times10^{-3}\,\mathrm{m\,K}",
                          color=YELLOW).scale(0.36).to_edge(RIGHT, buff=0.3).shift(UP * 0.4)
        self.play(FadeIn(wien_eq, shift=LEFT * 0.2), run_time=0.6)
        self.play(FadeIn(peak_marker, scale=1.3), Create(peak_vline), run_time=0.5)

        # --- 3000 → 4000 K: curve grows, peak slides left ------------------------
        self.play(T_tracker.animate.set_value(4000),
                  Transform(curve_3k, curve_4k, replace_mobject_with_target_in_scene=False),
                  Transform(curve_3k_glow, curve_4k_glow, replace_mobject_with_target_in_scene=False),
                  run_time=2.2, rate_func=smooth)
        # Move peak marker to new (λ_max, peak B) for 4000 K
        new_x = lambda_max(4000) / 1000.0
        new_y = B_law(new_x, 4000)
        new_vline = DashedLine(axes.c2p(new_x, 0), axes.c2p(new_x, new_y),
                               color=YELLOW, stroke_width=2, stroke_opacity=0.7)
        self.play(Transform(peak_vline, new_vline),
                  peak_marker.animate.move_to(axes.c2p(new_x, new_y)),
                  run_time=1.0, rate_func=smooth)

        # --- 4000 → 5000 K ------------------------------------------------------
        self.play(T_tracker.animate.set_value(5000),
                  Transform(curve_3k, curve_5k, replace_mobject_with_target_in_scene=False),
                  Transform(curve_3k_glow, curve_5k_glow, replace_mobject_with_target_in_scene=False),
                  run_time=2.2, rate_func=smooth)
        new_x = lambda_max(5000) / 1000.0
        new_y = B_law(new_x, 5000)
        new_vline = DashedLine(axes.c2p(new_x, 0), axes.c2p(new_x, new_y),
                               color=YELLOW, stroke_width=2, stroke_opacity=0.7)
        self.play(Transform(peak_vline, new_vline),
                  peak_marker.animate.move_to(axes.c2p(new_x, new_y)),
                  run_time=1.0, rate_func=smooth)

        # --- 5000 → 6000 K ------------------------------------------------------
        self.play(T_tracker.animate.set_value(6000),
                  Transform(curve_3k, curve_6k, replace_mobject_with_target_in_scene=False),
                  Transform(curve_3k_glow, curve_6k_glow, replace_mobject_with_target_in_scene=False),
                  run_time=2.2, rate_func=smooth)
        new_x = lambda_max(6000) / 1000.0
        new_y = B_law(new_x, 6000)
        new_vline = DashedLine(axes.c2p(new_x, 0), axes.c2p(new_x, new_y),
                               color=YELLOW, stroke_width=2, stroke_opacity=0.7)
        self.play(Transform(peak_vline, new_vline),
                  peak_marker.animate.move_to(axes.c2p(new_x, new_y)),
                  run_time=1.0, rate_func=smooth)

        # =====================================================================
        # ACT IV — REVEAL: hero frame — Wien hyperbola + T^5 + T^4 readout
        # =====================================================================
        # BEAT A4.B1 | 19.50-25.50 s
        # Clear curve-related scaffolding; build a clean hero composition
        self.play(FadeOut(curve_3k), FadeOut(curve_3k_glow),
                  FadeOut(peak_vline), FadeOut(peak_marker),
                  FadeOut(wien_eq), run_time=0.6)

        # Reveal the universal shape f(u) = u^5/(e^u - 1) on a secondary small axes
        small_axes = Axes(
            x_range=[0, 12, 2],
            y_range=[0, 1.2, 0.3],
            x_length=4.6,
            y_length=3.2,
            tips=False,
            axis_config={"stroke_opacity": 0.5, "color": GREY_B, "include_numbers": False},
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        small_xlbl = Text("u = hc/(λk_BT)", color=GREY_A).scale(0.26).next_to(small_axes.x_axis, RIGHT, buff=0.1)
        small_ylbl = MathTex(r"f(u)=\frac{u^{5}}{e^{u}-1}", color=ORANGE).scale(0.32).next_to(small_axes, UP, buff=0.1)

        def f_u(u):
            return u ** 5 / (math.exp(u) - 1.0)

        f_curve = small_axes.plot(f_u, x_range=[0.5, 11.0], color=ORANGE, stroke_width=4)
        f_glow = small_axes.plot(f_u, x_range=[0.5, 11.0], color=ORANGE, stroke_width=14, stroke_opacity=0.2)
        u_star_line = DashedLine(small_axes.c2p(4.9651, 0), small_axes.c2p(4.9651, f_u(4.9651)),
                                 color=YELLOW, stroke_width=2)
        u_star_dot = Dot(small_axes.c2p(4.9651, f_u(4.9651)), color=YELLOW, radius=0.08)
        u_star_lbl = MathTex(r"u^{*}\approx 4.965", color=YELLOW).scale(0.34).next_to(u_star_dot, UP, buff=0.15)

        self.play(FadeIn(small_axes), FadeIn(small_xlbl), FadeIn(small_ylbl), run_time=0.6)
        self.play(Create(f_glow), Create(f_curve), run_time=1.4)
        self.play(Create(u_star_line), FadeIn(u_star_dot, scale=1.4), Write(u_star_lbl), run_time=0.9)

        # Three relationships on the right side, stacked
        eq1 = MathTex(r"\lambda_{\max}\,T = b", color=YELLOW).scale(0.42)
        eq2 = MathTex(r"B_{\lambda,\max}\propto T^{5}", color=GREEN_C).scale(0.42)
        eq3 = MathTex(r"j^{*}=\sigma T^{4}", color=WHITE).scale(0.42)
        hero_eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=0.6)
        self.play(Write(eq1), run_time=0.7)
        self.play(Write(eq2), run_time=0.7)
        self.play(Write(eq3), run_time=0.7)

        # Tag on top: "universal shape"
        tag = Text("universal shape → one peak", color=BLUE_B).scale(0.30).next_to(small_axes, DOWN, buff=0.3)
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.5)
        self.wait(1.4)

        # =====================================================================
        # ACT V — RECAP: final sweep along Wien's hyperbola, then idle loop
        # =====================================================================
        # BEAT A5.B1 | 25.50-30.00 s
        self.play(FadeOut(small_axes), FadeOut(small_xlbl), FadeOut(small_ylbl),
                  FadeOut(f_curve), FadeOut(f_glow),
                  FadeOut(u_star_line), FadeOut(u_star_dot), FadeOut(u_star_lbl),
                  FadeOut(tag), FadeOut(eq1), FadeOut(eq2), FadeOut(eq3), run_time=0.6)

        # Restore the main axes + a single living curve that breathes with T
        # We rebuild axes cleanly (they were never removed, but ensure visibility)
        axes.set_opacity(1.0)
        x_lbl.set_opacity(1.0)
        y_lbl.set_opacity(1.0)

        # Recap headline
        recap = Text("Doubling T halves λ_max  ·  height × 32  ·  flux × 16",
                     color=YELLOW).scale(0.36).next_to(title, DOWN, buff=0.25)
        self.play(Write(recap), run_time=1.5)

        # A live idle: a marker traveling along the Wien hyperbola λ = b/T
        T_idle = ValueTracker(6000)
        # The idle curve is a fresh static curve built for T=6000, then re-rendered via Transform
        idle_curve = axes.plot(lambda t: B_law(t, 6000), x_range=[0.2, 3.0], color=WHITE, stroke_width=4)
        idle_glow = axes.plot(lambda t: B_law(t, 6000), x_range=[0.2, 3.0],
                              color=WHITE, stroke_width=14, stroke_opacity=0.18)
        idle_peak = Dot(axes.c2p(lambda_max(6000) / 1000.0,
                                 B_law(lambda_max(6000) / 1000.0, 6000)),
                        color=YELLOW, radius=0.10)
        idle_vline = DashedLine(
            axes.c2p(lambda_max(6000) / 1000.0, 0),
            axes.c2p(lambda_max(6000) / 1000.0, B_law(lambda_max(6000) / 1000.0, 6000)),
            color=YELLOW, stroke_width=2, stroke_opacity=0.7)
        self.play(FadeIn(idle_glow), Create(idle_curve),
                  FadeIn(idle_peak, scale=1.3), Create(idle_vline), run_time=0.7)

        # T_number already exists; rebind its updater to T_idle
        T_number.clear_updaters()
        T_number.add_updater(lambda m: m.set_value(T_idle.get_value()))
        T_unit.clear_updaters()
        T_unit.add_updater(lambda m: m.set_color(WHITE))

        # idle: sweep T_idle 6000 → 3000 → 6000 to show λ_max sliding along the hyperbola
        self.play(T_idle.animate.set_value(3000),
                  idle_peak.animate.move_to(axes.c2p(lambda_max(3000) / 1000.0,
                                                    B_law(lambda_max(3000) / 1000.0, 3000))),
                  run_time=2.2, rate_func=smooth)
        self.play(T_idle.animate.set_value(6000),
                  idle_peak.animate.move_to(axes.c2p(lambda_max(6000) / 1000.0,
                                                    B_law(lambda_max(6000) / 1000.0, 6000))),
                  run_time=2.2, rate_func=smooth)