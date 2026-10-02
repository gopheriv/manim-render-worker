from manim import *
import numpy as np
import math


GOLD = "#FFD166"
RED = "#EF476F"
GREEN = "#06D6A0"
WHITE_HOT = "#FFE4A0"


class AetherLabScene(Scene):
    def construct(self):
                # constants
                T_val = 5800.0
                h = 6.626e-34
                c = 3.0e8
                kB = 1.381e-23

                def planck_lam(lam_um):
                    lam = lam_um * 1e-6
                    num = 2.0 * h * c * c / (lam ** 5)
                    expo = h * c / (lam * kB * T_val)
                    return num / (math.exp(expo) - 1.0)

                def rj_lam(lam_um):
                    lam = lam_um * 1e-6
                    return 2.0 * c * kB * T_val / (lam ** 4)

                # BEAT A1.B1 | 0.00-5.00 s
                title = Text("Blackbody Spectrum", color=WHITE).scale(0.45).to_edge(UP)
                filament = Dot(radius=0.18, color=GOLD).move_to(LEFT * 3.6 + UP * 0.2)
                glow = Dot(radius=0.32, color=GOLD, fill_opacity=0.25).move_to(filament.get_center())
                self.play(
                    Write(title),
                    FadeIn(filament, scale=0.6),
                    FadeIn(glow),
                    run_time=0.6,
                )

                T_tracker = ValueTracker(0.0)
                T_label = Text("T = ", color=WHITE).scale(0.4).next_to(filament, RIGHT, buff=0.4)
                T_num = DecimalNumber(0.0, num_decimal_places=0, color=WHITE).scale(0.4)
                T_num.next_to(T_label, RIGHT, buff=0.1)
                self.add(T_label, T_num)
                T_num.add_updater(lambda m: m.set_value(T_tracker.get_value()))
                self.play(T_tracker.animate.set_value(T_val), run_time=2.5, rate_func=smooth)
                T_num.remove_updater(T_num.get_updaters()[0])

                # Energy level ladder
                rungs = VGroup()
                n_count = 5
                for n in range(1, n_count + 1):
                    y = -0.15 * n
                    rung = Line(LEFT * 0.35, RIGHT * 0.35, color=GREEN, stroke_width=3)
                    rung.move_to(LEFT * 3.6 + RIGHT * 0.9 + UP * (1.1 + y * 0.0) + UP * 0.0)
                    rung.shift(UP * (0.4 - 0.22 * (n - 1)))
                    rungs.add(rung)
                rungs.move_to(LEFT * 2.55 + UP * 0.2)
                rung_label = Text("E = n h f", color=GREEN).scale(0.28).next_to(rungs, UP, buff=0.1)
                self.play(
                    FadeIn(rungs, shift=UP * 0.1),
                    FadeIn(rung_label),
                    run_time=0.8,
                )
                self.wait(0.6)

                # BEAT A2.B1 | 5.00-11.00 s
                self.play(FadeOut(title), run_time=0.3)

                # left axes
                lam_max = 3.0
                I_max = 1.2
                x_unit = 0.9
                y_unit = 2.4 / I_max
                axes_l = Axes(
                    x_range=[0, lam_max, 0.5],
                    y_range=[0, I_max, 0.3],
                    x_length=x_unit * lam_max,
                    y_length=y_unit * I_max,
                    axis_config={"include_tip": False, "stroke_opacity": 0.6},
                    tips=False,
                )
                axes_l.move_to(LEFT * 0.4 + DOWN * 1.3)
                x_label_l = MathTex(r"\lambda", r"(\mu m)", color=WHITE).scale(0.35)
                x_label_l[0].set_color(WHITE)
                x_label_l.next_to(axes_l.x_axis, RIGHT, buff=0.1)
                y_label_l = MathTex(r"I_\lambda", color=WHITE).scale(0.35)
                y_label_l.next_to(axes_l.y_axis, UP, buff=0.1)
                self.play(
                    Create(axes_l),
                    FadeIn(x_label_l),
                    FadeIn(y_label_l),
                    run_time=0.6,
                )

                # measured curve
                lam_pts = np.linspace(0.15, lam_max, 220)
                planck_vals = np.array([planck_lam(l) for l in lam_pts])
                pmax = planck_vals.max()
                planck_norm = planck_vals / pmax * (I_max * 0.85)

                def planck_curve_func(x):
                    idx = int(np.argmin(np.abs(lam_pts - x)))
                    return float(planck_norm[idx])

                measured = axes_l.plot(planck_curve_func, x_range=[0.15, lam_max, 0.01], color=GOLD, stroke_width=4)
                peak_x = float(lam_pts[np.argmax(planck_norm)])
                peak_y = float(planck_norm.max())

                measured_label = Text("Measured", color=GOLD).scale(0.32)
                measured_label.next_to(axes_l.c2p(peak_x, peak_y), UP, buff=0.15)
                self.play(Create(measured), FadeIn(measured_label, shift=UP * 0.1), run_time=2.0)
                self.wait(2.5)

                # BEAT A3.B1 | 11.00-17.00 s
                # Rayleigh-Jeans curve
                rj_vals = np.array([rj_lam(l) for l in lam_pts])
                rj_norm = rj_vals / rj_vals[10] * float(planck_norm[10])  # match at long lambda

                def rj_curve_func(x):
                    idx = int(np.argmin(np.abs(lam_pts - x)))
                    return float(min(rj_norm[idx], I_max * 2.5))  # clamp visually

                rj_curve = axes_l.plot(rj_curve_func, x_range=[0.15, lam_max, 0.01], color=RED, stroke_width=3)
                rj_label = MathTex(r"I_\lambda^{RJ} = \frac{2ckT}{\lambda^4}", color=RED).scale(0.32)
                rj_label.next_to(axes_l.c2p(0.45, I_max * 0.95), UP, buff=0.1)
                uv_brace = Brace(Line(axes_l.c2p(0.18, 0.3), axes_l.c2p(0.18, 1.15)), direction=RIGHT, color=RED)
                uv_text = Text("UV catastrophe", color=RED).scale(0.3)
                uv_text.next_to(uv_brace, RIGHT, buff=0.1)
                self.play(
                    Create(rj_curve),
                    FadeIn(uv_brace),
                    FadeIn(uv_text),
                    FadeIn(rj_label),
                    run_time=3.0,
                )
                self.wait(3.0)

                # BEAT A3.B2 | 17.00-20.00 s
                overflow_dots = VGroup()
                for i, frac in enumerate([0.18, 0.16, 0.14, 0.12]):
                    y = I_max * 0.85 + i * 0.18
                    d = Dot(axes_l.c2p(frac, min(y, I_max * 1.05)), radius=0.05, color=RED)
                    overflow_dots.add(d)
                arrow = Arrow(axes_l.c2p(0.18, 1.1), axes_l.c2p(0.05, 1.18), color=RED, buff=0, stroke_width=3)
                inf_marker = Text("∞", color=RED).scale(0.5)
                inf_marker.next_to(arrow.get_end(), LEFT, buff=0.1)
                self.play(
                    LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in overflow_dots], lag_ratio=0.1),
                    GrowArrow(arrow),
                    FadeIn(inf_marker),
                    run_time=1.5,
                )
                self.wait(1.5)

                # BEAT A4.B1 | 20.00-27.00 s
                # clear left-side overlay clutter
                self.play(
                    FadeOut(VGroup(uv_brace, uv_text, rj_label, overflow_dots, arrow, inf_marker, measured_label)),
                    run_time=0.4,
                )

                # right axes: frequency vs intensity
                nu_max = 1500.0
                I_max_r = I_max
                nu_len = 4.2
                y_len = 2.0
                axes_r = Axes(
                    x_range=[0, nu_max, 300],
                    y_range=[0, I_max_r, 0.3],
                    x_length=nu_len,
                    y_length=y_len,
                    axis_config={"include_tip": False, "stroke_opacity": 0.6},
                    tips=False,
                )
                axes_r.move_to(RIGHT * 2.7 + DOWN * 0.7)
                x_label_r = MathTex(r"\nu", r"(PHz)", color=WHITE).scale(0.35)
                x_label_r.next_to(axes_r.x_axis, RIGHT, buff=0.1)
                y_label_r = MathTex(r"I_\nu", color=WHITE).scale(0.35)
                y_label_r.next_to(axes_r.y_axis, UP, buff=0.1)
                self.play(
                    Create(axes_r),
                    FadeIn(x_label_r),
                    FadeIn(y_label_r),
                    run_time=0.7,
                )

                # Planck-in-nu curve
                def planck_nu(nu_pHz):
                    nu = nu_pHz * 1e12
                    num = 2.0 * h * nu ** 3 / (c ** 2)
                    expo = h * nu / (kB * T_val)
                    return num / (math.exp(expo) - 1.0)

                nu_pts = np.linspace(50, nu_max, 200)
                pnu_vals = np.array([planck_nu(n) for n in nu_pts])
                pnu_max = pnu_vals.max()
                pnu_norm = pnu_vals / pnu_max * (I_max_r * 0.85)

                def planck_nu_func(x):
                    idx = int(np.argmin(np.abs(nu_pts - x)))
                    return float(pnu_norm[idx])

                planck_curve = axes_r.plot(planck_nu_func, x_range=[50, nu_max, 1], color=PURPLE, stroke_width=3)

                # stepped segments — one per rung
                steps = VGroup()
                step_edges = [200, 480, 760, 1040, 1320]
                for i, edge in enumerate(step_edges[:-1]):
                    x0 = step_edges[i]
                    x1 = step_edges[i + 1]
                    y0 = float(planck_nu_func(x0))
                    y1 = float(planck_nu_func(x0))
                    seg = Line(
                        axes_r.c2p(x0, y0),
                        axes_r.c2p(x1, y1),
                        color=PURPLE,
                        stroke_width=2.5,
                    )
                    steps.add(seg)
                    # vertical riser to next plateau
                    y_next = float(planck_nu_func(x1))
                    riser = Line(
                        axes_r.c2p(x1, y0),
                        axes_r.c2p(x1, y_next),
                        color=PURPLE,
                        stroke_width=2,
                    )
                    steps.add(riser)

                nhf_label = MathTex(r"E = n h f", color=GREEN).scale(0.42)
                nhf_label.next_to(axes_r, UP, buff=0.2)
                self.play(
                    Create(planck_curve),
                    LaggedStart(*[Create(s) for s in steps], lag_ratio=0.15),
                    FadeIn(nhf_label),
                    run_time=3.7,
                )
                self.wait(2.2)

                # BEAT A5.B1 | 27.00-30.00 s
                # clear right side and most of left
                self.play(
                    FadeOut(VGroup(
                        axes_r,
                        x_label_r,
                        y_label_r,
                        planck_curve,
                        steps,
                        nhf_label,
                        rj_curve,
                        filament,
                        glow,
                        rungs,
                        rung_label,
                        T_label,
                        T_num,
                    )),
                    run_time=0.5,
                )

                # remaining: measured gold curve, peak annotation, small filament
                peak_annot = MathTex(r"B_\lambda(T)", color=GOLD).scale(0.36)
                peak_annot.next_to(axes_l.c2p(peak_x, peak_y), UP, buff=0.15)
                small_fil = Dot(radius=0.12, color=GOLD).next_to(axes_l, DOWN, buff=0.25)

                # idle loop: measured curve breathes ±2% on y
                def breath_updater(mob):
                    base = planck_norm
                    amp = 0.02
                    phase = self.renderer.time * 0.4 * TAU * 0.5
                    scale = 1.0 + amp * math.sin(phase)
                    new_pts = []
                    for i, lp in enumerate(lam_pts):
                        x = lp
                        y = float(base[i]) * scale
                        new_pts.append(axes_l.c2p(x, y))
                    mob.set_points_as_corners(new_pts)

                measured.add_updater(breath_updater)
                self.play(FadeIn(peak_annot), FadeIn(small_fil), run_time=0.5)
                self.wait(2.0)