from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
                # Palette
                YELLOW_P = YELLOW
                BLUE_P = BLUE
                RED_P = RED
                NEAR_BLACK = "#0B1220"
                TEXT_DIM = "#94A3B8"
                ACCENT_ORANGE = "#F59E0B"

                # Constants
                G_const = 6.674e-11
                M_earth = 5.972e24
                R_earth = 6.371e6
                g_earth = 9.81
                v_esc_val = math.sqrt(2 * G_const * M_earth / R_earth)  # ~11180 m/s
                v_esc_kmps = v_esc_val / 1000.0  # ~11.18 km/s

                # Title and background
                title = Text("Escape Velocity", color="#F8FAFC", font_size=36).to_edge(UP)
                self.add(title)

                # Plot Axes (bottom-left of frame; anchor A2 cell)
                axes = Axes(
                    x_range=[0, 10.5, 1],
                    y_range=[-70, 5, 10],
                    x_length=8.5,
                    y_length=4.6,
                    axis_config={"stroke_color": "#1E293B", "stroke_width": 2},
                    tips=False,
                )
                axes.move_to(np.array([-2.2, -0.6, 0.0]))
                x_label = Text("r / R", color=TEXT_DIM, font_size=22).next_to(axes.x_axis, RIGHT, buff=0.15)
                y_label = Text("PE / MJ/kg", color=TEXT_DIM, font_size=22).next_to(axes.y_axis, UP, buff=0.15)

                # PE curve U(r) = -GM/(R*t) -> mapped so r/R corresponds to axes
                G_M = G_const * M_earth
                def pe_func(t):
                    r_over_R = t
                    r_m = max(r_over_R * R_earth, 1.0)
                    return -(G_M / r_m) / 1e6

                pe_curve = axes.plot(pe_func, x_range=[0.2, 10.0], color=YELLOW_P, stroke_width=4)
                # Dashed E=0 reference line
                zero_line = axes.plot(lambda t: 0, x_range=[0.2, 10.0], color="#475569", stroke_width=2)
                zero_line.set_stroke(opacity=0.85)
                zero_line = DashedVMobject(zero_line, num_dashes=70, dashed_ratio=0.6)

                # Earth sphere at lower-left of the well (anchor near x=1 on axes)
                sphere_pos = axes.c2p(1.0, pe_func(1.0))
                # Single combined earth marker (no overlapping duplicate mobjects)
                earth_inner = Circle(radius=0.34, color=BLUE_P, fill_opacity=1.0,
                                     stroke_color="#60A5FA", stroke_width=2).move_to(sphere_pos)
                # Continent-like patches
                cont1 = Circle(radius=0.07, color="#34D399", fill_opacity=1.0).move_to(sphere_pos + np.array([0.10, 0.10, 0.0]))
                cont2 = Circle(radius=0.05, color="#34D399", fill_opacity=1.0).move_to(sphere_pos + np.array([-0.12, -0.08, 0.0]))
                earth_grp = VGroup(earth_inner, cont1, cont2)

                earth_label = Text("Earth", color="#60A5FA", font_size=24).next_to(earth_inner, DOWN, buff=0.18)

                # ValueTrackers
                r_tracker = ValueTracker(1.0)  # r/R
                v_tracker = ValueTracker(0.0)  # m/s
                opacity_tracker = ValueTracker(0.92)

                # Projectile driven by r_tracker along the PE curve
                bob_tracker = ValueTracker(0.0)

                def projectile_with_bob():
                    t = r_tracker.get_value()
                    base_y = pe_func(t)
                    bob = 0.05 * math.sin(6.0 * bob_tracker.get_value())
                    return Dot(axes.c2p(t, base_y + bob * 0.001), color=RED_P, radius=0.10)

                proj = always_redraw(projectile_with_bob)

                # Live readout panel (DecimalNumbers) — anchored top-right
                readout_w = 3.6
                readout_h = 1.7
                readout_box = RoundedRectangle(width=readout_w, height=readout_h, corner_radius=0.12,
                                               color="#1E293B", fill_color="#0F172A", fill_opacity=0.9, stroke_width=2)
                readout_box.to_corner(DR, buff=0.45).shift(np.array([-0.05, 0.05, 0.0]))

                # Live speed v (m/s)
                v_label = Text("v", color=TEXT_DIM, font_size=24).move_to(readout_box.get_corner(UL) + np.array([0.25, -0.30, 0.0]))
                v_unit = Text("m/s", color=TEXT_DIM, font_size=20).move_to(v_label.get_center() + np.array([2.45, -0.02, 0.0]))

                # Live radius r
                r_label = Text("r", color=TEXT_DIM, font_size=24).move_to(v_label.get_center() + np.array([0.0, -0.45, 0.0]))
                r_unit = Text("km", color=TEXT_DIM, font_size=20).move_to(r_label.get_center() + np.array([2.35, -0.02, 0.0]))

                # Live energy E
                E_label = Text("E", color=TEXT_DIM, font_size=24).move_to(r_label.get_center() + np.array([0.0, -0.45, 0.0]))
                E_unit = Text("MJ/kg", color=TEXT_DIM, font_size=20).move_to(E_label.get_center() + np.array([2.05, -0.02, 0.0]))

                # DecimalNumbers (placed first, fade in separately before animating tracker)
                v_num = DecimalNumber(0.0, color=RED_P, num_decimal_places=0, font_size=28)
                v_num.move_to(v_label.get_center() + np.array([1.40, 0.0, 0.0]))
                v_num.add_updater(lambda m: m.set_value(v_tracker.get_value()))

                r_num = DecimalNumber(6371.0, color="#F8FAFC", num_decimal_places=0, font_size=28)
                r_num.move_to(r_label.get_center() + np.array([1.40, 0.0, 0.0]))
                r_num.add_updater(lambda m: m.set_value(r_tracker.get_value() * R_earth / 1000.0))

                # Energy in MJ/kg
                def E_specific_MJkg():
                    v = v_tracker.get_value()
                    r_r = r_tracker.get_value()
                    return (0.5 * v * v) / 1e6 - (G_M / R_earth) / 1e6 * (1.0 / max(r_r, 0.0001))

                E_num = DecimalNumber(-62.6, color=ACCENT_ORANGE, num_decimal_places=2, font_size=28)
                E_num.move_to(E_label.get_center() + np.array([1.20, 0.0, 0.0]))
                E_num.add_updater(lambda m: m.set_value(E_specific_MJkg()))

                readout_grp = VGroup(readout_box, v_label, r_label, E_label, v_unit, r_unit, E_unit,
                                     v_num, r_num, E_num)

                # === Content groups ===
                plot_content = VGroup(axes, x_label, y_label, pe_curve, zero_line, earth_grp, earth_label)
                # Center plot content diagonally in lower-left zone
                plot_content.move_to(np.array([-2.4, -0.7, 0.0]))

                # === ACT 1 / HOOK ===
                # BEAT A1.B1 | 0.00-3.00 s
                self.play(
                    FadeIn(plot_content, shift=UP * 0.2),
                    FadeIn(readout_grp, shift=LEFT * 0.2),
                    run_time=1.2,
                )

                # Place projectile at r=R (t=1) at v=0
                r_tracker.set_value(1.0)
                v_tracker.set_value(0.0)
                bob_tracker.set_value(0.0)
                self.add(proj)

                self.wait(1.8)  # hold A1.B1

                # === ACT 2 / ESTABLISH ===
                # BEAT A2.B1 | 5.00-7.80 s
                eq1 = MathTex(r"\tfrac{1}{2}mv^{2}-\dfrac{GMm}{R}=0", color="#F8FAFC", font_size=42)
                eq1.set_color_by_tex(r"\tfrac{1}{2}", YELLOW_P)
                eq1.set_color_by_tex(r"GMm", BLUE_P)
                eq1.to_corner(UL, buff=0.95)
                eq1.shift(np.array([0.0, 0.85, 0.0]))
                self.play(Write(eq1), run_time=0.7)
                self.wait(1.8)

                # BEAT A2.B2 | 7.80-11.00 s
                eq2 = MathTex(r"v_{\mathrm{esc}}=\sqrt{2gR}=\sqrt{2\cdot 9.81\cdot 6.371\times10^{6}}",
                              color="#F8FAFC", font_size=36)
                eq2.set_color_by_tex(r"v_{\mathrm{esc}}", ACCENT_ORANGE)
                eq2.set_color_by_tex(r"2gR", YELLOW_P)
                eq2.move_to(np.array([3.5, -2.05, 0.0]))
                # Tag below: v_esc ≈ 11.18 km/s
                v_tag = Text(f"≈ {v_esc_kmps:.2f} km/s", color=ACCENT_ORANGE, font_size=30)
                v_tag.next_to(eq2, DOWN, buff=0.25)
                self.play(
                    Transform(eq1, eq2),
                    FadeIn(v_tag),
                    run_time=0.8,
                )
                self.wait(1.55)

                # Clear A2 equations before evolve
                self.play(FadeOut(eq1), FadeOut(v_tag), run_time=0.35)

                # === ACT 3 / EVOLVE ===
                # BEAT A3.B1 | 11.00-16.00 s
                t_tracker = ValueTracker(0.0)

                update_launch = lambda mob=None: (
                    r_tracker.set_value(1.0 + 7.0 * t_tracker.get_value()),
                    v_tracker.set_value(v_esc_val * math.sqrt(max(1.0 - 1.0 / max(1.0 + 7.0 * t_tracker.get_value(), 1.0001), 0.0))),
                )
                t_tracker.add_updater(update_launch)
                self.add(t_tracker)
                self.play(t_tracker.animate.set_value(1.0), run_time=5.0, rate_func=linear)

                # BEAT A3.B2 | 16.00-20.00 s
                self.play(t_tracker.animate.set_value(2.0), run_time=3.8, rate_func=linear)
                # explicit highlight on dashed zero line
                highlight_box = SurroundingRectangle(zero_line, color=ACCENT_ORANGE, buff=0.08, stroke_width=3)
                self.play(Create(highlight_box), run_time=0.2)

                # === ACT 4 / REVEAL ===
                # BEAT A4.B1 | 20.00-26.00 s
                self.play(FadeOut(highlight_box), run_time=0.3)

                # Build hero label
                hero_eq = MathTex(r"v_{\mathrm{esc}}\approx 11.2\ \text{km/s}", color=ACCENT_ORANGE, font_size=58)
                hero_eq.move_to(np.array([2.6, 1.5, 0.0]))
                sub_eq = MathTex(r"v_{\mathrm{esc}}=\sqrt{\dfrac{2GM}{R}}", color="#F8FAFC", font_size=40)
                sub_eq.next_to(hero_eq, DOWN, buff=0.45)

                hero_grp = VGroup(hero_eq, sub_eq)
                hero_grp.scale_to_fit_width(min(hero_grp.get_width(), config.frame_width - 1.8))
                hero_grp.move_to(np.array([2.4, 1.4, 0.0]))

                self.play(
                    FadeIn(hero_grp, shift=UP * 0.2),
                    run_time=0.45,
                )
                self.wait(5.2)

                # === ACT 5 / RECAP ===
                # BEAT A5.B1 | 26.00-30.00 s
                self.play(FadeOut(hero_grp), run_time=0.3)

                # Build recap equation next to Earth (fade plot content together)
                recap_eq = MathTex(r"v_{\mathrm{esc}}=\sqrt{\dfrac{2GM}{R}}=\sqrt{2gR}",
                                   color="#F8FAFC", font_size=42)
                recap_eq.set_color_by_tex(r"v_{\mathrm{esc}}", ACCENT_ORANGE)
                recap_eq.set_color_by_tex(r"\sqrt{", YELLOW_P)
                recap_eq.next_to(earth_grp, RIGHT, buff=0.6).shift(UP * 0.2)
                # Fade out the well/axis content while fading in recap
                self.play(
                    FadeOut(pe_curve),
                    FadeOut(zero_line),
                    FadeOut(axes),
                    FadeOut(x_label),
                    FadeOut(y_label),
                    FadeOut(proj),
                    FadeIn(recap_eq),
                    run_time=0.5,
                )

                # Idle living ending: projectile bob + opacity pulse on earth + heartbeat on hero label.
                t_tracker.remove_updater(update_launch)
                # Create a simple bobbing projectile again (separate from r_tracker so heartbeat is independent)
                idle_proj = always_redraw(projectile_with_bob)
                self.add(idle_proj)

                self.play(
                    bob_tracker.animate.set_value(2 * math.pi),
                    opacity_tracker.animate.set_value(1.0),
                    run_time=2.0,
                    rate_func=linear,
                )
                self.play(
                    bob_tracker.animate.set_value(4 * math.pi),
                    opacity_tracker.animate.set_value(0.92),
                    run_time=1.1,
                    rate_func=linear,
                )
                self.wait(0.1)