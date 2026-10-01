from manim import *
import numpy as np
import math


# BEAT A1.B1 | 0.00-2.73 s
# BEAT A1.B2 | 2.73-5.00 s
# BEAT A2.B1 | 5.00-7.73 s
# BEAT A2.B2 | 7.73-10.00 s
# BEAT A3.B1 | 10.00-14.00 s
# BEAT A3.B2 | 14.00-18.00 s
# BEAT A4.B1 | 18.00-22.00 s
# BEAT A4.B2 | 22.00-26.00 s
# BEAT A5.B1 | 26.00-30.00 s

class AetherLabScene(Scene):
    def construct(self):
        # Physical constants
        h = 6.626e-34
        c_light = 3.0e8
        k = 1.381e-23
        b_wien = 2.898e-3
        y_star = 4.9651

        def planck(lam_m, T):
            u = h * c_light / (lam_m * k * T)
            if u > 500:
                return 0.0
            return (2 * h * c_light ** 2) / (lam_m ** 5 * (math.exp(u) - 1))

        def rayleigh_jeans(lam_m, T):
            return 2 * c_light * k * T / lam_m ** 4

        # =====================================================================
        # ACT 1: HOOK
        # =====================================================================

        # BEAT A1.B1 | 0.00-2.73 s
        # Iron bar fades in, faintly red
        title = Text("Blackbody Radiation", color=WHITE).scale(0.5).to_edge(UP, buff=0.2)

        iron_bar = Rectangle(width=5.0, height=0.7, color=RED, fill_opacity=1, stroke_width=1)
        iron_bar.set_fill(RED_E)
        iron_bar.set_color(MAROON)
        iron_bar.set_fill(color="#8B0000", opacity=0.95)
        iron_bar.move_to(DOWN * 1.8)

        bar_label = Text("iron bar", color=WHITE).scale(0.28)
        bar_label.next_to(iron_bar, DOWN, buff=0.12)

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(iron_bar, shift=UP * 0.1), FadeIn(bar_label, shift=UP * 0.1), run_time=0.6)
        self.wait(1.4)

        # BEAT A1.B2 | 2.73-5.00 s
        # Bar brightens orange, thermometer readout appears reading 3000 K
        T_tracker = ValueTracker(3000.0)
        lambda_max_tracker = ValueTracker(b_wien / T_tracker.get_value() * 1e9)

        temp_label = Text("T =", color=WHITE).scale(0.32)
        temp_value = always_redraw(lambda: DecimalNumber(
            T_tracker.get_value(), num_decimal_places=0, color=WHITE
        ).scale(0.32))
        temp_unit = Text("K", color=WHITE).scale(0.32)

        temp_group = VGroup(temp_label, temp_value, temp_unit).arrange(RIGHT, buff=0.08)
        temp_group.next_to(iron_bar, RIGHT, buff=0.4)

        # Update bar color via updater
        def update_bar_color(mob):
            T = T_tracker.get_value()
            # Map T from 2500..11000 to color: red -> orange -> white -> blue
            frac = np.clip((T - 2500) / 8500, 0, 1)
            if frac < 0.4:
                t = frac / 0.4
                R = 0.55 + 0.45 * t
                G = 0.0 + 0.45 * t
                B = 0.0 + 0.1 * t
            elif frac < 0.7:
                t = (frac - 0.4) / 0.3
                R = 1.0
                G = 0.45 + 0.55 * t
                B = 0.1 + 0.7 * t
            else:
                t = (frac - 0.7) / 0.3
                R = 1.0 - 0.3 * t
                G = 1.0
                B = 0.8 + 0.2 * t
            mob.set_fill(color="#%02x%02x%02x" % (int(R * 255), int(G * 255), int(B * 255)),
                         opacity=0.95)
            mob.set_color("#%02x%02x%02x" % (int(R * 255), int(G * 255), int(B * 255)))

        iron_bar.add_updater(update_bar_color)

        self.play(FadeIn(temp_group, shift=LEFT * 0.15), run_time=0.6)
        # Brief brighten
        self.play(T_tracker.animate.set_value(3000), run_time=0.4)
        self.wait(1.0)

        # =====================================================================
        # ACT 2: ESTABLISH
        # =====================================================================

        # BEAT A2.B1 | 5.00-7.73 s
        # Empty axes plot appears above the bar
        # Clear lower scene area for axes by shrinking
        axes = Axes(
            x_range=[0, 2000, 500],
            y_range=[0, 1.0, 0.25],
            x_length=7.5,
            y_length=3.2,
            axis_config={"stroke_opacity": 0.7, "color": GREY_B},
            tips=False,
        )
        axes.move_to(UP * 1.1)

        x_axis_label = Text("Wavelength λ (nm)", color=WHITE).scale(0.28)
        x_axis_label.next_to(axes.x_axis, RIGHT, buff=0.15)
        y_axis_label = Text("B_λ", color=WHITE).scale(0.28)
        y_axis_label.next_to(axes.y_axis, UP, buff=0.1)
        y_unit_label = Text("(W·m⁻²·sr⁻¹·m⁻¹)", color=GREY_A).scale(0.22)
        y_unit_label.next_to(y_axis_label, RIGHT, buff=0.08)

        axes_group = VGroup(axes, x_axis_label, y_axis_label, y_unit_label)
        self.play(FadeIn(axes_group, shift=DOWN * 0.2), run_time=0.7)
        self.wait(1.6)

        # BEAT A2.B2 | 7.73-10.00 s
        # Rayleigh-Jeans curve diverges — catastrophe
        # Build the RJ curve in normalized space for visibility
        lam_min_nm = 50.0
        lam_max_nm = 2000.0
        # Normalize RJ curve to the axes (just use arbitrary scaled values)
        # Compute maximum value for the plot normalization
        T_rj = 5778.0
        sample_lams = np.linspace(lam_min_nm, lam_max_nm, 300) * 1e-9
        rj_values = np.array([rayleigh_jeans(lam, T_rj) for lam in sample_lams])
        rj_max = np.max(rj_values[:50])  # peak near short λ

        def rj_plot_func(lam_nm):
            lam = lam_nm * 1e-9
            val = rayleigh_jeans(lam, T_rj)
            # Normalize and clip to fit
            return min(val / rj_max * 0.92, 0.95)

        rj_curve = axes.plot(rj_plot_func, color=BLUE, stroke_width=3)
        rj_curve.set_stroke(opacity=0.0)

        rj_eq = MathTex(r"B_{\lambda}^{RJ}=\frac{2ckT}{\lambda^4}", color=BLUE).scale(0.32)
        rj_eq.to_corner(UL, buff=0.5).shift(DOWN * 0.4 + RIGHT * 0.2)

        rj_label = Text("Rayleigh-Jeans", color=BLUE).scale(0.26)
        rj_label.next_to(rj_eq, DOWN, buff=0.08).align_to(rj_eq, LEFT)

        # Animate RJ curve growing and shooting up at left
        rj_curve.set_stroke(opacity=1.0)
        self.play(Create(rj_curve), FadeIn(rj_eq, shift=RIGHT * 0.1), run_time=1.2)
        self.play(FadeIn(rj_label, shift=UP * 0.05), run_time=0.3)
        catastrophe_tag = Text("UV catastrophe", color=RED).scale(0.26)
        catastrophe_tag.next_to(axes.c2p(lam_min_nm + 80, 0.95), UP, buff=0.08)
        self.play(FadeIn(catastrophe_tag, shift=DOWN * 0.05), run_time=0.3)
        self.wait(0.5)

        # =====================================================================
        # ACT 3: EVOLVE
        # =====================================================================

        # BEAT A3.B1 | 10.00-14.00 s
        # RJ curve fades out, Planck curve at T=3000K is drawn (capped at IR)
        rj_group = VGroup(rj_curve, rj_eq, rj_label, catastrophe_tag)

        # Compute Planck values at T=3000 K
        T_cool = 3000.0
        lam_cool = np.linspace(lam_min_nm, lam_max_nm, 400) * 1e-9
        planck_cool = np.array([planck(lam, T_cool) for lam in lam_cool])
        planck_cool_max = np.max(planck_cool)
        # Peak location
        idx_peak_cool = np.argmax(planck_cool)
        lam_peak_cool_nm = lam_cool[idx_peak_cool] * 1e9

        def planck_cool_func(lam_nm):
            lam = lam_nm * 1e-9
            val = planck(lam, T_cool)
            return val / planck_cool_max * 0.88

        planck_cool_curve = axes.plot(planck_cool_func, color="#FF6B35", stroke_width=3)

        planck_eq = MathTex(
            r"B_{\lambda}(T)=\frac{2hc^2/\lambda^5}{e^{hc/\lambda kT}-1}",
            color="#FF6B35"
        ).scale(0.32)
        planck_eq.move_to(axes.get_top() + DOWN * 0.25).to_edge(LEFT, buff=0.3)
        planck_eq.shift(DOWN * 0.05)

        planck_label = Text("Planck's law", color="#FF6B35").scale(0.26)
        planck_label.next_to(planck_eq, DOWN, buff=0.08).align_to(planck_eq, LEFT)

        self.play(
            FadeOut(rj_group, shift=UP * 0.2),
            run_time=0.6
        )
        self.play(
            Create(planck_cool_curve),
            FadeIn(planck_eq, shift=RIGHT * 0.1),
            run_time=1.6
        )
        self.play(FadeIn(planck_label, shift=UP * 0.05), run_time=0.3)

        # Peak dot for the cool curve
        peak_dot_cool = Dot(
            axes.c2p(lam_peak_cool_nm, planck_cool_func(lam_peak_cool_nm)),
            color=WHITE, radius=0.07
        )
        peak_label_cool = Text("λ_max = 966 nm", color=WHITE).scale(0.24)
        peak_label_cool.next_to(peak_dot_cool, UP, buff=0.1)
        self.play(FadeIn(peak_dot_cool, scale=0.5), FadeIn(peak_label_cool), run_time=0.4)
        self.wait(0.7)

        # BEAT A3.B2 | 14.00-18.00 s
        # Temperature rises: 3000 -> 5778 -> 10000 K
        # Plan: build a "current" Planck curve mobject that we update via .become
        # We'll precompute the curves for the three temperatures
        T_mid = 5778.0
        T_hot = 10000.0

        lam_p = np.linspace(lam_min_nm, lam_max_nm, 400) * 1e-9
        planck_mid_arr = np.array([planck(lam, T_mid) for lam in lam_p])
        planck_hot_arr = np.array([planck(lam, T_hot) for lam in lam_p])
        planck_mid_max = np.max(planck_mid_arr)
        planck_hot_max = np.max(planck_hot_arr)
        idx_peak_mid = np.argmax(planck_mid_arr)
        idx_peak_hot = np.argmax(planck_hot_arr)
        lam_peak_mid_nm = lam_p[idx_peak_mid] * 1e9
        lam_peak_hot_nm = lam_p[idx_peak_hot] * 1e9

        def make_planck_curve(arr, max_val, color):
            pts = []
            for i, lam_nm in enumerate(np.linspace(lam_min_nm, lam_max_nm, 200)):
                lam = lam_nm * 1e-9
                # find nearest
                idx = int((lam_nm - lam_min_nm) / (lam_max_nm - lam_min_nm) * (len(arr) - 1))
                idx = max(0, min(idx, len(arr) - 1))
                val = arr[idx] / max_val * 0.88
                pts.append(axes.c2p(lam_nm, val))
            return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(pts)

        planck_mid_curve = make_planck_curve(planck_mid_arr, planck_mid_max, "#FF6B35")
        planck_hot_curve = make_planck_curve(planck_hot_arr, planck_hot_max, "#FF6B35")

        # Animate temperature climb and morph curve
        peak_dot_mid = Dot(axes.c2p(lam_peak_mid_nm, 0.88), color=WHITE, radius=0.07)
        peak_dot_hot = Dot(axes.c2p(lam_peak_hot_nm, planck_hot_arr[idx_peak_hot] / planck_hot_max * 0.88),
                            color=WHITE, radius=0.07)

        # We morph the cool curve by replacing points, but the simplest is Transform
        # Move the existing curve to the mid shape
        self.play(
            T_tracker.animate.set_value(5778),
            Transform(planck_cool_curve, planck_mid_curve),
            Transform(peak_dot_cool, peak_dot_mid),
            FadeOut(peak_label_cool),
            run_time=1.8
        )
        peak_label_mid = Text("λ_max = 502 nm", color=WHITE).scale(0.24)
        peak_label_mid.next_to(peak_dot_mid, UP, buff=0.1)
        self.play(FadeIn(peak_label_mid), run_time=0.2)

        self.play(
            T_tracker.animate.set_value(10000),
            Transform(planck_cool_curve, planck_hot_curve),
            Transform(peak_dot_cool, peak_dot_hot),
            FadeOut(peak_label_mid),
            run_time=1.8
        )
        peak_label_hot = Text("λ_max = 290 nm", color=WHITE).scale(0.24)
        peak_label_hot.next_to(peak_dot_hot, UP, buff=0.1)
        self.play(FadeIn(peak_label_hot), run_time=0.2)
        # Update lambda_max tracker
        self.play(lambda_max_tracker.animate.set_value(290), run_time=0.1)
        self.wait(0.2)

        # =====================================================================
        # ACT 4: REVEAL
        # =====================================================================

        # BEAT A4.B1 | 18.00-22.00 s
        # Vertical guideline from peak to x-axis, Wien's law readout
        peak_guide = DashedLine(
            axes.c2p(lam_peak_hot_nm, 0),
            axes.c2p(lam_peak_hot_nm, planck_hot_arr[idx_peak_hot] / planck_hot_max * 0.88),
            color="#FFD700", stroke_width=2.5
        )
        guide_label = Text("λ_max", color="#FFD700").scale(0.26)
        guide_label.next_to(peak_guide.get_top(), LEFT, buff=0.1)

        wien_eq = MathTex(
            r"\lambda_{max}\,T=\frac{hc}{y^*k}\approx2.898\times10^{-3}\,\text{m·K}",
            color="#FFD700"
        ).scale(0.34)
        wien_eq.to_edge(UP, buff=0.55).shift(RIGHT * 0.2)

        wien_title = Text("Wien's displacement law", color="#FFD700").scale(0.3)
        wien_title.next_to(wien_eq, UP, buff=0.12).align_to(wien_eq, LEFT)

        # Live readout
        wien_product = ValueTracker(b_wien)  # in m·K
        wien_value_text = Text("λ_max T =", color=WHITE).scale(0.28)
        wien_number = always_redraw(lambda: DecimalNumber(
            wien_product.get_value(),
            num_decimal_places=4,
            color="#FFD700"
        ).scale(0.3))
        wien_unit = Text("×10⁻³ m·K", color=WHITE).scale(0.26)
        wien_readout = VGroup(wien_value_text, wien_number, wien_unit).arrange(RIGHT, buff=0.08)
        wien_readout.next_to(iron_bar, LEFT, buff=0.3).shift(UP * 0.3)

        self.play(
            Create(peak_guide),
            FadeIn(guide_label, shift=RIGHT * 0.05),
            run_time=0.8
        )
        self.play(
            FadeIn(wien_eq, shift=DOWN * 0.1),
            FadeIn(wien_title, shift=DOWN * 0.05),
            FadeIn(wien_readout, shift=RIGHT * 0.1),
            run_time=1.0
        )
        # Animate the product tracker gently
        self.play(wien_product.animate.set_value(2.901e-3), run_time=0.7)
        self.play(wien_product.animate.set_value(2.897e-3), run_time=0.5)
        self.wait(0.4)

        # BEAT A4.B2 | 22.00-26.00 s
        # Hero frame: bar glows blue-white at 10000 K, peak at 290 nm, Wien locked
        hero_y_star = MathTex(r"y^*\approx4.9651", color="#FFD700").scale(0.32)
        hero_y_star.next_to(wien_eq, DOWN, buff=0.18).align_to(wien_eq, LEFT)

        # Brighten the bar to blue-white visually
        # Animate the bar color gently to push toward bluer tone
        self.play(T_tracker.animate.set_value(10000), run_time=0.4)
        self.play(
            FadeIn(hero_y_star, shift=UP * 0.08),
            run_time=0.6
        )

        # Pulse the peak guide gently
        guide_pulse = ValueTracker(1.0)
        peak_guide.add_updater(lambda m: m.set_stroke(opacity=guide_pulse.get_value()))

        # Hold the hero frame
        self.play(guide_pulse.animate.set_value(0.6), run_time=0.8)
        self.play(guide_pulse.animate.set_value(1.0), run_time=0.8)
        self.play(guide_pulse.animate.set_value(0.7), run_time=0.6)
        self.play(guide_pulse.animate.set_value(1.0), run_time=0.4)
        self.wait(0.4)

        # =====================================================================
        # ACT 5: RECAP
        # =====================================================================

        # BEAT A5.B1 | 26.00-30.00 s
        # Clear and overlay three curves, single-line annotation
        # Remove all current scene furniture except the axes region
        # We'll build overlay planck curves at three temperatures
        guide_pulse.set_value(1.0)
        peak_guide.remove_updater(peak_guide.get_updaters()[0])

        recap_planck_eq = MathTex(
            r"B_{\lambda}(T)=\frac{2hc^2/\lambda^5}{e^{hc/\lambda kT}-1}",
            color=WHITE
        ).scale(0.36)
        recap_planck_eq.to_edge(UP, buff=0.25)

        # Clear non-essentials
        fadeouts = VGroup(
            iron_bar, bar_label, temp_group, wien_eq, wien_title,
            wien_readout, hero_y_star, peak_guide, guide_label,
            peak_label_hot, planck_cool_curve, planck_eq, planck_label,
            peak_dot_cool
        )
        self.play(FadeOut(fadeouts, shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(recap_planck_eq, shift=DOWN * 0.1), run_time=0.4)

        # Build the three overlay curves and their peak markers
        # Rescale axes for the recap: still the same axes
        # We need smaller, normalized versions of the curves
        # Use the same axes; plot three smaller curves stacked
        cool_overlay = make_planck_curve(planck_cool, planck_cool_max, RED)
        cool_overlay.set_stroke(opacity=0.9)
        mid_overlay = make_planck_curve(planck_mid_arr, planck_mid_max, ORANGE)
        mid_overlay.set_stroke(opacity=0.9)
        hot_overlay = make_planck_curve(planck_hot_arr, planck_hot_max, "#FFD700")
        hot_overlay.set_stroke(opacity=0.95)

        # Peak markers
        peak_cool_marker = Dot(axes.c2p(lam_peak_cool_nm, 0.88), color=RED, radius=0.06)
        peak_mid_marker = Dot(axes.c2p(lam_peak_mid_nm, 0.88), color=ORANGE, radius=0.06)
        peak_hot_marker = Dot(axes.c2p(lam_peak_hot_nm, 0.88), color="#FFD700", radius=0.06)

        legend_cool = Text("3000 K", color=RED).scale(0.24)
        legend_cool.next_to(axes.c2p(1800, 0.85), LEFT, buff=0.1)
        legend_mid = Text("5778 K", color=ORANGE).scale(0.24)
        legend_mid.next_to(axes.c2p(1800, 0.70), LEFT, buff=0.1)
        legend_hot = Text("10000 K", color="#FFD700").scale(0.24)
        legend_hot.next_to(axes.c2p(1800, 0.55), LEFT, buff=0.1)

        self.play(
            Create(cool_overlay), FadeIn(peak_cool_marker), FadeIn(legend_cool),
            run_time=0.6
        )
        self.play(
            Create(mid_overlay), FadeIn(peak_mid_marker), FadeIn(legend_mid),
            run_time=0.6
        )
        self.play(
            Create(hot_overlay), FadeIn(peak_hot_marker), FadeIn(legend_hot),
            run_time=0.6
        )

        recap_annotation = Text(
            "Higher T → shorter λ_max → bluer glow",
            color=WHITE
        ).scale(0.32)
        recap_annotation.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(recap_annotation, shift=UP * 0.1), run_time=0.5)

        # Idle loop: gentle breathing of the curves (subtle amplitude oscillation)
        idle_tracker = ValueTracker(0.0)
        overlay_group = VGroup(cool_overlay, mid_overlay, hot_overlay)

        def idle_breathe(mob):
            phase = idle_tracker.get_value()
            scale = 1.0 + 0.02 * math.sin(phase * 2.0)
            for m in mob:
                m.set_stroke(width=3 * scale)

        overlay_group.add_updater(idle_breathe)

        # Animate the idle tracker for a brief live loop
        self.play(idle_tracker.animate.set_value(2.5), run_time=2.0)
        self.play(idle_tracker.animate.set_value(5.0), run_time=1.5)

        # Final hold
        self.wait(0.5)