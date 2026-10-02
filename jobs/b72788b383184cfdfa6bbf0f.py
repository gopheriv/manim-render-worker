from manim import *
import numpy as np
import math


# Frequency-domain Planck intensity (arbitrary units, normalized to peak ~1)
# Peak around nu ~ 5.9e14 Hz for T=5800 K (visible). We plot on a 0..10 (x10^14 Hz) axis.
H_PLANCK = 6.62607015e-34
K_B = 1.380649e-23
C_LIGHT = 2.99792458e8
T_BODY = 5800.0


def planck_intensity(nu_14, T):
    nu = nu_14 * 1e14
    expo = (H_PLANCK * nu) / (K_B * T)
    if expo > 500:
        return 0.0
    return (8.0 * math.pi * H_PLANCK * nu**3) / (C_LIGHT**3) / (math.exp(expo) - 1.0)


def rayleigh_jeans(nu_14, T):
    nu = nu_14 * 1e14
    return (8.0 * math.pi * nu**2 * K_B * T) / (C_LIGHT**3)


# Normalize curves so they share a similar visual scale on the axes.
_NU_MAX = 10.0
_PEAK = max(planck_intensity(nu, T_BODY) for nu in np.linspace(0.1, _NU_MAX, 200))
_RJ_PEAK = rayleigh_jeans(_NU_MAX * 0.5, T_BODY)  # moderate scale for classical


def planck_norm(nu_14):
    return planck_intensity(nu_14, T_BODY) / _PEAK


def rj_norm(nu_14):
    return rayleigh_jeans(nu_14, T_BODY) / _RJ_PEAK * 0.8


# Accent color: solar sunset orange (Planck)
COLOR_PLANCK = "#FF8C00"
COLOR_CLASSICAL = "#4169E1"
COLOR_ACCENT = "#FFD700"
COLOR_INGOT_DARK = "#202020"
COLOR_INGOT_HOT = "#FF8C00"


