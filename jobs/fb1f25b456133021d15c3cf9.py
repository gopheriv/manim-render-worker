from manim import *
import numpy as np
class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        F_tracker = ValueTracker(0.0)
        pulse = ValueTracker(0.0)
        # BEAT A1.B1 | 0.00-4.00 s
        title = Text("Электростатика: два заряда", font_size=32, color=WHITE).to_edge(UP, buff=0.4)
        ruler = Line(LEFT * 3.2 + DOWN * 1.2, RIGHT * 3.2 + DOWN * 1.2, color=GRAY, stroke_width=3)
        ticks = VGroup(*[Line(p + UP * 0.12, p + DOWN * 0.12, color=GRAY, stroke_width=2) for p in [ruler.point_from_proportion(t) for t in np.linspace(0, 1, 9)]])
        c1 = Circle(radius=0.55, color=BLUE, fill_opacity=0.9, stroke_width=3).move_to(LEFT * 2.2 + UP * 0.2)
        c1.set_z_index(2)
        plus1 = Text("+", font_size=48, color=WHITE).move_to(c1.get_center())
        c2 = Circle(radius=0.55, color=RED, fill_opacity=0.9, stroke_width=3).move_to(RIGHT * 2.2 + UP * 0.2)
        c2.set_z_index(2)
        minus2 = Text("−", font_size=48, color=WHITE).move_to(c2.get_center())
        lab1 = Text("q1 = +2 нКл", font_size=30, color=BLUE).next_to(c1, DOWN, buff=0.35)
        lab2 = Text("q2 = −3 нКл", font_size=30, color=RED).next_to(c2, DOWN, buff=0.35)
        charges = VGroup(c1, plus1, c2, minus2, lab1, lab2, ruler, ticks)
        self.play(LaggedStart(FadeIn(title, shift=DOWN * 0.2), FadeIn(c1), FadeIn(plus1), FadeIn(c2), FadeIn(minus2), FadeIn(ruler), FadeIn(ticks), FadeIn(lab1), FadeIn(lab2), lag_ratio=0.12), run_time=2.0)
        self.wait(2.0)
        # BEAT A2.B1 | 4.00-10.00 s
        bracket = DoubleArrow(LEFT * 2.2 + DOWN * 0.55, RIGHT * 2.2 + DOWN * 0.55, color=WHITE, stroke_width=4, buff=0.1)
        # Narrower distance tag (critic: it grazed the charge labels); the tag
        # also leaves with the bracket when the charges shift in A3.B1.
        rlab = Text("r = 0,10 м", font_size=26, color=WHITE).next_to(bracket, DOWN, buff=0.15)
        arr1 = Arrow(c1.get_center() + RIGHT * 0.6, c1.get_center() + RIGHT * 1.7, color=WHITE, stroke_width=8, buff=0)
        arr2 = Arrow(c2.get_center() + LEFT * 0.6, c2.get_center() + LEFT * 1.7, color=WHITE, stroke_width=8, buff=0)
        arr1.set_z_index(3)
        arr2.set_z_index(3)
        qlab = Text("притяжение", font_size=30, color=WHITE).move_to(UP * 1.6)
        self.play(LaggedStart(Create(bracket), FadeIn(rlab, shift=UP * 0.2), Create(arr1), Create(arr2), FadeIn(qlab, shift=DOWN * 0.2), lag_ratio=0.2), run_time=2.2)
        self.wait(3.8)
        # BEAT A3.B1 | 10.00-14.00 s
        # The measurement assembly has served its purpose: fade it inside the
        # existing shift so it can never collide with the moved labels.
        self.play(c1.animate.shift(RIGHT * 0.5), plus1.animate.shift(RIGHT * 0.5), lab1.animate.shift(RIGHT * 0.5), c2.animate.shift(LEFT * 0.5), minus2.animate.shift(LEFT * 0.5), lab2.animate.shift(LEFT * 0.5), arr1.animate.shift(LEFT * 0.15).scale(1.15), arr2.animate.shift(RIGHT * 0.15).scale(1.15), FadeOut(bracket), FadeOut(rlab), run_time=1.8)
        self.play(c1.animate.shift(LEFT * 0.25), plus1.animate.shift(LEFT * 0.25), c2.animate.shift(RIGHT * 0.25), minus2.animate.shift(RIGHT * 0.25), run_time=0.8)
        self.wait(1.4)
        # BEAT A3.B2 | 14.00-18.00 s
        flabel = Text("Модуль силы:", font_size=30, color=WHITE).move_to(DOWN * 2.2 + LEFT * 1.6)
        fnum = DecimalNumber(0.0, num_decimal_places=2, color=WHITE, font_size=42)
        fnum.next_to(flabel, RIGHT, buff=0.25)
        funit = Text("мкН", font_size=30, color=WHITE).next_to(fnum, RIGHT, buff=0.2)
        fnum.add_updater(lambda m: m.set_value(F_tracker.get_value()))
        self.play(FadeIn(flabel), FadeIn(funit), FadeIn(fnum), run_time=0.6)
        self.play(F_tracker.animate.set_value(5.39), run_time=2.6, rate_func=smooth)
        self.wait(0.8)
        # BEAT A4.B1 | 18.00-22.00 s
        fnum.clear_updaters()
        self.play(FadeOut(charges), FadeOut(bracket), FadeOut(rlab), FadeOut(arr1), FadeOut(arr2), FadeOut(qlab), FadeOut(flabel), FadeOut(fnum), FadeOut(funit), FadeOut(title), run_time=0.6)
        # Explicit cdot between k and the fraction (critic: the r^2
        # denominator went missing with the bare k-frac adjacency).
        eq_before = MathTex(r"F = k \cdot \frac{|q_1 q_2|}{r^2}", font_size=52, color=WHITE).move_to(ORIGIN + UP * 0.5)
        lawlab = Text("Закон Кулона", font_size=32, color=WHITE).next_to(eq_before, UP, buff=0.3)
        vallab = Text("k — постоянная, q — заряды, r — расстояние", font_size=28, color=GRAY).next_to(eq_before, DOWN, buff=0.3)
        self.play(FadeIn(lawlab, shift=DOWN * 0.2), Create(eq_before), FadeIn(vallab), run_time=1.6)
        self.wait(1.8)
        # BEAT A4.B2 | 22.00-26.00 s
        eq_after = MathTex(r"|F| = \frac{8.99\times 10^9 \cdot 2\times 10^{-9} \cdot 3\times 10^{-9}}{(0.1)^2} \approx 5.4\times 10^{-6}\, H", font_size=34, color=WHITE).move_to(ORIGIN + UP * 0.3)
        reslab = Text("Подстановка чисел даёт 5,4 мкН", font_size=30, color=WHITE).next_to(eq_after, DOWN, buff=0.35)
        self.play(TransformMatchingTex(eq_before, eq_after), FadeOut(vallab), FadeIn(reslab, shift=UP * 0.2), run_time=1.6)
        self.wait(2.4)
        # BEAT A5.B1 | 26.00-30.00 s
        self.play(FadeOut(eq_before if eq_before in self.mobjects else eq_after), FadeOut(eq_after), FadeOut(lawlab), FadeOut(reslab), run_time=0.5)
        h_eq = MathTex(r"F = k \cdot \frac{|q_1 q_2|}{r^2}", font_size=44, color=WHITE).move_to(UP * 2.4)
        h_c1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.9, stroke_width=3).move_to(LEFT * 2.4 + UP * 0.6)
        h_p = Text("+", font_size=44, color=WHITE).move_to(h_c1.get_center())
        h_c2 = Circle(radius=0.5, color=RED, fill_opacity=0.9, stroke_width=3).move_to(RIGHT * 2.4 + UP * 0.6)
        h_m = Text("−", font_size=44, color=WHITE).move_to(h_c2.get_center())
        h_l1 = Text("q1 = +2 нКл", font_size=30, color=BLUE).next_to(h_c1, DOWN, buff=0.2)
        h_l2 = Text("q2 = −3 нКл", font_size=30, color=RED).next_to(h_c2, DOWN, buff=0.2)
        h_a1 = Arrow(h_c1.get_center() + RIGHT * 0.55, h_c1.get_center() + RIGHT * 1.8, color=YELLOW, stroke_width=10, buff=0)
        h_a2 = Arrow(h_c2.get_center() + LEFT * 0.55, h_c2.get_center() + LEFT * 1.8, color=YELLOW, stroke_width=10, buff=0)
        banner = RoundedRectangle(corner_radius=0.2, width=6.6, height=0.9, color=YELLOW, fill_opacity=0.95, stroke_width=0).move_to(DOWN * 2.2)
        banner.set_z_index(1)
        btext = Text("Притяжение: F≈5,4 мкН, r=0,10 м", font_size=30, color=BLACK).move_to(banner.get_center())
        # The caption used to overrun its banner and clip at the frame edge.
        btext.scale_to_fit_width(banner.width * 0.88)
        btext.set_z_index(2)
        hero = VGroup(h_eq, h_c1, h_p, h_c2, h_m, h_l1, h_l2, h_a1, h_a2, banner, btext)
        hero.scale(0.85)
        hero.move_to(ORIGIN + UP * 0.2)
        self.play(LaggedStart(FadeIn(h_eq, shift=DOWN * 0.2), FadeIn(h_c1), FadeIn(h_p), FadeIn(h_c2), FadeIn(h_m), FadeIn(h_l1), FadeIn(h_l2), Create(h_a1), Create(h_a2), FadeIn(banner), FadeIn(btext), lag_ratio=0.08), run_time=1.5)
        self.play(Flash(h_a1.get_center(), color=YELLOW), Circumscribe(VGroup(h_a1, h_a2), color=YELLOW), run_time=0.8)
        p1 = h_c1.get_center()
        p2 = h_c2.get_center()
        def glow_maker(pt):
            return always_redraw(lambda: Circle(radius=0.72 + 0.08 * np.sin(pulse.get_value() * 4.0), color=YELLOW, stroke_width=6).move_to(pt).set_stroke(opacity=0.25 + 0.25 * np.sin(pulse.get_value() * 4.0)))
        g1 = glow_maker(p1)
        g2 = glow_maker(p2)
        idle_num = DecimalNumber(5.39, num_decimal_places=2, color=YELLOW, font_size=30)
        idle_num.move_to(DOWN * 1.25)
        idle_num.add_updater(lambda m: m.set_value(5.39 + 0.04 * np.sin(pulse.get_value() * 5.0)))
        self.add(g1, g2, idle_num)
        self.play(pulse.animate.set_value(12.56), run_time=1.2, rate_func=linear)
