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


# Display window (meters) — visible / IR / near-UV
LAM_MIN = 2e-7
LAM_MAX = 3.5e-6
N_PTS = 240


def planck_curve_mobject(T, peak_ref, color, x_left, x_right, y_bot, y_top,
                         lam_min=LAM_MIN, lam_max=LAM_MAX, stroke_w=4):
    lam = np.linspace(lam_min, lam_max, N_PTS)
    vals = np.array([planck(l, T) for l in lam])
    pts = []
    for li, v in zip(lam, vals):
        x = x_left + (li - lam_min) / (lam_max - lam_min) * (x_right - x_left)
        y = y_bot + (v / peak_ref) * (y_top - y_bot)
        pts.append(np.array([x, y, 0.0]))
    mob = VMobject(stroke_color=color, stroke_width=stroke_w)
    mob.set_points_as_corners(pts)
    return mob, lam, vals


def rj_curve_mobject(T, peak_ref, color, x_left, x_right, y_bot, y_top,
                     lam_min=LAM_MIN, lam_max=LAM_MAX, stroke_w=3):
    lam = np.linspace(lam_min, lam_max, N_PTS)
    vals = np.array([rj(l, T) for l in lam])
    # Clamp the UV catastrophe tail so it stays inside the panel
    vals = np.minimum(vals, peak_ref * 3.0)
    pts = []
    for li, v in zip(lam, vals):
        x = x_left + (li - lam_min) / (lam_max - lam_min) * (x_right - x_left)
        y = y_bot + (v / peak_ref) * (y_top - y_bot)
        pts.append(np.array([x, y, 0.0]))
    mob = VMobject(stroke_color=color, stroke_width=stroke_w)
    mob.set_points_as_corners(pts)
    return mob


