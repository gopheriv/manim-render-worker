from manim import *
import numpy as np
import math

class AetherLabScene(Scene):
    def construct(self):
        g = 9.81
        l_val = 1.0
        th_max = 0.2
        omega = math.sqrt(g / l_val)
        T_val = 2 * math.pi * math.sqrt(l_val / g)
        t = ValueTracker(0.0)
        pivot = np.array([-3.4, 2.6, 0.0])
        rod_len = 2.3

        def bob_point():
            th = th_max * math.cos(omega * t.get_value())
            return pivot + rod_len * np.array([math.sin(th), -math.cos(th), 0.0])

        bar = Rectangle(width=3.2, height=0.18, color=GRAY, fill_opacity=1).move_to(pivot + np.array([0, 0.15, 0]))
        bar.set_z_index(1)
        eq_line = DashedLine(pivot, pivot + np.array([0, -2.7, 0]), color=BLUE, stroke_width=3, stroke_opacity=0.9)
        eq_line.set_z_index(0)
        eq_label = Text("равновесие", font_size=28, color=BLUE_B).scale(0.7)
        eq_label.next_to(pivot + np.array([0, -2.7, 0]), RIGHT, buff=0.15)
        eq_label.set_z_index(3)
        eq_label.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.08)

        def make_pend():
            th = th_max * math.cos(omega * t.get_value())
            end = pivot + rod_len * np.array([math.sin(th), -math.cos(th), 0.0])
            rod = Line(pivot, end, color=WHITE, stroke_width=5)
            rod.set_z_index(2)
            bob = Dot(end, color=YELLOW, radius=0.22)
            bob.set_z_index(2)
            sup = Dot(pivot, color=GRAY, radius=0.07)
            sup.set_z_index(2)
            return VGroup(rod, bob, sup)
        pend = always_redraw(make_pend)

        timer_title = Text("время качания", font_size=28, color=WHITE).scale(0.7)
        timer_title.move_to(RIGHT * 3.2 + UP * 2.9)
        timer_num = DecimalNumber(0.0, num_decimal_places=2, color=YELLOW)
        timer_num.scale(0.9)
        timer_num.next_to(timer_title, DOWN, buff=0.12)
        unit_t = Text("с", font_size=28, color=WHITE).scale(0.7)
        unit_t.next_to(timer_num, RIGHT, buff=0.15)
        timer_grp = VGroup(timer_title, timer_num, unit_t)
        timer_grp.set_z_index(3)

        t0_mark = [0.0]
        def timer_upd(m):
            m.set_value(max(0.0, t.get_value() - t0_mark[0]))
        timer_num.add_updater(timer_upd)

        # BEAT A1 0-4 : balanced composition - pendulum left, timer right from start
        self.play(Create(bar), Create(eq_line), FadeIn(eq_label), FadeIn(pend), FadeIn(timer_grp), t.animate.set_value(3.0), run_time=3.6, rate_func=linear)
        self.wait(0.4)

        # BEAT A2 4-7 : high-contrast amplitude label
        arc = Arc(radius=1.3, start_angle=-math.pi/2 - th_max, angle=2*th_max, arc_center=pivot, color=YELLOW, stroke_width=6)
        arc.set_z_index(2)
        amp_label = Text("амплитуда 0,2 рад", font_size=30, color=YELLOW).scale(0.75)
        amp_label.add_background_rectangle(color=BLACK, opacity=0.85, buff=0.12)
        amp_label.move_to(pivot + np.array([0.0, -1.55, 0.0]))
        amp_label.set_z_index(4)
        self.play(Create(arc), FadeIn(amp_label), t.animate.set_value(5.2), run_time=2.4, rate_func=linear)
        self.wait(0.6)

        # BEAT A2B2 7-10
        small_label = Text("малые колебания", font_size=28, color=WHITE).scale(0.75)
        small_label.move_to(DOWN * 3.1 + LEFT * 2.2)
        small_label.set_z_index(3)
        small_label.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        approx = MathTex(r"\sin\theta \approx \theta", color=WHITE).scale(0.85)
        approx.next_to(small_label, UP, buff=0.15)
        approx.set_z_index(3)
        approx.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        self.play(FadeOut(amp_label), FadeIn(small_label), FadeIn(approx), t.animate.set_value(7.5), run_time=2.4, rate_func=linear)
        self.wait(0.6)

        # BEAT A3B1 10-14 : live period timer readout - reset and count 1.5T
        self.play(FadeOut(arc), FadeOut(approx), run_time=0.6)
        t0_mark[0] = t.get_value()
        self.play(t.animate.set_value(7.5 + T_val * 1.5), run_time=3.0, rate_func=linear)
        self.wait(0.4)

        # BEAT A3B2 14-18 : graph right side, timer stays, no duplicated label
        axes = Axes(x_range=[0, 4.2, 1], y_range=[-0.25, 0.25, 0.2], x_length=4.6, y_length=2.0, axis_config={"stroke_opacity": 0.6}).scale(0.9)
        axes.shift(RIGHT * 2.7 + DOWN * 0.55)
        axes.set_z_index(0)
        xlab = MathTex("t", color=WHITE).scale(0.7).next_to(axes.x_axis, RIGHT, buff=0.12)
        ylab = MathTex(r"\theta", color=WHITE).scale(0.7).next_to(axes.y_axis, UP, buff=0.12)
        ylab.set_z_index(3)
        curve = axes.plot(lambda x: th_max * math.cos(omega * x), x_range=[0, 4.2], color=YELLOW)
        curve.set_z_index(1)
        curve.set_stroke(width=4)
        sine_label = Text("угол идёт синусом", font_size=28, color=YELLOW).scale(0.7)
        sine_label.next_to(axes, UP, buff=0.22)
        sine_label.set_z_index(3)
        sine_label.add_background_rectangle(color=BLACK, opacity=0.85, buff=0.1)
        self.play(FadeOut(small_label), FadeOut(eq_label), FadeOut(eq_line), Create(axes), FadeIn(xlab), FadeIn(ylab), Create(curve), FadeIn(sine_label), run_time=1.2)
        dot_t0 = ValueTracker(0.0)
        live_dot = Dot(color=YELLOW, radius=0.09)
        live_dot.set_z_index(3)
        def dot_upd(m):
            xx = dot_t0.get_value()
            m.move_to(axes.c2p(xx, th_max * math.cos(omega * xx)))
        live_dot.add_updater(dot_upd)
        self.add(live_dot)
        self.play(dot_t0.animate.set_value(4.0), t.animate.set_value(7.5 + T_val * 1.5 + 2.0), run_time=2.4, rate_func=linear)
        self.wait(0.4)
        live_dot.clear_updaters()
        # keep bar + pend + timer, remove graph clutter cleanly
        self.play(FadeOut(axes), FadeOut(curve), FadeOut(xlab), FadeOut(ylab), FadeOut(sine_label), FadeOut(live_dot), run_time=0.6)

        # BEAT A4 18-26 : sequential derivation, no ghosting - one formula at a time
        timer_num.clear_updaters()
        chain_label = Text("вывод периода", font_size=28, color=WHITE).scale(0.75)
        chain_label.to_edge(UP)
        chain_label.set_z_index(3)
        chain_label.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        eq1 = MathTex(r"\ddot{\theta} + \frac{g}{l}\theta = 0", color=WHITE).scale(0.9)
        eq1.move_to(ORIGIN + UP * 1.0)
        eq1.set_z_index(3)
        eq1.add_background_rectangle(color=BLACK, opacity=0.85, buff=0.12)
        self.play(FadeOut(timer_grp), FadeIn(chain_label), FadeIn(eq1), t.animate.set_value(13.0), run_time=1.2, rate_func=linear)
        self.wait(0.5)
        eq2 = MathTex(r"\omega_0 = \sqrt{\frac{g}{l}}", color=WHITE).scale(0.9)
        eq2.move_to(ORIGIN + UP * 1.0)
        eq2.set_z_index(3)
        eq2.add_background_rectangle(color=BLACK, opacity=0.85, buff=0.12)
        self.play(FadeOut(eq1), FadeIn(eq2), t.animate.set_value(14.0), run_time=1.2, rate_func=linear)
        self.wait(0.4)
        eq3 = MathTex(r"T = 2\pi\sqrt{\frac{l}{g}}", color=YELLOW).scale(1.0)
        eq3.move_to(ORIGIN + UP * 1.0)
        eq3.set_z_index(3)
        eq3.add_background_rectangle(color=BLACK, opacity=0.9, buff=0.14)
        self.play(FadeOut(eq2), FadeIn(eq3), t.animate.set_value(15.0), run_time=1.0, rate_func=linear)
        num_label = Text("l = 1 м даёт 2,01 с", font_size=30, color=YELLOW).scale(0.8)
        num_label.next_to(eq3, DOWN, buff=0.35)
        num_label.set_z_index(3)
        num_label.add_background_rectangle(color=BLACK, opacity=0.85, buff=0.1)
        self.play(FadeIn(num_label), Flash(eq3, color=YELLOW), t.animate.set_value(16.0), run_time=1.2, rate_func=linear)
        self.wait(0.8)
        self.play(FadeOut(chain_label), FadeOut(eq3), FadeOut(num_label), run_time=0.5)

        # BEAT A5 26-30 : hero - same bar/pivot retained, no floating string
        hero_formula = MathTex(r"T = 2\pi\sqrt{\frac{l}{g}} = 2.01", color=YELLOW).scale(0.95)
        hero_formula.set_z_index(3)
        hero_formula.add_background_rectangle(color=BLACK, opacity=0.9, buff=0.12)
        hero_sub = Text("малые колебания", font_size=28, color=WHITE).scale(0.75)
        hero_sub.set_z_index(3)
        hero_sub.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        hero_l = Text("l = 1 м", font_size=28, color=YELLOW).scale(0.75)
        hero_l.set_z_index(3)
        hero_l.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        hero_l.next_to(hero_formula, UP, buff=0.25)
        hero_sub.next_to(hero_formula, DOWN, buff=0.25)
        hero_grp = VGroup(hero_l, hero_formula, hero_sub)
        hero_grp.move_to(RIGHT * 2.8 + UP * 0.2)
        self.play(FadeIn(hero_grp), t.animate.set_value(17.5), run_time=0.8, rate_func=linear)
        self.play(Flash(hero_formula, color=YELLOW), Circumscribe(hero_formula, color=YELLOW), t.animate.set_value(18.5), run_time=1.0)
        self.play(t.animate.set_value(21.5), LaggedStart(hero_formula.animate.scale(1.06), hero_formula.animate.scale(1/1.06), lag_ratio=1.0), run_time=1.8, rate_func=linear)
        self.wait(0.4)