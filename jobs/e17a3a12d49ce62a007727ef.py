from manim import *
import numpy as np
import math

# Constants (SI)
H = 6.62607015e-34
C = 2.99792458e8
K_B = 1.380649e-23


def planck_spectral(lam_nm, T):
    """Planck spectral radiance in arbitrary units vs wavelength in nm."""
    lam = lam_nm * 1e-9
    x = H * C / (lam * K_B * T)
    # Numerical safety
    if x > 500:
        return 0.0
    return (2.0 * H * C * C / (lam ** 5)) / (math.exp(x) - 1.0)


def rayleigh_jeans(lam_nm, T):
    """Classical Rayleigh-Jeans law (same leading coefficient form) in a.u."""
    lam = lam_nm * 1e-9
    return (2.0 * C * K_B * T) / (lam ** 4)


class AetherLabScene(Scene):
    def construct(self):
                # --- Palette / canvas ----------------------------------------------------
                BG = "#0B1020"
                INK = "#E2E8F0"
                TEAL = "#22D3EE"
                AMBER = "#F59E0B"
                PINK = "#EC4899"
                self.camera.background_color = BG

                # --- Title ---------------------------------------------------------------
                title = Text("Blackbody Spectrum", color=INK).scale(0.55).to_edge(UP)
                sub = Text("Planck vs. Rayleigh–Jeans", color=TEAL).scale(0.32)
                sub.next_to(title, DOWN, buff=0.18)
                self.play(Write(title), run_time=1.0)
                self.wait(0.2)
                self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.6)

                # --- Axes (shared frame for both curves) ---------------------------------
                lam_nm = np.linspace(50, 3000, 900)
                x_max = 3000
                y_max = 1.15

                def planck_norm(lam):
                    return planck_spectral(lam, 5800.0)

                p_vals = np.array([planck_norm(l) for l in lam_nm])
                p_norm = p_vals / np.max(p_vals) * 0.85

                rj_vals = np.array([rayleigh_jeans(l, 5800.0) for l in lam_nm])
                rj_norm = rj_vals / np.max(rj_vals) * 0.85
                rj_display = np.clip(rj_norm, 0, 1.0)

                axes = Axes(
                    x_range=[0, x_max, 500],
                    y_range=[0, y_max, 0.25],
                    x_length=10.5,
                    y_length=4.0,
                    tips=False,
                    axis_config={"stroke_color": "#475569", "stroke_opacity": 0.55},
                )
                axes.move_to(DOWN * 0.55)

                x_lab = Text("wavelength λ (nm)", color="#94A3B8").scale(0.28)
                x_lab.next_to(axes.x_axis, DOWN, buff=0.15)
                y_lab = Text("spectral radiance B_λ", color="#94A3B8").scale(0.28)
                y_lab.next_to(axes.y_axis, LEFT, buff=0.15).rotate(90 * DEGREES)

                self.play(
                    LaggedStart(
                        Create(axes, stroke_opacity=0.55),
                        FadeIn(x_lab, shift=UP * 0.1),
                        FadeIn(y_lab, shift=RIGHT * 0.1),
                        lag_ratio=0.25,
                    ),
                    run_time=1.6,
                )
                self.wait(0.3)

                # --- Build the two spectra as static curves ------------------------------
                planck_pts = [axes.c2p(lam_nm[i], p_norm[i]) for i in range(len(lam_nm))]
                rj_pts = [axes.c2p(lam_nm[i], rj_display[i]) for i in range(len(lam_nm))]

                planck_curve = VMobject(stroke_color=TEAL, stroke_width=4)
                planck_curve.set_points_as_corners(planck_pts)

                rj_curve = VMobject(stroke_color=AMBER, stroke_width=3.5)
                rj_curve.set_points_as_corners(rj_pts)

                # Glow under Planck
                glow = planck_curve.copy().set_stroke(width=18, opacity=0.18)

                # --- ACT I — HOOK: the measured Planck spectrum rises then falls -------
                planck_label = Text("Planck's law", color=TEAL).scale(0.34)
                planck_label.move_to(axes.c2p(1700, 0.9))

                # BEAT A1.B1 | 0.00-5.50 s
                self.play(
                    Create(planck_curve),
                    FadeIn(planck_label, shift=LEFT * 0.2),
                    run_time=3.2,
                    rate_func=smooth,
                )
                self.add(glow)
                self.wait(1.3)

                # --- ACT II — ESTABLISH: classical Rayleigh-Jeans diverges --------------
                # BEAT A2.B1 | 5.50-11.50 s
                rj_label = Text("Rayleigh–Jeans (classical)", color=AMBER).scale(0.32)
                rj_label.move_to(axes.c2p(2400, 0.18))

                self.play(
                    Create(rj_curve),
                    FadeIn(rj_label, shift=LEFT * 0.2),
                    run_time=2.6,
                    rate_func=smooth,
                )

                # UV catastrophe callout
                cat_text = Text("ultraviolet catastrophe", color=PINK).scale(0.32)
                cat_text.to_edge(RIGHT).shift(DOWN * 0.6)
                cat_arrow = Arrow(
                    cat_text.get_left() + LEFT * 0.1,
                    axes.c2p(800, 0.55),
                    color=PINK,
                    stroke_width=4,
                    buff=0.1,
                    max_tip_length_to_length_ratio=0.12,
                )
                self.play(
                    FadeIn(cat_text, shift=RIGHT * 0.15),
                    GrowArrow(cat_arrow),
                    run_time=0.7,
                )
                self.wait(1.2)
                self.play(
                    FadeOut(cat_arrow),
                    FadeOut(cat_text),
                    run_time=0.5,
                )

                # --- ACT III — REVEAL: discrete energy quanta tame the divergence ------
                # BEAT A3.B1 | 11.50-19.50 s
                hbar_eq = MathTex(
                    r"E = h\nu", r"\;\Rightarrow\;",
                    r"\langle n\rangle = \frac{1}{e^{h\nu/k_BT}-1}",
                    color=INK,
                ).scale(0.55)
                hbar_eq.to_edge(UP, buff=1.55).shift(LEFT * 0.3)

                # Shaded "forbidden / finite" region under Planck tail
                tail_pts = [
                    axes.c2p(lam_nm[i], p_norm[i])
                    for i in range(len(lam_nm))
                    if lam_nm[i] > 1800
                ]
                tail_baseline = [axes.c2p(lam_nm[i], 0.0) for i in range(len(lam_nm)) if lam_nm[i] > 1800]
                tail_poly = Polygon(
                    *tail_pts, *reversed(tail_baseline),
                    fill_color=TEAL, fill_opacity=0.18, stroke_width=0,
                )
                finite_lab = Text("finite high-ν tail", color=TEAL).scale(0.3)
                finite_lab.next_to(axes.c2p(2400, 0.08), DOWN, buff=0.05).shift(RIGHT * 0.4)

                self.play(
                    FadeIn(hbar_eq, shift=DOWN * 0.2),
                    FadeIn(tail_poly, scale=0.95),
                    FadeIn(finite_lab, shift=UP * 0.1),
                    run_time=1.2,
                )
                self.wait(1.1)

                # --- ACT IV — CONSERVED: temperature slider (live readout) -------------
                # BEAT A4.B1 | 19.50-25.50 s
                T_tracker = ValueTracker(5800.0)

                # Temperature pill
                t_label = Text("T =", color="#94A3B8").scale(0.36)
                t_number = DecimalNumber(5800.0, num_decimal_places=0, color=AMBER).scale(0.42)
                t_unit = Text("K", color="#94A3B8").scale(0.36)
                t_group = VGroup(t_label, t_number, t_unit).arrange(RIGHT, buff=0.12)
                t_group.to_edge(RIGHT, buff=0.6).shift(UP * 0.2)

                # Single combined always_redraw: peak dot + label, dot drives label position
                peak_idx = int(np.argmax(p_vals))
                peak_dot = Dot(
                    axes.c2p(lam_nm[peak_idx], p_norm[peak_idx]),
                    color=PINK,
                    radius=0.09,
                )
                peak_warn = DecimalNumber(
                    lam_nm[peak_idx],
                    num_decimal_places=0,
                    color=PINK,
                ).scale(0.3)
                peak_warn.add_updater(
                    lambda m: m.next_to(peak_dot, UP, buff=0.12)
                )

                # Animate a hotter temperature: rebuild a single bright curve and
                # TRANSFORM it onto the Planck curve (no always_redraw on the curve).
                hot_lam = np.linspace(50, 3000, 900)
                hot_vals = np.array([planck_spectral(l, 7800.0) for l in hot_lam])
                hot_norm = hot_vals / np.max(p_vals) * 0.85
                hot_pts = [axes.c2p(hot_lam[i], hot_norm[i]) for i in range(len(hot_lam))]
                hot_curve = VMobject(stroke_color=TEAL, stroke_width=4)
                hot_curve.set_points_as_corners(hot_pts)

                self.play(
                    FadeIn(t_group, shift=LEFT * 0.1),
                    Transform(planck_curve, hot_curve),
                    run_time=2.4,
                    rate_func=smooth,
                )
                self.add(peak_dot, peak_warn)
                self.wait(0.2)
                self.play(T_tracker.animate.set_value(7800.0), run_time=1.6, rate_func=smooth)
                self.wait(0.6)

                # --- ACT V — RECAP / idle loop -----------------------------------------
                # BEAT A5.B1 | 25.50-30.00 s
                # Clear callouts but keep the two hero curves + a living marker
                self.play(
                    FadeOut(hbar_eq),
                    FadeOut(finite_lab),
                    FadeOut(tail_poly),
                    FadeOut(planck_label),
                    FadeOut(rj_label),
                    run_time=0.9,
                )

                # A small "photon" marker traveling along the Planck curve as a TracedPath
                wn_tracker = ValueTracker(0.0)

                def get_t():
                    return wn_tracker.get_value() * 28.0 + 1.0

                def planck_xy(s):
                    val = planck_norm(s)
                    val = val / np.max(p_vals) * 0.85
                    return axes.c2p(s, val)

                photon = always_redraw(
                    lambda: Dot(
                        planck_xy(get_t()),
                        color=AMBER,
                        radius=0.07,
                        z_index=5,
                    )
                )
                trail = TracedPath(
                    photon.get_center,
                    stroke_color=AMBER,
                    stroke_width=2.2,
                    stroke_opacity=0.7,
                    time_traced=1.2,
                )
                self.add(trail, photon)

                # Cap the number readout to a moving T that oscillates gently
                def t_updater(m):
                    m.set_value(5800.0 + 1800.0 * math.sin(get_t() * 0.35))

                t_number.add_updater(t_updater)

                # Wavelength shift companion readout — single updater, not always_redraw
                wn_lab = Text("λ_peak ≈", color="#94A3B8").scale(0.3)
                wn_val = Text(str(int(lam_nm[peak_idx])) + " nm", color=AMBER).scale(0.3)
                wn_unit = Text("nm", color="#94A3B8").scale(0.3)
                wn_group = VGroup(wn_lab, wn_val, wn_unit).arrange(RIGHT, buff=0.1)
                wn_group.next_to(t_group, DOWN, buff=0.18).align_to(t_group, RIGHT)

                self.play(
                    FadeIn(wn_group, shift=UP * 0.1),
                    wn_tracker.animate.set_value(1.05),
                    run_time=3.5,
                    rate_func=linear,
                )
                t_number.remove_updater(t_updater)
                self.wait(0.7)