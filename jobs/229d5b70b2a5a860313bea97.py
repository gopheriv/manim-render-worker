from manim import *
import numpy as np

class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        F_tracker = ValueTracker(0.0)
        pulse = ValueTracker(0.0)

        # BEAT A1 0.00-4.00
        title = Text("Электростатика: два заряда", font_size=32, color=WHITE).to_edge(UP, buff=0.4)
        ruler = Line(LEFT * 3.2 + DOWN * 1.1, RIGHT * 3.2 + DOWN * 1.1, color=GRAY, stroke_width=3)
        ticks = VGroup(*[Line(p + UP * 0.12, p + DOWN * 0.12, color=GRAY, stroke_width=2) for p in [ruler.point_from_proportion(t) for t in np.linspace(0, 1, 9)]])
        c1 = Circle(radius=0.55, color=BLUE, fill_opacity=0.9, stroke_width=3).move_to(LEFT * 2.2 + UP * 0.6)
        c1.set_z_index(2)
        plus1 = Text("+", font_size=48, color=WHITE).move_to(c1.get_center())
        c2 = Circle(radius=0.55, color=RED, fill_opacity=0.9, stroke_width=3).move_to(RIGHT * 2.2 + UP * 0.6)
        c2.set_z_index(2)
        minus2 = Text("−", font_size=48, color=WHITE).move_to(c2.get_center())
        lab1 = Text("q1 = +2 нКл", font_size=26, color=BLUE_E).next_to(c1, DOWN, buff=0.15)
        lab2 = Text("q2 = −3 нКл", font_size=26, color=RED_E).next_to(c2, DOWN, buff=0.15)
        charges = VGroup(c1, plus1, c2, minus2, lab1, lab2, ruler, ticks)
        self.play(LaggedStart(FadeIn(title, shift=DOWN * 0.2), FadeIn(c1), FadeIn(plus1), FadeIn(c2), FadeIn(minus2), FadeIn(ruler), FadeIn(ticks), FadeIn(lab1), FadeIn(lab2), lag_ratio=0.12), run_time=2.0)
        self.wait(2.0)

        # BEAT A2 4.00-10.00 : separated distance label, field lines
        bracket = DoubleArrow(LEFT * 2.2 + DOWN * 1.1, RIGHT * 2.2 + DOWN * 1.1, color=WHITE, stroke_width=4, buff=0.12)
        bracket.set_z_index(3)
        rlab = Text("r = 0,10 м", font_size=28, color=WHITE).next_to(bracket, DOWN, buff=0.18)
        arr1 = Arrow(c1.get_center() + RIGHT * 0.6, c1.get_center() + RIGHT * 1.6, color=WHITE, stroke_width=8, buff=0)
        arr2 = Arrow(c2.get_center() + LEFT * 0.6, c2.get_center() + LEFT * 1.6, color=WHITE, stroke_width=8, buff=0)
        arr1.set_z_index(3)
        arr2.set_z_index(3)
        qlab = Text("притяжение", font_size=30, color=YELLOW).move_to(UP * 1.9)
        field = VGroup(*[DashedLine(LEFT * 1.4 + UP * (0.9 - i * 0.35), RIGHT * 1.4 + UP * (0.9 - i * 0.35), color=GRAY, stroke_width=2, dash_length=0.12) for i in range(3)])
        self.play(LaggedStart(Create(bracket), FadeIn(rlab, shift=UP * 0.2), Create(arr1), Create(arr2), FadeIn(qlab, shift=DOWN * 0.2), Create(field), lag_ratio=0.15), run_time=2.2)
        self.wait(3.8)

        # BEAT A3 EVOLVE 10.00-14.00 : large visible motion
        self.play(
            c1.animate.shift(RIGHT * 1.0), plus1.animate.shift(RIGHT * 1.0), lab1.animate.shift(RIGHT * 1.0),
            c2.animate.shift(LEFT * 1.0), minus2.animate.shift(LEFT * 1.0), lab2.animate.shift(LEFT * 1.0),
            FadeOut(field),
            run_time=1.8
        )
        new_a1 = Arrow(c1.get_center() + RIGHT * 1.0 + RIGHT * 0.6, c1.get_center() + RIGHT * 1.0 + RIGHT * 2.0, color=YELLOW, stroke_width=10, buff=0)
        new_a2 = Arrow(c2.get_center() + LEFT * 1.0 + LEFT * 0.6, c2.get_center() + LEFT * 1.0 + LEFT * 2.0, color=YELLOW, stroke_width=10, buff=0)
        new_a1.set_z_index(3)
        new_a2.set_z_index(3)
        rlab2 = Text("r = 0,06 м", font_size=28, color=YELLOW).move_to(rlab.get_center())
        self.play(Transform(arr1, new_a1), Transform(arr2, new_a2), Transform(rlab, rlab2), Indicate(qlab, color=YELLOW), run_time=1.0)
        self.play(c1.animate.shift(LEFT * 0.2), plus1.animate.shift(LEFT * 0.2), c2.animate.shift(RIGHT * 0.2), minus2.animate.shift(RIGHT * 0.2), run_time=0.6)
        self.wait(1.4)

        # BEAT 14.00-18.00 force number
        flabel = Text("Модуль силы:", font_size=28, color=WHITE).move_to(DOWN * 2.35 + LEFT * 1.7)
        fnum = DecimalNumber(0.0, num_decimal_places=2, color=WHITE, font_size=42)
        fnum.next_to(flabel, RIGHT, buff=0.25)
        funit = Text("мкН", font_size=28, color=WHITE).next_to(fnum, RIGHT, buff=0.2)
        fnum.add_updater(lambda m: m.set_value(F_tracker.get_value()))
        self.play(FadeIn(flabel), FadeIn(funit), FadeIn(fnum), run_time=0.6)
        self.play(F_tracker.animate.set_value(5.39), run_time=2.6, rate_func=smooth)
        self.wait(0.8)

        # BEAT A4.B1 18.00-22.00 Coulomb law + curve
        fnum.clear_updaters()
        self.play(FadeOut(charges), FadeOut(bracket), FadeOut(rlab), FadeOut(arr1), FadeOut(arr2), FadeOut(qlab), FadeOut(flabel), FadeOut(fnum), FadeOut(funit), FadeOut(title), FadeOut(field), run_time=0.6)
        lawlab = Text("Закон Кулона", font_size=32, color=WHITE).move_to(UP * 1.8)
        eq_before = MathTex(r"F = k \frac{|q_1 q_2|}{r^2}", font_size=56, color=WHITE).move_to(UP * 0.7)
        eq_before.set(width=min(eq_before.width, 6.0))
        vallab = Text("k — постоянная, q — заряды, r — расстояние", font_size=24, color=GRAY).next_to(eq_before, DOWN, buff=0.25)
        ax = Axes(x_range=[0.05, 0.2, 0.05], y_range=[0, 20, 10], x_length=4.2, y_length=2.0, axis_config={"stroke_width": 2, "color": GRAY}, tips=False).move_to(DOWN * 1.3)
        ax_labels = VGroup(Text("r", font_size=22, color=GRAY).next_to(ax.x_axis, RIGHT, buff=0.1), Text("F", font_size=22, color=GRAY).next_to(ax.y_axis, UP, buff=0.1))
        curve = ax.plot(lambda x: 0.054 / (x ** 2), x_range=[0.055, 0.2], color=BLUE, stroke_width=4)
        dot = Dot(color=YELLOW, radius=0.08).move_to(ax.c2p(0.1, 5.4))
        dotlab = Text("r=0,10 м → 5,4 мкН", font_size=20, color=YELLOW).next_to(dot, RIGHT, buff=0.15)
        self.play(FadeIn(lawlab, shift=DOWN * 0.2), Create(eq_before), FadeIn(vallab), run_time=1.2)
        self.play(Create(ax), Create(curve), FadeIn(ax_labels), FadeIn(dot), FadeIn(dotlab), Indicate(eq_before, color=YELLOW), Circumscribe(eq_before, color=YELLOW, time_width=0.8), run_time=2.0)
        self.wait(0.6)

        # BEAT A4.B2 22.00-26.00 substitution, two lines to avoid clipping
        eq_top = MathTex(r"|F| = \frac{8.99 \times 10^9 \cdot 6 \times 10^{-18}}{(0.1)^2}", font_size=36, color=WHITE).move_to(UP * 0.55)
        eq_bot = MathTex(r"\approx 5.4 \times 10^{-6}\,\text{N} = 5.4\,\mu\text{N}", font_size=36, color=YELLOW).next_to(eq_top, DOWN, buff=0.2)
        eq_top.set(width=min(eq_top.width, 6.2))
        eq_bot.set(width=min(eq_bot.width, 6.2))
        eq_group = VGroup(eq_top, eq_bot)
        reslab = Text("Подстановка чисел даёт 5,4 мкН", font_size=26, color=WHITE).move_to(DOWN * 2.55)
        self.play(FadeOut(vallab), FadeOut(ax), FadeOut(curve), FadeOut(ax_labels), FadeOut(dot), FadeOut(dotlab), run_time=0.5)
        self.play(Transform(eq_before, eq_top), FadeIn(eq_bot, shift=UP * 0.2), FadeIn(reslab, shift=UP * 0.2), Indicate(eq_bot, color=YELLOW), run_time=2.1)
        self.wait(1.5)

        # BEAT A5 26.00-30.00 hero, banner fitted inside frame
        self.play(FadeOut(eq_before), FadeOut(eq_bot), FadeOut(lawlab), FadeOut(reslab), run_time=0.5)
        h_eq = MathTex(r"F = k \frac{|q_1 q_2|}{r^2}", font_size=44, color=WHITE).move_to(UP * 2.4)
        h_eq.set(width=min(h_eq.width, 5.5))
        h_c1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.9, stroke_width=3).move_to(LEFT * 2.0 + UP * 0.6)
        h_p = Text("+", font_size=44, color=WHITE).move_to(h_c1.get_center())
        h_c2 = Circle(radius=0.5, color=RED, fill_opacity=0.9, stroke_width=3).move_to(RIGHT * 2.0 + UP * 0.6)
        h_m = Text("−", font_size=44, color=WHITE).move_to(h_c2.get_center())
        h_l1 = Text("q1 = +2 нКл", font_size=24, color=BLUE_E).next_to(h_c1, DOWN, buff=0.2)
        h_l2 = Text("q2 = −3 нКл", font_size=24, color=RED_E).next_to(h_c2, DOWN, buff=0.2)
        h_a1 = Arrow(h_c1.get_center() + RIGHT * 0.55, h_c1.get_center() + RIGHT * 1.7, color=YELLOW, stroke_width=10, buff=0)
        h_a2 = Arrow(h_c2.get_center() + LEFT * 0.55, h_c2.get_center() + LEFT * 1.7, color=YELLOW, stroke_width=10, buff=0)
        banner = RoundedRectangle(corner_radius=0.2, width=5.6, height=0.8, color=YELLOW, fill_opacity=0.95, stroke_width=0).move_to(DOWN * 2.2)
        banner.set_z_index(1)
        btext = Text("Притяжение: F≈5,4 мкН, r=0,10 м", font_size=24, color=BLACK).move_to(banner.get_center())
        btext.set(width=min(btext.width, banner.width - 0.5))
        btext.set_z_index(2)
        hero = VGroup(h_eq, h_c1, h_p, h_c2, h_m, h_l1, h_l2, h_a1, h_a2, banner, btext)
        self.play(LaggedStart(FadeIn(h_eq, shift=DOWN * 0.2), FadeIn(h_c1), FadeIn(h_p), FadeIn(h_c2), FadeIn(h_m), FadeIn(h_l1), FadeIn(h_l2), Create(h_a1), Create(h_a2), FadeIn(banner), FadeIn(btext), lag_ratio=0.08), run_time=1.5)
        self.play(Flash(h_a1.get_center(), color=YELLOW), Circumscribe(VGroup(h_a1, h_a2), color=YELLOW), run_time=0.8)
        p1 = h_c1.get_center()
        p2 = h_c2.get_center()

        def glow_maker(pt):
            return always_redraw(lambda: Circle(radius=0.68 + 0.08 * np.sin(pulse.get_value() * 4.0), color=YELLOW, stroke_width=6).move_to(pt).set_stroke(opacity=0.25 + 0.25 * np.sin(pulse.get_value() * 4.0)))

        g1 = glow_maker(p1)
        g2 = glow_maker(p2)
        idle_num = DecimalNumber(5.39, num_decimal_places=2, color=YELLOW, font_size=28)
        idle_num.move_to(DOWN * 1.25)
        idle_num.add_updater(lambda m: m.set_value(5.39 + 0.04 * np.sin(pulse.get_value() * 5.0)))
        self.add(g1, g2, idle_num)
        self.play(pulse.animate.set_value(12.56), run_time=1.2, rate_func=linear)