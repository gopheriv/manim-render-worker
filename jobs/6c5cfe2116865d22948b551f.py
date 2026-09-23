from manim import *
import numpy as np
import math

# Physical constants (SI units) and helpers
H = 6.626e-34
C = 3.0e8
K = 1.381e-23
T_SUN = 5800.0


def planck_spectral_radiance(lam_nm, T):
    lam = lam_nm * 1e-9
    num = 2.0 * H * C * C / (lam ** 5)
    expo = H * C / (lam * K * T)
    return num / (math.exp(expo) - 1.0)


def rayleigh_jeans(lam_nm, T):
    lam = lam_nm * 1e-9
    return 2.0 * C * K * T / (lam ** 4)


def normalize_planck(lam_nm):
    vals = np.array([planck_spectral_radiance(l, T_SUN) for l in lam_nm])
    return vals / vals.max()


class AetherLabScene(Scene):
    def construct(self):
        frame_w = config.frame_width

        title = Text("Planck's Blackbody Spectrum", color="#FFD580").scale(0.42).to_edge(UP, buff=0.25)
        self.add(title)

        filament = Circle(radius=0.55, color="#FFD580", fill_opacity=0.0, stroke_width=2)
        filament.move_to(np.array([-4.6, 0.4, 0.0]))
        filament_glow = Circle(radius=0.62, color="#FFD580", fill_opacity=0.0, stroke_width=0)
        filament_glow.move_to(filament.get_center())

        temp_tracker = ValueTracker(0.0)

        temp_label = Text("T =", color="#FFD580").scale(0.32).next_to(filament, DOWN, buff=0.2).align_to(filament, LEFT)
        temp_num = Integer(0, color="#FFD580").scale(0.34).next_to(temp_label, RIGHT, buff=0.1)
        temp_unit = Text("K", color="#FFD580").scale(0.32).next_to(temp_num, RIGHT, buff=0.08)

        rad_label = Text("Radiance =", color="#FF6B6B").scale(0.30).next_to(temp_label, DOWN, buff=0.18).align_to(filament, LEFT)
        rad_num = DecimalNumber(0.0, num_decimal_places=2, color="#FF6B6B").scale(0.32).next_to(rad_label, RIGHT, buff=0.08)

        def get_filament_color():
            t = temp_tracker.get_value() / T_SUN
            t = min(max(t, 0.0), 1.0)
            r = 0.5 + 0.5 * t
            g = 0.1 + 0.85 * t
            b = 0.1 + 0.55 * t
            return rgb_to_color([r, g, b])

        # Combined updater: one updater on a VGroup (counts as one live object)
        filament_group = VGroup(filament, filament_glow)
        filament_group.add_updater(lambda m: (
            m[0].set_stroke(get_filament_color(), width=3),
            m[1].set_fill(get_filament_color(), opacity=0.18 + 0.5 * (temp_tracker.get_value() / T_SUN)),
        ))
        temp_num.add_updater(lambda m: m.set_value(int(temp_tracker.get_value())))

        axes = Axes(
            x_range=[200, 1200, 200],
            y_range=[0, 1.05, 0.25],
            x_length=5.6,
            y_length=3.4,
            tips=False,
        )
        axes.move_to(np.array([2.4, -0.2, 0.0]))
        x_label = Text("wavelength (nm)", color="#FFFFFF").scale(0.26).next_to(axes.x_axis, DOWN, buff=0.18)
        y_label = Text("spectral radiance", color="#FFFFFF").scale(0.26).next_to(axes.y_axis, LEFT, buff=0.18).rotate(90 * DEGREES)

        lam_pts = np.linspace(200, 1200, 160)
        planck_vals = normalize_planck(lam_pts)
        rj_vals_raw = np.array([rayleigh_jeans(l, T_SUN) for l in lam_pts])
        rj_clip = np.clip(rj_vals_raw, 0.0, 4.0 * planck_vals.max())
        rj_norm = np.clip(rj_clip / planck_vals.max(), 0.0, 1.15)

        planck_curve = VMobject(stroke_width=3, color="#FFD580")
        planck_curve.set_points_as_corners([axes.c2p(x, y) for x, y in zip(lam_pts, planck_vals)])
        planck_curve.make_smooth()

        rj_curve = VMobject(stroke_width=3, color="#5BA8FF")
        rj_curve.set_points_as_corners([axes.c2p(x, y) for x, y in zip(lam_pts, rj_norm)])
        rj_curve.make_smooth()

        wall = Line(axes.c2p(200, 0), axes.c2p(200, 1.15), color="#FF6B6B", stroke_width=6)
        wall_label = Text("ultraviolet catastrophe", color="#FF6B6B").scale(0.28)
        wall_label.next_to(wall.get_top(), RIGHT, buff=0.1).shift(DOWN * 0.6)

        marker_300_p = Dot(axes.c2p(300, planck_vals[np.argmin(np.abs(lam_pts - 300))]), color="#FFD580", radius=0.06)
        marker_300_rj = Dot(axes.c2p(300, rj_norm[np.argmin(np.abs(lam_pts - 300))]), color="#5BA8FF", radius=0.06)

        rad_300_label = Text("@ 300 nm", color="#FFFFFF").scale(0.22)
        rad_300_label.next_to(marker_300_p, RIGHT, buff=0.12)

        rad_at_300_num = DecimalNumber(0.0, num_decimal_places=2, color="#FFD580").scale(0.28)
        rad_at_300_num.next_to(rad_300_label, RIGHT, buff=0.08)

        # Pre-build Planck and RJ readouts as constants (avoid per-frame trig)
        planck_300_over_500 = planck_spectral_radiance(300, T_SUN) / planck_spectral_radiance(500, T_SUN)
        rj_300_over_500 = rayleigh_jeans(300, T_SUN) / planck_spectral_radiance(500, T_SUN)
        rj_300_clamped = min(8.0, rj_300_over_500)

        step_x_centers = [260, 330, 420, 520, 640, 780, 940, 1120]
        step_widths = [22, 28, 36, 44, 52, 60, 70, 80]
        steps = VGroup()
        for cx, w in zip(step_x_centers, step_widths):
            h = 0.08 + 0.22 * (1.0 - (cx - 200) / 1000.0)
            rect = Rectangle(
                width=w * (axes.x_axis.get_length() / 1000.0),
                height=h * (axes.y_axis.get_length() / 1.05),
                color="#FFD580", fill_opacity=0.35, stroke_width=1,
            )
            p_bottom = axes.c2p(cx, 0)
            rect.move_to(p_bottom + np.array([0, h * (axes.y_axis.get_length() / 1.05) * 0.5, 0]))
            steps.add(rect)
        step_caption = Text("E = n·h·ν  (discrete photon packets)", color="#FFD580").scale(0.24)
        step_caption.next_to(steps, DOWN, buff=0.15)

        hero_eq = MathTex(
            r"B_{\lambda}(T) = \frac{2hc^{2}}{\lambda^{5}} \cdot \frac{1}{e^{hc/\lambda k T} - 1}",
            color="#FFD580",
        ).scale(0.42)
        hero_eq.to_corner(UR, buff=0.4)

        wien_marker = Dot(axes.c2p(500, planck_vals[np.argmin(np.abs(lam_pts - 500))]), color="#FFD580", radius=0.09)
        wien_line = DashedLine(
            axes.c2p(500, 0),
            axes.c2p(500, planck_vals[np.argmin(np.abs(lam_pts - 500))]),
            color="#FFD580", dash_length=0.08, stroke_width=2,
        )
        wien_label = MathTex(r"\lambda_{peak} \approx 500\,\mathrm{nm}", color="#FFD580").scale(0.32)
        wien_label.next_to(wien_marker, UP, buff=0.18).shift(RIGHT * 0.2)
        wien_sub = Text("at 5800 K", color="#FFD580").scale(0.24).next_to(wien_label, DOWN, buff=0.08)

        panel_1 = Rectangle(width=2.2, height=1.3, color="#5BA8FF", stroke_width=2)
        panel_1_txt_1 = Text("Rayleigh-Jeans", color="#5BA8FF").scale(0.24)
        panel_1_txt_2 = Text("diverges", color="#5BA8FF").scale(0.26).next_to(panel_1_txt_1, DOWN, buff=0.08)
        panel_1_grp = VGroup(panel_1, panel_1_txt_1, panel_1_txt_2)

        panel_2 = Rectangle(width=2.2, height=1.3, color="#FFD580", stroke_width=2)
        panel_2_txt_1 = Text("Planck", color="#FFD580").scale(0.24)
        panel_2_txt_2 = Text("finite peak", color="#FFD580").scale(0.26).next_to(panel_2_txt_1, DOWN, buff=0.08)
        panel_2_grp = VGroup(panel_2, panel_2_txt_1, panel_2_txt_2)

        panel_3 = Rectangle(width=2.2, height=1.3, color="#FF6B6B", stroke_width=2)
        panel_3_txt_1 = MathTex(r"E = n \cdot h \cdot \nu", color="#FF6B6B").scale(0.34)
        panel_3_grp = VGroup(panel_3, panel_3_txt_1)
        panels_grp = VGroup(panel_1_grp, panel_2_grp, panel_3_grp).arrange(RIGHT, buff=0.25).scale_to_fit_width(frame_w - 1)
        panels_grp.move_to(np.array([0, -2.6, 0.0]))

        closing_eq = MathTex(
            r"B_{\lambda}(T) = \frac{2hc^{2}}{\lambda^{5}} \cdot \frac{1}{e^{hc/\lambda k T} - 1}",
            color="#FFD580",
        ).scale(0.5)
        closing_eq.move_to(np.array([0, -1.6, 0.0]))

        # --- Pre-build fragments near the wall (used later via Transform) ---
        frag_segs = VGroup()
        for i in range(6):
            x0 = 205 + i * 12
            y_top = float(rj_norm[int(np.argmin(np.abs(lam_pts - (x0 + 3))))])
            y_top = min(y_top, 1.05)
            seg = DashedLine(
                axes.c2p(x0, 0),
                axes.c2p(x0, y_top),
                color="#5BA8FF",
                dash_length=0.06,
                stroke_width=2,
            )
            frag_segs.add(seg)

        # ====================================================================
        # BEAT A1.B1 | 0.00-1.36 s
        # ====================================================================
        self.add(filament, filament_glow, temp_label, temp_num, temp_unit, rad_label, rad_num)
        self.play(
            FadeIn(filament, scale=0.6),
            FadeIn(filament_glow),
            FadeIn(temp_label),
            FadeIn(temp_unit),
            FadeIn(rad_label),
            FadeIn(rad_num),
            run_time=0.273,
        )
        self.play(
            temp_tracker.animate.set_value(T_SUN),
            run_time=0.818,
            rate_func=linear,
        )
        self.wait(0.273)

        # ====================================================================
        # BEAT A1.B2 | 1.36-3.18 s
        # ====================================================================
        self.play(
            Create(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=0.35,
        )
        self.wait(1.168)
        self.play(FadeOut(x_label), FadeOut(y_label), run_time=0.3)

        # ====================================================================
        # BEAT A1.B3 | 3.18-5.00 s
        # ====================================================================
        self.play(
            Create(planck_curve),
            FadeIn(marker_300_p),
            FadeIn(rad_300_label),
            FadeIn(rad_at_300_num),
            run_time=0.35,
        )
        self.play(
            rad_at_300_num.animate.set_value(planck_300_over_500),
            run_time=1.168,
            rate_func=linear,
        )
        self.play(FadeOut(marker_300_p), FadeOut(rad_300_label), FadeOut(rad_at_300_num), run_time=0.3)

        # ====================================================================
        # BEAT A2.B1 | 5.00-8.00 s
        # ====================================================================
        rad_at_300_num.set_value(0.0)
        rad_at_300_num.set_color("#5BA8FF")
        self.add(rad_at_300_num)
        self.play(
            Create(rj_curve),
            FadeIn(marker_300_rj),
            rad_at_300_num.animate.set_value(rj_300_clamped),
            run_time=2.65,
            rate_func=linear,
        )
        self.play(FadeOut(marker_300_rj), run_time=0.3)

        # ====================================================================
        # BEAT A2.B2 | 8.00-11.00 s
        # ====================================================================
        flash = Circle(radius=0.3, color="#FF6B6B", fill_opacity=0.7, stroke_width=0)
        flash.move_to(axes.c2p(200, 1.0))
        self.play(
            Create(wall),
            FadeIn(flash, scale=2.0),
            run_time=0.35,
        )
        self.play(
            flash.animate.scale(2.5).set_opacity(0.0),
            run_time=0.6,
        )
        self.play(Write(wall_label), run_time=0.5)
        self.wait(1.25)
        self.play(FadeOut(flash), run_time=0.3)

        # ====================================================================
        # BEAT A3.B1 | 11.00-15.00 s
        # ====================================================================
        self.play(
            LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in steps], lag_ratio=0.1),
            FadeIn(step_caption),
            run_time=0.35,
        )
        self.wait(3.65)

        # ====================================================================
        # BEAT A3.B2 | 15.00-18.00 s
        # ====================================================================
        self.play(
            Transform(rj_curve, frag_segs),
            rad_at_300_num.animate.set_color("#FFD580").set_value(planck_300_over_500),
            run_time=0.35,
        )
        self.wait(2.65)

        # ====================================================================
        # BEAT A4.B1 | 18.00-22.00 s
        # ====================================================================
        self.play(Write(hero_eq), run_time=0.35)
        self.wait(3.65)

        # ====================================================================
        # BEAT A4.B2 | 22.00-25.00 s
        # ====================================================================
        peak_y = float(planck_vals[np.argmin(np.abs(lam_pts - 500))])
        wien_marker.move_to(axes.c2p(500, peak_y))
        wien_line = DashedLine(
            axes.c2p(500, 0),
            axes.c2p(500, peak_y),
            color="#FFD580", dash_length=0.08, stroke_width=2,
        )
        self.play(
            Create(wien_line),
            FadeIn(wien_marker),
            FadeIn(wien_label),
            FadeIn(wien_sub),
            run_time=2.35,
        )
        self.wait(0.65)

        # ====================================================================
        # BEAT A5.B1 | 25.00-28.00 s
        # ====================================================================
        self.play(
            temp_tracker.animate.set_value(3000.0),
            FadeOut(VGroup(
                filament_glow, rad_label, rad_num, wall, wall_label,
                rj_curve, steps, step_caption, hero_eq, wien_line,
                wien_marker, wien_label, wien_sub, axes,
                temp_label, temp_num, temp_unit, rad_at_300_num,
                filament, marker_300_p,
            )),
            run_time=0.35,
        )
        rainbow_axes = Axes(
            x_range=[380, 1100, 200],
            y_range=[0, 1.05, 0.5],
            x_length=frame_w - 1.2,
            y_length=1.2,
            tips=False,
        )
        rainbow_axes.move_to(np.array([0, 0.6, 0.0]))
        rainbow_lam = np.linspace(380, 1100, 140)
        rainbow_vals = normalize_planck(rainbow_lam)
        rainbow_curve = VMobject(stroke_width=4, color="#FFD580")
        rainbow_curve.set_points_as_corners([rainbow_axes.c2p(x, y) for x, y in zip(rainbow_lam, rainbow_vals)])
        rainbow_curve.make_smooth()
        self.play(
            Create(rainbow_axes),
            Create(rainbow_curve),
            LaggedStart(
                FadeIn(panel_1_grp, shift=UP * 0.15),
                FadeIn(panel_2_grp, shift=UP * 0.15),
                FadeIn(panel_3_grp, shift=UP * 0.15),
                lag_ratio=0.15,
            ),
            run_time=2.35,
        )
        self.wait(0.3)

        # ====================================================================
        # BEAT A5.B2 | 28.00-30.00 s
        # ====================================================================
        self.play(
            FadeOut(rainbow_axes),
            FadeOut(panel_1_grp),
            FadeOut(panel_2_grp),
            FadeOut(panel_3_grp),
            run_time=0.35,
        )
        rainbow_curve.move_to(np.array([0, 0.8, 0.0])).scale(1.2)
        self.play(Write(closing_eq), run_time=1.35)
        self.wait(0.3)