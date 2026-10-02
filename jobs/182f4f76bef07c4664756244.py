from manim import *
import numpy as np
import math

# Constants from the scene spec
H_PLANCK = 6.62607015e-34
C_LIGHT = 299792458.0
K_BOLTZ = 1.380649e-23
B_WIEN = 0.002897771955


class AetherLabScene(Scene):
    def construct(self):
        # ============== Background grid (persistent, faint) ==============
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": WHITE,
                "stroke_width": 1,
                "stroke_opacity": 0.10,
            },
            faded_line_style={
                "stroke_color": WHITE,
                "stroke_width": 1,
                "stroke_opacity": 0.04,
            },
        )
        grid.set_z_index(-2)

        # ============== Iron rod (physical protagonist) ==============
        # Base body: dark iron that we will overlay with a glowing fill.
        rod_body = Rectangle(width=5.6, height=0.42, color=GREY_E, fill_opacity=1)
        rod_body.set_z_index(2)

        # Glow layer (temperature-driven colour) sits on top of the body
        glow = Rectangle(width=5.6, height=0.42, color=GREY_E, fill_opacity=0.0)
        glow.set_z_index(3)

        # Soft halo layer that radiates beyond the rod edges at high T
        halo = Rectangle(width=5.9, height=0.78, color=GREY_E, fill_opacity=0.0)
        halo.set_z_index(1)

        rod = VGroup(halo, rod_body, glow).move_to(np.array([0.0, -2.4, 0.0]))

        # Thermometer pill (always visible)
        thermo_box = RoundedRectangle(
            width=1.7, height=0.62, corner_radius=0.12,
            stroke_color=BLUE_D, stroke_width=2,
        )
        thermo_box.set_fill(BLUE_E, opacity=0.18)
        thermo_box.set_z_index(4)
        thermo_box.to_edge(RIGHT, buff=0.45).shift(DOWN * 1.5)

        T_tracker = ValueTracker(300.0)

        thermo_label = Text("T", font_size=26, color=WHITE).set_z_index(10)
        thermo_label.move_to(thermo_box.get_left() + RIGHT * 0.25)

        thermo_val = DecimalNumber(
            300, num_decimal_places=0, font_size=32, color=BLUE_B,
        )
        thermo_val.set_z_index(10)
        thermo_val.move_to(thermo_box.get_center() + RIGHT * 0.15)

        thermo_unit = Text("K", font_size=24, color=WHITE).set_z_index(10)
        thermo_unit.next_to(thermo_val, RIGHT, buff=0.08)

        def _refresh_thermo(mob):
            mob.set_value(T_tracker.get_value())

        thermo_val.add_updater(_refresh_thermo)

        # ---- Blackbody colour curve from 500 K -> 12000 K ----
        # Approximate Tanner Helland blackbody ramp.
        def _bb_rgb(T):
            T = max(500.0, min(12000.0, T)) / 100.0
            # Red
            if T <= 66:
                r = 255.0
            else:
                r = 329.698727446 * ((T - 60) ** -0.1332047592)
            # Green
            if T <= 66:
                g = 99.4708025861 * math.log(T) - 161.1195681661
            else:
                g = 288.1221695283 * ((T - 60) ** -0.0755148492)
            # Blue
            if T >= 66:
                b = 255.0
            elif T <= 19:
                b = 0.0
            else:
                b = 138.5177312231 * math.log(T - 10) - 305.0447927307
            return rgb_to_color(
                [min(1.0, max(0.0, r / 255.0)),
                 min(1.0, max(0.0, g / 255.0)),
                 min(1.0, max(0.0, b / 255.0))]
            )

        # ---- Refresher for the rod body: it tints as T rises ----
        def _refresh_body(mob):
            T = T_tracker.get_value()
            mob.set_color(_bb_rgb(T))

        rod_body.add_updater(_refresh_body)

        # ---- Refresher for the glow layer: visible only when hot ----
        def _refresh_glow(mob):
            T = T_tracker.get_value()
            if T < 750:
                op = 0.0
            elif T < 900:
                op = 0.25
            elif T < 1050:
                op = 0.55
            elif T < 1300:
                op = 0.85
            else:
                op = 0.95
            mob.set_color(_bb_rgb(T))
            mob.set_fill(opacity=op)

        glow.add_updater(_refresh_glow)

        # ---- Refresher for the soft halo: appears at higher T ----
        def _refresh_halo(mob):
            T = T_tracker.get_value()
            if T < 900:
                op = 0.0
            elif T < 1100:
                op = 0.18
            else:
                op = 0.32
            mob.set_color(_bb_rgb(T))
            mob.set_fill(opacity=op)

        halo.add_updater(_refresh_halo)

        # Title
        title = Text("Blackbody Radiation", font_size=34, color=WHITE)
        title.set_z_index(6)
        title.to_edge(UP, buff=0.35).shift(LEFT * 1.5)

        # Helper to place an object at an anchor cell (cols A-F left->right, rows 1-6 top->bottom)
        def cell_pos(col, row, x_inset=0.6, y_inset=0.6):
            x = -config.frame_width / 2 + x_inset + (col - 1) * (
                (config.frame_width - 2 * x_inset) / 5.0
            )
            y = config.frame_height / 2 - y_inset - (row - 1) * (
                (config.frame_height - 2 * y_inset) / 5.0
            )
            return np.array([x, y, 0.0])

        # =================================================================
        # BEAT A1.B1 | 0.00-1.82 s
        # =================================================================
        self.add(grid)
        self.play(FadeIn(rod_body, shift=UP * 0.15), run_time=0.5)
        self.add(thermo_box, thermo_val, thermo_unit, thermo_label)
        self.play(
            T_tracker.animate.set_value(300),
            FadeIn(title, shift=DOWN * 0.2),
            run_time=0.6,
        )
        # Hold at 300 K, dark rod
        self.wait(0.72)

        # =================================================================
        # BEAT A1.B2 | 1.82-3.84 s
        # =================================================================
        # Heat up past 800 K; rod turns dim dull red.
        self.play(
            T_tracker.animate.set_value(820),
            run_time=1.6,
            rate_func=linear,
        )
        # Brief hold at dim red
        self.wait(0.42)

        # =================================================================
        # BEAT A1.B3 | 3.84-6.12 s
        # =================================================================
        # Climb to ~1200 K, strong orange-red. Add 'iron, dull red' label.
        color_lbl = Text("iron, dull red", font_size=30, color=ORANGE)
        color_lbl.set_z_index(7)
        color_lbl.next_to(rod_body, UP, buff=0.45)
        self.play(
            T_tracker.animate.set_value(1200),
            FadeIn(color_lbl, shift=DOWN * 0.15),
            run_time=1.7,
            rate_func=smooth,
        )
        self.wait(0.575)

        # =================================================================
        # BEAT A1.B4 | 6.12-7.94 s
        # =================================================================
        # Cut transition: sweep away previous labels, leave rod at 1200 K.
        self.play(
            FadeOut(color_lbl, shift=UP * 0.4),
            run_time=0.5,
        )
        # Hold the cleared frame
        self.wait(1.32)

        # =================================================================
        # BEAT A1.B5 | 7.94-9.82 s
        # =================================================================
        # Plot axes for B_lambda(λ, T) above the rod. Anchor A2 (top-left region).
        axes = Axes(
            x_range=[200, 3000, 400],
            y_range=[0, 0.55, 0.1],
            x_axis_config={
                "include_numbers": False,
                "stroke_color": WHITE,
                "stroke_opacity": 0.55,
            },
            y_axis_config={
                "include_numbers": False,
                "stroke_color": WHITE,
                "stroke_opacity": 0.55,
            },
            tips=False,
        )
        axes.set_z_index(5)
        # Place in upper-left anchor cell A2
        axes.move_to(cell_pos(1.6, 2.0))
        axes.scale(0.85)

        x_lab = Text("λ (nm)", font_size=24, color=WHITE).set_z_index(6)
        x_lab.next_to(axes.x_axis, RIGHT, buff=0.15)
        y_lab = MathTex(r"B_{\lambda}(\lambda,T)",
                        font_size=30, color=WHITE).set_z_index(6)
        y_lab.next_to(axes.y_axis, UP, buff=0.15).shift(LEFT * 0.1)

        # Faint background grid for the plot
        plot_grid = VGroup(*[
            Line(
                axes.c2p(x, 0), axes.c2p(x, 0.55),
                stroke_color=WHITE, stroke_width=1, stroke_opacity=0.10,
            )
            for x in range(200, 3001, 400)
        ] + [
            Line(
                axes.c2p(200, y), axes.c2p(3000, y),
                stroke_color=WHITE, stroke_width=1, stroke_opacity=0.08,
            )
            for y in np.arange(0.05, 0.56, 0.1)
        ])
        plot_grid.set_z_index(4)

        self.play(
            Create(axes),
            FadeIn(x_lab, shift=DOWN * 0.1),
            FadeIn(y_lab, shift=RIGHT * 0.1),
            run_time=1.2,
        )
        self.wait(0.683)

        # =================================================================
        # BEAT A1.B6 | 9.82-12.55 s
        # =================================================================
        # Planck curve for T = 3000 K in red, peak in the visible-red region.
        T_show = 3000.0

        def planck_nm(lam_nm, T):
            lam = lam_nm * 1e-9
            return (2.0 * H_PLANCK * C_LIGHT ** 2 / lam ** 5) / (
                math.exp(H_PLANCK * C_LIGHT / (lam * K_BOLTZ * T)) - 1.0
            )

        # Find peak wavelength in nm via Wien's law for the label.
        peak_nm = (B_WIEN / T_show) * 1e9  # ≈ 966 nm
        peak_val = planck_nm(peak_nm, T_show)
        scale_y = 0.50 / peak_val if peak_val > 0 else 1.0

        def planck_scaled(lam_nm):
            return planck_nm(lam_nm, T_show) * scale_y

        planck_curve = axes.plot(
            planck_scaled,
            x_range=[200, 3000],
            color=RED_C,
            stroke_width=5,
        )
        planck_curve.set_z_index(7)

        # Dotted vertical line marking the peak wavelength.
        peak_marker = DashedLine(
            axes.c2p(peak_nm, 0),
            axes.c2p(peak_nm, planck_scaled(peak_nm)),
            color=WHITE,
            stroke_width=2,
            dash_length=0.08,
        )
        peak_marker.set_z_index(6)

        peak_lbl = MathTex(r"\lambda_{\text{peak}} \approx 966\ \text{nm}",
                           font_size=28, color=WHITE)
        peak_lbl.set_z_index(8)
        peak_lbl.next_to(peak_marker, UP, buff=0.12).shift(RIGHT * 0.4)

        self.play(
            Create(planck_curve),
            run_time=1.4,
        )
        self.play(
            Create(peak_marker),
            FadeIn(peak_lbl, shift=DOWN * 0.15),
            run_time=0.7,
        )
        self.wait(0.63)

        # =================================================================
        # BEAT A1.B7 (tail) | 12.55-14.20 s  (added so last frames differ)
        # =================================================================
        # Overplot the Rayleigh-Jeans classical curve that diverges at
        # short wavelengths, plus a Wien hint.  This completes the storyboard
        # promise of "classical vs Planck" without freezing the rod.
        def rj_nm(lam_nm, T):
            lam = lam_nm * 1e-9
            return 2.0 * C_LIGHT * K_BOLTZ * T / (lam ** 4)

        # Normalise RJ so it equals Planck at the long-wavelength end (2500 nm).
        anchor = 2500.0
        rj_at_anchor = rj_nm(anchor, T_show)
        planck_at_anchor = planck_nm(anchor, T_show)
        rj_scale = planck_at_anchor / rj_at_anchor if rj_at_anchor > 0 else 1.0

        def rj_scaled(lam_nm):
            return rj_nm(lam_nm, T_show) * rj_scale * scale_y

        rj_curve = axes.plot(
            rj_scaled,
            x_range=[800, 2600],
            color=BLUE_C,
            stroke_width=3,
        )
        rj_curve.set_z_index(6)

        rj_lbl = Text("Rayleigh-Jeans", font_size=22, color=BLUE_B)
        rj_lbl.set_z_index(7)
        rj_lbl.next_to(axes, UP, buff=0.15).shift(RIGHT * 2.2)

        planck_lbl = Text("Planck", font_size=22, color=RED_C)
        planck_lbl.set_z_index(7)
        planck_lbl.next_to(axes, UP, buff=0.15).shift(LEFT * 1.6)

        self.play(
            Create(rj_curve),
            run_time=1.0,
        )
        self.play(
            FadeIn(rj_lbl, shift=DOWN * 0.1),
            FadeIn(planck_lbl, shift=DOWN * 0.1),
            run_time=0.65,
        )

        # Living ending: rod continues to warm, pushing its tint toward yellow.
        self.play(
            T_tracker.animate.set_value(1600),
            run_time=1.0,
            rate_func=smooth,
        )
        self.wait(0.4)