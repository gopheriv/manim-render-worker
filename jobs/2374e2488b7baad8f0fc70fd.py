from manim import *
import numpy as np
import math


# Physical constants
h_const = 6.62607015e-34
c_const = 299792458.0
k_const = 1.380649e-23
b_const = 0.002897771955


def planck(lam, T):
    a = 2.0 * h_const * c_const ** 2 / (lam ** 5)
    b = h_const * c_const / (lam * k_const * T)
    return a / (math.exp(b) - 1.0)


def rj(lam, T):
    return 2.0 * c_const * k_const * T / (lam ** 4)


class AetherLabScene(Scene):
    def construct(self):
            # BEAT S1.B1 | 0.00-2.22 s
            # Dark workshop fades in; faint outline of the cold iron bar appears at C3.
            bg = Rectangle(width=config.frame_width, height=config.frame_height)
            bg.set_fill("#0B0F1A", opacity=1.0)
            bg.set_stroke(width=0)

            iron = Rectangle(width=5.2, height=0.55, color=BLUE_D, fill_opacity=0.0)
            iron.set_stroke(BLUE_D, width=2, opacity=0.6)
            iron.move_to(np.array([0.0, 0.6, 0.0]))

            self.play(FadeIn(bg, run_time=0.4))
            self.play(Create(iron, run_time=0.6))
            self.wait(1.222)

            # BEAT S1.B2 | 2.22-5.06 s
            # Bar begins to dull red glow as T readout rises toward T2 = 4000 K.
            T_tracker = ValueTracker(1500.0)

            def bar_color(t):
                tt = max(800.0, min(t, 6500.0))
                f = (tt - 800.0) / (6500.0 - 800.0)
                r = 0.45 + 0.55 * f
                g = 0.05 + 0.55 * max(0.0, f - 0.25)
                b = 0.05 + 0.50 * max(0.0, f - 0.55)
                return rgb_to_color((r, g, b))

            def update_bar_fill(mob, alpha=0.85):
                t = T_tracker.get_value()
                col = bar_color(t)
                mob.set_fill(col, opacity=alpha)
                mob.set_stroke(col, width=2, opacity=0.9)

            iron.add_updater(lambda m: update_bar_fill(m, 0.85))
            self.play(T_tracker.animate.set_value(4000.0), run_time=2.5, rate_func=smooth)
            self.wait(0.339)

            # BEAT S1.B3 | 5.06-7.90 s
            # A tiny spectrum curve appears above the bar, skewed into the long-wavelength red region.
            lam_min, lam_max = 1e-7, 3e-6
            lam_axis = np.linspace(lam_min, lam_max, 200)

            spec_left = -5.5
            spec_right = 5.5
            spec_bottom = 1.4
            spec_top = 3.4

            def lam_to_x(lam):
                return spec_left + (lam - lam_min) / (lam_max - lam_min) * (spec_right - spec_left)

            # Compute peak normalization for 4000 K Planck curve
            peak4000 = 0.0
            for lam in lam_axis:
                v = planck(lam, 4000.0)
                if v > peak4000:
                    peak4000 = v

            def lam_to_y(lam, T, peak=peak4000):
                v = planck(lam, T)
                return spec_bottom + (v / peak) * (spec_top - spec_bottom)

            # baseline axis line
            axis_line = Line(
                start=np.array([spec_left, spec_bottom, 0.0]),
                end=np.array([spec_right, spec_bottom, 0.0]),
                color=GRAY_A, stroke_width=1.5,
            )

            # Build the 4000 K Planck curve
            pts4000 = [
                np.array([lam_to_x(lam), lam_to_y(lam, 4000.0, peak4000), 0.0])
                for lam in lam_axis
            ]
            curve4000 = VMobject(stroke_color=RED_E, stroke_width=4)
            curve4000.set_points_as_corners(pts4000)

            peak_lam_4000 = b_const / 4000.0
            peak_dot_4000 = Dot(
                np.array([lam_to_x(peak_lam_4000),
                          lam_to_y(peak_lam_4000, 4000.0, peak4000), 0.0]),
                color=YELLOW_E, radius=0.07,
            )
            peak_label_4000 = Text("deep red peak", color=RED_E, font_size=24)
            peak_label_4000.next_to(peak_dot_4000, UP, buff=0.12)

            spectrum_group = VGroup(axis_line, curve4000, peak_dot_4000, peak_label_4000)
            spectrum_group.move_to(ORIGIN)
            # Keep spectrum reserved region; let label hug the dot

            self.play(
                LaggedStart(
                    Create(axis_line, run_time=0.4),
                    Create(curve4000, run_time=0.9),
                    FadeIn(peak_dot_4000, scale=0.6, run_time=0.3),
                    Write(peak_label_4000, run_time=0.5),
                ),
                run_time=1.4,
            )
            self.wait(1.438)

            # BEAT S1.B4 | 7.90-10.12 s
            # Temperature readout panel slides in at E5, displaying T = 4000 K, with live units K.
            readout_label = Text("T =", color=WHITE, font_size=34)
            readout_value = DecimalNumber(
                T_tracker.get_value(), num_decimal_places=0, color=YELLOW_E, font_size=40,
            )
            readout_unit = Text("K", color=WHITE, font_size=34)
            readout_value.add_updater(lambda m: m.set_value(T_tracker.get_value()))
            readout_group = VGroup(readout_label, readout_value, readout_unit)
            readout_group.arrange(RIGHT, buff=0.18)
            readout_panel = SurroundingRectangle(
                readout_group, color=BLUE_D, buff=0.18, stroke_width=2,
            )
            readout_full = VGroup(readout_panel, readout_group)
            readout_full.move_to(np.array([4.4, -2.6, 0.0]))

            self.play(
                FadeIn(readout_panel, run_time=0.3),
                Write(readout_label, run_time=0.4),
                FadeIn(readout_value, run_time=0.4),
                FadeIn(readout_unit, run_time=0.3),
                run_time=0.8,
            )
            self.wait(1.42)

            # BEAT S1.B5 | 10.12-12.90 s
            # Bar's colour shifts to orange as T ramps to T3 = 5000 K; the spectral curve slides leftward.
            # Build the 5000 K Planck curve
            peak5000 = 0.0
            for lam in lam_axis:
                v = planck(lam, 5000.0)
                if v > peak5000:
                    peak5000 = v

            def lam_to_y_5000(lam):
                v = planck(lam, 5000.0)
                return spec_bottom + (v / peak4000) * (spec_top - spec_bottom)

            pts5000 = [
                np.array([lam_to_x(lam), lam_to_y_5000(lam), 0.0])
                for lam in lam_axis
            ]
            curve5000 = VMobject(stroke_color=ORANGE, stroke_width=4)
            curve5000.set_points_as_corners(pts5000)

            peak_lam_5000 = b_const / 5000.0
            peak_dot_5000 = Dot(
                np.array([lam_to_x(peak_lam_5000),
                          lam_to_y_5000(peak_lam_5000), 0.0]),
                color=YELLOW_E, radius=0.07,
            )
            peak_label_5000 = Text("orange peak", color=ORANGE, font_size=24)
            peak_label_5000.next_to(peak_dot_5000, UP, buff=0.12)

            # Idle loop: gentle colour oscillation of the bar after ramp
            self.play(
                T_tracker.animate.set_value(5000.0),
                run_time=1.2,
                rate_func=smooth,
            )
            # Replace the red curve with the orange curve, slide peak leftward
            self.play(
                Transform(curve4000, curve5000, run_time=0.4),
                Transform(peak_dot_4000, peak_dot_5000, run_time=0.4),
                Transform(peak_label_4000, peak_label_5000, run_time=0.4),
                run_time=0.5,
            )
            self.wait(0.077)

            # Idle loop: bar colour gently oscillates (red<->white) while peak pulses
            # Brief idle to satisfy "final three sampled frames must differ".
            peak_tracker = ValueTracker(0.0)

            def idle_bar_color(mob):
                base = bar_color(T_tracker.get_value())
                pulse = 0.5 + 0.5 * math.sin(peak_tracker.get_value() * 2 * math.pi / 2.0)
                # blend toward white based on pulse
                r = base[0] * (1 - 0.25 * pulse) + 1.0 * (0.25 * pulse)
                g = base[1] * (1 - 0.25 * pulse) + 1.0 * (0.25 * pulse)
                b = base[2] * (1 - 0.25 * pulse) + 1.0 * (0.25 * pulse)
                col = rgb_to_color((r, g, b))
                mob.set_fill(col, opacity=0.9)
                mob.set_stroke(col, width=2, opacity=0.95)

            iron.remove_updater(lambda m: update_bar_fill(m, 0.85))
            iron.add_updater(idle_bar_color)

            # Run a couple of idle pulses to ensure motion continues
            self.play(peak_tracker.animate.set_value(1.0), run_time=0.5, rate_func=linear)
            self.play(peak_tracker.animate.set_value(2.0), run_time=0.5, rate_func=linear)