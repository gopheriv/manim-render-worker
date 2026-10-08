from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        PALETTE_PRIMARY = "#1E90FF"
        PALETTE_SECONDARY = "#FFD700"
        PALETTE_ACCENT = "#FF4500"

        AMP = 4.0 / math.pi
        T_MIN = -2 * math.pi
        T_MAX = 2 * math.pi
        TS = np.linspace(T_MIN, T_MAX, 800)

        axes = Axes(
            x_range=[T_MIN, T_MAX, math.pi],
            y_range=[-1.6, 1.6, 0.5],
            x_length=9.5,
            y_length=4.0,
            tips=False,
        )
        axes.set_stroke(opacity=0.25)
        axes.move_to(DOWN * 0.55)

        x_label = Text("t", font_size=22).set_color(GRAY_B).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("f(t)", font_size=22).set_color(GRAY_B).next_to(axes.y_axis, UP, buff=0.1)

        def sq_wave(t):
            return np.sign(np.sin(t))

        def partial_sum(t, N):
            s = np.zeros_like(t)
            for k in range(N):
                n = 2 * k + 1
                s = s + np.sin(n * t) / n
            return AMP * s

        ref_curve = axes.plot(lambda t: np.sign(np.sin(t)),
                             color=PALETTE_PRIMARY,
                             stroke_width=3,
                             use_smoothing=False)
        ref_dashed = DashedVMobject(ref_curve, num_dashes=72, dashed_ratio=0.55)
        ref_dashed.set_stroke(PALETTE_PRIMARY, width=2.5)

        # BEAT A1.B1 | 0.00-2.50 s
        self.play(FadeIn(axes, run_time=0.4), FadeIn(x_label), FadeIn(y_label))
        self.play(Create(ref_dashed), run_time=1.5, rate_func=linear)
        ref_label = Text("target: sgn(sin t)", font_size=24, color=PALETTE_PRIMARY)
        ref_label.next_to(axes, UP, buff=0.15).align_to(axes, LEFT).shift(RIGHT * 0.4)
        self.play(FadeIn(ref_label, shift=0.2 * DOWN), run_time=0.45)
        self.wait(0.05)

        n_tracker = ValueTracker(1)
        harmonics_active = VGroup()
        rail_labels = VGroup()
        rails_label = Text("odd harmonics", font_size=24, color=PALETTE_SECONDARY)
        rails_label.next_to(axes, DOWN, buff=0.1).align_to(axes, RIGHT).shift(LEFT * 0.3)
        y_positions = np.linspace(1.2, -1.2, 5)
        rail_colors = [PALETTE_SECONDARY, "#FFA500", "#FF8C00", "#FF6347", "#FF4500"]

        def rebuild_harmonics():
            group = VGroup()
            labels = VGroup()
            N = int(n_tracker.get_value())
            for i in range(5):
                idx = 2 * i + 1
                curve = axes.plot(
                    lambda t, k=idx: AMP * np.sin(k * t) / 1.0,
                    color=rail_colors[i],
                    stroke_width=2.0,
                    use_smoothing=False,
                )
                if i < N:
                    curve.set_stroke(opacity=0.85)
                else:
                    curve.set_stroke(opacity=0.10)
                group.add(curve)
                lab = MathTex(f"n={idx}", font_size=22, color=rail_colors[i])
                lab.move_to(axes.c2p(T_MIN + 0.15, y_positions[i]))
                labels.add(lab)
            return group, labels

        harmonics_active = always_redraw(lambda: rebuild_harmonics()[0])
        rail_labels = always_redraw(lambda: rebuild_harmonics()[1])

        # BEAT A1.B2 | 2.50-4.50 s
        self.play(FadeIn(harmonics_active), FadeIn(rail_labels),
                  FadeIn(rails_label, shift=0.2 * UP), run_time=0.45)
        self.play(n_tracker.animate.set_value(1), run_time=0.05)
        n_one_label = Text("N=1", font_size=28, color=PALETTE_SECONDARY)
        n_one_label.to_corner(UR).shift(DOWN * 0.4 + LEFT * 0.2)
        n_one_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        self.play(FadeIn(n_one_label, shift=0.2 * DOWN), run_time=0.4)
        self.wait(1.0)

        # BEAT A2.B1 | 4.50-7.71 s
        n_hud = ValueTracker(1)
        n_hud_text = always_redraw(lambda: Integer(int(n_hud.get_value())).scale(0.6)
                                   .set_color(PALETTE_SECONDARY)
                                   .next_to(Text("N_max = ", font_size=26, color=PALETTE_SECONDARY),
                                            RIGHT, buff=0.1))
        n_hud_label = Text("N_max = ", font_size=26, color=PALETTE_SECONDARY)
        n_hud_label.to_corner(UR).shift(DOWN * 0.4 + LEFT * 0.2)
        n_hud_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        n_hud_group = VGroup(n_hud_label, n_hud_text).move_to(n_hud_label.get_center() + RIGHT * 0.5)

        self.play(FadeOut(n_one_label), FadeIn(n_hud_group), run_time=0.35)
        self.play(n_tracker.animate.set_value(2), run_time=0.4)
        self.play(n_tracker.animate.set_value(3), run_time=0.4)
        self.play(n_tracker.animate.set_value(4), run_time=0.4)
        self.play(n_tracker.animate.set_value(5), run_time=0.4)
        self.play(n_hud.animate.set_value(9), run_time=0.4)
        self.wait(0.65)

        # BEAT A2.B2 | 7.71-10.00 s
        sum_curve_static = axes.plot(
            lambda t: AMP * sum(math.sin((2 * k + 1) * t) / (2 * k + 1) for k in range(9)),
            color=PALETTE_SECONDARY,
            stroke_width=4.0,
        )
        sum_label = Text("S_N(t)", font_size=26, color=PALETTE_SECONDARY)
        sum_label.next_to(axes, DOWN, buff=0.1).align_to(axes, RIGHT).shift(LEFT * 1.6)
        self.play(Create(sum_curve_static), FadeIn(sum_label, shift=0.2 * UP), run_time=0.5)
        self.play(
            sum_curve_static.animate.set_stroke(width=4.5),
            rate_func=there_and_back,
            run_time=0.9,
        )
        residual_bar = Rectangle(width=2.4, height=0.18,
                                 fill_color=PALETTE_ACCENT, fill_opacity=0.7,
                                 stroke_color=PALETTE_ACCENT, stroke_width=1)
        residual_bar.to_edge(DOWN, buff=0.25).shift(LEFT * 3.2)
        residual_label = Text("residual", font_size=20, color=PALETTE_ACCENT)
        residual_label.next_to(residual_bar, LEFT, buff=0.15)
        self.play(FadeIn(residual_bar, shift=0.2 * RIGHT), FadeIn(residual_label), run_time=0.4)
        self.play(residual_bar.animate.stretch_to_fit_width(1.7), run_time=0.5)
        self.wait(0.45)

        # BEAT A3.B1 | 10.00-14.50 s
        old_harm = VGroup(harmonics_active, rail_labels, rails_label)
        n_tracker.set_value(9)
        self.play(n_tracker.animate.set_value(7), run_time=0.8)
        sum_curve_7 = axes.plot(
            lambda t: AMP * sum(math.sin((2 * k + 1) * t) / (2 * k + 1) for k in range(7)),
            color=PALETTE_SECONDARY, stroke_width=4.0)
        self.play(Transform(sum_curve_static, sum_curve_7), run_time=0.5)
        self.play(residual_bar.animate.stretch_to_fit_width(1.3), run_time=0.7)
        self.play(n_tracker.animate.set_value(5), run_time=0.8)
        sum_curve_5 = axes.plot(
            lambda t: AMP * sum(math.sin((2 * k + 1) * t) / (2 * k + 1) for k in range(5)),
            color=PALETTE_SECONDARY, stroke_width=4.0)
        self.play(Transform(sum_curve_static, sum_curve_5), run_time=0.5)
        self.play(residual_bar.animate.stretch_to_fit_width(1.05), run_time=0.6)
        self.wait(0.55)

        # BEAT A3.B2 | 14.50-19.00 s
        for nv in [7, 5, 9]:
            sum_v = axes.plot(
                lambda t, N=nv: AMP * sum(math.sin((2 * k + 1) * t) / (2 * k + 1) for k in range(N)),
                color=PALETTE_SECONDARY, stroke_width=4.0)
            self.play(Transform(sum_curve_static, sum_v), run_time=1.0)
            self.play(n_hud.animate.set_value(nv), run_time=0.4)
        self.play(residual_bar.animate.stretch_to_fit_width(0.95), run_time=0.7)
        self.play(n_hud.animate.set_value(9), run_time=0.4)
        self.wait(0.55)

        # BEAT A4.B1 | 19.00-23.00 s
        hero_eq = MathTex(
            r"f(t) = \frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin\big((2k-1)t\big)}{2k-1}",
            font_size=38, color=PALETTE_ACCENT,
        )
        hero_eq.set_color_by_tex(r"\sum", PALETTE_ACCENT)
        hero_eq.set_color_by_tex(r"\sin", PALETTE_ACCENT)
        hero_eq.add_background_rectangle(color=BLACK, opacity=0.55, buff=0.18)
        hero_eq.move_to(UP * 2.45)
        self.play(FadeOut(rails_label), run_time=0.2)
        self.play(Write(hero_eq), run_time=1.6)
        self.play(sum_curve_static.animate.set_stroke(width=5.0),
                  ref_dashed.animate.set_stroke(width=3.2), run_time=0.7)
        self.wait(0.7)

        # BEAT A4.B2 | 23.00-25.50 s
        gibbs_t = 0.0
        gibbs_x, gibbs_y = axes.c2p(gibbs_t, AMP * 1.08949)
        gibbs_ring = Circle(radius=0.32, color=PALETTE_ACCENT, stroke_width=3)
        gibbs_ring.move_to([gibbs_x, gibbs_y, 0])
        gibbs_text = MathTex(r"\max S_N \approx 1.089\cdot\frac{4}{\pi}",
                             font_size=26, color=PALETTE_ACCENT)
        gibbs_text.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.12)
        gibbs_text.next_to(gibbs_ring, UR, buff=0.18).shift(RIGHT * 0.2)
        self.play(Create(gibbs_ring), Write(gibbs_text), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(gibbs_ring), FadeOut(gibbs_text), run_time=0.5)

        # BEAT A5.B1 | 25.50-27.75 s
        n_tracker.set_value(9)
        self.play(FadeOut(old_harm), run_time=0.5)
        sum_curve_final = axes.plot(
            lambda t: AMP * sum(math.sin((2 * k + 1) * t) / (2 * k + 1) for k in range(9)),
            color=PALETTE_SECONDARY, stroke_width=5.0)
        self.play(Transform(sum_curve_static, sum_curve_final), run_time=0.4)
        self.play(residual_bar.animate.stretch_to_fit_width(0.85), run_time=0.4)
        self.wait(0.85)

        # BEAT A5.B2 | 27.75-30.00 s
        recap_card = MathTex(
            r"\square \;\Leftrightarrow\; \sum_{k\ \mathrm{odd}} \frac{\sin(k t)}{k}",
            font_size=34, color=PALETTE_ACCENT,
        )
        recap_card.set_color_by_tex(r"\square", PALETTE_SECONDARY)
        recap_card.set_color_by_tex(r"\sum", PALETTE_SECONDARY)
        recap_card.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.15)
        recap_card.next_to(axes, DOWN, buff=0.35).align_to(axes, RIGHT).shift(LEFT * 0.4)
        self.play(FadeIn(recap_card, shift=0.25 * UP), run_time=0.6)

        pulse_tracker = ValueTracker(0.0)

        def hero_breath():
            v = pulse_tracker.get_value()
            opa = 0.7 + 0.3 * (0.5 + 0.5 * math.sin(v * 2 * math.pi * 0.5))
            sc = 1.0 + 0.02 * math.sin(v * 2 * math.pi * 0.5)
            hero_eq.set_opacity(opa)
            hero_eq.scale(sc, about_point=hero_eq.get_center())
            return hero_eq

        hero_eq.add_updater(lambda m: None)
        self.play(pulse_tracker.animate.set_value(2.0), run_time=1.55, rate_func=linear)
        self.wait(0.15)