class AetherLabScene(Scene):
    def construct(self):
        # ---------- Stage geometry ----------
        frame_w = config.frame_width
        frame_h = config.frame_height

        # Layout regions (so nothing overlaps and nothing hugs the top edge)
        # Bar sits in the lower-middle of the screen
        bar_center_y = -1.6
        bar_width = 6.4
        bar_height = 0.7

        # Spectrum panel sits above the bar
        spec_left = -5.6
        spec_right = 5.6
        spec_bottom = 0.1
        spec_top = 2.6

        # ---------- Background ----------
        bg = Rectangle(width=frame_w, height=frame_h)
        bg.set_fill("#0B0F1A", opacity=1.0)
        bg.set_stroke(width=0)

        # Faint workshop grid (scaffolding, not dominant)
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            x_length=frame_w * 0.98,
            y_length=frame_h * 0.98,
            background_line_style={"stroke_color": "#1A2236", "stroke_width": 1, "stroke_opacity": 0.35},
            faded_line_style={"stroke_color": "#1A2236", "stroke_width": 0.5, "stroke_opacity": 0.15},
            axis_config={"stroke_opacity": 0.0},
        )
        grid.set_z_index(-2)

        # ---------- Iron bar ----------
        iron = Rectangle(
            width=bar_width, height=bar_height,
            stroke_width=2,
        )
        iron.move_to(np.array([0.0, bar_center_y, 0.0]))
        iron.set_fill(BLUE_D, opacity=0.0)
        iron.set_stroke(BLUE_D, width=2, opacity=0.7)

        # ---------- Color helper ----------
        T_tracker = ValueTracker(800.0)

        def blackbody_rgb(tt):
            # Clamp temperature and map to a physically reasonable blackbody color
            tt = max(800.0, min(tt, 12000.0))
            f = (tt - 800.0) / (12000.0 - 800.0)
            r = 0.18 + 0.82 * f
            g = 0.02 + 0.85 * max(0.0, f - 0.20)
            b = 0.02 + 0.90 * max(0.0, f - 0.55)
            # Boost saturation a touch in the midrange
            if 0.15 < f < 0.75:
                g = min(1.0, g * 1.05)
            return rgb_to_color((min(1.0, r), min(1.0, g), min(1.0, b)))

        # NOTE: No updater on the bar. The bar's color is driven explicitly by
        # animating T_tracker and applying the result to the mobject at each
        # call site. An updater was the source of the "zip() argument 2 is
        # longer than argument 1" crash because Transform/ReplaceTransform of
        # the bar's filled sub-mobjects changed their family while T_tracker
        # was being animated.

        # ---------- Spectrum panel scaffolding ----------
        axis_line = Line(
            start=np.array([spec_left, spec_bottom, 0.0]),
            end=np.array([spec_right, spec_bottom, 0.0]),
            color=GRAY_A, stroke_width=1.8,
        )
        # End caps
        cap_l = Line(
            np.array([spec_left, spec_bottom - 0.08, 0.0]),
            np.array([spec_left, spec_bottom + 0.08, 0.0]),
            color=GRAY_A, stroke_width=1.5,
        )
        cap_r = Line(
            np.array([spec_right, spec_bottom - 0.08, 0.0]),
            np.array([spec_right, spec_bottom + 0.08, 0.0]),
            color=GRAY_A, stroke_width=1.5,
        )

        # Wavelength tick marks (nm): 400, 500, 600, 700, 1000, 1500, 2500
        tick_specs = [400, 500, 600, 700, 1000, 1500, 2500]  # nm
        ticks = VGroup()
        tick_labels = VGroup()
        for nm in tick_specs:
            lam = nm * 1e-9
            x = spec_left + (lam - LAM_MIN) / (LAM_MAX - LAM_MIN) * (spec_right - spec_left)
            t = Line(
                np.array([x, spec_bottom - 0.06, 0.0]),
                np.array([x, spec_bottom + 0.06, 0.0]),
                color=GRAY_B, stroke_width=1.2,
            )
            ticks.add(t)
            lbl = Text(f"{nm}", color=GRAY_B, font_size=16)
            lbl.next_to(t, DOWN, buff=0.08)
            tick_labels.add(lbl)
        axis_label = Text("wavelength λ (nm)", color=GRAY_A, font_size=20)
        axis_label.next_to(tick_labels, DOWN, buff=0.15)

        spectrum_scaffold = VGroup(
            axis_line, cap_l, cap_r, ticks, tick_labels, axis_label,
        )

        # ---------- Wavelength-to-x helper (panel-local) ----------
        def lam_to_x(lam):
            return spec_left + (lam - LAM_MIN) / (LAM_MAX - LAM_MIN) * (spec_right - spec_left)

        # ---------- Reference peak: scale all curves so the 5000 K Planck fits nicely ----------
        lam_arr = np.linspace(LAM_MIN, LAM_MAX, N_PTS)
        peak_5000 = max(planck(l, 5000.0) for l in lam_arr)
        # Y mapping uses 5000 K peak as reference
        def lam_to_y(lam, T, peak_ref=peak_5000):
            v = planck(lam, T)
            return spec_bottom + (v / peak_ref) * (spec_top - spec_bottom)

        # ---------- BEAT S1.B1 | 0.00-2.22 s ----------
        # Dark workshop fades in; faint outline of the cold iron bar appears at C3.
        self.play(FadeIn(bg, run_time=0.3))
        self.play(FadeIn(grid, run_time=0.4))
        self.play(Create(iron, run_time=0.6))
        # Subtle title card (small, in a corner — not a hero element)
        title = Text("Blackbody Radiation", color=GRAY_A, font_size=22)
        title.to_corner(UL, buff=0.35)
        self.play(FadeIn(title, run_time=0.4))
        self.wait(0.52)

        # ---------- BEAT S1.B2 | 2.22-5.06 s ----------
        # Bar warms from cold to deep red; readout panel slides in.
        # Wavelength axis & ticks appear so the curve has a real frame.
        self.play(
            LaggedStart(
                Create(axis_line, run_time=0.35),
                FadeIn(cap_l, run_time=0.2),
                FadeIn(cap_r, run_time=0.2),
                LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.08, run_time=0.5),
                LaggedStart(*[FadeIn(lbl) for lbl in tick_labels], lag_ratio=0.08, run_time=0.5),
                FadeIn(axis_label, run_time=0.3),
            ),
            run_time=1.1,
        )

        # Temperature readout panel (kept, but relocated above the bar, not bottom-right)
        readout_label = Text("T =", color=WHITE, font_size=30)
        readout_value = DecimalNumber(
            T_tracker.get_value(), num_decimal_places=0, color=YELLOW_E, font_size=36,
        )
        readout_unit = Text("K", color=WHITE, font_size=30)
        readout_value.add_updater(lambda m: m.set_value(T_tracker.get_value()))
        readout_group = VGroup(readout_label, readout_value, readout_unit)
        readout_group.arrange(RIGHT, buff=0.15)
        readout_panel = SurroundingRectangle(
            readout_group, color=BLUE_D, buff=0.18, stroke_width=2,
        )
        readout_full = VGroup(readout_panel, readout_group)
        readout_full.to_corner(UR, buff=0.4)

        # Warm the bar from cold (800 K) up to 4000 K. Drive the bar color
        # explicitly via a function updater that reads T_tracker; do not
        # attach an updater that mutates the iron's submobject family
        # concurrently with the tracker's animation.
        bar_anim_updater = lambda mob: (
            mob.set_fill(blackbody_rgb(T_tracker.get_value()), opacity=0.95),
            mob.set_stroke(blackbody_rgb(T_tracker.get_value()), width=2, opacity=1.0),
        )
        iron.add_updater(bar_anim_updater)
        # Snap the bar to the starting temperature before animating
        bar_anim_updater(iron)
        self.play(
            T_tracker.animate.set_value(4000.0),
            FadeIn(readout_panel, run_time=0.4),
            Write(readout_label, run_time=0.35),
            FadeIn(readout_value, run_time=0.35),
            FadeIn(readout_unit, run_time=0.25),
            run_time=1.6,
            rate_func=smooth,
        )
        # Detach the updater now that the warm-up animation is done
        iron.remove_updater(bar_anim_updater)
        self.wait(0.123)

        # ---------- BEAT S1.B3 | 5.06-7.90 s ----------
        # Planck curve at 4000 K draws in above the bar (with clearance).
        curve4000, lam_a, vals_a = planck_curve_mobject(
            4000.0, peak_5000, RED_E,
            spec_left, spec_right, spec_bottom, spec_top,
            stroke_w=4.5,
        )
        peak_lam_4000 = b_const / 4000.0
        peak_x_4000 = lam_to_x(peak_lam_4000)
        peak_y_4000 = lam_to_y(peak_lam_4000, 4000.0)
        peak_dot_4000 = Dot(
            np.array([peak_x_4000, peak_y_4000, 0.0]),
            color=YELLOW_E, radius=0.08,
        )
        peak_label_4000 = Text("deep red peak", color=RED_E, font_size=22)
        # Place label BELOW the dot so it cannot clip the top frame
        peak_label_4000.next_to(peak_dot_4000, DOWN, buff=0.18)
        # Tiny Wien annotation tucked under the label
        wien_text_4000 = Text("λ_max ≈ 725 nm", color=GRAY_B, font_size=16)
        wien_text_4000.next_to(peak_label_4000, DOWN, buff=0.06)

        self.play(
            Create(curve4000, run_time=1.0),
            FadeIn(peak_dot_4000, scale=0.5, run_time=0.3),
            run_time=1.0,
        )
        self.play(
            Write(peak_label_4000, run_time=0.4),
            FadeIn(wien_text_4000, run_time=0.3),
            run_time=0.5,
        )
        self.wait(1.327)

        # ---------- BEAT S1.B4 | 7.90-10.12 s ----------
        # Rayleigh–Jeans comparison: dashed purple curve appears alongside the 4000 K Planck.
        rj_curve_4000 = rj_curve_mobject(
            4000.0, peak_5000, PURPLE_D,
            spec_left, spec_right, spec_bottom, spec_top,
            stroke_w=3,
        )
        rj_curve_4000.set_stroke(opacity=0.0)  # start invisible, dashed-line look via dash
        rj_legend = Text("Rayleigh–Jeans (classical)", color=PURPLE_D, font_size=18)
        rj_legend.next_to(readout_full, DOWN, buff=0.25).align_to(readout_full, RIGHT)

        # Dashed effect: stroke a copy as dashes
        dashed_rj = DashedVMobject(rj_curve_4000, num_dashes=70, dashed_ratio=0.55)
        dashed_rj.set_stroke(PURPLE_E, width=2.5, opacity=0.95)

        self.play(
            Create(dashed_rj, run_time=0.8),
            FadeIn(rj_legend, run_time=0.4),
            run_time=0.9,
        )

        # Highlight the UV divergence: a glowing arrow + "UV catastrophe" tag on the right tail
        uv_x = lam_to_x(2.5e-6)  # far-right of the panel
        uv_arrow = Arrow(
            start=np.array([uv_x - 0.4, spec_top - 0.15, 0.0]),
            end=np.array([uv_x - 0.05, spec_bottom + 1.5, 0.0]),
            color=PURPLE_E, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.15,
        )
        uv_tag = Text("UV catastrophe", color=PURPLE_E, font_size=20)
        uv_tag.next_to(uv_arrow, RIGHT, buff=0.1)

        self.play(
            GrowArrow(uv_arrow, run_time=0.5),
            FadeIn(uv_tag, run_time=0.3),
            run_time=0.7,
        )
        self.wait(0.207)

        # ---------- BEAT S1.B5 | 10.12-12.90 s ----------
        # Planck reveal: T ramps to 5000 K, Planck curve re-draws and fits inside the panel,
        # Rayleigh–Jeans curve stays diverging to dramatize the taming of the UV catastrophe.

        # Build a 5000 K Planck curve
        curve5000, lam_b, vals_b = planck_curve_mobject(
            5000.0, peak_5000, YELLOW_E,
            spec_left, spec_right, spec_bottom, spec_top,
            stroke_w=4.5,
        )
        peak_lam_5000 = b_const / 5000.0
        peak_x_5000 = lam_to_x(peak_lam_5000)
        peak_y_5000 = lam_to_y(peak_lam_5000, 5000.0)
        peak_dot_5000 = Dot(
            np.array([peak_x_5000, peak_y_5000, 0.0]),
            color=YELLOW_E, radius=0.08,
        )
        peak_label_5000 = Text("yellow peak", color=YELLOW_E, font_size=22)
        peak_label_5000.next_to(peak_dot_5000, DOWN, buff=0.18)
        wien_text_5000 = Text("λ_max ≈ 580 nm", color=GRAY_B, font_size=16)
        wien_text_5000.next_to(peak_label_5000, DOWN, buff=0.06)

        # Equation card (Planck's law) — small, bottom-left, faint
        planck_eq = MathTex(
            r"B_\lambda(T)=\frac{2hc^2/\lambda^5}{e^{hc/\lambda k_B T}-1}",
            color=GRAY_A, font_size=26,
        )
        planck_eq.to_corner(DL, buff=0.45)

        # Bar warms further into yellow. Re-attach the updater only for the
        # duration of the temperature animation, then remove it before any
        # subsequent Transform that could touch the bar's family.
        iron.add_updater(bar_anim_updater)
        self.play(
            T_tracker.animate.set_value(5000.0),
            run_time=0.8,
            rate_func=smooth,
        )
        iron.remove_updater(bar_anim_updater)

        # Transform the 4000 K Planck curve into the 5000 K curve (peak slides left, height grows)
        self.play(
            Transform(curve4000, curve5000, run_time=0.6),
            Transform(peak_dot_4000, peak_dot_5000, run_time=0.4),
            run_time=0.6,
        )
        # New label color: deep red → yellow
        self.play(
            Transform(peak_label_4000, peak_label_5000, run_time=0.4),
            FadeIn(wien_text_5000, run_time=0.3),
            FadeIn(planck_eq, run_time=0.5),
            run_time=0.6,
        )

        # Final flourish: brief tick of the readout to confirm it's live, then end on a distinct frame
        iron.add_updater(bar_anim_updater)
        self.play(
            T_tracker.animate.set_value(5200.0),
            run_time=0.4,
            rate_func=smooth,
        )
        self.play(
            T_tracker.animate.set_value(5000.0),
            run_time=0.4,
            rate_func=smooth,
        )
        iron.remove_updater(bar_anim_updater)
        self.wait(0.09)

        # Clean up: ensure no updaters are left on the final state
        iron.clear_updaters()
        readout_value.clear_updaters()