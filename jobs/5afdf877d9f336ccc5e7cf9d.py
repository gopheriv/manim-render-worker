from manim import *
import numpy as np
import math

# Constants (SI, normalized for visual)
h = 6.626e-34
c = 3.0e8
kB = 1.381e-23
T0 = 5800.0

# Use nm for x-axis convenience
def planck_lam(lam_nm, T):
    lam = lam_nm * 1e-9
    expo = (h * c) / (lam * kB * T)
    return (2.0 * h * c * c / (lam ** 5)) / (math.exp(expo) - 1.0)

def rayleigh_jeans_lam(lam_nm, T):
    lam = lam_nm * 1e-9
    return (2.0 * c * kB * T) / (lam ** 4)


class AetherLabScene(Scene):
    def construct(self):
            # ---------------- BEAT A1.B1 | 0.00-4.00 s — HOOK / TITLE ----------------
            title = Text("The Blackbody Spectrum", color=WHITE, font_size=40)
            title.to_edge(UP, buff=0.4)
            sub = Text("Planck vs. Rayleigh–Jeans", color=TEAL_A, font_size=24)
            sub.next_to(title, DOWN, buff=0.15)
            self.play(
                Write(title),
                FadeIn(sub, shift=UP * 0.2),
                run_time=1.2,
            )
            self.wait(2.1)
            self.play(FadeOut(title), FadeOut(sub), run_time=0.6)

            # ---------------- BEAT A2.B1 | 4.00-9.00 s — ESTABLISH AXES + RJ ----------------
            ax = Axes(
                x_range=[0, 3000, 500],
                y_range=[0, 1.6, 0.5],
                x_length=9.5,
                y_length=4.6,
                tips=False,
            ).shift(DOWN * 0.35)

            x_lab = ax.get_x_axis_label("\\lambda\\,(nm)", edge=RIGHT, direction=DOWN, buff=0.15)
            y_lab = ax.get_y_axis_label("B_\\lambda", edge=UP, direction=LEFT, buff=0.15)
            x_lab.set_color(GREY_B).scale(0.55)
            y_lab.set_color(GREY_B).scale(0.55)
            for t in ax.x_axis.get_tick_labels():
                t.set_color(GREY_B).scale(0.55)
            for t in ax.y_axis.get_tick_labels():
                t.set_color(GREY_B).scale(0.55)

            rj_vals = np.array([rayleigh_jeans_lam(x, T0) for x in np.linspace(1.0, 3000.0, 800)])
            rj_peak = rj_vals.max()
            rj_fn = lambda x: rayleigh_jeans_lam(x, T0) / rj_peak

            rj_glow = ax.plot(rj_fn, x_range=[400, 3000, 1], color=PURE_RED,
                              stroke_width=14, stroke_opacity=0.25)
            rj_curve = ax.plot(rj_fn, x_range=[400, 3000, 1], color=PURE_RED,
                               stroke_width=2.6)
            rj_label = Text("Rayleigh–Jeans", color=PURE_RED, font_size=22)
            rj_label.next_to(ax.c2p(2400, 1.35), RIGHT, buff=0.15)

            self.play(
                Create(ax, lag_ratio=0.0),
                FadeIn(x_lab),
                FadeIn(y_lab),
                Create(rj_glow),
                Create(rj_curve),
                FadeIn(rj_label, shift=LEFT * 0.15),
                run_time=2.0,
                rate_func=smooth,
            )
            self.wait(1.0)

            # ---------------- BEAT A3.B1 | 9.00-14.50 s — ULTRAVIOLET CATASTROPHE ----------------
            catastrophe = Text("ultraviolet catastrophe", color=PURE_RED, font_size=24)
            catastrophe.next_to(ax.c2p(2200, 1.15), DOWN, buff=0.15)
            arrow = Arrow(ax.c2p(2400, 1.45), ax.c2p(2900, 1.55),
                          color=PURE_RED, stroke_width=5, buff=0.1)
            self.play(
                FadeIn(catastrophe, shift=RIGHT * 0.15),
                GrowArrow(arrow),
                run_time=1.2,
            )
            self.wait(0.8)

            self.play(
                rj_curve.animate.shift(RIGHT * 6).set_opacity(0),
                rj_glow.animate.shift(RIGHT * 6).set_opacity(0),
                rj_label.animate.shift(RIGHT * 6).set_opacity(0),
                catastrophe.animate.shift(RIGHT * 6).set_opacity(0),
                arrow.animate.shift(RIGHT * 6).set_opacity(0),
                run_time=2.2,
                rate_func=smooth,
            )
            self.wait(0.8)

            # ---------------- BEAT A4.B1 | 14.50-23.50 s — PLANCK REVEAL + LIVE READOUT ----------------
            planck_vals = np.array([planck_lam(x, T0) for x in np.linspace(1.0, 3000.0, 800)])
            p_peak = planck_vals.max()
            planck_fn = lambda x: planck_lam(x, T0) / p_peak

            pl_glow = ax.plot(planck_fn, x_range=[100, 3000, 1], color=TEAL_A,
                              stroke_width=14, stroke_opacity=0.28)
            pl_curve = ax.plot(planck_fn, x_range=[100, 3000, 1], color=TEAL_A,
                               stroke_width=2.8)
            pl_label = Text("Planck", color=TEAL_A, font_size=24)
            pl_label.next_to(ax.c2p(1400, 0.55), RIGHT, buff=0.15)

            hero_eq = MathTex(
                "B_{\\lambda}(T) = \\dfrac{2hc^{2}}{\\lambda^{5}}\\,",
                "\\dfrac{1}{e^{hc/(\\lambda k_{B}T)} - 1}",
                color=WHITE,
            ).scale(0.55)
            hero_eq.to_edge(UP, buff=0.3)

            T_tracker = ValueTracker(T0)

            readout_num = DecimalNumber(T0, num_decimal_places=0, color=WHITE, font_size=30)
            readout_num.add_updater(lambda m: m.set_value(T_tracker.get_value()))
            readout_lab = Text("T =", color=GREY_B, font_size=24).next_to(readout_num, LEFT, buff=0.1)
            readout_unit = Text("K", color=GREY_B, font_size=24).next_to(readout_num, RIGHT, buff=0.1)
            readout_group = VGroup(readout_lab, readout_num, readout_unit)
            readout_group.to_edge(RIGHT, buff=0.5).shift(UP * 1.6)

            peak_dot = Dot(ax.c2p((2.898e6) / T0, 1.0), color=GOLD, radius=0.09)
            peak_dot.add_updater(lambda d: d.move_to(
                ax.c2p(2.898e6 / T_tracker.get_value(),
                       planck_lam(2.898e6 / T_tracker.get_value(), T_tracker.get_value()) / p_peak)))

            peak_tag = always_redraw(lambda: Text(
                f"\\lambda_{{max}} \\approx {2.898e6 / T_tracker.get_value():.0f}\\,nm",
                color=GOLD, font_size=22
            ).next_to(peak_dot, UP, buff=0.15))

            self.play(
                Write(hero_eq),
                Create(pl_glow),
                Create(pl_curve),
                FadeIn(pl_label, shift=LEFT * 0.15),
                FadeIn(readout_group, shift=LEFT * 0.2),
                run_time=2.4,
                rate_func=smooth,
            )
            self.add(peak_dot, peak_tag)

            # ---------------- BEAT A5.B1 | 23.50-30.00 s — TEMPERATURE SWEEP (IDLE LOOP) ----------------
            rj_ghost_dashed = DashedVMobject(
                ax.plot(lambda x: min(rayleigh_jeans_lam(x, T0) / rj_peak, 1.55),
                        x_range=[400, 3000, 1], color=PURE_RED, stroke_width=1.6,
                        stroke_opacity=0.5),
                num_dashes=80,
            )
            self.play(FadeIn(rj_ghost_dashed, lag_ratio=0.0), run_time=0.7)
            self.wait(0.6)

            # Single combined sweep: T → 7800 → 4200 → 6500 as one continuous motion
            self.play(
                T_tracker.animate(run_time=2.2).set_value(7800),
                rate_func=smooth,
            )
            self.play(
                T_tracker.animate(run_time=2.4).set_value(4200),
                rate_func=smooth,
            )
            self.play(
                T_tracker.animate(run_time=1.4).set_value(6500),
                rate_func=smooth,
            )
            self.wait(0.7)

            self.play(Indicate(hero_eq, color=GOLD, scale_factor=1.04), run_time=0.8)
            self.wait(0.6)

            discrete_tag = Text("discrete quanta  \\,h\\nu", color=GOLD, font_size=26)
            discrete_tag.next_to(pl_label, DOWN, buff=0.25).align_to(pl_label, LEFT)

            def _idle_loop(mob, alpha):
                T_tracker.set_value(5500 + 1500 * math.sin(2 * math.pi * alpha))

            idle_anim = UpdateFromAlphaFunc(peak_dot, _idle_loop, run_time=4.4)
            self.play(
                FadeOut(readout_group),
                FadeOut(rj_ghost_dashed),
                FadeIn(discrete_tag, shift=UP * 0.15),
                idle_anim,
                run_time=4.4,
            )
            self.wait(0.4)