class AetherLabScene(Scene):
    def construct(self):
            # ---- Persistent scaffolding (background axes appear in A2.B1) ----
            frame_w = config.frame_width
            frame_h = config.frame_height

            # Left-side stage where the heated ingot sits
            ingot_center = np.array([-4.6, 0.0, 0.0])
            hotplate = Rectangle(width=3.4, height=0.25, color=GRAY, fill_opacity=0.4, stroke_width=1)
            hotplate.move_to(ingot_center + DOWN * 2.2)

            ingot = Square(side_length=1.6, color=WHITE, stroke_width=2,
                           fill_color=rgb_to_color([0x20 / 255, 0x20 / 255, 0x20 / 255]),
                           fill_opacity=1.0)
            ingot.move_to(ingot_center + UP * 0.3)

            ingot_label = Text("Fe ingot", color=WHITE, font_size=22)
            ingot_label.next_to(ingot, DOWN, buff=0.12)

            # Temperature DecimalNumber (ValueTracker-driven)
            T_tracker = ValueTracker(0.0)
            T_readout = DecimalNumber(
                0, num_decimal_places=0, color=COLOR_ACCENT, font_size=44
            )
            T_readout.add_updater(lambda m: m.set_value(int(T_tracker.get_value())))
            T_unit = Text("K", color=COLOR_ACCENT, font_size=30)
            T_eq_label = Text("T =", color=WHITE, font_size=30)
            T_group = VGroup(T_eq_label, T_readout, T_unit).arrange(RIGHT, buff=0.12)
            T_group.next_to(ingot, UP, buff=0.45)

            # Photon counter (discrete packet accumulator)
            photon_tracker = ValueTracker(0.0)
            photon_readout = Integer(
                0, color=COLOR_ACCENT, font_size=36
            )
            photon_readout.add_updater(lambda m: m.set_value(int(photon_tracker.get_value())))
            photon_label = Text("photons", color=WHITE, font_size=22)
            photon_caption = Text("E = h\u03bd", color=COLOR_ACCENT, font_size=24)
            photon_group = VGroup(photon_label, photon_readout, photon_caption).arrange(RIGHT, buff=0.12)
            photon_group.next_to(hotplate, DOWN, buff=0.35)

            # Right-side spectrum axes
            axes = Axes(
                x_range=[0, 10, 2],
                y_range=[0, 1.2, 0.5],
                x_length=6.2,
                y_length=3.6,
                tips=False,
                axis_config={"color": GRAY, "stroke_width": 1, "include_numbers": False},
            )
            axes.move_to(np.array([2.1, 0.2, 0.0]))

            x_label = MathTex(r"\nu\ (10^{14}\ \mathrm{Hz})", color=WHITE, font_size=28)
            x_label.next_to(axes.x_axis, RIGHT, buff=0.15)
            y_label = MathTex(r"I(\nu)", color=WHITE, font_size=30)
            y_label.next_to(axes.y_axis, UP, buff=0.15)

            # Pre-build static curves (used multiple times via Transform)
            planck_curve = axes.plot(planck_norm, x_range=[0.2, 9.5, 0.05],
                                     color=COLOR_PLANCK, stroke_width=4)
            rj_curve = axes.plot(rj_norm, x_range=[0.0, 9.5, 0.05],
                                 color=COLOR_CLASSICAL, stroke_width=3)

            planck_area = axes.get_area(planck_curve, x_range=[0.2, 9.5, 0.05],
                                        color=COLOR_PLANCK, opacity=0.35)

            # Vertical sweep line (for A3.B2)
            sweep_tracker = ValueTracker(0.0)

            def make_sweep_line():
                x_val = sweep_tracker.get_value()
                line = DashedLine(
                    axes.c2p(x_val, 0),
                    axes.c2p(x_val, 1.05),
                    color=COLOR_ACCENT,
                    stroke_width=2,
                    dash_length=0.08,
                )
                return line

            sweep_line = always_redraw(make_sweep_line)

            # ============================================================
            # BEAT A1.B1 | 0.00-4.00 s
            # ============================================================
            # Animate the ingot heating from dark to glowing orange
            hot_color = rgb_to_color([0xFF / 255, 0x8C / 255, 0x00 / 255])

            self.play(
                FadeIn(hotplate, shift=UP * 0.2),
                FadeIn(ingot, scale=0.6),
                FadeIn(ingot_label, shift=UP * 0.1),
                run_time=0.7,
            )
            self.play(
                ingot.animate.set_fill(hot_color, opacity=1.0),
                T_tracker.animate.set_value(5800.0),
                FadeIn(T_eq_label, shift=DOWN * 0.1),
                FadeIn(T_readout, shift=DOWN * 0.1),
                FadeIn(T_unit, shift=DOWN * 0.1),
                run_time=3.3,
                rate_func=rate_functions.ease_in_out_cubic,
            )

            # ============================================================
            # BEAT A2.B1 | 4.00-10.00 s
            # ============================================================
            # Short equation tag near the rising classical curve
            rj_tag = MathTex(
                r"I_{\mathrm{RJ}}(\nu)=\frac{8\pi\nu^{2}kT}{c^{3}}",
                color=COLOR_CLASSICAL, font_size=26,
            )
            rj_tag.next_to(axes, UP, buff=0.25).align_to(axes, LEFT).shift(RIGHT * 0.2)

            # Build axes, both curves, and tag simultaneously
            self.play(
                Create(axes, lag_ratio=0.0),
                FadeIn(x_label, shift=LEFT * 0.2),
                FadeIn(y_label, shift=DOWN * 0.2),
                Create(rj_curve),
                Create(planck_curve),
                FadeIn(rj_tag, shift=DOWN * 0.1),
                run_time=5.3,
                rate_func=rate_functions.smooth,
            )
            self.wait(0.7)

            # ============================================================
            # BEAT A3.B1 | 10.00-14.00 s
            # ============================================================
            # Larger, runaway classical curve (same functional form, much bigger)
            def rj_runaway(nu_14):
                return rj_norm(nu_14) * 5.5

            # Clip the curve to the visible axes range (still leaves the runaway impression)
            runaway_curve_clip = axes.plot(
                lambda nu: min(rj_runaway(nu), 1.18),
                x_range=[0.0, 9.5, 0.05],
                color=COLOR_CLASSICAL, stroke_width=3,
            )

            catastrophe = Text("ULTRAVIOLET CATASTROPHE", color=RED, font_size=28, weight=BOLD)
            catastrophe.move_to(np.array([3.6, 2.6, 0.0]))

            # A growing y_max readout (ValueTracker-driven) — small live value
            ymax_tracker = ValueTracker(0.5)
            ymax_readout = DecimalNumber(0.5, num_decimal_places=2,
                                         color=RED, font_size=26)
            ymax_readout.add_updater(lambda m: m.set_value(ymax_tracker.get_value()))
            ymax_readout.next_to(catastrophe, DOWN, buff=0.18)

            # Remove the moderate rj_curve and bring in the runaway + catastrophe + readout
            self.remove(rj_curve)
            self.play(
                FadeIn(runaway_curve_clip, lag_ratio=0.0),
                FadeIn(catastrophe, shift=DOWN * 0.2),
                FadeIn(ymax_readout, shift=UP * 0.1),
                ymax_tracker.animate.set_value(4.85),
                run_time=3.4,
                rate_func=rate_functions.ease_in_quad,
            )
            self.wait(0.6)

            # ============================================================
            # BEAT A3.B2 | 14.00-18.00 s
            # ============================================================
            # Remove the runaway visualization clutter; keep a moderate rj curve
            rj_moderate = axes.plot(rj_norm, x_range=[0.0, 9.5, 0.05],
                                    color=COLOR_CLASSICAL, stroke_width=3)

            # A small flash of E = h nu next to the dashed line at the end of sweep
            ehv_marker = MathTex(r"h\nu", color=COLOR_ACCENT, font_size=32)
            ehv_marker.next_to(axes.c2p(8.0, 1.05), UP, buff=0.1)

            # Combined transition + counter + sweep + marker beats
            self.play(
                FadeOut(catastrophe, shift=UP * 0.2),
                FadeOut(ymax_readout, shift=UP * 0.2),
                FadeOut(runaway_curve_clip, shift=DOWN * 0.1),
                FadeIn(rj_moderate, lag_ratio=0.0),
                FadeIn(photon_label, shift=RIGHT * 0.2),
                FadeIn(photon_readout, shift=UP * 0.2),
                FadeIn(photon_caption, shift=LEFT * 0.1),
                run_time=0.7,
            )

            # Add the dashed sweep line (always_redraw attached to tracker)
            self.add(sweep_line)
            # Sweep along the x-axis; bump the photon counter; reveal E=hν marker
            sweep_duration = 3.2
            self.play(
                sweep_tracker.animate.set_value(8.0),
                photon_tracker.animate.set_value(8.0),
                FadeIn(ehv_marker, shift=DOWN * 0.15),
                run_time=sweep_duration,
                rate_func=linear,
            )

            # ============================================================
            # BEAT A4.B1 | 18.00-23.00 s
            # ============================================================
            # Arrow annotation: "peaks near 5.9 x 10^14 Hz — solar visible"
            peak_point = axes.c2p(5.9, planck_norm(5.9))
            arrow = Arrow(
                start=peak_point + UP * 0.9 + RIGHT * 0.1,
                end=peak_point + UP * 0.15,
                color=COLOR_ACCENT, stroke_width=3, max_tip_length_to_length_ratio=0.18,
                buff=0.0,
            )
            peak_label = Text(
                "peaks near 5.9\u00d710\u00b9\u2074 Hz \u2014 solar visible",
                color=COLOR_ACCENT, font_size=22,
            )
            peak_label.next_to(arrow.get_start(), UP, buff=0.15)

            # Clear sweep + marker, fill area, grow arrow + label in one beat
            self.play(
                FadeOut(sweep_line),
                FadeOut(ehv_marker, shift=UP * 0.2),
                FadeIn(planck_area, lag_ratio=0.0),
                GrowArrow(arrow),
                FadeIn(peak_label, shift=DOWN * 0.15),
                run_time=1.0,
            )
            # Hold the hero composition
            self.wait(4.0)

            # ============================================================
            # BEAT A4.B2 | 23.00-26.00 s
            # ============================================================
            # The Rayleigh-Jeans curve shrinks to a small purple segment near the origin
            rj_lowfreq = axes.plot(
                lambda nu: rj_norm(nu) * 0.35,
                x_range=[0.0, 2.5, 0.05],
                color=PURPLE, stroke_width=3,
            )

            self.play(
                FadeOut(rj_moderate, shift=DOWN * 0.2),
                FadeIn(rj_lowfreq, lag_ratio=0.0),
                FadeOut(arrow),
                FadeOut(peak_label, shift=UP * 0.2),
                run_time=0.6,
            )
            rj_lowfreq.set_opacity(0.15)
            self.wait(2.4)

            # ============================================================
            # BEAT A5.B1 | 26.00-30.00 s
            # ============================================================
            # Clear the hero composition; type the final Planck's law equation
            planck_tag = Text("Planck's law", color=COLOR_ACCENT, font_size=28, weight=BOLD)
            planck_eq = MathTex(
                r"B(\lambda,T)=\frac{2hc^{2}}{\lambda^{5}}\frac{1}{e^{hc/\lambda kT}-1}",
                color=WHITE, font_size=36,
            )
            recap_block = VGroup(planck_tag, planck_eq).arrange(DOWN, buff=0.2)
            # Center the ingot and counter for the recap
            recap_group = VGroup(ingot, ingot_label, hotplate, T_group, photon_group)
            recap_block.next_to(recap_group, DOWN, buff=0.6)
            if recap_block.get_width() > frame_w - 1:
                recap_block.scale_to_fit_width(frame_w - 1)
            recap_block.move_to(np.array([0.0, -2.6, 0.0]))

            # Idle-loop: gentle breathing of T between 5799 and 5801 with a
            # tiny embers shimmer on the ingot's fill color.
            T_breath = ValueTracker(0.0)

            def ingot_shimmer():
                phase = math.sin(T_breath.get_value() * 1.7)
                r = 0xFF / 255
                g = (0x8C + 12 * phase) / 255
                b = (0x00 + 6 * phase) / 255
                g = max(0.0, min(1.0, g))
                b = max(0.0, min(1.0, b))
                ingot.set_fill(rgb_to_color([r, g, b]), opacity=1.0)
                return ingot

            shimmer_handle = always_redraw(ingot_shimmer)

            def breath_readout():
                return int(round(5800.0 + math.sin(T_breath.get_value()) * 1.0))

            breath_number = Integer(5800, color=COLOR_ACCENT, font_size=44)
            breath_number.add_updater(lambda m: m.set_value(breath_readout()))
            breath_number.move_to(T_readout.get_center())

            # Replace the static ingot with a shimmering one, and swap the
            # DecimalNumber for a breathing Integer.
            T_readout.clear_updaters()
            photon_readout.clear_updaters()
            self.remove(T_readout)
            self.add(breath_number)
            self.add(shimmer_handle)

            # Combined hero-clear + final-equation beat, then idle breath
            self.play(
                FadeOut(planck_area),
                FadeOut(planck_curve, shift=UP * 0.2),
                FadeOut(rj_lowfreq),
                FadeOut(rj_tag),
                FadeOut(x_label),
                FadeOut(y_label),
                FadeOut(axes),
                FadeIn(planck_tag, shift=UP * 0.2),
                Write(planck_eq),
                run_time=2.0,
            )
            # Run the idle loop for the remaining time
            self.play(T_breath.animate.set_value(2.0 * math.pi), run_time=2.0, rate_func=linear)